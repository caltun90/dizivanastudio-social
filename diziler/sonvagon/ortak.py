"""Son Vagon: dizinin ortak parcalari. Karakterler ve aksesuarlar, pozlar, yuruyus, dekorlar (vagon kesiti, tren disaridan,
istasyon, koruk, arka kapi), bilet, hoparlor, levha, kare dongusu ve komutlar. Bolum dosyalari (bNN/bolum.py) yalnizca sahneleri yazar:

    from ortak import *
    def scene1(cv, t): ...
    if __name__ == '__main__': run({1: scene1, ...})

Bolum klasorunun icinden calistirilir (senaryo.py ve voice/ orada):
  FMT=v python bolum.py still <klasor> 3.0 21.5 ...     -> kare kontrolu (FMT=h de)
  FMT=v python bolum.py scene <no>                      -> tek sahne (scenes_v/sN.mp4)
  FMT=v python bolum.py all out-dikey.mp4               -> butun sahneler (paralel) + birlestir + ses

Dunya: vagonlar soldan saga dizilir; tren SAGA gider. Arka (son vagon) solda, on (lokomotif) sagda: 'one gecmek' = saga yurumek.
"""
import math, os, sys, subprocess, shutil
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'motor'))
os.environ.setdefault('STAGE_H', '1.0,960,880')          # yatayda sahne kuculmez
import skia
import orgu
from orgu import *
from senaryo import TITLE, EP, EP_NAME
import senaryo as _sen
import sinema

def _ffmpeg():
    p = shutil.which('ffmpeg')
    if p: return p
    import imageio_ffmpeg; return imageio_ffmpeg.get_ffmpeg_exe()
FFMPEG = _ffmpeg()
TL = Timeline()
S, E, B = TL.S, TL.E, TL.B
LTRB = skia.Rect.MakeLTRB
RRXY = skia.RRect.MakeRectXY

# ---------- renkler ve oyuncular ----------
GREENC, ROSE, SKYB = (96, 170, 110), (226, 132, 150), (110, 170, 226)
NAVYH, REDS, GRAYH, SHAWL, BOWL, CASE = (40, 52, 96), (214, 60, 64), (208, 206, 216), (150, 130, 200), (70, 52, 48), (150, 96, 60)
WALLC, WAINS, SEATC, BRASS, LAMPC = (44, 84, 92), (112, 48, 60), (150, 56, 66), (214, 170, 96), (252, 236, 190)
AMBER, REDL, EXTC, PAPER = (255, 182, 70), (255, 86, 74), (124, 50, 62), (244, 232, 204)
FAR, NEAR = GY - 64, GY + 14                               # iki yuruyus seridi
CAST = {
    'M': dict(x=300, gy=NEAR, s=0.70, c=MUSTARD, seed=31),   # Mia: hardal; lacivert kut sac, kirmizi atki
    'R': dict(x=520, gy=FAR, s=0.74, c=GREENC, seed=33),     # Ren: yesil; kulaklik
    'D': dict(x=760, gy=NEAR, s=0.64, c=ROSE, seed=35),      # Ada: gul kurusu; gri topuz, lila sal
    'E': dict(x=940, gy=FAR, s=0.70, c=SKYB, seed=37),       # Eli: gok mavisi; melon sapka, biyik
}
for _c in CAST.values(): _c['head'] = 1.2                 # buyuk kafa (b02'den itibaren; b01 1.0 ile uretildi)
DEFAULT_MOOD = 'kontrast'                                  # sinema: gece mavisi golgeler + sicak lamba havuzu (b02'den itibaren)
SCARF = {'M': (REDS, 150, -1)}
orgu.SPK.update({'A': ('ANONS', AMBER), 'M': ('MIA', MUSTARD), 'R': ('REN', GREENC), 'D': ('ADA', ROSE), 'E': ('ELI', SKYB)})


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
def lashes(cv, hx, hy, s, look, a, HR=None):
    """kirpikler; HR verilirse gozlerin yeri kafanin gercek boyundan hesaplanir (buyuk kafa)"""
    if HR: s = HR / 118.0; ey = hy + 6 * s - 12 * HR / 110.0
    else: ey = hy - 7 * s
    for sd in (-1, 1):
        ex_ = hx + sd * 34 * (HR / 110.0 if HR else s) + look * 6 * s
        for dx_, dy_ in ((11, -16), (16, -9)): cv.drawLine(ex_ + sd * (dx_ - 5) * s, ey + (dy_ + 5) * s, ex_ + sd * (dx_ + 5) * s, ey + (dy_ - 3) * s, stroke(THREAD, 3.6 * s, a))


def bob(cv, hx, hy, u, a, back, c=NAVYH):
    """kut sac (Mia): cene hizasinda biter, yana taranmis kakul; arkadan bakista basi orter"""
    p = skia.Path(); p.moveTo(hx - u * 1.10, hy + u * 0.78)
    p.cubicTo(hx - u * 1.46, hy - u * 0.70, hx - u * 0.80, hy - u * 1.30, hx, hy - u * 1.24)
    p.cubicTo(hx + u * 0.80, hy - u * 1.30, hx + u * 1.46, hy - u * 0.70, hx + u * 1.10, hy + u * 0.78)
    if back: p.quadTo(hx, hy + u * 1.04, hx - u * 1.10, hy + u * 0.78)
    else:
        p.quadTo(hx + u * 0.92, hy + u * 0.80, hx + u * 0.80, hy + u * 0.52)
        p.cubicTo(hx + u * 1.00, hy - u * 0.10, hx + u * 0.72, hy - u * 0.62, hx + u * 0.24, hy - u * 0.72)
        p.cubicTo(hx - u * 0.22, hy - u * 0.52, hx - u * 0.70, hy - u * 0.58, hx - u * 0.90, hy - u * 0.14)
        p.cubicTo(hx - u * 1.00, hy + u * 0.16, hx - u * 0.90, hy + u * 0.40, hx - u * 0.80, hy + u * 0.52)
        p.quadTo(hx - u * 0.92, hy + u * 0.80, hx - u * 1.10, hy + u * 0.78)
    p.close()
    cv.drawPath(p, fill(shade(c, 0.8), a)); cv.save(); cv.clipPath(p, True)
    for i in range(22):
        t_ = i / 21; ex = hx + u * lerp(-1.4, 1.4, t_)
        q = skia.Path(); q.moveTo(hx + u * 0.2 + (ex - hx) * 0.1, hy - u * 1.26); q.quadTo(lerp(hx, ex, 0.7), hy - u * 0.9, ex, hy + u * 1.0)
        cv.drawPath(q, stroke(shade(c, (0.86, 1.0, 1.3, 1.0, 0.92)[i % 5]), u * 0.12, a))
    cv.restore(); cv.drawPath(p, stroke(shade(c, 0.6), u * 0.03, a))


def headphones(cv, hx, hy, u, a):
    pth = skia.Path(); pth.addArc(LTRB(hx - u * 1.10, hy - u * 1.16, hx + u * 1.10, hy + u * 1.04), 196, 148)
    cv.drawPath(pth, stroke((44, 48, 66), u * 0.16, a))
    for sd in (-1, 1):
        rc = RRXY(LTRB(hx + sd * u * 1.06 - u * 0.2, hy - u * 0.30, hx + sd * u * 1.06 + u * 0.2, hy + u * 0.40), u * 0.16, u * 0.16)
        cv.drawRRect(rc, fill(CORAL, a)); cv.drawRRect(rc, stroke((44, 48, 66), u * 0.05, a))


def bun(cv, hx, hy, u, a, back):
    """gri topuz (Ada)"""
    cv.drawCircle(hx, hy - u * 1.22, u * 0.36, fill(GRAYH, a)); cv.drawCircle(hx, hy - u * 1.22, u * 0.22, dashed(shade(GRAYH, 0.7), u * 0.04, a * 0.8, (u * 0.1, u * 0.08)))
    if back: cv.drawCircle(hx, hy, u * 1.04, fill(GRAYH, a)); cv.drawCircle(hx, hy, u * 0.8, dashed(shade(GRAYH, 0.74), u * 0.035, a * 0.7, (u * 0.12, u * 0.1))); return
    p = skia.Path(); p.addArc(LTRB(hx - u * 1.06, hy - u * 1.10, hx + u * 1.06, hy + u * 1.02), 198, 144); p.close()
    cv.drawPath(p, fill(GRAYH, a)); cv.drawPath(p, dashed(shade(GRAYH, 0.72), u * 0.03, a * 0.8, (u * 0.1, u * 0.08)))


def bowler(cv, hx, hy, u, a):
    """melon sapka (Eli)"""
    p = skia.Path(); p.addArc(LTRB(hx - u * 0.88, hy - u * 1.62, hx + u * 0.88, hy - u * 0.10), 180, 180); p.close(); cv.drawPath(p, fill(BOWL, a))
    cv.drawRect(LTRB(hx - u * 0.87, hy - u * 1.02, hx + u * 0.87, hy - u * 0.88), fill(REDS, a))
    cv.drawRRect(RRXY(LTRB(hx - u * 1.28, hy - u * 0.92, hx + u * 1.28, hy - u * 0.74), u * 0.09, u * 0.09), fill(shade(BOWL, 0.8), a))


def accessories(cv, who, f, s, look, alpha, back):
    (hx, hy), u, a = f['head'], f['HR'], 255 * alpha
    if who == 'M':
        bob(cv, hx, hy, u, a, back)
        if not back: lashes(cv, hx, hy, s, look, a, u)
    elif who == 'R': headphones(cv, hx, hy, u, a)
    elif who == 'D':
        bun(cv, hx, hy, u, a, back)
        nx, ny = f['neck']                                 # lila sal
        pts = [(nx - 80 * s, ny + 18 * s), (nx + 80 * s, ny + 18 * s), (nx + 108 * s, ny + 96 * s), (nx, ny + 158 * s), (nx - 108 * s, ny + 96 * s)]
        poly(cv, pts, SHAWL, a)
        sm = skia.Path(); sm.moveTo(nx - 96 * s, ny + 92 * s); sm.lineTo(nx, ny + 144 * s); sm.lineTo(nx + 96 * s, ny + 92 * s)
        cv.drawPath(sm, dashed(shade(SHAWL, 1.45), 3 * s, 220 * alpha, (9 * s, 7 * s)))
        if not back: lashes(cv, hx, hy, s, look, a, u)
    elif who == 'E':
        bowler(cv, hx, hy, u, a)
        if not back:                                       # biyik
            k_ = u / 118.0; mx, my = hx + look * 5 * k_, hy + 6 * k_ + 27 * u / 110.0; s = k_
            for sd in (-1, 1):
                p = skia.Path(); p.moveTo(mx, my); p.quadTo(mx + sd * 16 * s, my - 8 * s, mx + sd * 34 * s, my + 7 * s)
                cv.drawPath(p, stroke(BOWL, 9 * s, a))


# ---------- kucuk nesneler (el esyalari) ----------
def briefcase(cv, x, y, s, a=1.0, rot=0.0):
    """Eli'nin evrak cantasi; (x, y): govdenin ortasi"""
    w, h, A = 170 * s, 118 * s, 255 * a
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    hd = skia.Path(); hd.addArc(LTRB(-30 * s, -h / 2 - 26 * s, 30 * s, -h / 2 + 22 * s), 180, 180); cv.drawPath(hd, stroke(shade(CASE, 0.6), 9 * s, A))
    rc = LTRB(-w / 2, -h / 2, w / 2, h / 2)
    cv.drawRRect(RRXY(rc.makeOffset(5, 8), 12 * s, 12 * s), fill((4, 6, 20), 90 * a))
    cv.drawRRect(RRXY(rc, 12 * s, 12 * s), fill(CASE, A)); cv.drawRRect(RRXY(rc.makeInset(9 * s, 9 * s), 7 * s, 7 * s), dashed(shade(CASE, 1.5), 2.5, 220 * a, (10, 8)))
    cv.drawRect(LTRB(-w / 2, -h * 0.12, w / 2, -h * 0.02), fill(shade(CASE, 0.7), A))
    cv.drawRRect(RRXY(LTRB(-13 * s, -h * 0.2, 13 * s, h * 0.08), 4 * s, 4 * s), fill(BRASS, A)); cv.restore()


def mini_ticket(cv, x, y, s, a=1.0, rot=-10, c=None):
    w, h, A = 92 * s, 54 * s, 255 * a
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    rc = LTRB(-w / 2, -h / 2, w / 2, h / 2)
    cv.drawRRect(RRXY(rc.makeOffset(3, 4), 5 * s, 5 * s), fill((4, 6, 20), 90 * a)); cv.drawRRect(RRXY(rc, 5 * s, 5 * s), fill(PAPER, A))
    cv.drawRect(LTRB(-w / 2, -h / 2, -w / 2 + 20 * s, h / 2), fill(c or (150, 40, 46), A))
    for yy in (-10, 4, 16): cv.drawLine(-w / 2 + 30 * s, yy * s, w / 2 - 10 * s, yy * s, stroke((120, 100, 90), 3 * s, 200 * a, cap=False))
    cv.restore()


def prop_case(cv, f, s, a):
    briefcase(cv, (f['handL'][0] + f['handR'][0]) / 2, f['handL'][1] + 10 * s, s * 0.95, a)
def prop_watch(cv, f, s, a):
    watch(cv, f['handR'][0] + 4 * s, f['handR'][1] - 30 * s, 23.2, 0.62 * s / 0.7, a)
def prop_ticket(cv, f, s, a):
    mini_ticket(cv, f['handR'][0] + 8 * s, f['handR'][1] - 30 * s, s / 0.7, a, c=CAST[f['who']]['c'] if 'who' in f else None)
def prop_knit(cv, f, s, a):
    """Ada'nin orgusu: iki sis ve aralarinda sarkan orgu parcasi"""
    (lx, ly), (rx, ry) = f['handL'], f['handR']; A = 255 * a
    poly(cv, [(lx + 6 * s, ly - 6 * s), (rx - 6 * s, ry - 6 * s), (rx - 14 * s, ry + 92 * s), (lx + 14 * s, ly + 92 * s)], CREAM, A)
    for j in range(1, 5): cv.drawLine(lx + 12 * s, ly - 6 * s + j * 19 * s, rx - 12 * s, ry - 6 * s + j * 19 * s, dashed(shade(CORAL, 1.0), 3 * s, 210 * a, (7 * s, 6 * s)))
    cv.drawLine(lx - 30 * s, ly + 20 * s, rx + 16 * s, ry - 40 * s, stroke((120, 110, 130), 5 * s, A)); cv.drawLine(rx + 30 * s, ry + 20 * s, lx - 16 * s, ly - 40 * s, stroke((120, 110, 130), 5 * s, A))
PROPS = dict(case=prop_case, watch=prop_watch, ticket=prop_ticket, knit=prop_knit)
KNIT = dict(aL=(-84, 110, -40, 180), aR=(84, 110, 40, 180))
SHOW = dict(aR=(96, 60, 70, -30))                           # elindekini (bilet, saat) gosterir
DOORP = dict(aL=(-90, 50, -70, -50), aR=(90, 50, 70, -50))  # eller kapida (arkadan)
BEND = dict(crouch=120, lean=26, belly=-18, kL=(-110, -100), kR=(110, -100), aR=(110, 150, 150, 300))   # yere egilir


def actor(cv, ts, who, expr='sakin', pose=None, look=0.0, place=None, alpha=1.0, back=False, talk='auto', prop=None, dx=0.0, dy=0.0):
    """place=(x, gy, s) sahne koordinati. prop: 'case' | 'watch' | 'ticket' | 'knit'"""
    c = CAST[who]; k = kk(ts)
    if alpha <= 0.01: return None
    x, gy, s = place if place else (c['x'], c['gy'], c['s'])
    tk = (TL.talk(who, ts) if talk == 'auto' else talk)
    P = dict(HOLD) if prop == 'case' else (dict(KNIT) if prop == 'knit' else {})
    P.update(pose or {})
    if tk is not None and 'fL' not in P:                    # konusan ziplamaz: govdesiyle hafifce one arkaya salinir
        P['lean'] = P.get('lean', 0) + alt(k, -5, 6, 2); P['belly'] = P.get('belly', 0) + alt(k, 4, -5, 2)
    bl = ((k + c['seed'] * 3) % 37) in (20, 21) and expr in ('mutlu', 'sakin', 'merak', 'endise', 'yorgun', 'kararli', 'uzgun')
    sinema.contact_shadow(cv, x + dx, gy + dy, s, alpha)
    f = figure(cv, x + dx, gy + dy, s, c['c'], None if back else expr, P, c['seed'], talk=None if back else tk,
               blink=bl and not back, look=look, alpha=alpha, scarf=SCARF.get(who), head=c.get('head', 1.0))
    f['s'], f['who'], f['look'], f['expr'] = s, who, look, expr
    accessories(cv, who, f, s, look, alpha, back)
    if prop: PROPS[prop](cv, f, s, alpha)
    if tk is not None: sinema.note(cv, f, who)
    return f


def people(cv, ts, P, st):
    """P: {kim: (x, gy, s)}; st: {kim: (ifade, poz, bakis[, ek kwargs])}. Arkadaki once cizilir."""
    out = {}
    for w in sorted(st, key=lambda w_: P[w_][1]):
        v = st[w]; kw = dict(v[3]) if len(v) > 3 else {}
        out[w] = actor(cv, ts, w, v[0], v[1], v[2], place=P[w], **kw)
    return out


# ---------- disarisi: gece ve istasyon ----------
_STARS = [((i * 197) % 2400 - 600, 30 + (i * 131) % 640, 2 + (i * 7) % 4) for i in range(48)]
def night(cv, scroll=0.0, k=0, y_h=930, moon=(800, 740), x0=-560, x1=1640, poles=True):
    """gece gogu, ay, uzak tepeler (yavas kayar), direkler (hizli kayar). y_h: ufuk cizgisi. scroll: trenin aldigi yol"""
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, y_h)], [col((10, 14, 34)), col((34, 54, 96))]))
    cv.drawRect(LTRB(x0, -400, x1, y_h + 400), g)
    for sx, sy, r in _STARS:
        x = (sx - scroll * 0.01 + 600) % 2400 - 600
        cv.drawCircle(x, sy, r * (1.4 if (k // 6 + sx) % 9 == 0 else 1.0), fill((236, 232, 210), 200))
    if moon:
        gl = fill((240, 226, 170), 46); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40)); cv.drawCircle(moon[0], moon[1], 110, gl)
        blit(cv, sprite('moon', 170, 170, lambda c: yarn_ball(c, 80, 80, 58, (240, 226, 170))), moon[0] - 80, moon[1] - 80)
    for j, (par, yb, hh, c_) in enumerate(((0.05, y_h, 170, (24, 38, 70)), (0.12, y_h + 24, 100, (14, 22, 46)))):
        p = skia.Path(); off = (scroll * par) % 700; x = x0 - 700 - off; p.moveTo(x, y_h + 400)
        while x < x1 + 700:
            p.lineTo(x, yb - 10); p.quadTo(x + 175, yb - hh, x + 350, yb - 20); p.quadTo(x + 525, yb - hh * 0.55, x + 700, yb - 10); x += 700
        p.lineTo(x, y_h + 400); p.close(); cv.drawPath(p, fill(c_))
    if poles:
        x = x0 - 900 - (scroll % 900) + 450
        cv.drawLine(x0, y_h - 296, x1, y_h - 296, stroke((8, 12, 24), 2.5, cap=False))
        while x < x1 + 900:
            cv.drawLine(x, y_h - 330, x, y_h + 60, stroke((8, 12, 24), 12, cap=False)); cv.drawLine(x - 46, y_h - 300, x + 46, y_h - 300, stroke((8, 12, 24), 9, cap=False)); x += 900


def fog(cv, a, k=0, y=1000, x0=-560, x1=1640, h=260, c=(196, 206, 228)):
    """yerde suzulen sis bantlari"""
    if a <= 0: return
    for i in range(7):
        x = x0 + ((i * 397 + k * (2 + i % 3)) % int(x1 - x0 + 600)) - 300
        p = fill(c, 62 * a); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 46))
        cv.drawOval(LTRB(x - 300, y - h / 2 + (i % 3) * 40, x + 300, y + h / 2 + (i % 3) * 40), p)


def station_bg(cv, name, sx, k=0, fog_a=0.6, bw=250, by=696, x0=-560, x1=1640):
    """peron (vagonun arkasinda ya da penceresinden): sacak, bina duvari, sx'te asili tabela, lamba, saat"""
    night(cv, 0, k, y_h=880, moon=None, poles=False, x0=x0, x1=x1)
    cv.drawRect(LTRB(x0, 610, x1, 1010), fill((36, 44, 62)))
    for px in range(int(x0), int(x1), 330): cv.drawRRect(RRXY(LTRB(px + 20, 660, px + 310, 990), 10, 10), dashed((60, 72, 98), 3, 160, (14, 10)))
    cv.drawRect(LTRB(x0, 548, x1, 618), fill((18, 22, 36))); cv.drawLine(x0, 614, x1, 614, dashed((70, 84, 112), 3, 170, (16, 12)))
    cv.drawRect(LTRB(x0, 1010, x1, 1600), fill((74, 76, 92))); cv.drawLine(x0, 1030, x1, 1030, dashed((232, 200, 110), 7, 230, (30, 20)))
    for sd in (-1, 1): cv.drawLine(sx + sd * (bw - 30), 616, sx + sd * (bw - 30), by + 4, stroke((14, 18, 30), 6, cap=False))
    rc = LTRB(sx - bw, by, sx + bw, by + 110)
    cv.drawRRect(RRXY(rc, 14, 14), fill(PAPER)); cv.drawRRect(RRXY(rc.makeInset(9, 9), 8, 8), dashed((150, 40, 46), 3, 220, (12, 9)))
    f = skia.Font(TFB, 64); w = f.measureText(name)
    if w > 2 * bw - 50: f.setSize(64 * (2 * bw - 50) / w); w = f.measureText(name)
    cv.drawString(name, sx - w / 2, by + 55 + f.getSize() * 0.36, f, fill((150, 40, 46)))
    for lx in (sx + bw + 190, sx - bw - 560):               # sarkan lambalar
        fl = 1.0 if (k * 5 + int(lx)) % 23 else 0.5
        poly(cv, [(lx - 30, 668), (lx + 30, 668), (lx + 220, 1040), (lx - 220, 1040)], LAMPC, 30 * fl)
        cv.drawLine(lx, 616, lx, 644, stroke((14, 18, 30), 5, cap=False)); poly(cv, [(lx - 20, 642), (lx + 20, 642), (lx + 44, 672), (lx - 44, 672)], (20, 24, 34))
        cv.drawOval(LTRB(lx - 28, 664, lx + 28, 682), fill(LAMPC, 255 * fl))
    cx_ = sx - bw - 190                                      # istasyon saati: 23:12
    cv.drawCircle(cx_, 760, 62, fill((20, 24, 38))); cv.drawCircle(cx_, 760, 52, fill(PAPER)); hands(cv, cx_, 760, 23.2, 0.82)
    fog(cv, fog_a, k, y=1000, x0=x0, x1=x1)


def track(cv, scroll=0.0, x0=-560, x1=1640, y=1570):
    """ray, traversler ve balast (y: rayin ustu)"""
    cv.drawRect(LTRB(x0, y + 14, x1, 2600), fill((16, 18, 28)))
    x = x0 - (scroll % 130)
    while x < x1: cv.drawRect(LTRB(x, y + 4, x + 62, y + 30), fill((46, 38, 42))); x += 130
    cv.drawLine(x0, y, x1, y, stroke((124, 132, 154), 7, cap=False))
    span = int(x1 - x0)
    for i in range(70): cv.drawCircle(x0 + (i * 173 - scroll) % span, y + 44 + (i * 37) % 150, 3 + i % 4, fill((62, 64, 82), 200))
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y + 90), skia.Point(0, y + 420)], [skia.Color(6, 8, 22, 0), skia.Color(6, 8, 22, 230)]))
    cv.drawRect(LTRB(x0, y + 14, x1, 2600), g)


# ---------- levha, hoparlor, bilet ----------
def plate(cv, x, y, txt, hi=0.0, k=0, sc_=1.0):
    """vagon numarasi levhasi; hi 0..1: kirmizi yanip soner"""
    w, h = 250 * sc_, 62 * sc_; rc = LTRB(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    if hi > 0:
        gl = fill(REDL, 150 * hi * (1.0 if (k // 3) % 2 else 0.55)); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22 * sc_))
        cv.drawRRect(RRXY(rc.makeOutset(16 * sc_, 16 * sc_), 16 * sc_, 16 * sc_), gl)
    cv.drawRRect(RRXY(rc, 12 * sc_, 12 * sc_), fill((22, 26, 40))); cv.drawRRect(RRXY(rc.makeInset(6 * sc_, 6 * sc_), 8 * sc_, 8 * sc_), dashed((110, 120, 150), 2.5 * sc_, 200, (9 * sc_, 7 * sc_)))
    fs = 42 * sc_; tw = skia.Font(TFB, fs).measureText(txt)
    if tw > w - 34 * sc_: fs *= (w - 34 * sc_) / tw                # uzun yazi (LOKOMOTIF) levhaya sigar
    text(cv, txt, x, y + fs * 0.357, fs, lerpt(AMBER, REDL, hi))


def speaker(cv, x, y, level=None, k=0, sc_=1.0):
    """anons hoparloru; level verilirse anons konusuyor: iki yana ses halkalari"""
    cv.drawRRect(RRXY(LTRB(x - 46 * sc_, y - 34 * sc_, x + 46 * sc_, y + 34 * sc_), 12 * sc_, 12 * sc_), fill((30, 34, 48)))
    cv.drawRRect(RRXY(LTRB(x - 38 * sc_, y - 26 * sc_, x + 38 * sc_, y + 26 * sc_), 8 * sc_, 8 * sc_), dashed((110, 120, 150), 2 * sc_, 190, (7 * sc_, 6 * sc_)))
    cv.drawCircle(x, y, 20 * sc_, fill((64, 70, 92)))
    for r in (7, 14): cv.drawCircle(x, y, r * sc_, stroke((20, 24, 36), 2.5 * sc_))
    if level is not None:
        cv.drawCircle(x + 34 * sc_, y - 22 * sc_, 4.5 * sc_, fill(AMBER))
        for i in range(3):
            r = (60 + i * 30 + 12 * level * ((k + i) % 2)) * sc_
            for a0 in (-28, 152):
                p = skia.Path(); p.addArc(LTRB(x - r, y - r, x + r, y + r), a0, 56); cv.drawPath(p, stroke(AMBER, 6 * sc_, (235 - i * 60) * (0.45 + 0.55 * level)))


def ticket(cv, cx, cy, w, who_c, name, station, a=1.0, rot=0.0, hi=0.0, k=0):
    """bilet (ekran koordinati). station None ise INIS satiri bos; hi 0..1: bos satir kirmizi yanip soner"""
    if a <= 0: return
    u = w / 760.0; h = 380 * u; A = 255 * clamp(a); z = lerp(0.84, 1.0, smooth(a))
    cv.save(); cv.translate(cx, cy); cv.rotate(rot); cv.scale(z, z)
    rc = LTRB(-w / 2, -h / 2, w / 2, h / 2); rr = RRXY(rc, 24 * u, 24 * u)
    sh = fill((4, 6, 20), 150 * clamp(a)); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16))
    cv.drawRRect(RRXY(rc.makeOffset(10 * u, 16 * u), 24 * u, 24 * u), sh)
    cv.drawRRect(rr, fill(PAPER, A))
    cv.save(); cv.clipRRect(rr, True); cv.drawRect(LTRB(-w / 2, -h / 2, -w / 2 + 150 * u, h / 2), fill(who_c, A)); cv.restore()
    cv.drawLine(-w / 2 + 150 * u, -h / 2 + 14 * u, -w / 2 + 150 * u, h / 2 - 14 * u, dashed((110, 92, 80), 5 * u, 230 * clamp(a), (12 * u, 10 * u)))
    cv.drawRRect(RRXY(rc.makeInset(12 * u, 12 * u), 16 * u, 16 * u), dashed((150, 40, 46), 3 * u, 150 * clamp(a), (14 * u, 10 * u)))
    cv.save(); cv.translate(-w / 2 + 92 * u, 0); cv.rotate(-90); text(cv, name, 0, 0, 50 * u, INKBLUE, a=A); cv.restore()
    x0 = -w / 2 + 190 * u
    text(cv, 'GECE EKSPRESİ', x0, -h / 2 + 84 * u, 52 * u, (150, 40, 46), a=A, align='l')
    text(cv, 'KALKIŞ  23:00', x0, -h / 2 + 150 * u, 34 * u, (90, 78, 86), TFM, a=A, align='l')
    text(cv, 'İNİŞ', x0, h / 2 - 66 * u, 46 * u, (90, 78, 86), a=A, align='l')
    bx0, bx1, by = x0 + 132 * u, w / 2 - 40 * u, h / 2 - 52 * u
    if station:
        f = skia.Font(TFB, 56 * u); tw = f.measureText(station)
        if tw > bx1 - bx0: f.setSize(56 * u * (bx1 - bx0) / tw); tw = f.measureText(station)
        cv.drawString(station, (bx0 + bx1) / 2 - tw / 2, by - 12 * u, f, fill(INKBLUE, A))
        cv.drawLine(bx0, by, bx1, by, stroke((90, 78, 86), 4 * u, A, cap=False))
    else:
        on_ = hi <= 0 or (k // 3) % 2 == 0
        c_ = lerpt((90, 78, 86), REDL, hi)
        if hi > 0 and on_:
            gl = fill(REDL, 80 * hi * clamp(a)); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14 * u)); cv.drawRect(LTRB(bx0 - 10 * u, by - 74 * u, bx1 + 10 * u, by + 12 * u), gl)
        cv.drawLine(bx0, by, bx1, by, dashed(c_, 6 * u, A, (18 * u, 12 * u)))
        if hi > 0 and on_: text(cv, '?', (bx0 + bx1) / 2, by - 12 * u, 64 * u, REDL, a=A)
    cv.restore()


def hook_text(cv, t, s, a=1.0):
    """ilk karedeki buyuk kanca yazisi (ekran koordinati)"""
    if a <= 0: return
    size, y = (128, 560) if FMT == 'v' else (88, 214)
    sc_ = lerp(1.22, 1.0, smooth(seg(t, 0, 0.3)))
    f = skia.Font(TFB, size); f.setEmbolden(True); w = f.measureText(s)
    if w > W * 0.74: size *= W * 0.74 / w
    f.setSize(size * sc_); w = f.measureText(s); x = W / 2 - w / 2
    st = stroke((0, 0, 0), size * 0.2, 255 * a); st.setStrokeJoin(skia.Paint.kRound_Join)
    cv.drawString(s, x + 5, y + 10, f, fill((0, 0, 0), 120 * a)); cv.drawString(s, x, y, f, st); cv.drawString(s, x, y, f, fill((255, 214, 80), 255 * a))


# ---------- dekor: vagon (ic kesit) ----------
WL = 2700                                                  # vagonun dunya uzunlugu (x: 0 arka uc .. WL on uc)
ROOF, CEIL, WF, FEDGE = 470, 560, 1215, 1362               # cati, tavan, duvarin zemine degdigi cizgi, zeminin on kenari
WINS, WW, WY0, WY1 = (330, 750, 1170, 1590, 2010), 280, 690, 960
LAMPS = tuple(x + WW / 2 for x in WINS)
SEATS = (680, 1100, 1520, 1940)
RDOOR, FDOOR, SPKX = (50, 240), (2460, 2650), 2365
def seat_xy(i, side=1):
    """i. koltugun minderinin ustu (dunya x, y): uzerine esya koymak icin. side: 1 sag minder, -1 sol"""
    return SEATS[i] + side * 80, 1120


def wagon(cv, cam, no, k=0, scroll=0.0, lamps=1.0, out=None, plate_hi=0.0, door_f=0.0, door_r=0.0, last=True, spk=None):
    """vagonun ic kesiti. cam: kadrajin sol kenarindaki vagon x'i. scroll: trenin aldigi yol (disarisi ve tekerler buna gore akar).
    lamps: 0..1 ya da f(i) (i: arkadan one lamba sirasi). out(cv): pencerelerin ve catinin ardi (varsayilan gece).
    plate_hi: on kapinin ustundeki 'VAGON no' levhasi kirmizi yanar. door_f / door_r: on / arka kapi acikligi. last: arkasinda vagon yok.
    spk: anons konusuyorsa ses duzeyi (hoparlorden halkalar)"""
    cv.clear(col((8, 12, 24)))
    Lf = lamps if callable(lamps) else (lambda i: lamps)
    X = lambda x: x - cam
    with stage(cv):
        x0, x1 = -560, 1640
        (out or (lambda c: night(c, scroll, k)))(cv)
        track(cv, scroll, x0, x1)
        a0, a1 = X(-40), X(WL + 40)
        for sd, ex in ((-1, a0), (1, a1)):                  # komsu vagon (koruk + dis govde) ya da son vagonun kuyruk lambasi
            if sd < 0 and last:
                gl = fill(REDL, 150); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26)); cv.drawCircle(ex - 8, 1120, 40, gl)
                cv.drawCircle(ex - 8, 1120, 15, fill((255, 120, 104))); continue
            b0, b1 = (ex - 110, ex) if sd < 0 else (ex, ex + 110)
            cv.drawRect(LTRB(b0, 620, b1, FEDGE + 30), fill((14, 18, 28)))
            for j in range(1, 5): cv.drawLine(b0 + j * 22, 630, b0 + j * 22, FEDGE + 20, stroke((36, 42, 58), 4, cap=False))
            n0, n1 = (ex - 3000, ex - 110) if sd < 0 else (ex + 110, ex + 3000)
            cv.drawRRect(RRXY(LTRB(n0 - 14, ROOF - 46, n1 + 14, CEIL), 40, 40), fill((24, 34, 48)))
            cv.drawRect(LTRB(n0, CEIL, n1, FEDGE + 64), fill(EXTC)); cv.drawRect(LTRB(n0, 1040, n1, 1064), fill(CREAM, 190))
            wx = n1 - 330 if sd < 0 else n0 + 70
            cv.drawRRect(RRXY(LTRB(wx, WY0, wx + 260, WY1), 20, 20), fill((250, 214, 120)))
        body = skia.Path(); body.addRect(LTRB(a0, ROOF, a1, WF))
        for wx in WINS: body.addRRect(RRXY(LTRB(X(wx), WY0, X(wx) + WW, WY1), 26, 26))
        body.setFillType(skia.PathFillType.kEvenOdd); cv.drawPath(body, fill(WALLC))
        for px in range(-40, WL + 40, 420): cv.drawLine(X(px + 280), CEIL + 10, X(px + 280), 1004, dashed(shade(WALLC, 1.35), 2.5, 120, (12, 10)))
        cv.drawRect(LTRB(a0, 1010, a1, WF), fill(WAINS)); cv.drawLine(a0, 1022, a1, 1022, dashed(shade(WAINS, 1.5), 4, 190, (18, 14)))
        cv.drawRect(LTRB(a0, WF - 40, a1, WF), fill(shade(WAINS, 0.72)))
        cv.drawRRect(RRXY(LTRB(a0 - 14, ROOF - 46, a1 + 14, CEIL), 40, 40), fill((24, 34, 48)))
        cv.drawLine(a0, CEIL - 8, a1, CEIL - 8, dashed((70, 90, 110), 3, 170, (16, 12)))
        for vx in range(200, WL, 520): cv.drawRRect(RRXY(LTRB(X(vx), ROOF - 68, X(vx) + 120, ROOF - 42), 10, 10), fill((18, 26, 38)))
        for wx in WINS:                                     # pencere cerceveleri ve perdeler
            rc = LTRB(X(wx), WY0, X(wx) + WW, WY1)
            if rc.right() < x0 or rc.left() > x1: continue
            for sd, xx in ((1, rc.left()), (-1, rc.right())):
                poly(cv, [(xx, rc.top()), (xx + sd * 78, rc.top()), (xx + sd * 22, rc.top() + 150), (xx, rc.top() + 176)], shade(WAINS, 1.12), 240)
            cv.drawRRect(RRXY(rc, 26, 26), stroke(BRASS, 9)); cv.drawRRect(RRXY(rc.makeOutset(14, 14), 36, 36), dashed(shade(WALLC, 1.5), 3, 170, (12, 10)))
            cv.drawLine(rc.left() + 96, rc.top() + 70, rc.left() + 150, rc.top() + 26, stroke((255, 255, 255), 7, 34))
        cv.drawLine(X(300), 640, X(2320), 640, stroke(BRASS, 7, cap=False))                     # bagaj rafi
        for bx in range(330, 2330, 210): cv.drawLine(X(bx), 640, X(bx), 610, stroke(shade(BRASS, 0.7), 5, cap=False))
        for bx, bw_, bh, c_ in ((820, 150, 60, (96, 70, 110)), (1240, 110, 50, (150, 110, 70)), (2080, 130, 66, (70, 110, 100))):
            rc = LTRB(X(bx), 636 - bh, X(bx) + bw_, 636); cv.drawRRect(RRXY(rc, 10, 10), fill(c_)); cv.drawRRect(RRXY(rc.makeInset(7, 7), 6, 6), dashed(shade(c_, 1.5), 2.5, 190, (9, 7)))
        for i, lx in enumerate(LAMPS):                      # pencere isigi yere vurur
            if Lf(i) > 0.02: poly(cv, [(X(lx) - 130, 1600), (X(lx) + 130, 1600), (X(lx) + 230, 1790), (X(lx) - 230, 1790)], LAMPC, 30 * clamp(Lf(i)))
        for i, lx in enumerate(LAMPS):                      # tavan lambalari
            on_ = clamp(Lf(i)); x = X(lx)
            if x < x0 - 300 or x > x1 + 300: continue
            if on_ > 0.02: poly(cv, [(x - 50, CEIL + 30), (x + 50, CEIL + 30), (x + 230, WF), (x - 230, WF)], LAMPC, 22 * on_)
            cv.drawRRect(RRXY(LTRB(x - 58, CEIL - 4, x + 58, CEIL + 30), 15, 15), fill(lerpt((58, 62, 72), LAMPC, on_)))
        for sx_ in SEATS:                                   # sirt sirta ikili koltuklar
            x = X(sx_)
            if x < x0 - 200 or x > x1 + 200: continue
            for sd in (-1, 1):
                l_, r_ = sorted((x + sd * 6, x + sd * 70))
                cv.drawRRect(RRXY(LTRB(l_, 968, r_, WF + 4), 18, 18), fill(SEATC))
                cv.drawRRect(RRXY(LTRB(l_ + 6, 980, r_ - 6, 1034), 10, 10), fill(CREAM, 235))
                l2, r2 = sorted((x + sd * 6, x + sd * 152))
                cv.drawRect(LTRB(l2, 1150, r2, WF + 4), fill(shade(SEATC, 0.7)))
                cv.drawRRect(RRXY(LTRB(l2, 1120, r2, 1168), 14, 14), fill(shade(SEATC, 1.16)))
                cv.drawLine(l2 + 12, 1144, r2 - 12, 1144, dashed(shade(SEATC, 1.6), 3, 170, (10, 8)))
        for (d0, d1), u_, front in ((RDOOR, door_r, False), (FDOOR, door_f, True)):   # kapilar
            xa, xb = X(d0), X(d1)
            if xb < x0 - 40 or xa > x1 + 40: continue
            lit = front or not last
            cv.drawRect(LTRB(xa - 16, 640, xb + 16, WF), fill((26, 34, 46)))
            cv.drawRect(LTRB(xa, 656, xb, WF), fill(LAMPC if lit else (10, 14, 28)))
            if lit: cv.drawRect(LTRB(xa + 12, 668, xb - 12, WF + 20), dashed((214, 180, 96), 3, 220))
            w = (xb - xa) * (1 - 0.92 * clamp(u_)); lx0 = xa if front else xb - w
            cv.drawRect(LTRB(lx0, 656, lx0 + w, WF), fill((98, 62, 52)))
            if w > 90:
                cv.drawRect(LTRB(lx0 + 14, 672, lx0 + w - 14, WF - 14), dashed((170, 120, 96), 3, 200))
                gr = RRXY(LTRB(lx0 + w * 0.24, 710, lx0 + w * 0.76, 900), 14, 14)
                cv.drawRRect(gr, fill(LAMPC if lit else (14, 20, 40), 235)); cv.drawRRect(gr, stroke(BRASS, 5))
                cv.drawCircle(lx0 + (w * 0.86 if front else w * 0.14), 1016, 11, fill(BRASS))
            if u_ > 0 and lit: poly(cv, [(xa, WF), (xb, WF), (xb + 90, FEDGE), (xa - 90, FEDGE)], LAMPC, 60 * clamp(u_))
        plate(cv, X((FDOOR[0] + FDOOR[1]) / 2), 598, f'VAGON {no}', plate_hi, k)
        speaker(cv, X(SPKX), 606, spk, k)
        cv.drawRect(LTRB(a0, WF, a1, FEDGE), fill((84, 44, 54)))                                # zemin: yolluk hali
        cv.drawRect(LTRB(a0, WF + 36, a1, FEDGE - 24), fill((122, 60, 72)))
        for yy in (WF + 47, FEDGE - 35): cv.drawLine(a0, yy, a1, yy, dashed((184, 118, 126), 3.5, 190, (16, 12)))
        cv.drawRect(LTRB(a0, FEDGE, a1, FEDGE + 64), fill((26, 30, 42))); cv.drawLine(a0, FEDGE + 10, a1, FEDGE + 10, dashed((90, 100, 124), 3, 170, (14, 10)))
        for bx in (420, WL - 420):                          # tekerler
            cv.drawRRect(RRXY(LTRB(X(bx) - 200, 1440, X(bx) + 200, 1476), 12, 12), fill((20, 24, 34)))
            for wx_ in (-130, 130):
                x, cy, r = X(bx + wx_), 1508, 62
                if x < x0 - 80 or x > x1 + 80: continue
                cv.drawCircle(x, cy, r, fill((36, 40, 54))); cv.drawCircle(x, cy, r - 12, stroke((124, 132, 154), 5))
                for j in range(4):
                    a_ = scroll / r + j * math.pi / 2; cv.drawLine(x, cy, x + math.cos(a_) * (r - 14), cy + math.sin(a_) * (r - 14), stroke((124, 132, 154), 5))
                cv.drawCircle(x, cy, 13, fill((170, 60, 64)))
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kSoftLight); p.setAlphaf(0.4); cv.drawImage(noise_img(), 0, 0, LIN, p)


def wagon_dark(cv, cam, lamps, a=0.78):
    """sonen lambalarin altindaki bolumleri karartir (oyunculardan SONRA cagir). lamps: f(i) 0..1"""
    with stage(cv):
        for i, lx in enumerate(LAMPS):
            d = 1 - clamp(lamps(i))
            if d > 0.02:
                p = fill((5, 7, 20), 255 * a * d); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 34))
                cv.drawRect(LTRB(lx - 215 - cam - (400 if i == 0 else 0), ROOF - 20, lx + 215 - cam + (420 if i == len(LAMPS) - 1 else 0), FEDGE + 40), p)


# ---------- dekor: tren disaridan ----------
def ext_wagon(cv, x, y, u, a=1.0, lit=1.0, tail=False, heads=None, num=None, k=0):
    """disaridan vagon; (x, y): sol alt kose (govdenin alti). Genislik 165u, govde yuksekligi 96u. heads: pencerelerdeki yolcu renkleri"""
    w, h, A = 165 * u, 96 * u, 255 * a
    if a <= 0.01: return
    for wx in (30, 135):
        cv.drawCircle(x + wx * u, y + 8 * u, 13 * u, fill((24, 26, 38), A)); cv.drawCircle(x + wx * u, y + 8 * u, 5 * u, fill((170, 60, 64), A))
    cv.drawRect(LTRB(x + 4 * u, y - 2 * u, x + w - 4 * u, y + 6 * u), fill((20, 22, 32), A))
    cv.drawRRect(RRXY(LTRB(x, y - h, x + w, y), 8 * u, 8 * u), fill(EXTC, A))
    cv.drawRRect(RRXY(LTRB(x - 3 * u, y - h - 10 * u, x + w + 3 * u, y - h + 8 * u), 7 * u, 7 * u), fill((30, 36, 50), A))
    cv.drawRect(LTRB(x, y - 30 * u, x + w, y - 23 * u), fill(CREAM, 200 * a))
    cv.drawRRect(RRXY(LTRB(x + 5 * u, y - h + 13 * u, x + w - 5 * u, y - 6 * u), 5 * u, 5 * u), dashed(shade(EXTC, 1.5), max(1.2, 1.4 * u), 150 * a, (5 * u, 4 * u)))
    for i in range(5):
        wx = x + (13 + i * 29) * u; rc = LTRB(wx, y - h + 22 * u, wx + 23 * u, y - h + 54 * u)
        if lit > 0.3:
            gl = fill((250, 214, 120), 60 * lit * a); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 7 * u)); cv.drawRRect(RRXY(rc.makeOutset(4 * u, 4 * u), 5 * u, 5 * u), gl)
        cv.drawRRect(RRXY(rc, 4 * u, 4 * u), fill(lerpt((26, 34, 60), (250, 214, 120), lit), A))
        if heads and i < len(heads) and heads[i]:
            cv.save(); cv.clipRect(rc)
            cv.drawCircle(rc.centerX(), rc.bottom() - 9 * u, 9.5 * u, fill(heads[i], A)); cv.drawRect(LTRB(rc.centerX() - 8 * u, rc.bottom() - 2 * u, rc.centerX() + 8 * u, rc.bottom() + 4 * u), fill(heads[i], A))
            for sd in (-1, 1): cv.drawCircle(rc.centerX() + sd * 3.4 * u, rc.bottom() - 10 * u, 1.3 * u, fill(THREAD, A))
            cv.restore()
    if num: text(cv, str(num), x + w / 2, y - 9 * u, 15 * u, CREAM, a=220 * a)
    if tail:
        gl = fill(REDL, 170 * a); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 9 * u)); cv.drawCircle(x - 2 * u, y - 22 * u, 13 * u, gl)
        cv.drawCircle(x - 1 * u, y - 22 * u, 4.5 * u, fill((255, 130, 110), A))


def ext_loco(cv, x, y, u, k=0):
    """lokomotif; (x, y): sol alt. Genislik 200u; saga gider. Bacadan buhar arkaya (sola) suzulur"""
    for i in range(7):                                      # buhar
        ph = ((k * 0.5 + i * 3) % 21) / 21.0
        cv.drawCircle(x + 158 * u - ph * 300 * u, y - 118 * u - ph * 90 * u - 10 * u * math.sin(i * 2.1), (11 + 30 * ph) * u, fill((214, 220, 236), 150 * (1 - ph)))
    bm = skia.Path(); bm.moveTo(x + 196 * u, y - 60 * u); bm.lineTo(x + 900 * u, y - 150 * u); bm.lineTo(x + 900 * u, y + 40 * u); bm.close()
    pb = skia.Paint(AntiAlias=True); pb.setShader(skia.GradientShader.MakeLinear([skia.Point(x + 196 * u, 0), skia.Point(x + 700 * u, 0)], [skia.Color(255, 236, 170, 110), skia.Color(255, 236, 170, 0)]))
    cv.drawPath(bm, pb)
    for wx in (36, 92, 148): cv.drawCircle(x + wx * u, y + 6 * u, 16 * u, fill((150, 50, 56))); cv.drawCircle(x + wx * u, y + 6 * u, 6 * u, fill((30, 32, 44)))
    cv.drawLine(x + 36 * u, y + 6 * u + 8 * u * math.sin(k * 0.8), x + 148 * u, y + 6 * u + 8 * u * math.sin(k * 0.8), stroke((200, 204, 220), 4 * u))
    cv.drawRRect(RRXY(LTRB(x + 56 * u, y - 74 * u, x + 194 * u, y), 30 * u, 30 * u), fill((30, 62, 72)))
    cv.drawRect(LTRB(x, y - 108 * u, x + 68 * u, y), fill((24, 50, 60))); cv.drawRect(LTRB(x - 5 * u, y - 116 * u, x + 73 * u, y - 104 * u), fill((18, 24, 36)))
    cv.drawRRect(RRXY(LTRB(x + 14 * u, y - 92 * u, x + 54 * u, y - 56 * u), 5 * u, 5 * u), fill((250, 214, 120)))
    cv.drawRect(LTRB(x + 146 * u, y - 112 * u, x + 168 * u, y - 70 * u), fill((18, 24, 36))); cv.drawRect(LTRB(x + 140 * u, y - 120 * u, x + 174 * u, y - 108 * u), fill((18, 24, 36)))
    cv.drawCircle(x + 110 * u, y - 78 * u, 11 * u, fill(BRASS)); cv.drawRect(LTRB(x + 56 * u, y - 44 * u, x + 194 * u, y - 38 * u), fill(BRASS, 220))
    poly(cv, [(x + 194 * u, y - 16 * u), (x + 226 * u, y + 18 * u), (x + 194 * u, y + 18 * u)], (150, 50, 56))
    gl = fill((255, 236, 170), 200); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8 * u)); cv.drawCircle(x + 194 * u, y - 58 * u, 13 * u, gl)
    cv.drawCircle(x + 192 * u, y - 58 * u, 7 * u, fill((255, 246, 214)))


PITCH = 175                                                # vagon araligi (u birimi)
def train_len(n): return 200 + n * PITCH
def train_ext(cv, xr, y, u, n=5, k=0, fade=0.0, heads=None, nums=True):
    """trenin tamami (sahne koordinati). xr: lokomotifin burnunun x'i (sag uc); vagonlar sola dizilir. n: vagon sayisi.
    fade 0..1: SON vagon sise karisip kaybolur. heads: {vagon_no: [renkler]}. Donus: {vagon_no: vagonun orta x'i}"""
    x = xr - 200 * u; ext_loco(cv, x, y, u, k); mid = {}
    for i in range(1, n + 1):
        wx = x - i * PITCH * u; last = i == n; a = (1 - fade) if last else 1.0
        cv.drawRect(LTRB(wx + 165 * u, y - 16 * u, wx + PITCH * u, y - 8 * u), fill((18, 22, 32), 255 * a))
        ext_wagon(cv, wx, y, u, a=a, lit=a if last else 1.0, tail=(last and fade < 0.6) or (i == n - 1 and fade >= 0.6), heads=(heads or {}).get(i), num=i if nums else None, k=k)
        mid[i] = wx + 82 * u
        if last and fade > 0:
            for j in range(6):
                p = fill((196, 206, 228), 120 * math.sin(math.pi * clamp(fade)) + 60 * fade); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22 * u))
                cv.drawCircle(wx + (20 + j * 26) * u + 8 * u * math.sin(k * 0.3 + j), y - (30 + 34 * (j % 2)) * u, 50 * u, p)
    return mid


def ext_bg(cv, scroll=0.0, k=0, y=1120, moon=(820, 520), fog_a=0.5):
    """disarisi: gece, tepeler, tas kemerli kopru ve ray (y: rayin ustu), kemerlerin altinda ay isigi vuran su"""
    night(cv, scroll, k, y_h=y - 40, moon=moon)
    cv.drawRect(LTRB(-560, y, 1640, 2600), fill((20, 26, 42)))
    track(cv, scroll, y=y + 22)
    top = y + 62
    cv.drawRect(LTRB(-560, top, 1640, 2600), fill((44, 52, 76)))
    cv.drawRect(LTRB(-560, top, 1640, top + 22), fill((58, 68, 96))); cv.drawLine(-560, top + 34, 1640, top + 34, dashed((104, 116, 148), 4, 190, (24, 16)))
    span = 560; x = -560 - (scroll % span) - span
    while x < 1700:
        p = skia.Path(); p.moveTo(x + 70, 2600); p.lineTo(x + 70, top + 320); p.arcTo(LTRB(x + 70, top + 110, x + span - 70, top + 530), 180, 180, False); p.lineTo(x + span - 70, 2600); p.close()
        cv.drawPath(p, fill((10, 16, 36)))
        cv.save(); cv.clipPath(p, True)
        cv.drawRect(LTRB(x, top + 560, x + span, 2600), fill((16, 30, 62)))
        for j in range(5): cv.drawLine(x + 150 + 26 * j, top + 600 + 44 * j, x + span - 150 - 26 * j, top + 600 + 44 * j, stroke((240, 226, 170), 5, 70 - 10 * j))
        cv.restore(); cv.drawPath(p, dashed((104, 116, 148), 4, 180, (20, 14)))
        x += span
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, top + 420), skia.Point(0, top + 900)], [skia.Color(6, 8, 22, 0), skia.Color(6, 8, 22, 220)]))
    cv.drawRect(LTRB(-560, top, 1640, 2600), g)
    fog(cv, fog_a, k, y=y + 40)
    return
    x = -560 - ((scroll * 1.8) % 760)
    while x < 1700:                                        # on plan: cali siluetleri
        for j, (dx_, r_) in enumerate(((0, 90), (110, 130), (250, 80))): cv.drawCircle(x + dx_, y + 470 + 20 * j, r_, fill((6, 10, 20)))
        x += 760


# ---------- dekor: peron (disaridan, duran tren) ----------
def platform(cv, name, tx=0.0, k=0, lit5=1.0, heads4=None, heads5=None, fog_a=0.6, n_last=5):
    """perondan trene bakis: solda son vagon, sagda bir onceki. tx: tren duracagi yerden ne kadar geride (fren). Tabela sacaktan sarkar"""
    cv.clear(col((8, 12, 24)))
    with stage(cv):
        night(cv, 0, k, y_h=900, moon=(160, 560) if FMT == 'v' else (-180, 620), poles=False)
        u = 6.2; y = 1232; gx = 500 + tx                     # iki vagonun arasi gx'te
        track(cv, -tx, y=y + 62)
        ext_wagon(cv, gx - 165 * u - 22, y, u, lit=lit5, tail=True, heads=heads5, num=n_last, k=k)
        cv.drawRect(LTRB(gx - 26, y - 90, gx + 26, y - 50), fill((18, 22, 32)))
        ext_wagon(cv, gx + 22, y, u, heads=heads4, num=n_last - 1, k=k)
        cv.drawRect(LTRB(-560, y + 96, 1640, 2600), fill((74, 76, 92)))                            # peron
        cv.drawRect(LTRB(-560, y + 96, 1640, y + 122), fill((150, 150, 164)))
        cv.drawLine(-560, y + 160, 1640, y + 160, dashed((232, 200, 110), 9, 230, (36, 24)))
        for px in range(-560, 1700, 220): cv.drawLine(px, y + 122, px - 60, 2000, stroke((60, 62, 78), 3, 120, cap=False))
        cv.drawRect(LTRB(-560, 380, 1640, 478), fill((16, 20, 34))); cv.drawLine(-560, 472, 1640, 472, dashed((70, 84, 112), 3.5, 180, (18, 14)))   # sacak
        sx = 540                                             # tabela
        for sd in (-1, 1): cv.drawLine(sx + sd * 250, 476, sx + sd * 250, 540, stroke((14, 18, 30), 7, cap=False))
        rc = LTRB(sx - 310, 536, sx + 310, 664)
        cv.drawRRect(RRXY(rc.makeOffset(6, 10), 16, 16), fill((4, 6, 20), 120)); cv.drawRRect(RRXY(rc, 16, 16), fill(PAPER)); cv.drawRRect(RRXY(rc.makeInset(10, 10), 9, 9), dashed((150, 40, 46), 3.5, 220, (14, 10)))
        text(cv, name, sx, 628, 82, (150, 40, 46))
        for lx in ((960, -260) if FMT == 'v' else (1160, -200)):   # sacak lambalari
            fl = 1.0 if (k * 5 + lx) % 23 else 0.5
            poly(cv, [(lx - 36, 540), (lx + 36, 540), (lx + 330, y + 130), (lx - 330, y + 130)], LAMPC, 34 * fl)
            cv.drawLine(lx, 476, lx, 510, stroke((14, 18, 30), 6, cap=False)); poly(cv, [(lx - 24, 506), (lx + 24, 506), (lx + 54, 544), (lx - 54, 544)], (20, 24, 34))
            cv.drawOval(LTRB(lx - 34, 534, lx + 34, 556), fill(LAMPC, 255 * fl))
        bx = 800 if FMT == 'v' else 1240                     # bos bank
        cv.drawRRect(RRXY(LTRB(bx - 150, y + 250, bx + 150, y + 282), 10, 10), fill((40, 60, 66)))
        cv.drawRRect(RRXY(LTRB(bx - 150, y + 170, bx + 150, y + 232), 10, 10), fill((50, 76, 84)))
        for sd in (-1, 1): cv.drawRect(LTRB(bx + sd * 120 - 8, y + 282, bx + sd * 120 + 8, y + 350), fill((30, 44, 50)))
        fog(cv, fog_a, k, y=y + 150, h=320)
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y + 330), skia.Point(0, y + 720)], [skia.Color(8, 10, 26, 0), skia.Color(8, 10, 26, 220)]))
        cv.drawRect(LTRB(-560, y + 300, 1640, 2600), g)
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kSoftLight); p.setAlphaf(0.4); cv.drawImage(noise_img(), 0, 0, LIN, p)


# ---------- dekor: koruk (iki vagonun arasi, kesit) ----------
GL, GR = 280, 800                                          # korugun sol ve sag ucu (sahne x)
def gangway(cv, k=0, scroll=0.0, shake=0.0, closed=0.0, nos=(5, 4), out_l=None, lamp_l=1.0, hi=(0.0, 0.0), gone_l=False, out_r=None):
    """solda arka vagonun on ucu, ortada koruk, sagda ondeki vagonun arka ucu. shake: sarsinti; closed 0..1: soldaki kapi kapanir.
    out_l(cv) / out_r(cv): soldaki / sagdaki vagonun penceresinin ardi (varsayilan gece). lamp_l 0..1: soldaki vagonun lambasi. hi: (sol, sag) levha kirmizi yanar.
    gone_l: soldaki vagon yok (bos ray); koruk kisalir, ucunda kuyruk lambasi yanar"""
    cv.clear(col((8, 12, 24)))
    with stage(cv):
        night(cv, scroll, k)
        track(cv, scroll)
        jl, jr = jit(k, shake), jit(k + 3, shake)
        for sd, (dx_, dy_), no in ((-1, jl, nos[0]), (1, jr, nos[1])):
            if sd < 0 and gone_l: continue
            lon = clamp(lamp_l) if sd < 0 else 1.0
            cv.save(); cv.translate(dx_, dy_)
            xa, xb = (-700, GL) if sd < 0 else (GR, 1800); ex = GL if sd < 0 else GR
            cv.drawRRect(RRXY(LTRB(xa - 14, ROOF - 46, xb + 14, CEIL), 40, 40), fill((24, 34, 48)))
            cv.drawRect(LTRB(xa, CEIL, xb, WF), fill(WALLC)); cv.drawRect(LTRB(xa, 1010, xb, WF), fill(WAINS)); cv.drawLine(xa, 1022, xb, 1022, dashed(shade(WAINS, 1.5), 4, 190, (18, 14)))
            wx = ex - 560 if sd < 0 else ex + 280
            wr = RRXY(LTRB(wx, WY0, wx + 280, WY1), 26, 26)
            cv.save(); cv.clipRRect(wr, True); cv.translate(-dx_, -dy_)
            if sd < 0 and out_l: out_l(cv)
            elif sd > 0 and out_r: out_r(cv)
            else: night(cv, scroll, k)
            cv.restore()
            cv.drawRRect(wr, stroke(BRASS, 9))
            lx = ex + sd * 420
            if lon > 0.02: poly(cv, [(lx - 50, CEIL + 30), (lx + 50, CEIL + 30), (lx + 230, WF), (lx - 230, WF)], LAMPC, 24 * lon)
            cv.drawRRect(RRXY(LTRB(lx - 58, CEIL - 4, lx + 58, CEIL + 30), 15, 15), fill(lerpt((58, 62, 72), LAMPC, lon)))
            cv.drawRect(LTRB(xa, WF, xb, FEDGE), fill((84, 44, 54))); cv.drawRect(LTRB(xa, WF + 36, xb, FEDGE - 24), fill((122, 60, 72)))
            cv.drawRect(LTRB(xa, FEDGE, xb, FEDGE + 64), fill((26, 30, 42)))
            cv.drawRect(LTRB(ex - 22, CEIL, ex + 22, 668), fill((26, 34, 46)))                 # kapi ustu (uc duvarin kesiti)
            plate(cv, ex + sd * 118, 612, f'VAGON {no}', hi[0 if sd < 0 else 1], k, sc_=0.8)
            bx = ex + sd * 330
            for wx_ in (-90, 90):
                cv.drawCircle(bx + wx_, 1508, 62, fill((36, 40, 54))); cv.drawCircle(bx + wx_, 1508, 50, stroke((124, 132, 154), 5)); cv.drawCircle(bx + wx_, 1508, 13, fill((170, 60, 64)))
                for j in range(4):
                    a_ = scroll / 62 + j * math.pi / 2; cv.drawLine(bx + wx_, 1508, bx + wx_ + math.cos(a_) * 48, 1508 + math.sin(a_) * 48, stroke((124, 132, 154), 5))
            cv.restore()
        # koruk: karanlik kumas, kaburgalar, sallanan fener
        bl = (590 if gone_l else GL + 22) + jl[0]             # korugun sol ucu (vagon yoksa kisalmis)
        cv.drawRect(LTRB(bl, 668 + jl[1], GR - 22 + jr[0], FEDGE + 30), fill((16, 20, 32)))
        n = 4 if gone_l else 9
        for j in range(n + 1):
            f = j / n; x = lerp(bl, GR - 22 + jr[0], f); dy_ = lerp(jl[1], jr[1], f)
            cv.drawLine(x, 668 + dy_, x, FEDGE + 30 + dy_, stroke((40, 46, 64), 6, cap=False))
        zz = skia.Path(); zz.moveTo(bl, 668 + jl[1])
        for j in range(1, 2 * n + 1):
            f = j / (2 * n); zz.lineTo(lerp(bl, GR - 22 + jr[0], f), 668 + lerp(jl[1], jr[1], f) - (26 if j % 2 else 0))
        zz.lineTo(GR - 22 + jr[0], 668 + jr[1]); zz.close(); cv.drawPath(zz, fill((26, 32, 48)))
        sw = 16 * math.sin(k * 0.55) * (0.3 + shake / 6.0)
        lx0_ = 690 if gone_l else 540
        lx_, ly_ = lx0_ + sw * 2.2, 760
        cv.drawLine(lx0_, 668, lx_, ly_ - 26, stroke((90, 96, 116), 4))
        poly(cv, [(lx_ - 34, ly_ + 22), (lx_ + 34, ly_ + 22), (lx_ + 200, FEDGE), (lx_ - 200, FEDGE)], AMBER, 26)
        gl = fill(AMBER, 150); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22)); cv.drawCircle(lx_, ly_, 40, gl)
        cv.drawRRect(RRXY(LTRB(lx_ - 22, ly_ - 26, lx_ + 22, ly_ + 24), 9, 9), fill((255, 226, 150))); cv.drawRRect(RRXY(LTRB(lx_ - 22, ly_ - 26, lx_ + 22, ly_ + 24), 9, 9), stroke((60, 50, 40), 5))
        for (xa, xb, (dx_, dy_)) in (((590, GR + 10, jr),) if gone_l else ((GL - 10, 570, jl), (510, GR + 10, jr))):   # ust uste binen iki sac levha
            cv.drawRect(LTRB(xa + dx_, WF + 34 + dy_, xb + dx_, FEDGE + dy_), fill((84, 90, 108))); cv.drawLine(xa + dx_, WF + 46 + dy_, xb + dx_, WF + 46 + dy_, dashed((150, 156, 176), 3, 190, (12, 10)))
        cv.drawRect(LTRB(580 if gone_l else GL - 30, FEDGE + 20, GR + 30, FEDGE + 54), fill((14, 16, 26)))
        if gone_l:                                          # acik uc: kuyruk lambasi
            gl = fill(REDL, 150); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26)); cv.drawCircle(bl - 6, 1120, 40, gl)
            cv.drawCircle(bl - 6, 1120, 15, fill((255, 120, 104)))
        if closed > 0 and not gone_l:                                      # soldaki kapi kapanir (kesitte kalin bir kanat)
            h = (WF - 668) * clamp(closed)
            cv.drawRect(LTRB(GL - 16 + jl[0], WF - h + jl[1], GL + 16 + jl[0], WF + jl[1]), fill((98, 62, 52))); cv.drawRect(LTRB(GL - 16 + jl[0], WF - h + jl[1], GL + 16 + jl[0], WF + jl[1]), stroke(BRASS, 3, cap=False))
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kSoftLight); p.setAlphaf(0.4); cv.drawImage(noise_img(), 0, 0, LIN, p)


# ---------- dekor: vagonun arka kapisi (karsidan) ----------
D0, D1, DT = 340, 740, 640
def rear_view(cv, g, gone=1.0, fog_a=0.0, scroll=0.0, k=0):
    """arka kapinin camindan gorunen: gone 0: arkadaki vagonun (isiklari sonmus) on yuzu; gone 1: bos ray. fog_a: camdaki sis"""
    cx, vy = g.centerX(), g.top() + g.height() * 0.40
    p = skia.Paint(); p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, g.top()), skia.Point(0, vy)], [col((10, 14, 34)), col((34, 54, 96))]))
    cv.drawRect(g, p)
    for i in range(9): cv.drawCircle(g.left() + (i * 67 + 30) % g.width(), g.top() + 12 + (i * 29) % (g.height() * 0.3), 2.5, fill((236, 232, 210), 200))
    cv.drawRect(LTRB(g.left(), vy, g.right(), g.bottom()), fill((14, 20, 36)))
    for j in range(9):                                      # traversler: geriye bakiyoruz, uzaklasirlar
        f = (((j - scroll / 90.0) % 9) / 9.0) ** 2
        y = lerp(vy, g.bottom(), f); hw = lerp(10, g.width() * 0.5, f); cv.drawLine(cx - hw, y, cx + hw, y, stroke((70, 60, 64), 2 + 10 * f, cap=False))
    for sd in (-1, 1): cv.drawLine(cx + sd * 5, vy, cx + sd * g.width() * 0.40, g.bottom(), stroke((150, 158, 180), 6))
    gl = fill(REDL, 150); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)); cv.drawCircle(cx + 62, vy - 22, 9, gl); cv.drawCircle(cx + 62, vy - 22, 4, fill((255, 150, 130)))
    if gone < 1:
        a = 255 * (1 - gone)
        cv.drawRect(LTRB(g.left() + 10, g.top() + 8, g.right() - 10, g.bottom() + 40), fill((60, 28, 38), a))
        cv.drawRect(LTRB(cx - 70, g.top() + 50, cx + 70, g.bottom() + 40), fill((34, 22, 30), a)); cv.drawRRect(RRXY(LTRB(cx - 44, g.top() + 80, cx + 44, g.top() + 220), 10, 10), fill((10, 12, 26), a))
        cv.drawRect(LTRB(g.left() + 10, g.top() + 8, g.right() - 10, g.top() + 40), fill((20, 24, 36), a))
    if fog_a > 0:
        cv.drawRect(g, fill((178, 190, 214), 215 * clamp(fog_a)))
        for i in range(5):
            p = fill((226, 232, 244), 120 * clamp(fog_a)); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26))
            cv.drawCircle(g.left() + ((i * 97 + k * 3) % int(g.width() + 120)) - 60, g.top() + 60 + (i * 71) % int(g.height() - 60), 70, p)


def fwd_glass(cv, g, k=0):
    """on kapinin caminin ardi: ondeki vagonun isikli koridoru (perspektif)"""
    cx, cy, w, h = g.centerX(), g.top() + g.height() * 0.46, g.width(), g.height()
    cv.drawRect(g, fill((236, 204, 136)))
    poly(cv, [(g.left(), g.bottom()), (g.right(), g.bottom()), (cx + w * 0.10, cy + h * 0.16), (cx - w * 0.10, cy + h * 0.16)], (150, 74, 84))
    for sd in (-1, 1):
        poly(cv, [(cx + sd * w * 0.5, g.top()), (cx + sd * w * 0.12, cy - h * 0.2), (cx + sd * w * 0.12, cy + h * 0.16), (cx + sd * w * 0.5, g.bottom())], shade(WALLC, 1.25))
        for j, f in enumerate((0.92, 0.6, 0.36)):
            x = cx + sd * w * (0.12 + 0.38 * f); y0 = cy + h * (0.02 + 0.2 * f); y1 = cy + h * (0.16 + 0.34 * f)
            cv.drawRRect(RRXY(LTRB(min(x, x - sd * w * 0.13 * f), y0, max(x, x - sd * w * 0.13 * f), y1), 6, 6), fill(shade(SEATC, 0.8 + 0.2 * f)))
    cv.drawRect(LTRB(cx - w * 0.07, cy - h * 0.2, cx + w * 0.07, cy + h * 0.16), fill((70, 46, 44)))
    for j, f in enumerate((0.9, 0.55, 0.28)):
        cv.drawOval(LTRB(cx - w * 0.16 * f, g.top() + h * (0.04 + 0.2 * (1 - f)), cx + w * 0.16 * f, g.top() + h * (0.09 + 0.2 * (1 - f))), fill((255, 244, 206)))


def loco_glass(cv, g, k=0):
    """lokomotifin kapisinin ardi: karanlik, komur yigini, ocak isigi"""
    cx, w, h = g.centerX(), g.width(), g.height()
    cv.drawRect(g, fill((10, 12, 20)))
    fl = 0.75 + 0.25 * math.sin(k * 0.9) * math.sin(k * 0.37)
    gl = fill((255, 120, 50), 210 * fl); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, w * 0.16)); cv.drawCircle(cx, g.bottom() - h * 0.34, w * 0.26, gl)
    cv.drawRRect(RRXY(LTRB(cx - w * 0.2, g.bottom() - h * 0.48, cx + w * 0.2, g.bottom() - h * 0.2), w * 0.08, w * 0.08), fill((255, 190, 90), 255 * fl))
    cv.drawRRect(RRXY(LTRB(cx - w * 0.2, g.bottom() - h * 0.48, cx + w * 0.2, g.bottom() - h * 0.2), w * 0.08, w * 0.08), stroke((30, 30, 40), w * 0.04))
    for j in range(7): cv.drawCircle(g.left() + w * (0.08 + 0.14 * j), g.bottom() - h * (0.05 + 0.05 * (j % 3)), w * 0.13, fill((22, 22, 30)))
    for j in range(1, 4):                                   # ocak izgarasi
        x = cx - w * 0.2 + j * w * 0.1; cv.drawLine(x, g.bottom() - h * 0.47, x, g.bottom() - h * 0.21, stroke((30, 30, 40), w * 0.025, cap=False))
    for x in (0.16, 0.3, 0.84): cv.drawLine(g.left() + w * x, g.top(), g.left() + w * x, g.top() + h * (0.5 if x > 0.5 else 0.3), stroke((60, 62, 76), w * 0.04, cap=False))   # borular
    gx, gy_ = g.left() + w * 0.6, g.top() + h * 0.16                                              # tek basinc saati
    cv.drawCircle(gx, gy_, w * 0.08, fill(BRASS)); cv.drawCircle(gx, gy_, w * 0.058, fill((240, 232, 210)))
    a_ = -0.6 + 0.25 * math.sin(k * 0.3); cv.drawLine(gx, gy_, gx + math.sin(a_) * w * 0.045, gy_ - math.cos(a_) * w * 0.045, stroke((170, 40, 40), 3))
    vx, vy = g.left() + w * 0.23, g.top() + h * 0.4                                               # vana carki
    cv.drawCircle(vx, vy, w * 0.07, stroke((170, 60, 64), w * 0.022))
    for j in range(3): cv.drawLine(vx - math.cos(j * 1.047) * w * 0.07, vy - math.sin(j * 1.047) * w * 0.07, vx + math.cos(j * 1.047) * w * 0.07, vy + math.sin(j * 1.047) * w * 0.07, stroke((170, 60, 64), w * 0.014))


def door_view(cv, k=0, gone=1.0, fog_a=0.0, scroll=0.0, plate_hi=0.0, plate_on=1.0, shake=(0, 0), no=5, label=None, glass=None, open_u=0.0, lock=False):
    """vagonun icinden kapiya bakis (karsidan). Varsayilan ARKA kapi: ustunde ardindaki vagonun levhasi (VAGON no), caminda rear_view.
    One bakis icin: label (levha yazisi), glass=fwd_glass ya da loco_glass (camin ardi), open_u 0..1 (kapi saga kayarak acilir),
    lock (kapida asma kilit)"""
    cv.clear(col((16, 26, 34)))
    with stage(cv, *shake):
        cv.drawRect(LTRB(-560, -400, 1640, 2600), fill((84, 44, 54)))
        poly(cv, [(300, WF), (780, WF), (1000, 2600), (80, 2600)], (122, 60, 72))
        for sd in (-1, 1): cv.drawLine(540 + sd * 228, WF + 10, 540 + sd * 440, 2600, dashed((184, 118, 126), 4, 190, (18, 14)))
        for sd in (-1, 1):                                  # yan duvarlar (perspektif), pencere ve koltuk
            xe, xo = 540 + sd * 500, 540 + sd * 1120
            poly(cv, [(xe, CEIL - 20), (xo, 330), (xo, 1640), (xe, WF)], shade(WALLC, 0.82))
            poly(cv, [(xe, 1010), (xo, 1150), (xo, 1640), (xe, WF)], shade(WAINS, 0.86))
            wq = [(xe + sd * 130, 700), (xe + sd * 470, 610), (xe + sd * 470, 1040), (xe + sd * 130, 968)]
            wp = poly(cv, wq, (26, 40, 76)); cv.save(); cv.clipPath(wp, True)
            xx = xe + sd * 130 + ((scroll * 1.3 + (0 if sd < 0 else 170)) % 340) * sd
            cv.drawLine(xx, 560, xx, 1080, stroke((8, 12, 24), 16, cap=False)); cv.restore()
            cv.drawPath(wp, stroke(BRASS, 8))
            poly(cv, [(xe + sd * 30, 990), (xe + sd * 150, 975), (xe + sd * 150, 1290), (xe + sd * 30, WF + 4)], SEATC)
            poly(cv, [(xe + sd * 38, 1000), (xe + sd * 140, 988), (xe + sd * 140, 1048), (xe + sd * 38, 1052)], CREAM, 235)
        cv.drawRect(LTRB(-560, -400, 1640, 332), fill((24, 34, 48))); poly(cv, [(40, CEIL - 20), (1040, CEIL - 20), (1660, 330), (-580, 330)], (24, 34, 48))
        for f_ in (0.2, 0.4, 0.6, 0.8):                    # tavan: perspektifte kirisler ve iki bagaj rafi
            cv.drawLine(lerp(40, -580, f_), lerp(CEIL - 20, 330, f_), lerp(1040, 1660, f_), lerp(CEIL - 20, 330, f_), dashed((60, 80, 100), 3 + 3 * f_, 170, (18, 14)))
        for yy in (250, 130, 10, -110): cv.drawLine(-560, yy, 1640, yy, dashed((60, 80, 100), 6, 150, (22, 16)))
        for xx in (200, 540, 880): cv.drawLine(xx, CEIL - 20, 540 + (xx - 540) * 2.2, 330, stroke((34, 48, 64), 5, cap=False)); cv.drawLine(540 + (xx - 540) * 2.2, 330, 540 + (xx - 540) * 2.2, -400, stroke((34, 48, 64), 5, cap=False))
        for sd in (-1, 1): cv.drawLine(540 + sd * 500, 650, 540 + sd * 1120, 500, stroke(BRASS, 8, cap=False))
        cv.drawRect(LTRB(40, CEIL - 20, 1040, WF), fill(WALLC)); cv.drawRect(LTRB(40, 1010, 1040, WF), fill(WAINS)); cv.drawLine(40, 1022, 1040, 1022, dashed(shade(WAINS, 1.5), 4, 190, (18, 14)))
        cv.drawRect(LTRB(40, WF - 40, 1040, WF), fill(shade(WAINS, 0.72)))
        for xx in (40, 1040): cv.drawLine(xx, CEIL - 20, xx, WF, stroke(shade(WALLC, 0.6), 6, cap=False))
        for lx in (190, 890):                               # iki tavan lambasi
            poly(cv, [(lx - 44, CEIL + 8), (lx + 44, CEIL + 8), (lx + 200, WF), (lx - 200, WF)], LAMPC, 24)
            cv.drawRRect(RRXY(LTRB(lx - 56, CEIL - 26, lx + 56, CEIL + 8), 15, 15), fill(LAMPC))
        cv.drawRect(LTRB(D0 - 22, DT - 22, D1 + 22, WF), fill((26, 34, 46)))
        behind = (lambda g_: glass(cv, g_, k)) if glass else (lambda g_: rear_view(cv, g_, gone, fog_a, scroll, k))
        op = LTRB(D0, DT, D1, WF)
        if open_u > 0: cv.save(); cv.clipRect(op); behind(op); cv.restore()
        cv.save(); cv.clipRect(op); cv.translate((D1 - D0) * 0.96 * clamp(open_u), 0)
        cv.drawRect(LTRB(D0, DT, D1, WF), fill((98, 62, 52))); cv.drawRect(LTRB(D0 + 18, DT + 18, D1 - 18, WF - 16), dashed((170, 120, 96), 3.5, 200))
        g = LTRB(D0 + 56, DT + 50, D1 - 56, 1010); gr = RRXY(g, 20, 20)
        cv.save(); cv.clipRRect(gr, True); behind(g); cv.restore()
        cv.drawRRect(gr, stroke(BRASS, 9)); cv.drawLine(g.left() + 36, g.top() + 90, g.left() + 96, g.top() + 30, stroke((255, 255, 255), 7, 40))
        cv.drawRRect(RRXY(LTRB(D1 - 76, 1050, D1 - 36, 1136), 10, 10), fill(BRASS))
        if lock:                                            # asma kilit
            lx_, ly_ = D1 - 56, 1168
            sk = skia.Path(); sk.addArc(LTRB(lx_ - 17, ly_ - 44, lx_ + 17, ly_ - 6), 180, 180); cv.drawPath(sk, stroke((150, 156, 176), 8))
            cv.drawRRect(RRXY(LTRB(lx_ - 27, ly_ - 24, lx_ + 27, ly_ + 26), 8, 8), fill(BRASS)); cv.drawCircle(lx_, ly_ - 2, 6, fill((40, 30, 24))); cv.drawRect(LTRB(lx_ - 2.5, ly_, lx_ + 2.5, ly_ + 14), fill((40, 30, 24)))
        cv.restore()
        if label: plate(cv, 540, DT - 62, label, plate_hi, k)
        elif plate_on > 0: plate(cv, 540, DT - 62, f'VAGON {no}', plate_hi, k)
        else: cv.drawRRect(RRXY(LTRB(540 - 125, DT - 93, 540 + 125, DT - 31), 12, 12), fill((22, 26, 40)))
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kSoftLight); p.setAlphaf(0.4); cv.drawImage(noise_img(), 0, 0, LIN, p)


# ---------- ortak yardimcilar ----------
_IMG = {}
def noise_img():
    if 'noise' in _IMG: return _IMG['noise']
    surf = skia.Surface(W, H); cv = surf.getCanvas(); cv.clear(skia.Color(128, 128, 128, 255))
    n = skia.Paint(); n.setShader(skia.PerlinNoiseShader.MakeFractalNoise(0.9, 0.9, 3, 6.0)); cv.drawRect(skia.Rect.MakeWH(W, H), n)
    _IMG['noise'] = surf.makeImageSnapshot(); return _IMG['noise']


def scr(x, y):
    """sahne koordinati -> ekran koordinati"""
    return CX + (x - 540) * K, GYD + (y - GY) * K


class zoom:
    """yakin plan: icinde cizilen her sey z kat buyur; sahne noktasi p, sahne noktasi q'ya oturur"""
    def __init__(s, cv, z, p, q=None): s.cv, s.z, s.p, s.q = cv, z, p, q or p
    def __enter__(s):
        px, py = scr(*s.p); qx, qy = scr(*s.q); s.cv.save(); s.cv.translate(qx, qy); s.cv.scale(s.z, s.z); s.cv.translate(-px, -py)
    def __exit__(s, *a): s.cv.restore()


def mouth_of(f):
    """actor() ciktisindan agzin sahne konumu"""
    s = f['s']; return f['head'][0] + f.get('look', 0) * 5 * s, f['head'][1] + 49 * s


def hand_ball(cv, x, y, r, c, seed=3):
    def d(c_): stil.R.seed(seed); yarn_ball(c_, r + 12, r + 12, r, c, rows=5)
    blit(cv, sprite(('hand', round(r, 1), c, seed), 2 * r + 40, 2 * r + 44, d), x - r - 12, y - r - 12)


def reach_pose(x, gy, s, target, base=None, side=1, bend=40):
    """eli sahnedeki bir noktaya (target) uzanan kol pozu. side: 1 sag kol, -1 sol kol"""
    P = dict(IDLE); P.update(base or {}); g = geo(x, gy, s, P); sh = g['sh']
    hx, hy = (target[0] - sh[0]) / s, (target[1] - sh[1]) / s
    out = dict(base or {}); out['aR' if side > 0 else 'aL'] = (hx * 0.5 + side * 0, hy * 0.5 + bend, hx, hy); return out


def badge_at(cv, x, y, txt, red=False, a=1.0, r=36):
    """sahne koordinatinda sayi rozeti"""
    cv.drawCircle(x + 3, y + 5, r, fill((4, 6, 20), 110 * a))
    cv.drawCircle(x, y, r, fill((255, 86, 74) if red else CREAM, 255 * a)); cv.drawCircle(x, y, r - 7, dashed(INKBLUE, 2.5, 150 * a, (7, 6)))
    text(cv, txt, x, y + r * 0.47, r * 1.28, CREAM if red else INKBLUE, a=255 * a)


def sfx_text(cv, x, y, txt, size=54, c=CREAM, rot=-8, a=1.0, rays=True):
    """ses yazisi (TIK, CIT): sessiz izleyen de anlasin"""
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    f = skia.Font(TFB, size); w = f.measureText(txt)
    cv.drawString(txt, -w / 2, 0, f, stroke((14, 16, 44), size * 0.2, 230 * a)); cv.drawString(txt, -w / 2, 0, f, fill(c, 255 * a))
    if rays:
        for an in (-150, -90, -30):
            ax, ay = math.cos(math.radians(an)), math.sin(math.radians(an)) * 0.8
            cv.drawLine(ax * (w / 2 + 14), -size * 0.4 + ay * (size * 0.7), ax * (w / 2 + 34), -size * 0.4 + ay * (size * 1.1), stroke(c, 5, 255 * a))
    cv.restore()


class tint:
    """icinde cizilen her seyi renk matrisinden gecirir (geri donus rengi). m: 20 sayilik satir sirali matris"""
    def __init__(s, cv, m): s.cv, s.m = cv, m
    def __enter__(s):
        p = skia.Paint(); p.setColorFilter(skia.ColorFilters.Matrix(list(s.m))); s.cv.saveLayer(None, p)
    def __exit__(s, *a): s.cv.restore()


def sepia_m(u=1.0, lift=0.06):
    """u: 0 renkli .. 1 tam sepya; lift: soluklastirma (siyahlar acilir)"""
    sp = [0.393, 0.769, 0.189, 0.349, 0.686, 0.168, 0.272, 0.534, 0.131]; idn = [1, 0, 0, 0, 1, 0, 0, 0, 1]
    m = [lerp(a, b, u) * (1 - lift) for a, b in zip(idn, sp)]
    return m[0:3] + [0, lift] + m[3:6] + [0, lift * 0.9] + m[6:9] + [0, lift * 0.7] + [0, 0, 0, 1, 0]


def sat_m(sat=1.2, gain=1.04):
    """doygunluk ve parlaklik (canli, net ani)"""
    r, g, b = 0.213, 0.715, 0.072; out = []
    for i in range(3):
        row = [(1 - sat) * w for w in (r, g, b)]; row[i] += sat
        out += [v * gain for v in row] + [0, 0]
    return out + [0, 0, 0, 1, 0]


def memory_frame(cv, label, c=CREAM, a=1.0):
    """geri donus cercevesi: kenarlari soluk, kosesi yuvarlak fotograf kenarligi ve ust etiket (ekran koordinati)"""
    if a <= 0: return
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), max(W, H) * 0.66,
                                  [skia.Color(c[0], c[1], c[2], 0), skia.Color(c[0], c[1], c[2], 0), skia.Color(c[0], c[1], c[2], int(150 * a))]))
    cv.drawRect(skia.Rect.MakeWH(W, H), g)
    th = 30 if FMT == 'v' else 24
    inner_ = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(th, th, W - th, H - th), 54, 54)
    p = skia.Path(); p.addRect(skia.Rect.MakeWH(W, H)); p.addRRect(inner_); p.setFillType(skia.PathFillType.kEvenOdd)
    cv.drawPath(p, fill(c, 255 * a)); cv.drawRRect(inner_, dashed(shade(c, 0.62), 3.5, 220 * a, (16, 12)))
    f = skia.Font(TFB, 38 if FMT == 'v' else 30); w = f.measureText(label); hgt = f.getSize() * 1.9
    x, y = (W / 2, 392) if FMT == 'v' else (60 + (w + 56) / 2, 118)
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - w / 2 - 28, y, x + w / 2 + 28, y + hgt), hgt / 2, hgt / 2), fill((255, 110, 96), 245 * a))
    cv.drawString(label, x - w / 2, y + hgt * 0.68, f, fill(CREAM, 255 * a))


def flash(cv, a, c=(255, 250, 236)):
    if a > 0: cv.drawRect(skia.Rect.MakeWH(W, H), fill(c, 255 * clamp(a)))



# ============ kare dongusu ve komutlar ============
def run(DRAW, no_tag=None, white=(), sine=None, hud=None):
    """DRAW: {sahne_no: cizim_fonksiyonu(cv, t)}. no_tag: ust etiketin gizlenecegi sahneler (varsayilan: son sahne).
    white: [(sahne, sonraki_sahne)] bu gecislerde kararma yapilmaz (sahneler kendi beyaz parlamasini cizer: geri donus; ya da sert kesme).
    hud(cv, t, sahne_no): kameradan ve isiktan SONRA ekran koordinatinda cizilir (sayac gibi kirpilmamasi gereken gostergeler).
    Ilk 2 saniye kancadir (KIT kural 16): bolum kararmadan acilmaz ve ust etiket (dizi adi) 2. saniyeden once gorunmez."""
    KS = sorted(TL.scenes); no_tag = no_tag or (KS[-1],)
    def bounds(k):
        """sahnenin 12 fps kare araligi (cift sayiya yuvarlanir: 30 fps'e tam oturur)"""
        a, b = TL.span(k); return 2 * round(a * STEP / 2), (2 * round(b * STEP / 2) if k != KS[-1] else 2 * math.ceil(TL.total * STEP / 2))
    def scene_of(t):
        k = KS[0]
        for s_ in KS:
            if t >= bounds(s_)[0] / STEP - 1e-6: k = s_
        return k
    SINE = sine or {}
    def frame(cv, t, k=None):
        k = k or scene_of(t)
        if not sinema.ON:
            DRAW[k](cv, t)
        else:                                                # sinema katmani: kamera + isik (motor/sinema.py)
            opt = dict(SINE.get(k, {})); opt.setdefault('mood', DEFAULT_MOOD)
            if k == KS[-1]: opt.setdefault('cam', 'genis')   # bitis karti kirpilmasin
            a_, b_ = bounds(k)[0] / STEP, bounds(k)[1] / STEP
            if k not in sinema.CAM.scene_light:
                cv.save(); DRAW[k](cv, a_ + 0.6); cv.restore()
                sinema.CAM.scene_light[k] = sinema.find_light(surf.makeImageSnapshot())
            z, x_, y_ = sinema.CAM.plan(k, KS.index(k), a_, b_, t, TL.who(t), opt)
            cv.save(); cv.clear(skia.Color(0, 0, 0)); sinema.Camera.apply(cv, z, x_, y_); DRAW[k](cv, t); cv.restore()
            sinema.light_pass(cv, surf, kk(t), sinema.CAM.scene_light[k], opt)
        if hud: hud(cv, t, k)
        tb = TL.beats.get('title')
        if not (tb and tb[0] <= t < tb[1]) and k not in no_tag and t >= 2.0: tag(cv, TITLE, EP)
        for lid, off in getattr(_sen, 'ABONE', []): abone(cv, t, S(lid) + off)   # abone ol bandi (senaryo.ABONE)
        (sinema.captions if sinema.ON else captions)(cv, TL, t)
        a, b = bounds(k)[0] / STEP, bounds(k)[1] / STEP
        i = KS.index(k)
        fi = 1.0 if i > 0 and (KS[i - 1], k) in white else seg(t, a, a + 0.25)
        fo = 1.0 if i + 1 < len(KS) and (k, KS[i + 1]) in white else 1 - seg(t, b - 0.25, b)
        f = min(fi, fo)
        if k == KS[-1]: f = min(fi, 1 - seg(t, TL.total - 0.6, TL.total - 0.05))
        if k == KS[0]: f = fo                                # ilk kare dolu: kararmadan acilir
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
