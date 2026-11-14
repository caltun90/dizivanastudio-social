"""13. Kat: dizinin ortak parcalari. Karakterler ve aksesuarlar, pozlar, yuruyus, dekorlar (kabin, lobi, koridor),
sayac ve rozetler, kare dongusu ve komutlar. Bolum dosyalari (bNN/bolum.py) yalnizca sahneleri yazar:

    from ortak import *
    def scene1(cv, t): ...
    if __name__ == '__main__': run({1: scene1, ...})

Bolum klasorunun icinden calistirilir (senaryo.py ve voice/ orada):
  FMT=v python bolum.py still <klasor> 3.0 21.5 ...     -> kare kontrolu (FMT=h de)
  FMT=v python bolum.py scene <no>                      -> tek sahne (scenes_v/sN.mp4)
  FMT=v python bolum.py all out-dikey.mp4               -> butun sahneler (paralel) + birlestir + ses
"""
import math, os, sys, subprocess, shutil
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'motor'))
os.environ.setdefault('STAGE_H', '1.0,960,880')          # yatayda sahne kuculmez: kabin 1920'nin ortasina oturur
import skia
import orgu
from orgu import *
from senaryo import TITLE, EP, EP_NAME
import senaryo as _sen

def _ffmpeg():
    p = shutil.which('ffmpeg')
    if p: return p
    import imageio_ffmpeg; return imageio_ffmpeg.get_ffmpeg_exe()
FFMPEG = _ffmpeg()
TL = Timeline()
S, E, B = TL.S, TL.E, TL.B
FLOOR = 1215
DX0, DX1, DY0 = 250, 830, 580
NAVY, TAN, GREEN, PINKB = (92, 116, 196), (190, 146, 100), (70, 116, 92), (244, 120, 140)
CAST = {
    'Z': dict(x=200, gy=GY - 70, s=0.66, c=CORAL, seed=21),
    'S': dict(x=540, gy=GY - 70, s=0.66, c=TAN, seed=23),
    'K': dict(x=880, gy=GY - 70, s=0.66, c=NAVY, seed=25),
    'L': dict(x=350, gy=GY + 26, s=0.80, c=TEAL, seed=5),
    'U': dict(x=730, gy=GY + 26, s=0.56, c=LILAC, seed=9),
}
ORDER = ('Z', 'S', 'K', 'L', 'U')
orgu.SPK.update({'V': ('ASANSÖR', (255, 150, 90)), 'L': ('LEO', TEAL), 'Z': ('ZOE', CORAL), 'K': ('KAI', NAVY), 'U': ('LUNA', LILAC), 'S': ('SAM', TAN)})


def step(t): return math.floor(t * STEP + 1e-6) / STEP
def kk(t): return int(t * STEP + 1e-6)
def jit(k, amp): return (((k * 37) % 7 - 3) / 3 * amp, ((k * 53) % 5 - 2) / 2 * amp) if amp > 0 else (0, 0)
def alt(k, a, b, hold=3): return b if (k // hold) % 2 else a
def frac(lid, f): return S(lid) + (E(lid) - S(lid)) * f
def on(ts, lid, pre=0.05, post=0.15): return S(lid) - pre <= ts < E(lid) + post
def poly(cv, pts, c, a=255):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); cv.drawPath(p, fill(c, a)); return p
def dashed(c, w, a=200, d=(14, 10)):
    ds = stroke(c, w, a, cap=False); ds.setPathEffect(skia.DashPathEffect.Make(list(d), 0)); return ds
def dim(cv, a, c=(6, 8, 22)):
    if a > 0: cv.drawRect(skia.Rect.MakeWH(W, H), fill(c, 255 * clamp(a)))


# ---------- pozlar ----------
HOLD = dict(aL=(-90, 140, -46, 236), aR=(90, 140, 46, 236))
HOLDUP = dict(aL=(-90, 110, -46, 196), aR=(90, 110, 46, 196))
HIP = dict(aR=(150, 120, 46, 232))
UP = dict(aL=(-120, 40, -150, -110), aR=(120, 40, 150, -110))
CALM = dict(aL=(-120, 100, -176, 60), aR=(120, 100, 176, 60))
PRESS_A = dict(aR=(120, 60, 190, -10), lean=18, belly=-10); PRESS_B = dict(aR=(120, 70, 150, 20), lean=12, belly=-6)
POINTUP = dict(aR=(70, 20, 90, -130))
POINT_R = dict(aR=(120, 110, 190, 190))
THUMB = dict(aR=(100, 30, 70, -70))
RANT = dict(aL=(-130, 60, -180, -40), aR=(130, 60, 180, -40))
POCKET = dict(aR=(130, 150, 60, 236))
REACH_L = dict(aL=(-120, 90, -190, 40))
# bukulen pozlar: 'belly' omurgayi egri yapar, 'crouch' comeltir, dizler disari acilir
COWER = dict(crouch=34, lean=-8, belly=16, kL=(-104, -112), kR=(104, -112), aL=(-80, 96, -34, 44), aR=(80, 96, 34, 44))
COWER_HOLD = dict(crouch=34, lean=-8, belly=16, kL=(-104, -112), kR=(104, -112))
LOOKUP = dict(lean=-6, belly=-14)
LEAN_IN = dict(lean=22, belly=-12)
SLUMP = dict(crouch=18, lean=10, belly=-14, kL=(-86, -124), kR=(86, -124))


def walk(dist, s, facing=1, scared=False, hold=False, run=False, off=0.0):
    """yandan yuruyus dongusu: adim mesafeden hesaplanir, ayak kaymaz. facing: 1 saga, -1 sola"""
    stride, lift = (74, 60) if run else (62, 44)
    th = 2 * math.pi * (dist / (4 * stride * s) + off)
    def leg(a):
        c, sn = math.cos(a), math.sin(a)
        up = max(0.0, c)                                   # ileri savrulurken ayak kalkar, diz one cikar
        fx = stride * sn; kx = fx * 0.45 + 22 + 34 * up
        return (facing * kx, -128 - 16 * up), (facing * fx, -18 - lift * up)
    kL, fL = leg(th); kR, fR = leg(th + math.pi)
    sw = math.sin(th)
    P = dict(kL=kL, fL=fL, kR=kR, fR=fR, bob=-9 * (1 - abs(sw)), lean=facing * (20 if run else 12), belly=-facing * 8)
    if scared: P.update(crouch=16, lean=facing * 6, belly=facing * 12)
    if hold: pass
    elif scared: P.update(aL=(-70 + 14 * sw, 100, -30 + 20 * sw, 52), aR=(70 + 14 * sw, 100, 30 + 20 * sw, 52))
    else: P.update(aL=(facing * (-24 - 56 * sw), 160, facing * (-14 - 104 * sw), 282), aR=(facing * (24 + 56 * sw), 160, facing * (14 + 104 * sw), 282))
    return P


# ---------- aksesuarlar ----------
def tie_at(cv, x, y, s, alpha=1.0, rot=0.0):
    cv.save(); cv.translate(x, y); cv.rotate(rot); a = 255 * alpha
    poly(cv, [(-13 * s, 0), (13 * s, 0), (9 * s, 30 * s), (-9 * s, 30 * s)], shade(MUSTARD, 0.82), a)
    poly(cv, [(-10 * s, 30 * s), (10 * s, 30 * s), (24 * s, 150 * s), (0, 182 * s), (-24 * s, 150 * s)], MUSTARD, a)
    cv.drawLine(0, 44 * s, 0, 160 * s, dashed(shade(MUSTARD, 0.6), 2.5 * s, 200 * alpha, (9 * s, 7 * s))); cv.restore()


HAIR = (244, 208, 112)                                     # sari
SKIRT = (128, 66, 118)
def hair(cv, hx, hy, HR, a, back, c_seed=21):
    """uzun sari sac: ortadan ayrik, omuzlardan gogse dokulen yun tutamlari; arkadan bakista basi ve sirti orter"""
    u = HR
    sh = skia.Path()
    sh.moveTo(hx - u * 1.04, hy + u * 1.95)
    sh.cubicTo(hx - u * 1.58, hy + u * 0.90, hx - u * 1.42, hy - u * 1.26, hx, hy - u * 1.24)
    sh.cubicTo(hx + u * 1.42, hy - u * 1.26, hx + u * 1.58, hy + u * 0.90, hx + u * 1.04, hy + u * 1.95)
    if back:
        sh.quadTo(hx, hy + u * 2.2, hx - u * 1.04, hy + u * 1.95)
    else:
        sh.quadTo(hx + u * 0.74, hy + u * 2.04, hx + u * 0.56, hy + u * 1.72)
        sh.cubicTo(hx + u * 0.82, hy + u * 1.10, hx + u * 1.00, hy + u * 0.30, hx + u * 0.82, hy - u * 0.25)   # sag yan
        sh.cubicTo(hx + u * 0.64, hy - u * 0.66, hx + u * 0.30, hy - u * 0.80, hx + u * 0.10, hy - u * 0.86)   # alin (ayrim)
        sh.cubicTo(hx - u * 0.25, hy - u * 0.64, hx - u * 0.66, hy - u * 0.52, hx - u * 0.86, hy - u * 0.12)   # yana taranmis kakul
        sh.cubicTo(hx - u * 1.00, hy + u * 0.40, hx - u * 0.82, hy + u * 1.10, hx - u * 0.56, hy + u * 1.72)
        sh.quadTo(hx - u * 0.74, hy + u * 2.04, hx - u * 1.04, hy + u * 1.95)
    sh.close()
    sd = fill((4, 6, 20), 70 * a / 255.0); cv.save(); cv.translate(u * 0.06, u * 0.09); cv.drawPath(sh, sd); cv.restore()
    cv.drawPath(sh, fill(shade(HAIR, 0.70), a)); cv.save(); cv.clipPath(sh, True)
    px, py = hx + u * 0.10, hy - u * 1.22                   # ayrim noktasi
    n = 30
    for i in range(n):                                     # tutamlar: ayrimdan asagi yelpaze, uclari dalgali
        t_ = i / (n - 1); ex = hx + u * lerp(-1.5, 1.5, t_) + u * 0.06 * math.sin(i * 2.1); ey = hy + u * 2.2
        mx_ = lerp(px, ex, 0.5) + u * 0.72 * (2 * t_ - 1); my_ = lerp(py, ey, 0.22)
        p = skia.Path(); p.moveTo(px + (ex - px) * 0.04, py); p.quadTo(mx_, my_, ex, ey)
        cv.drawPath(p, stroke(shade(HAIR, (0.84, 1.0, 1.22, 1.0, 0.92)[(i + c_seed) % 5]), u * 0.115, a))
    cv.restore()
    cv.drawPath(sh, stroke(shade(HAIR, 0.58), u * 0.03, a))


def skirt(cv, f, s, a):
    """kece etek: belden kalcanin altina, etek ucunda dikis"""
    (hx_, hy_), (mx_, my_) = f['hip'], f['mid']
    wx, wy = lerp(mx_, hx_, 0.45), lerp(my_, hy_, 0.45); by = hy_ + 96 * s
    p = skia.Path(); p.moveTo(wx - 46 * s, wy); p.lineTo(wx + 46 * s, wy)
    p.quadTo(hx_ + 92 * s, hy_ + 30 * s, hx_ + 112 * s, by); p.quadTo(hx_, by + 22 * s, hx_ - 112 * s, by)
    p.quadTo(hx_ - 92 * s, hy_ + 30 * s, wx - 46 * s, wy); p.close()
    cv.drawPath(p, fill(SKIRT, a))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(wx - 50 * s, wy - 9 * s, wx + 50 * s, wy + 12 * s), 8 * s, 8 * s), fill(shade(SKIRT, 0.76), a))
    hm = skia.Path(); hm.moveTo(hx_ - 100 * s, by - 16 * s); hm.quadTo(hx_, by + 5 * s, hx_ + 100 * s, by - 16 * s)
    cv.drawPath(hm, dashed(shade(SKIRT, 1.5), 3 * s, 220 * a / 255.0, (10 * s, 8 * s)))


def accessories(cv, who, f, s, look, alpha, back):
    (hx, hy), HR, a = f['head'], f['HR'], 255 * alpha
    if who == 'L':                                         # kurye sapkasi
        p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(hx - HR * 1.05, hy - HR * 1.08, hx + HR * 1.05, hy + HR * 1.02), 208, 124); p.close()
        cv.drawPath(p, fill(MUSTARD, a))
        sd = -1 if look < -0.5 else 1                       # siperlik bakilan yone doner
        if not back: cv.drawOval(skia.Rect.MakeLTRB(hx + sd * HR * 0.82 - HR * 0.68, hy - HR * 0.66, hx + sd * HR * 0.82 + HR * 0.68, hy - HR * 0.4), fill(shade(MUSTARD, 0.78), a))
        cv.drawCircle(hx, hy - HR * 1.04, HR * 0.09, fill(shade(MUSTARD, 0.7), a))
    elif who == 'S':                                       # bere
        p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(hx - HR * 1.06, hy - HR * 1.1, hx + HR * 1.06, hy + HR * 1.02), 210, 120); p.close()
        cv.drawPath(p, fill(GREEN, a))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(hx - HR * 0.98, hy - HR * 0.66, hx + HR * 0.98, hy - HR * 0.46), HR * 0.1, HR * 0.1), fill(shade(GREEN, 1.35), a))
        cv.drawCircle(hx, hy - HR * 1.14, HR * 0.2, fill(CREAM, a))
    elif who == 'U':                                       # fiyonk
        bx, by = hx + HR * 0.5, hy - HR * 0.92
        for sd in (-1, 1): poly(cv, [(bx, by), (bx + sd * HR * 0.46, by - HR * 0.28), (bx + sd * HR * 0.46, by + HR * 0.28)], PINKB, a)
        cv.drawCircle(bx, by, HR * 0.12, fill(shade(PINKB, 0.8), a))
    elif who == 'Z':                                       # sac (yun tutamlari) + gozluk
        hair(cv, hx, hy, HR, a, back, c_seed=21)
        if back: return
        ey = hy - 7 * s; r = 27 * s
        for sd in (-1, 1):                                  # kirpikler
            ex_ = hx + sd * 34 * s + look * 6 * s
            for dx_, dy_ in ((11, -16), (16, -9)): cv.drawLine(ex_ + sd * (dx_ - 5) * s, ey + (dy_ + 5) * s, ex_ + sd * (dx_ + 5) * s, ey + (dy_ - 3) * s, stroke(THREAD, 3.6 * s, a))
        for sd in (-1, 1): cv.drawCircle(hx + sd * 36.5 * s + look * 6.4 * s, ey, r, stroke(THREAD, 5 * s, a))
        cv.drawLine(hx - 9.5 * s + look * 6.4 * s, ey, hx + 9.5 * s + look * 6.4 * s, ey, stroke(THREAD, 5 * s, a))
    elif who == 'K' and not back:                          # kravat
        tie_at(cv, f['neck'][0], f['neck'][1] + 26 * s, s, alpha)


def package(cv, f, s, alpha=1.0, tie=False, left=False):
    x = (f['handL'][0] + f['handR'][0]) / 2 if not left else f['handL'][0] + 40 * s
    y = f['handL'][1] + 4 * s; w, h, a = 176 * s, 124 * s, 255 * alpha
    rc = skia.Rect.MakeLTRB(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    cv.drawRRect(skia.RRect.MakeRectXY(rc.makeOffset(6, 9), 8, 8), fill((4, 6, 20), 90 * alpha))
    cv.drawRRect(skia.RRect.MakeRectXY(rc, 8, 8), fill((214, 170, 110), a))
    cv.drawRRect(skia.RRect.MakeRectXY(rc.makeInset(9 * s, 9 * s), 5, 5), dashed((150, 108, 60), 2.5, 220 * alpha, (10, 8)))
    lb = skia.Rect.MakeLTRB(x - 44 * s, y - 30 * s, x + 44 * s, y + 30 * s)
    cv.drawRRect(skia.RRect.MakeRectXY(lb, 5, 5), fill(WHITE, a))
    text(cv, 'KAT 13', x, y + 9 * s, 24 * s, (190, 52, 56), a=a)
    if tie: tie_at(cv, x - 50 * s, y - h / 2 - 8 * s, 0.5, alpha, rot=-74)


def actor(cv, ts, who, expr='mutlu', pose=None, look=0.0, alpha=1.0, back=False, dx=0.0, dy=0.0, talk='auto', tie=False, place=None, pkg_left=False):
    """place=(x, gy, s) verilirse kabin yerlesimi yerine o konum/olcek kullanilir (koridor)"""
    c = CAST[who]; k = kk(ts)
    x, gy, s = place if place else (c['x'], c['gy'], c['s'])
    tk = (TL.talk(who, ts) if talk == 'auto' else talk)
    P = dict(HOLD) if who == 'L' else {}
    P.update(pose or {})
    if tk is not None and not place:                        # konusan ziplamaz: govdesiyle hafifce one arkaya salinir
        P['lean'] = P.get('lean', 0) + alt(k, -6, 7, 2); P['belly'] = P.get('belly', 0) + alt(k, 5, -6, 2)
    bl = ((k + c['seed'] * 3) % 37) in (20, 21) and expr in ('mutlu', 'sakin', 'merak', 'endise', 'yorgun', 'kararli', 'uzgun')
    f = figure(cv, x + dx, gy + dy, s, c['c'], None if back else expr, P, c['seed'], talk=None if back else tk,
               blink=bl and not back, look=look, alpha=alpha)
    if who == 'Z': skirt(cv, f, s, 255 * alpha)
    accessories(cv, who, f, s, look, alpha, back)
    if who == 'L': package(cv, f, s, alpha, tie, pkg_left)
    return f


def cast(cv, ts, st, who=ORDER, dy=None):
    """st: {kim: (ifade, poz, bakis[, ek kwargs])}"""
    out = {}
    for w in who:
        if w not in st: continue
        v = st[w]; kw = dict(v[3]) if len(v) > 3 else {}
        if dy: kw['dy'] = kw.get('dy', 0) + dy.get(w, 0)
        out[w] = actor(cv, ts, w, v[0], v[1], v[2], **kw)
    return out


def eye_pos(who):
    c = CAST[who]; g = geo(c['x'], c['gy'], c['s'], IDLE); return g['hc'][0], g['hc'][1] - 7 * c['s'], c['s']


def dark_eyes(cv, who, alpha=1.0, red=None):
    """isiklar sonunce yalnizca gozler. red: o an kirmizi parlayan kisi (sirayla doner: herhangi biri olabilir)"""
    for w in who:
        x, y, s = eye_pos(w); c = (255, 110, 90) if w == red else (240, 232, 200)
        for sd in (-1, 1): cv.drawOval(skia.Rect.MakeLTRB(x + sd * 36 * s - 13 * s, y - 9 * s, x + sd * 36 * s + 13 * s, y + 9 * s), fill(c, 235 * alpha))


def badge(cv, who, txt, red=False):
    """basin ustunde sayi rozeti (sayim)"""
    x, y, s = eye_pos(who); cy = y - 215 * s; r = 36
    cv.drawCircle(x + 3, cy + 5, r, fill((4, 6, 20), 110))
    cv.drawCircle(x, cy, r, fill((255, 86, 74) if red else CREAM)); cv.drawCircle(x, cy, r - 7, dashed(INKBLUE, 2.5, 150, (7, 6)))
    text(cv, txt, x, cy + 17, 46, CREAM if red else INKBLUE)


def tally(cv, marks, alpha=1.0):
    """ekranin ustunde kisi sayaci. marks: [(renk, durum)], durum: 'on' | 'x' (gitti)"""
    if not marks or alpha <= 0: return
    u = 1.0 if FMT == 'v' else 0.82
    n = len(marks); w = 76 * u; tw = n * w + 44 * u
    cx = W / 2 if FMT == 'v' else W - 70 - tw / 2
    cy = 305 if FMT == 'v' else 76
    rc = skia.Rect.MakeLTRB(cx - tw / 2, cy - 50 * u, cx + tw / 2, cy + 50 * u)
    cv.drawRRect(skia.RRect.MakeRectXY(rc, 50 * u, 50 * u), fill(INKBLUE, 215 * alpha))
    cv.drawRRect(skia.RRect.MakeRectXY(rc.makeInset(8 * u, 8 * u), 42 * u, 42 * u), dashed((206, 214, 246), 2.5, 170 * alpha, (10, 8)))
    for i, (c, stt) in enumerate(marks):
        x = cx - (n - 1) * w / 2 + i * w; a = (95 if stt == 'x' else 255) * alpha
        cv.drawCircle(x, cy - 16 * u, 13 * u, fill(c, a))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - 17 * u, cy + 1 * u, x + 17 * u, cy + 30 * u), 12 * u, 12 * u), fill(c, a))
        if stt == 'x':
            cv.drawLine(x - 22 * u, cy - 32 * u, x + 22 * u, cy + 32 * u, stroke((255, 86, 74), 7 * u, 255 * alpha))
            cv.drawLine(x + 22 * u, cy - 32 * u, x - 22 * u, cy + 32 * u, stroke((255, 86, 74), 7 * u, 255 * alpha))


# ---------- dekor: koridor ----------
def corridor(cv, near, far, end, lamp=1.0):
    nx0, ny0, nx1, ny1 = near; fx0, fy0, fx1, fy1 = far
    poly(cv, [(nx0, ny0), (nx1, ny0), (fx1, fy0), (fx0, fy0)], (40, 48, 58))
    poly(cv, [(nx0, ny1), (nx1, ny1), (fx1, fy1), (fx0, fy1)], (92, 50, 62))
    poly(cv, [(nx0, ny0), (fx0, fy0), (fx0, fy1), (nx0, ny1)], (58, 80, 86))
    poly(cv, [(nx1, ny0), (fx1, fy0), (fx1, fy1), (nx1, ny1)], (50, 70, 78))
    poly(cv, [(lerp(nx0, nx1, .3), ny1), (lerp(nx0, nx1, .7), ny1), (lerp(fx0, fx1, .74), fy1), (lerp(fx0, fx1, .26), fy1)], (124, 64, 76))
    sc_ = (nx1 - nx0) / 2200.0
    for i, f in enumerate((0.34, 0.56, 0.71, 0.81, 0.88, 0.93)):
        x0, y0, x1, y1 = lerp(nx0, fx0, f), lerp(ny0, fy0, f), lerp(nx1, fx1, f), lerp(ny1, fy1, f)
        cv.drawRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), dashed((150, 170, 176), max(1.2, 5 * (1 - f) * sc_ + 1), 130, (14 * (1 - f) + 3, 10 * (1 - f) + 2)))
        lw = (x1 - x0) * 0.09; on_ = lamp if (i % 2 == 0 or lamp >= 1) else lamp * 0.4
        cv.drawOval(skia.Rect.MakeLTRB((x0 + x1) / 2 - lw * 2.2, y0 - lw * 0.5, (x0 + x1) / 2 + lw * 2.2, y0 + lw * 1.3), fill((250, 236, 190), 46 * on_))
        cv.drawOval(skia.Rect.MakeLTRB((x0 + x1) / 2 - lw, y0, (x0 + x1) / 2 + lw, y0 + lw * 0.4), fill((250, 236, 190), 235 * on_))
    cxm, cym = (fx0 + fx1) / 2, (fy0 + fy1) / 2
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeRadial(skia.Point(cxm, cym), (ny1 - ny0) * 0.5, [skia.Color(6, 8, 20, 215), skia.Color(6, 8, 20, 0)]))
    cv.drawRect(skia.Rect.MakeLTRB(nx0, ny0, nx1, ny1), g)
    rc = skia.Rect.MakeLTRB(fx0, fy0, fx1, fy1)
    if end == 'red':
        cv.drawRect(rc, fill((204, 54, 58))); cv.drawRect(rc.makeInset((fx1 - fx0) * 0.12, (fy1 - fy0) * 0.08), dashed((255, 170, 160), 2, 220, (6, 5)))
        cv.drawCircle(fx1 - (fx1 - fx0) * 0.24, cym + 4, (fx1 - fx0) * 0.06, fill(YEL))
    else:
        cv.drawRect(rc.makeOutset(6, 6), fill((30, 34, 48))); cv.drawRect(rc, fill((250, 228, 156)))
        cv.drawLine(cxm, fy0, cxm, fy1, stroke((200, 170, 100), 2))


def phone(cv, x, y, s, k):
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - 34 * s, y - 16 * s, x + 34 * s, y + 16 * s), 7 * s, 7 * s), fill((200, 236, 255)))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - 34 * s, y - 16 * s, x + 34 * s, y + 16 * s), 7 * s, 7 * s), stroke(THREAD, 4 * s))
    for i in range(3):
        r = (40 + i * 26 + (10 if k % 2 else 0)) * s
        p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(x - r, y - 10 * s - r, x + r, y - 10 * s + r), 220, 100); cv.drawPath(p, stroke((200, 236, 255), 5 * s, 220 - i * 60))


_IMG = {}
# ---------- dekor: yandan koridor (soldaki asansorden sagdaki kirmizi kapiya) ----------
CFLOOR, CTOP = 1200, 520
FAR, NEAR = GY - 70, GY + 12                               # iki yuruyus seridi
LIFT_X = (40, 330)                                         # asansor kapisinin dunya x araligi


def noise_img():
    if 'noise' in _IMG: return _IMG['noise']
    surf = skia.Surface(W, H); cv = surf.getCanvas(); cv.clear(skia.Color(128, 128, 128, 255))
    n = skia.Paint(); n.setShader(skia.PerlinNoiseShader.MakeFractalNoise(0.9, 0.9, 3, 6.0)); cv.drawRect(skia.Rect.MakeWH(W, H), n)
    _IMG['noise'] = surf.makeImageSnapshot(); return _IMG['noise']


def side_corridor(cv, cam, door_x, lamp=1.0, k=0, open_u=0.0):
    """cam: kadrajin sol kenarindaki dunya x'i. Dunya: asansor solda, door_x'te kirmizi kapi ve duvar"""
    cv.clear(col((40, 48, 58)))
    with stage(cv):
        x0, x1 = -520, 1620                                 # gorunen sahne araligi (yatayda genis)
        cv.drawRect(skia.Rect.MakeLTRB(x0, CTOP, x1, CFLOOR), fill((58, 80, 86)))
        cv.drawLine(x0, 930, x1, 930, dashed((110, 136, 142), 4, 170, (18, 14)))
        cv.drawRect(skia.Rect.MakeLTRB(x0, CFLOOR - 46, x1, CFLOOR), fill((44, 62, 68)))                       # supurgelik
        cv.drawLine(x0, 410, x1, 410, stroke((58, 68, 80), 20)); cv.drawLine(x0, 404, x1, 404, stroke((74, 86, 100), 5))   # tavandaki boru
        for j in range(int((cam + x0) // 310) - 1, int((cam + x1) // 310) + 2):
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(310 * j - cam - 9, 388, 310 * j - cam + 9, 432), 5, 5), fill((40, 48, 60)))
        cv.drawRect(skia.Rect.MakeLTRB(x0, CFLOOR, x1, 5000), fill((92, 50, 62)))
        cv.drawRect(skia.Rect.MakeLTRB(x0, CFLOOR + 34, x1, CFLOOR + 230), fill((124, 64, 76)))
        for yy in (CFLOOR + 46, CFLOOR + 218): cv.drawLine(x0, yy, x1, yy, dashed((176, 110, 120), 3.5, 190, (16, 12)))
        i0 = int((cam + x0 - 900) // 620) - 1
        for i in range(i0, i0 + 6):
            wx = 900 + 620 * i - cam                        # duvar paneli dikisi (kapi yok: tek hedef kirmizi kapi)
            if 420 < 900 + 620 * i < door_x - 120:
                cv.drawLine(wx, CTOP + 60, wx, CFLOOR - 6, stroke((46, 66, 72), 5))
                cv.drawLine(wx + 9, CTOP + 60, wx + 9, CFLOOR - 6, dashed((98, 124, 130), 2.5, 150, (12, 10)))
            lx = 590 + 620 * i - cam                        # tavan lambalari
            if 300 < 590 + 620 * i < door_x:
                on_ = lamp if (i + k // 9) % 4 else lamp * 0.35
                poly(cv, [(lx - 60, CTOP + 34), (lx + 60, CTOP + 34), (lx + 250, CFLOOR), (lx - 250, CFLOOR)], (250, 236, 190), 20 * on_)
                cv.drawLine(lx, CTOP - 40, lx, CTOP, stroke((30, 36, 44), 6))
                cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(lx - 62, CTOP, lx + 62, CTOP + 36), 16, 16), fill((250, 236, 190), 255 * (0.35 + 0.65 * on_)))
        # asansor (solda, isikli)
        a0, a1 = LIFT_X[0] - cam, LIFT_X[1] - cam
        if a1 > x0:
            cv.drawRect(skia.Rect.MakeLTRB(a0 - 22, 668, a1 + 22, CFLOOR), fill((30, 34, 48)))
            cv.drawRect(skia.Rect.MakeLTRB(a0, 690, a1, CFLOOR), fill((250, 228, 156)))
            cv.drawRect(skia.Rect.MakeLTRB(a0 + 14, 706, a1 - 14, CFLOOR), dashed((214, 180, 96), 3, 220))
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB((a0 + a1) / 2 - 62, 598, (a0 + a1) / 2 + 62, 656), 10, 10), fill((28, 32, 46)))
            text(cv, '13', (a0 + a1) / 2, 644, 44, (255, 86, 74))
            poly(cv, [(a0, CFLOOR), (a1, CFLOOR), (a1 + 200, CFLOOR + 260), (a0 - 60, CFLOOR + 260)], (250, 228, 156), 34)
        if LIFT_X[0] - cam > x0: cv.drawRect(skia.Rect.MakeLTRB(x0, CTOP, LIFT_X[0] - 40 - cam, 5000), fill((34, 44, 52)))
        # koridorun sonu: duvar ve kirmizi kapi
        d0 = door_x - cam
        if d0 < x1 + 60:
            cv.drawRect(skia.Rect.MakeLTRB(d0 + 250, CTOP - 400, x1 + 400, 5000), fill((34, 44, 52)))
            cv.drawRect(skia.Rect.MakeLTRB(d0 - 22, 748, d0 + 212, CFLOOR), fill((70, 24, 30)))
            if open_u > 0:                                  # kapinin ardi: yine asansor (sari isik + kat gostergesi)
                cv.drawRect(skia.Rect.MakeLTRB(d0, 770, d0 + 190, CFLOOR), fill((250, 228, 156)))
                cv.drawRect(skia.Rect.MakeLTRB(d0 + 14, 786, d0 + 176, CFLOOR), dashed((214, 180, 96), 3, 220))
                cv.drawLine(d0 + 6, 1040, d0 + 184, 1040, stroke((200, 170, 100), 10))
                cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(d0 + 95 - 62, 676, d0 + 95 + 62, 736), 10, 10), fill((28, 32, 46)))
                text(cv, '13', d0 + 95, 723, 44, (255, 86, 74), a=255 * open_u)
                poly(cv, [(d0, CFLOOR), (d0 + 190, CFLOOR), (d0 + 250, CFLOOR + 260), (d0 - 200, CFLOOR + 260)], (250, 228, 156), 40 * open_u)
            dw = 190 * (1 - 0.86 * open_u); dx0 = d0 + 190 - dw   # kanat: mentese sagda, acildikca daralir
            cv.drawRect(skia.Rect.MakeLTRB(dx0, 770, d0 + 190, CFLOOR), fill(shade((204, 54, 58), 1 - 0.32 * open_u)))
            if dw > 70: cv.drawRect(skia.Rect.MakeLTRB(dx0 + 18 * dw / 190, 790, d0 + 172, CFLOOR - 18), dashed((255, 170, 160), 3.5, 220))
            cv.drawCircle(dx0 + 34 * dw / 190, 1004, 11, fill(YEL))
            gl = fill((255, 90, 80), 60 * (1 - open_u)); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
            cv.drawRect(skia.Rect.MakeLTRB(d0 - 60, 720, d0 + 250, CFLOOR + 40), gl)
            if open_u > 0:
                gw = fill((250, 228, 156), 70 * open_u); gw.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60))
                cv.drawRect(skia.Rect.MakeLTRB(d0 - 160, 720, d0 + 230, CFLOOR + 60), gw)
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, GY + 60), skia.Point(0, GY + 430)], [skia.Color(10, 8, 26, 0), skia.Color(10, 8, 26, 225)]))
        cv.drawRect(skia.Rect.MakeLTRB(x0, GY, x1, 5000), g)
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kSoftLight); p.setAlphaf(0.4); cv.drawImage(noise_img(), 0, 0, LIN, p)


def shadow(cv, x, s=0.74, alpha=1.0, reach=0.0, k=0, ring=False):
    """arkadan gelen karalti; reach 0..1: kollarini one uzatir. ring: elinde calan telefon"""
    P = dict(aL=(-66, 170, -44, 300), aR=(lerp(66, 150, reach), lerp(170, 60, reach), lerp(44, 250, reach), lerp(300, 40, reach)), lean=14 + 10 * reach, belly=-10)
    if ring: P['aR'] = (110, 110, 150, 40)
    f = figure(cv, x, FAR + 6, s, (38, 36, 56), None, P, 13, hood=True, look=1.0, alpha=alpha)
    if ring: phone(cv, f['handR'][0] + 8, f['handR'][1] - 24, 0.5, k)
    return f


# ---------- dekor: lobi (asansorun disi) ----------
LOBBY = (136, 126, 108)
def lobby(cv, u):
    """u: kapi acikligi 0..1. Kapinin ardi isikli kabin"""
    cv.clear(col(shade(LOBBY, 0.7)))
    with stage(cv):
        cv.drawRect(skia.Rect.MakeLTRB(-3000, -3000, 4000, FLOOR), fill(LOBBY))
        cv.drawRect(skia.Rect.MakeLTRB(-3000, 1010, 4000, FLOOR), fill(shade(LOBBY, 0.78)))
        cv.drawLine(-3000, 1010, 4000, 1010, dashed(shade(LOBBY, 1.45), 4, 190, (18, 14)))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(24, 640, 216, 728), 12, 12), fill((44, 50, 62)))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(34, 650, 206, 718), 8, 8), dashed((150, 160, 190), 2.5, 200, (9, 7)))
        text(cv, 'LOBİ', 120, 705, 52, CREAM)
        cv.drawRect(skia.Rect.MakeLTRB(DX0 - 34, DY0 - 34, DX1 + 34, FLOOR), fill((52, 58, 72)))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(540 - 132, 468, 540 + 132, 562), 16, 16), fill((28, 32, 46)))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(540 - 120, 478, 540 + 120, 552), 10, 10), dashed((90, 100, 130), 2.5, 200, (9, 7)))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(904, 850, 968, 990), 12, 12), fill((44, 50, 66)))
        cv.drawCircle(936, 896, 13, fill(YEL)); cv.drawCircle(936, 946, 13, fill((206, 212, 226)))
        cv.save(); cv.clipRect(skia.Rect.MakeLTRB(DX0, DY0, DX1, FLOOR))
        cv.drawRect(skia.Rect.MakeLTRB(DX0, DY0, DX1, FLOOR), fill((250, 228, 156)))
        cv.drawRect(skia.Rect.MakeLTRB(DX0 + 34, DY0 + 34, DX1 - 34, FLOOR + 40), dashed((214, 180, 96), 3.5, 220))
        cv.drawLine(DX0, 1040, DX1, 1040, stroke((200, 170, 100), 14))
        w = (DX1 - DX0) / 2
        for sd in (-1, 1):
            x0 = (DX0 - w * u) if sd < 0 else (540 + w * u)
            rc = skia.Rect.MakeLTRB(x0, DY0, x0 + w, FLOOR)
            cv.drawRect(rc, fill((150, 162, 178))); cv.drawRect(rc.makeInset(16, 18), dashed((214, 222, 236), 3.5, 200))
            cv.drawLine(x0 + (w if sd < 0 else 0), DY0, x0 + (w if sd < 0 else 0), FLOOR, stroke((84, 94, 112), 5))
        cv.restore()
        cv.drawRect(skia.Rect.MakeLTRB(-3000, FLOOR, 4000, 5000), fill((92, 80, 76)))
        cv.drawLine(-3000, FLOOR + 30, 4000, FLOOR + 30, dashed((160, 144, 132), 4, 200, (16, 12)))
        if u > 0: poly(cv, [(DX0, FLOOR), (DX1, FLOOR), (DX1 + 190, FLOOR + 300), (DX0 - 190, FLOOR + 300)], (250, 228, 156), 46 * u)
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, GY + 60), skia.Point(0, GY + 430)], [skia.Color(14, 12, 34, 0), skia.Color(14, 12, 34, 225)]))
        cv.drawRect(skia.Rect.MakeLTRB(-3000, FLOOR, 4000, 5000), g)
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kSoftLight); p.setAlphaf(0.4); cv.drawImage(noise_img(), 0, 0, LIN, p)


def panel_flash(cv, sh, r_, c_):
    """dugme basilinca kirmizi yanip soner (calismiyor)"""
    with stage(cv, *sh):
        x, y = 938 + c_ * 36, 790 + r_ * 38
        gl = fill((255, 86, 74), 150); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16)); cv.drawCircle(x, y, 26, gl)
        cv.drawCircle(x, y, 13, fill((255, 110, 96)))


# ---------- dekor: asansor kabini ----------
WALL = (104, 124, 138)
def cabin_bg():
    if 'cab' in _IMG: return _IMG['cab']
    surf = skia.Surface(W, H); cv = surf.getCanvas(); cv.clear(col(WALL))
    with stage(cv):
        cv.drawRect(skia.Rect.MakeLTRB(-3000, -3000, -60, FLOOR), fill(shade(WALL, 0.8))); cv.drawRect(skia.Rect.MakeLTRB(1140, -3000, 4000, FLOOR), fill(shade(WALL, 0.8)))
        cv.drawRect(skia.Rect.MakeLTRB(-3000, -3000, 4000, 330), fill((62, 74, 88)))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(360, 236, 720, 296), 30, 30), fill((252, 240, 200)))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(376, 250, 704, 282), 16, 16), dashed((214, 190, 130), 3, 220))
        for x0, x1 in ((36, 214), (866, 1044), (-420, -96), (1176, 1500)):
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x0, 600, x1, 1170), 10, 10), dashed(shade(WALL, 1.45), 3.5, 190))
            cv.drawLine(x0 + 4, 1040, x1 - 4, 1040, stroke((58, 68, 82), 14))
        for x in (-60, 1140): cv.drawLine(x, 330, x, FLOOR, stroke(shade(WALL, 0.62), 6))
        cv.drawRect(skia.Rect.MakeLTRB(DX0 - 20, DY0 - 20, DX1 + 20, FLOOR), fill((56, 64, 80)))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(540 - 132, 468, 540 + 132, 562), 16, 16), fill((28, 32, 46)))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(540 - 120, 478, 540 + 120, 552), 10, 10), dashed((90, 100, 130), 2.5, 200, (9, 7)))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(912, 760, 1000, 1010), 12, 12), fill((44, 50, 66)))
        for r_ in range(6):
            for c_ in range(2):
                cv.drawCircle(938 + c_ * 36, 790 + r_ * 38, 11, fill(YEL if (r_, c_) == (0, 1) else (206, 212, 226)))
        cv.drawRect(skia.Rect.MakeLTRB(-3000, FLOOR, 4000, 5000), fill((80, 68, 96)))
        fl = skia.Path(); fl.moveTo(-3000, FLOOR + 30); fl.lineTo(4000, FLOOR + 30); cv.drawPath(fl, dashed((150, 136, 176), 4, 200, (16, 12)))
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, GY + 60), skia.Point(0, GY + 430)], [skia.Color(14, 12, 34, 0), skia.Color(14, 12, 34, 225)]))
        cv.drawRect(skia.Rect.MakeLTRB(-3000, FLOOR, 4000, 5000), g)
    n = skia.Paint(); n.setShader(skia.PerlinNoiseShader.MakeFractalNoise(0.9, 0.9, 3, 4.0)); n.setBlendMode(skia.BlendMode.kSoftLight); n.setAlphaf(0.45)
    cv.drawRect(skia.Rect.MakeWH(W, H), n)
    _IMG['cab'] = surf.makeImageSnapshot(); return _IMG['cab']


def cabin(cv, sh, u=0.0, lamp=1.0):
    """arka plan + kapi araligi. sh: (dx, dy) sarsinti, u: kapi acikligi 0..1"""
    cv.clear(col(shade(WALL, 0.6))); cv.drawImage(cabin_bg(), sh[0] * K, sh[1] * K)
    with stage(cv, *sh):
        cv.save(); cv.clipRect(skia.Rect.MakeLTRB(DX0, DY0, DX1, FLOOR))
        cv.drawRect(skia.Rect.MakeLTRB(DX0, DY0, DX1, FLOOR), fill((14, 16, 28)))
        if u > 0: corridor(cv, (DX0, DY0, DX1, FLOOR), (490, 664, 590, 790), 'red', lamp)
        w = (DX1 - DX0) / 2
        for sd in (-1, 1):
            x0 = (DX0 - w * u) if sd < 0 else (540 + w * u)
            rc = skia.Rect.MakeLTRB(x0, DY0, x0 + w, FLOOR)
            cv.drawRect(rc, fill((150, 162, 178))); cv.drawRect(rc.makeInset(16, 18), dashed((214, 222, 236), 3.5, 200))
            cv.drawLine(x0 + (w if sd < 0 else 0), DY0, x0 + (w if sd < 0 else 0), FLOOR, stroke((84, 94, 112), 5))
        cv.restore()


def display(cv, sh, txt, red=False, level=None, k=0):
    """kat gostergesi; level verilirse asansorun sesi konusuyor: ses cubuklari"""
    with stage(cv, *sh):
        c = (255, 86, 74) if red else (255, 182, 70)
        gl = fill(c, 70); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22))
        cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(540 - 110, 482, 540 + 110, 548), 10, 10), gl)
        if level is not None:
            for i in range(9):
                h = 8 + 44 * level * (0.45 + 0.55 * abs(math.sin(i * 1.9 + k * 1.3)))
                cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(540 - 92 + i * 22, 515 - h / 2, 540 - 80 + i * 22, 515 + h / 2), 5, 5), fill(c))
        else:
            text(cv, txt, 540, 540, 66, c)


# ============ kare dongusu ve komutlar ============
def run(DRAW, no_tag=None):
    """DRAW: {sahne_no: cizim_fonksiyonu(cv, t)}. no_tag: ust etiketin gizlenecegi sahneler (varsayilan: son sahne)"""
    KS = sorted(TL.scenes); no_tag = no_tag or (KS[-1],)
    def bounds(k):
        """sahnenin 12 fps kare araligi (cift sayiya yuvarlanir: 30 fps'e tam oturur)"""
        a, b = TL.span(k); return 2 * round(a * STEP / 2), (2 * round(b * STEP / 2) if k != KS[-1] else 2 * math.ceil(TL.total * STEP / 2))
    def scene_of(t):
        k = KS[0]
        for s_ in KS:
            if t >= bounds(s_)[0] / STEP - 1e-6: k = s_
        return k
    def frame(cv, t, k=None):
        k = k or scene_of(t)
        DRAW[k](cv, t)
        tb = TL.beats.get('title')
        if not (tb and tb[0] <= t < tb[1]) and k not in no_tag: tag(cv, TITLE, EP)
        for lid, off in getattr(_sen, 'ABONE', []): abone(cv, t, S(lid) + off)   # abone ol bandi (senaryo.ABONE)
        captions(cv, TL, t)
        a, b = bounds(k)[0] / STEP, bounds(k)[1] / STEP
        f = min(seg(t, a, a + 0.25), 1 - seg(t, b - 0.25, b))
        if k == KS[-1]: f = min(seg(t, a, a + 0.25), 1 - seg(t, TL.total - 0.6, TL.total - 0.05))
        if k == KS[0]: f = min(seg(t, 0, 0.4), 1 - seg(t, b - 0.25, b))
        dim(cv, 1 - f, (4, 5, 14))

    cmd = sys.argv[1]; d = f'scenes_{FMT}'
    surf = skia.Surface(W, H); cv = surf.getCanvas()
    def join(out):
        if TL.dry and 'taslak' not in out: sys.exit("voice/final.json bir TASLAK (ses yok). Once 'ses.py build' calistir ya da cikti adina 'taslak' yaz.")
        open(f'{d}/list.txt', 'w').write(''.join(f"file 's{k}.mp4'\n" for k in KS))
        tmp = out.replace('.mp4', '.tmp.mp4')
        r = subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{d}/list.txt', '-i', 'voice/mix.wav',
                            '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', tmp])
        if r.returncode != 0: sys.exit(1)
        os.replace(tmp, out); print('ok', out)
    if cmd == 'still':
        os.makedirs(sys.argv[2], exist_ok=True)
        for ts in sys.argv[3:]:
            frame(cv, float(ts)); surf.makeImageSnapshot().save(f'{sys.argv[2]}/{FMT}_{float(ts):06.2f}.png', skia.kPNG)
    elif cmd == 'scene':
        k = int(sys.argv[2]); a, b = bounds(k); os.makedirs(d, exist_ok=True)
        tmp, out = f'{d}/tmp_s{k}.mp4', f'{d}/s{k}.mp4'
        p = subprocess.Popen([FFMPEG, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(STEP), '-i', '-',
                              '-vf', 'fps=30', '-c:v', 'libx264', '-crf', os.environ.get('CRF', '21'), '-preset', os.environ.get('PRESET', 'medium'), '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
        for i in range(a, b):
            frame(cv, i / STEP, k); p.stdin.write(surf.toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
        p.stdin.close()
        if p.wait() != 0: sys.exit(1)
        os.replace(tmp, out); print('sahne', k, b - a, 'kare', flush=True)
    elif cmd == 'join':
        join(sys.argv[2])
    elif cmd == 'all':                                       # sahneleri paralel isle, sonra birlestir
        import concurrent.futures as cf
        n = int(os.environ.get('JOBS', os.cpu_count() or 2))
        with cf.ThreadPoolExecutor(max(1, n)) as ex:
            rs = list(ex.map(lambda k: subprocess.run([sys.executable, sys.argv[0], 'scene', str(k)]).returncode, KS))
        if any(rs): sys.exit(1)
        join(sys.argv[2])
    elif cmd == 'info':
        print('toplam', TL.total, 'sn | sahneler', {k: TL.span(k) for k in KS}, '| taslak' if TL.dry else '')
