"""Dizi seslendirme (bolum klasorunun icinden calistirilir: python ../../../motor/ses.py tts): Gemini TTS (grup basina tek istek) -> satirlara bolme -> kontrol -> zaman cizelgesi + efekt/fon.

  GEMINI_API_KEY=... python3 ses.py tts        -> voice/raw_<grup>.wav (var olani yeniden uretmez)
  GEMINI_API_KEY=... python3 ses.py check      -> her satiri yaziya dokup senaryoyla karsilastirir
  python3 ses.py build                         -> voice/voice.wav, voice/mix.wav, voice/final.json
"""
import os, sys, json, base64, re, difflib, urllib.request, urllib.error, io
sys.path.insert(0, os.getcwd())                             # senaryo.py bolum klasorunden (calisma dizini) okunur
import numpy as np, soundfile as sf
from senaryo import SEQ, GROUPS, VOICES, NAMES, LINES, SEG_ALIAS, mix_plan
try:
    from senaryo import VOICE_FX
except ImportError:
    VOICE_FX = {}
try:
    from senaryo import TEMPO
except ImportError:
    TEMPO = {}

MODEL = os.environ.get("TTS_MODEL", "gemini-3.1-flash-tts-preview")   # gunluk ucretsiz kota model basina 10 istek; dolarsa TTS_MODEL=gemini-2.5-flash-preview-tts
API = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent"
SR = 24000


def api(model, body, timeout=240):
    req = urllib.request.Request(API % model, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    import time
    for attempt in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=timeout))
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:600]
            if e.code in (500, 503) and attempt < 3: time.sleep(8 * (attempt + 1)); continue
            raise SystemExit(f"API hatasi {e.code}: {msg}")


def tts(name):
    g = GROUPS[name]; spk = [LINES[i]['spk'] for i in g['ids']]
    kinds = list(dict.fromkeys(spk))
    if len(kinds) == 1:
        text = g['style'] + "\n\n" + "\n\n".join(LINES[i]['text'] for i in g['ids'])
        cfg = {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICES[kinds[0]]}}}
    else:
        text = g['style'] + "\n\n" + "\n".join(f"{NAMES[LINES[i]['spk']]}: {LINES[i]['text']}" for i in g['ids'])
        cfg = {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
            {"speaker": NAMES[k], "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICES[k]}}} for k in kinds]}}
    for attempt in range(3):
        r = api(MODEL, {"contents": [{"parts": [{"text": text}]}], "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": cfg}})
        c = r.get("candidates", [{}])[0]
        if "content" in c: break
        print("ses gelmedi:", name, c.get("finishReason"), str(r.get("promptFeedback", ""))[:200])
    else:
        raise SystemExit(f"TTS ses uretmedi: {name}")
    part = c["content"]["parts"][0]["inlineData"]
    m = re.search(r"rate=(\d+)", part.get("mimeType", "")); sr = int(m.group(1)) if m else SR
    x = np.frombuffer(base64.b64decode(part["data"]), dtype="<i2").astype(np.float32) / 32768.0
    assert sr == SR
    return x


def expected(name):
    """grubun beklenen suresi (sn): hece sayisindan + replik arasi 1 sn"""
    g = GROUPS[name]; tot = 0.0
    for i in g['ids']:
        L = LINES[i]; n = sum(ch in 'aeıioöuüAEIİOÖUÜ' for ch in L['text'])
        tot += (0.33 + 0.174 * n) + 1.0
    return tot


def sanity(name, x):
    """TTS bazen araya dakikalarca sessizlik koyar ya da metni tekrar okur. Uzun sessizlikleri 1 sn'ye indirir;
    sonra sure beklenenin 1.35 katini (+2 sn) gecerse kayit bozuktur (False): metin tekrar okunmus ya da replik atlanmistir.
    Yanlis alarm oldugundan eminsen TTS_KABUL=1 ile kaydet; her durumda 'check' sart."""
    gaps = [g for g in silences(x, 3.0) if g[0] > 0.05 and g[1] < len(x) / SR - 0.05]
    if gaps:
        parts, pos = [], 0
        for a_, b_ in gaps:
            parts.append(x[pos:int((a_ + 0.5) * SR)]); pos = int((b_ - 0.5) * SR)
        parts.append(x[pos:]); x = np.concatenate(parts)
        print(f"UYARI {name}: {len(gaps)} uzun sessizlik 1 sn'ye indirildi")
    return x, os.environ.get('TTS_KABUL') == '1' or len(x) / SR <= 1.35 * expected(name) + 2.0


def silences(x, min_dur=0.12):
    hop = int(SR * 0.01); n = len(x) // hop
    rms = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
    quiet = rms < max(0.010, 0.04 * np.percentile(rms, 95))
    gaps, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            if (j - i) * 0.01 >= min_dur: gaps.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    return gaps


def align(x, texts):
    """Kaydi len(texts) parcaya boler: beklenen sinir karakter oranindan, en yakin (ve uzun) sessizlige oturur."""
    total = len(x) / SR; gaps = silences(x)
    lead = gaps[0][1] if gaps and gaps[0][0] < 0.05 else 0.0
    trail = gaps[-1][0] if gaps and gaps[-1][1] > total - 0.05 else total
    inner = [g for g in gaps if g[0] > lead + 0.05 and g[1] < trail - 0.05]
    if len(texts) == 1: return [(lead, trail)], inner
    mids = np.array([(a + b) / 2 for a, b in inner]); durs = np.array([b - a for a, b in inner])
    vb = np.array([(g[0] - lead) - sum(d for (a2, b2), d in zip(inner, durs) if b2 <= g[0]) for g in inner])
    vt = (trail - lead) - durs.sum()
    w = np.array([len(t) + 6 for t in texts], dtype=float)
    exp = vt * np.cumsum(w)[:-1] / w.sum()
    nb, ng = len(exp), len(inner)
    if ng < nb: raise SystemExit(f"Yeterli duraklama yok ({ng} < {nb})")
    cost = np.abs(vb[None, :] - exp[:, None]) - 2.2 * np.minimum(durs, 0.8)[None, :]
    INF = 1e9; dp = np.full((nb, ng), INF); arg = np.zeros((nb, ng), dtype=int); dp[0] = cost[0]
    for i in range(1, nb):
        best, bj = INF, -1
        for j in range(ng):
            if j >= 1 and dp[i - 1, j - 1] < best: best, bj = dp[i - 1, j - 1], j - 1
            if bj >= 0: dp[i, j] = best + cost[i, j]; arg[i, j] = bj
    j = int(np.argmin(dp[-1])); pick = [j]
    for i in range(nb - 1, 0, -1):
        j = arg[i, j]; pick.append(j)
    pick = pick[::-1]
    cuts = [lead] + [float(mids[j]) for j in pick] + [trail]
    return list(zip(cuts[:-1], cuts[1:])), inner


def trim(s):
    idx = np.where(np.abs(s) > 0.012)[0]
    return s[max(0, idx[0] - int(0.03 * SR)): idx[-1] + int(0.07 * SR)] if len(idx) else s


def refx(s, fx):
    """sesleri birbirinden ayirmak icin: rate>1 daha ince ve hizli (cocuk), <1 daha kalin; intercom: anons hoparloru"""
    if fx.get('rate'):
        n = int(len(s) / fx['rate']); s = np.interp(np.linspace(0, len(s) - 1, n), np.arange(len(s)), s).astype(np.float32)
    if fx.get('intercom'):
        s = highpass(lowpass(s.astype(np.float32), 3000), 380); s = (np.tanh(s * 2.4) / np.tanh(2.4)).astype(np.float32)
        d = int(0.055 * SR); e = np.zeros(len(s) + d, dtype=np.float32); e[:len(s)] += s; e[d:] += 0.3 * s; s = e
    return s


def squeeze(s, maxgap=0.26):
    """cumle ici uzun duraklamalari kisaltir (TTS'in 1 sn'lik nefesleri sureyi sisiriyor)"""
    gaps = [g for g in silences(s, maxgap + 0.06) if g[0] > 0.05 and g[1] < len(s) / SR - 0.05]
    if not gaps: return s
    out, pos, f = [], 0, int(0.006 * SR)
    for a_, b_ in gaps:
        k0 = int((a_ + maxgap / 2) * SR); k1 = int((b_ - maxgap / 2) * SR)
        p = s[pos:k0].copy(); p[-f:] *= np.linspace(1, 0, f); out.append(p); pos = k1
    p = s[pos:].copy(); out.append(p)
    for p in out[1:]: p[:f] *= np.linspace(0, 1, f)
    return np.concatenate(out)


def atempo(s, r):
    """perdeyi degistirmeden hizlandirir (ffmpeg atempo)"""
    if abs(r - 1) < 0.005: return s
    import subprocess, shutil
    ff = shutil.which('ffmpeg')
    if not ff:
        import imageio_ffmpeg; ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.run([ff, '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-filter:a', f'atempo={r}', '-f', 'f32le', '-'],
                       input=s.astype('<f4').tobytes(), capture_output=True)
    if p.returncode: raise SystemExit(p.stderr.decode()[:300])
    return np.frombuffer(p.stdout, dtype='<f4').copy()


def segments(override=None):
    """{line_id: samples}; override: {grup: [kesim zamanlari]} ile elle duzeltme"""
    out = {}
    ov = override or (json.load(open('voice/cuts.json', encoding='utf-8')) if os.path.exists('voice/cuts.json') else {})
    for name, g in GROUPS.items():
        x, sr = sf.read(f'voice/raw_{name}.wav', dtype='float32')
        texts = [LINES[i]['text'] for i in g['ids']]
        if name in ov:
            c = ov[name]; spans = list(zip(c[:-1], c[1:]))
        else:
            spans, _ = align(x, texts)
        for i, (a, b) in zip(g['ids'], spans):
            s = trim(x[int(a * SR):int(b * SR)]).copy()
            s = squeeze(s)
            out[i] = s
        print(name, 'kesimler:', [round(a, 2) for a, _ in spans] + [round(spans[-1][1], 2)])
    for a, b in SEG_ALIAS.items(): out[a] = out[b]
    for i in out:
        if LINES[i]['spk'] in VOICE_FX: out[i] = refx(out[i], VOICE_FX[LINES[i]['spk']])
    for i in out:
        out[i] = atempo(out[i], TEMPO.get(LINES[i]['spk'], TEMPO.get('*', 1.0)))
    return out


def wav_b64(s):
    bio = io.BytesIO(); sf.write(bio, s, SR, format='WAV', subtype='PCM_16'); return base64.b64encode(bio.getvalue()).decode()


def norm(t): return re.sub(r'[^a-zçğıöşü0-9 ]', '', t.lower().replace('İ', 'i').replace('I', 'ı').replace('â', 'a'))


def check(segs, only=None):
    bad = 0
    for name, g in GROUPS.items():
        if only and name not in only: continue
        parts = [{"text": "Asagida numarali ses parcalari var. Her parcayi kelimesi kelimesine Turkce yaziya dok. "
                          "Cikti bicimi: her satir 'Parca N: metin'. Baska hicbir sey yazma."}]
        for k, i in enumerate(g['ids']):
            parts += [{"text": f"Parca {k + 1}:"}, {"inlineData": {"mimeType": "audio/wav", "data": wav_b64(segs[i])}}]
        r = api(os.environ.get("CHECK_MODEL", "gemini-3-flash-preview"), {"contents": [{"parts": parts}]})
        txt = r["candidates"][0]["content"]["parts"][0]["text"]
        got = dict((int(m.group(1)), m.group(2).strip()) for m in re.finditer(r'Par[cç]a\s*(\d+)\s*:\s*(.*)', txt))
        for k, i in enumerate(g['ids']):
            exp = LINES[i]['text']; g_ = got.get(k + 1, '')
            ratio = difflib.SequenceMatcher(None, norm(exp), norm(g_)).ratio()
            flag = 'OK ' if ratio > 0.8 else 'XX '
            bad += ratio <= 0.8
            print(f"{flag}{i:4s} {len(segs[i]) / SR:5.2f}s {ratio:.2f} | {g_}")
    print('SORUNLU SATIR:', bad)


# ---------- zaman cizelgesi ----------
def timeline(segs):
    t = 0.0; lines, beats, scenes, place = [], {}, {}, []
    for it in SEQ:
        if it[0] == 'scene': scenes[it[1]] = round(t, 3)
        elif it[0] == 'beat': beats[it[1]] = (round(t, 3), round(t + it[2], 3)); t += it[2]
        else:
            L = LINES[it[1]]; d = len(segs[L['id']]) / SR
            lines.append(dict(id=L['id'], spk=L['spk'], text=L['text'], hl=L['hl'], start=round(t, 3), end=round(t + d, 3)))
            place.append((t, segs[L['id']])); t += d + L['gap']
    total = t
    buf = np.zeros(int(total * SR) + 1, dtype=np.float32)
    for st, s in place:
        s = s.copy(); f = int(0.008 * SR); s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f)
        s = s / max(1e-6, np.abs(s).max()) * 0.82
        k = int(st * SR); buf[k:k + len(s)] += s
    return dict(total=round(total, 3), lines=lines, beats=beats, scenes=scenes), buf


# ---------- efekt ve fon ----------
RNG = np.random.default_rng(7)

def lowpass(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / (1 + (f / fc) ** 4); return np.fft.irfft(X, len(x)).astype(np.float32)
def highpass(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 - 1 / (1 + (f / fc) ** 4); return np.fft.irfft(X, len(x)).astype(np.float32)
def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a, r):
    n = int(d * SR); e = np.ones(n, dtype=np.float32); na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na) ** 1.5; e[n - nr:] = np.linspace(1, 0, nr) ** 1.5; return e
def put(buf, x, t, g=1.0):
    k = int(t * SR); n = min(len(x), len(buf) - k)
    if n > 0: buf[k:k + n] += x[:n] * g

def hum(d):
    t = tt(d); x = (np.sin(2 * np.pi * 55 * t) + 0.6 * np.sin(2 * np.pi * 82.5 * t) + 0.35 * np.sin(2 * np.pi * 110.4 * t)) * (0.75 + 0.25 * np.sin(2 * np.pi * 3.2 * t))
    return (x * env(d, 0.4, 0.5)).astype(np.float32) * 0.5
def rumble(d):
    n = int(d * SR); x = lowpass(np.cumsum(RNG.standard_normal(n)).astype(np.float32) * 0.02, 120)
    x = highpass(x, 28); x /= max(1e-6, np.abs(x).max())
    t = tt(d); e = np.minimum(1, t / 0.25) * np.exp(-np.maximum(0, t - 1.2) * 1.6)
    y = x * e
    for k in range(9):                                   # dusen parcalar: kisa tok vuruslar
        st = 0.3 + k * 0.17 + RNG.uniform(-0.04, 0.04); dd = 0.22; th = tt(dd)
        hit = np.sin(2 * np.pi * (70 + 30 * RNG.random()) * th) * np.exp(-th * 22) * (1 - k / 12)
        put(y, hit.astype(np.float32), st, 0.7)
    return y.astype(np.float32)
def snap():
    t = tt(0.35); x = highpass(RNG.standard_normal(len(t)).astype(np.float32), 1500) * np.exp(-t * 60) * 0.8
    x += np.sin(2 * np.pi * (900 * np.exp(-t * 9)) * t) * np.exp(-t * 14) * 0.5
    return x.astype(np.float32)
def tick(f=1900):
    t = tt(0.06); return (np.sin(2 * np.pi * f * t) * np.exp(-t * 90) + 0.4 * np.sin(2 * np.pi * f * 2.7 * t) * np.exp(-t * 140)).astype(np.float32)
def whoosh(d, up=True):
    n = int(d * SR); t = tt(d); x = RNG.standard_normal(n).astype(np.float32)
    out = np.zeros(n, dtype=np.float32); nb = 24; seg = n // nb
    for b in range(nb):                                  # merkez frekansi kayan bant
        u = b / (nb - 1); fc = 300 * (8 ** (u if up else 1 - u))
        s = x[b * seg:(b + 1) * seg]
        out[b * seg:(b + 1) * seg] = lowpass(highpass(np.pad(s, 256), fc * 0.7), fc * 1.4)[256:256 + len(s)]
    gl = np.sin(2 * np.pi * np.cumsum(180 * (4 ** (t / d if up else 1 - t / d))) / SR) * 0.25
    return ((out / max(1e-6, np.abs(out).max()) * 0.6 + gl) * env(d, d * 0.35, d * 0.3)).astype(np.float32)
def chime(freqs, d=2.4):
    t = tt(d); x = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (1.6 + i * 0.5)) / (1 + i * 0.4) for i, f in enumerate(freqs))
    return (x * np.minimum(1, t / 0.01)).astype(np.float32) * 0.35
def pad(d, freqs):
    t = tt(d); x = np.zeros(len(t))
    for i, f in enumerate(freqs):
        lfo = 0.6 + 0.4 * np.sin(2 * np.pi * (0.07 + 0.023 * i) * t + i * 1.7)
        x += (np.sin(2 * np.pi * f * t + 0.6 * np.sin(2 * np.pi * 0.19 * t + i)) + 0.5 * np.sin(2 * np.pi * f * 1.004 * t)) * lfo / (1 + i * 0.25)
    return (x / len(freqs)).astype(np.float32)

def buzz(d=0.2):
    t = tt(d); x = np.sign(np.sin(2 * np.pi * 100 * t)) * 0.5 + 0.5 * np.sin(2 * np.pi * 50 * t)
    x = lowpass(x.astype(np.float32), 1800) * (0.6 + 0.4 * RNG.random(len(t)))
    return (x * env(d, 0.01, min(0.06, d / 3))).astype(np.float32) * 0.45
def ding():
    t = tt(1.8); x = np.sin(2 * np.pi * 1318.5 * t) * np.exp(-t * 3.0) + 0.6 * np.sin(2 * np.pi * 1046.5 * (t - 0.28).clip(0)) * np.exp(-(t - 0.28).clip(0) * 3.0) * (t > 0.28)
    return (x * np.minimum(1, t / 0.005)).astype(np.float32) * 0.4
def slide(d=1.4):
    n = int(d * SR); x = lowpass(highpass(RNG.standard_normal(n).astype(np.float32), 180), 900)
    x /= max(1e-6, np.abs(x).max()); t = tt(d)
    return (x * env(d, 0.15, 0.25) * 0.5 + 0.25 * np.sin(2 * np.pi * 62 * t) * env(d, 0.1, 0.2)).astype(np.float32)
def steps(d=3.0, rate=1.5):
    y = np.zeros(int(d * SR) + 1, dtype=np.float32); th = tt(0.25); k = 0; t0 = 0.0
    while t0 < d - 0.25:
        hit = np.sin(2 * np.pi * (58 + 10 * (k % 2)) * th) * np.exp(-th * 26) + 0.25 * lowpass(RNG.standard_normal(len(th)).astype(np.float32), 400) * np.exp(-th * 40)
        put(y, hit.astype(np.float32), t0, 0.5 + 0.5 * min(1, t0 / max(0.5, d * 0.7))); t0 += 1.0 / rate; k += 1
    return y
def ring(d=2.0):
    t = tt(d); trill = np.where(np.sin(2 * np.pi * 22 * t) > 0, 1480.0, 1760.0)
    x = np.sin(2 * np.pi * np.cumsum(trill) / SR); gate = ((t % 1.0) < 0.55).astype(np.float32)
    g = lowpass(gate, 40)
    return (lowpass(x.astype(np.float32), 2600) * g * env(d, 0.02, 0.1)).astype(np.float32) * 0.3

# komedi efektleri (Kiraci Uzayli): boing (yay), pop (balon), sniff (Hugo kokluyor), munch (Tobi yiyor), zip (uzayli antenleri),
# knock (kapi vurusu), whistle_up / whistle_down (kayan duduk: kalkma, dusme)
def boing(d=0.7):
    t = tt(d); f = 180 + 260 * np.exp(-t * 5) * (1 + 0.35 * np.sin(2 * np.pi * 14 * t))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5) * np.minimum(1, t / 0.004)).astype(np.float32) * 0.5
def pop():
    t = tt(0.12); return (np.sin(2 * np.pi * (700 * np.exp(-t * 30) + 200) * t) * np.exp(-t * 50) + 0.3 * highpass(RNG.standard_normal(len(t)).astype(np.float32), 2000) * np.exp(-t * 80)).astype(np.float32) * 0.6
def sniff(n=3):
    y = np.zeros(int((0.2 * n + 0.3) * SR), dtype=np.float32); th = tt(0.16)
    for k in range(n):
        x = lowpass(highpass(RNG.standard_normal(len(th)).astype(np.float32), 900), 4200) * np.sin(np.pi * np.arange(len(th)) / len(th)) ** 2
        put(y, x * 0.5, k * 0.2)
    return y
def munch(n=4):
    y = np.zeros(int((0.24 * n + 0.3) * SR), dtype=np.float32); th = tt(0.12)
    for k in range(n):
        x = lowpass(RNG.standard_normal(len(th)).astype(np.float32), 2400) * np.exp(-th * 30) + 0.4 * np.sin(2 * np.pi * 90 * th) * np.exp(-th * 25)
        put(y, x.astype(np.float32) * 0.6, k * 0.24 + RNG.uniform(0, 0.03))
    return y
def zip_(d=0.5):
    t = tt(d); f = 900 + 1600 * (t / d); return (np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * 30 * t)) * env(d, 0.02, 0.1)).astype(np.float32) * 0.25
def knock(n=3):
    y = np.zeros(int((0.26 * n + 0.3) * SR), dtype=np.float32); th = tt(0.18)
    for k in range(n):
        x = np.sin(2 * np.pi * 120 * th) * np.exp(-th * 35) + 0.5 * lowpass(RNG.standard_normal(len(th)).astype(np.float32), 1200) * np.exp(-th * 60)
        put(y, x.astype(np.float32) * 0.7, k * 0.26)
    return y
def whistle_up(d=0.6):
    t = tt(d); f = 600 * 3 ** (t / d); return (np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, 0.03, 0.08)).astype(np.float32) * 0.3
def whistle_down(d=0.8):
    t = tt(d); f = 1800 / 3 ** (t / d); return (np.sin(2 * np.pi * np.cumsum(f) / SR) * env(d, 0.03, 0.1)).astype(np.float32) * 0.3

FX = dict(hum=hum, rumble=rumble, snap=snap, tick=tick, whoosh=whoosh, chime=chime, buzz=buzz, ding=ding, slide=slide, steps=steps, ring=ring,
          boing=boing, pop=pop, sniff=sniff, munch=munch, zip=zip_, knock=knock, whistle_up=whistle_up, whistle_down=whistle_down)


# ---------- muzik: gerilim (minor, seyrek piyano + uzak muzik kutusu) / sicak (major, muzik kutusu melodisi + yumusak piyano) ----------
# mix_plan(T) donusune 'music': [(bas, bit, mod, kazanc)] eklenirse calar. mod: 'gerilim' | 'sicak' | 'gizem' | 'komik' | 'sinsi'.
# Ayni anda pads de calabilir ama ton catisir: muzik kullanan bolumde pads'i bos birak ya da ayni tonda tut (gerilim D minor, sicak F major).
def _note(f, d, partials, decay, attack=0.004):
    t = tt(d); x = np.zeros(len(t))
    for k, (m, a, dk) in enumerate(partials):
        x += a * np.sin(2 * np.pi * f * m * t + k) * np.exp(-t * decay * dk)
    return (x * np.minimum(1, t / attack)).astype(np.float32)
def piano(f, d=2.6, vel=1.0):
    """yumusak piyano: hafif inharmonik kismi tonlar, hizli atak, uzun sonum"""
    x = _note(f, d, [(1, 1.0, 1.0), (2.003, 0.42, 1.6), (3.009, 0.20, 2.4), (4.02, 0.10, 3.2), (5.03, 0.05, 4.0)], 1.25)
    return lowpass(x, 2600) * 0.32 * vel
def musicbox(f, d=1.8, vel=1.0):
    """muzik kutusu: cana benzer, 4. ve 7. kismi tonlar cabuk soner"""
    return _note(f, d, [(1, 1.0, 1.0), (4.0, 0.34, 3.5), (6.98, 0.12, 5.0), (2.0, 0.18, 2.0)], 2.3, 0.002) * 0.22 * vel
def drone(d, root):
    t = tt(d); lfo = 0.75 + 0.25 * np.sin(2 * np.pi * 0.08 * t)
    x = (np.sin(2 * np.pi * root * t) + 0.55 * np.sin(2 * np.pi * root * 1.5 * t + 1) + 0.3 * np.sin(2 * np.pi * root * 2.003 * t)) * lfo
    n = lowpass(RNG.standard_normal(len(t)).astype(np.float32), 180) * 2.5
    return ((x * 0.22 + n * 0.08) * env(d, min(1.5, d / 3), min(1.5, d / 3))).astype(np.float32)

def hz(midi): return 440.0 * 2 ** ((midi - 69) / 12)
DMIN = [62, 64, 65, 67, 69, 70, 72, 74]                      # D minor (D4..D5)
FMAJ_M = [65, 67, 69, 70, 72, 74, 76, 77]                    # F major (F4..F5)
# sicak melodi: (derece, vurus) 8 olcu, 3/4 hissi; dereceler FMAJ_M icinde
MEL = [(0, 1), (2, 1), (4, 1), (5, 2), (4, 1), (2, 1), (1, 1), (2, 2), (0, 1), (2, 1), (4, 1), (7, 2), (5, 1), (4, 1), (2, 1), (4, 3),
       (5, 1), (4, 1), (2, 1), (1, 2), (2, 1), (0, 1), (1, 1), (2, 2), (4, 1), (2, 1), (1, 1), (0, 3)]
CHORDS_F = [(53, 57, 60), (48, 52, 55), (50, 53, 57), (46, 50, 53)]   # F, C, Dm, Bb
# komedi (Kiraci Uzayli, 26 Kasim 2026): komik (C major, hoplayan bas + pizzicato melodi) ve sinsi (D minor, parmak ucu pizzicato:
# saklanma, gizlice yurume, Hugo'nun koklamasi)
def pluck(f, d=0.36, vel=1.0):
    return lowpass(_note(f, d, [(1, 1.0, 1.0), (2.0, 0.45, 1.8), (3.0, 0.2, 2.6)], 9.0, 0.002), 3200) * 0.34 * vel
def bassn(f, d=0.32, vel=1.0):
    return lowpass(_note(f, d, [(1, 1.0, 1.0), (2.0, 0.35, 2.0), (3.0, 0.12, 3.0)], 7.0, 0.003), 900) * 0.55 * vel
CMAJ = [60, 62, 64, 65, 67, 69, 71, 72, 74]
KOMIK_MEL = [4, -1, 4, 5, 4, -1, 2, -1, 0, 2, 4, -1, 5, -1, 4, -1, 7, -1, 5, 4, 2, -1, 4, -1, 2, 1, 0, -1, 1, -1, 0, -1]
KOMIK_BAS = [(48, 55), (53, 60), (55, 50), (48, 55)]           # C, F, G, C: kok + besli
def music_bed(a, b, mode, seed=0):
    d = b - a; out = np.zeros(int(d * SR) + SR * 3, dtype=np.float32); R = np.random.default_rng(seed)
    if mode == 'gerilim':
        put(out, drone(d + 1.0, hz(38)), 0, 1.0)              # D2
        t = R.uniform(0.4, 1.4)
        while t < d - 0.5:                                    # seyrek piyano tek notalari (minor)
            m = DMIN[int(R.integers(0, len(DMIN)))] - (12 if R.random() < 0.35 else 0)
            put(out, piano(hz(m), 3.0, R.uniform(0.6, 1.0)), t); t += R.uniform(1.6, 2.9)
        t = R.uniform(2.0, 4.0)
        while t < d - 0.5:                                    # uzaktan muzik kutusu harmonigi
            put(out, musicbox(hz(DMIN[int(R.integers(3, 8))] + 12), 2.2, 0.45), t); t += R.uniform(4.5, 7.5)
    elif mode == 'gizem':
        put(out, drone(d + 1.0, hz(38)) * 0.7, 0, 1.0)
        beat = 0.62; t = 0.3; i = 0
        seq = [7, 5, 4, 2, 4, 5, 4, 0]
        while t < d - 0.4:
            put(out, musicbox(hz(DMIN[seq[i % len(seq)]] + 12), 2.0, 0.8), t); t += beat * (2 if i % 4 == 3 else 1); i += 1
    elif mode == 'komik':
        beat = 0.30; t = 0.1; i = 0
        while t < d - 0.3:
            bar = (i // 8) % 4; r, f5 = KOMIK_BAS[bar]
            if i % 4 == 0: put(out, bassn(hz(r - 12), vel=0.8), t)     # um
            elif i % 4 == 2: put(out, bassn(hz(f5 - 12), vel=0.65), t) # pa
            if i % 4 in (1, 3): put(out, pluck(hz(r + 12), 0.2, 0.35), t)
            m = KOMIK_MEL[i % len(KOMIK_MEL)]
            if m >= 0: put(out, pluck(hz(CMAJ[m] + 12), 0.36, 0.6 + 0.15 * R.random()), t)
            t += beat; i += 1
    elif mode == 'sinsi':
        beat = 0.34; t = 0.1; i = 0
        walk = [50, 49, 48, 47, 46, 45, 46, 47]                        # D'den inen kromatik parmak ucu
        while t < d - 0.3:
            put(out, pluck(hz(walk[(i // 2) % len(walk)]), 0.3, 0.9), t)
            if i % 2 == 1: put(out, pluck(hz(walk[(i // 2) % len(walk)] + 7), 0.25, 0.5), t)
            if i % 16 == 12: put(out, musicbox(hz(DMIN[int(R.integers(4, 8))] + 12), 1.6, 0.5), t)
            t += beat; i += 1
    else:                                                     # sicak
        beat = 0.70; t = 0.25; i = 0; bar = 0
        while t < d - 0.4:
            deg, n = MEL[i % len(MEL)]
            put(out, musicbox(hz(FMAJ_M[deg] + 12), 2.0, 0.9), t)
            if i % 4 == 0:                                    # her olcu basinda yumusak piyano akoru
                for m in CHORDS_F[bar % 4]: put(out, piano(hz(m), 3.2, 0.5), t)
                bar += 1
            t += beat * n; i += 1
    e = np.ones(len(out), dtype=np.float32); f = int(0.8 * SR)
    e[:f] = np.linspace(0, 1, f); k = int(d * SR); e[k:] = 0; e[max(0, k - f):k] *= np.linspace(1, 0, k - max(0, k - f))
    return out * e


def mix(T, voice):
    """senaryo.mix_plan(T) -> dict(pads=[(bas, bit, frekanslar, kazanc)], fx=[(ad, zaman, kazanc, kwargs)])"""
    P = mix_plan(T)
    fx = np.zeros(len(voice), dtype=np.float32); pd = np.zeros(len(voice), dtype=np.float32)
    for a, b, fr, g in P['pads']:
        d = b - a + 1.2; put(pd, pad(d, fr) * env(d, 1.0, 1.2), max(0, a - 0.6), g)
    for name, t, g, kw in P['fx']:
        if kw.get('d', 1) <= 0.05: continue
        put(fx, FX[name](**kw), max(0, t), g)
    mu = np.zeros(len(voice), dtype=np.float32)
    for j, (a, b, mode, g) in enumerate(P.get('music', [])):
        put(mu, music_bed(a, b, mode, seed=j + 1), max(0, a), g)
    if np.abs(mu).max() > 0:                                  # konusma varken muzik kisilir (ducking)
        ev = lowpass(np.abs(voice).astype(np.float32), 3.0); ev = np.clip(ev / (np.percentile(ev, 95) + 1e-6), 0, 1)
        mu = mu * (1 - 0.5 * ev)
    out = voice + fx * 0.42 + pd * 0.085 + mu * 0.30
    return out / max(1e-6, np.abs(out).max()) * 0.93


if __name__ == "__main__":
    os.makedirs("voice", exist_ok=True)
    cmd = sys.argv[1]
    if cmd == "tts":
        for name in (sys.argv[2:] or GROUPS):
            f = f"voice/raw_{name}.wav"
            if os.path.exists(f) and len(sys.argv) < 3: print("var:", f); continue
            x = tts(name); x, ok = sanity(name, x)
            if ok: sf.write(f, x, SR); print("uretildi:", name, round(len(x) / SR, 1), "sn")
            else:
                sf.write(f"voice/bozuk_{name}.wav", x, SR)
                print(f"BOZUK KAYIT: {name} ({round(len(x) / SR, 1)} sn, beklenen ~{round(expected(name), 1)} sn). raw_{name}.wav YAZILMADI. "
                      f"Grubu ikiye bol (ozellikle anlatici: en fazla 4 paragraf) ve yalnizca o grubu yeniden uret.")
    elif cmd == "gaps":
        for name in (sys.argv[2:] or GROUPS):
            x, _ = sf.read(f"voice/raw_{name}.wav", dtype="float32")
            print(name, round(len(x) / SR, 2), [(round(a, 2), round(b, 2)) for a, b in silences(x, 0.2)])
    elif cmd == "check":
        check(segments(), sys.argv[2:])
    elif cmd == "dry":
        # SES OLMADAN taslak zaman cizelgesi: gorsel calisma ve kare kontrolu icin. Gercek ses gelince 'build' ustune yazar.
        segs = {}
        for i, L in LINES.items():
            n = sum(ch in 'aeıioöuüAEIİOÖUÜ' for ch in L['text']); d = (0.33 + 0.174 * n) / VOICE_FX.get(L['spk'], {}).get('rate', 1.0)
            t = tt(d); segs[i] = (0.05 * np.sin(2 * np.pi * 180 * t) * (0.55 + 0.45 * np.sin(2 * np.pi * 4.5 * t))).astype(np.float32)
        T, voice = timeline(segs); T['dry'] = True
        sf.write("voice/voice.wav", voice, SR); sf.write("voice/mix.wav", voice * 0, SR)
        json.dump(T, open("voice/final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("TASLAK toplam", T['total'], "sn | sahneler", T['scenes'])
    elif cmd == "build":
        segs = segments(); T, voice = timeline(segs)
        sf.write("voice/voice.wav", voice, SR)
        sf.write("voice/mix.wav", mix(T, voice), SR)
        json.dump(T, open("voice/final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("toplam", T['total'], "sn | sahneler", T['scenes'])
