"""Orgu dunya cizim motoru: sahne donusumu (dikey/yatay), sprite onbellegi, yuzler, karakterler, dekor, altyazi.

Sahneler DIKEY sahne koordinatlarinda yazilir (x 0-1080 ana alan, zemin GY=1330). FMT=h iken ayni sahne
kucultulup 1920x1080 kadrajin ortasina oturur; x<0 ve x>1080 bolgesindeki dekor yalnizca yatayda gorunur.
"""
import math, os, json
import numpy as np, skia
import stil
from stil import (yarn_limb, yarn_ball, thread, blush, fill, stroke, shade, col, star, TFB, TFM,
                  THREAD, CREAM, TEAL, CORAL, LILAC, MUSTARD)

FMT = os.environ.get('FMT', 'v')
W, H = (1080, 1920) if FMT == 'v' else (1920, 1080)
K, CX, GYD = (1.0, 540.0, 1330.0) if FMT == 'v' else (0.74, 960.0, 850.0)
if FMT == 'h' and os.environ.get('STAGE_H'):          # dizi kendi yatay kadrajini verebilir: 'olcek,merkez_x,zemin_y'
    K, CX, GYD = (float(v) for v in os.environ['STAGE_H'].split(','))
GY = 1330
STEP = 12                      # hareket saniyede 12 adim (stop-motion hissi)
YEL = (255, 212, 94)
WHITE = (250, 248, 240)
TONGUE = (236, 96, 110)
CHAR = (74, 70, 92)
INKBLUE = (20, 24, 52)
LIN = skia.SamplingOptions(skia.FilterMode.kLinear)


def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))
def seg(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def smooth(u): u = clamp(u); return u * u * (3 - 2 * u)
def lerp(a, b, u): return a + (b - a) * u
def lerpt(p, q, u): return tuple(lerp(a, b, u) for a, b in zip(p, q))
def mixpose(p, q, u):
    u = smooth(u); out = {}
    for k in set(p) | set(q):
        a, b = p.get(k, IDLE.get(k, 0)), q.get(k, IDLE.get(k, 0))
        out[k] = lerpt(a, b, u) if isinstance(a, tuple) else lerp(a, b, u)
    return out


class stage:
    """sahne koordinatlarini kadraja oturtur"""
    def __init__(s, cv, dx=0, dy=0): s.cv, s.dx, s.dy = cv, dx, dy
    def __enter__(s):
        s.cv.save(); s.cv.translate(CX + s.dx * K, GYD + s.dy * K); s.cv.scale(K, K); s.cv.translate(-540, -GY)
    def __exit__(s, *a): s.cv.restore()


# ---------- sprite onbellegi (golgeli) ----------
_CACHE = {}
def sprite(key, w, h, draw, shadow=True):
    if key in _CACHE: return _CACHE[key]
    pw, ph = int(w * K) + 2, int(h * K) + 2
    surf = skia.Surface(pw, ph); c = surf.getCanvas(); c.clear(0); c.scale(K, K); draw(c)
    img = surf.makeImageSnapshot()
    if shadow:
        q = 4; ss = skia.Surface(pw // q + 2, ph // q + 2); sc = ss.getCanvas(); sc.clear(0)
        p = skia.Paint(); p.setColorFilter(skia.ColorFilters.Blend(skia.Color(4, 6, 20, 255), skia.BlendMode.kSrcIn))
        p.setImageFilter(skia.ImageFilters.Blur(2.4, 2.4))
        sc.scale(1 / q, 1 / q); sc.drawImage(img, 0, 0, LIN, p)
        sh = ss.makeImageSnapshot()
        out = skia.Surface(pw, ph); oc = out.getCanvas(); oc.clear(0)
        oc.save(); oc.translate(11 * K, 17 * K); oc.scale(q, q); pa = skia.Paint(); pa.setAlphaf(0.5); oc.drawImage(sh, 0, 0, LIN, pa); oc.restore()
        oc.drawImage(img, 0, 0)
        img = out.makeImageSnapshot()
    if len(_CACHE) > 70: _CACHE.pop(next(iter(_CACHE)))
    _CACHE[key] = img
    return img


def blit(cv, img, x, y, alpha=1.0):
    cv.save(); cv.translate(x, y); cv.scale(1 / K, 1 / K)
    p = skia.Paint(); p.setAlphaf(clamp(alpha)); cv.drawImage(img, 0, 0, LIN, p); cv.restore()


def text(cv, s, x, y, size, c=CREAM, tf=None, a=255, align='c'):
    f = skia.Font(tf or TFB, size); w = f.measureText(s)
    cv.drawString(s, x - w / 2 if align == 'c' else x, y, f, fill(c, a)); return w


# ---------- yuz ----------
def face(cv, cx, cy, r, expr, talk=None, blink=False, look=0.0):
    s = r / 110.0
    lx, rx, y = cx - 34 * s + look * 6 * s, cx + 34 * s + look * 6 * s, cy - 12 * s
    my = cy + 40 * s; mx = cx + look * 5 * s

    def closed(x, yy, up=False):
        p = skia.Path(); k = -1 if up else 1
        p.moveTo(x - 15 * s, yy + 2 * s * k); p.quadTo(x, yy + 12 * s * k, x + 15 * s, yy + 2 * s * k); thread(cv, p, 8 * s)
    def bead(x, yy, big=1.0):
        if blink: return closed(x, yy)
        cv.drawOval(skia.Rect.MakeLTRB(x - 10 * s * big, yy - 17 * s * big, x + 10 * s * big, yy + 17 * s * big), fill(THREAD))
        cv.drawCircle(x - 3 * s + look * 3 * s, yy - 8 * s, 3.6 * s, fill((255, 255, 255), 220))
    def brow(x, d, y0, y1, w=9):
        b = skia.Path(); b.moveTo(x - 20 * s * d, y + y0 * s); b.lineTo(x + 18 * s * d, y + y1 * s); thread(cv, b, w * s)
    def wide(x):
        if blink: return closed(x, y)
        cv.drawCircle(x, y, 22 * s, fill(WHITE)); cv.drawCircle(x, y, 22 * s, stroke(THREAD, 6 * s))
        cv.drawCircle(x + look * 6 * s, y + 1 * s, 8 * s, fill(THREAD))
    def tear(x, yy, sc_=1.0):
        d = skia.Path(); d.moveTo(x, yy - 20 * s * sc_); d.quadTo(x + 15 * s * sc_, yy + 6 * s * sc_, x, yy + 12 * s * sc_)
        d.quadTo(x - 15 * s * sc_, yy + 6 * s * sc_, x, yy - 20 * s * sc_)
        cv.drawPath(d, fill((150, 215, 245))); cv.drawPath(d, stroke(THREAD, 3.5 * s))
    def wavy(yy, w=8):
        p = skia.Path(); p.moveTo(mx - 34 * s, yy + 4 * s); p.quadTo(mx - 22 * s, yy - 12 * s, mx - 11 * s, yy + 4 * s)
        p.quadTo(mx, yy + 18 * s, mx + 11 * s, yy + 4 * s); p.quadTo(mx + 22 * s, yy - 12 * s, mx + 34 * s, yy + 4 * s); thread(cv, p, w * s)
    def openm(w_, h_, teeth=False):
        rc = skia.Rect.MakeLTRB(mx - w_, my - h_ * 0.35, mx + w_, my + h_ * 1.3)
        cv.drawOval(rc, fill(THREAD)); cv.save(); pth = skia.Path(); pth.addOval(rc); cv.clipPath(pth, True)
        if teeth: cv.drawRect(skia.Rect.MakeLTRB(mx - w_, my - h_, mx + w_, my - h_ * 0.02), fill(WHITE))
        cv.drawOval(skia.Rect.MakeLTRB(mx - w_ * 0.6, my + h_ * 0.7, mx + w_ * 0.6, my + h_ * 1.9), fill(TONGUE)); cv.restore()

    cheeks = True
    if expr in ('mutlu', 'sakin'): bead(lx, y); bead(rx, y)
    elif expr == 'heyecan':
        closed(lx, y, up=True); closed(rx, y, up=True)
    elif expr in ('panik', 'bagir'):
        wide(lx); wide(rx); brow(lx, 1, -30, -46); brow(rx, -1, -30, -46); tear(cx + 80 * s, cy - 50 * s); cheeks = False
    elif expr == 'endise':
        bead(lx, y + 3 * s, .8); bead(rx, y + 3 * s, .8); brow(lx, 1, -24, -40, 8); brow(rx, -1, -24, -40, 8); cheeks = False
    elif expr == 'uzgun':
        bead(lx, y + 4 * s, .8); bead(rx, y + 4 * s, .8); brow(lx, 1, -22, -42, 8); brow(rx, -1, -22, -42, 8)
        tear(lx - 4 * s, y + 44 * s, .7); cheeks = False
    elif expr == 'aglama':
        closed(lx, y); closed(rx, y); brow(lx, 1, -22, -42, 8); brow(rx, -1, -22, -42, 8)
        for x in (lx, rx):
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - 7 * s, y + 12 * s, x + 7 * s, y + 70 * s), 7 * s, 7 * s), fill((150, 215, 245), 230))
        cheeks = False
    elif expr == 'merak':
        bead(lx, y); bead(rx, y, 1.15); brow(rx, -1, -50, -40, 8); brow(lx, 1, -32, -34, 8)
    elif expr == 'saskin': wide(lx); wide(rx)
    elif expr == 'yorgun':
        for x in (lx, rx):
            p = skia.Path(); p.moveTo(x - 17 * s, y); p.lineTo(x + 17 * s, y); thread(cv, p, 10 * s)
            if not blink: cv.drawCircle(x + 4 * s + look * 4 * s, y + 9 * s, 6 * s, fill(THREAD))
        brow(lx, 1, -26, -34, 8); brow(rx, -1, -26, -34, 8); cheeks = False
    elif expr == 'kararli':
        bead(lx, y + 2 * s, .9); bead(rx, y + 2 * s, .9); brow(lx, 1, -42, -24, 10); brow(rx, -1, -42, -24, 10); cheeks = False
    if cheeks:
        blush(cv, cx - 62 * s, cy + 22 * s, 20 * s); blush(cv, cx + 62 * s, cy + 22 * s, 20 * s)

    if expr == 'bagir': return openm(34 * s, 40 * s, teeth=True)
    if talk is not None:
        o = clamp(talk)
        if o < 0.12:
            p = skia.Path(); p.moveTo(mx - 20 * s, my + 2 * s); p.quadTo(mx, my + 8 * s, mx + 20 * s, my + 2 * s); thread(cv, p, 8 * s)
        else: openm((20 + 8 * o) * s, (8 + 26 * o) * s, teeth=o > 0.5)
        return
    p = skia.Path()
    if expr == 'mutlu':
        p.moveTo(mx - 30 * s, my - 6 * s); p.quadTo(mx, my + 24 * s, mx + 30 * s, my - 6 * s); thread(cv, p, 9 * s)
    elif expr == 'sakin':
        p.moveTo(mx - 15 * s, my + 7 * s); p.lineTo(mx + 15 * s, my + 7 * s); thread(cv, p, 8 * s)
    elif expr == 'heyecan': openm(30 * s, 24 * s, teeth=True)
    elif expr in ('panik', 'endise'): wavy(my)
    elif expr == 'uzgun':
        p.moveTo(mx - 24 * s, my + 12 * s); p.quadTo(mx, my - 8 * s, mx + 24 * s, my + 12 * s); thread(cv, p, 8 * s)
    elif expr == 'aglama': openm(22 * s, 18 * s)
    elif expr == 'merak': cv.drawOval(skia.Rect.MakeLTRB(mx - 9 * s, my - 2 * s, mx + 9 * s, my + 16 * s), fill(THREAD))
    elif expr == 'saskin':
        cv.drawOval(skia.Rect.MakeLTRB(mx - 15 * s, my - 4 * s, mx + 15 * s, my + 34 * s), fill(THREAD))
        cv.drawOval(skia.Rect.MakeLTRB(mx - 8 * s, my + 14 * s, mx + 8 * s, my + 32 * s), fill(TONGUE))
    elif expr == 'yorgun':
        p.moveTo(mx - 22 * s, my + 8 * s); p.quadTo(mx, my + 2 * s, mx + 24 * s, my + 10 * s); thread(cv, p, 8 * s)
    elif expr == 'kararli':
        p.moveTo(mx - 20 * s, my + 8 * s); p.lineTo(mx + 20 * s, my + 6 * s); thread(cv, p, 9 * s)


# ---------- karakter ----------
IDLE = dict(aL=(-100, 170, -120, 300), aR=(100, 170, 120, 300), bob=0, lean=0, crouch=0, belly=0,
            kL=(-70, -130), fL=(-84, -18), kR=(70, -130), fR=(84, -18))
SIT = dict(crouch=175, kL=(-120, -100), fL=(-185, -18), kR=(120, -100), fR=(185, -18))


def geo(x, gy, s, P):
    HR = 118 * s; bob = P['bob'] * s; cr = P['crouch'] * s
    hip = (x, gy - 250 * s + bob * 0.5 + cr)
    neck = (x + P['lean'] * s * 0.6, gy - 520 * s + bob + cr)
    hc = (neck[0] + P['lean'] * s * 0.5, neck[1] - HR * 0.88)
    sh = (neck[0], neck[1] + 40 * s)
    arm = lambda a, side: [(sh[0] + side * 6 * s, sh[1]), (sh[0] + a[0] * s, sh[1] + a[1] * s), (sh[0] + a[2] * s, sh[1] + a[3] * s)]
    leg = lambda k, f: [hip, (x + k[0] * s, gy + k[1] * s), (x + f[0] * s, gy + f[1] * s)]
    mid = ((neck[0] + hip[0]) / 2 + P['belly'] * s, (neck[1] + hip[1]) / 2)
    return dict(HR=HR, hip=hip, neck=neck, hc=hc, sh=sh, mid=mid, armL=arm(P['aL'], -1), armR=arm(P['aR'], 1),
                legL=leg(P['kL'], P['fL']), legR=leg(P['kR'], P['fR']))


def _draw_fig(cv, x, gy, s, c, expr, P, seed, talk, blink, look, scarf, antenna, ant_sw, hood):
    stil.R.seed(seed)
    g = geo(x, gy, s, P); HR, lw = g['HR'], 68 * s
    hip, neck, hc = g['hip'], g['neck'], g['hc']
    yarn_limb(cv, [(neck[0], neck[1] - 10 * s), g['mid'], (hip[0], hip[1] - 4 * s)], lw * 1.14, c)
    for L, sd in ((g['legL'], -1), (g['legR'], 1)):
        yarn_limb(cv, L, lw, c)
        yarn_ball(cv, L[-1][0] + sd * 12 * s, L[-1][1] + 0 * s, 38 * s, c, rows=6)
    if hood:
        cl = skia.Path(); cl.moveTo(neck[0] - 66 * s, neck[1] + 10 * s); cl.lineTo(neck[0] + 66 * s, neck[1] + 10 * s)
        cl.lineTo(x + 190 * s, gy - 130 * s); cl.quadTo(x, gy - 96 * s, x - 190 * s, gy - 130 * s); cl.close()
        cv.drawPath(cl, fill((50, 46, 72)))
        ds = stroke((132, 126, 168), 3 * s, 210, cap=False); ds.setPathEffect(skia.DashPathEffect.Make([12 * s, 9 * s], 0))
        hm = skia.Path(); hm.moveTo(x - 172 * s, gy - 148 * s); hm.quadTo(x, gy - 116 * s, x + 172 * s, gy - 148 * s); cv.drawPath(hm, ds)
    yarn_limb(cv, g['armL'], lw * 0.9, c); yarn_limb(cv, g['armR'], lw * 0.9, c)
    yarn_ball(cv, g['armL'][-1][0], g['armL'][-1][1], 33 * s, c, rows=5)
    yarn_ball(cv, g['armR'][-1][0], g['armR'][-1][1], 33 * s, c, rows=5)
    if antenna:
        ax, ay = hc[0] + 20 * s, hc[1] - HR * 0.9
        tip = (ax + (70 + ant_sw * 26) * s, ay - (96 - abs(ant_sw) * 8) * s)
        yarn_limb(cv, [(ax, ay), (ax + (26 + ant_sw * 10) * s, ay - 70 * s), tip], 16 * s, shade(c, 0.85))
        if antenna != 'yok': yarn_ball(cv, tip[0] + 4 * s, tip[1] - 2 * s, 24 * s, antenna, rows=5)
    yarn_ball(cv, hc[0], hc[1], HR, c)
    if scarf:
        sc_, ln, sdir = scarf; n0, n1 = neck
        yarn_limb(cv, [(n0 - 62 * s, n1 + 6 * s), (n0, n1 + 34 * s), (n0 + 62 * s, n1 + 6 * s)], 40 * s, sc_)
        y0 = n1 + 26 * s; floor = gy - 12 * s; drop = min(ln * s, floor - y0)
        pts = [(n0 + 40 * s, y0), (n0 + 68 * s, y0 + drop * 0.5), (n0 + 54 * s, y0 + drop)]
        extra = ln * s - drop
        if extra > 12 * s: pts += [(n0 + 54 * s + sdir * extra * 0.5, floor + 2 * s), (n0 + 54 * s + sdir * extra, floor)]
        yarn_limb(cv, pts, 34 * s, sc_)
    if hood:
        hd = skia.Path(); hd.moveTo(hc[0] - HR * 1.16, hc[1] + HR * 1.0)
        hd.cubicTo(hc[0] - HR * 1.35, hc[1] - HR * 0.6, hc[0] - HR * 0.5, hc[1] - HR * 1.5, hc[0] + HR * 0.15, hc[1] - HR * 1.55)
        hd.cubicTo(hc[0] + HR * 0.9, hc[1] - HR * 1.3, hc[0] + HR * 1.35, hc[1] - HR * 0.4, hc[0] + HR * 1.16, hc[1] + HR * 1.0)
        hd.quadTo(hc[0], hc[1] + HR * 1.3, hc[0] - HR * 1.16, hc[1] + HR * 1.0); hd.close()
        cv.drawPath(hd, fill((50, 46, 72)))
        cv.drawOval(skia.Rect.MakeLTRB(hc[0] - HR * 0.74, hc[1] - HR * 0.66, hc[0] + HR * 0.74, hc[1] + HR * 0.92), fill((14, 12, 26)))
        ds = stroke((132, 126, 168), 3 * s, 210, cap=False); ds.setPathEffect(skia.DashPathEffect.Make([12 * s, 9 * s], 0))
        cv.drawOval(skia.Rect.MakeLTRB(hc[0] - HR * 0.86, hc[1] - HR * 0.78, hc[0] + HR * 0.86, hc[1] + HR * 1.02), ds)
        ey = hc[1] + HR * 0.02; op = 1.0 if talk is None else 0.75 + 0.25 * (1 - talk)
        for sd in (-1, 1):
            ex = hc[0] + sd * HR * 0.3 + look * 8 * s
            cv.save(); cv.translate(ex, ey); cv.rotate(-12 * sd)
            cv.drawOval(skia.Rect.MakeLTRB(-15 * s, -6 * s * op, 15 * s, 6 * s * op), fill((240, 232, 200), 235)); cv.restore()
    elif expr:
        face(cv, hc[0], hc[1] + 6 * s, HR, expr, talk=talk, blink=blink, look=look)


def figure(cv, x, gy, s, c, expr, pose=None, seed=5, talk=None, blink=False, look=0.0, scarf=None, antenna=None, ant_sw=0.0, hood=False, alpha=1.0):
    P = dict(IDLE); P.update(pose or {})
    if talk is not None: talk = round(clamp(talk) * 4) / 4
    q = lambda v: tuple(round(a, 1) for a in v) if isinstance(v, tuple) else round(v, 1)
    key = ('fig', round(s, 3), c, expr, tuple((k, q(P[k])) for k in sorted(P)), seed, talk, blink, round(look, 2),
           (scarf[0], round(scarf[1]), scarf[2]) if scarf else None, antenna, round(ant_sw, 1), hood)
    ox, oy, w, h = 470 * s + 20, 930 * s + 20, 1160 * s + 60, 1000 * s + 60
    img = sprite(key, w, h, lambda c_: _draw_fig(c_, ox, oy, s, c, expr, P, seed, talk, blink, look, scarf, antenna, ant_sw, hood))
    blit(cv, img, x - ox, gy - oy, alpha)
    g = geo(x, gy, s, P)
    return dict(head=g['hc'], HR=g['HR'], handL=g['armL'][-1], handR=g['armR'][-1], neck=g['neck'], hip=g['hip'], mid=g['mid'])


# ---------- dekor ----------
def felt_sky(cv, c0, c1, fibre):
    cv.clear(col(c1))
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeRadial(skia.Point(W * 0.5, H * 0.5), max(W, H) * 0.75, [col(c0), col(c1)]))
    cv.drawRect(skia.Rect.MakeWH(W, H), g)
    n = skia.Paint(); n.setShader(skia.PerlinNoiseShader.MakeFractalNoise(0.9, 0.9, 3, 4.0)); n.setBlendMode(skia.BlendMode.kSoftLight); n.setAlphaf(0.5)
    cv.drawRect(skia.Rect.MakeWH(W, H), n)
    R = stil.R
    for _ in range(2600):
        x, y = R.uniform(0, W), R.uniform(0, H); a = R.uniform(0, math.pi); ln = R.uniform(4, 13)
        cv.drawLine(x, y, x + math.cos(a) * ln, y + math.sin(a) * ln, stroke(fibre, 1.0, R.randint(10, 30)))


def house(cv, x, w, h, body, roof, win, lit):
    y0 = GY - 40 - h
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - w / 2, y0, x + w / 2, GY + 20), 10, 10), fill(body))
    r = skia.Path(); r.moveTo(x - w / 2 - 18, y0 + 6); r.lineTo(x, y0 - w * 0.42); r.lineTo(x + w / 2 + 18, y0 + 6); r.close(); cv.drawPath(r, fill(roof))
    ds = stroke(shade(body, 1.5), 3, 170, cap=False); ds.setPathEffect(skia.DashPathEffect.Make([12, 9], 0))
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - w / 2 + 12, y0 + 14, x + w / 2 - 12, GY + 40), 6, 6), ds)
    r2 = skia.Path(); r2.moveTo(x - w / 2 + 6, y0 - 6); r2.lineTo(x, y0 - w * 0.42 + 24); r2.lineTo(x + w / 2 - 6, y0 - 6); cv.drawPath(r2, ds)
    for i, wx in enumerate((x - w * 0.22, x + w * 0.22)):
        for wy in range(int(y0 + 50), int(GY - 150), 130):
            on = lit and ((i + wy // 130) % 3 != 0)
            cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(wx - 22, wy, wx + 22, wy + 56), 8, 8), fill(win if on or not lit else shade(body, 0.7)))


HOUSES = [(-640, 230, 360), (-380, 200, 250), (-110, 220, 430), (60, 170, 240), (1030, 180, 300), (1220, 230, 440), (1480, 200, 280), (1720, 240, 380)]
_BG = {}
def bg(mode):
    """mode: 'night' | 'day'. Gok + yildiz/bulut + tepe + evler; kadraja gore tam ekran"""
    if mode in _BG: return _BG[mode]
    surf = skia.Surface(W, H); cv = surf.getCanvas(); stil.R.seed(11)
    night = mode == 'night'
    if night: felt_sky(cv, (54, 84, 150), (16, 22, 52), (190, 205, 255))
    else: felt_sky(cv, (164, 212, 240), (92, 160, 214), (255, 255, 255))
    with stage(cv):
        if night:
            for (x, y, r, rot) in ((130, 420, 24, 10), (960, 560, 18, 30), (820, 330, 13, 0), (250, 640, 12, 20), (70, 860, 14, 40), (1010, 900, 12, 5),
                                   (420, 300, 10, 25), (-300, 380, 20, 15), (-560, 620, 13, 0), (-160, 720, 11, 30), (1320, 420, 18, 10), (1560, 300, 12, 40),
                                   (1700, 640, 15, 0), (1250, 760, 10, 20), (-760, 330, 12, 5), (1880, 450, 11, 0)):
                star(cv, x, y, r, rot=rot)
            blit(cv, sprite('moon', 170, 170, lambda c: yarn_ball(c, 80, 80, 58, (240, 226, 170))), 905 - 80, 400 - 80)
        else:
            blit(cv, sprite('sun', 230, 230, lambda c: yarn_ball(c, 110, 110, 84, (250, 200, 80))), 905 - 110, 400 - 110)
            def cloud(c, w):
                p = skia.Path()
                for dx, dy, rr in ((0, 0, 46), (w * 0.3, -22, 56), (w * 0.62, -4, 48), (w * 0.86, 10, 34)): p.addCircle(60 + dx, 80 + dy, rr)
                p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(40, 76, 70 + w * 0.9, 124), 24, 24))
                c.drawPath(p, fill((248, 244, 234)))
            for i, (x, y, w) in enumerate(((120, 330, 240), (-420, 260, 300), (1330, 300, 280), (640, 220, 180), (1700, 520, 220))):
                blit(cv, sprite(('cloud', w), w + 160, 200, lambda c, w=w: cloud(c, w)), x - 60, y - 80, 0.96)
        pal = ([((70, 86, 150), (104, 84, 160)), ((62, 78, 140), (90, 100, 170)), ((80, 92, 158), (120, 92, 166))] if night else
               [((238, 224, 196), (224, 130, 110)), ((180, 220, 214), (96, 150, 190)), ((246, 214, 170), (150, 110, 170))])
        for i, (x, w, h) in enumerate(HOUSES):
            b, r = pal[i % 3]; house(cv, x, w, h, b, r, (250, 214, 120) if night else (150, 196, 226), night)
        hc = (98, 84, 156) if night else (120, 176, 132)
        hill = skia.Path(); hill.moveTo(-2000, GY - 50); hill.quadTo(540, GY - 82, 3000, GY - 50); hill.lineTo(3000, GY + 2000); hill.lineTo(-2000, GY + 2000); hill.close()
        cv.drawPath(hill, fill(hc))
        cv.save(); cv.clipPath(hill, True)
        n = skia.Paint(); n.setShader(skia.PerlinNoiseShader.MakeFractalNoise(0.9, 0.9, 3, 9.0)); n.setBlendMode(skia.BlendMode.kSoftLight); n.setAlphaf(0.5)
        cv.drawRect(skia.Rect.MakeLTRB(-2000, GY - 100, 3000, GY + 2000), n)
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, GY + 40), skia.Point(0, GY + 420)], [skia.Color(20, 16, 50, 0), skia.Color(14, 12, 40, 215)]))
        cv.drawRect(skia.Rect.MakeLTRB(-2000, GY - 100, 3000, GY + 2000), g); cv.restore()
        hs = stroke(shade(hc, 1.7), 4, 200, cap=False); hs.setPathEffect(skia.DashPathEffect.Make([16, 12], 0))
        h2 = skia.Path(); h2.moveTo(-2000, GY - 24); h2.quadTo(540, GY - 56, 3000, GY - 24); cv.drawPath(h2, hs)
    _BG[mode] = surf.makeImageSnapshot()
    return _BG[mode]


# ---------- kule ----------
TX, TTOP, TW = 540, 470, 210
def _tower(c, lit):
    ox, oy = 190, 190                      # yerel: kule ekseni x=ox, cati tepesi y=oy-150+...
    def X(x): return x - TX + ox
    def Y(y): return y - (TTOP - 150) + 40
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(X(TX - TW / 2), Y(TTOP), X(TX + TW / 2), Y(GY + 40)), 14, 14), fill((86, 104, 168)))
    roof = skia.Path(); roof.moveTo(X(TX - TW / 2 - 26), Y(TTOP + 8)); roof.lineTo(X(TX), Y(TTOP - 150)); roof.lineTo(X(TX + TW / 2 + 26), Y(TTOP + 8)); roof.close()
    c.drawPath(roof, fill((122, 96, 170)))
    ds = stroke((206, 214, 246), 3.5, 190, cap=False); ds.setPathEffect(skia.DashPathEffect.Make([14, 10], 0))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(X(TX - TW / 2 + 14), Y(TTOP + 16), X(TX + TW / 2 - 14), Y(GY + 60)), 8, 8), ds)
    r2 = skia.Path(); r2.moveTo(X(TX - TW / 2 + 2), Y(TTOP - 6)); r2.lineTo(X(TX), Y(TTOP - 122)); r2.lineTo(X(TX + TW / 2 - 2), Y(TTOP - 6)); c.drawPath(r2, ds)
    wc = (250, 214, 120) if lit else (56, 70, 126)
    for wy in (860, 1030):
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(X(TX - 30), Y(wy), X(TX + 30), Y(wy + 90)), 30, 30), fill(wc, 235))
        c.drawLine(X(TX), Y(wy + 6), X(TX), Y(wy + 84), stroke((86, 104, 168), 5)); c.drawLine(X(TX - 26), Y(wy + 48), X(TX + 26), Y(wy + 48), stroke((86, 104, 168), 5))
    # balkon (sagda)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(X(TX + TW / 2 - 6), Y(742), X(TX + TW / 2 + 150), Y(764)), 8, 8), fill((122, 96, 170)))
    for bx in (TX + TW / 2 + 30, TX + TW / 2 + 84, TX + TW / 2 + 138):
        c.drawLine(X(bx), Y(690), X(bx), Y(744), stroke((122, 96, 170), 9))
    c.drawLine(X(TX + TW / 2), Y(690), X(TX + TW / 2 + 146), Y(690), stroke((122, 96, 170), 10))
    # saat kadrani
    cx, cy, r = X(TX), Y(640), 74
    c.drawCircle(cx, cy, r + 10, fill((60, 50, 110))); c.drawCircle(cx, cy, r, fill((246, 236, 214)))
    d2 = stroke((150, 130, 190), 3, 220, cap=False); d2.setPathEffect(skia.DashPathEffect.Make([9, 7], 0)); c.drawCircle(cx, cy, r - 9, d2)
    for k in range(12):
        a = k * math.pi / 6; c.drawCircle(cx + math.sin(a) * (r - 22), cy - math.cos(a) * (r - 22), 4 if k % 3 else 6, fill(THREAD))


def hands(cv, cx, cy, hours, sc_=1.0):
    """hours: ondalik saat (19.117 = 19:07)"""
    am = math.radians((hours % 1) * 360); ah = math.radians((hours % 12) * 30)
    cv.drawLine(cx, cy, cx + math.sin(ah) * 34 * sc_, cy - math.cos(ah) * 34 * sc_, stroke(THREAD, 9 * sc_))
    cv.drawLine(cx, cy, cx + math.sin(am) * 52 * sc_, cy - math.cos(am) * 52 * sc_, stroke(CORAL, 6 * sc_))
    cv.drawCircle(cx, cy, 7 * sc_, fill(THREAD))


def tower(cv, hours, lit=True, ang=0.0, drop=0.0, dx=0.0, extra=None):
    """ang: derece (saga yatma), drop: asagi batma. extra(cv): kuleyle birlikte donen cizim (balkondaki Pit vb.)"""
    img = sprite(('tower', lit), 560, 1130, lambda c: _tower(c, lit))
    cv.save(); cv.clipRect(skia.Rect.MakeLTRB(-3000, -3000, 4000, GY - 62))
    cv.translate(TX + dx, GY + 30); cv.rotate(ang); cv.translate(-TX, -(GY + 30) + drop)
    blit(cv, img, TX - 190, TTOP - 150 - 40)
    hands(cv, TX, 640, hours)
    if extra: extra(cv)
    cv.restore()


RUB = 1.45
def _rubble(c):
    c.scale(RUB, RUB)
    R = stil.R; R.seed(31); bx, by = 330, 300
    for i in range(16):
        x = bx + R.uniform(-250, 250); h_ = R.uniform(40, 150) * (1 - abs(x - bx) / 330); w_ = R.uniform(70, 150)
        p = skia.Path(); a = R.uniform(-0.5, 0.5)
        pts = [(-w_ / 2, 0), (-w_ / 2 + R.uniform(0, 20), -h_), (w_ / 2 - R.uniform(0, 30), -h_ * R.uniform(0.6, 1)), (w_ / 2, 0)]
        for j, (px, py) in enumerate(pts):
            qx, qy = x + px * math.cos(a) - py * math.sin(a) * 0.3, by + py
            p.moveTo(qx, qy) if j == 0 else p.lineTo(qx, qy)
        p.close(); c.drawPath(p, fill(R.choice([(86, 104, 168), (76, 92, 152), (122, 96, 170), (96, 112, 176)])))
        ds = stroke((206, 214, 246), 3, 150, cap=False); ds.setPathEffect(skia.DashPathEffect.Make([10, 8], 0)); c.drawPath(p, ds)
    # yan yatmis saat kadrani: 7'yi 7 gece durmus
    c.save(); c.translate(bx + 40, by - 86); c.rotate(24)
    c.drawCircle(0, 0, 84, fill((60, 50, 110))); c.drawCircle(0, 0, 74, fill((246, 236, 214)))
    for k in range(12):
        a = k * math.pi / 6; c.drawCircle(math.sin(a) * 52, -math.cos(a) * 52, 4 if k % 3 else 6, fill(THREAD))
    hands(c, 0, 0, 19 + 7 / 60); c.restore()
    cr = skia.Path(); cr.moveTo(bx + 20, by - 150); cr.lineTo(bx + 44, by - 110); cr.lineTo(bx + 30, by - 84); cr.lineTo(bx + 62, by - 40); c.drawPath(cr, stroke(THREAD, 4))
    for i in range(7):
        yarn_ball(c, bx + R.uniform(-270, 270), by - R.uniform(6, 40), R.uniform(16, 30), R.choice([(206, 214, 246), (122, 96, 170), (236, 226, 200)]), rows=5)
    rf = skia.Path(); rf.moveTo(bx - 250, by); rf.lineTo(bx - 120, by - 120); rf.lineTo(bx - 60, by); rf.close(); c.drawPath(rf, fill((122, 96, 170)))


def rubble(cv, alpha=1.0):
    blit(cv, sprite('rubble', 680 * RUB, 340 * RUB, _rubble), TX - 330 * RUB, GY - 52 - 300 * RUB, alpha)


def dust(cv, u, seed=3):
    """u: 0..1, kulenin dibinden yayilan yun bulutlari"""
    if u <= 0 or u >= 1: return
    R = stil.R; R.seed(seed)
    for i in range(16):
        a = R.uniform(math.pi, 2 * math.pi); d = R.uniform(120, 460) * (1 - (1 - u) ** 2); r = R.uniform(40, 100) * (0.5 + u)
        x, y = TX + math.cos(a) * d * 1.25, GY - 70 + math.sin(a) * d * 0.6
        cv.drawCircle(x, y, r, fill((226, 222, 240), 170 * (1 - u) ** 1.3))


# ---------- esyalar ----------
def _watch(c):
    R = stil.R; R.seed(21)
    yarn_ball(c, 70, 78, 46, MUSTARD, rows=6)
    c.drawCircle(70, 78, 31, fill((246, 236, 214))); c.drawCircle(70, 78, 31, stroke((120, 90, 40), 4))
    for k in range(12):
        a = k * math.pi / 6; c.drawCircle(70 + math.sin(a) * 23, 78 - math.cos(a) * 23, 2.6, fill(THREAD))
    yarn_ball(c, 70, 24, 13, shade(MUSTARD, 0.85), rows=3)
def watch(cv, x, y, hours, sc_=1.0, alpha=1.0):
    cv.save(); cv.translate(x, y); cv.scale(sc_, sc_)
    blit(cv, sprite('watch', 150, 150, _watch), -70, -78, alpha)
    if alpha > 0.5: hands(cv, 0, 0, hours, 0.5)
    cv.restore()


def pompom(cv, x, y, rot=0.0, sc_=1.0):
    cv.save(); cv.translate(x, y); cv.rotate(rot); cv.scale(sc_, sc_)
    blit(cv, sprite('pompom', 90, 90, lambda c: yarn_ball(c, 40, 40, 26, MUSTARD, rows=5)), -40, -40); cv.restore()


# ---------- zaman cizelgesi, ses zarfi, altyazi ----------
class Timeline:
    def __init__(s, path='voice/final.json', wav='voice/voice.wav'):
        import soundfile as sf
        D = json.load(open(path, encoding='utf-8')); s.dry = D.get('dry', False); s.total = D['total']; s.lines = D['lines']; s.beats = {k: tuple(v) for k, v in D['beats'].items()}
        s.scenes = {int(k): v for k, v in D['scenes'].items()}; s.L = {l['id']: l for l in s.lines}
        s.au, s.sr = sf.read(wav, dtype='float32')
        h = int(s.sr * 0.02); n = len(s.au) // h
        e = np.sqrt((s.au[:n * h].reshape(n, h) ** 2).mean(axis=1)); s.env = np.clip(e / (np.percentile(e, 97) + 1e-6), 0, 1)
        s.caps = []
        for i, l in enumerate(s.lines):
            ch = chunks(l['text']); st = s.chunk_times(l['start'], l['end'], ch)
            nxt = s.lines[i + 1]['start'] if i + 1 < len(s.lines) else s.total
            for k, x in enumerate(ch):
                b = st[k + 1] if k + 1 < len(ch) else min(l['end'] + 0.3, nxt - 0.02)
                s.caps.append(dict(a=st[k], b=b, words=x, line=l))
    def S(s, i): return s.L[i]['start']
    def E(s, i): return s.L[i]['end']
    def B(s, n): return s.beats[n]
    def span(s, k):
        ks = sorted(s.scenes); i = ks.index(k); return s.scenes[k], (s.scenes[ks[i + 1]] if i + 1 < len(ks) else s.total)
    def level(s, t):
        i = int(t / 0.02); return float(s.env[max(0, i - 1):i + 3].max()) if 0 <= i < len(s.env) else 0.0
    def talk(s, spk, t):
        """konusan karakter icin agiz acikligi, konusmuyorsa None"""
        for l in s.lines:
            if l['spk'] == spk and l['start'] - 0.03 <= t <= l['end'] + 0.05: return s.level(t)
        return None
    def who(s, t):
        for l in s.lines:
            if l['start'] - 0.03 <= t <= l['end'] + 0.05: return l['spk']
        return None
    def chunk_times(s, t0, t1, ch):
        if len(ch) == 1: return [t0]
        hop = 0.01; x = s.au[int(t0 * s.sr):int(t1 * s.sr)]; h = int(s.sr * hop); n = len(x) // h
        if n < 3: return [t0] * len(ch)
        rms = np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(axis=1) + 1e-12)
        voiced = rms > max(0.008, 0.07 * np.percentile(rms, 95))
        cum = np.concatenate([[0], np.cumsum(voiced)]) * hop
        gaps, i = [], 0
        while i < n:
            if not voiced[i]:
                j = i
                while j < n and not voiced[j]: j += 1
                if (j - i) * hop >= 0.07 and i > 0 and j < n: gaps.append((i * hop, j * hop))
                i = j
            else: i += 1
        w = np.array([syl(c) + 0.12 * sum(ch_.isalpha() for ch_ in ''.join(c)) for c in ch], float)
        tgt = cum[-1] * np.cumsum(w)[:-1] / w.sum(); starts = [t0]
        for v in tgt:
            tb = np.searchsorted(cum, v) * hop
            near = [g for g in gaps if g[1] >= tb - 0.1 and g[0] <= tb + 0.4 and t0 + g[1] > starts[-1] + 0.25]
            on = (min(near, key=lambda g: abs(g[1] - tb))[1] - 0.04 if near else tb + 0.12)
            starts.append(max(starts[-1] + 0.25, t0 + on))
        return starts


VOWELS = set('aeıioöuüâîûAEIİOÖUÜÂÎÛ')
def syl(words): return max(1, sum(ch in VOWELS for ch in ''.join(words)))
def chunks(text, maxc=24):
    out, cur = [], []
    for wd in text.split():
        if cur and len(' '.join(cur + [wd])) > maxc: out.append(cur); cur = []
        cur.append(wd)
        if wd[-1] in '.!?…' and len(' '.join(cur)) > 5: out.append(cur); cur = []
        elif wd[-1] in ',:' and len(' '.join(cur)) > 9: out.append(cur); cur = []
    if cur: out.append(cur)
    if len(out) > 1 and len(' '.join(out[-1])) < 5:
        last = out.pop(); out[-1] += last
    return out


SPK = {'N': ('ANLATICI', (176, 190, 232)), 'T': ('TAN', TEAL), 'P': ('PIT', LILAC), 'Y': ('YABANCI', (150, 146, 170))}
def captions(cv, TL, t):
    cur = None
    for c in TL.caps:
        if c['a'] <= t < c['b']: cur = c
    if not cur: return
    a = seg(t, cur['a'], cur['a'] + 0.08)
    if FMT == 'v': size, cy, maxw, ps, lh = 72, 1560, 920, 30, 96
    else: size, cy, maxw, ps, lh = 58, 1000, 1500, 26, 76
    f = skia.Font(TFB, size); sp = f.measureText(' ') * 1.05
    rows, row = [], []
    for w_ in cur['words']:
        if row and sum(f.measureText(x) for x in row + [w_]) + sp * len(row) > maxw: rows.append(row); row = []
        row.append(w_)
    rows.append(row)
    y = cy - (len(rows) - 1) * lh / 2
    who, pc = SPK[cur['line']['spk']]
    f2 = skia.Font(TFB, ps); pw = f2.measureText(who); py = y - size * 1.42
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(W / 2 - pw / 2 - 24, py - ps * 1.25, W / 2 + pw / 2 + 24, py + ps * 0.55), ps * 0.9, ps * 0.9), fill(pc, 255 * a))
    cv.drawString(who, W / 2 - pw / 2, py, f2, fill(INKBLUE, 255 * a))
    for row in rows:
        wd = [f.measureText(w_) for w_ in row]; x = W / 2 - (sum(wd) + sp * (len(row) - 1)) / 2
        for w_, ww in zip(row, wd):
            if w_ in cur['line']['hl']:
                cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - 10, y - size * 0.86, x + ww + 10, y + size * 0.28), 14, 14), fill(YEL, 255 * a))
                cv.drawString(w_, x, y, f, fill((30, 26, 40), 255 * a))
            else:
                cv.drawString(w_, x, y, f, stroke((14, 16, 44), size * 0.15, 215 * a)); cv.drawString(w_, x, y, f, fill(CREAM, 255 * a))
            x += ww + sp
        y += lh


def tag(cv, title, ep):
    s = f'{title} · {ep}'
    if FMT == 'v': f = skia.Font(TFB, 34); x, y = W / 2, 150
    else: f = skia.Font(TFB, 28); x, y = 60 + (f.measureText(s) + 56) / 2, 44
    w = f.measureText(s); hgt = f.getSize() * 1.9
    cv.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - w / 2 - 28, y, x + w / 2 + 28, y + hgt), hgt / 2, hgt / 2), fill(CREAM, 235))
    cv.drawString(s, x - w / 2, y + hgt * 0.68, f, fill(INKBLUE))


def card(cv, lines, alpha=1.0, sc_=1.0, cy=None):
    """orta kart: lines = [(metin, punto, renk)]"""
    if alpha <= 0: return
    u = (1.0 if FMT == 'v' else 0.86) * sc_
    hh = sum(sz * 1.35 for _, sz, _ in lines) * u + 120 * u
    ww = max(skia.Font(TFB, sz * u).measureText(tx) for tx, sz, _ in lines) + 150 * u
    cx = W / 2; cy = cy if cy is not None else H * (0.42 if FMT == 'v' else 0.45)
    rc = skia.Rect.MakeLTRB(cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2)
    sh = fill((4, 6, 20), 120 * alpha); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
    cv.drawRRect(skia.RRect.MakeRectXY(rc.makeOffset(10, 16), 34, 34), sh)
    cv.drawRRect(skia.RRect.MakeRectXY(rc, 34, 34), fill((30, 36, 78), 250 * alpha))
    ds = stroke((206, 214, 246), 4, 220 * alpha, cap=False); ds.setPathEffect(skia.DashPathEffect.Make([16, 12], 0))
    cv.drawRRect(skia.RRect.MakeRectXY(rc.makeInset(18, 18), 22, 22), ds)
    y = cy - hh / 2 + 60 * u
    for tx, sz, c in lines:
        y += sz * u; text(cv, tx, cx, y, sz * u, c, a=255 * alpha); y += sz * 0.35 * u
