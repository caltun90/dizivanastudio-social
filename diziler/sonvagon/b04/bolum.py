"""Son Vagon, 4. Bolum: Konduktor. Yalnizca sahneler; ortak parcalar ../ortak.py icinde.
Yapi: MEKTUP BICIMINDE. Ada'nin orgusunun icinden cikan notu Ada'nin sesi okur: ekranda nakis kasnagi icinde Ada (konusur) ve
el yazili kagit; goruntude Mia iki numaradan bir numaraya gecer, Sarnic'ta iki numara (bos) birakilir, arka kapidan Konduktor girer.
Kanca (arka kapi: ardinda vagon yok, camda fener ve karalti) -> disaridan: iki vagon -> orgu hisirdar, not ve kalem -> baslik ->
mektup (kagit) -> arkaya bakis: bos ray; one bakis -> anons ve levha -> koruk; orgudeki uc istasyon adi -> bir numara; kilitli lokomotif kapisi ->
Sarnic peronu (sarnic kuyusu) -> arka kapi: iki numara soner -> rayda fener -> kapi acilir: Konduktor -> "Herkes indi" (carpilar onaya doner) ->
halkada uc zimbali bilet -> uc istasyonda birakilan uc vagon (sepya) -> zimba bos bileti delmez -> duraklar seridi: Son Durak'tan sonrasi karanlik ->
mektubun sonu: kalem bos satirin ustunde -> kapanis.
Yeni mekanlar: bir numara (lokomotif kapisi yandan), Sarnic peronu, istasyonda kalan vagon (disaridan).
Yeni gorsel fikirler: kasnakta konusan Ada ve el yazisi, rayda yaklasan fener, bilet halkasi ve zimba, duraklar seridi, kalem."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import *
import ortak
from senaryo import ABONE, ABONE_END, FEEL, FIND, LOCKS, BRAKE, HALT, OUT_OFF, GONE, OPEN, RING_AT, PUNCH

V = FMT == 'v'
QW = (540, 1060) if V else (540, 1000)                     # genis vagon planlarinda sahnenin oturdugu yer
QC = (540, 1000) if V else (540, 1010)                     # yakin planlarda
STN = 'SARNIÇ'
RED, GREEN, INK = (255, 110, 96), (96, 200, 130), (44, 50, 110)
WOOD = (190, 132, 78)
KS_ = sorted(TL.scenes)
END0 = TL.span(31)[0]
HK = TL.span(2)[0]                                         # kancadan disari plana kesme ani
BIG = LTRB(-3000, -3000, 5000, 5000)

# ---------- pozlar ----------
SHOWB = dict(aR=(150, 70, 196, -40))                        # elindekini yuzunun yaninda gosterir (buyuk kafa)
FWD = dict(aR=(110, 70, 214, 50))                           # sag elini ileri (saga) uzatir
BACKP = dict(aL=(-120, 40, -206, -16))                      # solu (arkayi) gosterir
READ = dict(aL=(-70, 90, -34, 150), aR=(70, 90, 34, 150))   # iki eliyle kagidi gogsunun onunde tutar
DIG = dict(aL=(-84, 110, -40, 180), aR=(60, 130, 0, 196))   # sag eli orgunun icinde
SALUTE = dict(aR=(150, -40, 104, -236))                     # eli kasketin siperliginde
LANTUP = dict(aL=(-130, 50, -210, 0))                       # feneri sola (kapiya) kaldirir
GIVEL = dict(aL=(-110, 80, -204, 56))                       # sol eliyle sola uzatir
OPENR = dict(aR=(120, 90, 200, 120))                        # sag eli acik, anlatir
CHEST = dict(aL=(-70, 110, -12, 160), aR=(70, 110, 12, 160))


# ---------- trenin aldigi yol ----------
SPEED = {1: 160, 12: 260, 13: 0, 14: 0, 15: 160}
def _speed(t):
    k = KS_[0]
    for s_ in KS_:
        if t >= TL.scenes[s_] - 1e-6: k = s_
    return SPEED.get(k, 420)
_T = np.arange(0, TL.total + 3, 1 / 24.0); _D = np.concatenate([[0], np.cumsum(np.array([_speed(x) for x in _T[:-1]]) / 24.0)])
def SC(t): return float(np.interp(t, _T, _D))


def otext(cv, s, x, y, size, c=(255, 255, 255), a=1.0, tf=None, bold=True, align='c'):
    f = skia.Font(tf or TFB, size); f.setEmbolden(bold); w = f.measureText(s)
    x0 = x - w / 2 if align == 'c' else (x - w if align == 'r' else x)
    st = stroke((0, 0, 0), size * 0.2, 255 * a); st.setStrokeJoin(skia.Paint.kRound_Join)
    cv.drawString(s, x0 + 3, y + 6, f, fill((0, 0, 0), 110 * a)); cv.drawString(s, x0, y, f, st); cv.drawString(s, x0, y, f, fill(c, 255 * a)); return w


def yarn_strand(cv, pts, w=6):
    p = skia.Path(); p.moveTo(*pts[0])
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]; p.quadTo((x0 + x1) / 2, (y0 + y1) / 2 + (9 if i % 2 else -9), x1, y1)
    cv.drawPath(p, stroke(shade(CORAL, 0.7), w + 3)); cv.drawPath(p, stroke(CORAL, w)); cv.drawPath(p, dashed(shade(CORAL, 1.35), 2, 200, (8, 7)))


def title_card(cv, t):
    tb = B('title'); a = seg(t, tb[0], tb[0] + 0.35)
    if a > 0:
        dim(cv, 0.5 * a)
        card(cv, [(TITLE, 112, RED), (f'{EP.title()}: {EP_NAME}', 48, CREAM)], a, lerp(0.9, 1.0, smooth(seg(t, tb[0], tb[0] + 0.5))))


def check(cv, x, y, r, c=GREEN, a=1.0):
    p = skia.Path(); p.moveTo(x - r * 0.7, y); p.lineTo(x - r * 0.15, y + r * 0.55); p.lineTo(x + r * 0.8, y - r * 0.6)
    st = stroke((0, 0, 0), r * 0.62, 230 * a); st.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, st)
    st = stroke(c, r * 0.36, 255 * a); st.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, st)


def cross(cv, x, y, r, a=1.0):
    for sd in (-1, 1):
        cv.drawLine(x - r, y - sd * r, x + r, y + sd * r, stroke((0, 0, 0), r * 0.5, 230 * a)); cv.drawLine(x - r, y - sd * r, x + r, y + sd * r, stroke(RED, r * 0.3, 255 * a))


# ---------- Mia'nin elindekiler ----------
def knit_piece(cv, x, y, s, a=1.0):
    """elden sarkan yarim orgu (kucuk)"""
    A = 255 * a
    poly(cv, [(x - 36 * s, y), (x + 36 * s, y - 5 * s), (x + 32 * s, y + 88 * s), (x - 32 * s, y + 92 * s)], CREAM, A)
    for j in range(1, 4): cv.drawLine(x - 29 * s, y + j * 23 * s, x + 29 * s, y - 4 * s + j * 23 * s, dashed(CORAL, 4 * s, 225 * a, (8 * s, 6 * s)))
    cv.drawLine(x - 56 * s, y + 3 * s, x + 58 * s, y - 11 * s, stroke((70, 64, 84), 8 * s, A)); cv.drawLine(x - 56 * s, y + 3 * s, x + 58 * s, y - 11 * s, stroke((150, 142, 166), 5 * s, A))


def paper(cv, x, y, s, a=1.0, rot=-8, w=70, h=92):
    """kucuk not kagidi"""
    cv.save(); cv.translate(x, y); cv.rotate(rot); rc = LTRB(-w / 2 * s, -h / 2 * s, w / 2 * s, h / 2 * s)
    cv.drawRRect(RRXY(rc.makeOffset(3, 4), 4, 4), fill((4, 6, 20), 80 * a)); cv.drawRRect(RRXY(rc, 4, 4), fill((252, 246, 228), 255 * a))
    for yy in (-26, -12, 2, 16): cv.drawLine((-w / 2 + 9) * s, yy * s, (w / 2 - 9) * s, yy * s, stroke(INK, 2.6 * s, 190 * a, cap=False))
    cv.restore()


def pencil(cv, x, y, L, rot, th=26, a=1.0):
    """kursun kalem; (x, y): ucu (yazan uc). Govde uctan itibaren rot acisina dogru uzanir"""
    A = 255 * a
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    cv.drawRect(LTRB(th * 1.5 + 4, -th / 2 + 6, L + 4, th / 2 + 6), fill((4, 6, 20), 80 * a))
    cv.drawRect(LTRB(th * 1.5, -th / 2, L, th / 2), fill(CORAL, A)); cv.drawRect(LTRB(th * 1.5, -th / 6, L, th / 6), fill(shade(CORAL, 1.25), A))
    cv.drawRect(LTRB(L - th * 0.9, -th / 2, L, th / 2), fill((170, 176, 196), A)); cv.drawRect(LTRB(L, -th / 2, L + th * 0.7, th / 2), fill((236, 150, 160), A))
    poly(cv, [(0, 0), (th * 1.5, -th / 2), (th * 1.5, th / 2)], (226, 190, 140), A); poly(cv, [(0, 0), (th * 0.5, -th / 6), (th * 0.5, th / 6)], (44, 44, 56), A)
    cv.restore()


def prop_found(cv, f, s, a):
    """sol elde orgu, sag elde (yuzun yaninda) rulo not; ucundan kalem gorunur"""
    u = s / 0.7; knit_piece(cv, f['handL'][0], f['handL'][1] + 12 * s, u, a)
    hx, hy = f['handR']
    pencil(cv, hx - 10 * u, hy - 78 * u, 70 * u, 80, th=13 * u, a=a)
    cv.save(); cv.translate(hx, hy - 6 * u); cv.rotate(-10)
    rc = LTRB(-19 * u, -52 * u, 19 * u, 40 * u); cv.drawRRect(RRXY(rc, 16 * u, 16 * u), fill((252, 246, 228), 255 * a)); cv.drawRRect(RRXY(rc, 16 * u, 16 * u), stroke(shade(CREAM, 0.7), 2.5 * u, 255 * a))
    cv.drawLine(-19 * u, -4 * u, 19 * u, -4 * u, stroke(CORAL, 4 * u, 255 * a)); cv.restore()
    hand_ball(cv, hx, hy, 33 * s, MUSTARD, seed=4)
def prop_carry(cv, f, s, a): u = s / 0.7; knit_piece(cv, f['handL'][0], f['handL'][1] + 12 * s, u, a); paper(cv, f['handL'][0] - 6 * s, f['handL'][1] - 34 * s, u, a, rot=-14)
def prop_read(cv, f, s, a):
    u = s / 0.7; mx, my = (f['handL'][0] + f['handR'][0]) / 2, (f['handL'][1] + f['handR'][1]) / 2
    paper(cv, mx, my - 22 * s, u * 1.5, a, rot=-3)
    for h in (f['handL'], f['handR']): hand_ball(cv, h[0], h[1], 33 * s, MUSTARD, seed=4)
def prop_tk(cv, f, s, a): prop_carry(cv, f, s, a); mini_ticket(cv, f['handR'][0] + 8 * s, f['handR'][1] - 30 * s, s / 0.7 * 1.2, a, c=MUSTARD)
def prop_givet(cv, f, s, a): mini_ticket(cv, f['handL'][0] - 10 * s, f['handL'][1] - 26 * s, s / 0.7 * 1.2, a, rot=8, c=MUSTARD)
def prop_pen(cv, f, s, a):
    u = s / 0.7; prop_carry(cv, f, s, a); hx, hy = f['handR']
    mini_ticket(cv, f['handL'][0] + 60 * s, f['handL'][1] - 70 * s, u * 1.3, a, rot=6, c=MUSTARD)
    pencil(cv, hx - 30 * u, hy + 44 * u, 100 * u, -62, th=14 * u, a=a); hand_ball(cv, hx, hy, 33 * s, MUSTARD, seed=4)
ortak.PROPS.update(found=prop_found, carry=prop_carry, read=prop_read, tk=prop_tk, givet=prop_givet, pen=prop_pen)


# ---------- portre: nakis kasnagi (Ada'nin mektup sesi) ya da pirinc pencere ----------
def portrait(cv, ts, who, cx, cy, r, a=1.0, expr='sakin', ring='hoop', prop=None, look=0.0, label=None):
    if a <= 0.01: return
    cv.saveLayerAlpha(BIG, int(255 * clamp(a)))
    sh = fill((4, 6, 20), 130); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14)); cv.drawCircle(cx + 6, cy + 12, r * 1.08, sh)
    cv.drawCircle(cx, cy, r, fill(CREAM if ring == 'hoop' else (250, 214, 130)))
    cv.save(); cp = skia.Path(); cp.addCircle(cx, cy, r); cv.clipPath(cp, True)
    if ring == 'hoop':
        for j in range(-7, 8): cv.drawLine(cx - r, cy + j * r / 7, cx + r, cy + j * r / 7, dashed(shade(CREAM, 0.84), max(1.5, r * 0.012), 130, (8, 7)))
    else:
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeRadial(skia.Point(cx, cy - r * 0.2), r * 1.3, [col((255, 232, 170)), col((214, 150, 96))])); cv.drawCircle(cx, cy, r, g)
    c_ = CAST[who]; s = r / 318.0; HR = 118 * s * c_.get('head', 1.0); gy = cy - r * 0.02 + HR * 0.88 + 520 * s
    actor(cv, ts, who, expr, dict(KNIT) if prop == 'knit' else {}, look, place=(cx, gy, s), prop=prop)
    cv.restore()
    if ring == 'hoop':
        cv.drawCircle(cx, cy, r, stroke(shade(WOOD, 0.7), r * 0.13)); cv.drawCircle(cx, cy, r, stroke(WOOD, r * 0.09)); cv.drawCircle(cx, cy, r, dashed(shade(WOOD, 1.3), max(1.5, r * 0.014), 170, (10, 8)))
        cv.drawRRect(RRXY(LTRB(cx - r * 0.1, cy - r * 1.2, cx + r * 0.1, cy - r * 1.02), 4, 4), fill(BRASS)); cv.drawCircle(cx, cy - r * 1.22, r * 0.07, fill(shade(BRASS, 0.7)))
    else:
        cv.drawCircle(cx, cy, r, stroke(shade(BRASS, 0.6), r * 0.12)); cv.drawCircle(cx, cy, r, stroke(BRASS, r * 0.075))
    if label:
        fs = r * 0.22; f = skia.Font(TFB, fs); w = f.measureText(label); y0 = cy + r * 1.14
        rc = LTRB(cx - w / 2 - fs * 0.7, y0, cx + w / 2 + fs * 0.7, y0 + fs * 1.7)
        if ring == 'hoop':
            cv.drawRRect(RRXY(rc, fs * 0.85, fs * 0.85), fill(ROSE)); cv.drawString(label, cx - w / 2, y0 + fs * 1.2, f, fill(INKBLUE))
        else:
            cv.drawRRect(RRXY(rc, fs * 0.3, fs * 0.3), fill(PAPER)); cv.drawRRect(RRXY(rc.makeInset(4, 4), fs * 0.2, fs * 0.2), dashed((150, 40, 46), 2, 220, (8, 6)))
            cv.drawString(label, cx - w / 2, y0 + fs * 1.2, f, fill((150, 40, 46)))
    cv.restore()


CAMEO = ('d2', 'd3', 'd4', 'd7')                             # Ada'nin sesi aksiyonun ustunde: kosede kasnak
def cameo(cv, t):
    ts = step(t)
    a = max(min(seg(t, S(i) - 0.3, S(i) - 0.05), 1 - seg(t, E(i) + 0.25, E(i) + 0.5)) for i in CAMEO)
    a = min(a, max(1 - seg(t, frac('d3', 0.27) - 0.25, frac('d3', 0.27)), seg(t, frac('d3', 0.66), frac('d3', 0.66) + 0.25)))   # orgu planinda kasnak cekilir
    for lid, off in ABONE: a = min(a, max(1 - seg(t, S(lid) + off - 0.2, S(lid) + off), seg(t, S(lid) + off + 4.6, S(lid) + off + 4.9)))
    if V: portrait(cv, ts, 'D', 172, 470, 128, a, prop='knit', label='ADA\'NIN MEKTUBU')
    else: portrait(cv, ts, 'D', 1740, 190, 124, a, prop='knit', label='ADA\'NIN MEKTUBU')


def hud(cv, t, k):
    if t < HK: hook_text(cv, t, 'ARKADA VAGON YOK', 1 - seg(t, HK - 0.12, HK))
    tb = B('title')
    if not (tb[0] <= t < tb[1]): cameo(cv, t)
    if k == 23: memory_frame(cv, "ADA'NIN MEKTUBU", a=0.9)
    if k == 31: abone(cv, t, END0 + ABONE_END, pos=(W / 2, 1500) if V else (W / 2, 800))


# ---------- mektup plani: el yazili kagit + buyuk kasnak ----------
def letter_plan(cv, ts, k, lines, lid, bgf):
    """lines: kagitta okunacak satirlar; lid: okunan replik (yazi sesle birlikte belirir). bgf(): arka plan"""
    bgf(); dim(cv, 0.66)
    rc = LTRB(120, 420, 960, 1090) if V else LTRB(170, 280, 1090, 872)
    fs = 66 if V else 62; lh = fs * 1.75
    cv.save(); cv.translate(rc.centerX(), rc.centerY()); cv.rotate(-2.2 + 0.4 * math.sin(k * 0.12)); cv.translate(-rc.centerX(), -rc.centerY())
    sh = fill((4, 6, 20), 150); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18)); cv.drawRRect(RRXY(rc.makeOffset(10, 18), 12, 12), sh)
    cv.drawRRect(RRXY(rc, 12, 12), fill((252, 246, 228)))
    for j in range(1, 3): cv.drawLine(rc.left(), rc.top() + rc.height() * j / 3, rc.right(), rc.top() + rc.height() * j / 3, stroke(shade(CREAM, 0.86), 3, 150, cap=False))   # kat izleri
    cv.drawCircle(rc.right() - 70, rc.top() + 64, 20, fill(CORAL)); cv.drawCircle(rc.right() - 70, rc.top() + 64, 11, dashed(shade(CORAL, 1.4), 2, 200, (5, 4)))   # yun dugme: Ada'nin imi
    x0 = rc.left() + 64; y = rc.top() + 150
    tot = sum(len(s_) for s_ in lines); acc = 0; u = seg(ts, S(lid) - 0.05, E(lid) - 0.1)
    f = skia.Font(TFM, fs); f.setSkewX(-0.22)
    for s_ in lines:
        cv.drawLine(x0 - 10, y + fs * 0.34, rc.right() - 54, y + fs * 0.34, stroke((176, 190, 232), 2.5, 200, cap=False))
        lu = clamp((u * tot - acc) / len(s_)); acc += len(s_)
        if lu > 0:
            w = f.measureText(s_); cv.save(); cv.clipRect(LTRB(x0 - 20, y - fs * 1.2, x0 + w * lu + 6, y + fs * 0.6))
            cv.drawString(s_, x0, y, f, fill(INK)); cv.restore()
            if lu < 1: pencil(cv, x0 + w * lu + 4, y + 4, 150, -58, th=20)
        y += lh
    while y < rc.bottom() - 50:                              # mektubun henuz okunmamis satirlari
        cv.drawLine(x0 - 10, y + fs * 0.34, rc.right() - 54, y + fs * 0.34, stroke((176, 190, 232), 2.5, 200, cap=False))
        p = skia.Path(); p.moveTo(x0, y)
        for q_ in range(int((rc.width() - 180 - (140 if y + lh >= rc.bottom() - 50 else 0)) / 26)): p.rQuadTo(6.5, -16 * (1 if q_ % 2 else -0.6), 13, 0); p.rQuadTo(6.5, 10, 13, 0)
        cv.drawPath(p, stroke(INK, 4, 60)); y += lh
    cv.restore()
    if V: portrait(cv, ts, 'D', 540, 1476, 160, prop='knit', label="ADA'NIN MEKTUBU")
    else: portrait(cv, ts, 'D', 1480, 500, 226, prop='knit', label="ADA'NIN MEKTUBU")


# ---------- iki numara (CAMA) ve bir numara (CAMB on, CAMR arka) ----------
CAMA, XM = 1560, 1990
CAMB, XMB = 1560, 2080
CAMR, XMR, XCR = -120, 740, 300
def w2(cv, ts, k, st, extra=None, **kw):
    wagon(cv, CAMA, 2, k, scroll=SC(ts), last=True, **kw)
    with stage(cv):
        f = people(cv, ts, {w: v[0] for w, v in st.items()}, {w: v[1] for w, v in st.items()})
        if extra: extra(f)
    return f
def w1(cv, ts, k, cam, st, extra=None, last=True, **kw):
    wagon(cv, cam, 1, k, scroll=SC(ts), last=last, **kw)
    with stage(cv):
        loco_door(cv, cam, k)
        f = people(cv, ts, {w: v[0] for w, v in st.items()}, {w: v[1] for w, v in st.items()})
        if extra: extra(f)
    return f
MIA2 = (XM - CAMA, NEAR, 0.70)
MIAR, CONR = (XMR - CAMR, NEAR, 0.70), (XCR - CAMR, NEAR, 0.74)
def zM(z=1.5): return (z if V else z + 0.05, (MIAR[0], 950), QC)        # Mia'ya yakin (bir numara, arka)
def zC(z=1.5): return (z if V else z + 0.05, (CONR[0] + 10, 930), QC)   # Konduktor'e yakin
def z2(z=1.2): return (z if V else z + 0.05, ((MIAR[0] + CONR[0]) / 2, 960), (540, 1010))   # ikisi


# ---------- bir numaranin arka kapisi (karsidan): ardinda iki numara, sonra bos ray, sonra fener ----------
GLS = LTRB(D0 + 56, DT + 50, D1 - 56, 1010)
ZG = 2.2 if V else 2.0
PG, QG = (540, 850), ((540, 900) if V else (540, 960))
def back_door(cv, ts, k, z=1.0, p=(540, 1000), q=(540, 1000), lamp=1.0, gone=False, fog_a=0.0, sc=0.0, lant=0.0, sil=0.0, open_u=0.0,
              mia=None, cond=None, shake=(0, 0), hi=0.0):
    """z, p, q: yakinlasma. lamp 0..1: iki numaranin isigi. gone: vagon yok (bos ray). lant 0..1: rayda yaklasan fener. sil 0..1: camdaki karalti.
    open_u 0..1: kapi saga kayar. mia: (x, ifade, poz, bakis) arkadan. cond: (ifade, poz, bakis, ek) kapi araliginda Konduktor"""
    def glass(c, g_, k_):
        if gone: rear_view(c, g_, 1.0, 0.0, sc, k_)
        else: fwd_glass(c, g_, k_)
    with zoom(cv, z, p, q): door_view(cv, k, plate_hi=hi, plate_on=0.0 if gone else 1.0, no=2, glass=glass, shake=shake, open_u=open_u)
    Z = lambda x, y: (q[0] + z * (x - p[0]) + shake[0], q[1] + z * (y - p[1]) + shake[1])
    with stage(cv):
        if open_u <= 0:
            l_, t_ = Z(GLS.left() + 6, GLS.top() + 6); r_, b_ = Z(GLS.right() - 6, GLS.bottom() - 6)
            cv.save(); cv.clipRRect(RRXY(LTRB(l_, t_, r_, b_), 16 * z, 16 * z), True)
            if not gone and lamp < 1: cv.drawRect(LTRB(l_, t_, r_, b_), fill((5, 7, 20), 238 * (1 - lamp)))
            if fog_a > 0:
                cv.drawRect(LTRB(l_, t_, r_, b_), fill((178, 190, 214), 225 * clamp(fog_a)))
                for i in range(5):
                    pf = fill((226, 232, 244), 120 * clamp(fog_a)); pf.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26 * z))
                    cv.drawCircle(l_ + ((i * 97 + k * 3) % int(r_ - l_ + 120)) - 60, t_ + 60 * z + (i * 71 * z) % int(b_ - t_ - 60 * z), 70 * z, pf)
            if lant > 0 or sil > 0:
                vy = GLS.top() + GLS.height() * 0.40; sw = 7 * math.sin(k * 0.6) * lant
                if sil > 0:                                  # karalti: kasketli biri (yuzu secilmez)
                    hx_, hy_ = Z(552, lerp(vy - 4, 838, sil)); hr = lerp(5, 66, sil) * z; c_ = (7, 9, 24)
                    poly(cv, [(hx_ - hr * 1.7, hy_ + hr * 1.3), (hx_ + hr * 1.7, hy_ + hr * 1.3), (hx_ + hr * 2.3, b_ + 40), (hx_ - hr * 2.3, b_ + 40)], c_)
                    cv.drawCircle(hx_, hy_, hr, fill(c_))
                    cv.drawRRect(RRXY(LTRB(hx_ - hr * 1.0, hy_ - hr * 1.5, hx_ + hr * 1.0, hy_ - hr * 0.72), hr * 0.3, hr * 0.3), fill((70, 16, 24)))
                    cv.drawOval(LTRB(hx_ - hr * 0.94, hy_ - hr * 0.98, hx_ + hr * 0.94, hy_ - hr * 0.5), fill((4, 5, 14)))
                    rim = skia.Path(); rim.addArc(LTRB(hx_ - hr, hy_ - hr, hx_ + hr, hy_ + hr), 120, 90); cv.drawPath(rim, stroke(AMBER, max(1.5, hr * 0.07), 150 * sil))
                if lant > 0:
                    lx_, ly_ = Z(540 - 74 * lant + sw, lerp(vy + 6, 922, lant)); lr = lerp(3, 25, lant) * z
                    gl = fill((255, 214, 130), 170); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, lr * 1.5)); cv.drawCircle(lx_, ly_, lr * 3.4, gl)
                    if lant > 0.35:
                        rr = RRXY(LTRB(lx_ - lr * 0.8, ly_ - lr, lx_ + lr * 0.8, ly_ + lr * 1.1), lr * 0.25, lr * 0.25)
                        cv.drawRRect(rr, fill((255, 236, 170))); cv.drawRRect(rr, stroke((50, 44, 40), lr * 0.18)); cv.drawLine(lx_, ly_ - lr, lx_, ly_ + lr * 1.1, stroke((50, 44, 40), lr * 0.12))
                        hd = skia.Path(); hd.addArc(LTRB(lx_ - lr * 0.6, ly_ - lr * 1.9, lx_ + lr * 0.6, ly_ - lr * 0.7), 180, 180); cv.drawPath(hd, stroke((50, 44, 40), lr * 0.16))
                    else: cv.drawCircle(lx_, ly_, lr, fill((255, 244, 206)))
            cv.drawLine(l_ + 30 * z, t_ + 84 * z, l_ + 90 * z, t_ + 24 * z, stroke((255, 255, 255), 7 * z, 40))
            cv.restore()
        elif cond:                                           # acilan kapinin araliginda Konduktor
            l_, t_ = Z(D0, DT); r_, b_ = Z(D0 + (D1 - D0) * 0.96 * clamp(open_u), WF + 14)
            cv.save(); cv.clipRect(LTRB(l_, t_ - 4, r_, b_))
            cx_, cy_ = Z(532, WF + 6); kw = dict(cond[3]) if len(cond) > 3 else {}
            gl = fill((255, 214, 130), 70); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60 * z)); cv.drawCircle(cx_ - 90 * z, cy_ - 200 * z, 200 * z, gl)
            actor(cv, ts, 'C', cond[0], cond[1], cond[2], place=(cx_, cy_, 0.60 * z), **kw)
            cv.restore()
        if mia:
            mx, my = Z(mia[0], NEAR)
            actor(cv, ts, 'M', mia[1], mia[2], mia[3], place=(mx, my, 0.70 * z), back=True, prop='carry')


# ---------- disaridan: tren ----------
def ext(cv, ts, k, xr, n, heads=None, sc=None, fog_a=0.6, moon=None):
    u, y = (1.0, 1130) if V else (1.5, 1150)
    with stage(cv):
        ext_bg(cv, SC(ts) if sc is None else sc, k, y=y + 21 * u - 22, moon=moon or ((800, 520) if V else (1180, 620)), fog_a=fog_a)
        mid = train_ext(cv, xr, y, u, n, k, heads=heads or {})
    return mid, y, u


# ---------- orgudeki uc istasyon adi (Mia'nin elinde, yakin) ----------
KNAMES = ('YEDİGÖL', 'DEĞİRMEN', 'KARAKÖPRÜ')              # ustten alta (b03'teki gibi)
FW, FH, BH = 760, 450, 150
def _fabric(c):
    rc = LTRB(20, 40, 20 + FW, 40 + FH + 34)
    c.drawRRect(RRXY(rc, 20, 20), fill(CREAM))
    for j, nm in enumerate(KNAMES):
        y0 = 40 + j * BH
        if j: c.drawLine(34, y0, 6 + FW, y0, dashed(CORAL, 5, 230, (16, 12)))
        f = skia.Font(TFB, 96); f.setEmbolden(True); w = f.measureText(nm)
        if w > FW - 110: f.setSize(96 * (FW - 110) / w); w = f.measureText(nm)
        c.drawString(nm, 20 + FW / 2 - w / 2 + 3, y0 + BH * 0.5 + f.getSize() * 0.36 + 4, f, fill(shade(CORAL, 0.62), 150))
        c.drawString(nm, 20 + FW / 2 - w / 2, y0 + BH * 0.5 + f.getSize() * 0.36, f, fill(CORAL))
    c.drawLine(34, 40 + FH, 6 + FW, 40 + FH, dashed(CORAL, 5, 230, (16, 12)))
    c.save(); c.clipRRect(RRXY(rc, 20, 20), True)
    vs = stroke(shade(CREAM, 0.74), 2.6, 96)
    for r in range(int((FH + 34) / 20) + 1):
        y = 46 + r * 20
        for q in range(int(FW / 22) + 1):
            x = 24 + q * 22; c.drawLine(x, y, x + 9, y + 14, vs); c.drawLine(x + 18, y, x + 9, y + 14, vs)
    c.restore(); c.drawRRect(RRXY(rc, 20, 20), stroke(shade(CREAM, 0.66), 4))


def knit_names(cv, ts, k, hi, bgf):
    """hi: (Karakopru, Degirmen, Yedigol) parlama 0..1"""
    bgf(); dim(cv, 0.62)
    x0 = 540 - FW / 2; y0 = 590 if V else 560; sway = 3 * math.sin(k * 0.25)
    with stage(cv):
        cv.save(); cv.translate(sway, 0)
        for sd in (-1, 1):
            hx_, hy_ = 540 + sd * (FW / 2 + 30), y0 + 6 + alt(k, 0, 5, 4) * sd
            yarn_limb(cv, [(hx_ + sd * 300, y0 + 900), (hx_ + sd * 170, y0 + 420), (hx_ + sd * 10, hy_ + 30)], 104, MUSTARD)
        cv.drawLine(x0 - 130, y0 - 14, x0 + FW + 110, y0 - 2, stroke((70, 64, 84), 20)); cv.drawLine(x0 - 130, y0 - 14, x0 + FW + 110, y0 - 2, stroke((150, 142, 166), 13))
        cv.drawCircle(x0 - 136, y0 - 14, 20, fill((150, 142, 166)))
        blit(cv, sprite(('fabric4', FMT), FW + 40, FH + 120, _fabric), x0 - 20, y0 - 40)
        for q_ in range(int(FW / 34)): cv.drawOval(LTRB(x0 + 8 + q_ * 34, y0 - 24, x0 + 34 + q_ * 34, y0 + 12), stroke(CREAM, 5))
        for j, nm in enumerate(KNAMES):
            a = hi[2 - j]
            if a > 0:
                f = skia.Font(TFB, 96); f.setEmbolden(True); w = f.measureText(nm)
                if w > FW - 110: f.setSize(96 * (FW - 110) / w); w = f.measureText(nm)
                yy = y0 + j * BH + BH * 0.5 + f.getSize() * 0.36
                gl = fill((255, 214, 80), 120 * a); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26)); cv.drawRect(LTRB(540 - w / 2 - 20, yy - f.getSize() * 0.86, 540 + w / 2 + 20, yy + 16), gl)
                cv.drawString(nm, 540 - w / 2, yy, f, fill((150, 30, 40), 255 * a))
                badge_at(cv, x0 + FW - 6, yy - 30, str(3 - j), a=a, r=34)
        for sd in (-1, 1): hand_ball(cv, 540 + sd * (FW / 2 + 30), y0 + 6 + alt(k, 0, 5, 4) * sd, 60, MUSTARD, seed=5 + sd)
        cv.restore()


# ---------- duraklar seridi (ekran koordinati) ----------
STOPS = ('KARAKÖPRÜ', 'DEĞİRMEN', 'YEDİGÖL', 'SARNIÇ', 'SON DURAK')
def stops_strip(cv, k, a=1.0, done=4, hot=None, beyond=0.0):
    """bes durak: gecilenler onayli; hot: kirmizi yanan; beyond 0..1: Son Durak'tan sonrasi (karanlik, ray biter)"""
    if a <= 0: return
    if V: pts = [(540, 400 + j * 104) for j in range(5)]; fs = 44; bw = 520
    else: pts = [(300 + j * 330, 236) for j in range(5)]; fs = 32; bw = 290
    cv.saveLayerAlpha(skia.Rect.MakeWH(W, H), int(255 * clamp(a)))
    (xa, ya), (xb, yb) = pts[0], pts[-1]
    ex = (xb, yb + 150) if V else (xb + 260, yb)
    cv.drawLine(xa, ya, xb, yb, stroke((0, 0, 0), 18, 200)); cv.drawLine(xa, ya, xb, yb, stroke((150, 158, 180), 8))
    if beyond > 0:
        cv.drawLine(xb, yb, lerp(xb, ex[0], beyond), lerp(yb, ex[1], beyond), dashed((150, 158, 180), 8, 230, (16, 14)))
        if beyond > 0.6: otext(cv, '?', ex[0] if V else ex[0] + 10, ex[1] + (70 if V else 26), 84 if V else 70, RED, a=seg(beyond, 0.6, 1.0) * (1.0 if (k // 3) % 2 else 0.65))
    for j, (x, y) in enumerate(pts):
        hot_ = hot == j and (k // 3) % 2 == 0
        rc = LTRB(x - bw / 2, y - fs * 0.9, x + bw / 2, y + fs * 0.9)
        cv.drawRRect(RRXY(rc.makeOffset(4, 6), 10, 10), fill((4, 6, 20), 140)); cv.drawRRect(RRXY(rc, 10, 10), fill(RED if hot_ else PAPER))
        cv.drawRRect(RRXY(rc.makeInset(6, 6), 6, 6), dashed((150, 40, 46), 2.5, 220, (10, 8)))
        f = skia.Font(TFB, fs); w = f.measureText(STOPS[j])
        if w > bw - 90: f.setSize(fs * (bw - 90) / w); w = f.measureText(STOPS[j])
        cv.drawString(STOPS[j], x - w / 2 - (18 if j < done else 0), y + f.getSize() * 0.36, f, fill(CREAM if hot_ else (150, 40, 46)))
        if j < done: check(cv, rc.right() - 36, y, 18, (40, 150, 90))
    cv.restore()


# ---------- uc yolcu (ekran koordinati): carpi, sonra onay ----------
TRIO = (('E', SKYB, 'ELI'), ('R', GREENC, 'REN'), ('D', ROSE, 'ADA'))
def trio(cv, k, a3, ok=0.0):
    """a3: uc yolcunun gorunurlugu; ok 0..1: carpilar onaya doner"""
    for j, ((w_, c_, nm), a) in enumerate(zip(TRIO, a3)):
        if a <= 0: continue
        x, y, r = ((250 + j * 290, 470, 56) if V else (700 + j * 260, 200, 50))
        y += 16 * (1 - a)
        hand_ball(cv, x, y, r, c_, seed=3 + j)
        otext(cv, nm, x, y + r + 50, 40 if V else 34, CREAM, a=a)
        if ok < 0.5: cross(cv, x, y, r * 0.62, a * (1 - seg(ok, 0.2, 0.5)))
        else: check(cv, x + 4, y, r * 0.62 * lerp(1.4, 1.0, smooth(seg(ok, 0.5, 0.8))), a=a * seg(ok, 0.5, 0.65))


# ============ SAHNE 1: kanca. Bir numaranin arka kapisi: ardinda vagon yok, camda fener ve kasketli bir karalti ============
def door_hook(cv, ts, k, u, bang=False, z=1.12):
    """u 0..1: karalti buyur"""
    mia = (250, 'panik', dict(aR=(110, 30, 190, -70 + (alt(k, 0, 26, 2) if bang else 0)), lean=-10, belly=8), 2)
    back_door(cv, ts, k, z, (540, 930), (540, 960) if V else (540, 1010), gone=True, sc=SC(ts), lant=lerp(0.8, 1.0, u), sil=lerp(0.72, 1.0, u), mia=mia)


def scene1(cv, t):
    ts, k = step(t), kk(t)
    door_hook(cv, ts, k, smooth(seg(ts, 0.0, HK)), bang=True)
    flash(cv, 0.8 * seg(t, HK - 0.12, HK))


# ============ SAHNE 2: disaridan: iki vagon; uc, dort ve bes numaranin yeri bos ============
def scene2(cv, t):
    ts, k = step(t), kk(t)
    a0 = TL.span(2)[0]
    xr = (1040 if V else 1300) + 22 * (ts - a0)
    mid, y, u = ext(cv, ts, k, xr, 2, heads={2: [None, None, MUSTARD, None, None]})
    yb = y - 170 * u
    with stage(cv):
        for i, c_ in ((3, ROSE), (4, GREENC), (5, SKYB)):                               # kaybolan vagonlarin hayali
            gx = mid[2] - (i - 2) * PITCH * u; hot = i == 3 and frac('n1', 0.12) <= ts < frac('n1', 0.5)
            cv.drawRRect(RRXY(LTRB(gx - 82 * u, y - 96 * u, gx + 83 * u, y), 8 * u, 8 * u), dashed(RED if hot else CREAM, 4, 230 if hot else 130, (14, 10)))
            text(cv, str(i), gx, y - 34 * u, 44 * u, CREAM, a=120)
            a = seg(ts, a0 + 0.1 + 0.1 * (5 - i), a0 + 0.3 + 0.1 * (5 - i))
            if a > 0:
                hand_ball(cv, gx, yb + 14 * (1 - a) + 30, 30 if V else 36, c_, seed=3 + i)
                for sd in (-1, 1): cv.drawLine(gx - 28, yb + 30 - sd * 28, gx + 28, yb + 30 + sd * 28, stroke(RED, 8, 255 * a))
        a = seg(ts, frac('n1', 0.6), frac('n1', 0.6) + 0.15)
        if a > 0: badge_at(cv, mid[2], yb + 14 * (1 - a) + 20, '1', a=a, r=44)
    flash(cv, 0.8 * (1 - seg(t, HK, HK + 0.2)))


# ============ SAHNE 3: iki numara: Mia orguyu sikar (hisirti); icinden rulo bir not cikar ============
def scene3(cv, t):
    ts, k = step(t), kk(t)
    fb, nb = B('feel'), B('find'); o = ts - nb[0]
    sq = any(0 <= ts - fb[0] - x < 0.22 for x in FEEL)
    close = ts >= frac('m2', 0.48)
    if o >= FIND: M_ = ('saskin', dict(SHOWB, aL=(-84, 110, -40, 180), lean=alt(k, 0, 3, 5)), 1.4, dict(prop='found'))
    elif o >= 0.05: M_ = ('merak', mixpose(KNIT, DIG, seg(o, 0.05, 0.4)), 0, dict(prop='knit'))
    else:
        d = 12 if sq else 0
        M_ = ('merak' if ts >= fb[0] + FEEL[0] else 'uzgun', dict(aL=(-84 + d, 110, -40 + d, 180), aR=(84 - d, 110, 40 - d, 180), lean=3 if sq else 0), 0, dict(prop='knit'))
    def ex(f):
        if sq: sfx_text(cv, f['M']['handR'][0] + 130, f['M']['handR'][1] - 50, 'HIŞ', 56, a=1.0)
        if FIND <= o < FIND + 0.5: sfx_text(cv, f['M']['handR'][0] + 60, f['M']['handR'][1] - 150, 'HIŞŞ', 50, a=1 - seg(o, FIND + 0.3, FIND + 0.5))
    zz = (1.5 if V else 1.55, (MIA2[0] + 30, 950), QC) if close else (0.95 if V else 1.0, (480, 1000), QW)
    with zoom(cv, *zz): w2(cv, ts, k, {'M': (MIA2, M_)}, extra=ex)


# ============ SAHNE 4: eller (cok yakin): not acilir, icinden kursun kalem cikar; baslik ============
def bg2(cv, ts, k):
    with zoom(cv, 2.3, (MIA2[0], 1000), (540, 1000)): wagon(cv, CAMA, 2, k, scroll=SC(ts), last=True)
def scene4(cv, t):
    ts, k = step(t), kk(t)
    a0 = TL.span(4)[0]; u = smooth(seg(ts, a0 + 0.1, a0 + 0.9)); pu = smooth(seg(ts, frac('m3', 0.42), frac('m3', 0.42) + 0.4))
    bg2(cv, ts, k); dim(cv, 0.6)
    with stage(cv):
        cx, cy = 540, (790 if V else 900); w = lerp(170, 660, u); h = 440
        for sd in (-1, 1):
            hx_ = cx + sd * (w / 2 + 26)
            yarn_limb(cv, [(hx_ + sd * 280, cy + 760), (hx_ + sd * 160, cy + 400), (hx_ + sd * 12, cy + 80)], 100, MUSTARD)
        rc = LTRB(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
        sh = fill((4, 6, 20), 150); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16)); cv.drawRRect(RRXY(rc.makeOffset(8, 16), 12, 12), sh)
        cv.drawRRect(RRXY(rc, 12, 12), fill((252, 246, 228)))
        cv.save(); cv.clipRRect(RRXY(rc, 12, 12), True)
        f = skia.Font(TFM, 82); f.setSkewX(-0.22); cv.drawString("Mia'ya", cx - 290, cy - 96, f, fill(INK))
        for j in range(3):
            y = cy + 6 + j * 84; cv.drawLine(cx - 300, y + 24, cx + 300, y + 24, stroke((176, 190, 232), 2.5, 200, cap=False))
            p = skia.Path(); p.moveTo(cx - 290, y)
            for q_ in range(20 - 5 * (j == 2)): p.rQuadTo(6.5, -16 * (1 if q_ % 2 else -0.6), 13, 0); p.rQuadTo(6.5, 10, 13, 0)
            cv.drawPath(p, stroke(INK, 4.5, 150))
        cv.restore()
        for sd in (-1, 1):                                   # kivrik kenarlar (rulo izleri)
            xx = cx + sd * w / 2; cv.drawRRect(RRXY(LTRB(xx - 20, cy - h / 2 - 6, xx + 20, cy + h / 2 + 6), 20, 20), fill(shade(CREAM, 0.9))); cv.drawLine(xx, cy - h / 2 + 10, xx, cy + h / 2 - 10, dashed(shade(CREAM, 0.7), 2.5, 180, (10, 8)))
        py = lerp(cy + 40, cy + h / 2 + 96, pu)              # kalem: rulonun icinden asagi kayar
        if u > 0.5: pencil(cv, cx - 250, py, 470, 4 + 6 * (1 - pu), th=42, a=seg(u, 0.5, 0.8))
        for sd in (-1, 1): hand_ball(cv, cx + sd * (w / 2 + 26), cy + 64, 62, MUSTARD, seed=5 + sd)
        if pu > 0.9: star(cv, cx + 250, py - 50, 20 + 6 * math.sin(k * 0.8), YEL)
    title_card(cv, t)


# ============ SAHNE 5: mektup: "Mia, kizim. Bu notu bulduysan ben yerime vardim." ============
def scene5(cv, t):
    ts, k = step(t), kk(t)
    letter_plan(cv, ts, k, ['Mia, kızım.', 'Bu notu bulduysan', 'ben yerime vardım.'], 'd1', lambda: bg2(cv, ts, k))


# ============ SAHNE 6: Mia okur, arkasina bakar: bos ray; sonra onu: isikli kapi ============
def scene6(cv, t):
    ts, k = step(t), kk(t)
    t1, t2 = frac('d2', 0.3), frac('d2', 0.64)
    if ts < t1:
        lk = 0 if ts < frac('d2', 0.1) else -2
        M_ = ('uzgun', dict(READ, lean=-6 if lk else 0), lk, dict(prop='read'))
        with zoom(cv, 1.5 if V else 1.55, (MIA2[0], 950), QC): w2(cv, ts, k, {'M': (MIA2, M_)})
    elif ts < t2:
        with zoom(cv, lerp(1.0, 1.25, seg(ts, t1, t2)), (540, 900), (540, 930) if V else (540, 1000)): door_view(cv, k, gone=1.0, scroll=SC(ts), plate_on=0.0)
    else:
        with zoom(cv, lerp(1.25, 1.0, seg(ts, t2, E('d2') + 0.5)), (540, 900), (540, 930) if V else (540, 1000)):
            door_view(cv, k, scroll=-SC(ts), label='VAGON 1', glass=fwd_glass)


# ============ SAHNE 7: anons; levha: VAGON 2 kirmizi yanar ============
def scene7(cv, t):
    ts, k = step(t), kk(t)
    lv = TL.talk('A', ts); ch = B('chime'); late = ts >= frac('a1', 0.5)
    sh = jit(k, 2.5) if ch[0] <= ts < ch[0] + 0.8 else (0, 0)
    spk = lv if lv is not None else (0.5 if ch[0] <= ts < ch[0] + 0.8 else None)
    hi = 1.0 if ts >= frac('a1', 0.62) else 0.0
    if late:
        with zoom(cv, 2.6 if V else 2.3, (2500 - CAMA, 612), (540, 800) if V else (540, 950)): wagon(cv, CAMA, 2, k, scroll=SC(ts), last=True, spk=spk, plate_hi=hi)
        return
    up = ts >= ch[0] + 0.3
    M_ = ('merak' if up else 'uzgun', dict(READ, **LOOKUP) if up else READ, 2 if up else 0, dict(prop='read'))
    with zoom(cv, 1.0 if V else 1.05, ((640 if V else 560) + sh[0], 960 + sh[1]), (540, 1010)): w2(cv, ts, k, {'M': (MIA2, M_)}, spk=spk, plate_hi=hi)


# ============ SAHNE 8: "Burasi iki numara!": Mia one kosar ============
def scene8(cv, t):
    ts, k = step(t), kk(t)
    t1 = frac('m4', 0.5); x = lerp(XM, 2600, seg(ts, t1 + 0.1, E('m4') + 0.55) ** 1.3); am = 1 - seg(x, 2500, 2590)
    if ts < t1: M_ = ('saskin', dict(POINTUP, **LOOKUP), 2, dict(prop='carry'))
    elif x <= XM + 1: M_ = ('panik', dict(lean=10), 2, dict(prop='carry'))
    else: M_ = ('panik', dict(walk(x - XM, 0.70, 1, run=True, hold=True), aL=(-60, 110, -20, 190), aR=(90, 100, 150, 60)), 2, dict(prop='carry', alpha=am))
    with zoom(cv, 0.95 if V else 1.0, (620, 1000), QW):
        w2(cv, ts, k, {'M': ((x - CAMA, NEAR, 0.70), M_)}, plate_hi=1.0, door_f=smooth(seg(ts, t1, t1 + 0.5)))


# ============ SAHNE 9: koruk: ikiden bire; orgudeki uc istasyon adi; Mia toparlanir ============
def gw(cv, ts, k, x, M_, shake=3.0, closed=0.0):
    gangway(cv, k, scroll=SC(ts), shake=shake, nos=(2, 1), hi=(1.0, 0.0), closed=closed)
    with stage(cv): return actor(cv, ts, 'M', M_[0], M_[1], M_[2], place=(x, NEAR, 0.70), prop='carry')
def scene9(cv, t):
    ts, k = step(t), kk(t)
    a0 = TL.span(9)[0]; t1, t2 = frac('d3', 0.27), frac('d3', 0.66)
    if ts < t1:
        x = lerp(40, 500, seg(ts, a0, t1))
        with zoom(cv, 0.95 if V else 1.0, (540, 1000), QW): gw(cv, ts, k, x, ('panik', walk(x - 40, 0.70, 1, scared=True, hold=True), 2))
    elif ts < t2:
        def pulse(t0): return clamp(1 - abs(ts - t0 - 0.35) / 0.7) if ts >= t0 else 0.0
        hi = [max(pulse(frac('d3', f_)), 0.35 if ts >= frac('d3', f_) else 0) for f_ in (0.33, 0.45, 0.56)]
        def bgf():
            with zoom(cv, 2.2, (540, 1000), (540, 1000)): gangway(cv, k, scroll=SC(ts), shake=2.0, nos=(2, 1), hi=(1.0, 0.0))
        knit_names(cv, ts, k, hi, bgf)
    else:
        x = lerp(560, 640, seg(ts, t2, E('d3') + 0.3))
        with zoom(cv, 1.45 if V else 1.5, (x + 20, 950), QC): gw(cv, ts, k, x, ('kararli', dict(walk(x - 560, 0.70, 1, hold=True), **CHEST), 2), shake=2.0)


# ============ SAHNE 10: bir numara (genis): Mia arka kapidan girer; vagon bos ============
CAM10 = -180
def scene10(cv, t):
    ts, k = step(t), kk(t)
    eb = B('enter'); o = ts - eb[0]
    x = lerp(150, 560, smooth(seg(o, 0.2, 1.5)))
    if 150 < x < 559: M_ = ('endise', walk(x - 150, 0.70, 1, hold=True), 2, dict(prop='carry'))
    else: M_ = ('merak', {}, alt(k, 2, -1, 8), dict(prop='carry'))
    with zoom(cv, 0.92 if V else 1.0, (540, 1000), QW):
        w1(cv, ts, k, CAM10, {'M': ((x - CAM10, NEAR, 0.70), M_)}, last=False, door_r=1 - smooth(seg(o, 0.9, 1.4)))


# ============ SAHNE 11: lokomotifin kapisi: asma kilit ============
def scene11(cv, t):
    ts, k = step(t), kk(t)
    o = ts - B('lock')[0]
    hit = any(0 <= o - x < 0.2 for x in LOCKS)
    sh = jit(k, 5) if hit else (0, 0)
    close = ts >= frac('m5', 0.5)
    def draw():
        door_view(cv, k, scroll=-SC(ts), label='LOKOMOTİF', glass=loco_glass, lock=True, shake=sh, plate_hi=1.0 if o >= LOCKS[-1] + 0.2 and not close else 0.0)
        with stage(cv, *sh):
            if not close:
                rch = smooth(seg(o, -0.1, 0.2)); hx_, hy_ = 690 + (-8 if hit else 0), 1096 + 420 * (1 - rch) + (6 if hit else 0)
                yarn_limb(cv, [(930, 1700 + 420 * (1 - rch)), (840, 1400 + 420 * (1 - rch)), (hx_ + 20, hy_ + 26)], 84, MUSTARD)
                hand_ball(cv, hx_, hy_, 46, MUSTARD)
            for j, x in enumerate(LOCKS):
                if 0 <= o - x < 0.3: sfx_text(cv, 800 + 30 * (j % 2), 1000 - 40 * j, 'TAK', 62, a=1 - seg(o - x, 0.15, 0.3))
            if o >= LOCKS[-1] + 0.25 and not close:
                a = 1.0 if (k // 3) % 2 == 0 else 0.6
                sfx_text(cv, 540, 990, 'KİLİTLİ', 70, c=RED, rot=-4, a=a, rays=False)
    if close:
        with zoom(cv, 1.55, (540, 850), (540, 880) if V else (540, 960)): draw()
    else: draw()


# ============ SAHNE 12: Mia notu okur (bir numaranin onu); sonra hoparlor: "her sesin bir sahibi olur" ============
MIAB = (XMB - CAMB, NEAR, 0.70)
def scene12(cv, t):
    ts, k = step(t), kk(t)
    t1 = frac('d4', 0.5)
    if ts < t1:
        M_ = ('merak', READ, 0, dict(prop='read'))
        with zoom(cv, 1.45 if V else 1.5, (MIAB[0] + 40, 950), QC): w1(cv, ts, k, CAMB, {'M': (MIAB, M_)}, last=False)
    else:
        with zoom(cv, lerp(2.2, 2.7, seg(ts, t1, E('d4') + 0.4)) if V else lerp(2.0, 2.4, seg(ts, t1, E('d4') + 0.4)), (SPKX - CAMB + 30, 606), (540, 860) if V else (540, 960)):
            wagon(cv, CAMB, 1, k, scroll=SC(ts), last=False)


# ============ SAHNE 13: Sarnic peronu: tren durur; peronda tas bir sarnic kuyusu ============
def cistern(cv, x, y, k):
    """perondaki tas sarnic: agzinda ay isigi vuran su, yaninda yanan fener"""
    cv.drawOval(LTRB(x - 190, y - 16, x + 190, y + 120), fill((4, 6, 20), 110))
    cv.drawRect(LTRB(x - 176, y - 40, x + 176, y + 40), fill((92, 96, 116)))
    cv.drawOval(LTRB(x - 176, y - 2, x + 176, y + 82), fill((92, 96, 116)))
    for j in range(7): cv.drawLine(x - 150 + j * 50, y - 24, x - 150 + j * 50, y + 44, dashed((60, 62, 82), 3, 170, (12, 9)))
    cv.drawOval(LTRB(x - 176, y - 84, x + 176, y + 4), fill((126, 130, 150))); cv.drawOval(LTRB(x - 176, y - 84, x + 176, y + 4), dashed((70, 74, 96), 3, 200, (14, 10)))
    w = LTRB(x - 140, y - 70, x + 140, y - 10)
    p = skia.Paint(AntiAlias=True); p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, w.top()), skia.Point(0, w.bottom())], [col((44, 78, 140)), col((18, 34, 84))])); cv.drawOval(w, p)
    wob = 2 * math.sin(k * 0.3)
    cv.drawOval(LTRB(x - 46 + wob, y - 52, x + 46 + wob, y - 28), fill((244, 232, 184))); cv.drawLine(x - 70, y - 22, x + 70, y - 22, stroke((244, 232, 184), 3, 120))


def scene13(cv, t):
    ts, k = step(t), kk(t)
    s0 = B('stop')[0]; u = seg(ts, s0, s0 + HALT); tx = -700 * (1 - u) ** 2
    sh = jit(k, 3) if s0 + HALT - 0.05 <= ts < s0 + HALT + 0.3 else (0, 0)
    cv.save(); cv.translate(sh[0] * K, 0)
    platform(cv, STN, tx, k, heads4=[None, None, None, MUSTARD, None], heads5=[None] * 5, n_last=2, fog_a=0.45)
    with stage(cv):
        cistern(cv, 250 if V else 40, 1232 + (300 if V else 196), k)
        bx, by = (800 if V else 1240), 1232 + 170                                       # bankta yanan fener: istasyon bakimli
        gl = fill((255, 214, 130), 150); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)); cv.drawCircle(bx - 84, by - 44, 62, gl)
        cv.drawRRect(RRXY(LTRB(bx - 106, by - 74, bx - 62, by - 6), 8, 8), fill((255, 226, 150))); cv.drawRRect(RRXY(LTRB(bx - 106, by - 74, bx - 62, by - 6), 8, 8), stroke((50, 44, 40), 6))
    cv.restore()


# ============ SAHNE 14: bir numaranin arka kapisi: iki numara (bos) soner, sis, bos ray ============
def scene14(cv, t):
    ts, k = step(t), kk(t)
    ot = B('out'); o = ts - ot[0]
    if ts >= S('m6') - 0.12:                                 # Mia (yandan, yakin)
        M_ = ('uzgun' if ts < frac('m6', 0.5) else 'endise', dict(lean=-4), -2, dict(prop='carry'))
        with zoom(cv, 1.45 if V else 1.5, (430 - CAMR + 10 - 120, 950), QC): w1(cv, ts, k, CAMR, {'M': ((430 - CAMR - 120, NEAR, 0.70), M_)})
        return
    n_off = sum(1 for x in OUT_OFF if o >= x); lamp = 1 - n_off / 3.0
    if n_off < 3 and any(0 <= o - x < 0.16 for x in OUT_OFF) and k % 2: lamp = min(1.0, lamp + 0.2)
    gone = o >= GONE
    fa = smooth(seg(o, 1.35, 1.9)) * (1 - smooth(seg(o, GONE + 0.15, GONE + 0.8)))
    sh = jit(k, 2.5) if GONE - 0.3 <= o < GONE + 0.3 else (0, 0)
    u = smooth(seg(o, 0.0, 1.6)); z = lerp(1.0, 1.5, u)
    mia = (250, 'endise', dict(aR=(110, 40, 170, -40), lean=-4), 2)
    back_door(cv, ts, k, z, (540, lerp(1000, 870, u)), (540, lerp(1000, 920 if V else 970, u)), lamp=lamp, gone=gone, fog_a=fa,
              sc=200 * max(0.0, o - GONE) ** 1.4, shake=sh, mia=mia if u < 0.9 else None, hi=0.0 if gone else 1.0)


# ============ SAHNE 15: cam (yakin): rayda bir fener yaklasir; Mia geri cekilir; kapi acilir: Konduktor ============
def scene15(cv, t):
    ts, k = step(t), kk(t)
    lb, ob = B('lamp'), B('open'); o = ts - lb[0]; t1 = frac('m7', 0.44)
    if ts < S('m7') - 0.1:
        back_door(cv, ts, k, ZG, PG, QG, gone=True, sc=SC(ts), lant=0.62 * seg(o, 0.25, 2.7) ** 1.5, sil=0.5 * seg(o, 1.5, 2.7))
    elif ts < t1:
        x = 430 - CAMR - 120 + 60 * seg(ts, S('m7'), t1)
        M_ = ('panik', dict(BACKP, lean=10, belly=-6), -2, dict(prop='carry'))
        with zoom(cv, 1.45 if V else 1.5, (x - 30, 950), QC): w1(cv, ts, k, CAMR, {'M': ((x, NEAR, 0.70), M_)})
    elif ts < ob[0] + OPEN[0]:
        door_hook(cv, ts, k, seg(ts, t1, ob[0] + OPEN[0]), bang=False)
    else:
        oo = ts - ob[0]; ou = smooth(seg(oo, OPEN[0], OPEN[1]))
        cond = ('yorgun', dict(aR=(110, 130, 90, 240)), 0, dict(prop='lp'))
        mia = (236 - 30 * seg(oo, OPEN[0], OPEN[1] + 0.4), 'panik', dict(aL=(-90, 60, -60, -30), aR=(90, 60, 60, -30), lean=-14, belly=10), 2)
        z = lerp(1.12, 1.3, smooth(seg(oo, OPEN[1], 2.0)))
        back_door(cv, ts, k, z, (540, 930), (540, 960) if V else (540, 1010), gone=True, sc=SC(ts), open_u=ou, cond=cond, mia=mia, shake=jit(k, 3) if OPEN[1] <= oo < OPEN[1] + 0.25 else (0, 0))
        if OPEN[1] <= oo < OPEN[1] + 0.5:
            with stage(cv): sfx_text(cv, 800, 700, 'TAK', 70, a=1 - seg(oo, OPEN[1] + 0.3, OPEN[1] + 0.5))


# ============ SAHNE 16: bir numara (genis): "Iyi geceler kucuk hanim. Biletiniz lutfen." ============
def duo(cv, ts, k, zz, M_, C_, extra=None, door_r=0.0):
    with zoom(cv, *zz): return w1(cv, ts, k, CAMR, {'M': (MIAR, M_), 'C': (CONR, C_)}, extra=extra, door_r=door_r)
def scene16(cv, t):
    ts, k = step(t), kk(t)
    a0 = TL.span(16)[0]
    if ts < S('m8') - 0.12:
        ask = ts >= frac('c1', 0.55)
        C_ = ('yorgun', mixpose({}, FWD, seg(ts, frac('c1', 0.5), frac('c1', 0.5) + 0.3)) if ask else {}, 2, dict(prop='lp'))
        M_ = ('panik' if ts < frac('c1', 0.3) else 'endise', dict(lean=10, belly=-8, aL=(-90, 90, -50, 30), aR=(90, 90, 50, 30)), -2, dict(prop='carry'))
        duo(cv, ts, k, (0.95 if V else 1.0, (540, 1000), QW), M_, C_, door_r=1 - smooth(seg(ts, a0 + 0.2, a0 + 0.9)))
    else:
        M_ = ('saskin', dict(BACKP, lean=alt(k, -4, 2, 3)) if ts >= frac('m8', 0.35) else dict(lean=6), -2, dict(prop='carry'))
        duo(cv, ts, k, zM(), M_, ('yorgun', {}, 2, dict(prop='lp')))


# ============ SAHNE 17: Konduktor (yakin): "Otuz yildir bu trenin konduktoruyum." ============
def scene17(cv, t):
    ts, k = step(t), kk(t)
    C_ = ('sakin', mixpose({}, SALUTE, seg(ts, S('c2') - 0.1, S('c2') + 0.25)) if ts < frac('c2', 0.45) else mixpose(SALUTE, {}, seg(ts, frac('c2', 0.45), frac('c2', 0.45) + 0.3)), 2, dict(prop='lantern'))
    duo(cv, ts, k, zC(1.55), ('saskin', {}, -2, dict(prop='carry')), C_)


# ============ SAHNE 18: "O kapinin ardinda vagon yok! Nereden geldiniz?" "Sarnic'tan." ============
def scene18(cv, t):
    ts, k = step(t), kk(t)
    if ts < S('c3') - 0.12:
        M_ = ('panik' if on(ts, 'm9', 0.0, 0.1) else 'endise', dict(BACKP, lean=alt(k, -6, 0, 3)), -2, dict(prop='carry'))
        duo(cv, ts, k, z2(1.15), M_, ('yorgun', {}, 2, dict(prop='lp')))
    else:
        up = ts < frac('c3', 0.3)
        C_ = ('sakin', dict(LANTUP) if up else dict(OPENR), -1.5 if up else 2, dict(prop='lantern' if not up else 'lp'))
        duo(cv, ts, k, zC(1.4), ('endise', {}, -2, dict(prop='carry')), C_)


# ============ SAHNE 19: Mia (yakin): "Eli, Ren, Ada... Hepsi sizin yuzunuzden kayboldu!" ============
def scene19(cv, t):
    ts, k = step(t), kk(t)
    M_ = ('bagir' if on(ts, 'm10', 0.0, 0.1) and ts >= frac('m10', 0.4) else 'uzgun', dict(RANT, lean=alt(k, -6, 2, 3)) if ts >= frac('m10', 0.4) else dict(CHEST), -2, dict(prop='carry') if ts < frac('m10', 0.4) else {})
    duo(cv, ts, k, zM(1.55), M_, ('yorgun', {}, 2, dict(prop='lp')))
    trio(cv, k, [seg(ts, frac('m10', f_), frac('m10', f_) + 0.15) for f_ in (0.0, 0.12, 0.24)])


# ============ SAHNE 20: Konduktor bilet halkasini kaldirir: "Kimse kaybolmadi kucuk hanim. Herkes indi." ============
def scene20(cv, t):
    ts, k = step(t), kk(t)
    jb = B('jingle')[0]; up = seg(ts, jb + 0.1, jb + 0.5)
    C_ = ('sakin', mixpose({}, dict(SHOWB, lean=alt(k, 0, 2, 4)), up), 2, dict(prop='lr' if up > 0.2 else 'lantern'))
    duo(cv, ts, k, zC(1.55), ('uzgun', {}, -2, dict(prop='carry')), C_)
    trio(cv, k, [1.0, 1.0, 1.0], ok=seg(ts, frac('c4', 0.6), frac('c4', 0.6) + 0.6))


# ============ SAHNE 21: "Indi mi? Kapilar hic acilmadi!" "Bu trende yolcu, vagonuyla birlikte iner." ============
def scene21(cv, t):
    ts, k = step(t), kk(t)
    if ts < S('c5') - 0.12:
        duo(cv, ts, k, zM(1.5), ('saskin', dict(RANT, lean=alt(k, -4, 2, 3)) if ts >= frac('m11', 0.3) else {}, -2), ('sakin', SHOWB, 2, dict(prop='lr')))
    else:
        C_ = ('sakin', dict(OPENR, lean=alt(k, 0, 3, 4)) if ts >= frac('c5', 0.2) else {}, 2, dict(prop='lantern'))
        duo(cv, ts, k, z2(1.2), ('saskin', dict(CHEST), -2, dict(prop='carry')), C_)


# ============ SAHNE 22: halka (cok yakin): uc zimbali bilet ============
RT = (('ELI', SKYB, 'KARAKÖPRÜ'), ('REN', GREENC, 'DEĞİRMEN'), ('ADA', ROSE, 'YEDİGÖL'))
def bgR(cv, ts, k, px=None):
    with zoom(cv, 2.3, (px if px is not None else CONR[0], 1000), (540, 1000)): wagon(cv, CAMR, 1, k, scroll=SC(ts), last=True)
def scene22(cv, t):
    ts, k = step(t), kk(t)
    if ts >= S('c6') - 0.12:
        duo(cv, ts, k, zC(1.5), ('saskin', {}, -2, dict(prop='carry')), ('sakin', dict(SHOWB, lean=alt(k, 0, 2, 4)), 2, dict(prop='lr')))
        return
    rb = B('ring')[0]; bgR(cv, ts, k); dim(cv, 0.64)
    if V: pos = [(580, 440, 600, -3), (580, 730, 600, 2), (580, 1010, 600, -2)]
    else: pos = [(390, 480, 550, -3), (960, 480, 550, 2), (1530, 480, 550, -2)]
    if V:
        cv.drawRRect(RRXY(LTRB(70, 330, 170, 1120), 50, 50), stroke(shade(BRASS, 0.6), 24)); cv.drawRRect(RRXY(LTRB(70, 330, 170, 1120), 50, 50), stroke(BRASS, 15))
    else:
        cv.drawRRect(RRXY(LTRB(250, 170, 1670, 270), 50, 50), stroke(shade(BRASS, 0.6), 22)); cv.drawRRect(RRXY(LTRB(250, 170, 1670, 270), 50, 50), stroke(BRASS, 14))
    for j, ((nm, c_, stn), (x, y, w, rot)) in enumerate(zip(RT, pos)):
        t0 = rb + RING_AT[j]; a = seg(ts, t0 - 0.12, t0 + 0.1)
        if a <= 0: continue
        hl = on(ts, 'm12') and frac('m12', (0.0, 0.2, 0.4)[j]) <= ts < frac('m12', (0.2, 0.4, 0.62)[j])
        ticket(cv, x, y - (10 if hl else 0), w * (1.05 if hl else 1.0), c_, nm, stn, a, rot=rot)
        h = w / 760 * 380; hx_, hy_ = x + w * 0.39, y - h * 0.24 - (10 if hl else 0)
        if ts >= t0 + 0.1:                                   # zimba deligi
            cv.drawCircle(hx_, hy_, w * 0.042, fill((14, 18, 36))); cv.drawCircle(hx_, hy_, w * 0.042, stroke((120, 100, 90), 3))
            check(cv, hx_ - w * 0.11, hy_, w * 0.035, (40, 150, 90))
        if t0 + 0.1 <= ts < t0 + 0.5: sfx_text(cv, hx_ + 10, hy_ - 54, 'ÇIT', 50, a=1 - seg(ts, t0 + 0.3, t0 + 0.5))
        lx_ = x - w / 2                                      # halkaya baglayan pirinc kopca
        if V: cv.drawLine(170, y, lx_ + 10, y, stroke(BRASS, 9))
        else: cv.drawLine(x, 270, x, y - h / 2 + 8, stroke(BRASS, 9))


# ============ SAHNE 23: mektup: uc istasyon, uc vagon, uc yolcu (sepya) ============
def stay_view(cv, ts, k, name, head_c, no, a0):
    """istasyonda birakilan vagon: isiklari yaniyor, yolcusu pencerede; tren uzaklasir"""
    cv.clear(col((8, 12, 24))); pr = ts - a0
    with stage(cv):
        night(cv, 0, k, y_h=900, moon=(160, 560) if V else (-180, 620), poles=False)
        u = 6.2; y = 1232; x0 = (28 if V else -60) - 30 * pr
        track(cv, 0, y=y + 62)
        ext_wagon(cv, x0 + 165 * u + 150 + 520 * pr, y, u, tail=True, num=no - 1 if no > 1 else None, k=k)
        ext_wagon(cv, x0, y, u, heads=[None, None, head_c, None, None], num=no, k=k)
        cv.drawRect(LTRB(-560, y + 96, 1640, 2600), fill((74, 76, 92))); cv.drawRect(LTRB(-560, y + 96, 1640, y + 122), fill((150, 150, 164)))
        cv.drawLine(-560, y + 160, 1640, y + 160, dashed((232, 200, 110), 9, 230, (36, 24)))
        cv.drawRect(LTRB(-560, 380, 1640, 478), fill((16, 20, 34))); cv.drawLine(-560, 472, 1640, 472, dashed((70, 84, 112), 3.5, 180, (18, 14)))
        sx = 540
        for sd in (-1, 1): cv.drawLine(sx + sd * 250, 476, sx + sd * 250, 540, stroke((14, 18, 30), 7, cap=False))
        rc = LTRB(sx - 310, 536, sx + 310, 664)
        cv.drawRRect(RRXY(rc.makeOffset(6, 10), 16, 16), fill((4, 6, 20), 120)); cv.drawRRect(RRXY(rc, 16, 16), fill(PAPER)); cv.drawRRect(RRXY(rc.makeInset(10, 10), 9, 9), dashed((150, 40, 46), 3.5, 220, (14, 10)))
        f = skia.Font(TFB, 82); w = f.measureText(name)
        if w > 560: f.setSize(82 * 560 / w); w = f.measureText(name)
        cv.drawString(name, sx - w / 2, 600 + f.getSize() * 0.36, f, fill((150, 40, 46)))
        for lx in ((960, -260) if V else (1160, -200)):
            poly(cv, [(lx - 36, 540), (lx + 36, 540), (lx + 330, y + 130), (lx - 330, y + 130)], LAMPC, 34)
            cv.drawLine(lx, 476, lx, 510, stroke((14, 18, 30), 6, cap=False)); poly(cv, [(lx - 24, 506), (lx + 24, 506), (lx + 54, 544), (lx - 54, 544)], (20, 24, 34)); cv.drawOval(LTRB(lx - 34, 534, lx + 34, 556), fill(LAMPC))
        fog(cv, 0.4, k, y=y + 150, h=320)
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kSoftLight); p.setAlphaf(0.4); cv.drawImage(noise_img(), 0, 0, LIN, p)


def scene23(cv, t):
    ts, k = step(t), kk(t)
    cuts = [S('d5'), frac('d5', 0.2), frac('d5', 0.4), frac('d5', 0.6)]
    j = sum(1 for x in cuts[1:] if ts >= x)
    with tint(cv, sepia_m(0.45)):
        if j < 3:
            nm, c_, stn = RT[j]; stay_view(cv, ts, k, stn, c_, 5 - j, cuts[j] if j else TL.span(23)[0])
        else:
            bgR(cv, ts, k, MIAR[0]); dim(cv, 0.7)
            if V: pos = [(250, 550, 145), (830, 550, 145), (540, 850, 140)]
            else: pos = [(420, 440, 200), (960, 440, 200), (1500, 440, 200)]
            for i, ((w_, c_, nm), (x, y, r)) in enumerate(zip(TRIO, pos)):
                a = seg(ts, cuts[3] + 0.12 * i, cuts[3] + 0.12 * i + 0.2)
                portrait(cv, ts, w_, x, y + 20 * (1 - a), r, a, ring='win', label=RT[i][2], prop='knit' if w_ == 'D' else None, expr='mutlu' if w_ == 'D' else 'sakin')


# ============ SAHNE 24: "Simdi sira sizde. Biletiniz?" Mia biletini uzatir ============
def scene24(cv, t):
    ts, k = step(t), kk(t)
    C_ = ('sakin', mixpose({}, FWD, seg(ts, frac('c7', 0.45), frac('c7', 0.45) + 0.3)), 2, dict(prop='lp'))
    if ts < S('m13') - 0.1: M_ = ('endise', {}, -2, dict(prop='carry'))
    elif ts < frac('m13', 0.3): M_ = ('endise', mixpose({}, POCKET, seg(ts, S('m13') - 0.1, S('m13') + 0.2)), -1, dict(prop='carry'))
    else: M_ = ('endise', mixpose(dict(aL=(-90, 140, -50, 220)), GIVEL, seg(ts, frac('m13', 0.3), frac('m13', 0.3) + 0.3)), -2, dict(prop='givet'))
    duo(cv, ts, k, z2(1.25), M_, C_)


# ============ SAHNE 25: zimba ve bos bilet (cok yakin): zimba tutmaz ============
def scene25(cv, t):
    ts, k = step(t), kk(t)
    pb = B('punch')[0]; o = ts - pb
    hit = [x for x in PUNCH if 0 <= o - x < 0.2]
    bgR(cv, ts, k); dim(cv, 0.64)
    cx, cy, w = (500, 740, 780) if V else (860, 480, 760)
    sh = jit(k, 4) if hit else (0, 0)
    ticket(cv, cx + sh[0], cy + sh[1], w, MUSTARD, 'MIA', None, 1.0, rot=-2, hi=1.0 if o > 0.3 else 0.0, k=k)
    h = w / 760 * 380
    inn = smooth(seg(o, 0.0, 0.4)); cl = 1.0 if hit else (0.0 if o < PUNCH[-1] + 0.5 else 0.15)
    tx_, ty_ = cx + w / 2 - 26 + 420 * (1 - inn), cy + 20                                 # zimbanin agzi biletin sag kenarinda
    s_ = 3.6 if V else 3.4
    hx_, hy_ = tx_ + 74 * s_, ty_ + 30
    yarn_limb(cv, [(hx_ + 520, hy_ + 560), (hx_ + 300, hy_ + 300), (hx_ + 110, hy_ + 60)], 110, CNAVY)
    punch_tool(cv, hx_, hy_, s_, rot=180 + 8, close=cl)
    hand_ball(cv, hx_ + 120, hy_ + 30, 70, CNAVY, seed=7)
    for j, x in enumerate(PUNCH):
        if 0 <= o - x < 0.45: sfx_text(cv, tx_ - 60, ty_ - 120 - 50 * j, 'TIK', 76, c=RED, a=1 - seg(o - x, 0.25, 0.45), rot=-8 + 14 * j)
    if o >= PUNCH[-1] + 0.3:
        a = seg(o, PUNCH[-1] + 0.3, PUNCH[-1] + 0.5)
        otext(cv, 'DELMİYOR', cx, cy - h / 2 - (50 if V else 40), 70 if V else 60, RED, a=a * (1.0 if (k // 3) % 2 else 0.7))


# ============ SAHNE 26: Mia (yakin): "Gisede ilk kalkan trene bilet istedim. Yer soylemedim." ============
def scene26(cv, t):
    ts, k = step(t), kk(t)
    M_ = ('uzgun', dict(SHOWB, lean=alt(k, 0, 3, 5)) if ts < frac('m14', 0.62) else dict(CHEST), 1.4 if ts < frac('m14', 0.62) else -2, dict(prop='tk' if ts < frac('m14', 0.62) else 'carry'))
    duo(cv, ts, k, zM(1.55), M_, ('sakin', {}, 2, dict(prop='lp')))


# ============ SAHNE 27: "Bileti bos olan inemez." "Ya Son Durak'ta?" "Bu tren, Son Durak'tan sonra hic durmaz." ============
def scene27(cv, t):
    ts, k = step(t), kk(t)
    if ts < S('m15') - 0.12:
        duo(cv, ts, k, zC(1.55), ('endise', {}, -2, dict(prop='tk')), ('uzgun', dict(lean=alt(k, 0, 2, 5)), 2, dict(prop='lp')))
    elif ts < S('c10') - 0.12:
        duo(cv, ts, k, zM(1.55), ('endise', dict(CHEST, lean=-6), -2, dict(prop='carry')), ('uzgun', {}, 2, dict(prop='lp')))
    else:
        C_ = ('uzgun', dict(LANTUP, aL=(-110, 100, -170, 110)), 2, dict(prop='lp'))
        duo(cv, ts, k, z2(1.05), ('panik' if ts >= frac('c10', 0.6) else 'endise', dict(CHEST), -2, dict(prop='carry')), C_)
        a = seg(ts, S('c10') - 0.05, S('c10') + 0.25); dim(cv, 0.45 * a)
        stops_strip(cv, k, a, done=4, hot=4 if ts >= frac('c10', 0.25) else None, beyond=smooth(seg(ts, frac('c10', 0.5), frac('c10', 0.95))))


# ============ SAHNE 28: disaridan: lokomotif ve tek vagon; onu karanlik ============
def scene28(cv, t):
    ts, k = step(t), kk(t)
    a0 = TL.span(28)[0]
    xr = (700 if V else 760) + 50 * (ts - a0)
    ext(cv, ts, k, xr, 1, heads={1: [None, CNAVY, None, MUSTARD, None]}, fog_a=0.8, moon=(180, 500) if V else (-120, 600))
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(W * 0.52, 0), skia.Point(W, 0)], [skia.Color(3, 4, 12, 0), skia.Color(3, 4, 12, 245)]))
    cv.drawRect(skia.Rect.MakeWH(W, H), g)
    a = seg(ts, a0 + 0.5, a0 + 0.9)
    otext(cv, 'SON DURAK', W * 0.5, 520 if V else 250, 84 if V else 70, CREAM, a=a)
    otext(cv, 'SONRASI YOK', W * 0.5, 630 if V else 340, 70 if V else 58, RED, a=seg(ts, a0 + 1.2, a0 + 1.5) * (1.0 if (k // 3) % 2 else 0.7))


# ============ SAHNE 29: mektubun sonu: "Seninki bos." "Bos bilet, henuz yazilmamis bilettir." ============
def scene29(cv, t):
    ts, k = step(t), kk(t)
    if ts < S('d7') - 0.15:
        letter_plan(cv, ts, k, ['Benim biletimde', 'bir yer yazıyordu kızım.', 'Seninki boş.'], 'd6', lambda: bgR(cv, ts, k, MIAR[0]))
    else:
        M_ = ('merak', dict(SHOWB, lean=alt(k, 0, 3, 5)), 1.4, dict(prop='tk'))
        duo(cv, ts, k, zM(1.5), M_, ('sakin', {}, 2, dict(prop='lp')))


# ============ SAHNE 30: kalem, bos satirin ustunde (cok yakin) ============
def blank_macro(cv, ts, k, cx, cy, w, hover):
    """bos bilet ve Mia'nin elinde kalem; hover: ucun satira uzakligi"""
    ticket(cv, cx, cy, w, MUSTARD, 'MIA', None, 1.0, rot=-2, hi=1.0, k=k)
    u = w / 760.0; tx_, ty_ = cx + 150 * u, cy + 380 * u / 2 - 70 * u - hover + 4 * math.sin(k * 0.5)
    yarn_limb(cv, [(tx_ + 560 * u, ty_ + 620 * u), (tx_ + 420 * u, ty_ + 380 * u), (tx_ + 250 * u, ty_ + 190 * u)], 116 * u, MUSTARD)
    pencil(cv, tx_, ty_, 420 * u, 40, th=40 * u)
    hand_ball(cv, tx_ + 236 * u, ty_ + 196 * u, 74 * u, MUSTARD, seed=6)


def scene30(cv, t):
    ts, k = step(t), kk(t)
    bgR(cv, ts, k, MIAR[0]); dim(cv, 0.66)
    hv = lerp(90, 14, smooth(seg(ts, S('d8'), frac('d8', 0.45)))) + 30 * smooth(seg(ts, frac('d8', 0.55), E('d8')))
    if V: blank_macro(cv, ts, k, 500, 760, 840, hv)
    else: blank_macro(cv, ts, k, 860, 500, 800, hv)
    if ts >= frac('d8', 0.05):
        a = 1 - seg(ts, frac('d8', 0.4), frac('d8', 0.5))
        star(cv, (500 + 150 * 840 / 760 + 60) if V else (860 + 150 * 800 / 760 + 60), (760 if V else 500) - 30, 22 + 6 * math.sin(k * 0.8), YEL) if a > 0 else None


# ============ SAHNE 31: kapanis karti ============
def scene31(cv, t):
    ts, k = step(t), kk(t)
    a0 = END0
    ext(cv, ts, k, (640 if V else 760) + 60 * (ts - a0), 1, heads={1: [None, CNAVY, None, MUSTARD, None]}, fog_a=0.7, moon=(840, 380) if V else (1300, 640))
    dim(cv, 0.6)
    a = smooth(seg(ts, a0 + 0.5, a0 + 1.1))
    cx, cy, w = (W / 2 - 30, 900, 520) if V else (W / 2 - 20, 560, 400)
    gl = fill((255, 226, 150), 70 * a); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60)); cv.drawCircle(cx, cy, w * 0.5, gl)
    ticket(cv, cx, cy + 30 * (1 - a), w, MUSTARD, 'MIA', None, a, rot=-4, hi=1.0, k=k)
    if a > 0.6: pencil(cv, cx + w * 0.30, cy + w * 0.13 + 4 * math.sin(k * 0.4), w * 0.5, 42, th=w * 0.05, a=seg(a, 0.6, 1.0))
    c_ = seg(t, a0 + 0.3, a0 + 0.8)
    card(cv, [('Mia biletine', 72, RED), ('ne yazacak?', 72, RED), ('Yorumlara yaz', 40, CREAM), ('Sıradaki: 5. Bölüm, Son Durak', 36, (176, 190, 232))],
         c_, cy=470 if V else 215)


SINE = {1: dict(zmax=1.12), 2: dict(mood='gece'), 4: dict(zmax=1.1), 5: dict(zmax=1.1, rays=False), 6: dict(zmax=1.12), 9: dict(zmax=1.12), 13: dict(mood='soguk'),
        14: dict(mood='soguk'), 22: dict(zmax=1.1, rays=False), 23: dict(mood='sepya'), 25: dict(zmax=1.1, rays=False), 27: dict(zmax=1.1),
        28: dict(mood='gece'), 29: dict(zmax=1.1, rays=False), 30: dict(zmax=1.1, rays=False), 31: dict(mood='gece')}

if __name__ == '__main__':
    DRAW = {i: globals()[f'scene{i}'] for i in range(1, 32)}
    run(DRAW, white=tuple((i, i + 1) for i in range(1, 31)), sine=SINE, hud=hud)
