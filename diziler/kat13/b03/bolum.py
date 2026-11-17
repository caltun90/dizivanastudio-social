"""13. Kat, 3. Bolum: Ayna. Yalnizca sahneler; ortak parcalar ../ortak.py icinde.
Yapi: TEK KARAKTERIN GOZUNDEN (Zoe'nin ic sesi). Kanca (suya bakis: iki yansima) -> asansorde suphe ve kural ->
aynali salonda yere bakarak yuruyus, camin icindeki karalti -> sorgu (Leo lobiyi hatirlamaz) -> su birikintisi,
Zoe basini kaldirir: EKRAN AYNA OLUR -> son sahneler camin obur tarafindan (Zoe'nin elleri camda) -> bitis karti.
Yeni mekan: aynali salon (yandan). Yeni gorsel fikirler: inik goz kapaklari (yere bakis), suda dalgalanan yansima,
aynanin icinde yuruyen karalti, ekranin ayna cercevesine donmesi ve camin ardindan bakis, dusunce noktalari."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import *
from senaryo import ABONE_END, KNOCK, DRIP, DROP2, GLOW, FALL

orgu.SPK['I'] = ('ZOE · İÇ SES', CORAL)
# kabinde uc kisi: Zoe arka sirada ortada, Leo ve Luna onde iki yanda (Sam'in yeri bos kalmasin)
CAST['Z'] = dict(CAST['Z'], x=540); CAST['L'] = dict(CAST['L'], x=300); CAST['U'] = dict(CAST['U'], x=790)
LTRB = skia.Rect.MakeLTRB
RRXY = skia.RRect.MakeRectXY
RED = (255, 86, 74)
GOLD = (176, 140, 78)
GLASS0, GLASS1 = (24, 34, 58), (8, 10, 22)
WALLH = (46, 40, 64)
SHADOWC = (38, 36, 56)
WATER = (150, 180, 220)

# ---------- aynali salon: dunya olculeri ----------
MT, MB = 590, 1130                                         # aynalarin ust ve alt kenari
MU, MW, M0 = 440, 300, 420                                 # ayna araligi, ayna genisligi, ilk aynanin dunya x'i
G0, GX1, GX2 = 500, 1190, 1870                             # Zoe'nin durdugu yerler: cikis, cama vurus, su birikintisi
CAM5 = GX2 - 430                                           # su birikintisi sahnesinin sabit kadraji
DOOR = CAM5 + 880                                          # kirmizi kapi (dunya x)
PX, PY = GX2 + 250, NEAR + 22                              # su birikintisinin ortasi
OFF = {'U': (-320, NEAR, 0.54), 'L': (-180, FAR, 0.70), 'Z': (0, NEAR, 0.62)}
SX5 = {w: GX2 + o - CAM5 for w, (o, _, _) in OFF.items()}  # su basindaki sahne konumlari
PHASE = {'U': 0.3, 'Z': 0.15, 'L': 0.7}
HEADZ = (SX5['Z'], 958)                                    # Zoe'nin basi (ayakta)
GLX, GLY = SX5['Z'] + 20, FAR + 34                         # gozlugun dustugu yer

# ---------- bu bolumun pozlari ----------
HOLDB = dict(aL=(-80, 90, -34, 150), aR=(80, 90, 34, 150))      # Luna bereyi gogsunde tutar
STB = dict(crouch=10, lean=10, belly=-12)                       # ayakta, basi one egik
LEANP = dict(crouch=16, lean=24, belly=-16)                     # suya dogru egilir
KNEEL = dict(crouch=96, lean=36, belly=-22, kL=(-104, -104), kR=(112, -100), aL=(-60, 130, -20, 226), aR=(110, 120, 156, 214))
UPR = dict(lean=0, belly=-10)
PICKG = dict(crouch=165, lean=14, belly=-16, kL=(-118, -100), kR=(118, -100))
POINT_L = dict(aL=(-126, 96, -206, 70))
POINT_DOWN = dict(aL=HOLDB['aL'], aR=(74, 150, 100, 268))
HEAD_R = dict(aR=(104, -4, 58, -100))


def wk(w, dist):
    """basi one egik yuruyus (saga)"""
    P = dict(walk(dist, OFF[w][2], 1, hold=w != 'Z', off=PHASE[w]), crouch=10, lean=20)
    if w == 'U': P.update(HOLDB)
    return P


def stand(w, base=STB):
    return dict(base, **HOLDB) if w == 'U' else dict(base)


def people(cv, ts, P, st, order=('L', 'U', 'Z')):
    """P: {kim: (x, gy, s)}; st: {kim: (ifade, poz, bakis[, ek])}. ek: down (goz kapaklari inik, varsayilan True), gl (Leo'nun paketinde gozluk)"""
    out = {}
    for w in order:
        if w not in st or w not in P: continue
        v = st[w]; kw = dict(v[3]) if len(v) > 3 else {}
        down = kw.pop('down', True); gl = kw.pop('gl', False)
        if w == 'L': kw.setdefault('tie', True)
        f = actor(cv, ts, w, v[0], v[1], v[2], place=P[w], **kw)
        if down and not kw.get('back'): lids(cv, f)
        a = kw.get('alpha', 1.0)
        if w == 'U' and not kw.get('back'): beret_at(cv, (f['handL'][0] + f['handR'][0]) / 2, f['handL'][1] + 12, 0.5, a=a)
        if w == 'L' and gl:
            s = P[w][2]; x = (f['handL'][0] + f['handR'][0]) / 2 if not kw.get('pkg_left') else f['handL'][0] + 40 * s
            glasses_at(cv, x + 34 * s, f['handL'][1] + 4 * s - 62 * s - 20 * s, 0.6, rot=-6, a=a)
        out[w] = f
    return out


def think_dots(cv, f, k):
    """ic ses: Zoe'nin basindan yukselen dusunce noktalari"""
    hx, hy = f['head']; r = f['HR']; n = 1 + (k // 4) % 3
    for i, (dx, dy, rr) in enumerate(((0.84, -0.98, 0.10), (1.08, -1.30, 0.15), (1.42, -1.70, 0.22))[:n]):
        cv.drawCircle(hx + dx * r + 2, hy + dy * r + 4, rr * r, fill((4, 6, 20), 110)); cv.drawCircle(hx + dx * r, hy + dy * r, rr * r, fill(CREAM))


def inner(ts): return TL.who(ts) == 'I'


# ---------- dekor: aynali salon (yandan; solda asansor, sagda kirmizi kapi) ----------
def pane_x(i): return M0 + MU * i


def puddle(cv, x, y=None, rx=150):
    y = y or PY
    cv.drawOval(LTRB(x - rx - 10, y - 25, x + rx + 10, y + 25), fill((40, 20, 32)))
    g = skia.Paint(AntiAlias=True); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y - 20), skia.Point(0, y + 20)], [col((34, 52, 86)), col((12, 18, 36))]))
    cv.drawOval(LTRB(x - rx, y - 19, x + rx, y + 19), g)
    cv.drawOval(LTRB(x - rx + 8, y - 14, x + rx - 8, y + 14), dashed(WATER, 2.5, 130, (14, 12)))
    for dx_, w_ in ((-70, 46), (20, 70), (84, 30)): cv.drawLine(x + dx_, y - 5, x + dx_ + w_, y - 5, stroke((200, 222, 250), 3, 120))


def drop_fall(cv, x, t_hit, ts, word=False):
    """tavandan suya dusen damla + halkalar. word: SIP yazisi"""
    d = ts - t_hit
    if -0.36 <= d < 0:
        y = lerp(440, PY - 6, ((d + 0.36) / 0.36) ** 2)
        cv.drawOval(LTRB(x - 6, y - 16, x + 6, y + 4), fill((190, 215, 245))); cv.drawLine(x, y - 30, x, y - 16, stroke((190, 215, 245), 3, 150))
    elif 0 <= d < 0.9:
        for j in range(2):
            u = d / 0.9 - j * 0.22
            if u > 0: cv.drawOval(LTRB(x - 20 - 130 * u, PY - 4 - 16 * u, x + 20 + 130 * u, PY + 4 + 16 * u), stroke((200, 222, 250), 3.5, 210 * (1 - u)))
        if d < 0.25:
            for sd in (-1, 0, 1): cv.drawLine(x + sd * 12, PY - 8, x + sd * 34, PY - 44 * (1 - d / 0.3), stroke((200, 222, 250), 3.5, 220))
        if word and d < 0.6: sfx_text(cv, x + 96, PY - 110, 'ŞIP!', 50 * lerp(0.7, 1.0, smooth(seg(d, 0, 0.15))), (190, 220, 255), rot=8)


def hall(cv, cam, lamp=1.0, k=0, open_u=0.0, inside=None, floor='15'):
    """cam: kadrajin sol kenarindaki dunya x'i. lamp: sayi ya da aplik_no -> parlaklik. inside(cv): aynalarin icine cizilir (cama kirpilir)"""
    lv = lamp if callable(lamp) else (lambda i: lamp)
    cv.clear(col((16, 18, 30)))
    with stage(cv):
        x0, x1 = -520, 1620
        cv.drawRect(LTRB(x0, 440, x1, CFLOOR), fill(WALLH))
        cv.drawLine(x0, 520, x1, 520, dashed(shade(WALLH, 1.5), 3.5, 150, (18, 14)))
        cv.drawRect(LTRB(x0, CFLOOR - 46, x1, CFLOOR), fill(shade(WALLH, 0.7)))
        cv.drawLine(x0, 410, x1, 410, stroke((40, 42, 60), 20, cap=False)); cv.drawLine(x0, 404, x1, 404, stroke((60, 62, 86), 5, cap=False))
        for j in range(int((cam + x0) // 310) - 1, int((cam + x1) // 310) + 2):
            cv.drawRRect(RRXY(LTRB(310 * j - cam - 9, 388, 310 * j - cam + 9, 432), 5, 5), fill((30, 32, 48)))
        cv.drawRect(LTRB(PX - cam - 16, 420, PX - cam + 16, 446), fill((30, 32, 48)))              # damlatan boru eki
        cv.drawRect(LTRB(x0, CFLOOR, x1, 5000), fill((66, 34, 50)))
        cv.drawRect(LTRB(x0, CFLOOR + 50, x1, CFLOOR + 250), fill((88, 44, 60)))
        for yy in (CFLOOR + 62, CFLOOR + 238): cv.drawLine(x0, yy, x1, yy, dashed((150, 94, 106), 3.5, 180, (16, 12)))
        clip = skia.Path(); panes = []
        i0 = int((cam + x0 - M0) // MU) - 1
        for i in range(max(0, i0), i0 + 8):                 # aynalar: yaldizli cerceve, karanlik cam
            if pane_x(i) + MW > DOOR - 60: continue
            sx = pane_x(i) - cam
            if sx > x1 + 20 or sx + MW < x0 - 20: continue
            rc = LTRB(sx, MT, sx + MW, MB)
            cv.drawRRect(RRXY(rc.makeOutset(20, 20).makeOffset(5, 8), 28, 28), fill((10, 10, 22), 150))
            cv.drawRRect(RRXY(rc.makeOutset(20, 20), 28, 28), fill(shade(GOLD, 0.6)))
            cv.drawRRect(RRXY(rc.makeOutset(15, 15), 24, 24), fill(GOLD))
            cv.drawRRect(RRXY(rc.makeOutset(8, 8), 18, 18), dashed(shade(GOLD, 1.5), 2.5, 210, (10, 8)))
            g = skia.Paint(AntiAlias=True); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, MT), skia.Point(0, MB)], [col(GLASS0), col(GLASS1)]))
            cv.drawRRect(RRXY(rc, 12, 12), g)
            clip.addRRect(RRXY(rc, 12, 12)); panes.append((i, sx))
        if inside and panes:
            cv.save(); cv.clipPath(clip, True); inside(cv); cv.restore()
        for i, sx in panes:                                 # camdaki parilti (kamera kaydikca kayar)
            cv.save(); cv.clipRect(LTRB(sx, MT, sx + MW, MB))
            o = ((cam * 0.22 + i * 67) % 260) - 20
            for dx_, w_, a_ in ((o, 46, 22), (o + 80, 16, 15)):
                poly(cv, [(sx + dx_ + 150, MT), (sx + dx_ + 150 + w_, MT), (sx + dx_ - 150 + w_, MB), (sx + dx_ - 150, MB)], (170, 200, 240), a_)
            cv.restore()
        for i in range(max(-1, i0), i0 + 8):                # aynalarin arasinda aplikler
            wx = pane_x(i) + MW + (MU - MW) / 2
            if wx < 380 or wx > DOOR - 40: continue
            lx = wx - cam
            if lx < x0 - 300 or lx > x1 + 300: continue
            on_ = clamp(lv(i))
            poly(cv, [(lx - 30, 720), (lx + 30, 720), (lx + 230, CFLOOR + 150), (lx - 230, CFLOOR + 150)], (250, 236, 190), 18 * on_)
            gl = fill((250, 236, 190), 70 * on_); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)); cv.drawCircle(lx, 690, 64, gl)
            cv.drawRRect(RRXY(LTRB(lx - 9, 706, lx + 9, 772), 5, 5), fill(shade(GOLD, 0.7)))
            cv.drawCircle(lx, 690, 27, fill((250, 236, 190), 255 * (0.2 + 0.8 * on_))); cv.drawCircle(lx, 690, 27, stroke(shade(GOLD, 0.7), 4))
        a0, a1 = LIFT_X[0] - cam, LIFT_X[1] - cam           # asansor (solda, isikli)
        if a1 > x0:
            cv.drawRect(LTRB(a0 - 22, 668, a1 + 22, CFLOOR), fill((30, 34, 48)))
            cv.drawRect(LTRB(a0, 690, a1, CFLOOR), fill((250, 228, 156)))
            cv.drawRect(LTRB(a0 + 14, 706, a1 - 14, CFLOOR), dashed((214, 180, 96), 3, 220))
            cv.drawRRect(RRXY(LTRB((a0 + a1) / 2 - 62, 598, (a0 + a1) / 2 + 62, 656), 10, 10), fill((28, 32, 46)))
            text(cv, floor, (a0 + a1) / 2, 644, 44, RED)
            poly(cv, [(a0, CFLOOR), (a1, CFLOOR), (a1 + 200, CFLOOR + 260), (a0 - 60, CFLOOR + 260)], (250, 228, 156), 34)
        if LIFT_X[0] - cam > x0: cv.drawRect(LTRB(x0, 380, LIFT_X[0] - 40 - cam, 5000), fill((30, 28, 44)))
        d0 = DOOR - cam                                     # salonun sonu: duvar ve kirmizi kapi
        if d0 < x1 + 60:
            cv.drawRect(LTRB(d0 + 250, -400, x1 + 400, 5000), fill((30, 28, 44)))
            cv.drawLine(d0 + 250, 380, d0 + 250, 5000, stroke((58, 54, 80), 6, cap=False))
            rc = LTRB(d0 + 360, MT + 40, d0 + 560, MB - 40)
            cv.drawRRect(RRXY(rc.makeOutset(16, 16), 24, 24), fill(shade(GOLD, 0.55))); cv.drawRRect(RRXY(rc.makeOutset(11, 11), 20, 20), fill(shade(GOLD, 0.85)))
            cv.drawRRect(RRXY(rc, 10, 10), fill(GLASS1)); cv.drawRRect(RRXY(rc.makeOutset(5, 5), 14, 14), dashed(shade(GOLD, 1.4), 2.5, 190, (10, 8)))
            poly(cv, [(d0 + 420, MT + 40), (d0 + 452, MT + 40), (d0 + 392, MB - 40), (d0 + 360, MB - 40)], (170, 200, 240), 16)
            cv.drawRRect(RRXY(LTRB(d0 + 664, 706, d0 + 682, 772), 5, 5), fill(shade(GOLD, 0.55)))
            cv.drawCircle(d0 + 673, 690, 25, fill((250, 236, 190), 120 * clamp(lv(9)))); cv.drawCircle(d0 + 673, 690, 25, stroke(shade(GOLD, 0.6), 4))
            cv.drawRect(LTRB(d0 - 22, 748, d0 + 212, CFLOOR), fill((70, 24, 30)))
            if open_u > 0:                                  # kapinin ardi: yine asansor
                cv.drawRect(LTRB(d0, 770, d0 + 190, CFLOOR), fill((250, 228, 156)))
                cv.drawRect(LTRB(d0 + 14, 786, d0 + 176, CFLOOR), dashed((214, 180, 96), 3, 220))
                cv.drawLine(d0 + 6, 1040, d0 + 184, 1040, stroke((200, 170, 100), 10, cap=False))
                cv.drawRRect(RRXY(LTRB(d0 + 95 - 62, 676, d0 + 95 + 62, 736), 10, 10), fill((28, 32, 46)))
                text(cv, floor, d0 + 95, 723, 44, RED, a=255 * open_u)
                poly(cv, [(d0, CFLOOR), (d0 + 190, CFLOOR), (d0 + 250, CFLOOR + 260), (d0 - 200, CFLOOR + 260)], (250, 228, 156), 40 * open_u)
            dw = 190 * (1 - 0.86 * open_u); dx0 = d0 + 190 - dw
            cv.drawRect(LTRB(dx0, 770, d0 + 190, CFLOOR), fill(shade((204, 54, 58), 1 - 0.32 * open_u)))
            if dw > 70: cv.drawRect(LTRB(dx0 + 18 * dw / 190, 790, d0 + 172, CFLOOR - 18), dashed((255, 170, 160), 3.5, 220))
            cv.drawCircle(dx0 + 34 * dw / 190, 1004, 11, fill(YEL))
            gl = fill((255, 90, 80), 60 * (1 - open_u)); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 40))
            cv.drawRect(LTRB(d0 - 60, 720, d0 + 250, CFLOOR + 40), gl)
            if open_u > 0:
                gw = fill((250, 228, 156), 70 * open_u); gw.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60))
                cv.drawRect(LTRB(d0 - 160, 720, d0 + 230, CFLOOR + 60), gw)
        if x0 - 200 < PX - cam < x1 + 200: puddle(cv, PX - cam)
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, GY + 60), skia.Point(0, GY + 430)], [skia.Color(10, 8, 26, 0), skia.Color(10, 8, 26, 225)]))
        cv.drawRect(LTRB(x0, GY, x1, 5000), g)
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kSoftLight); p.setAlphaf(0.4); cv.drawImage(noise_img(), 0, 0, LIN, p)


def glow_eyes(cv, x, y, op, look=0.0, s=1.25, a=1.0):
    """camin icindeki karanlikta acilan gozler. op: 0 kapali .. 1 acik"""
    if op <= 0.03: return
    gl = fill((240, 232, 200), 46 * a * op); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    cv.drawOval(LTRB(x - 66 * s, y - 26 * s, x + 66 * s, y + 26 * s), gl)
    for sd in (-1, 1):
        cv.save(); cv.translate(x + sd * 30 * s + look * 7 * s, y); cv.rotate(-12 * sd)
        cv.drawOval(LTRB(-19 * s, -8 * s * op, 19 * s, 8 * s * op), fill((240, 232, 200), 240 * a)); cv.restore()


# ---------- kabin kapisinin ardi: aynali salon (perspektif) ----------
_VIEW = dict(glow=0.0)
def mirror_view(cv, near, far, lamp):
    nx0, ny0, nx1, ny1 = near; fx0, fy0, fx1, fy1 = far
    X = lambda sd, f: lerp(nx0 if sd < 0 else nx1, fx0 if sd < 0 else fx1, f)
    Y = lambda f, v: lerp(lerp(ny0, fy0, f), lerp(ny1, fy1, f), v)
    poly(cv, [(nx0, ny0), (nx1, ny0), (fx1, fy0), (fx0, fy0)], (16, 18, 30))
    poly(cv, [(nx0, ny1), (nx1, ny1), (fx1, fy1), (fx0, fy1)], (66, 34, 50))
    poly(cv, [(lerp(nx0, nx1, .3), ny1), (lerp(nx0, nx1, .7), ny1), (lerp(fx0, fx1, .74), fy1), (lerp(fx0, fx1, .26), fy1)], (88, 44, 60))
    fs = [0.0, 0.3, 0.52, 0.68, 0.8, 0.88, 0.94, 1.0]
    for sd in (-1, 1):                                      # iki yanda boydan boya aynalar
        poly(cv, [(X(sd, 0), ny0), (X(sd, 1), fy0), (X(sd, 1), fy1), (X(sd, 0), ny1)], shade(WALLH, 0.85))
        for j, (a, b) in enumerate(zip(fs[:-1], fs[1:])):
            a2, b2 = lerp(a, b, 0.16), lerp(a, b, 0.86)
            pts = [(X(sd, a2), Y(a2, 0.13)), (X(sd, b2), Y(b2, 0.13)), (X(sd, b2), Y(b2, 0.86)), (X(sd, a2), Y(a2, 0.86))]
            pth = poly(cv, pts, lerpt(GLASS0, GLASS1, 0.3 + 0.5 * a))
            m0, m1 = lerp(a2, b2, 0.25), lerp(a2, b2, 0.5)
            poly(cv, [(X(sd, m0), Y(m0, 0.13)), (X(sd, m1), Y(m1, 0.13)), (X(sd, m0), Y(m0, 0.86)), (X(sd, a2), Y(a2, 0.86)), (X(sd, a2), Y(a2, 0.6))], (170, 200, 240), 30 * (1 - a) * lamp)
            cv.drawPath(pth, stroke(shade(GOLD, 1 - 0.45 * a), max(2.0, 11 * (1 - a))))
    for i, f in enumerate((0.34, 0.6, 0.78)):               # tavan lambalari
        xm, y0 = (X(-1, f) + X(1, f)) / 2, Y(f, 0); lw = (X(1, f) - X(-1, f)) * 0.09
        cv.drawOval(LTRB(xm - lw * 2.2, y0 - lw * 0.5, xm + lw * 2.2, y0 + lw * 1.3), fill((250, 236, 190), 40 * lamp))
        cv.drawOval(LTRB(xm - lw, y0, xm + lw, y0 + lw * 0.4), fill((250, 236, 190), 225 * lamp))
    cxm, cym = (fx0 + fx1) / 2, (fy0 + fy1) / 2
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeRadial(skia.Point(cxm, cym), (ny1 - ny0) * 0.52, [skia.Color(6, 8, 20, 215), skia.Color(6, 8, 20, 0)]))
    cv.drawRect(LTRB(nx0, ny0, nx1, ny1), g)
    rc = LTRB(fx0, fy0, fx1, fy1); gw = _VIEW['glow']
    if gw > 0:
        gl = fill((255, 90, 80), 150 * gw); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)); cv.drawRect(rc.makeOutset(30, 30), gl)
    cv.drawRect(rc, fill(shade((204, 54, 58), 0.8 + 0.4 * gw))); cv.drawRect(rc.makeInset((fx1 - fx0) * 0.12, (fy1 - fy0) * 0.08), dashed((255, 170, 160), 2, 220, (6, 5)))
    cv.drawCircle(fx1 - (fx1 - fx0) * 0.24, cym + 4, (fx1 - fx0) * 0.06, fill(YEL))


# ---------- yakin plan: Zoe'nin gozunden su birikintisi ----------
PCX, PCY, PRX, PRY = 540, 1070, 468, 350
DPX, DPY = 560, 1130                                       # damlanin dustugu nokta
_RS = {}
def _pool_path(grow=0):
    n = 40; pts = []
    for i in range(n):
        a = 2 * math.pi * i / n; f = 1 + 0.07 * math.sin(3 * a + 1.0) + 0.045 * math.sin(5 * a + 0.4)
        pts.append((PCX + math.cos(a) * (PRX + grow) * f, PCY + math.sin(a) * (PRY + grow) * f))
    mid = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    p = skia.Path(); p.moveTo(*mid(pts[-1], pts[0]))
    for i in range(n): p.quadTo(pts[i][0], pts[i][1], *mid(pts[i], pts[(i + 1) % n]))
    p.close(); return p


def pool_view(cv, ts, k, drops, a3=0.0, a2=0.0, aq=0.0):
    """drops: damlalarin suya degdigi anlar. a3, a2, aq: '3 KISI', '2 YANSIMA' ve '?' rozetlerinin gorunurlugu.
    Sudaki iki yansimadan biri Zoe'nin; oteki yuzsuz, koyu ve dalgali: kimin oldugu secilmez."""
    cv.clear(col((58, 30, 44)))
    pp = _pool_path()
    with stage(cv):
        cv.drawRect(LTRB(-700, -400, 1800, 2400), fill((80, 40, 56)))
        for yy in range(240, 2000, 260): cv.drawLine(-700, yy, 1800, yy, dashed((128, 76, 92), 3.5, 150, (16, 12)))
        for xx in range(-560, 1800, 330): cv.drawLine(xx, -400, xx, 2400, dashed((128, 76, 92), 3, 90, (16, 12)))
        cv.drawPath(_pool_path(18), fill((48, 24, 36)))
        g = skia.Paint(AntiAlias=True); g.setShader(skia.GradientShader.MakeRadial(skia.Point(PCX, PCY - 90), 540, [col((36, 56, 92)), col((10, 16, 34))]))
        cv.drawPath(pp, g)
    amp = 3.0 + sum(16 * math.exp(-(ts - d) * 1.0) for d in drops if ts >= d)
    if 's' not in _RS: _RS['s'] = skia.Surface(W, H)
    c2 = _RS['s'].getCanvas(); c2.clear(0)
    with stage(c2):
        figure(c2, 748 + 24 * math.sin(ts * 0.9), 1500, 0.88, (44, 56, 88), None, dict(lean=-4, belly=6), 41)
        actor(c2, ts, 'Z', 'merak', dict(lean=6, belly=-8, aL=(-96, 150, -70, 280), aR=(96, 150, 70, 280)), 0, place=(376, 1520, 0.92), talk=None)
    tp = skia.Paint(Color=skia.Color(14, 26, 54, 128)); tp.setBlendMode(skia.BlendMode.kSrcATop); c2.drawRect(skia.Rect.MakeWH(W, H), tp)
    img = _RS['s'].makeImageSnapshot()
    with stage(cv):
        cv.save(); cv.clipPath(pp, True)
        cv.save(); cv.resetMatrix(); hgt = 6; pa = skia.Paint(); pa.setAlphaf(0.92)
        for y in range(0, H, hgt):                           # yansima satir satir saga sola kayar: dalga
            dx = amp * math.sin(y * 0.045 + ts * 5.0) + 0.5 * amp * math.sin(y * 0.11 - ts * 3.1)
            cv.drawImageRect(img, skia.Rect.MakeLTRB(0, y, W, y + hgt), skia.Rect.MakeLTRB(dx, y, W + dx, y + hgt), LIN, pa)
        cv.restore()
        for d in drops:
            age = ts - d
            if 0 <= age < 2.6:
                for j in range(3):
                    u = age - j * 0.24
                    if u > 0: cv.drawOval(LTRB(DPX - 36 - 250 * u, DPY - 28 - 190 * u, DPX + 36 + 250 * u, DPY + 28 + 190 * u), stroke((180, 208, 245), 5, 170 * (1 - age / 2.6)))
        for gx_, gy_, w_ in ((250, 860, 120), (700, 800, 70), (330, 1290, 90), (760, 1320, 130)):
            cv.drawLine(gx_ + 6 * math.sin(ts * 3 + gx_), gy_, gx_ + w_ + 6 * math.sin(ts * 3 + gx_), gy_, stroke((200, 222, 250), 4, 70))
        cv.restore()
        cv.drawPath(pp, dashed(WATER, 4, 150, (18, 14)))
        if aq > 0: badge_at(cv, 748, 790, '?', red=True, a=aq, r=46)
        for a_, bx, num, lab, red in ((a3, 150, '3', 'KİŞİ', False), (a2, 560, '2', 'YANSIMA', True)):
            if a_ <= 0: continue
            f = skia.Font(TFB, 52); wd = f.measureText(lab)
            cv.drawRRect(RRXY(LTRB(bx - 56, 522, bx + 86 + wd, 630), 54, 54), fill(INKBLUE, 215 * a_))
            badge_at(cv, bx, 576, num, red=red, a=a_, r=42)
            text(cv, lab, bx + 58, 595, 52, (255, 150, 140) if red else CREAM, a=255 * a_, align='l')
    dim(cv, 0.16)


# ---------- ekran ayna olur: cerceve, camin soguk isigi, camdaki eller ----------
def mirror_frame(cv, a, inside=0.0):
    """a: cercevenin gorunurlugu. inside 0..1: camin obur tarafindan bakis (daha soguk, kenarlar karanlik)"""
    if a <= 0: return
    th = 40 if FMT == 'v' else 30; A = clamp(a)
    cv.drawRect(skia.Rect.MakeWH(W, H), fill((140, 185, 235), 20 * A + 22 * inside))
    for dx_, w_, al in ((W * 0.20, W * 0.10, 13), (W * 0.40, W * 0.035, 10)):
        poly(cv, [(dx_ + H * 0.22, 0), (dx_ + H * 0.22 + w_, 0), (dx_ + w_ - H * 0.22, H), (dx_ - H * 0.22, H)], (220, 235, 255), al * A)
    if inside > 0:
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.48), max(W, H) * 0.62, [skia.Color(6, 10, 26, 0), skia.Color(6, 10, 26, 0), skia.Color(6, 10, 26, int(170 * inside))]))
        cv.drawRect(skia.Rect.MakeWH(W, H), g)
    inner_ = RRXY(LTRB(th, th, W - th, H - th), 46, 46)
    p = skia.Path(); p.addRect(skia.Rect.MakeWH(W, H)); p.addRRect(inner_); p.setFillType(skia.PathFillType.kEvenOdd)
    cv.drawPath(p, fill(GOLD, 255 * A))
    cv.drawRRect(inner_, stroke(shade(GOLD, 0.5), 7, 255 * A))
    cv.drawRRect(RRXY(LTRB(th * 0.45, th * 0.45, W - th * 0.45, H - th * 0.45), 50, 50), dashed(shade(GOLD, 1.55), 3, 220 * A, (14, 10)))


def hand_pos():
    return ([(130, 1858), (950, 1858)], 112) if FMT == 'v' else ([(-292, 1474), (1372, 1474)], 104)


def glass_hands(cv, bump=(0, 0), dy=0.0, ring=(0, 0)):
    """Zoe'nin cama dayali elleri (ekranin alt koselerinde). bump: vurus ani yukari itme, ring: vurus halkasi 0..1"""
    pos, r = hand_pos()
    with stage(cv):
        for i, (x, y) in enumerate(pos):
            y += dy - bump[i]; sd = -1 if i == 0 else 1
            if ring[i] > 0: cv.drawCircle(x, y - r * 0.5, r * (1.2 + 0.9 * ring[i]), stroke((220, 235, 255), 6, 200 * (1 - ring[i])))
            hs = (1.56, 1.84, 1.78, 1.50) if sd < 0 else (1.50, 1.78, 1.84, 1.56)
            for j in range(4):
                fx_ = x + (j - 1.5) * r * 0.46
                cv.drawLine(fx_, y - r * 0.4, fx_, y - r * hs[j], stroke(shade(CORAL, 0.56), r * 0.42, 255))
                cv.drawLine(fx_, y - r * 0.4, fx_, y - r * hs[j], stroke(shade(CORAL, 0.92), r * 0.32, 255))
            cv.drawLine(x + sd * r * 0.6, y - r * 0.1, x + sd * r * 1.18, y - r * 0.62, stroke(shade(CORAL, 0.56), r * 0.42, 255))
            cv.drawLine(x + sd * r * 0.6, y - r * 0.1, x + sd * r * 1.18, y - r * 0.62, stroke(shade(CORAL, 0.92), r * 0.32, 255))
            hand_ball(cv, x, y, r, CORAL, 3 + i)


def title_card(cv, t):
    tb = B('title'); a = seg(t, tb[0], tb[0] + 0.35)
    if a > 0:
        dim(cv, 0.45 * a)
        card(cv, [(TITLE, 130, (255, 110, 96)), (f'{EP.title()}: {EP_NAME}', 48, CREAM)], a, lerp(0.9, 1.0, smooth(seg(t, tb[0], tb[0] + 0.5))))


# ============ SAHNE 1: kanca (ileriden bir an: su birikintisi) ============
def scene1(cv, t):
    ts, k = step(t), kk(t)
    p0 = B('pool0'); T0, dr = frac('i1', 0.5), frac('i1', 0.75)
    if ts < p0[0] + 0.1:                                     # uc kisi basi egik yurur, suyun basinda durur
        d = -85.0 * max(0.0, T0 - ts); moving = ts < T0
        hall(cv, CAM5, 1.0, k)
        P = {w: (SX5[w] + d, OFF[w][1], OFF[w][2]) for w in OFF}; st = {}
        for w in OFF:
            if moving: st[w] = ('sakin' if w == 'U' else 'endise', wk(w, d + 3000), 0)
            elif w == 'Z': st[w] = ('merak', mixpose(STB, LEANP, seg(ts, dr, dr + 0.4)), 1.5)
            else: st[w] = ('sakin' if w == 'U' else 'endise', stand(w), 0)
        with stage(cv):
            drop_fall(cv, PX - CAM5, dr, ts)
            fs = people(cv, ts, P, st)
            if inner(ts): think_dots(cv, fs['Z'], k)
        dim(cv, 0.26)
    else:                                                    # yakin plan: suda iki yansima
        f3, f2 = frac('i2', 0.36), frac('i2', 0.70)
        pool_view(cv, ts, k, [p0[0] + 0.25], a3=seg(ts, f3, f3 + 0.2), a2=seg(ts, f2, f2 + 0.2))
    title_card(cv, t)


# ============ SAHNE 2: asansor (hatirlatma, suphe, kural) ============
def scene2(cv, t):
    ts, k = step(t), kk(t)
    who = ('Z', 'L', 'U')
    lg, dg, dn = B('lights'), B('ding'), B('down')
    dark = ts < lg[0] + 0.1
    flick = lg[0] + 0.1 <= ts < lg[0] + 0.72
    u = smooth(seg(ts, dg[0] + 0.6, dg[0] + 1.9))
    sh = jit(k, 5 if S('u1') + 0.2 <= ts < dg[0] + 0.15 else 0)
    vt = TL.talk('V', ts); bowed = ts >= dn[0] + 0.35
    _VIEW['glow'] = (0.55 + 0.45 * alt(k, 0, 1, 2)) if on(ts, 'l2', 0.0, 0.5) else 0.0
    cabin(cv, sh, u, lamp=0.8, view=mirror_view)
    LK = dict(lean=-6, belly=-14); HB = HOLDB; q = []
    if ts < S('i5') - 0.05:                                  # hatirlatma: Sam ve Kai gitti
        st = {'Z': ('kararli', {}, 0), 'L': ('uzgun', {}, 0), 'U': ('uzgun', HB, 0)}
    elif on(ts, 'i5', 0.05, 0.25):                           # biri fazla: ya Leo, ya Luna
        a, b = ts >= frac('i5', 0.42), ts >= frac('i5', 0.74)
        st = {'Z': ('merak', HIP, 2.0 if b else (1.5 if a else 0)), 'L': ('endise', {}, 0), 'U': ('sakin', HB, 0)}
        q = (['L'] if a else []) + (['U'] if b else [])
    elif on(ts, 'z1', 0.3, 0.1):
        st = {'Z': ('kararli', HIP, 2.0), 'L': ('endise', {}, 1.5), 'U': ('sakin', HB, -2.0)}
    elif on(ts, 'u1', 0.1, 0.1):
        st = {'Z': ('merak', HIP, 2.0), 'L': ('endise', {}, 1.5), 'U': ('kararli', HB, -2.0)}
    elif ts < dg[0] + 0.5:
        st = {'Z': ('endise', LOOKUP, 0), 'L': ('endise', LK, 0), 'U': ('sakin', dict(HB, **LOOKUP), 0)}
    elif ts < S('v1') - 0.1:                                 # kapi acilir: Zoe ve Luna donup bakar
        st = {'Z': ('sakin', {}, 0, dict(back=True)), 'L': ('saskin', {}, -1), 'U': ('sakin', {}, 0, dict(back=True))}
    elif on(ts, 'v1', 0.1, 0.2):
        ex = 'saskin' if ts >= frac('v1', 0.7) else 'endise'
        st = {'Z': (ex, LOOKUP, 0), 'L': (ex, LK, 0), 'U': ('sakin', dict(HB, **LOOKUP), 0)}
    elif on(ts, 'l1', 0.1, 0.2):                             # Leo arkasindaki aynalari gosterir
        st = {'Z': ('saskin', {}, 0, dict(back=True)), 'L': ('panik', THUMB, 0, dict(pkg_left=True)), 'U': ('sakin', {}, 0, dict(back=True))}
    elif on(ts, 'v2', 0.1, 0.2):
        st = {'Z': ('endise', COWER, 0), 'L': ('endise', COWER_HOLD, 0), 'U': ('sakin', dict(HB, **LOOKUP), 0)}
    elif on(ts, 'u2', 0.1, 0.2):                             # Luna yeri gosterir
        st = {'Z': ('merak', {}, 2.0), 'L': ('endise', {}, 1.5), 'U': ('kararli', POINT_DOWN, 0)}
    elif on(ts, 'i6', 0.1, 0.25):
        st = {'Z': ('merak', HIP, 2.0), 'L': ('endise', {}, 0), 'U': ('sakin', HB, 0)}
    elif on(ts, 'l2', 0.05, 0.2):                            # Leo cikisi gosterir; Zoe ve Luna donup bakar
        st = {'Z': ('sakin', {}, 0, dict(back=True)), 'L': ('kararli', THUMB, 0, dict(pkg_left=True)), 'U': ('sakin', {}, 0, dict(back=True))}
    elif not bowed:
        st = {'Z': ('endise', LOOKUP, 0), 'L': ('endise', LK, 0), 'U': ('sakin', dict(HB, **LOOKUP), 0)}
    else:                                                    # kural basladi: herkes basini egip yere bakar
        st = {'Z': ('endise', STB, 0), 'L': ('endise', dict(STB, lean=-10, belly=12), 0), 'U': ('sakin', dict(STB, **HB), 0)}
    st['L'] = st['L'][:3] + (dict(st['L'][3] if len(st['L']) > 3 else {}, tie=True),)
    with stage(cv, *sh):
        fs = cast(cv, ts, st, who=who)
        if bowed:
            for w in who: lids(cv, fs[w])
        fu = fs['U']
        if not (len(st['U']) > 3 and st['U'][3].get('back')):
            one = st['U'][1] is POINT_DOWN
            beret_at(cv, fu['handL'][0] + (10 if one else 0) if one else (fu['handL'][0] + fu['handR'][0]) / 2, fu['handL'][1] + 12, 0.54)
        if inner(ts) and not dark: think_dots(cv, fs['Z'], k)
        for w in q: badge(cv, w, '?', red=True)
    if dark: dim(cv, 0.94)
    elif flick: dim(cv, 0.94 if (k * 5) % 7 < 3 else 0.3)
    else: dim(cv, lerp(0.2, 0.42, smooth(seg(ts, dn[0] + 0.1, dn[0] + 0.8))))
    display(cv, sh, '15', red=True, level=vt, k=k)
    if dark or (flick and (k * 5) % 7 < 3):
        with stage(cv): dark_eyes(cv, who, red=who[(k // 5) % 3])
    if S('i3') - 0.1 <= ts < E('i5') + 0.12:                 # dort kisi bindi, ikisi gitti; ama uc kisi var
        marks = [(CREAM, 'on'), (CREAM, 'on'), (TAN, 'x' if ts >= frac('i3', 0.28) else 'on'), (NAVY, 'x' if ts >= frac('i3', 0.86) else 'on')]
        if ts >= frac('i4', 0.8): marks.append((RED, 'on'))
        tally(cv, marks)


# ============ SAHNE 3: aynali salon: yere bakarak yuruyus; camin icindeki ============
def scene3(cv, t):
    ts, k = step(t), kk(t)
    ob, fo, kn = B('out'), B('follow'), B('knock')
    W0, W1 = ob[0] + 0.35, kn[0] + KNOCK[0]
    gx = G0 + (GX1 - G0) * seg(ts, W0, W1); cam = gx - 620
    moving = W0 <= ts < W1
    ka = smooth(seg(ts, fo[0] + 0.1, fo[0] + 0.9)) * (1 - smooth(seg(ts, E('i9') - 0.8, E('i9') - 0.1)))
    kx = gx - 600 + 500 * smooth(seg(ts, fo[0], kn[0] + 0.2))          # karalti arkadan yetisir, Leo ile Zoe'nin arasinda durur
    kts = [kn[0] + o for o in KNOCK]
    hitk = any(0 <= ts - x < 0.14 for x in kts); seen = [i for i, x in enumerate(kts) if 0 <= ts - x < 0.32]
    up0, push = kts[2] + 0.12, S('z2') + 0.2

    def inside(c):
        if ka <= 0: return
        x = kx - cam
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeRadial(skia.Point(x, 760), 260, [skia.Color(130, 160, 220, int(110 * ka)), skia.Color(130, 160, 220, 0)]))
        c.drawRect(LTRB(x - 300, MT, x + 300, MB), g)                 # camin icinde soguk bir isik: karalti onun onunde
        if ts < kn[0] + 0.1: P = dict(walk(kx + 3000, 0.72, 1), lean=14)
        else: P = dict(aL=(-66, 170, -44, 300), aR=(120, 40, 196, -36) if hitk else (116, 30, 160, -74), lean=12, belly=-8)
        figure(c, x, 1130, 0.72, (70, 64, 104), None, P, 13, hood=True, look=1.0, alpha=ka * 0.96)
    hall(cv, cam, 1.0 if not hitk else 0.45, k, inside=inside)
    P = {w: (gx + o - cam, gy, s) for w, (o, gy, s) in OFF.items()}; st = {}
    lx = P['L'][0]
    for w in OFF:
        calm = 'sakin' if w == 'U' else 'endise'
        if ts < W0: st[w] = (calm, stand(w), 0)
        elif moving: st[w] = (calm, wk(w, gx - G0), 0)
        elif w == 'U': st[w] = ('sakin', stand(w), 0)        # Luna hic irkilmez
        elif w == 'L':
            if ts < up0: st[w] = ('saskin', COWER_HOLD, 0)
            elif ts < push: st[w] = ('saskin', dict(lean=-10, belly=-14), -1.6, dict(down=False))      # basini kaldiracak olur
            else: st[w] = ('endise', dict(STB, crouch=24), 0)
        else:
            if ts < up0: st[w] = ('saskin', COWER, 0)
            elif ts < E('z2') + 0.15:                        # Zoe, Leo'nun sapkasini asagi bastirir
                tg = (lx + 46, lerp(742, 772, seg(ts, push, push + 0.2)))
                st[w] = ('kararli', reach_pose(P['Z'][0], NEAR, 0.62, tg, dict(STB, lean=-14, belly=6), side=-1, bend=-30), -2.0)
            else: st[w] = ('kararli', stand(w), -1.0 if ts < S('i9') else 0)
    with stage(cv):
        fs = people(cv, ts, P, st)
        if inner(ts): think_dots(cv, fs['Z'], k)
    dim(cv, 0.28)
    with stage(cv):
        hx = kx - cam + 118
        hy = 1130 - 0.72 * 480 - 0.72 * 74
        for i in seen:
            d = ts - kts[i]
            cv.drawCircle(hx, hy, 26 + 90 * d / 0.32, stroke((220, 235, 255), 5, 220 * (1 - d / 0.32)))
            sfx_text(cv, hx + (-70, 60, -10)[i], hy - 86 - 34 * i, 'TAK', 52, YEL, rot=(-10, 8, -4)[i])


# ============ SAHNE 4: sorgu ============
def bubble_q(cv, x, y, a):
    """bos dusunce balonu: Leo lobiyi hatirlamiyor"""
    if a <= 0: return
    r = 96 * lerp(0.7, 1.0, smooth(a)); A = 255 * clamp(a)
    for dx_, dy_, rr in ((-58, 150, 13), (-34, 116, 19)): cv.drawCircle(x + dx_, y + dy_, rr, fill(CREAM, A))
    cv.drawCircle(x + 3, y + 6, r, fill((4, 6, 20), 110 * clamp(a))); cv.drawCircle(x, y, r, fill(CREAM, A)); cv.drawCircle(x, y, r - 9, dashed(INKBLUE, 2.5, 150 * clamp(a), (8, 7)))
    text(cv, 'LOBİ', x, y - 22, 40, INKBLUE, a=A); text(cv, '?', x, y + 62, 84, RED, a=A)


def scene4(cv, t):
    ts, k = step(t), kk(t)
    th, tu, dr = B('think'), B('turnu'), B('drip')
    W0, W1 = tu[0] + 0.2, dr[0] + DRIP - 0.3
    gx = GX1 + (GX2 - GX1) * seg(ts, W0, W1)
    cam = lerp(gx - 620, CAM5, smooth(seg(ts, W1 - 3.2, W1)))           # sonda kirmizi kapi kadraja girer
    moving = W0 <= ts < W1
    hall(cv, cam, 1.0, k)
    P = {w: (gx + o - cam, gy, s) for w, (o, gy, s) in OFF.items()}
    if ts < W0:                                              # duruyorlar; kimse kimsenin yuzune bakmiyor
        Z_ = ('kararli', stand('Z'), -1.2); L_ = ('endise', dict(STB, crouch=20), 0); U_ = ('sakin', stand('U'), 0)
        if on(ts, 'z3', 0.1, 0.15): Z_ = ('kararli', dict(STB, lean=-4, **HIP), -2.0)
        elif on(ts, 'l3', 0.1, 0.15): L_ = ('endise', dict(STB, crouch=20, bob=alt(k, 0, 7, 3)), alt(k, -1.2, 1.2, 4)); Z_ = ('kararli', dict(STB, lean=-4, **HIP), -2.0)
        elif on(ts, 'z4', 0.1, 0.1): Z_ = ('kararli', dict(STB, lean=-6, **POINT_L), -2.0); L_ = ('saskin', dict(STB, crouch=20), 1.0 if ts >= frac('z4', 0.45) else 0)
        elif th[0] - 0.05 <= ts < S('l4') - 0.05: L_ = ('endise', dict(STB, crouch=24, **HEAD_R), 0, dict(pkg_left=True)); Z_ = ('kararli', dict(STB, lean=-4), -2.0)
        elif on(ts, 'l4', 0.05, 0.2): L_ = ('uzgun', dict(STB, crouch=26, lean=4), 0); Z_ = ('merak', dict(STB, lean=-4), -2.0)
        elif ts >= E('l4'): L_ = ('uzgun', dict(STB, crouch=26, lean=4), 0); Z_ = ('merak' if ts < tu[0] else 'kararli', stand('Z'), 0 if ts < tu[0] else -2.0)
    elif moving:
        d = gx - GX1
        Z_ = ('merak' if on(ts, 'i11', 0.1, 0.3) else 'kararli', wk('Z', d), -2.0 if ts < E('u3') + 0.2 else 0)
        L_ = ('uzgun', wk('L', d), 0); U_ = ('sakin', wk('U', d), 1.0 if on(ts, 'u3') else 0)
    else:                                                    # damla: dururlar
        Z_ = ('saskin', stand('Z'), 1.5); L_ = ('endise', stand('L'), 0); U_ = ('sakin', stand('U'), 0)
    with stage(cv):
        drop_fall(cv, PX - cam, dr[0] + DRIP, ts, word=True)
        fs = people(cv, ts, P, {'Z': Z_, 'L': L_, 'U': U_})
        if inner(ts): think_dots(cv, fs['Z'], k)
    dim(cv, 0.28)
    ba = smooth(seg(ts, th[0] + 0.7, th[0] + 1.0)) * (1 - smooth(seg(ts, E('l4') + 0.1, E('l4') + 0.4)))
    if ba > 0:
        with stage(cv): bubble_q(cv, fs['L']['head'][0] + 96, fs['L']['head'][1] - 250, ba)


# ============ SAHNE 5: su birikintisi; Zoe basini kaldirir; ekran ayna olur ============
def scene5(cv, t):
    ts, k = step(t), kk(t)
    lw, rp, rs, se, tk = B('lookw'), B('ripple'), B('raise'), B('see'), B('taken')
    pv0, pv1 = lw[0] + 1.0, S('i16') - 0.12
    d1, d2, d3, d4 = frac('i12', 0.3), frac('i13', 0.9), lw[0] + 1.5, rp[0] + DROP2
    if pv0 <= ts < pv1:                                      # Zoe'nin gozunden su
        f3, f2, fq = frac('i14', 0.3), frac('i14', 0.7), frac('i15', 0.3)
        pool_view(cv, ts, k, [d2, d3, d4], a3=seg(ts, f3, f3 + 0.2), a2=seg(ts, f2, f2 + 0.2), aq=seg(ts, fq, fq + 0.2) * (1 - seg(ts, E('i15') - 0.1, E('i15') + 0.2)))
        return
    T = ts - tk[0]; gl = se[0] + GLOW; wide = T >= 2.25
    fa = smooth(seg(ts, gl, gl + 0.4))
    z = 1.0 if wide else 1.0 + 0.3 * smooth(seg(ts, frac('i16', 0.5), rs[1])) + 0.6 * smooth(seg(ts, gl, gl + 0.7))
    u_ = (z - 1) / 0.9; q = (lerp(HEADZ[0], 540, u_), lerp(HEADZ[1], 900, u_))
    fl = 0 <= T < 2.25 and any(a <= T < a + 0.14 for a in (0.15, 0.5, 0.85))
    lamp = 0.3 if fl else ((0.35 if (k // 2) % 2 else 0.7) if (wide and on(ts, 'v4', 0.1, 0.3)) else (0.62 if wide else 1.0))
    P = {w: (SX5[w], OFF[w][1], OFF[w][2]) for w in OFF}
    rise0 = frac('i16', 0.55)
    # --- Zoe ---
    zdown = True
    if ts < S('i12') - 0.1: Z_ = ('saskin', stand('Z'), 1.5)
    elif ts < lw[0]: Z_ = ('merak' if ts < S('i13') - 0.1 else 'kararli', LEANP, 1.5)
    elif ts < pv0: Z_ = ('merak', mixpose(LEANP, KNEEL, seg(ts, lw[0], lw[0] + 0.8)), 1.5)
    elif ts < rs[0] + 1.0: Z_ = ('kararli', mixpose(KNEEL, UPR, seg(ts, rise0, rs[0] + 0.9)), 1.4 * (1 - seg(ts, rise0, rs[0] + 0.5)))
    elif ts < gl + 0.8: Z_ = ('kararli' if ts < gl else 'merak', UPR, 0); zdown = False
    elif T < 0.55: Z_ = ('saskin', UPR, -1.8 * smooth(seg(ts, gl + 1.2, gl + 1.7))); zdown = False
    else: Z_ = ('panik', dict(UPR, lean=-6, aL=(-110, 60, -150, -40), aR=(110, 60, 150, -40)), 0); zdown = False
    pu = smooth(seg(T, 1.3, 2.2)); za = 1 - seg(T, 1.55, 2.2)
    # --- Leo ---
    if ts < rs[0] + 0.5: L_ = ('endise', stand('L'), 0)
    elif ts < S('l5') - 0.05: L_ = ('panik', stand('L'), 1.2)
    elif ts < E('l5') + 0.25: L_ = ('bagir', dict(STB, aR=(150, 70, 262, 30)), 2.0, dict(pkg_left=True))    # elini uzatir ama bakamaz
    elif not wide: L_ = ('panik', COWER_HOLD, 1.0)
    elif ts < S('v4') - 0.1: L_ = ('panik', COWER_HOLD, 0)
    else: L_ = ('uzgun', dict(STB, crouch=24), 0)
    # --- Luna ---
    if ts < rs[0] + 0.7: U_ = ('sakin', stand('U'), 0)
    elif not wide: U_ = ('endise', stand('U'), 1.5)
    elif ts < S('v4') - 0.1: U_ = ('saskin', dict(COWER_HOLD, **HOLDB), 0)
    else: U_ = ('uzgun', stand('U'), 0)
    with zoom(cv, z, HEADZ, q):
        hall(cv, CAM5, lamp, k)
        with stage(cv):
            for d in (d1, d2): drop_fall(cv, PX - CAM5, d, ts)
            fs = people(cv, ts, P, {'L': L_, 'U': U_}, order=('L', 'U'))
        if za > 0:                                           # ic yakinlastirma sahne donusumunun DISINDA (yatayda da dogru yer)
            with zoom(cv, 1 + 1.5 * pu, HEADZ, (HEADZ[0], HEADZ[1] + 140 * pu)):
                with stage(cv):
                    fz = actor(cv, ts, 'Z', Z_[0], Z_[1], Z_[2], place=P['Z'], alpha=za)
                    if zdown: lids(cv, fz)
                    if inner(ts): think_dots(cv, fz, k)
        with stage(cv):
            if T >= 1.9:                                     # gozluk yere duser
                uf = clamp((T - 1.9) / (FALL - 1.9)); bn = 14 * abs(math.sin((T - FALL) * 9)) * math.exp(-(T - FALL) * 5) if T > FALL else 0
                glasses_at(cv, lerp(HEADZ[0], GLX, uf), lerp(HEADZ[1], GLY, uf * uf) - bn, 0.62, rot=200 * (1 - uf) + 8)
    if fa > 0 and not wide:                                  # aynanin isigi Zoe'nin yuzunde
        qx, qy = scr(*q); g = skia.Paint(); g.setShader(skia.GradientShader.MakeRadial(skia.Point(qx, qy), 520 * K, [skia.Color(190, 220, 255, int(64 * fa)), skia.Color(190, 220, 255, 0)]))
        cv.drawRect(skia.Rect.MakeWH(W, H), g)
    dim(cv, 0.26 + (0.5 if fl else 0) + (0.6 if 2.25 <= T < 2.42 else 0) + 0.12 * (wide and T >= 2.42))
    if 0.45 <= T < 2.25:                                     # karaltinin kollari: aynadan (ekrandan) uzanir
        r_ = smooth(seg(T, 0.5, 1.2)); back = pu
        with stage(cv):
            for sd in (-1, 1):
                c0 = (540 + sd * (640 if FMT == 'v' else 1010), 1500)
                tg = (540 + sd * 150, 1040); e = lerpt(c0, tg, r_ * (1 - 0.75 * back))
                m = ((c0[0] + e[0]) / 2, (c0[1] + e[1]) / 2 - 70 * r_)
                stil.R.seed(60 + sd); yarn_limb(cv, [c0, m, e], 92, SHADOWC); yarn_ball(cv, e[0], e[1], 60, SHADOWC, rows=6)
    mirror_frame(cv, fa, inside=smooth(seg(T, 2.3, 3.2)))


# ============ SAHNE 6: camin obur tarafindan ============
def scene6(cv, t):
    ts, k = step(t), kk(t)
    gb, pk, lv = B('glass'), B('pick'), B('leave')
    m0, m1 = frac('i17', 0.4), E('i17') + 0.1
    grab, up = pk[0] + 1.0, pk[0] + 1.6
    W0, W1 = E('l6') - 0.3, lv[0] + 2.0
    LX1 = GLX - 74; DS = DOOR - CAM5
    wu = seg(ts, W0, W1)
    inn = smooth(seg(ts, S('v5') + 0.4, S('v5') + 1.7))                 # kapidan iceri girerler
    xL = lerp(lerp(lerp(SX5['L'], LX1, seg(ts, m0, m1)), DS - 120, wu), DS + 95, inn)
    xU = lerp(lerp(SX5['U'], DS - 270, wu), DS + 95, inn)
    al = 1 - seg(inn, 0.4, 1.0)
    open_u = smooth(seg(ts, lv[0] + 2.15, lv[0] + 3.0)) * (1 - smooth(seg(ts, E('v5') + 0.1, E('v5') + 0.9)))
    reach = smooth(seg(ts, W1 - 0.1, W1 + 0.2)) * (1 - smooth(seg(ts, lv[0] + 2.5, lv[0] + 2.9)))
    lamp = lerp(0.62, 0.22, smooth(seg(ts, S('i18'), E('i19'))))
    hall(cv, CAM5, lamp, k, open_u)
    P = {'L': (xL, FAR, 0.70), 'U': (xU, NEAR, 0.54)}
    has = ts >= grab
    # --- Leo ---
    if ts < m0: L_ = ('panik' if ts < gb[0] + 0.8 else 'endise', mixpose(COWER_HOLD, STB, seg(ts, gb[0] + 0.9, gb[0] + 1.6)), 0)
    elif ts < m1: L_ = ('uzgun', wk('L', xL - SX5['L']), 0)
    elif ts < pk[0] + 0.3: L_ = ('uzgun', stand('L'), 1.2)
    elif ts < up:                                            # comelir, gozlugu alir
        dn = smooth(seg(ts, pk[0] + 0.3, pk[0] + 0.9)) * (1 - smooth(seg(ts, grab + 0.1, up)))
        base = mixpose(STB, PICKG, dn)
        L_ = ('uzgun', reach_pose(xL, FAR, 0.70, (GLX, GLY - 8), base, side=1, bend=24) if (dn > 0.6 and not has) else base, 1.2, dict(pkg_left=dn > 0.3 and not has))
    elif ts < W0: L_ = ('uzgun', stand('L'), -1.6 if on(ts, 'u4', 0.1, 0.3) else 0)
    elif ts < W1: L_ = ('uzgun', wk('L', xL - LX1), 0)
    elif inn <= 0: L_ = ('kararli', mixpose(dict(HOLD, **STB), dict(aL=HOLD['aL'], aR=(150, 50, 250, 110), lean=18, belly=-8), reach), 0, dict(pkg_left=reach > 0.25))
    else: L_ = ('uzgun', wk('L', xL - LX1), 0)
    L_ = L_[:3] + (dict(L_[3] if len(L_) > 3 else {}, gl=has, alpha=al),)
    # --- Luna ---
    if ts < m0: U_ = ('saskin' if ts < gb[0] + 0.8 else 'uzgun', mixpose(dict(COWER_HOLD, **HOLDB), stand('U'), seg(ts, gb[0] + 0.9, gb[0] + 1.6)), 0)
    elif ts < W0: U_ = ('sakin' if ts >= S('u4') - 0.1 else 'uzgun', stand('U'), 1.5 if ts >= m1 else 0)
    elif ts < W1 or inn > 0: U_ = ('sakin', wk('U', xU - SX5['U']), 0)
    else: U_ = ('sakin', stand('U'), 0)
    U_ = U_[:3] + (dict(alpha=al),)
    with stage(cv):
        if not has: glasses_at(cv, GLX, GLY, 0.62, rot=8)
        if al > 0: people(cv, ts, P, {'L': L_, 'U': U_}, order=('L', 'U'))
    dim(cv, 0.3 + 0.2 * smooth(seg(ts, S('i18'), E('i19'))))
    kn = [gb[0] + o for o in (0.35, 0.6, 0.95, 1.2)]
    bump = [0, 0]; ring = [0, 0]
    for j, x in enumerate(kn):
        d = ts - x
        if 0 <= d < 0.3: ring[j % 2] = d / 0.3
        if 0 <= d < 0.1: bump[j % 2] = 26
    mirror_frame(cv, 1.0, inside=1.0)
    glass_hands(cv, bump, dy=90 * smooth(seg(ts, S('i18') - 0.3, E('i19'))), ring=ring)
    if ts >= S('i18') - 0.1:                                 # dort kisi bindi, ucu gitti; ama kapidan iki kisi gecti
        marks = [(CREAM, 'on'), (NAVY, 'x' if ts >= frac('i18', 0.62) else 'on'), (TAN, 'x' if ts >= frac('i18', 0.76) else 'on'), (CORAL, 'x' if ts >= frac('i18', 0.9) else 'on')]
        if ts >= frac('i19', 0.6): marks.append((RED, 'on'))
        tally(cv, marks)


# ============ SAHNE 7: bitis karti ============
def scene7(cv, t):
    ts, k = step(t), kk(t)
    a0, _ = TL.span(7)
    hall(cv, CAM5, 0.12, k); dim(cv, 0.84)
    eo = smooth(seg(ts, a0 + 0.5, a0 + 1.1)) * (0.25 if (k % 41) in (30, 31) else 1.0)
    with stage(cv): glow_eyes(cv, pane_x(3) - CAM5 + MW / 2, 842, eo, look=alt(k, -1.2, 1.2, 9))        # karsidaki aynada: karalti
    mirror_frame(cv, 1.0, inside=1.0)
    glass_hands(cv, dy=90)
    a = seg(t, a0 + 0.3, a0 + 0.8)
    card(cv, [('Zoe aynada ne gördü?', 62 if FMT == 'v' else 70, CREAM), ('Yorumlara yaz', 40, (176, 190, 232)), ('4. Bölüm: Lobi', 46, (255, 110, 96))], a, cy=450 if FMT == 'v' else 168)
    abone(cv, t, a0 + ABONE_END, pos=(W / 2, 1235) if FMT == 'v' else (W / 2, 770))


if __name__ == '__main__':
    run({1: scene1, 2: scene2, 3: scene3, 4: scene4, 5: scene5, 6: scene6, 7: scene7})
