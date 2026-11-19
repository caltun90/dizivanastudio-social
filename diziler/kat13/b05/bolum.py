"""13. Kat, 5. Bolum: Paket (dizi finali). Yalnizca sahneler; ortak parcalar ../ortak.py icinde.
Yapi: TEK MEKAN, GERCEK ZAMANLI. Kanca (sayacin sonundan bir an) + hatirlatma -> kabin 16'dan 17'ye -> kural: "biri kalir",
ekranda 01:30'dan geri sayan sayac baslar -> 90 saniye kesintisiz akar, yalnizca aci degisir: 17. kattan kabine bakis,
kutu (ustten), yaka karti, kabin (17. katin isiklari yanar), raflar dolusu ayni paket, karar, panel (L dugmesi takilir),
veda (Leo disari cikar, Luna'yi iceri iter, kapi 00:00'da kapanir) -> Luna tek basina -> asansor boslugu kesiti (her katta
kalanlardan biri geri doner) -> lobi: bes kisi iner -> 13. kat koridoru: hardal sapkali biri -> kapanis karti.
Yeni mekanlar: 17. kat (gorevli odasi), asansor boslugu kesiti. Yeni gorsel fikirler: gercek zamanli sayac (hud),
ustten kutu plani, yaka karti, L dugmesinin yuvasina oturmasi."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import *
from senaryo import (ABONE_END, COUNT, DOOR_OPEN, RIP, FLAPS, FLIP, LIGHTS, CLICK, PUSH, CLOSE_START, MOVE,
                     FALL_N, FALL_EASE, fall_u, RETURNS, LOBBY_DING, TALLY)

# kabinde iki kisi: Leo solda, Luna sagda
CAST['L'] = dict(CAST['L'], x=330); CAST['U'] = dict(CAST['U'], x=770)
CAB = {w: (CAST[w]['x'], CAST[w]['gy'], CAST[w]['s']) for w in ('L', 'U')}
LTRB = skia.Rect.MakeLTRB
RRXY = skia.RRect.MakeRectXY
RED, GRN, AMB = (255, 86, 74), (110, 224, 146), (255, 182, 70)
BOXC = (214, 170, 110)
MOMC = CAST['M']['c']
T0, T1 = E('v2'), B('close')[1]                            # sayac: 01:30 -> 00:00 (tam 90 saniye)
HOOK_END = S('n2') - 0.2
R_HOOK = COUNT - (S('u7') - T0)                            # kancadaki an sayacin kacinci saniyesi
ROOMW0, ROOMW1 = (14, 18, 30), (60, 48, 74)                # 17. kat: karanlik / isiklar yaninca

# ---------- bu bolumun pozlari ----------
HOLDB = dict(aL=(-80, 90, -34, 150), aR=(80, 90, 34, 150))      # Luna bereyi gogsunde tutar
BERUP = dict(aL=(-84, 30, -36, 40), aR=(84, 30, 36, 40))        # bereyi kaldirir
FREE = dict(aL=(-100, 170, -120, 300), aR=(100, 170, 120, 300))
CARDP = dict(aL=(-100, 160, -116, 290), aR=(84, 96, 40, 168))   # Leo: kart sag elde, gogus hizasinda
POINT_BOX = dict(aL=(-100, 160, -116, 290), aR=(120, 150, 170, 262))   # Leo yerdeki kutuyu gosterir
POINT_PK = dict(aL=(-110, 130, -196, 176), aR=HOLDB['aR'])      # Luna paketi gosterir
TUG = dict(aL=(-126, 96, -214, 60), aR=HOLDB['aR'], lean=-14, belly=8)   # Luna Leo'ya uzanir
STOP = dict(aL=HOLD['aL'], aR=(130, 60, 250, 110), lean=16, belly=-8)    # Leo kolunu Luna'nin onune uzatir
WAVE_A = dict(aR=(120, 30, 170, -100)); WAVE_B = dict(aR=(130, 40, 204, -72))
DOORP = dict(aL=(-90, 50, -70, -50), aR=(90, 50, 70, -50))      # eller kapida (arkadan)
PUSHP = dict(aL=(-70, 120, -130, 200), aR=(70, 120, 130, 200), lean=10, belly=-8)
HUG = dict(crouch=118, kL=(-120, -100), kR=(120, -100), fL=(-150, -18), fR=(150, -18), aL=(-60, 130, 40, 200), aR=(120, 90, 210, 150), lean=10)
TIEP = dict(aR=(60, 130, 16, 150))                              # Kai kravatina dokunur
GLP = dict(aR=(96, 20, 62, -70))                                # Zoe gozlugunu duzeltir


def people(cv, ts, P, st, order=('L', 'U')):
    """P: {kim: (x, gy, s)}; st: {kim: (ifade, poz, bakis[, ek])}. ek: down (goz kapaklari inik), gl (pakette Zoe'nin gozlugu),
    ber (Luna'nin elinde Sam'in beresi), card (Leo'nun sag elinde yaka karti)"""
    out = {}
    for w in order:
        if w not in st: continue
        v = st[w]; kw = dict(v[3]) if len(v) > 3 else {}
        down = kw.pop('down', False); gl = kw.pop('gl', True); ber = kw.pop('ber', True); crd = kw.pop('card', False)
        has_pkg = w == 'L' and kw.get('pkg', True)
        if has_pkg: kw.setdefault('tie', True)
        a = kw.get('alpha', 1.0); bk = kw.get('back')
        if a <= 0.01: continue
        f = actor(cv, ts, w, v[0], v[1], v[2], place=P[w], **kw)
        s = P[w][2]
        if down and not bk: lids(cv, f)
        if w == 'U' and ber and not bk:
            beret_at(cv, (f['handL'][0] + f['handR'][0]) / 2, f['handL'][1] + 12, 0.5 * s / 0.54, a=a)
        if has_pkg and gl:
            x = (f['handL'][0] + f['handR'][0]) / 2 if not kw.get('pkg_left') else f['handL'][0] + 40 * s
            glasses_at(cv, x + 34 * s, f['handL'][1] + 4 * s - 82 * s, 0.6 * s / 0.7, rot=-6, a=a)
        if w == 'L' and crd and not bk: mini_card(cv, f['handR'][0] + 6 * s, f['handR'][1] - 34 * s, s, a)
        out[w] = f
    return out


# ---------- kucuk nesneler ----------
def cap_on(cv, hx, hy, HR, a=255, look=1.0, brim=True):
    """hardal kurye sapkasi (bir basin ustune)"""
    p = skia.Path(); p.addArc(LTRB(hx - HR * 1.05, hy - HR * 1.08, hx + HR * 1.05, hy + HR * 1.02), 208, 124); p.close()
    cv.drawPath(p, fill(MUSTARD, a))
    sd = -1 if look < -0.5 else 1
    if brim: cv.drawOval(LTRB(hx + sd * HR * 0.82 - HR * 0.68, hy - HR * 0.66, hx + sd * HR * 0.82 + HR * 0.68, hy - HR * 0.4), fill(shade(MUSTARD, 0.78), a))
    cv.drawCircle(hx, hy - HR * 1.04, HR * 0.09, fill(shade(MUSTARD, 0.7), a))


def mini_card(cv, x, y, s, a=1.0):
    w, h = 66 * s, 90 * s; A = 255 * a
    cv.save(); cv.translate(x, y); cv.rotate(-8)
    rc = LTRB(-w / 2, -h / 2, w / 2, h / 2)
    cv.drawRRect(RRXY(rc.makeOffset(3, 4), 6 * s, 6 * s), fill((4, 6, 20), 90 * a))
    cv.drawRRect(RRXY(rc, 6 * s, 6 * s), fill(CREAM, A))
    cv.drawRect(LTRB(-w / 2 + 5 * s, -h / 2 + 9 * s, w / 2 - 5 * s, -h / 2 + 27 * s), fill(RED, A))
    cv.drawCircle(0, 12 * s, 16 * s, fill(TEAL, A))
    p = skia.Path(); p.addArc(LTRB(-17 * s, -6 * s, 17 * s, 28 * s), 200, 140); p.close(); cv.drawPath(p, fill(MUSTARD, A))
    cv.restore()


def lbutton(cv, x, y, r, a=1.0, lit=0.0):
    """lobi dugmesi: uzerinde L"""
    A = 255 * a
    if lit > 0:
        gl = fill(GRN, 130 * lit * a); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * 0.5)); cv.drawCircle(x, y, r * 1.5, gl)
    cv.drawCircle(x + r * 0.06, y + r * 0.13, r, fill((16, 18, 30), 150 * a))
    cv.drawCircle(x, y, r, fill(lerpt((238, 228, 200), GRN, lit), A))
    cv.drawCircle(x, y, r * 0.8, dashed(INKBLUE, max(1.2, r * 0.055), 120 * a, (max(2, r * 0.15), max(2, r * 0.13))))
    text(cv, 'L', x, y + r * 0.34, r * 0.98, INKBLUE, a=A)


def mini_pkg(cv, x, y, s, a=1.0):
    """raftaki kucuk paket; (x, y): alt orta"""
    w, h = 176 * s, 124 * s
    cv.drawRRect(RRXY(LTRB(x - w / 2, y - h, x + w / 2, y), 3, 3), fill(BOXC, 255 * a))
    cv.drawRect(LTRB(x - w * 0.25, y - h * 0.74, x + w * 0.25, y - h * 0.28), fill(WHITE, 255 * a))
    cv.drawLine(x - w * 0.16, y - h * 0.51, x + w * 0.16, y - h * 0.51, stroke((190, 52, 56), max(1.5, h * 0.1), 255 * a, cap=False))


def chair(cv, x, y, s, c=(150, 60, 66), a=1.0, back=False):
    """bos sandalye; (x, y): ayaklarin alt ortasi. back: arkadan (karanlik siluet)"""
    A = 255 * a; d = shade(c, 0.6)
    for sd in (-1, 1): cv.drawLine(x + sd * 70 * s, y - 150 * s, x + sd * 78 * s, y, stroke(d, 16 * s, A, cap=False))
    cv.drawRRect(RRXY(LTRB(x - 78 * s, y - 340 * s, x + 78 * s, y - 150 * s), 18 * s, 18 * s), fill(c, A))
    if not back: cv.drawRRect(RRXY(LTRB(x - 60 * s, y - 322 * s, x + 60 * s, y - 180 * s), 12 * s, 12 * s), dashed(shade(c, 1.5), max(1.5, 3 * s), 200 * a, (10 * s + 2, 8 * s + 2)))
    cv.drawRRect(RRXY(LTRB(x - 92 * s, y - 172 * s, x + 92 * s, y - 136 * s), 12 * s, 12 * s), fill(shade(c, 0.8 if back else 1.2), A))


def arm(cv, p0, p1, c, w=44):
    cv.drawLine(p0[0], p0[1], p1[0], p1[1], stroke(shade(c, 0.56), w + 10)); cv.drawLine(p0[0], p0[1], p1[0], p1[1], stroke(shade(c, 0.92), w))
    cv.drawLine(p0[0], p0[1], p1[0], p1[1], dashed(shade(c, 1.3), 3.5, 190, (12, 10)))


def ping(cv, x, y, r, u):
    """vurgu halkasi: u 0..1"""
    if 0 < u < 1: cv.drawCircle(x, y, r * lerp(0.6, 1.5, u), stroke(CREAM, 7, 255 * (1 - u)))


def chip(cv, x, y, c, u=1.0, a=1.0):
    cv.drawCircle(x, y - 34 * u, 24 * u, fill(c, 255 * a))
    cv.drawRRect(RRXY(LTRB(x - 32 * u, y - 4 * u, x + 32 * u, y + 52 * u), 22 * u, 22 * u), fill(c, 255 * a))


def open_box(cv, x, y, s, a=1.0, items=True):
    """kabinin zemininde acik kutu (onden); (x, y): alt orta. Kenarinda Kai'nin kravati, kapaginda Zoe'nin gozlugu"""
    w, h, A = 210 * s, 124 * s, 255 * a
    cv.drawOval(LTRB(x - w * 0.62, y - 14 * s, x + w * 0.62, y + 18 * s), fill((4, 6, 20), 90 * a))
    for sd in (-1, 1):                                       # acik kapaklar
        poly(cv, [(x + sd * w / 2, y - h), (x + sd * (w / 2 + 74 * s), y - h - 34 * s), (x + sd * (w / 2 + 64 * s), y - h + 10 * s), (x + sd * w / 2, y - h + 34 * s)], shade(BOXC, 1.15), A)
    cv.drawRRect(RRXY(LTRB(x - w / 2, y - h, x + w / 2, y), 6, 6), fill(BOXC, A))
    cv.drawRect(LTRB(x - w / 2, y - h, x + w / 2, y - h + 14 * s), fill((92, 66, 44), A))
    cv.drawRRect(RRXY(LTRB(x - w / 2 + 9 * s, y - h + 22 * s, x + w / 2 - 9 * s, y - 9 * s), 4, 4), dashed((150, 108, 60), 2.5, 220 * a, (10, 8)))
    cv.drawRRect(RRXY(LTRB(x - 46 * s, y - 84 * s, x + 46 * s, y - 28 * s), 5, 5), fill(WHITE, A)); text(cv, 'KAT 13', x, y - 46 * s, 24 * s, (190, 52, 56), a=A)
    if items:
        tie_at(cv, x - w / 2 + 16 * s, y - h - 4 * s, 0.5 * s, a, rot=14)
        glasses_at(cv, x + w / 2 + 34 * s, y - h - 20 * s, 0.6 * s, rot=-14, a=a)
    return (x - w / 2 + 16 * s, y - h + 40 * s), (x + w / 2 + 34 * s, y - h - 20 * s)


def alarm(cv, k, g=1.0):
    """son 30 saniye: kirmizi isik yanip soner"""
    cv.drawRect(skia.Rect.MakeWH(W, H), fill((210, 24, 28), 255 * g * alt(k, 0.07, 0.19, 3)))


def title_card(cv, t):
    tb = B('title'); a = seg(t, tb[0], tb[0] + 0.35)
    if a > 0:
        dim(cv, 0.5 * a)
        card(cv, [(TITLE, 130, (255, 110, 96)), (f'{EP.title()}: {EP_NAME}', 48, CREAM)], a, lerp(0.9, 1.0, smooth(seg(t, tb[0], tb[0] + 0.5))))


# ---------- sayac ve kanca yazisi (kameradan sonra, ekran koordinatinda) ----------
def timer(cv, rem, a=1.0, big=1.0, pos=None):
    if a <= 0: return
    n = int(math.ceil(max(0.0, rem) - 1e-3)); txt = f'{n // 60:02d}:{n % 60:02d}'
    hot, warm = n <= 10, n <= 30
    u = (1.0 if FMT == 'v' else 0.8) * big
    w, h = 336 * u, 112 * u
    cx, cy = pos if pos else ((W / 2, 312) if FMT == 'v' else (W - 70 - w / 2, 84))
    beat = 1 - (max(0.0, rem) % 1.0)                         # her saniyenin basinda 1
    pu = 1 + (0.09 if hot else 0.03) * clamp(1 - beat * 4) if n > 0 else 1.0
    cv.save(); cv.translate(cx, cy); cv.scale(pu, pu)
    rc = LTRB(-w / 2, -h / 2, w / 2, h / 2)
    sh = fill((4, 6, 20), 140 * a); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12)); cv.drawRRect(RRXY(rc.makeOffset(6, 10), h / 2, h / 2), sh)
    cv.drawRRect(RRXY(rc, h / 2, h / 2), fill((86, 16, 24) if (hot and beat < 0.5) else INKBLUE, 245 * a))
    c = RED if warm else AMB
    cv.drawRRect(RRXY(rc.makeInset(8 * u, 8 * u), h / 2 - 8 * u, h / 2 - 8 * u), dashed(c if warm else (206, 214, 246), 2.5, 180 * a, (10, 8)))
    ix, iw, ih = -w / 2 + 66 * u, 56 * u, 62 * u               # kapi simgesi: sure azaldikca kapanir
    g = (iw / 2 - 2 * u) * clamp(rem / COUNT) ** 0.8
    cv.drawRect(LTRB(ix - iw / 2, -ih / 2, ix + iw / 2, ih / 2), fill((250, 228, 156), 255 * a))
    cv.drawRect(LTRB(ix - iw / 2, -ih / 2, ix - g, ih / 2), fill((150, 162, 178), 255 * a)); cv.drawRect(LTRB(ix + g, -ih / 2, ix + iw / 2, ih / 2), fill((150, 162, 178), 255 * a))
    cv.drawRect(LTRB(ix - iw / 2, -ih / 2, ix + iw / 2, ih / 2), stroke((206, 214, 246), 4 * u, 255 * a, cap=False))
    f = skia.Font(TFB, 70 * u); cell = 41 * u; x = 46 * u - (4 * cell + 22 * u) / 2 + 12 * u
    for ch in txt:
        cw = 22 * u if ch == ':' else cell; ww = f.measureText(ch)
        cv.drawString(ch, x + (cw - ww) / 2, 25 * u, f, fill(c, 255 * a)); x += cw
    cv.restore()


def hook_text(cv, t, a):
    if a <= 0: return
    size, y = (136, 560) if FMT == 'v' else (86, 216)
    sc_ = lerp(1.22, 1.0, smooth(seg(t, 0, 0.3)))
    f = skia.Font(TFB, size * sc_); f.setEmbolden(True); s = 'BİRİ KALIR'; w = f.measureText(s); x = W / 2 - w / 2
    st = stroke((0, 0, 0), size * 0.2, 255 * a); st.setStrokeJoin(skia.Paint.kRound_Join)
    cv.drawString(s, x + 5, y + 10, f, fill((0, 0, 0), 120 * a)); cv.drawString(s, x, y, f, st); cv.drawString(s, x, y, f, fill((255, 214, 80), 255 * a))


def hud(cv, t, k):
    if t < HOOK_END:                                         # kanca: sayac + buyuk yazi
        a = 1 - seg(t, HOOK_END - 0.25, HOOK_END)
        timer(cv, R_HOOK - t, a, big=1.35, pos=(W / 2, 330) if FMT == 'v' else (W / 2, 70))
        hook_text(cv, t, a)
    elif T0 <= t < T1 + 1.3:
        timer(cv, COUNT - (t - T0), min(seg(t, T0, T0 + 0.2), 1 - seg(t, T1 + 0.9, T1 + 1.3)), big=lerp(1.5, 1.0, smooth(seg(t, T0, T0 + 0.7))))
    if k == 14 and t >= S('n5') - 0.1:                       # dort kisi bindi, bes kisi indi
        marks = [(c, 'on') for c, f_ in zip((NAVY, CORAL, TAN, LILAC), TALLY[:4]) if t >= frac('n5', f_)]
        if t >= frac('n5', TALLY[4]): marks.append((MOMC, 'on'))
        tally(cv, marks)


# ---------- dekor: 17. kat, kabinin kapisindan gorunus ----------
_V = dict(lit=0.0, k=0, leo=None)
HZ = 1080                                                  # odanin zemin cizgisi (kapidan bakinca)
def view17(cv, near, far, lamp):
    lit, k = _V['lit'], _V['k']
    x0, y0, x1, y1 = near
    wall = lerpt(ROOMW0, ROOMW1, lit)
    cv.drawRect(LTRB(x0, y0, x1, HZ), fill(wall))
    cv.drawRect(LTRB(x0, HZ, x1, y1 + 10), fill(lerpt((10, 12, 22), (76, 50, 62), lit)))
    cv.drawLine(x0, HZ, x1, HZ, dashed(shade(wall, 1.7), 3, 110 + 90 * lit, (12, 9)))
    if lit > 0.02:                                           # raflar dolusu ayni paket
        for yy in (704, 794, 884):
            for sx0, sx1 in ((x0 + 4, 446), (634, x1 - 4)):
                cv.drawLine(sx0, yy, sx1, yy, stroke((28, 22, 40), 8, 255 * lit, cap=False))
                for i in range(3): mini_pkg(cv, lerp(sx0 + 34, sx1 - 34, i / 2), yy - 4, 0.3, lit)
        cv.drawRRect(RRXY(LTRB(458, 722, 622, 772), 8, 8), fill((150, 40, 46), 255 * lit))
        text(cv, 'GÖREVLİ', 540, 759, 31, CREAM, a=255 * lit)
    fl = 1.0 if lit > 0.5 else (0.7 + 0.3 * ((k * 5) % 7 > 1))
    poly(cv, [(540 - 26, 668), (540 + 26, 668), (540 + 170, HZ + 70), (540 - 170, HZ + 70)], (250, 236, 190), (40 + 26 * lit) * fl)
    cv.drawLine(540, y0, 540, 640, stroke((8, 10, 16), 4, cap=False))
    poly(cv, [(540 - 16, 636), (540 + 16, 636), (540 + 42, 672), (540 - 42, 672)], (20, 24, 34))
    cv.drawOval(LTRB(540 - 26, 664, 540 + 26, 682), fill((252, 240, 200), 255 * fl))
    chair(cv, 540, HZ + 26, 0.62)
    if _V['leo']: _V['leo'](cv)


def lbutton_lit(cv, sh=(0, 0)):
    """kabin panelinde takilmis L dugmesi (yesil)"""
    with stage(cv, *sh):
        gl = fill(GRN, 150); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12)); cv.drawCircle(956, 1022, 22, gl)
        cv.drawCircle(956, 1022, 12, fill(GRN))


# ---------- dekor: 17. kat, odanin icinden asansore bakis ----------
A0, A1, AT = 240, 840, 520
def room17(cv, k):
    cv.clear(col((8, 10, 18)))
    with stage(cv):
        x0, x1 = -520, 1620
        cv.drawRect(LTRB(x0, 250, x1, CFLOOR), fill((20, 24, 38)))
        for j in range(-2, 6):
            px = -560 + 380 * j; cv.drawRRect(RRXY(LTRB(px + 24, 470, px + 356, 1150), 10, 10), dashed((44, 52, 74), 3, 150, (16, 12)))
        cv.drawRect(LTRB(x0, CFLOOR, x1, 5000), fill((16, 16, 28)))
        cv.drawLine(x0, CFLOOR + 8, x1, CFLOOR + 8, dashed((92, 84, 120), 3.5, 150, (16, 12)))
        for sx0, sx1 in ((-470, 170), (910, 1550)):          # yanlarda los raflar: paket siluetleri
            for yy in (680, 860, 1040):
                cv.drawLine(sx0, yy, sx1, yy, stroke((8, 10, 18), 14, cap=False))
                for i in range(4):
                    px = lerp(sx0 + 84, sx1 - 84, i / 3); cv.drawRRect(RRXY(LTRB(px - 70, yy - 108, px + 70, yy - 8), 4, 4), fill((34, 36, 54)))
                    cv.drawRect(LTRB(px - 30, yy - 78, px + 30, yy - 40), fill((50, 54, 76)))
        # asansor: isikli kabin
        cv.drawRect(LTRB(A0 - 30, AT - 30, A1 + 30, CFLOOR), fill((34, 38, 54)))
        cv.drawRRect(RRXY(LTRB(540 - 82, AT - 122, 540 + 82, AT - 46), 12, 12), fill((20, 22, 34))); text(cv, '17', 540, AT - 62, 58, RED)
        cv.drawRect(LTRB(A0, AT, A1, CFLOOR), fill(shade(WALL, 1.14)))
        cv.drawRect(LTRB(A0, AT, A1, AT + 74), fill((62, 74, 88)))
        cv.drawRRect(RRXY(LTRB(540 - 160, AT + 22, 540 + 160, AT + 58), 18, 18), fill((252, 240, 200)))
        cv.drawRRect(RRXY(LTRB(A0 + 44, AT + 130, A1 - 44, CFLOOR - 30), 10, 10), dashed(shade(WALL, 1.5), 3.5, 190))
        cv.drawLine(A0 + 30, 1040, A1 - 30, 1040, stroke((58, 68, 82), 14, cap=False))
        cv.drawRect(LTRB(A0, CFLOOR - 8, A1, CFLOOR + 14), fill((80, 68, 96)))
        for xx in (A0, A1 - 28):
            cv.drawRect(LTRB(xx, AT, xx + 28, CFLOOR), fill((150, 162, 178))); cv.drawLine(xx + 14, AT + 10, xx + 14, CFLOOR - 10, dashed((214, 222, 236), 2.5, 200))
        poly(cv, [(A0, CFLOOR + 14), (A1, CFLOOR + 14), (A1 + 300, CFLOOR + 460), (A0 - 300, CFLOOR + 460)], (250, 228, 156), 46)


def room17_front(cv, k):
    """on plan: bos sandalye (arkadan) ve ustundeki lamba"""
    with stage(cv):
        cx_ = 905 if FMT == 'v' else 1190
        fl = 0.7 + 0.3 * ((k * 5) % 7 > 1)
        poly(cv, [(cx_ - 34, 520), (cx_ + 34, 520), (cx_ + 250, 1640), (cx_ - 250, 1640)], (250, 236, 190), 26 * fl)
        cv.drawLine(cx_, 250, cx_, 480, stroke((6, 8, 14), 5, cap=False))
        poly(cv, [(cx_ - 22, 476), (cx_ + 22, 476), (cx_ + 58, 524), (cx_ - 58, 524)], (16, 20, 30))
        cv.drawOval(LTRB(cx_ - 34, 514, cx_ + 34, 536), fill((250, 236, 190), 230 * fl))
        chair(cv, cx_, 1610, 1.5, c=(74, 34, 44), back=True)
        cv.drawLine(cx_ - 117, 1100, cx_ - 117, 1384, stroke((250, 228, 156), 5, 110))   # kabinden vuran isik: kenar parlamasi


# ============ SAHNE 9'un plani (kancada da kullanilir): karar ============
def climax(cv, ts, k):
    dc = B('decide'); o = ts - dc[0]
    _V.update(lit=1.0, k=k, leo=None)
    cabin(cv, (0, 0), 1.0, view=view17)
    if ts < E('u7') + 0.1: L_ = ('endise', dict(CARDP, crouch=16, lean=-8, belly=12), 0.4); U_ = ('bagir' if on(ts, 'u7', 0.0, 0.0) else 'endise', TUG, -2.0)
    elif o < 0.9: L_ = ('uzgun', dict(CARDP, crouch=12), 0, dict(down=True)); U_ = ('endise', HOLDB, -2.0)      # karta bakar
    elif o < 1.8: L_ = ('endise', CARDP, 2.0); U_ = ('endise', HOLDB, -2.0)                                 # Luna'ya bakar
    elif ts < S('l9') - 0.05: L_ = ('kararli', dict(CARDP, **LOOKUP), 0); U_ = ('endise', HOLDB, -2.0)
    else: L_ = ('kararli', dict(CARDP, **LOOKUP), 0.8 if ts < frac('l9', 0.45) else 1.6); U_ = ('saskin', HOLDB, -2.0)
    L_ = L_[:3] + (dict(L_[3] if len(L_) > 3 else {}, pkg=False, card=True),)
    with stage(cv):
        open_box(cv, 540, 1372, 0.8)
        people(cv, ts, CAB, {'L': L_, 'U': U_})
    lbutton_none = None
    alarm(cv, k); dim(cv, 0.16)
    display(cv, (0, 0), '17', red=True)


# ============ SAHNE 1: kanca + hatirlatma + baslik ============
WAITP = {'S': (112, GY - 20, 0.62), 'Z': (318, GY - 20, 0.62), 'K': (846, GY - 20, 0.62), 'U': (694, GY + 26, 0.50)}
def scene1(cv, t):
    ts, k = step(t), kk(t)
    if ts < HOOK_END:                                        # 90 saniyenin icinden bir an: Luna "Kim kalacak?"
        climax(cv, S('u7') + min(ts, E('u7') - S('u7') + 1.3), k)
        flash(cv, 0.8 * seg(t, HOOK_END - 0.2, HOOK_END))
        return
    u = smooth(seg(ts, frac('n2', 0.40), frac('n2', 0.60)))  # onceki bolum: lobi; kapi acilir, Leo zaten iceride
    def inside(c): actor(c, ts, 'L', 'sakin', {}, 0, place=(540, FLOOR - 6, 0.56), talk=None)
    with tint(cv, sepia_m(0.72, 0.05)):
        lobby(cv, u, inside=inside)
        with stage(cv):
            for w in ('S', 'Z', 'K', 'U'): actor(cv, ts, w, 'sakin', {}, 0, back=True, place=WAITP[w], talk=None)
    display(cv, (0, 0), '1')
    dim(cv, 0.12)
    memory_frame(cv, 'ÖNCEKİ BÖLÜM')
    tally(cv, [(CREAM, 'on')] * 4 + ([(RED, 'on')] if ts >= frac('n2', 0.76) else []))
    flash(cv, 0.8 * (1 - seg(t, HOOK_END, HOOK_END + 0.25)))
    title_card(cv, t)


# ============ SAHNE 2: kabin, 16'dan 17'ye ============
def scene2(cv, t):
    ts, k = step(t), kk(t)
    dg = B('ding'); u = smooth(seg(ts, dg[0] + DOOR_OPEN, dg[1] - 0.1))
    moving = ts < B('ride')[1] + 0.8 or S('u2') <= ts < dg[0] + 0.1
    sh = jit(k, 3 if moving else 0)
    _V.update(lit=0.0, k=k, leo=None)
    cabin(cv, sh, u, view=view17)
    glow = 0.0
    if ts < S('l1') - 0.1: L_ = ('endise', {}, 0, dict(down=True)); U_ = ('sakin', HOLDB, 0)
    elif ts < S('u1') - 0.1: L_ = ('endise', dict(crouch=10, lean=6), 1.2); U_ = ('sakin', HOLDB, -2.0)
    elif ts < S('l2') - 0.1: L_ = ('endise', {}, 1.2); U_ = ('sakin', POINT_PK if ts >= frac('u1', 0.35) else HOLDB, -2.0); glow = seg(ts, frac('u1', 0.35), frac('u1', 0.6))
    elif ts < S('u2') - 0.1: L_ = ('panik' if ts > frac('l2', 0.3) else 'endise', dict(HOLDUP, crouch=8), 1.2); U_ = ('merak', HOLDB, -2.0)
    elif ts < dg[0] + 0.15: L_ = ('endise', {}, 0 if ts > E('u2') else 1.2, dict(down=ts > E('u2'))); U_ = ('sakin', HOLDB, -2.0)
    elif ts < dg[0] + DOOR_OPEN + 0.3: L_ = ('saskin', LOOKUP, 0); U_ = ('sakin', dict(HOLDB, **LOOKUP), 0)       # ding: goster geye bakarlar
    else: L_ = ('saskin', HOLD, 0, dict(back=True, pkg=False)); U_ = ('sakin', {}, 0, dict(back=True))             # kapiya donerler
    with stage(cv, *sh):
        if glow > 0:
            f0 = geo(CAB['L'][0], CAB['L'][1], CAB['L'][2], dict(IDLE, **HOLD))
            gl = fill((255, 226, 150), 110 * glow); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 34))
            cv.drawOval(LTRB(f0['armL'][-1][0] - 60, f0['armL'][-1][1] - 100, f0['armR'][-1][0] + 60, f0['armR'][-1][1] + 100), gl)
        people(cv, ts, CAB, {'L': L_, 'U': U_})
    dim(cv, 0.2)
    display(cv, sh, '17' if ts >= dg[0] + 0.15 else '16', red=True)


# ============ SAHNE 3: kural; sayac baslar ============
def scene3(cv, t):
    ts, k = step(t), kk(t)
    vt = TL.talk('V', ts); lk = B('look')
    _V.update(lit=0.0, k=k, leo=None)
    cabin(cv, (0, 0), 1.0, view=view17)
    rule = frac('v1', 0.72)
    BK = (('saskin', HOLD, 0, dict(back=True, pkg=False)), ('sakin', {}, 0, dict(back=True)))
    if ts < rule: L_, U_ = BK
    elif ts < S('v2') - 0.1: L_ = ('saskin', {}, 1.6); U_ = ('saskin', HOLDB, -2.0)                           # "biri kalir": birbirlerine bakarlar
    elif ts < T0: L_ = ('endise', LOOKUP, 0); U_ = ('sakin', dict(HOLDB, **LOOKUP), 0)
    elif ts < S('v3') + 0.3: L_ = ('panik', dict(LOOKUP, crouch=10), 0); U_ = ('saskin', dict(HOLDB, **LOOKUP), 0)   # sayac belirir
    elif ts < lk[0] + 0.3: L_ = ('endise', COWER_HOLD, 1.4); U_ = ('endise', HOLDB, -1.6)
    else: L_, U_ = BK                                                                                        # bos sandalyeye bakarlar
    with stage(cv):
        people(cv, ts, CAB, {'L': L_, 'U': U_})
    dim(cv, 0.2)
    display(cv, (0, 0), '17', red=True, level=vt, k=k)


# ============ SAHNE 4: 17. kattan kabine bakis ============
RL, RU = (420, CFLOOR + 4, 0.72), (672, CFLOOR + 4, 0.50)
def scene4(cv, t):
    ts, k = step(t), kk(t)
    room17(cv, k)
    go = smooth(seg(ts, frac('u3', 0.04), frac('u3', 0.5)))  # Luna disari adim atar
    pu = (lerp(RU[0], 632, go), lerp(RU[1], CFLOOR + 96, go), lerp(RU[2], 0.6, go))
    wk = 0 < go < 1
    if ts < S('l3') - 0.05:
        U_ = ('kararli', dict(walk(go * 150, pu[2], -1, hold=True), **HOLDB) if wk else HOLDB, 0)
        L_ = ('endise', {}, 2.0 if go > 0.2 else 0)
    elif ts < frac('l3', 0.2): U_ = ('saskin', HOLDB, -2.0); L_ = ('bagir', STOP, 2.0, dict(pkg_left=True))  # "Dur!"
    else: U_ = ('merak', HOLDB, -2.0); L_ = ('endise', STOP if ts < frac('l3', 0.5) else dict(HOLDUP, lean=8), 2.0 if ts < frac('l3', 0.5) else 1.0, dict(pkg_left=ts < frac('l3', 0.5)))
    with stage(cv):
        people(cv, ts, {'L': RL, 'U': pu}, {'L': L_, 'U': U_})
    room17_front(cv, k)
    dim(cv, 0.1)


def panel_xf(cv):
    """dikeyde panel yakin plani kuculur ve yukari kayar: L yuvasi ortadaki altyazinin ustunde kalsin"""
    if FMT == 'v': cv.translate(W / 2, 700); cv.scale(0.8, 0.8); cv.translate(-W / 2, -800)


# ============ SAHNE 5: kutu (ustten) ============
BX, BY, BW, BH = 540, 965, 590, 420
BTN5, CRD5 = (BX - 135, BY + 15), (BX + 138, BY)
LX, LY = 540, 585                                          # Leo (ustten): kutunun basinda comelmis
UX, UY = 925, 1010                                         # Luna (ustten): kutunun saginda
def box_top(cv, fl, rip, k):
    rc = LTRB(BX - BW / 2, BY - BH / 2, BX + BW / 2, BY + BH / 2)
    cv.drawRRect(RRXY(rc.makeOffset(14, 22), 10, 10), fill((4, 6, 20), 120))
    cv.drawRRect(RRXY(rc, 8, 8), fill(shade(BOXC, 0.9)))
    if fl > 0:                                               # kutunun ici
        inn = rc.makeInset(22, 22); cv.drawRect(inn, fill((96, 68, 46)))
        cv.drawRect(LTRB(inn.left(), inn.top(), inn.right(), inn.top() + 46), fill((40, 26, 18), 120))
        gl = fill((255, 226, 150), 120 * fl * (0.8 + 0.2 * alt(k, 0, 1, 3))); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 50))
        cv.drawOval(LTRB(BX - 250, BY - 160, BX + 250, BY + 160), gl)


def box_flaps(cv, fl, rip):
    rc = LTRB(BX - BW / 2, BY - BH / 2, BX + BW / 2, BY + BH / 2)
    for sd in (-1, 1):
        edge = BX + sd * BW / 2
        if fl < 0.5:                                         # kapali kapak daralir (mentese dis kenarda)
            wd = (BW / 2) * (1 - fl * 2)
            r_ = LTRB(min(edge, edge - sd * wd), rc.top(), max(edge, edge - sd * wd), rc.bottom())
            cv.drawRect(r_, fill(shade(BOXC, 1.0 - 0.3 * fl)))
            if wd > 60: cv.drawRect(r_.makeInset(14, 14), dashed((150, 108, 60), 3, 200, (12, 9)))
        else:                                                # acik kapak disari uzanir
            wd = (BW * 0.34) * (fl * 2 - 1)
            r_ = LTRB(min(edge, edge + sd * wd), rc.top() + 14, max(edge, edge + sd * wd), rc.bottom() - 14)
            cv.drawRect(r_, fill(shade(BOXC, 1.16)))
            if wd > 60: cv.drawRect(r_.makeInset(12, 12), dashed((150, 108, 60), 2.5, 170, (12, 9)))
    if fl <= 0:
        cv.drawLine(BX, rc.top(), BX, rc.bottom(), stroke((150, 108, 60), 3, cap=False))
        lb = LTRB(BX - 250, BY - 150, BX - 50, BY - 56)
        cv.drawRRect(RRXY(lb, 8, 8), fill(WHITE)); text(cv, 'KAT 13', BX - 150, BY - 86, 46, (190, 52, 56))
        if rip < 1:                                          # bant: alttan yukari sokulur
            tp = LTRB(BX - 24, rc.top() - 10, BX + 24, lerp(rc.bottom() + 10, rc.top() - 10, rip))
            cv.drawRect(tp, fill((238, 226, 190), 235)); cv.drawRect(tp.makeInset(6, 0), dashed((176, 150, 104), 2.5, 200, (10, 8)))


def scene5(cv, t):
    ts, k = step(t), kk(t)
    op = B('open'); o = ts - op[0]
    rip = seg(o, RIP, RIP + 0.45); fl = smooth(seg(o, FLAPS, FLAPS + 0.8))
    ia = seg(fl, 0.3, 0.8)
    lift = smooth(seg(ts, frac('l5', 0.45), frac('l5', 0.65))) * (1 - smooth(seg(ts, E('l5') + 0.05, E('l5') + 0.3)))
    pa = smooth(seg(ts, frac('u4', 0.36), frac('u4', 0.48))) * (1 - smooth(seg(ts, E('u4') + 0.05, E('u4') + 0.3)))   # panel yakin plani
    cv.clear(col((62, 52, 78)))
    with stage(cv):
        cv.drawRect(LTRB(-600, 300, 1700, 1750), fill((80, 68, 96)))
        for yy in range(390, 1750, 150): cv.drawLine(-600, yy, 1700, yy, dashed((112, 98, 134), 3, 90, (16, 12)))
        poly(cv, [(250, 300), (830, 300), (1040, 1750), (40, 1750)], (250, 228, 156), 30)       # kapidan vuran isik
        for x0_, x1_ in ((-600, -330), (1410, 1700)):
            cv.drawRect(LTRB(x0_, 300, x1_, 1750), fill(shade(WALL, 0.5)))
        cv.drawLine(-330, 300, -330, 1750, dashed(shade(WALL, 1.2), 4, 170, (16, 12))); cv.drawLine(1410, 300, 1410, 1750, dashed(shade(WALL, 1.2), 4, 170, (16, 12)))
        tie_at(cv, 96, 1010, 0.9, rot=64)                    # Kai'nin kravati ve Zoe'nin gozlugu: paketin ustunden alindi
        glasses_at(cv, 170, 1300, 1.25, rot=-12)
        # Leo (ustten): omuzlar
        cv.drawOval(LTRB(LX - 196, LY - 46, LX + 196, LY + 78), fill(shade(TEAL, 0.6)))
        cv.drawOval(LTRB(LX - 186, LY - 40, LX + 186, LY + 68), fill(TEAL))
        cv.drawOval(LTRB(LX - 168, LY - 28, LX + 168, LY + 54), dashed(shade(TEAL, 1.3), 3, 170, (12, 10)))
        # Luna (ustten): omuzlar
        cv.drawOval(LTRB(UX - 70, UY - 112, UX + 78, UY + 112), fill(shade(LILAC, 0.6)))
        cv.drawOval(LTRB(UX - 62, UY - 104, UX + 70, UY + 104), fill(LILAC))
        box_top(cv, fl, rip, k)
        if ia > 0:
            hl = (on(ts, 'l4', 0.1, 0.2) or (on(ts, 'u4') and pa < 0.5) or lift > 0)
            cx_, cy_ = CRD5
            cv.save(); cv.translate(cx_, cy_); cv.rotate(9 + (alt(k, -3, 3, 2) if S('u5') + 0.6 <= ts else 0))   # kart: yuzu asagi
            rc = LTRB(-88, -118, 88, 118)
            cv.drawRRect(RRXY(rc.makeOffset(6, 9), 14, 14), fill((20, 12, 8), 130 * ia))
            cv.drawRRect(RRXY(rc, 14, 14), fill((218, 210, 190), 255 * ia)); cv.drawRRect(RRXY(rc.makeInset(10, 10), 9, 9), dashed(INKBLUE, 2.5, 110 * ia, (9, 7)))
            cv.drawRRect(RRXY(LTRB(-26, -104, 26, -90), 7, 7), fill((60, 64, 84), 255 * ia)); cv.restore()
            if ts >= S('u5') + 0.6: ping(cv, cx_, cy_, 150, ((ts - S('u5') - 0.6) % 0.9) / 0.9)
            bx, by, br = BTN5[0], BTN5[1] - 34 * lift, 72 * (1 + 0.22 * lift)
            if lift > 0: cv.drawOval(LTRB(bx - 60, BTN5[1] + 34, bx + 76, BTN5[1] + 84), fill((20, 12, 8), 110 * lift))
            lbutton(cv, bx, by, br, ia)
            if hl and ia >= 1: cv.drawCircle(bx, by, br + 20 + (6 if (k // 3) % 2 else 0), dashed(AMB, 6, 255, (16, 11)))
        box_flaps(cv, fl, rip)
        # Leo'nun kollari ve elleri
        if o < RIP: hL, hR = (BX - 70, BY - 150), (BX + 70, BY - 150)
        elif fl <= 0: hL, hR = (BX - 70, BY - 150), (lerp(BX + 30, BX + 250, rip), lerp(BY + 120, BY - 330, rip))
        else: hL, hR = (lerp(BX - 70, BX - BW / 2 - 60, fl), BY - 130), (lerp(BX + 250, BX + BW / 2 + 60, fl), lerp(BY - 330, BY - 130, fl))
        if lift > 0 or on(ts, 'l4', 0.1, 0.2): hL = (lerp(hL[0], BTN5[0] - 96, max(lift, 0.9 if on(ts, 'l4', 0.1, 0.2) else 0)), lerp(hL[1], BTN5[1] - 40 - 34 * lift, max(lift, 0.9 if on(ts, 'l4', 0.1, 0.2) else 0)))
        arm(cv, (LX - 150, LY + 20), hL, TEAL, 50); arm(cv, (LX + 150, LY + 20), hR, TEAL, 50)
        hand_ball(cv, hL[0], hL[1], 46, TEAL, 2); hand_ball(cv, hR[0], hR[1], 46, TEAL, 4)
        if 0 < rip and fl <= 0:                              # sokulen bant elde
            cv.save(); cv.translate(hR[0], hR[1]); cv.rotate(-30 - 40 * rip); cv.drawRect(LTRB(-20, 0, 20, 150 * rip + 30), fill((238, 226, 190), 235)); cv.restore()
        # Leo'nun sapkasi (ustten)
        cv.drawOval(LTRB(LX - 86, LY + 30, LX + 86, LY + 138), fill(shade(MUSTARD, 0.78)))
        cv.drawCircle(LX + 4, LY - 2, 110, fill((4, 6, 20), 70)); cv.drawCircle(LX, LY - 8, 106, fill(MUSTARD))
        cv.drawCircle(LX, LY - 8, 88, dashed(shade(MUSTARD, 0.66), 3, 190, (12, 10))); cv.drawCircle(LX, LY - 8, 13, fill(shade(MUSTARD, 0.7)))
        # Luna: kol (gosterirken), bas, fiyonk
        tgt = None
        if on(ts, 'u4') and pa < 0.5: tgt = (BTN5[0] + 150, BTN5[1] + 60)
        elif ts >= S('u5') - 0.1: tgt = (CRD5[0] + 130, CRD5[1] + 40)
        if tgt: arm(cv, (UX - 30, UY + 40), tgt, LILAC, 38); hand_ball(cv, tgt[0], tgt[1], 36, LILAC, 5)
        hand_ball(cv, UX, UY, 74, LILAC, 9)
        for sd in (-1, 1): poly(cv, [(UX + 30, UY - 52), (UX + 30 + sd * 40, UY - 78), (UX + 30 + sd * 40, UY - 26)], PINKB)
        cv.drawCircle(UX + 30, UY - 52, 10, fill(shade(PINKB, 0.8)))
        beret_at(cv, UX - 6, UY + 150, 0.42, rot=-10)
    dim(cv, 0.12)
    if pa > 0:                                               # "Panelde tam onun yeri bos"
        dim(cv, 0.6 * pa)
        cv.save(); panel_xf(cv)
        panel_closeup(cv, pa, hi=seg(ts, frac('u4', 0.5), frac('u4', 0.62)), k=k, finger=LILAC); cv.restore()


# ============ SAHNE 6: yaka karti ============
def idcard(cv, x, y, s, turn):
    """turn 0: arka yuz .. 1: on yuz (GOREVLI)"""
    w, h = 470 * s, 640 * s
    sx = math.cos(math.pi * (1 - turn)); front = sx > 0
    cv.save(); cv.translate(x, y); cv.rotate(lerp(8, -3, turn)); cv.scale(max(0.04, abs(sx)), 1)
    rc = LTRB(-w / 2, -h / 2, w / 2, h / 2)
    sh = fill((4, 6, 20), 150); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16)); cv.drawRRect(RRXY(rc.makeOffset(12, 18), 30 * s, 30 * s), sh)
    cv.drawRRect(RRXY(rc, 30 * s, 30 * s), fill(CREAM if front else (218, 210, 190)))
    cv.drawRRect(RRXY(rc.makeInset(16 * s, 16 * s), 20 * s, 20 * s), dashed(INKBLUE, 3 * s, 120, (12 * s, 9 * s)))
    cv.drawRRect(RRXY(LTRB(-48 * s, -h / 2 + 24 * s, 48 * s, -h / 2 + 46 * s), 11 * s, 11 * s), fill((60, 64, 84)))
    if front:
        cv.drawRRect(RRXY(LTRB(-w / 2 + 34 * s, -h / 2 + 70 * s, w / 2 - 34 * s, -h / 2 + 178 * s), 18 * s, 18 * s), fill((204, 54, 58)))
        text(cv, 'GÖREVLİ', 0, -h / 2 + 152 * s, 78 * s, CREAM)
        py, r = 38 * s, 110 * s
        cv.drawCircle(0, py, 158 * s, fill((176, 190, 232))); cv.drawCircle(0, py, 148 * s, dashed(INKBLUE, 3 * s, 110, (10 * s, 8 * s)))
        def d(c_): stil.R.seed(5); yarn_ball(c_, r + 16, r + 16, r, TEAL)
        blit(cv, sprite(('idhead', round(r, 1)), 2 * r + 40, 2 * r + 44, d), -r - 16, py + 12 * s - r - 16)
        face(cv, 0, py + 18 * s, r, 'sakin')
        cap_on(cv, 0, py + 12 * s, r)
        text(cv, 'LEO', 0, h / 2 - 62 * s, 66 * s, INKBLUE)
        text(cv, '13. KAT ASANSÖRÜ', 0, h / 2 - 28 * s, 26 * s, (120, 130, 160))
    cv.restore()


def scene6(cv, t):
    ts, k = step(t), kk(t)
    cd = B('card'); turn = smooth(seg(ts, cd[0] + FLIP, cd[0] + FLIP + 0.7)); rise = smooth(seg(ts, cd[0], cd[0] + 0.45))
    _V.update(lit=0.0, k=k, leo=None)
    cabin(cv, (0, 0), 1.0, view=view17); dim(cv, 0.76)
    x, y, s = 540, lerp(1000, 812, rise) + alt(k, 0, 3, 4), 0.9
    with stage(cv):
        gl = fill((255, 236, 190), 80 * turn); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 70)); cv.drawOval(LTRB(x - 330, y - 400, x + 330, y + 400), gl)
        for sd in (-1, 1): arm(cv, (x + sd * 200, y + 244), (x + sd * 330, 1760), TEAL, 74)
        idcard(cv, x, y, s, turn)
        for sd in (-1, 1): hand_ball(cv, x + sd * 200, y + 244, 58, TEAL, 3 + sd)
        if ts >= frac('n3', 0.5):                            # gorevli: yolculari yukari tasiyan kisi
            a = seg(ts, frac('n3', 0.5), frac('n3', 0.58)); sx_ = 150 if FMT == 'v' else 60
            cv.drawRRect(RRXY(LTRB(sx_ - 62, 540, sx_ + 62, 1130), 26, 26), fill(INKBLUE, 200 * a))
            cv.drawRRect(RRXY(LTRB(sx_ - 52, 550, sx_ + 52, 1120), 20, 20), dashed((206, 214, 246), 2.5, 170 * a, (10, 8)))
            for i, (c, f_) in enumerate(zip((NAVY, CORAL, TAN, LILAC), (0.62, 0.72, 0.82, 0.92))):
                if ts < frac('n3', f_): continue
                r_ = smooth(seg(ts, frac('n3', f_), frac('n3', f_) + 0.5))
                chip(cv, sx_, lerp(1090, 612 + i * 122, r_), c, 0.9)
            poly(cv, [(sx_, 462), (sx_ + 40, 516), (sx_ - 40, 516)], CREAM, 255 * a)
    dim(cv, 0.08)


# ============ SAHNE 7: kabin; 17. katin isiklari yanar ============
def lit_at(ts):
    lt = frac('v4', LIGHTS)
    if ts < lt: return 0.0
    if ts < lt + 0.55: return 1.0 if int((ts - lt) / 0.09) % 2 == 0 else 0.2
    return 1.0


def scene7(cv, t):
    ts, k = step(t), kk(t)
    vt = TL.talk('V', ts); turn_t = frac('v4', 0.66)
    _V.update(lit=lit_at(ts), k=k, leo=None)
    cabin(cv, (0, 0), 1.0, view=view17)
    C = dict(pkg=False, card=True)
    f_ = lambda x: ts >= frac('l7', x)
    if ts < turn_t: L_ = ('saskin', FREE, 0, dict(back=True, pkg=False)); U_ = ('sakin', {}, 0, dict(back=True))
    elif ts < S('u6') - 0.1: L_ = ('saskin', CARDP, 0.4, C); U_ = ('saskin', HOLDB, -2.0)
    elif ts < S('l7') - 0.1: L_ = ('endise', CARDP, 2.0, C); U_ = ('merak', dict(HOLDB, lean=-12, belly=6), -2.0)
    else: L_ = ('sakin', POINT_BOX if f_(0.3) and not f_(0.82) else CARDP, 2.0 if not f_(0.3) or f_(0.82) else 1.0, C); U_ = ('saskin', BERUP if f_(0.82) else HOLDB, -2.0 if not f_(0.82) else 0)
    with stage(cv):
        tp, gp = open_box(cv, 540, 1372, 0.8)
        people(cv, ts, CAB, {'L': L_, 'U': U_})
        if ts >= S('l7'):                                    # Kai (kravat), Zoe (gozluk), Sam (bere)
            ping(cv, tp[0], tp[1], 60, seg(ts, frac('l7', 0.34), frac('l7', 0.34) + 0.6))
            ping(cv, gp[0], gp[1], 60, seg(ts, frac('l7', 0.6), frac('l7', 0.6) + 0.6))
            ping(cv, CAB['U'][0], CAB['U'][1] - 300 * CAB['U'][2], 70, seg(ts, frac('l7', 0.86), frac('l7', 0.86) + 0.6))
    dim(cv, 0.18)
    display(cv, (0, 0), '17', red=True, level=vt, k=k)


# ============ SAHNE 8: raflar dolusu ayni paket ============
def shelves(cv, ts, k, pan):
    cv.clear(col((30, 24, 40)))
    with stage(cv):
        cv.drawRect(LTRB(-900, 200, 2000, 1800), fill(ROOMW1))
        for j in range(-3, 8):
            px = -700 + 330 * j - pan * 0.5; cv.drawLine(px, 300, px, 1500, dashed(shade(ROOMW1, 1.35), 3, 110, (16, 12)))
        lx = 540
        poly(cv, [(lx - 60, 530), (lx + 60, 530), (lx + 620, 1700), (lx - 620, 1700)], (250, 236, 190), 26)
        cv.drawLine(lx, 200, lx, 470, stroke((10, 10, 18), 6, cap=False))
        poly(cv, [(lx - 30, 466), (lx + 30, 466), (lx + 86, 536), (lx - 86, 536)], (22, 22, 34))
        cv.drawOval(LTRB(lx - 44, 524, lx + 44, 556), fill((252, 240, 200)))
        for row, yy in enumerate((800, 1030, 1260)):
            cv.drawRect(LTRB(-900, yy, 2000, yy + 24), fill((34, 26, 46))); cv.drawLine(-900, yy + 4, 2000, yy + 4, dashed((96, 80, 120), 3, 160, (14, 10)))
            for i in range(-5, 11):
                px = 92 + i * 224 - pan + (row % 2) * 112
                if px < -560 or px > 1640: continue
                if row == 1 and i == 1:                      # bos yer: Leo'nun getirdigi paket
                    cv.drawRRect(RRXY(LTRB(px - 82, yy - 118, px + 82, yy - 4), 8, 8), dashed(CREAM, 4, 150 + 100 * alt(k, 0, 1, 4), (14, 10)))
                else: package(cv, {'handL': (px, yy - 61), 'handR': (px, yy - 61)}, 0.92)
        cv.drawRect(LTRB(-900, 1470, 2000, 1900), fill((40, 30, 46)))
    dim(cv, 0.2)


def scene8(cv, t):
    ts, k = step(t), kk(t)
    a, _ = TL.span(8)
    if ts < S('v6') - 0.1:
        shelves(cv, ts, k, 150 * seg(ts, a, S('v6')))
        return
    vt = TL.talk('V', ts)                                    # asansorun cevabi: Leo raflara bakar (arkadan)
    _V.update(lit=1.0, k=k, leo=None)
    with zoom(cv, 1.3, (540, 930)):
        cabin(cv, (0, 0), 1.0, view=view17)
        with stage(cv):
            open_box(cv, 540, 1372, 0.8)
            people(cv, ts, CAB, {'L': ('uzgun', dict(FREE, **SLUMP), 0, dict(back=True, pkg=False)),
                                 'U': ('endise', HOLDB, -2.0 if ts < frac('v6', 0.5) else 0)})
        dim(cv, 0.2)
        display(cv, (0, 0), '17', red=True, level=vt, k=k)


# ============ SAHNE 9: karar ============
def scene9(cv, t):
    climax(cv, step(t), kk(t))


# ============ SAHNE 10: panel; L dugmesi yuvasina takilir ============
def scene10(cv, t):
    ts, k = step(t), kk(t)
    bt = B('btn'); o = ts - bt[0]; done = o >= CLICK
    _V.update(lit=1.0, k=k, leo=None)
    cabin(cv, (0, 0), 1.0, view=view17); alarm(cv, k); dim(cv, 0.62)
    cv.save()
    panel_xf(cv)
    panel_closeup(cv, 1.0, hi=0.0 if done else 1.0, k=k)
    u = 1.0 if FMT == 'v' else 0.80; cx_, cy_ = (W / 2, 800) if FMT == 'v' else (W / 2, 468)
    sx, sy = cx_, cy_ - 950 * u / 2 + 112 * u + 6 * 118 * u
    ap = smooth(seg(o, 0.5, CLICK)); bk = smooth(seg(o, CLICK + 0.25, CLICK + 0.9))
    bx, by = lerp(sx - 300 * u, sx, ap), lerp(sy + 380 * u, sy, ap)
    hx, hy = lerp(bx - 44 * u, sx - 300 * u, bk), lerp(by + 66 * u, sy + 420 * u, bk)
    if done:
        g = seg(o, CLICK, CLICK + 0.2)
        lbutton(cv, sx, sy, 46 * u * lerp(0.86, 1.0, g), lit=1.0)
        text(cv, 'L', sx - 128 * u, sy + 22 * u, 62 * u, GRN)
        r_ = seg(o, CLICK, CLICK + 0.55)
        if r_ < 1: cv.drawCircle(sx, sy, (56 + 90 * r_) * u, stroke(GRN, 7 * u, 255 * (1 - r_)))
        text(cv, 'LOBİ', sx + 150 * u, sy + 18 * u, 46 * u, GRN, a=255 * seg(o, CLICK + 0.1, CLICK + 0.4))
    else:
        lbutton(cv, bx, by, 46 * u)
    arm(cv, (hx - 250 * u, hy + 420 * u), (hx, hy), TEAL, 62 * u); hand_ball(cv, hx, hy, 52 * u, TEAL, 3)
    cv.restore()


# ============ SAHNE 11: veda; kapi 00:00'da kapanir ============
PA, PB, PC = (330, GY + 26, 0.80), (540, FLOOR + 8, 0.50), (415, HZ + 50, 0.42)
UA, UB, UC = (770, GY + 26, 0.56), (640, FLOOR + 20, 0.44), (640, GY - 26, 0.50)
def lerp3(p, q, u): return tuple(lerp(a, b, u) for a, b in zip(p, q))
def scene11(cv, t):
    ts, k = step(t), kk(t)
    ot, ps, cl = B('out'), B('push'), B('close')
    w = seg(ts, ot[0] + 0.25, ot[0] + 2.1)                   # Leo'nun yolu: kabin -> esik -> oda
    pl = lerp3(PA, PB, smooth(w / 0.55)) if w < 0.55 else lerp3(PB, PC, smooth((w - 0.55) / 0.45))
    walking = 0 < w < 1
    dist = math.hypot(pl[0] - PA[0], (pl[1] - PA[1]) * 2.2)
    run_u = smooth(seg(ts, frac('u8', 0.0), frac('u8', 0.38)))   # Luna esige kosar
    psh = smooth(seg(ts, ps[0] + PUSH, ps[0] + PUSH + 0.45))     # Leo iter: Luna geri kayar
    pu = lerp3(lerp3(UA, UB, run_u), UC, psh)
    step_in = smooth(seg(ts, ps[0] + 0.1, ps[0] + PUSH)) * (1 - smooth(seg(ts, ps[0] + PUSH + 0.3, ps[1])))   # Leo esige gelir, sonra geri cekilir
    if not walking and w >= 1: pl = lerp3(PC, (560, FLOOR - 26, 0.46), step_in)
    u = 1 - smooth(seg(ts, cl[0] + CLOSE_START, cl[1] - 0.05)) if ts < cl[1] - 0.05 else 0.0
    # --- Leo ---
    C = dict(pkg=False)
    if ts < ot[0] + 0.25: L_ = ('kararli', CARDP, 0, dict(C, card=True))
    elif walking: L_ = ('kararli', walk(dist, pl[2], 1, off=0.2), 0, dict(C, back=True))
    elif ts < S('u8') + 0.2: L_ = ('kararli', FREE, 0, dict(C, back=ts < ot[1] - 0.15))
    elif ts < ps[0]: L_ = ('sakin' if ts >= S('l10') - 0.1 else 'endise', FREE, 0.6, C)
    elif ts < ps[1] - 0.2: L_ = ('kararli', mixpose(FREE, PUSHP, step_in), 0.6, C)
    elif ts < cl[0] + 0.3: L_ = ('sakin', FREE, 0.6, C)
    else: L_ = ('sakin', alt(k, WAVE_A, WAVE_B, 3), 0.6, C)                                                  # el sallar
    # --- Luna ---
    if ts < S('u8') - 0.05: U_ = ('saskin', HOLDB, -2.0)
    elif run_u < 1: U_ = ('endise', dict(walk(run_u * 190, pu[2], -1, run=True, hold=True), **HOLDB), 0, dict(back=True))
    elif ts < ps[0] + PUSH: U_ = ('endise', dict(aL=(-90, 70, -110, -10), aR=(90, 110, 100, 200)), 0, dict(back=True))   # Leo'ya uzanir
    elif ts < cl[0] + CLOSE_START: U_ = ('uzgun', FREE, 0, dict(back=True))
    else: U_ = ('uzgun', mixpose(FREE, DOORP, seg(ts, cl[0] + CLOSE_START + 1.2, cl[0] + CLOSE_START + 2.0)), 0, dict(back=True))
    in_room = w >= 0.55
    def leo_far(c): people(c, ts, {'L': pl}, {'L': L_}, order=('L',))
    _V.update(lit=1.0, k=k, leo=leo_far if in_room else None)
    sh = jit(k, 5 if cl[1] - 0.08 <= ts < cl[1] + 0.4 else 0)
    cabin(cv, sh, u, view=view17)
    with stage(cv, *sh):
        open_box(cv, 300, 1392, 0.8)
        if not in_room: people(cv, ts, {'L': pl}, {'L': L_}, order=('L',))
        people(cv, ts, {'U': pu}, {'U': U_}, order=('U',))
    lbutton_lit(cv, sh)
    if ts < cl[1]: alarm(cv, k, 1.0 if ts < cl[1] - 10 else 1.5)
    dim(cv, 0.16 if ts < cl[1] else 0.4)
    display(cv, sh, '17', red=True)


# ============ SAHNE 12: Luna tek basina; asansor asagi hareket eder ============
def scene12(cv, t):
    ts, k = step(t), kk(t)
    sb, dn = B('shut'), B('down'); mv = dn[0] + MOVE
    sh = jit(k, 4 if mv <= ts < mv + 0.9 else 0)
    cabin(cv, sh, 0.0)
    if ts < sb[0] + 0.7: U_ = ('uzgun', DOORP, 0, dict(back=True))
    elif ts < dn[0]: U_ = ('uzgun', HOLDB, 0, dict(down=True))
    else: U_ = ('saskin' if ts >= mv else 'uzgun', dict(HOLDB, **LOOKUP) if ts >= mv else HOLDB, 0)
    with stage(cv, *sh):
        open_box(cv, 300, 1392, 0.8)
        people(cv, ts, {'U': UC}, {'U': U_}, order=('U',))
    lbutton_lit(cv, sh)
    dim(cv, lerp(0.4, 0.22, seg(ts, sb[0], sb[0] + 0.8)))
    display(cv, sh, '16' if ts >= mv + 0.5 else '17', red=ts < mv)


# ============ SAHNE 13: asansor boslugu (kesit): her katta kalanlardan biri geri doner ============
FH, CABF = 560, 1050                                       # kat yuksekligi, kabinin zemini (ekranda sabit)
SHAFT = (300, 780)
INCAB = {'U': (392, 0.27), 'M': (470, 0.31), 'Z': (550, 0.31), 'S': (630, 0.31), 'K': (708, 0.31)}
def floor_band(cv, n, y, k):
    """n. kat: y zemin cizgisi. Iki yanda o katin odasi"""
    x0, x1 = -520, 1620; top = y - FH + 26
    theme = {17: ROOMW1, 16: (34, 58, 66), 15: (40, 52, 76), 14: (46, 44, 40), 13: (58, 80, 86)}.get(n, (120, 104, 84))
    for a_, b_ in ((x0, SHAFT[0]), (SHAFT[1], x1)):
        cv.drawRect(LTRB(a_, top, b_, y), fill(theme))
        cv.drawLine(a_, y - 150, b_, y - 150, dashed(shade(theme, 1.5), 3, 130, (14, 10)))
        cv.drawRect(LTRB(a_, y, b_, y + 26), fill((16, 18, 28)))
    for sd, ex in ((-1, SHAFT[0]), (1, SHAFT[1])):           # kat kapisi (bosluga acilan)
        cv.drawRect(LTRB(ex - 26 if sd < 0 else ex, y - 330, ex if sd < 0 else ex + 26, y), fill((150, 162, 178)))
    cv.drawRRect(RRXY(LTRB(170, y - 446, 262, y - 366), 10, 10), fill((16, 18, 28)))
    text(cv, str(n) if n > 0 else 'L', 216, y - 388, 48, RED if n >= 13 else AMB)
    cv.drawRRect(RRXY(LTRB(818, y - 446, 910, y - 366), 10, 10), fill((16, 18, 28)))
    text(cv, str(n) if n > 0 else 'L', 864, y - 388, 48, RED if n >= 13 else AMB)
    if n == 17:                                              # gorevli odasi: Leo geride kalir
        chair(cv, 60, y, 0.5)
        f = figure(cv, 190 if FMT == 'v' else 130, y, 0.27, TEAL, 'sakin', alt(k, WAVE_A, WAVE_B, 3), 5, look=1.0)
        cap_on(cv, f['head'][0], f['head'][1], f['HR'])
        for i in range(3): mini_pkg(cv, 900 + i * 70, y - 190, 0.3)
    elif n == 16:                                            # uc kapi
        for i, c in enumerate(((206, 190, 150), (233, 180, 70), (204, 54, 58))):
            for bx in (-380 + i * 190, 880 + i * 150): cv.drawRect(LTRB(bx, y - 250, bx + 96, y), fill(c))
    elif n == 15:                                            # aynalar
        for bx in (-360, -170, 30, 890, 1010, 1210, 1400):
            cv.drawRect(LTRB(bx, y - 330, bx + 110, y - 30), fill((150, 190, 214))); cv.drawLine(bx + 16, y - 80, bx + 90, y - 300, stroke((230, 244, 250), 5, 170))
    elif n == 14:                                            # arsiv raflari
        for bx in (-400, -200, 0, 880, 1080, 1280):
            for j in range(3):
                cv.drawLine(bx, y - 90 - j * 90, bx + 150, y - 90 - j * 90, stroke((24, 22, 20), 8, cap=False))
                for i in range(4): cv.drawRect(LTRB(bx + 10 + i * 34, y - 132 - j * 90, bx + 36 + i * 34, y - 94 - j * 90), fill((214, 200, 170)))
    elif n == 13:                                            # koridor: kirmizi kapi
        for bx in (-300, 1040): cv.drawRect(LTRB(bx, y - 290, bx + 130, y), fill((204, 54, 58))); cv.drawCircle(bx + 104, y - 140, 9, fill(YEL))
    else:                                                    # siradan katlar: isikli pencere, kapi
        for bx in (-330, -100, 940, 1180):
            cv.drawRRect(RRXY(LTRB(bx, y - 330, bx + 120, y - 170), 10, 10), fill((250, 214, 120)))
            cv.drawLine(bx + 60, y - 330, bx + 60, y - 170, stroke(shade(theme, 0.8), 6, cap=False))


def scene13(cv, t):
    ts, k = step(t), kk(t)
    a, b = TL.span(13); uu = seg(ts, a, b)
    d = FALL_N * FH * uu ** FALL_EASE
    cv.clear(col((8, 10, 18)))
    sh = jit(k, 2)
    appear = {w: a + (b - a) * fall_u(n_) + (0.25 if w == 'M' else 0.0) for w, n_ in RETURNS}
    with stage(cv, *sh):
        for n in range(17, 9, -1):
            y = CABF + (17 - n) * FH - d
            if -200 < y < 2600: floor_band(cv, n, y, k)
        cv.drawRect(LTRB(SHAFT[0], -400, SHAFT[1], 2600), fill((10, 12, 22)))
        for xx in (SHAFT[0] + 10, SHAFT[1] - 10): cv.drawLine(xx, -400, xx, 2600, dashed((70, 80, 104), 4, 200, (22, 14), ))
        for i in range(-2, 12):                              # akip giden kat cizgileri (hiz hissi)
            yy = (i * 280 - d * 1.0) % 2800 - 300; cv.drawLine(SHAFT[0] + 24, yy, SHAFT[0] + 70, yy, stroke((40, 46, 66), 5, cap=False)); cv.drawLine(SHAFT[1] - 70, yy, SHAFT[1] - 24, yy, stroke((40, 46, 66), 5, cap=False))
        for xx in (516, 564): cv.drawLine(xx, -400, xx, CABF - 388, stroke((90, 96, 112), 5, cap=False))
        for w, n_ in RETURNS:                                # donus: o kattan kabine vuran isik
            fa = seg(ts, appear[w] - 0.12, appear[w]) * (1 - seg(ts, appear[w], appear[w] + 0.5))
            if fa > 0 and w != 'M': poly(cv, [(-520, CABF - 330), (334, CABF - 330), (334, CABF), (-520, CABF)], (255, 250, 230), 150 * fa)
        gl = fill((250, 228, 156), 80); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 46)); cv.drawRect(LTRB(300, CABF - 410, 780, CABF + 30), gl)
        cv.drawRRect(RRXY(LTRB(316, CABF - 392, 764, CABF + 22), 10, 10), fill((56, 64, 80)))
        cv.drawRect(LTRB(334, CABF - 370, 746, CABF), fill(shade(WALL, 1.2)))
        cv.drawRRect(RRXY(LTRB(430, CABF - 358, 650, CABF - 332), 13, 13), fill((252, 240, 200)))
        cv.drawRRect(RRXY(LTRB(350, CABF - 310, 730, CABF - 16), 8, 8), dashed(shade(WALL, 1.6), 3, 190))
        cv.drawLine(340, CABF - 120, 740, CABF - 120, stroke((58, 68, 82), 9, cap=False))
        cv.save(); cv.clipRect(LTRB(334, CABF - 370, 746, CABF + 6))
        mom_in = ts >= appear['M']
        for w in ('K', 'S', 'Z', 'M', 'U'):
            x, s = INCAB[w]
            if w == 'U':
                actor(cv, ts, 'U', 'heyecan' if mom_in else 'saskin', UP if mom_in and ts < appear['M'] + 0.8 else {}, -2.0 if mom_in else 1.5, place=(x, CABF - 4, s), talk=None)
                continue
            if ts < appear[w] - 0.02: continue
            p = seg(ts, appear[w], appear[w] + 0.3)
            actor(cv, ts, w, 'saskin' if ts < appear[w] + 1.0 else 'sakin', {}, 1.5 if w == 'M' else -1.0, place=(x, CABF - 4, s * lerp(0.7, 1.0, smooth(p))), alpha=p, talk=None)
            if p < 1: cv.drawCircle(x, CABF - 170 * s / 0.31, lerp(30, 150, p), stroke((255, 250, 230), 7, 255 * (1 - p)))
        cv.restore()
        cv.drawLine(334, CABF + 3, 746, CABF + 3, stroke((80, 68, 96), 8, cap=False))
    dim(cv, 0.1)


# ============ SAHNE 14: lobi; bes kisi iner ============
LIN_ = {'K': (345, FLOOR - 4, 0.42), 'Z': (462, FLOOR - 4, 0.42), 'S': (738, FLOOR - 4, 0.42), 'M': (566, FLOOR + 2, 0.46), 'U': (652, FLOOR + 2, 0.36)}
LOUT = {'K': (196, GY - 40, 0.60), 'Z': (372, GY - 46, 0.58), 'S': (884, GY - 40, 0.60), 'M': (566, GY - 16, 0.64), 'U': (742, GY - 16, 0.50)}
def scene14(cv, t):
    ts, k = step(t), kk(t)
    lb = B('lobby'); o = ts - lb[0]
    u = smooth(seg(o, LOBBY_DING + 0.3, LOBBY_DING + 1.2))
    num = ('3', '2', '1')[min(2, int(o / 0.3))] if o < 0.9 else 'L'
    out = smooth(seg(ts, S('m1') - 0.1, E('m1') + 0.4))
    hug = smooth(seg(ts, E('m1') - 0.4, E('m1') + 0.5))
    P = {w: lerp3(LIN_[w], LOUT[w], out) for w in LIN_}
    P['U'] = lerp3(P['U'], (LOUT['M'][0] + 118, LOUT['U'][1], LOUT['U'][2]), hug * (1 - 0.0))
    wk = 0 < out < 1
    n5 = ts >= S('n5') - 0.1
    def pose(w, base):
        return dict(walk(out * 260, P[w][2], -1 if LOUT[w][0] < 540 else 1, off=0.13 * 'KZSMU'.index(w)), **{k_: v_ for k_, v_ in base.items() if k_ in ('aL', 'aR')}) if wk else base
    st = {}
    st['K'] = ('saskin' if not n5 else 'merak', pose('K', TIEP if n5 else {}), 0 if not wk else -1, )
    st['Z'] = ('saskin' if ts < E('m1') else 'mutlu', pose('Z', GLP if n5 and ts < frac('n5', 0.5) else {}), 0.6)
    st['S'] = ('saskin' if ts < S('m1') else 'mutlu', pose('S', CALM if on(ts, 'u11') else {}), -0.8)
    if ts < S('m1') - 0.1: st['M'] = ('saskin', {}, 1.6); st['U'] = ('heyecan' if ts >= S('u10') - 0.15 else 'saskin', UP if ts >= S('u10') - 0.15 else {}, -2.0)
    elif hug < 0.5: st['M'] = ('aglama', pose('M', dict(aL=(-110, 60, -150, -30), aR=(110, 60, 150, -30))), 1.6); st['U'] = ('heyecan', pose('U', UP), -2.0)
    else: st['M'] = ('mutlu' if ts >= S('u11') else 'aglama', HUG, 1.8); st['U'] = ('mutlu', dict(CALM, lean=-10) if on(ts, 'u11') and ts > frac('u11', 0.5) else dict(aL=(-110, 90, -170, 120), aR=(60, 130, 20, 200), lean=-12), -2.0 if not (on(ts, 'u11') and ts > frac('u11', 0.5)) else 0)
    order = sorted(P, key=lambda w: P[w][1])
    def draw(c):
        for w in order: actor(c, ts, w, st[w][0], st[w][1], st[w][2], place=P[w])
    inside_now = u < 1 or out <= 0
    lobby(cv, u, inside=draw if inside_now else None, glow=0.85 * (1 - seg(o, LOBBY_DING + 0.5, LOBBY_DING + 1.5)))
    if not inside_now:
        with stage(cv): draw(cv)
    display(cv, (0, 0), num)
    dim(cv, 0.06)


# ============ SAHNE 15: 13. kat; hardal sapkali biri ============
def scene15(cv, t):
    ts, k = step(t), kk(t)
    a, _ = TL.span(15)
    gx = 470 + 150.0 * max(0.0, ts - a - 0.3)
    cam = gx - (430 if FMT == 'v' else 330)
    fl = alt(k, 1.0, 0.4, 1) if (ts - a) % 3.3 < 0.4 else 1.0
    side_corridor(cv, cam, 6000, lamp=fl, k=k)
    with stage(cv):
        x, s = gx - cam, 0.74
        P = dict(walk(gx - 470, s, 1, hold=True, off=0.2) if ts > a + 0.3 else {}, **HOLD)
        sinema.contact_shadow(cv, x, NEAR, s)
        look = 0.0 if ts >= frac('n6', 0.72) else 1.0        # sonunda bize bakar
        f = figure(cv, x, NEAR, s, (38, 36, 56), None, P, 5, look=look)
        hx, hy = f['head']
        for sd in (-1, 1): cv.drawOval(LTRB(hx + sd * 36 * s + look * 6 * s - 13 * s, hy - 16 * s, hx + sd * 36 * s + look * 6 * s + 13 * s, hy + 2 * s), fill((240, 232, 200), 235))
        cap_on(cv, hx, hy, f['HR'], look=1.0 if look else 1.0)
        package(cv, f, s)
    dim(cv, 0.3)


# ============ SAHNE 16: kapanis karti ============
def scene16(cv, t):
    ts, k = step(t), kk(t)
    a0, _ = TL.span(16)
    lobby(cv, 0.0); display(cv, (0, 0), 'L'); dim(cv, 0.86)
    cx, cy, sc_ = (W / 2, 850, 0.55) if FMT == 'v' else (W / 2, 505, 0.48)
    a = smooth(seg(ts, a0 + 0.4, a0 + 1.0))
    gl = fill((255, 226, 150), (80 + 26 * alt(k, 0, 1, 5)) * a); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 70 * sc_)); cv.drawCircle(cx, cy, 380 * sc_, gl)
    if a > 0: idcard(cv, cx, cy + 40 * (1 - a), sc_, a)                                                # Leo'nun yaka karti: GOREVLI
    c_ = seg(t, a0 + 0.3, a0 + 0.8)
    card(cv, [('13. Kat bitti', 74 if FMT == 'v' else 80, (255, 110, 96)), ('Yeni dizi çok yakında', 48, CREAM), ('Abone ol, ilk bölümü kaçırma', 34, (176, 190, 232))], c_, cy=470 if FMT == 'v' else 176)
    abone(cv, t, a0 + ABONE_END, pos=(W / 2, 1500) if FMT == 'v' else (W / 2, 800))


SINE = {1: dict(cam='genis'), 4: dict(mood='soguk'), 5: dict(cam='genis'), 6: dict(cam='genis'), 8: dict(cam='genis'),
        10: dict(cam='genis'), 11: dict(zmax=1.24), 13: dict(cam='genis', mood='gece'), 14: dict(cam='genis', mood='sicak'), 15: dict(mood='soguk')}

if __name__ == '__main__':
    run({1: scene1, 2: scene2, 3: scene3, 4: scene4, 5: scene5, 6: scene6, 7: scene7, 8: scene8, 9: scene9, 10: scene10,
         11: scene11, 12: scene12, 13: scene13, 14: scene14, 15: scene15, 16: scene16},
        white=((2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12)), sine=SINE, hud=hud)
