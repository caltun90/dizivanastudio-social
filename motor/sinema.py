"""Sinema katmani: kamera (yavas yakinlasma / uzaklasma, hafif yana kayma), isik (huzme, parlama, vinyet),
renk ayari, film greni, temas golgesi ve yeni altyazi. Diziden bagimsizdir; ortak.run() her karede kullanir.

Acma/kapama: SINEMA=0 ortam degiskeni eski gorunumu aynen verir.
Sahne bazinda ayar: bolum.py icinde  SINE = {sahne_no: dict(cam='sabit'|'genis'|'oto', mood='sicak'|'soguk'|'gece'|'kirmizi'|'sepya'|None,
                                               rays=True, zmax=1.3)}  ve run(DRAW, sine=SINE)
"""
import math, os
import numpy as np, skia
import orgu
from orgu import W, H, FMT, clamp, seg, smooth, lerp, fill, stroke, TFB, CREAM, INKBLUE

ON = os.environ.get('SINEMA', '1') != '0'
LIN = skia.SamplingOptions(skia.FilterMode.kLinear)
SHOT = 3.8                     # ortalama plan suresi (sn)

# ---------- konusan karakterin ekrandaki yeri (actor() her karede bildirir) ----------
_POS = {}                      # kim -> (ekran_x, ekran_y, ekran_bas_yaricapi)
def note(cv, f, who):
    if not ON: return
    m = cv.getTotalMatrix(); hx, hy = f['head']; p = m.mapXY(hx, hy); r = f['HR'] * m.getScaleX()
    _POS[who] = (p.x(), p.y(), r)


def contact_shadow(cv, x, gy, s, alpha=1.0):
    """ayak altinda yumusak temas golgesi (sahne koordinatinda, figure'dan once cizilir)"""
    if not ON or alpha <= 0.02: return
    p = fill((4, 6, 18), 120 * alpha); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18 * s + 4))
    cv.drawOval(skia.Rect.MakeLTRB(x - 175 * s, gy - 22 * s, x + 175 * s, gy + 26 * s), p)


# ---------- kamera ----------
class Camera:
    def __init__(s): s.scene_light = {}

    def shots(s, a, b):
        n = max(1, round((b - a) / SHOT)); return [a + (b - a) * i / n for i in range(n + 1)]

    def plan(s, k, i_scene, a, b, t, who, opt):
        """(zoom, merkez_x, merkez_y) ekran koordinatinda.
        Kamera SAKIN: yalnizca yavas yakinlasma / uzaklasma ve hafif yana kayma (Cem, 19 Kasim 2026). Konusani izlemez,
        sahne icinde sicrama yapmaz: planlar birbirine kesintisiz baglanir (yakinlas -> uzaklas -> yakinlas ...)."""
        mode = opt.get('cam', 'oto'); zmax = opt.get('zmax', 1.32)
        cx, cy = W / 2, H / 2
        if mode == 'sabit': return 1.0, cx, cy
        sh = s.shots(a, b); j = max(0, min(len(sh) - 2, sum(1 for x in sh[1:-1] if t >= x)))
        u = smooth(seg(t, sh[j], sh[j + 1]))
        z0, z1 = (1.09, 1.17) if FMT == 'v' else (1.04, 1.10)    # dikeyde alt bos ucte bir kirpilir
        z1 = max(z0, min(z1, zmax))
        d = (20 if FMT == 'v' else 30) * (1 if k % 2 else -1)       # yana kayma: en fazla bu kadar piksel
        if (j + i_scene) % 2 == 0: z, x = lerp(z0, z1, u), cx + d * lerp(-1, 1, u)
        else: z, x = lerp(z1, z0, u), cx + d * lerp(1, -1, u)
        if i_scene == 0: z *= lerp(1.13, 1.0, smooth(seg(t, 0, 0.9)))   # ilk saniye: kanca icin hizli hareket
        return z, x, cy - (60 if FMT == 'v' else 0)

    @staticmethod
    def apply(cv, z, x, y):
        """z: yakinlasma, (x, y): kadrajin ortasina gelecek ekran noktasi. Kenar disari tasmaz."""
        hw, hh = W / (2 * z), H / (2 * z)
        x = clamp(x, hw, W - hw); y = clamp(y, hh, H - hh)
        cv.translate(W / 2, H / 2); cv.scale(z, z); cv.translate(-x, -y)


CAM = Camera()


# ---------- isik ----------
def find_light(img):
    """sahnenin en parlak bolgesi (ust yarida): huzmenin kaynagi"""
    a = img.resize(W // 16, H // 16).toarray()[..., :3].astype(np.float32) if hasattr(img, 'resize') else None
    if a is None:
        small = skia.Surface(W // 16, H // 16); c = small.getCanvas()
        c.drawImageRect(img, skia.Rect.MakeWH(W // 16, H // 16), LIN); a = small.makeImageSnapshot().toarray()[..., :3].astype(np.float32)
    lum = a @ np.array([0.3, 0.59, 0.11], np.float32)
    top = lum[: int(lum.shape[0] * 0.55)]
    yy, xx = np.unravel_index(np.argmax(top), top.shape)
    return (xx + 0.5) * 16, (yy + 0.5) * 16, float(top.max()), float(lum.mean())


MOODS = {
    None:      dict(tint=(255, 226, 180), shade=(30, 40, 90), sat=1.10, con=1.07),
    'sicak':   dict(tint=(255, 204, 140), shade=(60, 34, 60), sat=1.12, con=1.08),
    'soguk':   dict(tint=(190, 220, 255), shade=(14, 30, 70), sat=1.04, con=1.08),
    'gece':    dict(tint=(170, 196, 255), shade=(6, 12, 50), sat=0.96, con=1.10),
    'kirmizi': dict(tint=(255, 120, 100), shade=(40, 6, 20), sat=1.10, con=1.10),
    'sepya':   None,
}


def _grade_filter(m):
    s, c = m['sat'], m['con']
    lr, lg, lb = 0.2126, 0.7152, 0.0722
    sm = [lr * (1 - s) + s, lg * (1 - s), lb * (1 - s),
          lr * (1 - s), lg * (1 - s) + s, lb * (1 - s),
          lr * (1 - s), lg * (1 - s), lb * (1 - s) + s]
    off = 0.5 * (1 - c)
    sh = [v / 255 * 0.05 for v in m['shade']]                      # golgelere hafif renk
    M = [sm[0] * c, sm[1] * c, sm[2] * c, 0, off + sh[0],
         sm[3] * c, sm[4] * c, sm[5] * c, 0, off + sh[1],
         sm[6] * c, sm[7] * c, sm[8] * c, 0, off + sh[2],
         0, 0, 0, 1, 0]
    return skia.ColorFilters.Matrix(M)


_GRAIN = []
def _grain(i):
    if not _GRAIN:
        rng = np.random.default_rng(7)
        for _ in range(4):
            g = rng.normal(128, 40, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)
            rgba = np.dstack([g, g, g, np.full_like(g, 255)])
            _GRAIN.append(skia.Image.fromarray(rgba))
    return _GRAIN[i % 4]


def rays(cv, lx, ly, strength, tint, k):
    """kaynaktan asagi yayilan yumusak isik huzmeleri"""
    if strength <= 0.02: return
    for i, (ang, wid, a) in enumerate(((-0.30, 0.10, 0.9), (-0.08, 0.14, 1.0), (0.16, 0.09, 0.8), (0.34, 0.07, 0.6))):
        wob = 0.03 * math.sin(k * 0.07 + i * 1.7)
        L = H * 1.1
        p = skia.Path(); p.moveTo(lx, ly)
        p.lineTo(lx + math.sin(ang + wob - wid) * L, ly + math.cos(ang + wob - wid) * L)
        p.lineTo(lx + math.sin(ang + wob + wid) * L, ly + math.cos(ang + wob + wid) * L); p.close()
        pa = skia.Paint(AntiAlias=True)
        pa.setShader(skia.GradientShader.MakeRadial(skia.Point(lx, ly), L * 0.75,
                     [skia.Color(*tint, int(95 * a * strength)), skia.Color(*tint, 0)]))
        pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)); pa.setBlendMode(skia.BlendMode.kPlus)
        cv.drawPath(p, pa)


def light_pass(cv, surf, k, light, opt):
    """kare cizildikten sonra: parlama, huzme, ISIK HAVUZU, vinyet, renk ayari, gren"""
    mood = opt.get('mood'); m = MOODS.get(mood) or MOODS[None]
    img = surf.makeImageSnapshot()
    # renk ayari (sepya sahneleri kendi rengini zaten ciziyor: dokunma)
    if mood != 'sepya':
        p = skia.Paint(); p.setColorFilter(_grade_filter(m)); cv.drawImage(img, 0, 0, LIN, p)
        img = surf.makeImageSnapshot()
    # parlama (bloom): parlak bolgeler bulanik olarak ustune eklenir
    q = 6; sw, shh = W // q, H // q
    small = skia.Surface(sw, shh); sc = small.getCanvas(); sc.clear(0)
    bp = skia.Paint(); bp.setColorFilter(skia.ColorFilters.Matrix([1.8, 0, 0, 0, -0.95, 0, 1.8, 0, 0, -0.95, 0, 0, 1.8, 0, -0.95, 0, 0, 0, 1, 0]))
    bp.setImageFilter(skia.ImageFilters.Blur(5, 5))
    sc.drawImageRect(img, skia.Rect.MakeWH(sw, shh), LIN, bp)
    pa = skia.Paint(); pa.setBlendMode(skia.BlendMode.kScreen); pa.setAlphaf(0.45 * clamp(1.4 - light[3] / 120, 0.25, 1.0))
    cv.drawImageRect(small.makeImageSnapshot(), skia.Rect.MakeWH(W, H), LIN, pa)
    # huzme ve isik havuzu
    lx, ly, peak, mean = light
    if opt.get('rays', True) and peak > 120:
        rays(cv, lx, ly, clamp((peak - 110) / 80) * (1.0 if mean < 110 else 0.5), m['tint'], k)
    if peak > 120:
        pool = skia.Paint(); pool.setBlendMode(skia.BlendMode.kSoftLight)
        gy = orgu.GYD if FMT == 'h' else 1330 * 1.0
        pool.setShader(skia.GradientShader.MakeRadial(skia.Point(lx, min(H * 0.86, gy)), W * 0.55,
                       [skia.Color(*m['tint'], 150), skia.Color(*m['tint'], 0)]))
        cv.drawRect(skia.Rect.MakeWH(W, H), pool)
    # vinyet
    vg = skia.Paint(); r = math.hypot(W, H) * 0.62
    vg.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.47), r,
                 [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 0), skia.Color(*m['shade'], 175)], [0.0, 0.55, 1.0]))
    cv.drawRect(skia.Rect.MakeWH(W, H), vg)
    # gren
    gp = skia.Paint(); gp.setBlendMode(skia.BlendMode.kOverlay); gp.setAlphaf(0.10)
    cv.drawImageRect(_grain(k), skia.Rect.MakeWH(W, H), LIN, gp)


# ---------- altyazi: ortada, buyuk, 1-3 kelime ----------
def _split3(cap):
    words = cap['words']; n = len(words)
    if n <= 3: return [(cap['a'], cap['b'], words)]
    parts, i = [], 0
    while i < n:
        take = 3 if n - i > 4 else (n - i if n - i <= 3 else 2)
        parts.append(words[i:i + take]); i += take
    w = np.array([orgu.syl(p) for p in parts], float); cum = np.concatenate([[0], np.cumsum(w)]) / w.sum()
    T = cap['b'] - cap['a']
    return [(cap['a'] + T * cum[j], cap['a'] + T * cum[j + 1], parts[j]) for j in range(len(parts))]


_CAPS = {}
def captions(cv, TL, t):
    if id(TL) not in _CAPS:
        _CAPS[id(TL)] = [(a, b, w, c['line']) for c in TL.caps for (a, b, w) in _split3(c)]
    cur = None
    for a, b, w, line in _CAPS[id(TL)]:
        if a <= t < b: cur = (a, b, w, line)
    if not cur: return
    a, b, words, line = cur
    pop = smooth(seg(t, a, a + 0.12))
    if FMT == 'v': size, cy, maxw = 104, 1250, 960
    else: size, cy, maxw = 76, 985, 1500
    size *= lerp(0.86, 1.0, pop)
    f = skia.Font(TFB, size); f.setEmbolden(True); sp = f.measureText(' ')
    s = ' '.join(words); wd = f.measureText(s)
    if wd > maxw: f.setSize(size * maxw / wd); wd = f.measureText(s)
    x = W / 2 - wd / 2
    st = stroke((0, 0, 0), f.getSize() * 0.22, 255); st.setStrokeJoin(skia.Paint.kRound_Join)
    sh = fill((0, 0, 0), 120); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
    cv.drawString(s, x + 4, cy + 10, f, sh)
    cv.drawString(s, x, cy, f, st)
    hl = set(line.get('hl') or [])
    xx = x
    for w_ in words:
        ww = f.measureText(w_)
        cv.drawString(w_, xx, cy, f, fill((255, 214, 80) if w_ in hl else (255, 255, 255)))
        xx += ww + sp
    # konusan: kelimelerin altinda ince renkli cizgi
    _, pc = orgu.SPK.get(line['spk'], ('', CREAM))
    bw = min(wd, 220); by = cy + f.getSize() * 0.32
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(W / 2 - bw / 2, by, W / 2 + bw / 2, by + 12), 6, 6), fill(pc, 235 * pop))


# ---------- plaka: uretilmis arka plan gorseli ----------
_PLATE = {}
def plate(cv, path, dim_=0.0, shift=(0.0, 0.0)):
    """Uretilmis arka plan gorselini sahne koordinatinda gorunen alanin tamamina doldurur (kirparak).
    path: dizi klasorune gore yol, FMT'ye gore '-v.jpg' ya da '-h.jpg' eki kendisi eklenir (orn. 'arkaplan/lobi').
    with stage(cv): icinde, dekordan once cagir. dim_: 0..1 karartma, shift: (dx, dy) sahne birimi kaydirma (parallax icin).
    Dosya yoksa False doner; sahne o zaman kodla cizilen dekora duser."""
    import inspect
    base = os.path.dirname(os.path.abspath(inspect.stack()[1].filename))
    for up in ('', '..', os.path.join('..', '..')):
        p = os.path.join(base, up, f"{path}-{'v' if FMT == 'v' else 'h'}.jpg")
        if os.path.exists(p): break
    else: return False
    if p not in _PLATE: _PLATE[p] = skia.Image.open(p)
    img = _PLATE[p]
    L, T, R, B = (0, 0, 1080, 1920) if FMT == 'v' else (-440, 430, 1520, 1550)
    w, h = R - L, B - T; s = max(w / img.width(), h / img.height()) * 1.04
    iw, ih = img.width() * s, img.height() * s
    x = L + (w - iw) / 2 + shift[0]; y = T + (h - ih) / 2 + shift[1]
    cv.drawImageRect(img, skia.Rect.MakeXYWH(x, y, iw, ih), LIN)
    if dim_ > 0: cv.drawRect(skia.Rect.MakeLTRB(L - 50, T - 50, R + 50, B + 50), fill((4, 6, 18), 255 * clamp(dim_)))
    return True
