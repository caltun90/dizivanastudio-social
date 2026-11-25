"""kopru.py: the bridge from the episode's voice (motor/ses.py) to the 3D engine's story folder.

  python3 yumurta/tools/kopru.py diziler/<dizi>/bNN yumurta/stories/<dizi>-bNN [--fps 30]

Reads   diziler/<dizi>/bNN/voice/final.json, voice.wav, mix.wav   (written by `ses.py build` or `ses.py dry`)
Writes  yumurta/stories/<dizi>-bNN/voice/timeline.json   lines (id, spk, text, hl, start, end), beats, scenes, total
        yumurta/stories/<dizi>-bNN/voice/words.json      every word with its time, speaker and emphasis (captions)
        yumurta/stories/<dizi>-bNN/voice/env.json        mouth envelope per speaker, one value per frame: {"L": [...], "T": [...]}
        yumurta/stories/<dizi>-bNN/audio/mix.m4a         the finished sound (voice + music + effects), muxed by the renderer
Run it again after every `ses.py build`; story.js reads the times from these files, never typed by hand.
"""
import sys, os, re, json, subprocess
import numpy as np

src, dst = sys.argv[1], sys.argv[2]
fps = int(sys.argv[sys.argv.index('--fps') + 1]) if '--fps' in sys.argv else 30
V = os.path.join(src, 'voice')
T = json.load(open(os.path.join(V, 'final.json'), encoding='utf-8'))
os.makedirs(os.path.join(dst, 'voice'), exist_ok=True); os.makedirs(os.path.join(dst, 'audio'), exist_ok=True)

# --- timeline (as it is) ---
json.dump(T, open(os.path.join(dst, 'voice', 'timeline.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# --- words: spread each line over its own time, weighted by syllables ---
VOW = 'aeıioöuüâîûAEIİOÖUÜÂÎÛ'
norm = lambda w: re.sub(r'[^\w]', '', w.replace('I', 'ı').replace('İ', 'i').lower())
words = []
for L in T['lines']:
    ws = L['text'].split()
    if not ws: continue
    hl = {norm(h) for h in L.get('hl', [])}
    wt = np.array([max(1, sum(ch in VOW for ch in w)) + .4 for w in ws]); cs = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
    a, b = L['start'], L['end']
    for j, w in enumerate(ws):
        words.append({'word': w, 'start': round(a + cs[j] * (b - a), 3), 'end': round(a + cs[j + 1] * (b - a), 3),
                      'spk': L['spk'], 'line': L['id'], 'hl': norm(w) in hl})
json.dump({'words': words, 'duration': T['total']}, open(os.path.join(dst, 'voice', 'words.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

# --- mouth envelope per speaker ---
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(V, 'voice.wav'), '-ac', '1', '-ar', '24000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32); hop = 24000 // fps; n = max(len(x) // hop, int(T['total'] * fps) + 1)
x = np.pad(x, (0, max(0, n * hop - len(x))))
rms = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(axis=1))
ref = np.percentile(rms[rms > 1e-4], 95) if (rms > 1e-4).any() else 1
e = np.convolve(np.clip(rms / ref, 0, 1), [.25, .5, .25], mode='same')
env = {'*': [round(float(v), 3) for v in e]}
for spk in sorted({L['spk'] for L in T['lines']}):
    m = np.zeros(n)
    for L in T['lines']:
        if L['spk'] == spk: m[max(0, int(L['start'] * fps) - 1): int(L['end'] * fps) + 2] = 1
    env[spk] = [round(float(v), 3) for v in e * m]
json.dump(env, open(os.path.join(dst, 'voice', 'env.json'), 'w'))

# --- the finished sound ---
mix = os.path.join(V, 'mix.wav')
if os.path.exists(mix):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mix, '-c:a', 'aac', '-b:a', '192k', os.path.join(dst, 'audio', 'mix.m4a')], check=True)
print(f"kopru: {len(T['lines'])} replik, {len(words)} kelime, {T['total']} sn{' (TASLAK ses)' if T.get('dry') else ''} -> {dst}")
