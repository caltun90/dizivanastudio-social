"""13. Kat, 2. Bolum: Sessizlik. Yalnizca sahneler; ortak parcalar ../ortak.py icinde.
Yapi: NEREDEYSE DIYALOGSUZ. Kanca (yakin plan: paket tikirdar) -> asansorde kisa konusma ve kural -> arsiv: citirti,
raflarin arasindaki gozler, avuca yazi -> parmakla sayim ve tikirdayan paket -> kagit kulesi, Sam'in bagirisi ->
asansor ve panelin yakin plani ('L' dugmesinin yeri bos) -> bitis karti.
Yeni mekan: arsiv (yandan). Yeni gorsel fikirler: yaziyla iletisim (avuc), parmakla sayma balonu, yakin plan, ses yazilari."""
import os, sys, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import *
from senaryo import ABONE_END, TIK, CRACK, EYES_OPEN, CRASH

LTRB = skia.Rect.MakeLTRB
RED = (255, 86, 74)
PAPER = (214, 202, 172)
BIND = [(126, 58, 66), (58, 96, 104), (168, 132, 70), (92, 84, 110), (140, 100, 58), (70, 104, 84), (112, 52, 60), (60, 74, 96)]

# ---------- arsiv: dunya olculeri ----------
SH_TOP = 560                                               # raflarin ust kenari
UNIT, UW, U0 = 560, 400, 430                               # raf araligi, raf genisligi, ilk rafin dunya x'i
DOOR = 3900                                                # kirmizi kapi (dunya x)
G0, GX1, GX2, GX3 = 500, 1190, 2310, 3170                  # grubun durdugu yerler: cikis, citirti, paket, kule
TXB = 2970                                                 # kagit kulesinin tabani
OFF = {'U': (-190, NEAR, 0.54), 'S': (-45, FAR, 0.62), 'Z': (115, NEAR, 0.62), 'L': (270, FAR, 0.70)}
A_ORDER = ('S', 'L', 'U', 'Z')                             # once uzak serit, sonra yakin
PHASE = {'U': 0.3, 'S': 0.55, 'Z': 0.15, 'L': 0.7}
def gap_x(i): return U0 + UW + (UNIT - UW) / 2 + UNIT * i  # raflar arasindaki karanlik araligin ortasi

# ---------- bu bolumun pozlari ----------
FOUR = dict(aR=(84, 30, 120, -90))
WHISPER = dict(aR=(100, 20, 62, -62), lean=10, belly=-8)
REACH_U = dict(aR=(110, 110, 170, 170), lean=12, belly=-8)
WRITE_A = dict(aL=(-76, 96, -18, 40), aR=(74, 84, 6, 22), lean=6, belly=-6)
WRITE_B = dict(aL=(-76, 96, -18, 40), aR=(74, 84, 18, 36), lean=6, belly=-6)
SHOW_L = dict(aL=(-112, 24, -150, -92), lean=-6)
SHOW_R = dict(aR=(112, 24, 150, -92), lean=6)
WAVE_A = dict(aL=(-120, 30, -170, -120), aR=(120, 30, 150, -130), lean=-10, belly=6)
WAVE_B = dict(aL=(-130, 20, -110, -140), aR=(130, 20, 190, -110), lean=-16, belly=10)
SHOUT = dict(aL=(-96, 24, -66, -70), aR=(96, 24, 66, -70), lean=-22, belly=14)
HUG = dict(crouch=38, lean=12, belly=-16, kL=(-100, -114), kR=(100, -114), aL=(-74, 110, -26, 190), aR=(74, 110, 26, 190))
HOLDB = dict(aL=(-80, 90, -34, 150), aR=(80, 90, 34, 150))      # Luna bereyi gogsunde tutar
PICK = dict(crouch=110, lean=-14, belly=8, kL=(-112, -96), kR=(112, -96), aL=(-90, 130, -70, 250), aR=(70, 140, 10, 250))

_C = {}
def cached(key, w, h, draw):
    if key not in _C:
        surf = skia.Surface(int(w * K) + 2, int(h * K) + 2); c = surf.getCanvas(); c.clear(0); c.scale(K, K); draw(c); _C[key] = surf.makeImageSnapshot()
    return _C[key]


# ---------- dekor: arsiv (yandan; solda asansor, sagda kirmizi kapi) ----------
def _unit(c, seed):
    R = random.Random(seed); rows = 5; hh = CFLOOR - SH_TOP; rh = hh / rows
    c.drawRect(LTRB(6, 10, 6 + UW, 10 + hh), fill((40, 36, 38)))
    for r in range(rows):
        y1 = 10 + (r + 1) * rh - 10; xx = 18
        while xx < UW - 30:
            kd = R.random()
            if kd < 0.5:                                   # klasor
                w = R.choice((24, 28, 34)); h = rh * R.uniform(0.60, 0.84); cc = R.choice(BIND)
                c.drawRect(LTRB(xx, y1 - h, xx + w, y1), fill(cc))
                c.drawRect(LTRB(xx + 5, y1 - h + 12, xx + w - 5, y1 - h + 32), fill(shade(PAPER, 0.86)))
                c.drawLine(xx + w, y1 - h, xx + w, y1, stroke(shade(cc, 0.6), 2, cap=False)); xx += w + 2
            elif kd < 0.8:                                 # kagit yigini
                w = R.uniform(56, 84); n = R.randint(3, 8)
                if xx + w > UW - 4: break
                for j in range(n):
                    o = R.uniform(-4, 4); c.drawRect(LTRB(xx + o, y1 - (j + 1) * 9, xx + w + o, y1 - j * 9 - 1.5), fill(shade(PAPER, R.uniform(0.74, 0.98))))
                xx += w + 10
            else:                                          # koli
                w = R.uniform(66, 96); h = rh * R.uniform(0.42, 0.66)
                if xx + w > UW - 4: break
                c.drawRect(LTRB(xx, y1 - h, xx + w, y1), fill((122, 92, 58)))
                c.drawRect(LTRB(xx + 7, y1 - h + 7, xx + w - 7, y1 - 7), dashed((176, 140, 92), 2, 200, (8, 6))); xx += w + 8
        c.drawRect(LTRB(0, y1, UW + 12, y1 + 10), fill((86, 68, 54)))
        c.drawLine(4, y1 + 5, UW + 8, y1 + 5, dashed((132, 108, 86), 2, 170, (10, 8)))
    for ux in (0, UW + 2): c.drawRect(LTRB(ux, 0, ux + 10, 10 + hh), fill((70, 56, 46)))
    c.drawRect(LTRB(0, 0, UW + 12, 12), fill((86, 68, 54)))


def _papers():
    R = random.Random(77); out = []; x = 390
    while x < DOOR - 130:
        band = R.choice(((1206, 1218), (1284, 1296), (1392, 1470), (1392, 1470)))
        out.append((x + R.uniform(-20, 20), R.uniform(*band), R.uniform(40, 62) if band[0] < 1300 else R.uniform(56, 84), R.uniform(-0.5, 0.5), R.uniform(0.70, 0.98)))
        x += R.uniform(44, 92)
    return out
PAPERS = _papers()


def paper(cv, x, y, w, skew, v=0.9, crumple=0.0):
    """yerde duran kagit (perspektifle basik). crumple>0: burusmus"""
    h = w * 0.34; sx = skew * h; c = shade(PAPER, v)
    if crumple > 0:
        pts = [(-w * 0.42, -h * 0.2), (-w * 0.2, -h * 1.0), (w * 0.08, -h * 0.55), (w * 0.3, -h * 1.1), (w * 0.46, -h * 0.25), (w * 0.3, h * 0.25), (0, h * 0.1), (-w * 0.3, h * 0.3)]
        poly(cv, [(x + a, y + b) for a, b in pts], c)
        for a, b in ((0, 2), (2, 6), (3, 5)): cv.drawLine(x + pts[a][0], y + pts[a][1], x + pts[b][0], y + pts[b][1], stroke(shade(c, 0.66), 2))
        return
    poly(cv, [(x - w / 2 + sx, y - h / 2), (x + w / 2 + sx, y - h / 2), (x + w / 2 - sx, y + h / 2), (x - w / 2 - sx, y + h / 2)], c)
    for f in (-0.18, 0.12): cv.drawLine(x - w * 0.34 + sx * f, y + h * f, x + w * 0.34 + sx * f, y + h * f, stroke(shade(c, 0.74), 1.5, cap=False))


def archive(cv, cam, lamp=1.0, k=0, open_u=0.0, floor='14'):
    """cam: kadrajin sol kenarindaki dunya x'i. lamp: sayi ya da lamba_no -> parlaklik fonksiyonu"""
    lv = lamp if callable(lamp) else (lambda i: lamp)
    cv.clear(col((20, 26, 34)))
    with stage(cv):
        x0, x1 = -520, 1620
        cv.drawRect(LTRB(x0, 440, x1, CFLOOR), fill((36, 50, 58)))
        cv.drawLine(x0, 930, x1, 930, dashed((66, 86, 94), 4, 150, (18, 14)))
        cv.drawLine(x0, 410, x1, 410, stroke((44, 54, 66), 20, cap=False)); cv.drawLine(x0, 404, x1, 404, stroke((58, 70, 84), 5, cap=False))
        for j in range(int((cam + x0) // 310) - 1, int((cam + x1) // 310) + 2):
            cv.drawRRect(skia.RRect.MakeRectXY(LTRB(310 * j - cam - 9, 388, 310 * j - cam + 9, 432), 5, 5), fill((30, 38, 48)))
        cv.drawRect(LTRB(x0, CFLOOR, x1, 5000), fill((70, 40, 52)))
        cv.drawRect(LTRB(x0, CFLOOR + 50, x1, CFLOOR + 250), fill((92, 50, 64)))
        for yy in (CFLOOR + 62, CFLOOR + 238): cv.drawLine(x0, yy, x1, yy, dashed((150, 94, 106), 3.5, 180, (16, 12)))
        for i in range(0, 6):                               # raflar ve aralarindaki karanlik araliklar
            sx = U0 + UNIT * i - cam
            if sx > x1 + 20 or sx + UNIT < x0 - 20: continue
            blit(cv, cached(('unit', i), UW + 12, CFLOOR - SH_TOP + 10, lambda c, i=i: _unit(c, 40 + i)), sx - 6, SH_TOP - 10)
            if i < 5:
                g0, g1 = sx + UW + 6, sx + UNIT - 6
                cv.drawRect(LTRB(g0, SH_TOP - 10, g1, CFLOOR), fill((8, 10, 18)))
                poly(cv, [(g0, CFLOOR), (g1, CFLOOR), (g1 - 46, CFLOOR - 96), (g0 + 46, CFLOOR - 96)], (30, 20, 28))
        for i in range(0, 6):                               # tavan lambalari
            lx = U0 + UW / 2 + UNIT * i - cam
            if lx < x0 - 300 or lx > x1 + 300: continue
            on_ = clamp(lv(i))
            poly(cv, [(lx - 50, 512), (lx + 50, 512), (lx + 280, CFLOOR + 150), (lx - 280, CFLOOR + 150)], (250, 236, 190), 24 * on_)
            cv.drawLine(lx, 380, lx, 480, stroke((24, 30, 38), 5, cap=False))
            poly(cv, [(lx - 26, 478), (lx + 26, 478), (lx + 58, 512), (lx - 58, 512)], (28, 34, 44))
            cv.drawOval(LTRB(lx - 44, 506, lx + 44, 522), fill((250, 236, 190), 255 * (0.16 + 0.84 * on_)))
        a0, a1 = LIFT_X[0] - cam, LIFT_X[1] - cam           # asansor (solda, isikli)
        if a1 > x0:
            cv.drawRect(LTRB(a0 - 22, 668, a1 + 22, CFLOOR), fill((30, 34, 48)))
            cv.drawRect(LTRB(a0, 690, a1, CFLOOR), fill((250, 228, 156)))
            cv.drawRect(LTRB(a0 + 14, 706, a1 - 14, CFLOOR), dashed((214, 180, 96), 3, 220))
            cv.drawRRect(skia.RRect.MakeRectXY(LTRB((a0 + a1) / 2 - 62, 598, (a0 + a1) / 2 + 62, 656), 10, 10), fill((28, 32, 46)))
            text(cv, floor, (a0 + a1) / 2, 644, 44, RED)
            poly(cv, [(a0, CFLOOR), (a1, CFLOOR), (a1 + 200, CFLOOR + 260), (a0 - 60, CFLOOR + 260)], (250, 228, 156), 34)
        if LIFT_X[0] - cam > x0: cv.drawRect(LTRB(x0, 380, LIFT_X[0] - 40 - cam, 5000), fill((34, 44, 52)))
        d0 = DOOR - cam                                     # arsivin sonu: duvar ve kirmizi kapi
        if d0 < x1 + 60:
            cv.drawRect(LTRB(d0 + 250, -400, x1 + 400, 5000), fill((34, 44, 52)))
            cv.drawLine(d0 + 250, 380, d0 + 250, 5000, stroke((52, 66, 76), 6, cap=False))
            cv.drawRect(LTRB(d0 - 22, 748, d0 + 212, CFLOOR), fill((70, 24, 30)))
            if open_u > 0:                                  # kapinin ardi: yine asansor
                cv.drawRect(LTRB(d0, 770, d0 + 190, CFLOOR), fill((250, 228, 156)))
                cv.drawRect(LTRB(d0 + 14, 786, d0 + 176, CFLOOR), dashed((214, 180, 96), 3, 220))
                cv.drawLine(d0 + 6, 1040, d0 + 184, 1040, stroke((200, 170, 100), 10, cap=False))
                cv.drawRRect(skia.RRect.MakeRectXY(LTRB(d0 + 95 - 62, 676, d0 + 95 + 62, 736), 10, 10), fill((28, 32, 46)))
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
        for (px, py, pw, sk, v) in PAPERS:                  # yerdeki kagitlar
            if x0 - 60 < px - cam < x1 + 60: paper(cv, px - cam, py, pw, sk, v)
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, GY + 60), skia.Point(0, GY + 430)], [skia.Color(10, 8, 26, 0), skia.Color(10, 8, 26, 225)]))
        cv.drawRect(LTRB(x0, GY, x1, 5000), g)
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kSoftLight); p.setAlphaf(0.4); cv.drawImage(noise_img(), 0, 0, LIN, p)


def gap_eyes(cv, x, y, op, look=0.0, s=1.25, a=1.0):
    """raflarin arasindaki karanlikta acilan gozler (karalti). op: 0 kapali .. 1 acik"""
    if op <= 0.03: return
    gl = fill((240, 232, 200), 46 * a * op); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    cv.drawOval(LTRB(x - 66 * s, y - 26 * s, x + 66 * s, y + 26 * s), gl)
    for sd in (-1, 1):
        cv.save(); cv.translate(x + sd * 30 * s + look * 7 * s, y); cv.rotate(-12 * sd)
        cv.drawOval(LTRB(-19 * s, -8 * s * op, 19 * s, 8 * s * op), fill((240, 232, 200), 240 * a)); cv.restore()


# ---------- kagit kulesi ----------
TW_N, TW_H = 24, 26
def _slabs():
    R = random.Random(9); out = []
    for j in range(TW_N):
        kind = 'f' if R.random() < 0.28 else 'p'
        out.append((R.uniform(128, 172), shade(PAPER, R.uniform(0.76, 1.0)) if kind == 'p' else R.choice(BIND), kind, R.uniform(-9, 9)))
    return out
SLABS = _slabs()


def paper_tower(cv, bx, D, fall=0.0):
    """bx: tabanin sahne x'i. D: tepenin sola kaymasi (egilme). fall 0..1: devrilme (sola, yere yayilir)"""
    for j, (w, c, kind, jx) in enumerate(SLABS):
        u = j / (TW_N - 1)
        xl, yl, rl = bx - D * u ** 1.7 + jx, CFLOOR + 6 - j * TW_H, -D / 190 * 15 * u
        tj = clamp(fall * 1.7 - 0.7 * (1 - u)) ** 2 if fall > 0 else 0.0
        xf, yf, rf = bx - 110 - 27 * j + jx * 2, CFLOOR + 16 + (j * 53) % 84, ((j * 37) % 50) - 25
        x, y, r = lerp(xl, xf, tj), lerp(yl, yf, tj) - math.sin(math.pi * tj) * 46 * u, lerp(rl, rf, tj) - 70 * math.sin(math.pi * tj) * u
        cv.save(); cv.translate(x, y); cv.rotate(r)
        rc = LTRB(-w / 2, -TW_H + 3, w / 2, 0); cv.drawRect(rc, fill(c))
        if kind == 'p':
            for yy in (-TW_H * 0.64, -TW_H * 0.34): cv.drawLine(-w / 2 + 3, yy, w / 2 - 3, yy, stroke(shade(c, 0.72), 1.5, cap=False))
        else: cv.drawRect(rc.makeInset(5, 4), dashed(shade(c, 1.45), 2, 190, (8, 6)))
        cv.restore()


def flutter(cv, bx, d):
    """devrilmeden sonra havada ucusan kagitlar. d: carpmadan sonra gecen sure"""
    if d < 0 or d > 2.0: return
    R = random.Random(21)
    for i in range(16):
        x0 = bx - R.uniform(60, 640); vy0 = R.uniform(360, 700); vx = R.uniform(-110, 90); ph = R.uniform(0, 6)
        y = CFLOOR + 30 - vy0 * d + 520 * d * d; x = x0 + vx * d + 26 * math.sin(d * 7 + ph)
        if y > CFLOOR + 110: continue
        cv.save(); cv.translate(x, y); cv.rotate(math.degrees(math.sin(d * 5 + ph)) * 0.9)
        cv.drawRect(LTRB(-26, -17, 26, 17), fill(shade(PAPER, R.uniform(0.8, 1.0)), 255 * (1 - seg(d, 1.5, 2.0)))); cv.restore()


# ---------- avuca yazi (ekran koordinati) ----------
def palm_note(cv, lines, a, c=CORAL, name='ZOE'):
    if a <= 0: return
    u = (1.0 if FMT == 'v' else 0.88) * lerp(0.7, 1.0, smooth(a)); A = 255 * clamp(a)
    cx, cy = (540, 590) if FMT == 'v' else (1700, 470)
    R_ = 190 * u; dk = shade(c, 0.56)
    cv.save(); cv.translate(cx, cy); cv.rotate(-5)
    sh = fill((4, 6, 20), 120 * clamp(a)); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14)); cv.drawCircle(10, 16, R_, sh)
    cv.drawLine(-R_ * 0.72, R_ * 0.22, -R_ * 1.2, -R_ * 0.3, stroke(dk, 84 * u, A)); cv.drawLine(-R_ * 0.72, R_ * 0.22, -R_ * 1.2, -R_ * 0.3, stroke(shade(c, 0.9), 72 * u, A))
    for i in range(4):
        x = (i - 1.5) * 86 * u; top = -R_ - (112 + (0, 24, 14, -18)[i]) * u
        cv.drawRRect(skia.RRect.MakeRectXY(LTRB(x - 41 * u, top - 4 * u, x + 41 * u, -R_ * 0.3), 41 * u, 41 * u), fill(dk, A))
        cv.drawRRect(skia.RRect.MakeRectXY(LTRB(x - 36 * u, top, x + 36 * u, -R_ * 0.3), 36 * u, 36 * u), fill(shade(c, 0.9), A))
        cv.drawLine(x, top + 30 * u, x, -R_ * 0.72, dashed(shade(c, 1.3), 3 * u, 170 * clamp(a), (9 * u, 8 * u)))
    cv.drawCircle(0, 0, R_ + 5 * u, fill(dk, A)); cv.drawCircle(0, 0, R_, fill(c, A))
    cv.drawCircle(0, 0, R_ - 14 * u, dashed(shade(c, 1.35), 3.5 * u, 190 * clamp(a), (13 * u, 10 * u)))
    y = -(len(lines) - 1) * 37 * u + 22 * u
    for ln in lines:
        text(cv, ln, 0, y, 62 * u, THREAD, a=A); y += 76 * u
    cv.restore()
    f = skia.Font(TFB, 30 * u); pw = f.measureText(name); px, py = cx - R_ * 0.78, cy + R_ * 0.98
    cv.drawRRect(skia.RRect.MakeRectXY(LTRB(px - pw / 2 - 22 * u, py - 38 * u, px + pw / 2 + 22 * u, py + 16 * u), 27 * u, 27 * u), fill(c, A))
    cv.drawString(name, px - pw / 2, py, f, fill(INKBLUE, A))


def people(cv, ts, P, st, order=A_ORDER):
    """P: {kim: (x, gy, s)} sahne konumu; st: {kim: (ifade, poz, bakis[, ek])}"""
    out = {}
    for w in order:
        if w not in st or w not in P: continue
        v = st[w]; kw = dict(v[3]) if len(v) > 3 else {}
        if w == 'L': kw.setdefault('tie', True)
        out[w] = actor(cv, ts, w, v[0], v[1], v[2], place=P[w], **kw)
    return out


def pkg_xy(f):
    return (f['handL'][0] + f['handR'][0]) / 2, f['handL'][1]


def tik_text(cv, f, i, small=False):
    x, y = pkg_xy(f); s = f['s']; sd = -1 if i % 2 else 1
    sfx_text(cv, x + (150 + 40 * (i % 2)) * s, y + (-96, 6, 96)[i % 3] * s, 'TIK', (30 if small else 46) * s / 0.7, YEL if not small else CREAM, rot=sd * 10, a=0.7 if small else 1.0)


# ---------- kabin kapisinin ardi: arsiv (perspektif) ----------
_VIEW = dict(glow=0.0, red=True)
def arch_view(cv, near, far, lamp):
    nx0, ny0, nx1, ny1 = near; fx0, fy0, fx1, fy1 = far
    X = lambda sd, f: lerp(nx0 if sd < 0 else nx1, fx0 if sd < 0 else fx1, f)
    Y = lambda f, v: lerp(lerp(ny0, fy0, f), lerp(ny1, fy1, f), v)
    poly(cv, [(nx0, ny0), (nx1, ny0), (fx1, fy0), (fx0, fy0)], (20, 26, 34))
    poly(cv, [(nx0, ny1), (nx1, ny1), (fx1, fy1), (fx0, fy1)], (70, 40, 52))
    poly(cv, [(lerp(nx0, nx1, .3), ny1), (lerp(nx0, nx1, .7), ny1), (lerp(fx0, fx1, .74), fy1), (lerp(fx0, fx1, .26), fy1)], (92, 50, 64))
    fs = [0.0, 0.3, 0.52, 0.68, 0.8, 0.88, 0.94, 1.0]; R = random.Random(5)
    for sd in (-1, 1):                                      # iki yanda raflar
        poly(cv, [(X(sd, 0), ny0), (X(sd, 1), fy0), (X(sd, 1), fy1), (X(sd, 0), ny1)], (40, 36, 38))
        for a, b in zip(fs[:-1], fs[1:]):
            for r in range(5):
                if R.random() < 0.18: continue
                vt, vb = (r + R.uniform(0.24, 0.5)) / 5, (r + 0.94) / 5; c = R.choice(BIND + [shade(PAPER, 0.8)] * 4)
                a2, b2 = lerp(a, b, 0.08), lerp(a, b, R.uniform(0.6, 0.94))
                poly(cv, [(X(sd, a2), Y(a2, vt)), (X(sd, b2), Y(b2, vt)), (X(sd, b2), Y(b2, vb)), (X(sd, a2), Y(a2, vb))], shade(c, 0.9 - 0.4 * a))
        for r in range(1, 6): cv.drawLine(X(sd, 0), Y(0, r / 5), X(sd, 1), Y(1, r / 5), stroke((96, 76, 60), 4, 255, cap=False))
        for f in fs[1:-1]: cv.drawLine(X(sd, f), Y(f, 0), X(sd, f), Y(f, 1), stroke((70, 56, 46), max(1.5, 7 * (1 - f)), cap=False))
    for i, f in enumerate((0.2, 0.45, 0.63, 0.76)):         # yerdeki kagitlar
        for a in (0.16, 0.5, 0.84)[i % 2::2] + (0.36,):
            x = lerp(X(-1, f), X(1, f), a + 0.06 * math.sin(i * 3 + a * 9)); y = Y(f, 1) - 3; w = 70 * (1 - f) + 8
            poly(cv, [(x - w / 2, y - w * 0.12), (x + w / 2, y - w * 0.16), (x + w * 0.56, y + w * 0.14), (x - w * 0.44, y + w * 0.16)], shade(PAPER, 0.9 - 0.3 * f))
    for i, f in enumerate((0.34, 0.6, 0.78)):               # tavan lambalari
        xm, y0 = (X(-1, f) + X(1, f)) / 2, Y(f, 0); lw = (X(1, f) - X(-1, f)) * 0.09; on_ = lamp if i != 1 else lamp * 0.45
        cv.drawOval(LTRB(xm - lw * 2.2, y0 - lw * 0.5, xm + lw * 2.2, y0 + lw * 1.3), fill((250, 236, 190), 40 * on_))
        cv.drawOval(LTRB(xm - lw, y0, xm + lw, y0 + lw * 0.4), fill((250, 236, 190), 225 * on_))
    cxm, cym = (fx0 + fx1) / 2, (fy0 + fy1) / 2
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeRadial(skia.Point(cxm, cym), (ny1 - ny0) * 0.52, [skia.Color(6, 8, 20, 225), skia.Color(6, 8, 20, 0)]))
    cv.drawRect(LTRB(nx0, ny0, nx1, ny1), g)
    rc = LTRB(fx0, fy0, fx1, fy1)
    if _VIEW['red']:
        gw = _VIEW['glow']
        if gw > 0:
            gl = fill((255, 90, 80), 150 * gw); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)); cv.drawRect(rc.makeOutset(30, 30), gl)
        cv.drawRect(rc, fill(shade((204, 54, 58), 0.8 + 0.4 * gw))); cv.drawRect(rc.makeInset((fx1 - fx0) * 0.12, (fy1 - fy0) * 0.08), dashed((255, 170, 160), 2, 220, (6, 5)))
        cv.drawCircle(fx1 - (fx1 - fx0) * 0.24, cym + 4, (fx1 - fx0) * 0.06, fill(YEL))
    else:
        cv.drawRect(rc, fill((10, 12, 22)))


# ============ SAHNE 1: kanca (ileriden bir an) ============
def scene1(cv, t):
    ts, k = step(t), kk(t)
    tk = B('tik0'); T0 = tk[0] + TIK[0]
    if ts < S('n2'):                                         # parmak ucunda yururler; paket tikirdar, herkes donar
        gx = GX2 - 115.0 * max(0.0, T0 - ts); cam = gx - 540
        hit = [i for i, o in enumerate(TIK) if 0 <= ts - (tk[0] + o) < 0.14]
        seen = [i for i, o in enumerate(TIK) if 0 <= ts - (tk[0] + o) < 0.34]
        frozen = ts >= T0; trn = ts >= T0 + 0.45
        archive(cv, cam, 1.0, k)
        P = {w: (gx + o - cam, gy, s) for w, (o, gy, s) in OFF.items()}; st = {}
        for w, (o, gy, s) in OFF.items():
            if not frozen: st[w] = ('sakin' if w == 'U' else 'endise', walk(gx - GX2 + 4000, s, 1, scared=True, hold=w == 'L', off=PHASE[w]), 2.0)
            elif w == 'L': st[w] = ('panik' if trn else 'saskin', COWER_HOLD, 0, dict(pkg_off=jit(k, 8) if hit else (0, 0)))
            else: st[w] = ('saskin', COWER, 2.0 if trn else 0.0)
        with stage(cv):
            fs = people(cv, ts, P, st)
        dim(cv, 0.3)
        with stage(cv):
            for i in seen: tik_text(cv, fs['L'], i)
    else:                                                    # yakin plan: Leo ve paket; arkada gozler acilir
        cam = gap_x(2) - 369
        fl = (k * 7) % 13 < 2
        hit = [i for i in range(4) if 0 <= ts - frac('n2', 0.15 + 0.2 * i) < 0.14]
        seen = [i for i in range(4) if 0 <= ts - frac('n2', 0.15 + 0.2 * i) < 0.36]
        with zoom(cv, 1.7, (540, 1000)):
            archive(cv, cam, 0.3 if fl else 0.9, k)
        dim(cv, 0.44)
        eo = smooth(seg(ts, frac('n2', 0.3), frac('n2', 0.55)))
        with zoom(cv, 1.7, (540, 1000)):
            with stage(cv): gap_eyes(cv, gap_x(2) - cam, 769, eo, look=1.6)
        with stage(cv):
            f = actor(cv, ts, 'L', 'panik' if eo < 0.5 else 'saskin', dict(lean=-4, belly=10, crouch=8), alt(k, -1.6, 1.6, 5) if eo < 0.5 else 0,
                      place=(540, 1560, 1.3), tie=True, pkg_off=jit(k, 12) if hit else (0, 0))
            for i in seen: tik_text(cv, f, i)
    tb = B('title'); a = seg(t, tb[0], tb[0] + 0.35)
    if a > 0:
        dim(cv, 0.45 * a)
        card(cv, [(TITLE, 130, (255, 110, 96)), (f'{EP.title()}: {EP_NAME}', 48, CREAM)], a, lerp(0.9, 1.0, smooth(seg(t, tb[0], tb[0] + 0.5))))


# ============ SAHNE 2: asansor (kisa konusma; kural) ============
def scene2(cv, t):
    ts, k = step(t), kk(t)
    who = ('Z', 'S', 'L', 'U')
    lg, fg, dg, hs = B('lights'), B('fingers'), B('ding'), B('hush')
    dark = ts < lg[0] + 0.15
    flick = lg[0] + 0.15 <= ts < lg[0] + 0.8
    u = smooth(seg(ts, dg[0] + 0.6, dg[0] + 1.9))
    sh = jit(k, 5 if S('l1') + 0.2 <= ts < dg[0] + 0.15 else 0)
    vt = TL.talk('V', ts); hushed = ts >= hs[0] + 0.35
    _VIEW.update(glow=(0.55 + 0.45 * alt(k, 0, 1, 2)) if on(ts, 'l2', 0.0, 0.5) else 0.0, red=True)
    cabin(cv, sh, u, lamp=0.8, view=arch_view)
    LK = dict(lean=-6, belly=-14)
    st = {'Z': ('endise', {}, alt(k, 1, 0, 6)), 'S': ('sakin', {}, 0), 'L': ('endise', {}, 0), 'U': ('sakin', {}, 0)}
    nf = 0
    if on(ts, 'z1', 0.05, 0.1):
        st = {'Z': ('kararli', HIP, 1), 'S': ('sakin', {}, -1), 'L': ('endise', {}, -1), 'U': ('sakin', {}, -1)}
    elif on(ts, 's1', 0.1, 0.05):
        h2 = ts >= frac('s1', 0.5)
        st = {'Z': ('yorgun', HIP, 1), 'S': ('sakin', POINT_R if h2 else CALM, 1 if h2 else -1), 'L': ('endise', {}, 1 if h2 else 0), 'U': ('kararli' if h2 else 'sakin', {}, -1)}
    elif fg[0] - 0.05 <= ts < S('l1') + 0.5:                 # Luna dort parmagini kaldirir: dogru saydim
        nf = clamp(int((ts - fg[0] - 0.35) / 0.22) + 1, 0, 4) if ts >= fg[0] + 0.35 else 0
        st = {'Z': ('saskin', {}, 1.5), 'S': ('endise', {}, 1), 'L': ('endise', {}, 1.5), 'U': ('kararli', FOUR, 0)}
        if on(ts, 'l1'): st['L'] = ('endise', LK, 0); nf = 4
    elif ts < dg[0] + 0.5:
        st = {'Z': ('endise', LOOKUP, 0), 'S': ('endise', LOOKUP, 0), 'L': ('endise', LK, 0), 'U': ('sakin', LOOKUP, 0)}
    elif ts < S('v1') - 0.1:                                 # kapi acilir: Zoe ve Luna donup bakar
        st = {'Z': ('sakin', {}, 0, dict(back=True)), 'S': ('saskin', LOOKUP, 0), 'L': ('saskin', {}, -1), 'U': ('sakin', {}, 0, dict(back=True))}
    elif on(ts, 'v1', 0.1, 0.2):
        ex = 'saskin' if ts >= frac('v1', 0.62) else 'endise'
        st = {'Z': (ex, LOOKUP, 0), 'S': (ex, LOOKUP, 0), 'L': (ex, LK, 0), 'U': ('sakin', LOOKUP, 0)}
    elif on(ts, 's2', 0.05, 0.2):
        st = {'Z': ('endise', {}, 1), 'S': ('merak', WHISPER, 0), 'L': ('endise', {}, 1), 'U': ('sakin', {}, -1)}
    elif on(ts, 'v2', 0.05, 0.2):
        st = {'Z': ('endise', COWER, 0), 'S': ('endise', LOOKUP, 0), 'L': ('endise', COWER_HOLD, 0), 'U': ('sakin', LOOKUP, 0)}
    elif on(ts, 'z2', 0.05, 0.2):
        st = {'Z': ('endise', {}, alt(k, -1.5, 1.5, 3)), 'S': ('endise', {}, -1), 'L': ('endise', {}, -1), 'U': ('sakin', {}, -1)}
    elif on(ts, 'l2', 0.05, 0.2):                            # Leo arkayi gosterir; Zoe ve Luna donup bakar
        st = {'Z': ('sakin', {}, 0, dict(back=True)), 'S': ('merak', {}, -1), 'L': ('kararli', THUMB, 0, dict(pkg_left=True)), 'U': ('sakin', {}, 0, dict(back=True))}
    elif on(ts, 's3', 0.05, 0.2):
        st = {'Z': ('endise', {}, 1), 'S': ('sakin', REACH_U, 1), 'L': ('endise', {}, 1), 'U': ('sakin', {}, -1.5)}
    elif not hushed:
        st = {'Z': ('endise', LOOKUP, 0), 'S': ('endise', LOOKUP, 0), 'L': ('endise', LK, 0), 'U': ('sakin', LOOKUP, 0)}
    else:                                                    # kural basladi: eller agizlara
        st = {'Z': ('saskin', HUSH, 0), 'S': ('saskin', HUSH, 0), 'L': ('endise', {}, alt(k, -1, 1, 4)), 'U': ('sakin', SHH, 0)}
    st['L'] = st['L'][:3] + (dict(st['L'][3] if len(st['L']) > 3 else {}, tie=True),)
    with stage(cv, *sh):
        fs = cast(cv, ts, st, who=who)
        if hushed:
            hush(cv, fs['Z']); hush(cv, fs['S']); shh(cv, fs['U'])
        if on(ts, 's2', 0.05, 0.2):
            mx, my = mouth_of(fs['S']); s = fs['S']['s']; hand_ball(cv, mx + 56 * s, my + 2 * s, 30 * s, TAN, 5)
        if fg[0] + 0.2 <= ts < S('l1') + 0.5:
            hx, hy = fs['U']['handR']; fingers(cv, hx + 44, hy - 100, nf, LILAC, r=72)
    if dark: dim(cv, 0.94)
    elif flick: dim(cv, 0.94 if (k * 5) % 7 < 3 else 0.3)
    else: dim(cv, lerp(0.2, 0.46, smooth(seg(ts, hs[0] + 0.1, hs[0] + 0.7))))
    display(cv, sh, '14', red=True, level=vt, k=k)
    if dark or (flick and (k * 5) % 7 < 3):
        with stage(cv): dark_eyes(cv, who, red=who[(k // 5) % 4])
    if S('n3') - 0.1 <= ts < lg[0] + 0.15:                   # hatirlatma: Kai gitti ama hala dort kisi
        marks = [(CREAM, 'on')] * 3 + [(NAVY, 'x' if ts >= frac('n3', 0.42) else 'on')]
        if ts >= frac('n3', 0.66): marks.append((RED, 'on'))
        tally(cv, marks)


# ============ SAHNE 3: arsiv: citirti, gozler, avuca yazi ============
def scene3(cv, t):
    ts, k = step(t), kk(t)
    ob, cb, wb, wr, nd = B('out'), B('crack'), B('wait'), B('write'), B('nod')
    W0, W1 = ob[0] + 0.35, cb[0] + CRACK
    gx = G0 + (GX1 - G0) * seg(ts, W0, W1); cam = gx - 540
    moving = W0 <= ts < W1
    eo_t = cb[0] + EYES_OPEN
    eo = smooth(seg(ts, eo_t, eo_t + 0.35)) * (1 - smooth(seg(ts, wb[1] - 0.65, wb[1] - 0.25)))
    fl = W1 <= ts < W1 + 0.5 and k % 2 == 0
    show = wr[0] + 1.85
    showing = show <= ts < E('n7') + 0.3; writing = wr[0] + 0.3 <= ts < show
    archive(cv, cam, 0.25 if fl else (0.7 if eo > 0.5 else 1.0), k)
    zx = GX1 + OFF['Z'][0] + 30 - cam                         # Zoe'nin bastigi kagit
    P = {w: (gx + o - cam, gy, s) for w, (o, gy, s) in OFF.items()}; st = {}
    toZ = {'U': 2.0, 'S': 2.0, 'L': -2.0}
    for w, (o, gy, s) in OFF.items():
        if ts < W0: st[w] = ('sakin' if w == 'U' else 'endise', dict(lean=6), 2.0)
        elif moving: st[w] = ('sakin' if w == 'U' else 'endise', walk(gx - G0, s, 1, scared=True, hold=w == 'L', off=PHASE[w]), 2.0)
        elif ts < wr[0] + 0.3:                               # donup kalirlar
            if w == 'Z': st[w] = ('panik' if ts < W1 + 0.9 else 'endise', COWER, 0)
            elif w == 'U': st[w] = ('sakin', dict(lean=-4), -2.0 if eo > 0.2 else 1.0)
            else: st[w] = ('saskin' if ts < wb[1] - 0.4 else 'endise', COWER_HOLD if w == 'L' else COWER, 1.0 if ts < W1 + 0.5 else 0)
        elif writing: st[w] = ('kararli', alt(k, WRITE_A, WRITE_B, 1), -0.4) if w == 'Z' else ('endise', dict(lean=4), toZ[w])
        elif showing: st[w] = ('kararli', SHOW_L, 0) if w == 'Z' else ('merak', {}, toZ[w])
        else: st[w] = ('kararli', dict(bob=alt(k, 0, 16, 2)), 0 if w == 'Z' else toZ[w])
    with stage(cv):
        paper(cv, zx, NEAR - 2, 74, 0.2, 0.96, crumple=1.0 if ts >= W1 else 0.0)
        fs = people(cv, ts, P, st)
        if writing:                                          # kalem
            hx, hy = fs['Z']['handR']; cv.drawLine(hx - 4, hy - 30, hx - 16, hy + 12, stroke(THREAD, 6))
    dim(cv, 0.3 + 0.12 * eo)
    with stage(cv):
        gap_eyes(cv, gap_x(0) - cam, 769, eo, look=alt(k, -1.6, 1.6, 6))
        if W1 <= ts < W1 + 0.75: sfx_text(cv, zx + 70, NEAR - 96, 'ÇIT!', 66 * lerp(0.7, 1.0, smooth(seg(ts, W1, W1 + 0.15))), YEL, rot=-8)
    pa = smooth(seg(ts, show, show + 0.25)) * (1 - smooth(seg(ts, E('n7') + 0.05, E('n7') + 0.3)))
    palm_note(cv, ['KÂĞIDA', 'BASMAYIN'], pa)


# ============ SAHNE 4: parmakla sayim; paket tikirdar ============
def scene4(cv, t):
    ts, k = step(t), kk(t)
    w2, ct, tk, hg, ak = B('walk2'), B('count'), B('tik'), B('hug'), B('ask')
    W0, W1 = w2[0] + 0.1, tk[0] + TIK[0]
    gx = GX1 + (GX2 - GX1) * seg(ts, W0, W1); cam = gx - 540
    moving = W0 <= ts < W1
    cstep = (ct[1] - ct[0] - 0.5) / 4
    ci = min(3, int((ts - ct[0] - 0.25) / cstep)) if ts >= ct[0] + 0.25 else -1
    counting = S('n8') + 0.4 <= ts < W1
    q = ts >= frac('n9', 0.5)
    ticks = [tk[0] + o for o in TIK] + [frac('n10', 0.1 + 0.16 * i) for i in range(3)]
    muff = [hg[0] + o for o in (0.2, 0.5, 0.8)]
    hit = [i for i, x in enumerate(ticks) if 0 <= ts - x < 0.14]; seen = [i for i, x in enumerate(ticks) if 0 <= ts - x < 0.34]
    mhit = [i for i, x in enumerate(muff) if 0 <= ts - x < 0.14]; mseen = [i for i, x in enumerate(muff) if 0 <= ts - x < 0.3]
    eo = smooth(seg(ts, hg[0] + 0.6, hg[0] + 0.95)) * (1 - smooth(seg(ts, frac('n11', 0.72), frac('n11', 0.95))))
    fl = hg[0] + 0.55 <= ts < hg[0] + 1.05 and k % 2 == 0
    show = ak[0] + 1.7
    showing = show <= ts < E('n12') - 0.15; writing = ak[0] + 0.25 <= ts < show
    hugging = hg[0] + 0.1 <= ts < ak[0] + 0.1
    archive(cv, cam, 0.25 if fl else (0.7 if eo > 0.5 else 1.0), k)
    P = {w: (gx + o - cam, gy, s) for w, (o, gy, s) in OFF.items()}; st = {}
    toZ = {'U': 2.0, 'S': 2.0, 'L': -2.0}
    for w, (o, gy, s) in OFF.items():
        if ts < W0: st[w] = ('kararli', {}, 2.0)
        elif moving:
            pose = walk(gx - GX1, s, 1, scared=True, hold=w == 'L', off=PHASE[w])
            if w == 'U' and counting: pose = dict(pose, aR=(64, 30, 150, -6))            # sayarken isaret eder
            st[w] = ('merak' if (w == 'U' and counting) else ('sakin' if w == 'U' else 'endise'), pose, 2.0)
        elif ts < hg[0] + 0.1:                               # paket tikirdar: herkes donar ve Leo'ya bakar
            trn = ts >= W1 + 0.4
            if w == 'L': st[w] = ('panik' if trn else 'saskin', COWER_HOLD, 0, dict(pkg_off=jit(k, 8) if hit else (0, 0)))
            elif w == 'U': st[w] = ('merak' if trn else 'saskin', {}, 2.0)
            else: st[w] = ('saskin' if (w == 'Z' or ts < S('n10')) else 'endise', COWER, 2.0 if trn else 0.0)
        elif hugging:
            if w == 'L': st[w] = ('endise', HUG, 0, dict(pkg_off=jit(k, (5, 3, 2)[mhit[0]]) if mhit else (0, 0)))
            elif w == 'U': st[w] = ('sakin', dict(lean=-4), -2.0 if eo > 0.2 else 2.0)
            else: st[w] = ('endise' if eo < 0.5 else 'saskin', COWER, 2.0 if eo < 0.2 else 0.0)
        elif writing: st[w] = ('merak', alt(k, WRITE_A, WRITE_B, 1), 0.4) if w == 'Z' else ('endise', {}, toZ[w] if w != 'L' else 0)
        elif showing:
            if w == 'Z': st[w] = ('merak', SHOW_R, 2.0)
            elif w == 'L': st[w] = ('endise', dict(bob=alt(k, 0, 8, 2)), alt(k, -1.5, 1.5, 2)) if ts >= S('n12') + 0.2 else ('saskin', {}, -2.0)
            else: st[w] = ('merak', {}, 2.0)
        else: st[w] = ('endise', {}, 2.0 if w != 'L' else 0)
    with stage(cv):
        fs = people(cv, ts, P, st)
        if writing:
            hx, hy = fs['Z']['handR']; cv.drawLine(hx - 4, hy - 30, hx - 16, hy + 12, stroke(THREAD, 6))
    dim(cv, 0.3 + 0.12 * eo)
    with stage(cv):
        gap_eyes(cv, gap_x(2) - cam, 769, eo, look=alt(k, -1.6, 1.6, 6))
        for i in seen: tik_text(cv, fs['L'], i)
        for i in mseen: tik_text(cv, fs['L'], i, small=True)
        if counting:                                         # Luna sayar: Sam 1, Zoe 2, Leo 3, kendisi 4 (parmaklar)
            for i, w in enumerate(('S', 'Z', 'L')):
                if ci >= i:
                    hx, hy = fs[w]['head']; badge_at(cv, hx, hy - fs[w]['HR'] - 52, '?' if q else str(i + 1), red=q)
            hx, hy = fs['U']['head']; fingers(cv, hx, hy - fs['U']['HR'] - 76, clamp(ci + 1, 0, 4), LILAC, r=66)
    if S('n9') <= ts < W1:                                   # dort kisi var; olmasi gereken uc
        marks = [(CREAM, 'on')] * 3 + [(NAVY, 'x')]
        if q: marks.append((RED, 'on'))
        tally(cv, marks)
    pa = smooth(seg(ts, show, show + 0.25)) * (1 - smooth(seg(ts, E('n12') - 0.4, E('n12') - 0.15)))
    palm_note(cv, ['İÇİNDE', 'NE VAR?'], pa)


# ============ SAHNE 5: kagit kulesi; Sam bagirir ============
def scene5(cv, t):
    ts, k = step(t), kk(t)
    ln, wv, th, cr, tkn, h2, br = B('lean'), B('wave'), B('think'), B('crash'), B('taken'), B('hush2'), B('beret')
    W0, W1 = ln[0] + 0.1, frac('n13', 0.4)
    u = seg(ts, W0, W1); gx = GX3 - 420 * (1 - u)
    cam = lerp(GX3 - 420 - 540, TXB - 170 - 190, smooth(u)) + 70 * smooth(seg(ts, B('crash')[0] + CRASH + 0.3, B('crash')[0] + CRASH + 1.3))
    moving = W0 <= ts < W1
    xU0, xU1, xU2 = GX3 - 420 + OFF['U'][0], TXB - 170, GX3 + 65
    run0 = E('s4') - 0.35; run1 = run0 + 0.85
    xU = lerp(xU0, xU1, u) if ts < run0 else lerp(xU1, xU2, seg(ts, run0, run1))
    hitT = cr[0] + CRASH
    back = 80 * smooth(seg(ts, hitT - 0.2, hitT + 0.3))
    X = {'S': gx + OFF['S'][0], 'Z': gx + OFF['Z'][0] + 25 + back, 'L': gx + OFF['L'][0] + back, 'U': xU}
    P = {w: (X[w] - cam, OFF[w][1], OFF[w][2]) for w in OFF}
    D = 26 + 8 * math.sin(ts * 2.1) + 120 * smooth(seg(ts, frac('n13', 0.45), wv[0] + 0.3)) + 30 * smooth(seg(ts, th[0] + 0.3, th[0] + 1.2)) + 24 * seg(ts, S('s4'), cr[0])
    fall = seg(ts, cr[0] + 0.15, hitT + 0.3)
    sh = jit(k, 9 if hitT - 0.1 <= ts < hitT + 0.9 else 0)
    T = ts - tkn[0]
    def lamp(i):
        if i == 4: return 1.0 if T < 0.05 else (0.3 if T < 0.2 and k % 2 else (1.0 if T < 0.2 else 0.0))
        if i == 5:
            if T < 0.6: return 1.0
            if T < 1.0: return 0.25 if k % 2 else 0.9
            if ts < h2[0] + 0.2: return 0.0
            return (0.3 if (k // 2) % 2 else 0.7) if on(ts, 'v4', 0.1, 0.3) else 0.62
        return 1.0
    eo = smooth(seg(T, 0.9, 1.25)) * (1 - smooth(seg(T, 3.0, 3.4)))
    ka = smooth(seg(T, 1.2, 1.9)) * (1 - smooth(seg(T, 2.9, 3.5)))
    sam_a = 1 - seg(T, 1.9, 3.0)
    seen = ts >= frac('n13', 0.6)                            # Sam ve otekiler kuleyi fark eder
    waving = wv[0] + 0.1 <= ts < frac('n14', 0.55)
    archive(cv, cam + sh[0], lamp, k)
    with stage(cv, 0, sh[1]):
        paper_tower(cv, TXB - cam, D, fall)
        flutter(cv, TXB - cam, ts - hitT)
        if ka > 0: shadow(cv, gap_x(4) - cam, s=0.8, alpha=ka * 0.96, reach=smooth(seg(T, 1.6, 2.2)), k=k)
        # --- Sam (uzak serit) ---
        if moving: S_ = ('endise', walk(gx - GX3 + 4000, 0.62, 1, scared=True, off=PHASE['S']), 2.0)
        elif not seen: S_ = ('endise', dict(lean=6), 2.0)
        elif ts < wv[0] + 0.1: S_ = ('saskin', dict(lean=-8), -2.0)
        elif waving: S_ = ('endise', alt(k, WAVE_A, WAVE_B, 1), -2.0)
        elif ts < th[0]: S_ = ('endise', dict(lean=-6), -2.0)
        elif ts < th[0] + 0.8: S_ = ('endise', LOOKUP, -1.2)
        elif ts < frac('n15', 0.5): S_ = ('endise', dict(lean=-6), -2.0)
        elif ts < S('s4') - 0.05: S_ = ('kararli', dict(lean=6, belly=-18), -2.0)     # nefesini toplar
        elif ts < E('s4') + 0.1: S_ = ('bagir', SHOUT, -2.0)
        elif T < 0.5: S_ = ('sakin', {}, -2.0 if ts < run1 - 0.3 else 1.6)
        else: S_ = ('sakin', SHH, 1.6)
        fS = None
        if sam_a > 0:
            fS = actor(cv, ts, 'S', S_[0], S_[1], S_[2], place=P['S'], alpha=sam_a, talk=None)
            if T >= 0.5: shh(cv, fS) if sam_a > 0.55 else None
        if 1.8 <= T < 3.2:                                   # sokulen iplik karaltiya cekilir
            al = 255 * (1 - seg(T, 2.9, 3.2)); kx = P['S'][0]; sx = gap_x(4) - cam - 30; y0 = FAR - 330 * 0.62
            pth = skia.Path(); pth.moveTo(kx, y0)
            for i in range(1, 7):
                u_ = i / 6; pth.lineTo(lerp(kx, sx, u_) + (18 if i % 2 else -18), y0 - 60 * u_ + (26 if (i + k) % 2 else -26) * (1 - u_))
            cv.drawPath(pth, stroke(TAN, 9, al))
        # --- Leo (uzak serit) ---
        if moving: L_ = ('endise', walk(gx - GX3 + 4000, 0.70, 1, scared=True, hold=True, off=PHASE['L']), 2.0)
        elif ts < frac('n13', 0.75): L_ = ('endise', dict(lean=6), 2.0)
        elif ts < S('s4'): L_ = ('saskin' if ts < wv[0] + 0.5 else 'endise', {}, -2.0)
        elif T < 0: L_ = ('saskin', COWER_HOLD, -2.0)
        elif ts < h2[0] + 0.2: L_ = ('panik', COWER_HOLD, -2.0)
        elif ts < br[0]: L_ = ('endise', {}, -1.5)
        else: L_ = ('uzgun', {}, -2.0)
        fL = actor(cv, ts, 'L', L_[0], L_[1], L_[2], place=P['L'], tie=True)
        # --- bere: Sam'den geriye kalan ---
        bx0, by0 = P['S'][0] + 10, FAR - 4
        pick = br[0] + 1.2
        if T >= 2.6 and ts < br[0] + 0.15:
            f_ = smooth(seg(T, 2.6, 3.3)); beret_at(cv, lerp(P['S'][0], bx0, f_), lerp(FAR - 0.62 * 600, by0, f_ * f_), 0.62, rot=38 * math.sin(f_ * 5))
        elif br[0] + 0.15 <= ts < pick:
            f_ = smooth(seg(ts, br[0] + 0.15, br[0] + 1.0)); beret_at(cv, lerp(bx0, P['U'][0] - 34, f_), lerp(by0, NEAR - 6, f_) - 30 * math.sin(math.pi * f_), 0.62, rot=-360 * f_)
        # --- Luna (yakin serit) ---
        if ts < W1: U_ = ('sakin', walk(xU - xU0, 0.54, 1, scared=True, off=PHASE['U']) if moving else dict(lean=6), 2.0)
        elif ts < frac('s4', 0.35): U_ = ('sakin', dict(lean=-4), -2.0)                 # arkasina, karanliga bakiyor: Sam'i gormez
        elif ts < run0: U_ = ('saskin', {}, 2.0)
        elif ts < run1: U_ = ('panik', walk(xU - xU1, 0.54, 1, run=True), 2.0)
        elif T < 0.9: U_ = ('panik', COWER, -2.0)
        elif ts < h2[0] + 0.3: U_ = ('panik', REACH_L, -2.0)
        elif ts < h2[0] + 0.75: U_ = ('bagir', REACH_L, -2.0)                           # ciglik atacak
        elif ts < br[0]: U_ = ('panik', {}, -2.0)
        elif ts < br[0] + 0.9: U_ = ('uzgun', {}, -1.5)
        elif ts < pick: U_ = ('uzgun', PICK, -1.0)
        else: U_ = ('aglama', HOLDB, 0)
        fU = actor(cv, ts, 'U', U_[0], U_[1], U_[2], place=P['U'], talk=None)
        if ts >= pick:
            hx = (fU['handL'][0] + fU['handR'][0]) / 2; beret_at(cv, hx, fU['handL'][1] + 12, 0.5)
        # --- Zoe (yakin serit, Luna'nin onunde cizilir) ---
        zx, zs = P['Z'][0], 0.62; cover = False
        if moving: Z_ = ('endise', walk(gx - GX3 + 4000, zs, 1, scared=True, off=PHASE['Z']), 2.0)
        elif ts < frac('n13', 0.7): Z_ = ('endise', dict(lean=6), 2.0)
        elif ts < wv[0] + 0.3: Z_ = ('saskin', {}, -2.0)
        elif ts < S('s4'): Z_ = ('panik', HUSH, -2.0); cover = True
        elif T < 0: Z_ = ('saskin', COWER, -2.0)
        elif ts < h2[0] + 0.6: Z_ = ('panik', COWER, -2.0)
        elif ts < br[0]:                                     # Luna'nin agzini kapatir
            mx, my = mouth_of(fU); Z_ = ('endise', reach_pose(zx, NEAR, zs, (mx + 6, my + 4), dict(lean=-12, belly=6), side=-1, bend=36), -2.0)
        elif ts < pick + 0.3: Z_ = ('uzgun', dict(lean=-6), -2.0)
        else:                                                # elini Luna'nin omzuna koyar
            Z_ = ('uzgun', reach_pose(zx, NEAR, zs, (fU['neck'][0] + 26, fU['neck'][1] + 26), dict(lean=-10, belly=4), side=-1, bend=30), -2.0)
        fZ = actor(cv, ts, 'Z', Z_[0], Z_[1], Z_[2], place=P['Z'], talk=None)
        if cover: hush(cv, fZ)
    dim(cv, 0.3 + 0.3 * smooth(seg(T, 0.2, 1.0)) * (1 - 0.6 * smooth(seg(ts, h2[0], h2[0] + 0.5))))
    with stage(cv, *sh):
        gap_eyes(cv, gap_x(4) - cam, 769, eo * (1 - ka), look=1.0)


# ============ SAHNE 6: asansore donus; panel ============
def scene6(cv, t):
    ts, k = step(t), kk(t)
    od, ins, rs, pn = B('door'), B('inside'), B('rise'), B('panel')
    if ts < ins[0]:                                          # kirmizi kapi: yine asansor
        cam = DOOR - 640; arr = od[0] + 0.9
        d = -170 * (1 - seg(ts, od[0], arr)); moving = ts < arr
        reach = smooth(seg(ts, od[0] + 0.75, od[0] + 1.05)) * (1 - smooth(seg(ts, od[0] + 1.5, od[0] + 1.9)))
        open_u = smooth(seg(ts, od[0] + 1.2, od[0] + 2.2))
        archive(cv, cam, 0.8, k, open_u)
        XS = {'L': DOOR - 105, 'Z': DOOR - 255, 'U': DOOR - 385}
        P = {w: (XS[w] + d - cam, OFF[w][1], OFF[w][2]) for w in XS}; st = {}
        for w in XS:
            if moving: st[w] = ('uzgun' if w != 'L' else 'kararli', dict(walk(d + 400, OFF[w][2], 1, hold=w != 'Z', off=PHASE[w]), **(HOLDB if w == 'U' else {})), 2.0)
            elif w == 'L': st[w] = ('kararli' if open_u < 0.6 else 'endise', mixpose(dict(HOLD, lean=10, belly=-6), dict(aL=HOLD['aL'], aR=(150, 50, 285, 115), lean=18, belly=-8), reach), 2.0, dict(pkg_left=reach > 0.25))
            else: st[w] = ('uzgun' if open_u < 0.6 else 'endise', dict(HOLDB, lean=6) if w == 'U' else dict(lean=6), 2.0)
        with stage(cv):
            fs = people(cv, ts, P, st, order=('L', 'U', 'Z'))
            hx = (fs['U']['handL'][0] + fs['U']['handR'][0]) / 2; beret_at(cv, hx, fs['U']['handL'][1] + 12, 0.5)
        dim(cv, 0.3)
        return
    who = ('Z', 'L', 'U')
    u = 1 - smooth(seg(ts, ins[0] + 0.1, ins[0] + 0.9))
    up = rs[0] + 0.7; num = '14' if ts < up else '15'
    sh = jit(k, 4 if rs[0] + 0.1 <= ts < up + 0.3 else 0)
    vt = TL.talk('V', ts)
    _VIEW.update(glow=0.0, red=False)
    cabin(cv, sh, u, lamp=0.6, view=arch_view)
    LK = dict(lean=-6, belly=-14)
    st = {'Z': ('uzgun', SLUMP, 0), 'L': ('uzgun', {}, 0), 'U': ('aglama', HOLDB, 0)}
    if S('v5') - 0.2 <= ts < rs[1]: st.update(Z=('endise', LOOKUP, 0), L=('endise', LK, 0))
    elif on(ts, 'z3', 0.1, 0.2): st.update(Z=('uzgun', {}, 1.5), L=('uzgun', {}, 1))
    elif on(ts, 'l3', 0.05, 0.1): st.update(Z=('uzgun', SLUMP, 1), L=('uzgun', {}, 1.5))
    elif ts < pn[0] + 0.15: st.update(Z=('uzgun', SLUMP, 1), L=('uzgun', {}, 1.5))
    elif ts < E('z4') + 0.2: st.update(Z=('merak', POINT_R if ts >= pn[0] + 1.2 else {}, 2.0), L=('uzgun' if ts < S('z4') else 'saskin', {}, 1.5 if ts < S('z4') else 2.0))
    elif on(ts, 'l4', 0.1, 0.2): st.update(Z=('merak', HIP, 1.0), L=('endise', {}, 2.0 if ts < frac('l4', 0.5) else 0), U=('sakin', HOLDB, -1.5))
    elif on(ts, 'z5', 0.1, 0.1): st.update(Z=('endise', {}, 1.0), L=('endise', {}, 2.0), U=('sakin', HOLDB, -1.5))
    else: st.update(Z=('endise', {}, 1.0), L=('endise', dict(lean=4, belly=-8), 0), U=('sakin', HOLDB, -2.0))   # ikisi de Leo'ya bakar
    st['L'] = st['L'][:3] + (dict(tie=True),)
    with stage(cv, *sh):
        fs = cast(cv, ts, st, who=who)
        hx = (fs['U']['handL'][0] + fs['U']['handR'][0]) / 2; beret_at(cv, hx, fs['U']['handL'][1] + 12, 0.54)
    dim(cv, lerp(0.22, 0.5, smooth(seg(ts, S('n17'), E('n17b')))))
    display(cv, sh, num, red=True, level=vt, k=k)
    pa = smooth(seg(ts, pn[0] + 0.5, pn[0] + 0.9)) * (1 - smooth(seg(ts, E('z4') + 0.05, E('z4') + 0.35)))
    if pa > 0:                                               # yakin plan: 'L' dugmesinin yeri bos
        dim(cv, 0.74 * pa)
        panel_closeup(cv, pa, smooth(seg(ts, pn[0] + 1.4, pn[0] + 1.8)), k, finger=CORAL)
    if ts >= S('n17') - 0.1:                                 # dort kisi bindi, ikisi gitti; ama uc kisi var
        marks = [(CREAM, 'on'), (CREAM, 'on'), (NAVY, 'x' if ts >= frac('n17', 0.75) else 'on'), (TAN, 'x' if ts >= frac('n17', 0.85) else 'on')]
        if ts >= frac('n17b', 0.5): marks.append((RED, 'on'))
        tally(cv, marks)


# ============ SAHNE 7: bitis karti ============
def scene7(cv, t):
    ts, k = step(t), kk(t)
    a0, _ = TL.span(7); who = ('Z', 'L', 'U')
    cabin(cv, (0, 0)); dim(cv, 0.94)
    display(cv, (0, 0), '15', red=True)
    with stage(cv):
        dark_eyes(cv, who, red=who[(k // 7) % 3])
        gl = fill(RED, 120 if (k // 6) % 2 else 60); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
        cv.drawCircle(956, 1022, 20, gl); cv.drawCircle(956, 1022, 13, dashed(RED, 3, 230, (5, 4)))             # bos 'L' yuvasi
    a = seg(t, a0 + 0.3, a0 + 0.8)
    card(cv, [('Sam bilerek mi bağırdı?', 62 if FMT == 'v' else 70, CREAM), ('Yorumlara yaz', 40, (176, 190, 232)), ('3. Bölüm: Ayna', 46, (255, 110, 96))], a, cy=450 if FMT == 'v' else 168)
    abone(cv, t, a0 + ABONE_END, pos=(W / 2, 1235) if FMT == 'v' else (W / 2, 770))


if __name__ == '__main__':
    run({1: scene1, 2: scene2, 3: scene3, 4: scene4, 5: scene5, 6: scene6, 7: scene7})
