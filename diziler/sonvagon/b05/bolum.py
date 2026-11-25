"""Son Vagon, 5. Bolum: Son Durak (dizinin son bolumu). Yalnizca sahneler; ortak parcalar ../ortak.py icinde.
Yapi: GERI DONUSLU + KAPANIS MONTAJI. Bugun (bir numara, lokomotif, Son Durak) ile bu aksam (sepya: ev, gise) arasinda gidip gelir;
sonu sabah montajidir. Onceki bolumlerin kurgusu (mektup, kayit, tersten) tekrar edilmez.
Kanca (lokomotif: makinist koltugu bos) -> disaridan tek vagon -> Konduktor duvardaki pirinc mikrofondan anons yapar -> lokomotifin kilidi acilir ->
lokomotif: kendi kendine oynayan kollar, bos koltuk -> yol tablosu (bes durak, bir bos bilet) -> on cam: karanlik ->
GERI DONUS: ev (kapi carpilir) -> gise ("Nereye?") -> ev (mutfagin isigi) -> on camda Son Durak'in isiklari -> kalem EV yazar -> zimba deler ->
Son Durak peronu: vagonun kapisi ilk kez acilir -> ayni gise, ayni saat -> yarim orgu Konduktor'e ->
SABAH: Karakopru (tas kopru, Eli), Degirmen (yel degirmeni, Ren ve kardesi), Yedigol (Ada, biten orgu), ev -> gece treni -> gisede yeni yolcu -> kapanis.
Yeni mekanlar: lokomotif (yandan ve on camdan), ev (gece ve sabah), gise, Son Durak peronu (acilan kapi), uc istasyonun sabahi.
Yeni gorsel fikirler: duvar mikrofonu, anahtar ve acilan kilit, yol tablosu, bilete elle yazilan EV, delen zimba, sabah isigi, biten orgu."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import *
import ortak
from senaryo import ABONE, ABONE_END, MIC, UNLOCK, SLAM, SLIP, WRITE, PUNCH, BRAKE, HALT, DOOR, HUG, HOME, NEW

V = FMT == 'v'
QW = (540, 1060) if V else (540, 1000)                     # genis planlarda sahnenin oturdugu yer
QC = (540, 1000) if V else (540, 1010)                     # yakin planlarda
RED, GREEN, INK = (255, 110, 96), (96, 200, 130), (44, 50, 110)
WOOD = (190, 132, 78)
IRON, IRON2 = (54, 68, 84), (36, 46, 60)
ORANGE = (250, 146, 76)
KS_ = sorted(TL.scenes)
END0 = TL.span(33)[0]
HK = TL.span(2)[0]                                         # kancadan disari plana kesme ani
BIG = LTRB(-3000, -3000, 5000, 5000)
X0, X1 = -560, 1640
CAST['K'] = dict(x=0, gy=NEAR, s=0.52, c=ORANGE, seed=43, head=1.25)   # Ren'in kardesi (montaj)
CAST['Y'] = dict(x=0, gy=NEAR, s=0.70, c=LILAC, seed=47, head=1.2)     # gisedeki yeni yolcu (son sahne)

# ---------- pozlar ----------
SHOWB = dict(aR=(150, 70, 196, -40))                        # elindekini yuzunun yaninda gosterir (buyuk kafa)
FWD = dict(aR=(110, 70, 214, 50))                           # sag elini ileri (saga) uzatir
BACKP = dict(aL=(-120, 40, -206, -16))                      # solu gosterir
LANTUP = dict(aL=(-130, 50, -210, 0))                       # feneri sola kaldirir
GIVEL = dict(aL=(-110, 80, -204, 26))                       # sol eliyle sola uzatir
OPENR = dict(aR=(120, 90, 200, 120))                        # sag eli acik, anlatir
CHEST = dict(aL=(-70, 110, -12, 160), aR=(70, 110, 12, 160))
SALUTE = dict(aR=(150, -40, 104, -236))                     # eli kasketin siperliginde
WAVE = dict(aR=(130, 0, 170, -150))


# ---------- trenin aldigi yol ----------
SPEED = {17: 320, 18: 320, 19: 300, 20: 280, 21: 260, 22: 240, 23: 200, 24: 0, 25: 0, 26: 0, 27: 0}
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


def ftext(cv, s, x, y, size, c, maxw, a=255):
    """genislige sigdirilan ortali yazi"""
    f = skia.Font(TFB, size); w = f.measureText(s)
    if w > maxw: f.setSize(size * maxw / w); w = f.measureText(s)
    cv.drawString(s, x - w / 2, y + f.getSize() * 0.36, f, fill(c, a))


def title_card(cv, t):
    tb = B('title'); a = seg(t, tb[0], tb[0] + 0.35)
    if a > 0:
        dim(cv, 0.5 * a)
        card(cv, [(TITLE, 112, RED), (f'{EP.title()}: {EP_NAME}', 48, CREAM)], a, lerp(0.9, 1.0, smooth(seg(t, tb[0], tb[0] + 0.5))))


def check(cv, x, y, r, c=GREEN, a=1.0):
    p = skia.Path(); p.moveTo(x - r * 0.7, y); p.lineTo(x - r * 0.15, y + r * 0.55); p.lineTo(x + r * 0.8, y - r * 0.6)
    st = stroke((0, 0, 0), r * 0.62, 230 * a); st.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, st)
    st = stroke(c, r * 0.36, 255 * a); st.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, st)


def glow(cv, x, y, r, c, a=150, blur=None):
    p = fill(c, a); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur or r * 0.5)); cv.drawCircle(x, y, r, p)


def grain(cv):
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kSoftLight); p.setAlphaf(0.4); cv.drawImage(noise_img(), 0, 0, LIN, p)


def bubble(cv, x, y, txt, size=54, a=1.0, tail=-1, c=PAPER, tc=(150, 40, 46)):
    """konusma balonu (sahne koordinati); (x, y): balonun ortasi. tail: kuyrugun yonu (-1 sol alt, 1 sag alt)"""
    if a <= 0: return
    f = skia.Font(TFB, size); w = f.measureText(txt); rc = LTRB(x - w / 2 - 34, y - size * 0.95, x + w / 2 + 34, y + size * 0.75)
    cv.saveLayerAlpha(BIG, int(255 * clamp(a)))
    cv.drawRRect(RRXY(rc.makeOffset(5, 8), 30, 30), fill((4, 6, 20), 110))
    poly(cv, [(x + tail * 40, rc.bottom() - 6), (x + tail * 96, rc.bottom() + 54), (x + tail * 90, rc.bottom() - 6)], c)
    cv.drawRRect(RRXY(rc, 30, 30), fill(c)); cv.drawRRect(RRXY(rc.makeInset(8, 8), 22, 22), dashed(tc, 2.5, 190, (10, 8)))
    cv.drawString(txt, x - w / 2, y + size * 0.3, f, fill(tc)); cv.restore()


# ---------- Mia'nin ve Konduktor'un elindekiler ----------
def knit_piece(cv, x, y, s, a=1.0):
    """elden sarkan yarim orgu (kucuk)"""
    A = 255 * a
    poly(cv, [(x - 36 * s, y), (x + 36 * s, y - 5 * s), (x + 32 * s, y + 88 * s), (x - 32 * s, y + 92 * s)], CREAM, A)
    for j in range(1, 4): cv.drawLine(x - 29 * s, y + j * 23 * s, x + 29 * s, y - 4 * s + j * 23 * s, dashed(CORAL, 4 * s, 225 * a, (8 * s, 6 * s)))
    cv.drawLine(x - 56 * s, y + 3 * s, x + 58 * s, y - 11 * s, stroke((70, 64, 84), 8 * s, A)); cv.drawLine(x - 56 * s, y + 3 * s, x + 58 * s, y - 11 * s, stroke((150, 142, 166), 5 * s, A))


def paper(cv, x, y, s, a=1.0, rot=-8, w=70, h=92):
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


def prop_carry(cv, f, s, a): u = s / 0.7; knit_piece(cv, f['handL'][0], f['handL'][1] + 12 * s, u, a); paper(cv, f['handL'][0] - 6 * s, f['handL'][1] - 34 * s, u, a, rot=-14)
def _tk(cv, f, s, a, side='R', rot=-10): h = f['hand' + side]; mini_ticket(cv, h[0] + 8 * s, h[1] - 30 * s, s / 0.7 * 1.25, a, rot=rot, c=MUSTARD)
def prop_tk(cv, f, s, a): prop_carry(cv, f, s, a); _tk(cv, f, s, a)
def prop_tko(cv, f, s, a): _tk(cv, f, s, a)                 # yalniz bilet
def prop_pen(cv, f, s, a):
    u = s / 0.7; prop_carry(cv, f, s, a); hx, hy = f['handR']
    mini_ticket(cv, f['handL'][0] + 60 * s, f['handL'][1] - 70 * s, u * 1.3, a, rot=6, c=MUSTARD)
    pencil(cv, hx - 30 * u, hy + 44 * u, 100 * u, -62, th=14 * u, a=a); hand_ball(cv, hx, hy, 33 * s, MUSTARD, seed=4)
def prop_lt(cv, f, s, a): ortak.prop_lantern(cv, f, s, a); mini_ticket(cv, f['handR'][0] - 4 * s, f['handR'][1] - 34 * s, s / 0.74 * 1.35, a, rot=8, c=MUSTARD)
def prop_lk(cv, f, s, a): ortak.prop_lantern(cv, f, s, a); knit_piece(cv, f['handR'][0], f['handR'][1] + 12 * s, s / 0.7, a)
ortak.PROPS.update(carry=prop_carry, tk=prop_tk, tko=prop_tko, pen=prop_pen, lt=prop_lt, lk=prop_lk)


def cast_at(cv, ts, st, extra=None):
    """st: {kim: ((x, gy, s), (ifade, poz, bakis[, ek]))}"""
    with stage(cv):
        f = people(cv, ts, {w: v[0] for w, v in st.items()}, {w: v[1] for w, v in st.items()})
        if extra: extra(f)
    return f


# ---------- portre: nakis kasnagi (Ada'nin sozu hatirlanir) ----------
def portrait(cv, ts, who, cx, cy, r, a=1.0, expr='sakin', prop=None, look=0.0, label=None):
    if a <= 0.01: return
    cv.saveLayerAlpha(BIG, int(255 * clamp(a)))
    sh = fill((4, 6, 20), 130); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14)); cv.drawCircle(cx + 6, cy + 12, r * 1.08, sh)
    cv.drawCircle(cx, cy, r, fill(CREAM))
    cv.save(); cp = skia.Path(); cp.addCircle(cx, cy, r); cv.clipPath(cp, True)
    for j in range(-7, 8): cv.drawLine(cx - r, cy + j * r / 7, cx + r, cy + j * r / 7, dashed(shade(CREAM, 0.84), max(1.5, r * 0.012), 130, (8, 7)))
    c_ = CAST[who]; s = r / 318.0; HR = 118 * s * c_.get('head', 1.0); gy = cy - r * 0.02 + HR * 0.88 + 520 * s
    actor(cv, ts, who, expr, dict(KNIT) if prop == 'knit' else {}, look, place=(cx, gy, s), prop=prop)
    cv.restore()
    cv.drawCircle(cx, cy, r, stroke(shade(WOOD, 0.7), r * 0.13)); cv.drawCircle(cx, cy, r, stroke(WOOD, r * 0.09)); cv.drawCircle(cx, cy, r, dashed(shade(WOOD, 1.3), max(1.5, r * 0.014), 170, (10, 8)))
    cv.drawRRect(RRXY(LTRB(cx - r * 0.1, cy - r * 1.2, cx + r * 0.1, cy - r * 1.02), 4, 4), fill(BRASS)); cv.drawCircle(cx, cy - r * 1.22, r * 0.07, fill(shade(BRASS, 0.7)))
    if label:
        fs = r * 0.26; f = skia.Font(TFM, fs); f.setSkewX(-0.2); w = f.measureText(label); y0 = cy + r * 1.14
        rc = LTRB(cx - w / 2 - fs * 0.8, y0, cx + w / 2 + fs * 0.8, y0 + fs * 1.9)
        cv.drawRRect(RRXY(rc.makeOffset(3, 5), 6, 6), fill((4, 6, 20), 110)); cv.drawRRect(RRXY(rc, 6, 6), fill((252, 246, 228))); cv.drawString(label, cx - w / 2, y0 + fs * 1.3, f, fill(INK))
    cv.restore()


# ---------- madalyonlar (ekran koordinati): inen yolcular ----------
def medals(cv, k, items, al, ok=1.0, y=None, r=None):
    """items: [(renk, ad)]; al: gorunurluk listesi; ok 0..1: onay isareti"""
    n = len(items); r = r or ((56 if n < 4 else 50) if V else 50); y = y if y is not None else (470 if V else 200)
    gap = (290 if n < 4 else 240) if V else 250; x0 = W / 2 - gap * (n - 1) / 2
    for j, ((c_, nm), a) in enumerate(zip(items, al)):
        if a <= 0: continue
        x, yy = x0 + j * gap, y + 16 * (1 - a)
        hand_ball(cv, x, yy, r, c_, seed=3 + j)
        otext(cv, nm, x, yy + r + 50, 40 if V else 34, CREAM, a=a)
        if ok > 0: check(cv, x + 4, yy, r * 0.62 * lerp(1.4, 1.0, smooth(seg(ok, 0.0, 0.6))), a=a * seg(ok, 0.0, 0.3))
TRIO = ((SKYB, 'ELI'), (GREENC, 'REN'), (ROSE, 'ADA'))


# ---------- disaridan: tren ----------
def ext(cv, ts, k, xr, n, heads=None, sc=None, fog_a=0.6, moon=None):
    u, y = (1.0, 1130) if V else (1.5, 1150)
    with stage(cv):
        ext_bg(cv, SC(ts) if sc is None else sc, k, y=y + 21 * u - 22, moon=moon or ((800, 520) if V else (1180, 620)), fog_a=fog_a)
        mid = train_ext(cv, xr, y, u, n, k, heads=heads or {})
    return mid, y, u


# ---------- bir numaranin onu: lokomotif kapisi, hoparlor, duvar mikrofonu ----------
CAMF = 1700
MIAF, CONF = (330, NEAR, 0.70), (590, NEAR, 0.74)
MICX, MICY = 716, 900
def mic_box(cv, on=False, k=0):
    """duvardaki pirinc anons mikrofonu: huni sola bakar, dugmeye basilinca kirmizi lamba yanar"""
    rc = LTRB(MICX - 34, MICY - 60, MICX + 34, MICY + 60)
    cv.drawRRect(RRXY(rc.makeOffset(4, 6), 10, 10), fill((4, 6, 20), 90))
    cv.drawRRect(RRXY(rc, 10, 10), fill((30, 34, 48))); cv.drawRRect(RRXY(rc.makeInset(6, 6), 6, 6), dashed((110, 120, 150), 2, 190, (7, 6)))
    poly(cv, [(MICX - 4, MICY - 34), (MICX - 4, MICY - 10), (MICX - 64, MICY + 6), (MICX - 64, MICY - 50)], BRASS)
    cv.drawOval(LTRB(MICX - 76, MICY - 52, MICX - 54, MICY + 8), fill(shade(BRASS, 0.55))); cv.drawOval(LTRB(MICX - 76, MICY - 52, MICX - 54, MICY + 8), stroke(BRASS, 4))
    if on: glow(cv, MICX + 8, MICY + 30, 30, REDL, 170 * (1.0 if (k // 3) % 2 else 0.6))
    cv.drawCircle(MICX + 8, MICY + 30, 12, fill(REDL if on else (110, 50, 52))); cv.drawCircle(MICX + 8, MICY + 30, 12, stroke((20, 24, 36), 3))
    cv.drawLine(MICX, MICY - 60, MICX - 40, 640, stroke((20, 24, 36), 4, cap=False))            # kablo hoparlore gider


def wf(cv, ts, k, st, extra=None, mic_on=False, **kw):
    wagon(cv, CAMF, 1, k, scroll=SC(ts), last=True, **kw)
    with stage(cv):
        loco_door(cv, CAMF, k); mic_box(cv, mic_on, k)
    return cast_at(cv, ts, st, extra)
def zM(z=1.5): return (z if V else z + 0.05, (MIAF[0], 950), QC)
def zC(z=1.5): return (z if V else z + 0.05, (CONF[0] - 10, 930), QC)
def z2(z=1.2): return (z if V else z + 0.05, ((MIAF[0] + CONF[0]) / 2, 960), (540, 1010))


# ---------- lokomotif (yandan kesit): bos makinist koltugu, kendi kendine oynayan kollar, ocak, yol tablosu ----------
SEATX = 668
CONC, MIAC = (200, NEAR, 0.74), (440, NEAR, 0.70)
def cab(cv, k, scroll=0.0, ghost=0.0):
    cv.clear(col((8, 12, 24)))
    with stage(cv):
        night(cv, scroll, k); track(cv, scroll)
        a0, a1 = -620, 1064
        cv.drawRRect(RRXY(LTRB(1060, 730, 1900, FEDGE + 44), 70, 70), fill((30, 62, 72)))          # kazan (yalniz yatayda gorunur)
        for bx in (1190, 1400): cv.drawRect(LTRB(bx, 730, bx + 24, FEDGE + 44), fill(BRASS, 220))
        cv.drawRect(LTRB(1280, 560, 1356, 740), fill((18, 24, 36))); cv.drawRect(LTRB(1268, 540, 1368, 574), fill((18, 24, 36)))
        for i in range(5):
            ph = ((k * 0.5 + i * 4) % 20) / 20.0
            cv.drawCircle(1318 - ph * 420, 520 - ph * 90, 34 + 60 * ph, fill((214, 220, 236), 130 * (1 - ph)))
        gl = skia.Path(); gl.moveTo(1500, 800); gl.lineTo(1500, 1000); gl.lineTo(1700, 1200); gl.lineTo(1700, 700); gl.close(); cv.drawPath(gl, fill((255, 236, 170), 30))
        cv.drawRRect(RRXY(LTRB(a0 - 14, ROOF - 46, a1 + 30, CEIL), 40, 40), fill((24, 34, 48)))
        cv.drawRect(LTRB(a0, CEIL, a1, WF), fill(IRON))
        for px in range(a0 + 40, a1, 220): cv.drawLine(px, CEIL + 16, px, 1030, dashed(shade(IRON, 1.5), 5, 150, (5, 26)))   # percinler
        cv.drawRect(LTRB(a0, 1040, a1, WF), fill(IRON2)); cv.drawLine(a0, 1052, a1, 1052, dashed(shade(IRON2, 1.9), 4, 190, (18, 14)))
        cv.drawRect(LTRB(a0, WF - 40, a1, WF), fill(shade(IRON2, 0.72)))
        cv.drawLine(a0, CEIL - 8, a1, CEIL - 8, dashed((70, 90, 110), 3, 170, (16, 12)))
        cv.drawRect(LTRB(a1 - 22, CEIL, a1 + 18, WF), fill((26, 34, 46)))                         # on duvar ve on cam (kesit)
        cv.drawRRect(RRXY(LTRB(a1 - 16, 664, a1 + 12, 900), 8, 8), fill((14, 22, 50))); cv.drawRRect(RRXY(LTRB(a1 - 16, 664, a1 + 12, 900), 8, 8), stroke(BRASS, 5))
        cv.drawLine(250, 592, a1 - 30, 592, stroke((92, 100, 120), 16, cap=False))                 # borular
        for jx in (430, 800, 960): cv.drawRect(LTRB(jx - 11, 577, jx + 11, 607), fill(BRASS))
        cv.drawLine(1000, 592, 1000, 1000, stroke((92, 100, 120), 14, cap=False))
        # vagona acilan kapi (acik, isikli)
        d0, d1 = 20, 200
        cv.drawRect(LTRB(d0 - 16, 640, d1 + 16, WF), fill((26, 34, 46))); cv.drawRect(LTRB(d0, 656, d1, WF), fill(LAMPC))
        cv.drawRect(LTRB(d0 + 12, 668, d1 - 12, WF + 20), dashed((214, 180, 96), 3, 220)); cv.drawRect(LTRB(d1 - 16, 656, d1, WF), fill((98, 62, 52)))
        poly(cv, [(d0, WF), (d1, WF), (d1 + 90, FEDGE), (d0 - 90, FEDGE)], LAMPC, 50)
        plate(cv, 110, 600, 'VAGON 1', 0.0, k, sc_=0.78)
        # yol tablosu (duvarda, kucuk)
        rb = LTRB(270, 668, 520, 912)
        cv.drawRRect(RRXY(rb, 14, 14), fill((22, 26, 40))); cv.drawRRect(RRXY(rb, 14, 14), stroke(BRASS, 8))
        text(cv, 'YOL TABLOSU', rb.centerX(), rb.top() + 42, 25, AMBER)
        for j in range(6):
            yy = rb.top() + 78 + j * 28; last = j == 5; on_ = (not last) or (k // 3) % 2 == 0
            if last and on_: glow(cv, rb.left() + 36, yy, 20, REDL, 150)
            cv.drawCircle(rb.left() + 36, yy, 8.5, fill((REDL if last else (120, 220, 150)) if on_ else (70, 40, 44)))
            cv.drawRect(LTRB(rb.left() + 60, yy - 6, rb.right() - 34 - (j * 17) % 50, yy + 6), fill((120, 60, 64) if last else (92, 100, 134)))
        for j, gx in enumerate((800, 880, 960)):                                                   # gostergeler
            gy_ = 690 + 36 * (j % 2); cv.drawCircle(gx, gy_, 36, fill(BRASS)); cv.drawCircle(gx, gy_, 27, fill((240, 232, 210)))
            a_ = -0.7 + 0.5 * math.sin(k * 0.3 + j * 2.1); cv.drawLine(gx, gy_, gx + math.sin(a_) * 22, gy_ - math.cos(a_) * 22, stroke((170, 40, 40), 4))
        # makinist koltugu: tepesinde lamba, altinda bos koltuk
        plate(cv, SEATX, 640, 'MAKİNİST', 0.0, k, sc_=0.8)
        poly(cv, [(SEATX - 46, CEIL + 30), (SEATX + 46, CEIL + 30), (SEATX + 210, WF), (SEATX - 210, WF)], LAMPC, 40)
        cv.drawRRect(RRXY(LTRB(SEATX - 58, CEIL - 4, SEATX + 58, CEIL + 30), 15, 15), fill(LAMPC))
        cv.drawOval(LTRB(SEATX - 100, WF - 22, SEATX + 100, WF + 14), fill((40, 46, 60)))
        cv.drawRect(LTRB(SEATX - 16, 1120, SEATX + 16, WF), fill((70, 76, 96)))
        cv.drawRRect(RRXY(LTRB(SEATX - 130, 770, SEATX - 62, 1110), 28, 28), fill(shade(SEATC, 1.2))); cv.drawRRect(RRXY(LTRB(SEATX - 120, 786, SEATX - 72, 890), 14, 14), fill(CREAM, 240))
        cv.drawRRect(RRXY(LTRB(SEATX - 120, 900, SEATX - 72, 1096), 14, 14), dashed(shade(SEATC, 1.9), 3, 190, (10, 8)))
        cv.drawRRect(RRXY(LTRB(SEATX - 130, 1070, SEATX + 116, 1134), 24, 24), fill(shade(SEATC, 1.36)))
        cv.drawLine(SEATX - 106, 1102, SEATX + 96, 1102, dashed(shade(SEATC, 2.0), 3, 190, (10, 8)))
        cv.drawLine(SEATX - 70, 1000, SEATX + 80, 1000, stroke((70, 76, 96), 13))                 # kolcak
        if ghost > 0:                                                                              # olmayan makinist: kesik cizgili bos yer
            on_ = (k // 3) % 2 == 0
            cv.drawCircle(SEATX + 6, 900, 78, dashed(CREAM, 6, 235 * ghost, (16, 12))); ftext(cv, '?', SEATX + 6, 900, 110, RED if on_ else CREAM, 200, 255 * ghost)
            cv.drawRRect(RRXY(LTRB(SEATX - 50, 986, SEATX + 62, 1072), 24, 24), dashed(CREAM, 6, 235 * ghost, (16, 12)))
        # kumanda: kollar kendi kendine oynar
        cv.drawRRect(RRXY(LTRB(806, 1040, 950, WF), 10, 10), fill((40, 48, 64))); cv.drawRRect(RRXY(LTRB(816, 1050, 940, WF - 10), 6, 6), dashed((110, 120, 150), 2.5, 190, (9, 7)))
        for j, lx in enumerate((842, 906)):
            a_ = (-0.34, 0.28)[j] + 0.2 * math.sin(k * 0.26 + j * 1.9)
            tx_, ty_ = lx + math.sin(a_) * 132, 1050 - math.cos(a_) * 132
            cv.drawLine(lx, 1050, tx_, ty_, stroke((150, 156, 176), 11)); cv.drawCircle(tx_, ty_, 17, fill(REDS)); cv.drawCircle(lx, 1050, 12, fill(BRASS))
        # ocak (onde, altta)
        fl = 0.75 + 0.25 * math.sin(k * 0.9) * math.sin(k * 0.37)
        glow(cv, 1010, 1150, 150, (255, 130, 50), 150 * fl, 60)
        cv.drawRRect(RRXY(LTRB(968, 1076, 1040, 1204), 12, 12), fill((30, 30, 40))); cv.drawRRect(RRXY(LTRB(980, 1092, 1030, 1190), 8, 8), fill((255, 190, 90), 255 * fl))
        for j in range(1, 4): cv.drawLine(980, 1092 + j * 24.5, 1030, 1092 + j * 24.5, stroke((30, 30, 40), 6, cap=False))
        # zemin (sac) ve tekerler
        cv.drawRect(LTRB(a0, WF, a1 + 18, FEDGE), fill((56, 60, 76))); cv.drawRect(LTRB(a0, WF + 36, a1 + 18, FEDGE - 24), fill((72, 78, 98)))
        for yy in (WF + 47, FEDGE - 35): cv.drawLine(a0, yy, a1, yy, dashed((124, 132, 156), 3.5, 190, (16, 12)))
        poly(cv, [(900, WF), (1064, WF), (1064, FEDGE), (780, FEDGE)], (255, 140, 60), 46 * fl)
        cv.drawRect(LTRB(a0, FEDGE, a1 + 40, FEDGE + 64), fill((26, 30, 42))); cv.drawLine(a0, FEDGE + 10, a1, FEDGE + 10, dashed((90, 100, 124), 3, 170, (14, 10)))
        ph = scroll / 92.0
        for wx in (200, 540, 880):
            cv.drawCircle(wx, 1506, 96, fill((150, 50, 56))); cv.drawCircle(wx, 1506, 78, fill((30, 32, 44))); cv.drawCircle(wx, 1506, 78, stroke((150, 50, 56), 6))
            for j in range(6): cv.drawLine(wx, 1506, wx + math.cos(ph + j * math.pi / 3) * 76, 1506 + math.sin(ph + j * math.pi / 3) * 76, stroke((150, 50, 56), 7))
            cv.drawCircle(wx, 1506, 18, fill(BRASS))
        cv.drawLine(200 + math.cos(ph) * 50, 1506 + math.sin(ph) * 50, 880 + math.cos(ph) * 50, 1506 + math.sin(ph) * 50, stroke((200, 204, 220), 12))
    grain(cv)
def cabp(cv, ts, k, st, extra=None, ghost=0.0):
    cab(cv, k, SC(ts), ghost); return cast_at(cv, ts, st, extra)
def zMc(z=1.5): return (z if V else z + 0.05, (MIAC[0], 950), QC)
def zCc(z=1.5): return (z if V else z + 0.05, (CONC[0] + 30, 930), QC)
def z2c(z=1.22): return (z if V else z + 0.05, ((MIAC[0] + CONC[0]) / 2 + 10, 960), (540, 1010))


# ---------- lokomotifin on cami (iceriden, ileri bakis): ray karanliga gider; near 0..1: Son Durak'in isiklari yaklasir ----------
def front_view(cv, k, scroll, near=0.0):
    cv.clear(col((4, 6, 16)))
    with stage(cv):
        vx, vy = 540, 930
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 420), skia.Point(0, vy)], [col((4, 6, 16)), col((24, 38, 78))]))
        cv.drawRect(LTRB(X0, -400, X1, vy), g)
        for sx, sy, r in ortak._STARS[:30]: cv.drawCircle((sx * 0.9) % 2100 - 500, 430 + sy * 0.62, r * 0.9, fill((236, 232, 210), 170))
        cv.drawRect(LTRB(X0, vy, X1, 2600), fill((9, 12, 26)))
        poly(cv, [(vx - 30, vy + 70), (vx + 30, vy + 70), (vx + 560, 1560), (vx - 560, 1560)], (255, 236, 170), 64)   # far isigi yalniz yakini aydinlatir
        for j in range(11):
            f = (((j + scroll / 110.0) % 11) / 11.0) ** 2
            y = lerp(vy, 1560, f); hw = lerp(6, 470, f)
            cv.drawLine(vx - hw, y, vx + hw, y, stroke((96, 80, 80), 2 + 20 * f, 255 * clamp(f * 3.5), cap=False))
        for sd in (-1, 1): cv.drawLine(vx + sd * 4, vy, vx + sd * 380, 1560, stroke((160, 168, 190), 8))
        dk = fill((3, 4, 12), 250 * (1 - 0.85 * near)); dk.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 50))
        cv.drawOval(LTRB(vx - 620, vy - 170, vx + 620, vy + 110), dk)                             # ufuk: karanlik
        if near > 0:                                                                              # Son Durak: rayin saginda peron, lambalar, tabela
            s_ = lerp(0.10, 1.0, near ** 1.7); A = 255 * clamp(near * 3)
            poly(cv, [(vx + 30 * s_, vy + 8 * s_), (vx + 520 * s_, vy + 8 * s_), (vx + 900 * s_, vy + 110 * s_), (vx + 70 * s_, vy + 110 * s_)], (74, 76, 92), A)
            cv.drawRect(LTRB(vx + 60 * s_, vy - 330 * s_, vx + 700 * s_, vy - 290 * s_), fill((16, 20, 34), A))
            for j in range(4):
                px, py = vx + (110 + j * 150) * s_, vy - 280 * s_
                glow(cv, px, py + 10 * s_, 70 * s_ + 8, LAMPC, 150 * clamp(near * 3), 30 * s_ + 4); cv.drawCircle(px, py, 13 * s_ + 2, fill((255, 246, 214), A))
                cv.drawLine(px, py, px, vy + 8 * s_, stroke((14, 18, 30), 5 * s_ + 1, A, cap=False))
            rc = LTRB(vx + 150 * s_, vy - 240 * s_, vx + 570 * s_, vy - 130 * s_)
            cv.drawRRect(RRXY(rc, 12 * s_, 12 * s_), fill(PAPER, A))
            if s_ > 0.2: ftext(cv, 'SON DURAK', rc.centerX(), rc.centerY(), 70 * s_, (150, 40, 46), rc.width() - 30 * s_, A)
        # on camin cercevesi ve gosterge paneli
        pane = LTRB(36, 560, 1044, 1236) if V else LTRB(-360, 520, 1440, 1236)
        fr = skia.Path(); fr.addRect(LTRB(X0, -400, X1, 2600)); fr.addRRect(RRXY(pane, 46, 46)); fr.setFillType(skia.PathFillType.kEvenOdd); cv.drawPath(fr, fill(IRON))
        cv.drawRRect(RRXY(pane, 46, 46), stroke(BRASS, 12)); cv.drawRRect(RRXY(pane.makeOutset(26, 26), 60, 60), dashed(shade(IRON, 1.7), 6, 220, (6, 26)))
        if not V:
            for xx in (-40, 1120): cv.drawLine(xx, pane.top(), xx, pane.bottom(), stroke(BRASS, 10, cap=False))
        cv.drawLine(pane.left() + 60, pane.top() + 150, pane.left() + 170, pane.top() + 40, stroke((255, 255, 255), 9, 30))
        cv.drawRect(LTRB(X0, 1262, X1, 2600), fill((30, 38, 52))); cv.drawLine(X0, 1280, X1, 1280, dashed((110, 120, 150), 4, 190, (18, 14)))
        for j, gx in enumerate(range(-320, 1500, 215)):
            cv.drawCircle(gx, 1370, 54, fill(BRASS)); cv.drawCircle(gx, 1370, 42, fill((240, 232, 210)))
            a_ = -0.7 + 0.5 * math.sin(k * 0.3 + j * 2.1); cv.drawLine(gx, 1370, gx + math.sin(a_) * 34, 1370 - math.cos(a_) * 34, stroke((170, 40, 40), 5))
    grain(cv)


# ---------- yol tablosu (ekran koordinati): bes durak ve bir bos bilet ----------
STOPS = (('KARAKÖPRÜ', SKYB), ('DEĞİRMEN', GREENC), ('YEDİGÖL', ROSE), ('SARNIÇ', None), ('SON DURAK', CNAVY))
def route_board(cv, k, lit, blank=0.0, never=0.0):
    """lit: yanan durak sayisi (0..5, ondalikli); blank 0..1: Mia'nin bos bileti; never 0..1: 'HIC DURMAZ'"""
    if V: pts = [(540, 385 + j * 116) for j in range(6)]; fs, bw = 54, 760
    else: pts = [(600 + (j // 3) * 720, 330 + (j % 3) * 150) for j in range(6)]; fs, bw = 50, 620
    hh = fs * 0.95
    otext(cv, 'YOL TABLOSU', W / 2, (286 if V else 176), 54 if V else 50, AMBER)
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]): cv.drawLine(xa, ya, xb, yb, stroke((0, 0, 0), 20, 200))
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]): cv.drawLine(xa, ya, xb, yb, stroke((150, 158, 180), 9))
    for j, (x, y) in enumerate(pts):
        last = j == 5; a = clamp(lit - j) if not last else blank
        rc = LTRB(x - bw / 2, y - hh, x + bw / 2, y + hh)
        cv.drawRRect(RRXY(rc.makeOffset(4, 6), 10, 10), fill((4, 6, 20), 140))
        if last:
            on_ = blank > 0 and (k // 3) % 2 == 0
            cv.drawRRect(RRXY(rc, 10, 10), fill(lerpt((40, 44, 60), (120, 36, 44), blank))); cv.drawRRect(RRXY(rc.makeInset(6, 6), 6, 6), dashed(RED, 3.5, 240, (12, 9)))
            if blank > 0:
                hand_ball(cv, rc.left() + hh * 1.05, y, hh * 0.62, MUSTARD, seed=9)
                if never > 0: ftext(cv, 'HİÇ DURMAZ', x + hh * 0.5, y, fs, YEL if on_ else CREAM, bw - hh * 3.2, 255)
                else: ftext(cv, 'MIA: ?' if on_ else 'MIA:', x + hh * 0.4, y, fs, CREAM, bw - hh * 3, 255 * blank)
        else:
            nm, c_ = STOPS[j]
            cv.drawRRect(RRXY(rc, 10, 10), fill(lerpt((150, 146, 140), PAPER, a))); cv.drawRRect(RRXY(rc.makeInset(6, 6), 6, 6), dashed((150, 40, 46), 2.5, 220, (10, 8)))
            ftext(cv, nm, x + (hh * 0.2 if c_ else 0) - hh * 0.3, y, fs, (150, 40, 46), bw - hh * 4.2)
            if c_: hand_ball(cv, rc.left() + hh * 1.05, y, hh * 0.62, c_, seed=3 + j)
            if a > 0: check(cv, rc.right() - hh * 0.95, y, hh * 0.44 * lerp(1.5, 1.0, a), (40, 150, 90), a=a)


# ---------- ev (geri donus: gece; son: sabah) ----------
def figure_sil(cv, x, y, s, c, a=255, arms=0.0):
    """bekleyen biri: yalniz golge (anne). (x, y): omuz ortasi"""
    cv.drawCircle(x, y - 58 * s, 46 * s, fill(c, a))
    cv.drawOval(LTRB(x - 54 * s, y - 112 * s, x + 54 * s, y - 40 * s), fill(c, a))                # sac
    cv.drawCircle(x + 2 * s, y - 118 * s, 22 * s, fill(c, a))                                     # topuz
    poly(cv, [(x - 60 * s, y - 14 * s), (x + 60 * s, y - 14 * s), (x + 96 * s, y + 420 * s), (x - 96 * s, y + 420 * s)], c, a)
    if arms > 0:
        for sd in (-1, 1): cv.drawLine(x + sd * 50 * s, y + 10 * s, x + sd * (60 + 80 * arms) * s, y + (130 - 110 * arms) * s, stroke(c, 34 * s, a))


def morning_sky(cv, k, y_h=930, sun=(800, 690)):
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, y_h)], [col((104, 158, 216)), col((255, 208, 164))]))
    cv.drawRect(LTRB(X0, -400, X1, y_h + 400), g)
    glow(cv, sun[0], sun[1], 260, (255, 240, 180), 130, 90); cv.drawCircle(sun[0], sun[1], 74, fill((255, 246, 214)))
    for i in range(5):
        x = X0 + ((i * 520 + k * 1.2) % (X1 - X0 + 400)) - 200; y = 240 + (i * 97) % 330
        p = fill((255, 250, 240), 150); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22)); cv.drawOval(LTRB(x - 150, y - 34, x + 150, y + 34), p)
    for par, yb, hh, c_ in ((0, y_h, 170, (150, 176, 190)), (350, y_h + 30, 110, (124, 168, 140))):
        p = skia.Path(); x = X0 - 700 - par; p.moveTo(x, y_h + 600)
        while x < X1 + 700:
            p.lineTo(x, yb - 10); p.quadTo(x + 175, yb - hh, x + 350, yb - 20); p.quadTo(x + 525, yb - hh * 0.55, x + 700, yb - 10); x += 700
        p.lineTo(x, y_h + 600); p.close(); cv.drawPath(p, fill(c_))


def home(cv, k, morning=False, door_u=0.0, sil=1.0, arms=0.0, shake=(0, 0)):
    """evin onu: solda kapi, sagda mutfak penceresi (isigi yanar, camda bekleyen biri), kaldirim. door_u 0..1: kapi acik"""
    nc = (lambda c: c) if morning else (lambda c: (c[0] * 0.46, c[1] * 0.52, c[2] * 0.74))
    cv.clear(col((8, 12, 24)))
    with stage(cv, *shake):
        if morning: morning_sky(cv, k, sun=(900, 560) if V else (1250, 600))
        else: night(cv, 0, k, y_h=930, moon=(930, 380) if V else (1300, 600), poles=False)
        cv.drawRect(LTRB(X0, WF - 60, X1, 2600), fill(nc((118, 166, 104))))                        # cim
        for px in range(770, X1, 64):                                                              # cit
            poly(cv, [(px, 1100), (px + 17, 1076), (px + 34, 1100), (px + 34, WF), (px, WF)], nc((236, 226, 206)))
        cv.drawRect(LTRB(760, 1130, X1, 1146), fill(nc((206, 196, 176))))
        for px in range(X0, -300, 64): poly(cv, [(px, 1100), (px + 17, 1076), (px + 34, 1100), (px + 34, WF), (px, WF)], nc((236, 226, 206)))
        tx_ = 1260                                                                                  # agac
        cv.drawRect(LTRB(tx_ - 22, 880, tx_ + 22, WF), fill(nc((120, 84, 60))))
        for dx_, dy_, r in ((0, -140, 150), (-110, -60, 110), (110, -70, 120)): cv.drawCircle(tx_ + dx_, 880 + dy_, r, fill(nc((86, 150, 100))))
        h0, h1, ht = -280, 740, 610
        cv.drawRect(LTRB(h0, ht, h1, WF), fill(nc((226, 168, 140))))
        for yy in range(ht + 60, WF, 74): cv.drawLine(h0, yy, h1, yy, dashed(nc((190, 130, 110)), 3, 150, (40, 22)))
        poly(cv, [(h0 - 70, ht), (h1 + 70, ht), (h1 - 50, ht - 210), (h0 + 50, ht - 210)], nc((128, 54, 62)))
        for yy in (ht - 60, ht - 130): cv.drawLine(h0 - 20, yy, h1 + 20, yy, dashed(nc((180, 96, 100)), 3.5, 170, (20, 14)))
        cv.drawRect(LTRB(540, ht - 310, 620, ht - 170), fill(nc((150, 80, 76)))); cv.drawRect(LTRB(528, ht - 326, 632, ht - 300), fill(nc((110, 56, 58))))
        if morning:
            for i in range(4):
                ph = ((k * 0.35 + i * 5) % 20) / 20.0; cv.drawCircle(580 + ph * 110, ht - 340 - ph * 200, 24 + 50 * ph, fill((250, 246, 240), 150 * (1 - ph)))
        # mutfak penceresi: isik yaniyor
        w0, w1, wt, wb = 410, 690, 770, 1000
        glow(cv, (w0 + w1) / 2, (wt + wb) / 2, 250, (255, 214, 130), 110 if not morning else 60, 80)
        cv.drawRect(LTRB(w0, wt, w1, wb), fill((255, 228, 156)))
        cv.save(); cv.clipRect(LTRB(w0, wt, w1, wb))
        cv.drawRect(LTRB(w0, wb - 50, w1, wb), fill((214, 170, 110))); cv.drawCircle(w0 + 70, wb - 62, 22, fill((226, 120, 100))); cv.drawRect(LTRB(w1 - 110, wb - 96, w1 - 70, wb - 50), fill((120, 170, 190)))
        if sil > 0: figure_sil(cv, (w0 + w1) / 2 + 30, wt + 150, 0.9, (96, 58, 70), 255 * sil)
        for sd, xx in ((1, w0), (-1, w1)): poly(cv, [(xx, wt), (xx + sd * 84, wt), (xx + sd * 30, wt + 130), (xx, wt + 160)], REDS, 235)
        cv.restore()
        cv.drawRect(LTRB(w0, wt, w1, wb), stroke(nc(CREAM) if not morning else CREAM, 12, cap=False)); cv.drawLine((w0 + w1) / 2, wt, (w0 + w1) / 2, wb, stroke(nc(CREAM) if not morning else CREAM, 7, cap=False))
        cv.drawRRect(RRXY(LTRB(w0 - 20, wb + 6, w1 + 20, wb + 50), 8, 8), fill(nc((150, 96, 60))))
        for j in range(6): cv.drawCircle(w0 + 12 + j * 52, wb + 2, 20, fill(nc(((236, 108, 84), (244, 190, 80), (226, 132, 150))[j % 3])))
        poly(cv, [(w0 - 40, WF), (w1 + 40, WF), (w1 + 150, FEDGE + 30), (w0 - 150, FEDGE + 30)], (255, 226, 150), 40 if not morning else 0)   # isik kaldirima vurur
        # kapi
        d0, d1, dt = 100, 300, 790
        cv.drawRect(LTRB(d0 - 18, dt - 18, d1 + 18, WF), fill(nc((96, 60, 56))))
        cv.drawRect(LTRB(d0, dt, d1, WF), fill((255, 226, 150) if door_u > 0 else nc((40, 30, 40))))
        if door_u > 0.3:
            cv.save(); cv.clipRect(LTRB(d0, dt, d1, WF)); figure_sil(cv, (d0 + d1) / 2 + 20, dt + 150, 1.0, (120, 66, 84), 255 * seg(door_u, 0.3, 0.8), arms=arms); cv.restore()
            poly(cv, [(d0, WF), (d1, WF), (d1 + 130, FEDGE + 30), (d0 - 130, FEDGE + 30)], (255, 226, 150), 70 * door_u)
        w = (d1 - d0) * (1 - 0.9 * clamp(door_u))
        cv.drawRect(LTRB(d0, dt, d0 + w, WF), fill(nc((70, 120, 124))))
        if w > 80:
            cv.drawRect(LTRB(d0 + 16, dt + 16, d0 + w - 16, WF - 16), dashed(nc((150, 200, 196)), 3.5, 200))
            cv.drawRRect(RRXY(LTRB(d0 + w * 0.28, dt + 44, d0 + w * 0.72, dt + 150), 12, 12), fill(nc((255, 228, 156)) if morning else (150, 130, 100)))
            cv.drawCircle(d0 + w * 0.84, dt + 250, 12, fill(nc(BRASS)))
        cv.drawRRect(RRXY(LTRB(d0 - 50, WF - 16, d1 + 50, WF + 12), 6, 6), fill(nc((170, 170, 180))))
        lx_, ly_ = (d0 + d1) / 2, dt - 80                                                          # kapi lambasi
        if not morning: glow(cv, lx_, ly_ + 20, 110, LAMPC, 120, 40); poly(cv, [(lx_ - 26, ly_ + 30), (lx_ + 26, ly_ + 30), (lx_ + 190, WF), (lx_ - 190, WF)], LAMPC, 26)
        poly(cv, [(lx_ - 22, ly_), (lx_ + 22, ly_), (lx_ + 34, ly_ + 30), (lx_ - 34, ly_ + 30)], (20, 24, 34)); cv.drawOval(LTRB(lx_ - 22, ly_ + 22, lx_ + 22, ly_ + 40), fill(LAMPC if not morning else (226, 220, 200)))
        # kaldirim ve yol
        cv.drawRect(LTRB(X0, WF, X1, FEDGE + 30), fill(nc((206, 198, 180)))); cv.drawLine(X0, WF + 18, X1, WF + 18, dashed(nc((160, 152, 140)), 3.5, 190, (60, 14)))
        cv.drawRect(LTRB(X0, FEDGE + 30, X1, 2600), fill(nc((120, 122, 136)))); cv.drawLine(X0, FEDGE + 190, X1, FEDGE + 190, dashed(nc((236, 226, 206)), 8, 200, (60, 44)))
        if not morning:                                                                            # sokak lambasi
            sx_ = 990
            poly(cv, [(sx_ - 30, 650), (sx_ + 30, 650), (sx_ + 250, FEDGE + 30), (sx_ - 250, FEDGE + 30)], LAMPC, 28)
            cv.drawLine(sx_, 640, sx_, WF + 4, stroke((14, 18, 30), 12, cap=False)); poly(cv, [(sx_ - 24, 610), (sx_ + 24, 610), (sx_ + 44, 650), (sx_ - 44, 650)], (20, 24, 34))
            glow(cv, sx_, 660, 60, LAMPC, 170, 22); cv.drawOval(LTRB(sx_ - 30, 644, sx_ + 30, 664), fill(LAMPC))
    grain(cv)


# ---------- gise: istasyon salonu (geri donuste ve Son Durak'ta AYNI yer) ----------
def gise(cv, k, hours=22.92, sign=False, slip=0.0, spk=None):
    cv.clear(col((16, 22, 34)))
    with stage(cv):
        cv.drawRect(LTRB(X0, -400, X1, WF), fill((60, 96, 102)))
        for px in range(X0, X1, 190): cv.drawLine(px, 480, px, 1004, dashed((82, 122, 128), 3, 140, (14, 12)))
        cv.drawRect(LTRB(X0, 1010, X1, WF), fill(WAINS)); cv.drawLine(X0, 1022, X1, 1022, dashed(shade(WAINS, 1.5), 4, 190, (18, 14)))
        cv.drawRect(LTRB(X0, -400, X1, 470), fill((24, 34, 48))); cv.drawLine(X0, 462, X1, 462, dashed((70, 90, 110), 3.5, 170, (16, 12)))
        cv.drawRect(LTRB(X0, WF, X1, 2600), fill((92, 92, 108)))
        for j, px in enumerate(range(X0, X1, 160)):
            poly(cv, [(px, WF), (px + 160, WF), (540 + (px + 160 - 540) * 2.2, 2100), (540 + (px - 540) * 2.2, 2100)], (112, 110, 124) if j % 2 else (78, 80, 98))
        for yy, a_ in ((WF + 70, 60), (WF + 190, 90), (WF + 360, 120)): cv.drawRect(LTRB(X0, yy, X1, yy + 5), fill((30, 34, 50), a_))
        # gise penceresi
        g0, g1, gt, gb = 340, 740, 660, 1090
        lx_ = (g0 + g1) / 2
        poly(cv, [(lx_ - 40, 520), (lx_ + 40, 520), (lx_ + 330, WF + 30), (lx_ - 330, WF + 30)], LAMPC, 26)
        cv.drawRRect(RRXY(LTRB(g0 - 30, gt - 30, g1 + 30, gb + 36), 44, 44), fill((98, 62, 52))); cv.drawRRect(RRXY(LTRB(g0 - 16, gt - 16, g1 + 16, gb + 22), 36, 36), dashed((170, 120, 96), 3.5, 200))
        op = RRXY(LTRB(g0, gt, g1, gb), 30, 30)
        cv.drawRRect(op, fill((255, 228, 156)))
        cv.save(); cv.clipRRect(op, True)
        cv.drawRect(LTRB(g0, gt, g1, gt + 120), fill((226, 190, 120)))
        for j in range(5): cv.drawRect(LTRB(g0 + 30 + j * 76, gt + 150, g0 + 86 + j * 76, gt + 200), fill((236, 220, 180)))   # arkadaki bilet raflari
        hand_ball(cv, lx_, 884, 76, (120, 146, 180), seed=8)                                        # gisedeki adam (yuzu parmakligin ardinda)
        cv.drawRRect(RRXY(LTRB(lx_ - 78, 792, lx_ + 78, 846), 16, 16), fill((40, 52, 96))); cv.drawOval(LTRB(lx_ - 84, 832, lx_ + 84, 864), fill((20, 22, 34)))
        poly(cv, [(lx_ - 110, 960), (lx_ + 110, 960), (lx_ + 150, gb), (lx_ - 150, gb)], (86, 110, 150))
        for bx in range(g0 + 34, g1, 55): cv.drawLine(bx, gt, bx, 1000, stroke(BRASS, 9, cap=False))
        cv.drawRect(LTRB(g0, 994, g1, 1010), fill(shade(BRASS, 0.8)))
        cv.restore()
        cv.drawRRect(op, stroke(BRASS, 8))
        cv.drawRRect(RRXY(LTRB(g0 - 60, gb, g1 + 60, gb + 40), 12, 12), fill((150, 96, 60))); cv.drawLine(g0 - 40, gb + 20, g1 + 40, gb + 20, dashed((214, 170, 120), 3, 190, (12, 9)))
        if slip > 0: mini_ticket(cv, lx_ + 10, lerp(1040, 1100, slip), 1.9, clamp(slip * 3), rot=4, c=MUSTARD)
        rc = LTRB(lx_ - 150, 540, lx_ + 150, 626)
        cv.drawRRect(RRXY(rc.makeOffset(4, 7), 12, 12), fill((4, 6, 20), 110)); cv.drawRRect(RRXY(rc, 12, 12), fill(PAPER)); cv.drawRRect(RRXY(rc.makeInset(8, 8), 7, 7), dashed((150, 40, 46), 3, 220, (12, 9)))
        ftext(cv, 'GİŞE', lx_, rc.centerY(), 60, (150, 40, 46), 240)
        cv.drawLine(lx_, 470, lx_, 500, stroke((14, 18, 30), 6, cap=False)); poly(cv, [(lx_ - 26, 496), (lx_ + 26, 496), (lx_ + 48, 528), (lx_ - 48, 528)], (20, 24, 34)); cv.drawOval(LTRB(lx_ - 34, 520, lx_ + 34, 540), fill(LAMPC))
        # saat
        cx_, cy_ = 872, 650
        cv.drawCircle(cx_ + 4, cy_ + 8, 88, fill((4, 6, 20), 110)); cv.drawCircle(cx_, cy_, 86, fill(BRASS)); cv.drawCircle(cx_, cy_, 72, fill(PAPER))
        for j in range(12): cv.drawCircle(cx_ + math.sin(j * math.pi / 6) * 60, cy_ - math.cos(j * math.pi / 6) * 60, 4, fill((90, 78, 86)))
        hands(cv, cx_, cy_, hours, 1.02)
        # kalkis tablosu
        bd = LTRB(74, 600, 316, 830)
        cv.drawRRect(RRXY(bd, 14, 14), fill((22, 26, 40))); cv.drawRRect(RRXY(bd.makeInset(8, 8), 8, 8), dashed((110, 120, 150), 2.5, 200, (9, 7)))
        ftext(cv, 'İLK KALKAN', bd.centerX(), bd.top() + 46, 30, AMBER, 220); ftext(cv, 'GECE', bd.centerX(), bd.top() + 100, 38, CREAM, 220)
        ftext(cv, 'EKSPRESİ', bd.centerX(), bd.top() + 144, 38, CREAM, 220); ftext(cv, '23:00', bd.centerX(), bd.top() + 196, 44, AMBER, 220)
        if sign:                                                                                   # istasyonun adi
            rc = LTRB(712, 790, 986, 880)
            cv.drawRRect(RRXY(rc.makeOffset(4, 7), 12, 12), fill((4, 6, 20), 110)); cv.drawRRect(RRXY(rc, 12, 12), fill(PAPER)); cv.drawRRect(RRXY(rc.makeInset(8, 8), 7, 7), dashed((150, 40, 46), 3, 220, (12, 9)))
            ftext(cv, 'SON DURAK', rc.centerX(), rc.centerY(), 50, (150, 40, 46), 244)
        speaker(cv, 200, 530, spk, k)
        # yatayda yanlar: bank, afis
        for bx in (-250, 1290):
            cv.drawRRect(RRXY(LTRB(bx - 150, 1150, bx + 150, 1182), 10, 10), fill((50, 76, 84))); cv.drawRRect(RRXY(LTRB(bx - 150, 1060, bx + 150, 1126), 10, 10), fill((62, 92, 100)))
            for sd in (-1, 1): cv.drawRect(LTRB(bx + sd * 120 - 8, 1182, bx + sd * 120 + 8, WF + 30), fill((30, 44, 50)))
        ps = LTRB(1180, 620, 1400, 900)
        cv.drawRect(ps, fill(PAPER)); cv.drawRect(ps.makeInset(10, 10), dashed((150, 40, 46), 3, 220, (12, 9))); ftext(cv, 'GECE', ps.centerX(), ps.top() + 60, 40, (150, 40, 46), 180); ftext(cv, 'EKSPRESİ', ps.centerX(), ps.top() + 108, 40, (150, 40, 46), 180)
        ext_wagon(cv, ps.left() + 30, ps.bottom() - 50, 0.95, lit=1.0)
        psl = LTRB(-330, 620, -110, 900)
        cv.drawRect(psl, fill(PAPER)); cv.drawRect(psl.makeInset(10, 10), dashed((150, 40, 46), 3, 220, (12, 9))); ftext(cv, 'HER GECE', psl.centerX(), psl.top() + 70, 38, (150, 40, 46), 180); ftext(cv, '23:00', psl.centerX(), psl.top() + 150, 60, INKBLUE, 180)
    grain(cv)


# ---------- Son Durak peronu (disaridan): bir numara ve lokomotif; vagonun kapisi ilk kez acilir ----------
PU, PY, PX = 6.2, 1232, 30                                 # vagonun olcegi, alt cizgisi, sol ucu
DX0, DX1, DTOP, DBOT = PX + 68 * PU, PX + 98 * PU, PY - 96 * PU + 16 * PU, PY - 3 * PU
DOORC = ((DX0 + DX1) / 2, DBOT - 4, 0.50)                  # kapi araliginda duran oyuncunun yeri
def son_durak(cv, ts, k, tx=0.0, door_u=0.0, st=None, heads=None, extra=None):
    """tx: tren duracagi yerden ne kadar geride. door_u 0..1: kapi sola kayarak acilir. st: {kim: (yer, durum)}; kapidakiler kapi araligina kirpilir"""
    cv.clear(col((8, 12, 24)))
    st = st or {}
    with stage(cv):
        night(cv, 0, k, y_h=900, moon=(160, 500) if V else (-180, 620), poles=False)
        u, y = PU, PY; x0 = PX + tx
        track(cv, -tx, y=y + 62)
        ext_wagon(cv, x0, y, u, heads=heads if heads is not None else [None] * 5, num=1, k=k, tail=True)
        cv.drawRect(LTRB(x0 + 165 * u, y - 90, x0 + 165 * u + 64, y - 50), fill((18, 22, 32)))
        cv.save(); cv.clipRect(LTRB(X0, -400, 1560, 2600)); ext_loco(cv, x0 + 165 * u + 64, y, u, k); cv.restore()
        # kapi (vagonun ortasinda)
        d0, d1 = DX0 + tx, DX1 + tx
        cv.drawRRect(RRXY(LTRB(d0 - 14, DTOP - 14, d1 + 14, DBOT + 6), 12, 12), fill((40, 22, 30)))
        cv.drawRect(LTRB(d0, DTOP, d1, DBOT), fill(lerpt((60, 30, 40), (255, 228, 156), clamp(door_u * 1.6))))
        if door_u > 0:
            cv.save(); cv.clipRect(LTRB(d0 + (d1 - d0) * (1 - door_u) * 0.0, DTOP, d1, DBOT + 4))
            cv.drawRect(LTRB(d0, DBOT - 60, d1, DBOT), fill((150, 74, 84)))
            ins = {w: v for w, v in st.items() if v[0][2] <= DOORC[2] + 0.001}
            if ins: people(cv, ts, {w: v[0] for w, v in ins.items()}, {w: v[1] for w, v in ins.items()})
            cv.restore()
        w = (d1 - d0) * (1 - 0.94 * clamp(door_u))
        cv.drawRect(LTRB(d0, DTOP, d0 + w, DBOT), fill(shade(EXTC, 1.25)))
        if w > 60:
            cv.drawRect(LTRB(d0 + 12, DTOP + 12, d0 + w - 12, DBOT - 12), dashed(shade(EXTC, 1.9), 3, 200))
            cv.drawRRect(RRXY(LTRB(d0 + w * 0.2, DTOP + 40, d0 + w * 0.8, DTOP + 200), 12, 12), fill((250, 214, 120)))
            cv.drawRRect(RRXY(LTRB(d0 + w * 0.76, DTOP + 250, d0 + w * 0.9, DTOP + 330), 6, 6), fill(BRASS))
        if door_u > 0: poly(cv, [(d0, y + 96), (d1, y + 96), (d1 + 150, y + 330), (d0 - 150, y + 330)], (255, 226, 150), 80 * door_u)
        cv.drawRect(LTRB(X0, y + 96, X1, 2600), fill((74, 76, 92)))                                 # peron
        cv.drawRect(LTRB(X0, y + 96, X1, y + 122), fill((150, 150, 164)))
        cv.drawLine(X0, y + 160, X1, y + 160, dashed((232, 200, 110), 9, 230, (36, 24)))
        for px in range(X0, 1700, 220): cv.drawLine(px, y + 122, px - 60, 2000, stroke((60, 62, 78), 3, 120, cap=False))
        if door_u > 0: poly(cv, [(d0, y + 96), (d1, y + 96), (d1 + 170, y + 380), (d0 - 170, y + 380)], (255, 226, 150), 70 * door_u)
        cv.drawRRect(RRXY(LTRB(d0 - 24, y + 60, d1 + 24, y + 98), 6, 6), fill((120, 124, 140)))    # basamak
        cv.drawRect(LTRB(X0, 380, X1, 478), fill((16, 20, 34))); cv.drawLine(X0, 472, X1, 472, dashed((70, 84, 112), 3.5, 180, (18, 14)))   # sacak
        sx = 540
        for sd in (-1, 1): cv.drawLine(sx + sd * 250, 476, sx + sd * 250, 540, stroke((14, 18, 30), 7, cap=False))
        rc = LTRB(sx - 310, 536, sx + 310, 664)
        cv.drawRRect(RRXY(rc.makeOffset(6, 10), 16, 16), fill((4, 6, 20), 120)); cv.drawRRect(RRXY(rc, 16, 16), fill(PAPER)); cv.drawRRect(RRXY(rc.makeInset(10, 10), 9, 9), dashed((150, 40, 46), 3.5, 220, (14, 10)))
        text(cv, 'SON DURAK', sx, 628, 82, (150, 40, 46))
        for lx in ((990, -110) if V else (1180, -200)):
            fl = 1.0 if (k * 5 + lx) % 23 else 0.5
            poly(cv, [(lx - 36, 540), (lx + 36, 540), (lx + 330, y + 130), (lx - 330, y + 130)], LAMPC, 34 * fl)
            cv.drawLine(lx, 476, lx, 510, stroke((14, 18, 30), 6, cap=False)); poly(cv, [(lx - 24, 506), (lx + 24, 506), (lx + 54, 544), (lx - 54, 544)], (20, 24, 34))
            cv.drawOval(LTRB(lx - 34, 534, lx + 34, 556), fill(LAMPC, 255 * fl))
        fog(cv, 0.35, k, y=y + 190, h=300)
        out = {w: v for w, v in st.items() if v[0][2] > DOORC[2] + 0.001}
        f = people(cv, ts, {w: v[0] for w, v in out.items()}, {w: v[1] for w, v in out.items()}) if out else {}
        if extra: extra(f)
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y + 420), skia.Point(0, y + 760)], [skia.Color(8, 10, 26, 0), skia.Color(8, 10, 26, 200)]))
        cv.drawRect(LTRB(X0, y + 400, X1, 2600), g)
    grain(cv)


# ---------- sabah: uc istasyon ----------
def post_sign(cv, x, name, y=650):
    cv.drawLine(x, y, x, WF + 6, stroke((70, 60, 64), 14, cap=False))
    rc = LTRB(x - 200, y - 56, x + 200, y + 46)
    cv.drawRRect(RRXY(rc.makeOffset(5, 8), 14, 14), fill((40, 40, 60), 90)); cv.drawRRect(RRXY(rc, 14, 14), fill(PAPER)); cv.drawRRect(RRXY(rc.makeInset(9, 9), 8, 8), dashed((150, 40, 46), 3, 220, (12, 9)))
    ftext(cv, name, x, rc.centerY(), 60, (150, 40, 46), 350)


def stayed_wagon(cv, x, y, no, u=2.5):
    """istasyonda kalan vagon (gunduz): kisa bir ray parcasinin ustunde"""
    cv.drawRect(LTRB(x - 30, y + 18 * u * 0.4, x + 165 * u + 30, y + 18 * u * 0.4 + 8), fill((90, 84, 90)))
    ext_wagon(cv, x, y, u, lit=0.0, num=no)


def meadow(cv, c=(126, 172, 110), path=(226, 208, 164)):
    cv.drawRect(LTRB(X0, WF - 90, X1, 2600), fill(c))
    for i in range(40): cv.drawCircle(X0 + (i * 173) % (X1 - X0), WF - 70 + (i * 37) % 60, 5, fill(((250, 236, 150), (244, 160, 150), (250, 250, 240))[i % 3], 220))
    cv.drawRect(LTRB(X0, WF, X1, FEDGE + 30), fill(path)); cv.drawLine(X0, WF + 20, X1, WF + 20, dashed(shade(path, 0.8), 3.5, 180, (40, 20)))
    cv.drawRect(LTRB(X0, FEDGE + 30, X1, 2600), fill(shade(c, 0.86)))
    for i in range(36): cv.drawCircle(X0 + (i * 211) % (X1 - X0), FEDGE + 90 + (i * 53) % 420, 6, fill(((250, 236, 150), (244, 160, 150), (250, 250, 240))[i % 3], 200))


def karakopru(cv, k):
    cv.clear(col((120, 170, 220)))
    with stage(cv):
        morning_sky(cv, k, y_h=960, sun=(860, 600) if V else (1240, 640))
        cv.drawRect(LTRB(X0, 1100, X1, 2600), fill((120, 168, 108)))
        stayed_wagon(cv, 30 if V else -330, 1160, 5)
        hx = 760 if V else 1150                                                                     # Eli'nin evi (karsi kiyida)
        cv.drawRect(LTRB(hx, 930, hx + 250, 1160), fill((240, 226, 200))); poly(cv, [(hx - 30, 930), (hx + 280, 930), (hx + 125, 800)], (150, 66, 70))
        cv.drawRect(LTRB(hx + 40, 1010, hx + 110, 1160), fill(SKYB)); cv.drawRect(LTRB(hx + 150, 990, hx + 220, 1060), fill((255, 228, 156)))
        cv.drawRect(LTRB(hx + 190, 800, hx + 222, 880), fill((150, 80, 76)))
        for i in range(4):
            ph = ((k * 0.35 + i * 5) % 20) / 20.0; cv.drawCircle(hx + 206 + ph * 90, 780 - ph * 170, 18 + 40 * ph, fill((250, 246, 240), 150 * (1 - ph)))
        post_sign(cv, 300 if V else 110, 'KARAKÖPRÜ')
        # tas kopru: korkuluk, yol, kemerler ve sabah isigi vuran su
        st_ = (52, 54, 70)
        cv.drawRect(LTRB(X0, 1120, X1, WF), fill(st_))
        for px in range(X0, X1, 130): cv.drawRRect(RRXY(LTRB(px, 1080, px + 60, 1124), 8, 8), fill(shade(st_, 1.25)))
        cv.drawLine(X0, 1150, X1, 1150, dashed(shade(st_, 1.7), 4, 190, (30, 16)))
        cv.drawRect(LTRB(X0, WF, X1, FEDGE + 30), fill((150, 146, 150))); cv.drawLine(X0, WF + 20, X1, WF + 20, dashed((110, 106, 116), 3.5, 190, (40, 20)))
        top = FEDGE + 30
        cv.drawRect(LTRB(X0, top, X1, 2600), fill(st_)); cv.drawRect(LTRB(X0, top, X1, top + 24), fill(shade(st_, 1.3)))
        span = 560; x = X0 - 100
        while x < X1 + 100:
            p = skia.Path(); p.moveTo(x + 70, 2600); p.lineTo(x + 70, top + 330); p.arcTo(LTRB(x + 70, top + 110, x + span - 70, top + 550), 180, 180, False); p.lineTo(x + span - 70, 2600); p.close()
            cv.drawPath(p, fill((150, 196, 226)))
            cv.save(); cv.clipPath(p, True)
            cv.drawRect(LTRB(x, top + 400, x + span, 2600), fill((96, 160, 206)))
            for j in range(5): cv.drawLine(x + 150 + 26 * j + 8 * math.sin(k * 0.3 + j), top + 440 + 44 * j, x + span - 150 - 26 * j, top + 440 + 44 * j, stroke((255, 244, 206), 6, 150 - 20 * j))
            cv.restore(); cv.drawPath(p, dashed(shade(st_, 1.8), 4, 190, (20, 14)))
            x += span
    grain(cv)


def degirmen(cv, k):
    cv.clear(col((120, 170, 220)))
    with stage(cv):
        morning_sky(cv, k, y_h=960, sun=(230, 560) if V else (-120, 600))
        hl = skia.Path(); hl.moveTo(360, 1300); hl.quadTo(820, 620, 1640, 1010); hl.lineTo(1640, 1300); hl.close(); cv.drawPath(hl, fill((112, 164, 110)))
        mx, my = 800, 880                                                                            # yel degirmeni
        poly(cv, [(mx - 86, my + 250), (mx + 86, my + 250), (mx + 54, my - 30), (mx - 54, my - 30)], (244, 232, 208))
        poly(cv, [(mx - 70, my - 30), (mx + 70, my - 30), (mx, my - 120)], (170, 66, 70))
        cv.drawRRect(RRXY(LTRB(mx - 26, my + 150, mx + 26, my + 250), 20, 20), fill((120, 84, 60))); cv.drawRect(LTRB(mx - 20, my + 50, mx + 20, my + 100), fill((120, 170, 200)))
        cv.save(); cv.translate(mx, my - 40); cv.rotate(k * 2.4)
        for j in range(4):
            cv.rotate(90); cv.drawLine(0, 0, 0, -230, stroke((120, 84, 60), 10)); cv.drawRect(LTRB(8, -226, 66, -54), fill(CREAM, 235)); cv.drawRect(LTRB(8, -226, 66, -54), dashed(CORAL, 3, 220, (12, 9)))
        cv.restore(); cv.drawCircle(mx, my - 40, 16, fill(BRASS))
        meadow(cv)
        stayed_wagon(cv, -470 if not V else -260, 1168, 4)
        post_sign(cv, 300 if V else 160, 'DEĞİRMEN')
    grain(cv)


def yedigol(cv, k):
    cv.clear(col((120, 170, 220)))
    with stage(cv):
        morning_sky(cv, k, y_h=930, sun=(820, 560) if V else (1220, 600))
        cv.drawRect(LTRB(X0, 960, X1, 2600), fill((120, 170, 112)))
        for j, (lx, ly, lw) in enumerate(((120, 1000, 150), (430, 990, 130), (760, 1004, 160), (1090, 992, 140), (-200, 1050, 190), (290, 1070, 210), (900, 1076, 230))):   # yedi gol
            rc = LTRB(lx - lw, ly - lw * 0.2, lx + lw, ly + lw * 0.2)
            cv.drawOval(rc.makeOutset(8, 5), fill((96, 150, 100))); cv.drawOval(rc, fill((110, 176, 220)))
            cv.drawLine(lx - lw * 0.4 + 6 * math.sin(k * 0.3 + j), ly, lx + lw * 0.3, ly, stroke((255, 246, 214), 5, 190))
        meadow(cv)
        stayed_wagon(cv, 1120 if not V else 800, 1168, 3)
        post_sign(cv, 330 if V else 60, 'YEDİGÖL', 650 if V else 730)
    grain(cv)


BENX, BENY = 560, 1238                                     # bankin ortasi ve oturma tahtasinin ustu
def bench(cv):
    cv.drawRRect(RRXY(LTRB(BENX - 250, BENY - 150, BENX + 250, BENY - 96), 12, 12), fill((70, 110, 118))); cv.drawRRect(RRXY(LTRB(BENX - 250, BENY - 80, BENX + 250, BENY - 30), 12, 12), fill((70, 110, 118)))
    for sd in (-1, 1): cv.drawRect(LTRB(BENX + sd * 220 - 10, BENY - 150, BENX + sd * 220 + 10, BENY + 96), fill((40, 66, 72)))
    cv.drawRRect(RRXY(LTRB(BENX - 270, BENY, BENX + 270, BENY + 34), 12, 12), fill((86, 130, 138))); cv.drawLine(BENX - 250, BENY + 17, BENX + 250, BENY + 17, dashed((150, 190, 190), 3, 190, (14, 10)))


# ---------- biten orgu (cok yakin): en ustte EV ----------
KROWS = (('EV', MUSTARD), ('YEDİGÖL', CORAL), ('DEĞİRMEN', CORAL), ('KARAKÖPRÜ', CORAL))
FW, BH = 700, 132
FH = BH * len(KROWS)
def _fabric(c):
    rc = LTRB(20, 40, 20 + FW, 40 + FH + 30)
    c.drawRRect(RRXY(rc, 20, 20), fill(CREAM))
    for j, (nm, cc) in enumerate(KROWS):
        y0 = 40 + j * BH
        if j: c.drawLine(34, y0, 6 + FW, y0, dashed(CORAL, 5, 230, (16, 12)))
        f = skia.Font(TFB, 92); f.setEmbolden(True); w = f.measureText(nm)
        if w > FW - 110: f.setSize(92 * (FW - 110) / w); w = f.measureText(nm)
        c.drawString(nm, 20 + FW / 2 - w / 2 + 3, y0 + BH * 0.5 + f.getSize() * 0.36 + 4, f, fill(shade(cc, 0.62), 150))
        c.drawString(nm, 20 + FW / 2 - w / 2, y0 + BH * 0.5 + f.getSize() * 0.36, f, fill(shade(cc, 0.9) if j == 0 else cc))
    c.save(); c.clipRRect(RRXY(rc, 20, 20), True)
    vs = stroke(shade(CREAM, 0.74), 2.6, 96)
    for r in range(int((FH + 34) / 20) + 1):
        y = 46 + r * 20
        for q in range(int(FW / 22) + 1):
            x = 24 + q * 22; c.drawLine(x, y, x + 9, y + 14, vs); c.drawLine(x + 18, y, x + 9, y + 14, vs)
    c.restore(); c.drawRRect(RRXY(rc, 20, 20), stroke(shade(CREAM, 0.66), 4))
    for q in range(int(FW / 40)): c.drawLine(40 + q * 40, 40 + FH + 30, 40 + q * 40, 40 + FH + 62, stroke(CORAL, 6))       # sacaklar


def knit_done(cv, ts, k, hi):
    x0 = 540 - FW / 2; y0 = 490 if V else 548; sway = 3 * math.sin(k * 0.25)
    with stage(cv):
        cv.save(); cv.translate(sway, 0)
        for sd in (-1, 1): yarn_limb(cv, [(540 + sd * (FW / 2 + 330), y0 + 900), (540 + sd * (FW / 2 + 200), y0 + 420), (540 + sd * (FW / 2 + 40), y0 + 36)], 100, ROSE)
        if hi > 0: glow(cv, 540, y0 + BH * 0.5, 330, (255, 226, 130), 150 * hi, 70)
        blit(cv, sprite(('fabric5', FMT), FW + 40, FH + 150, _fabric), x0 - 20, y0 - 40)
        if hi > 0:
            for sd in (-1, 1): star(cv, 540 + sd * 250, y0 + BH * 0.5 + 6 * sd, (22 + 6 * math.sin(k * 0.8 + sd)) * hi, YEL)
        for sd in (-1, 1): hand_ball(cv, 540 + sd * (FW / 2 + 30), y0 + 6 + alt(k, 0, 5, 4) * sd, 58, ROSE, seed=5 + sd)
        cv.restore()


# ---------- bilet (cok yakin): INIS satirina elle EV yazilir ----------
EV_E = [[(140, 62), (96, 62), (96, 126), (142, 126)], [(96, 94), (132, 94)]]
EV_V = [[(170, 60), (198, 126), (228, 60)]]
def _partial(strokes, u):
    """cizgilerin u (0..1) kadari ve kalemin ucu"""
    ln = [sum(math.dist(a, b) for a, b in zip(s_, s_[1:])) for s_ in strokes]; tot = sum(ln); left = tot * clamp(u); out = []; tip = strokes[0][0]
    for s_, L in zip(strokes, ln):
        if left <= 0: break
        pts = [s_[0]]
        for a, b in zip(s_, s_[1:]):
            d = math.dist(a, b)
            if left >= d: pts.append(b); left -= d; tip = b
            else: f = left / d; tip = (lerp(a[0], b[0], f), lerp(a[1], b[1], f)); pts.append(tip); left = 0; break
        out.append(pts)
    return out, tip


def ticket_ev(cv, cx, cy, w, eu, vu, k, rot=-2, hover=None, hole=0.0, hi=None):
    """Mia'nin bileti. eu, vu 0..1: E ve V harflerinin yazilan kismi. hover: kalem (None: yok; sayi: ucun kagittan yuksekligi). hole 0..1: zimba deligi"""
    u = w / 760.0; started = eu > 0
    ticket(cv, cx, cy, w, MUSTARD, 'MIA', None, 1.0, rot=rot, hi=(0.0 if started else 1.0) if hi is None else hi, k=k)
    cv.save(); cv.translate(cx, cy); cv.rotate(rot)
    st = stroke(INK, 11 * u, 255); st.setStrokeJoin(skia.Paint.kRound_Join); tip = (118 * u, 60 * u)
    for strokes, uu in ((EV_E, eu), (EV_V, vu)):
        if uu <= 0: continue
        parts, tp = _partial(strokes, uu)
        for pts in parts:
            p = skia.Path(); p.moveTo(pts[0][0] * u, pts[0][1] * u)
            for q in pts[1:]: p.lineTo(q[0] * u, q[1] * u)
            cv.drawPath(p, st)
        tip = (tp[0] * u, tp[1] * u)
    if vu >= 1: cv.drawLine(-58 * u, 138 * u, 340 * u, 138 * u, stroke((90, 78, 86), 5 * u, 255, cap=False))
    if hole > 0:
        hx_, hy_ = 296 * u, -100 * u
        cv.drawCircle(hx_, hy_, 30 * u, fill((14, 18, 36))); cv.drawCircle(hx_, hy_, 30 * u, stroke((120, 100, 90), 3))
        check(cv, hx_ - 84 * u, hy_, 27 * u, (40, 150, 90), a=hole)
    if hover is not None:
        tx_, ty_ = tip[0], tip[1] - hover + (3 * math.sin(k * 0.5) if hover > 4 else 0)
        yarn_limb(cv, [(tx_ + 560 * u, ty_ + 640 * u), (tx_ + 420 * u, ty_ + 390 * u), (tx_ + 250 * u, ty_ + 190 * u)], 116 * u, MUSTARD)
        pencil(cv, tx_, ty_, 420 * u, 40, th=40 * u)
        hand_ball(cv, tx_ + 236 * u, ty_ + 196 * u, 74 * u, MUSTARD, seed=6)
    cv.restore()
TKV = (480, 740, 820) if V else (860, 480, 780)             # bilet yakin planinin yeri (ekran): cx, cy, w


def hud(cv, t, k):
    if t < HK: hook_text(cv, t, 'MAKİNİST KOLTUĞU BOŞ', 1 - seg(t, HK - 0.12, HK))
    if k in FBL: memory_frame(cv, FBL[k], a=0.9)
    if k == 19:
        a = min(seg(t, S('m11') + 0.1, S('m11') + 0.4), 1 - seg(t, E('m11') + 0.1, E('m11') + 0.35))
        if V: portrait(cv, step(t), 'D', 230, 560, 164, a, expr='mutlu', prop='knit', label='"Sen karar ver."')
        else: portrait(cv, step(t), 'D', 1690, 250, 130, a, expr='mutlu', prop='knit', label='"Sen karar ver."')
    if k == 33: abone(cv, t, END0 + ABONE_END, pos=(W / 2, 1500) if V else (W / 2, 800))
FBL = {12: 'BU AKŞAM · EV', 13: 'BU AKŞAM · GİŞE', 15: 'BU AKŞAM · EV'}
def fb_in(cv, t, k): flash(cv, 0.85 * (1 - seg(t, TL.span(k)[0], TL.span(k)[0] + 0.22)))
def fb_out(cv, t, k): flash(cv, 0.85 * seg(t, TL.span(k)[1] - 0.14, TL.span(k)[1]))


# ============ SAHNE 1: kanca. Lokomotif: lambanin altinda makinist koltugu bos; kollar kendi kendine oynuyor ============
def scene1(cv, t):
    ts, k = step(t), kk(t)
    M_ = ('panik', dict(FWD, lean=alt(k, 8, 14, 2), belly=-8), 2, dict(prop='carry'))
    with zoom(cv, 1.0 if V else 1.05, (560, 1000), QW): cabp(cv, ts, k, {'M': ((350, NEAR, 0.70), M_)}, ghost=1.0)
    flash(cv, 0.8 * seg(t, HK - 0.12, HK))


# ============ SAHNE 2: disaridan: lokomotif ve tek vagon; uc yolcu indi, Mia'nin bileti bos ============
def scene2(cv, t):
    ts, k = step(t), kk(t)
    a0 = TL.span(2)[0]
    xr = (760 if V else 980) + 24 * (ts - a0)
    ext(cv, ts, k, xr, 1, heads={1: [None, None, MUSTARD, CNAVY, None]}, moon=(130, 300) if V else (-200, 600))
    al = [seg(ts, frac('n1', f_), frac('n1', f_) + 0.15) for f_ in (0.2, 0.26, 0.32)]
    medals(cv, k, TRIO, al, ok=seg(ts, frac('n1', 0.52), frac('n1', 0.52) + 0.5))
    a = smooth(seg(ts, frac('n1', 0.74), frac('n1', 0.74) + 0.3))
    if V: ticket(cv, 540, 800 + 30 * (1 - a), 520, MUSTARD, 'MIA', None, a, rot=-3, hi=1.0, k=k)
    else: ticket(cv, 1480, 560 + 30 * (1 - a), 440, MUSTARD, 'MIA', None, a, rot=-3, hi=1.0, k=k)
    flash(cv, 0.8 * (1 - seg(t, HK, HK + 0.2)))


# ============ SAHNE 3: bir numara: Konduktor duvardaki mikrofonun dugmesine basar; anons; levha kirmizi yanar ============
def scene3(cv, t):
    ts, k = step(t), kk(t)
    mb = B('mic'); o = ts - mb[0]; lv = TL.talk('A', ts); late = ts >= frac('a1', 0.55)
    on_ = o >= MIC and ts < E('a1') + 0.2
    hi = 1.0 if ts >= frac('a1', 0.62) else 0.0
    spk = lv if lv is not None else (0.5 if on_ else None)
    if late:
        with zoom(cv, 2.5 if V else 2.2, (2555 - CAMF - 60, 606), (540, 800) if V else (540, 950)): wf(cv, ts, k, {}, mic_on=on_, spk=spk, plate_hi=hi)
        return
    pr = reach_pose(CONF[0], CONF[1], CONF[2], (MICX + 4, MICY + 34), dict(lean=10, belly=-6))
    C_ = ('sakin', mixpose(dict(lean=4), pr, seg(o, 0.05, MIC)), 2, dict(prop='lantern', talk=lv))
    up = o >= MIC + 0.25
    M_ = ('merak' if up else 'endise', dict(LOOKUP) if up else {}, 2, dict(prop='carry'))
    def ex(f):
        if MIC <= o < MIC + 0.45: sfx_text(cv, MICX + 40, MICY - 110, 'TIK', 56, a=1 - seg(o, MIC + 0.3, MIC + 0.45))
    with zoom(cv, 1.12 if V else 1.15, (500, 960), (540, 1020)): wf(cv, ts, k, {'M': (MIAF, M_), 'C': (CONF, C_)}, extra=ex, mic_on=on_, spk=spk, plate_hi=hi)


# ============ SAHNE 4: Mia (yakin): "Bir numara mi? Bu son vagon!"; baslik ============
def scene4(cv, t):
    ts, k = step(t), kk(t)
    sp = on(ts, 'm2', 0.0, 0.1)
    M_ = ('saskin' if ts < frac('m2', 0.45) else 'panik', dict(POINTUP, **LOOKUP) if ts < frac('m2', 0.45) else dict(RANT, lean=alt(k, -4, 3, 3)) if sp else dict(CHEST), 2, dict(prop='carry') if ts < frac('m2', 0.45) else {})
    with zoom(cv, *zM(1.5)): wf(cv, ts, k, {'M': (MIAF, M_), 'C': (CONF, ('sakin', {}, -2, dict(prop='lantern')))}, plate_hi=1.0)
    title_card(cv, t)


# ============ SAHNE 5: "Son Durak benim duragim." "Peki ben? Benim biletim bos!" ============
def scene5(cv, t):
    ts, k = step(t), kk(t)
    if ts < S('m3') - 0.12:
        C_ = ('sakin', mixpose({}, dict(aR=(70, 110, 14, 150)), seg(ts, S('c1'), S('c1') + 0.3)) if ts < frac('c1', 0.55) else dict(OPENR), -2, dict(prop='lantern'))
        with zoom(cv, *z2(1.2)): wf(cv, ts, k, {'M': (MIAF, ('endise', {}, 2, dict(prop='carry'))), 'C': (CONF, C_)}, plate_hi=1.0)
    else:
        show = ts >= frac('m3', 0.3)
        M_ = ('panik' if show else 'endise', dict(SHOWB, lean=alt(k, 0, 4, 3)) if show else {}, 2 if not show else 1.4, dict(prop='tk' if show else 'carry'))
        with zoom(cv, *zM(1.5)): wf(cv, ts, k, {'M': (MIAF, M_), 'C': (CONF, ('sakin', {}, -2, dict(prop='lantern')))}, plate_hi=1.0)


# ============ SAHNE 6: Konduktor (yakin): "Bileti bos olan inemez. Siz lokomotifle devam edersiniz." ============
def scene6(cv, t):
    ts, k = step(t), kk(t)
    pt = ts >= frac('c2', 0.5)
    C_ = ('uzgun', dict(FWD, lean=6) if pt else dict(lean=alt(k, 0, 2, 5)), 2 if pt else -2, dict(prop='lantern'))
    zz = zC(1.5) if not pt else (1.3 if V else 1.35, (CONF[0] + 110, 940), QC)
    with zoom(cv, *zz): wf(cv, ts, k, {'M': (MIAF, ('endise', {}, 2, dict(prop='tk'))), 'C': (CONF, C_)}, plate_hi=1.0)


# ============ SAHNE 7: lokomotifin kapisi: "O kapi kilitli!" Konduktor'un anahtari kilidi acar, kapi kayar ============
def key(cv, x, y, rot, s=1.0):
    """anahtar; (x, y): ucu (kilide giren uc), govde rot acisina dogru uzanir"""
    cv.save(); cv.translate(x, y); cv.rotate(rot)
    cv.drawLine(0, 0, 96 * s, 0, stroke(shade(BRASS, 0.6), 15 * s)); cv.drawLine(0, 0, 96 * s, 0, stroke(BRASS, 10 * s))
    for dx_ in (8, 26): cv.drawRect(LTRB(dx_ * s, 0, (dx_ + 10) * s, 22 * s), fill(BRASS))
    cv.drawCircle(120 * s, 0, 30 * s, stroke(shade(BRASS, 0.6), 15 * s)); cv.drawCircle(120 * s, 0, 30 * s, stroke(BRASS, 10 * s)); cv.restore()


def scene7(cv, t):
    ts, k = step(t), kk(t)
    ub = B('unlock'); o = ts - ub[0]
    locked = o < UNLOCK[1]; ou = smooth(seg(o, UNLOCK[2], UNLOCK[3]))
    hit = 0 <= o - UNLOCK[1] < 0.2
    sh = jit(k, 4) if hit else (0, 0)
    z = lerp(1.0, 1.4, smooth(seg(o, UNLOCK[2] - 0.1, UNLOCK[3] + 0.1)))
    lx_, ly_ = D1 - 56, 1168
    with zoom(cv, z, (540, 900), (540, 930) if V else (540, 1000)):
        door_view(cv, k, scroll=-SC(ts), label='LOKOMOTİF', glass=loco_glass, lock=locked, open_u=ou, shake=sh, plate_hi=1.0 if (o < 0 and ts >= frac('m4', 0.5)) else 0.0)
        with stage(cv, *sh):
            if o < 0:                                        # Mia'nin eli kapiyi gosterir
                rch = smooth(seg(ts, S('m4') - 0.15, S('m4') + 0.25)); dy_ = 420 * (1 - rch)
                yarn_limb(cv, [(110, 1760 + dy_), (210, 1460 + dy_), (316, 1186 + dy_)], 84, MUSTARD); hand_ball(cv, 330, 1160 + dy_, 46, MUSTARD)
                if ts >= frac('m4', 0.5): sfx_text(cv, 540, 990, 'KİLİTLİ', 70, c=RED, rot=-4, a=1.0 if (k // 3) % 2 == 0 else 0.6, rays=False)
            elif o < UNLOCK[2] + 0.35:                       # Konduktor'un eli ve anahtar
                rch = smooth(seg(o, 0.0, UNLOCK[0])); out_ = smooth(seg(o, UNLOCK[1] + 0.08, UNLOCK[2] + 0.3))
                kx, ky = lx_ + 4 + 170 * (1 - rch) + 300 * out_, ly_ + 2 + 110 * (1 - rch) + 240 * out_
                turn = 80 * smooth(seg(o, UNLOCK[0] + 0.1, UNLOCK[1]))
                yarn_limb(cv, [(kx + 560, ky + 640), (kx + 400, ky + 340), (kx + 196, ky + 80)], 90, CNAVY)
                key(cv, kx, ky, 18 + turn * 0.25, 1.15); hand_ball(cv, kx + 180, ky + 62, 50, CNAVY, seed=7)
            if not locked and o < UNLOCK[1] + 0.7:           # acilan kilit yere duser
                d = o - UNLOCK[1]; fx_, fy_ = lx_ - 30 * d, ly_ + 900 * d * d
                cv.save(); cv.translate(fx_, fy_); cv.rotate(-200 * d)
                sk = skia.Path(); sk.addArc(LTRB(-17, -44, 17, -6), 150, 200); cv.drawPath(sk, stroke((150, 156, 176), 8))
                cv.drawRRect(RRXY(LTRB(-27, -24, 27, 26), 8, 8), fill(BRASS)); cv.drawCircle(0, -2, 6, fill((40, 30, 24))); cv.restore()
            if 0 <= o - UNLOCK[0] < 0.4: sfx_text(cv, 800, 1040, 'TIK', 60, a=1 - seg(o - UNLOCK[0], 0.25, 0.4))
            if 0 <= o - UNLOCK[1] < 0.45: sfx_text(cv, 820, 960, 'ÇIT', 70, c=YEL, a=1 - seg(o - UNLOCK[1], 0.3, 0.45))


# ============ SAHNE 8: lokomotif (genis): "Makinist koltugu bos!" "Hic kimse. Bu tren yolunu biletlerden okur." ============
def scene8(cv, t):
    ts, k = step(t), kk(t)
    a0 = TL.span(8)[0]
    if ts < S('c3') - 0.12:
        x = lerp(250, MIAC[0], smooth(seg(ts, a0, a0 + 0.7)))
        if x < MIAC[0] - 1: M_ = ('panik', dict(walk(x - 250, 0.70, 1, run=True, hold=True), aL=(-60, 110, -20, 190), aR=(90, 100, 150, 60)), 2, dict(prop='carry'))
        else: M_ = ('panik' if on(ts, 'm5', 0.0, 0.1) else 'endise', dict(FWD, lean=alt(k, 8, 14, 3), belly=-8), 2, dict(prop='carry'))
        close = ts >= frac('m5', 0.52)
        zz = (1.3 if V else 1.35, (SEATX - 70, 950), QC) if close else (1.0 if V else 1.05, (560, 1000), QW)
        with zoom(cv, *zz): cabp(cv, ts, k, {'M': ((x, NEAR, 0.70), M_), 'C': (CONC, ('yorgun', {}, 2, dict(prop='lantern')))}, ghost=seg(ts, S('m5'), S('m5') + 0.2))
    else:
        pt = ts >= frac('c3', 0.42)
        C_ = ('sakin', dict(POINTUP, lean=4) if pt else dict(lean=alt(k, 0, 2, 5)), 2, dict(prop='lantern'))
        M_ = ('saskin', dict(CHEST), -2 if not pt else -1, dict(prop='carry'))
        with zoom(cv, *z2c(1.22)): cabp(cv, ts, k, {'M': (MIAC, M_), 'C': (CONC, C_)})


# ============ SAHNE 9: yol tablosu (cok yakin): bes durak tek tek yanar; altinci bilet bos: tren hic durmaz ============
BOARD = (0.02, 0.07, 0.12, 0.17, 0.22)                    # c4 icinde duraklarin yandigi anlar
def bgC(cv, ts, k, px=440):
    with zoom(cv, 2.2, (px, 900), (540, 1000)): cab(cv, k, SC(ts))
def scene9(cv, t):
    ts, k = step(t), kk(t)
    bgC(cv, ts, k, 700); dim(cv, 0.74)
    lit = sum(seg(ts, frac('c4', f_), frac('c4', f_) + 0.1) for f_ in BOARD)
    route_board(cv, k, lit, blank=seg(ts, frac('c4', 0.30), frac('c4', 0.38)), never=seg(ts, frac('c4', 0.74), frac('c4', 0.74) + 0.1))


# ============ SAHNE 10: on cam: onde yalnizca karanlik; Mia (yakin) ============
def scene10(cv, t):
    ts, k = step(t), kk(t)
    ab = B('ahead')
    if ts < S('m6') - 0.12:
        with zoom(cv, lerp(1.0, 1.22, smooth(seg(ts, ab[0], ab[1]))), (540, 930), (540, 930) if V else (540, 940)): front_view(cv, k, SC(ts) * 1.4)
        a = seg(ts, ab[0] + 0.25, ab[0] + 0.45)
        otext(cv, 'ÖNÜ KARANLIK', W / 2, 700 if V else 250, 80 if V else 64, RED, a=a * (1.0 if (k // 3) % 2 else 0.7))
    else:
        M_ = ('aglama' if ts >= frac('m6', 0.55) else 'panik', dict(CHEST, lean=-6, belly=6), -2 if ts >= frac('m6', 0.3) else 2, dict(prop='carry'))
        with zoom(cv, *zMc(1.55)): cabp(cv, ts, k, {'M': (MIAC, M_), 'C': (CONC, ('uzgun', {}, 2, dict(prop='lantern')))})


# ============ SAHNE 11: "Nereye gittiginizi bilmiyorsunuz. Peki nereden geldiginizi biliyor musunuz?" ============
def scene11(cv, t):
    ts, k = step(t), kk(t)
    q = ts >= frac('c5', 0.42)
    if not q:
        C_ = ('sakin', dict(OPENR, lean=alt(k, 0, 3, 4)), 2, dict(prop='lantern'))
        with zoom(cv, *z2c(1.22)): cabp(cv, ts, k, {'M': (MIAC, ('uzgun', dict(CHEST), -2, dict(prop='carry'))), 'C': (CONC, C_)})
    else:
        C_ = ('sakin', dict(lean=8, belly=-6, aR=(110, 60, 150, -30)), 2, dict(prop='lantern'))
        with zoom(cv, *zCc(1.55)): cabp(cv, ts, k, {'M': (MIAC, ('merak', dict(CHEST), -2, dict(prop='carry'))), 'C': (CONC, C_)})
    fb_out(cv, t, 11)


# ============ SAHNE 12: GERI DONUS 1 (sepya): ev. Kapi carpilir; Mia hizla uzaklasir ============
def scene12(cv, t):
    ts, k = step(t), kk(t)
    sb = B('slam'); o = ts - sb[0]
    du = 1 - seg(o, SLAM - 0.12, SLAM)
    sh = jit(k, 5) if 0 <= o - SLAM < 0.25 else (0, 0)
    x = lerp(236, 860, seg(ts, sb[0] + SLAM + 0.15, E('m7') + 0.2) ** 0.9)
    if o < SLAM + 0.15: M_ = ('kararli', dict(lean=10, aL=(-150, 90, -216, 150)), 2)
    else: M_ = ('kararli' if ts < frac('m7', 0.5) else 'uzgun', walk(x - 236, 0.70, 1, hold=False), 2)
    with tint(cv, sepia_m(0.45)):
        with zoom(cv, 1.0 if V else 1.05, (560, 1000), QW):
            home(cv, k, door_u=du, shake=sh)
            with stage(cv, *sh):
                actor(cv, ts, 'M', M_[0], M_[1], M_[2], place=(x, NEAR, 0.70))
                if 0 <= o - SLAM < 0.5: sfx_text(cv, 210, 740, 'ÇAT!', 84, c=YEL, a=1 - seg(o - SLAM, 0.3, 0.5))
    fb_in(cv, t, 12)


# ============ SAHNE 13: GERI DONUS 2 (sepya): gise. "Nereye?" "Ilk kalkan trene." Bilet: INIS satiri bos ============
def scene13(cv, t):
    ts, k = step(t), kk(t)
    sb = B('slip'); o = ts - sb[0]
    sl = smooth(seg(o, SLIP, SLIP + 0.35))
    ans = ts >= frac('m8', 0.55)
    M_ = ('uzgun', dict(aR=(110, 60, 150, -40)) if ans and o < 0 else ({} if o < SLIP + 0.3 else dict(aR=(110, 90, 190, 60))), 2, dict(back=True))
    with tint(cv, sepia_m(0.45)):
        with zoom(cv, 1.08 if V else 1.05, (540, 960), QW):
            gise(cv, k, slip=sl)
            with stage(cv):
                actor(cv, ts, 'M', M_[0], M_[1], M_[2], place=(330, NEAR + 110, 0.80), back=True)
                bubble(cv, 780, 760, 'NEREYE?', 58, a=min(seg(ts, frac('m8', 0.3), frac('m8', 0.3) + 0.12), 1 - seg(ts, frac('m8', 0.54), frac('m8', 0.58))), tail=-1)
                bubble(cv, 690, 750, 'İLK KALKAN TRENE', 40, a=min(seg(ts, frac('m8', 0.58), frac('m8', 0.58) + 0.12), 1 - seg(o, 0.0, 0.2)), tail=-1, c=MUSTARD, tc=INKBLUE)
        a = smooth(seg(o, SLIP + 0.3, SLIP + 0.6))
        if a > 0:
            dim(cv, 0.5 * a)
            if V: ticket(cv, 540, 780 + 40 * (1 - a), 800, MUSTARD, 'MIA', None, a, rot=-3, hi=1.0, k=k)
            else: ticket(cv, 960, 500 + 40 * (1 - a), 760, MUSTARD, 'MIA', None, a, rot=-3, hi=1.0, k=k)
    fb_in(cv, t, 13); fb_out(cv, t, 13)


# ============ SAHNE 14: bugun: "Kacan yolcu yer soylemez. Satir o yuzden bos kaldi." ============
def scene14(cv, t):
    ts, k = step(t), kk(t)
    if ts < frac('c6', 0.48):
        C_ = ('sakin', dict(OPENR, lean=alt(k, 0, 3, 4)), 2, dict(prop='lantern'))
        with zoom(cv, *zCc(1.5)): cabp(cv, ts, k, {'M': (MIAC, ('uzgun', {}, -2, dict(prop='tk'))), 'C': (CONC, C_)})
    else:
        M_ = ('uzgun', dict(SHOWB, lean=alt(k, 0, 2, 5)), 1.4, dict(prop='tk'))
        with zoom(cv, *zMc(1.55)): cabp(cv, ts, k, {'M': (MIAC, M_), 'C': (CONC, ('sakin', {}, 2, dict(prop='lantern')))})
    fb_in(cv, t, 14); fb_out(cv, t, 14)


# ============ SAHNE 15: GERI DONUS 3 (sepya): Mia arkasina bakar; mutfagin isigi yaniyor, camda biri bekliyor ============
def scene15(cv, t):
    ts, k = step(t), kk(t)
    t1 = frac('m9', 0.46)
    with tint(cv, sepia_m(0.45)):
        if ts < t1:
            M_ = ('uzgun', dict(lean=-8, belly=4), -2 if ts >= frac('m9', 0.12) else 2)
            with zoom(cv, 1.0 if V else 1.05, (560, 1000), QW):
                home(cv, k)
                with stage(cv): actor(cv, ts, 'M', M_[0], M_[1], M_[2], place=(830, NEAR, 0.70))
        else:
            with zoom(cv, lerp(1.7, 2.0, seg(ts, t1, E('m9') + 0.4)), (550, 890), (540, 900) if V else (540, 960)): home(cv, k)
    fb_in(cv, t, 15); fb_out(cv, t, 15)


# ============ SAHNE 16: "Isik yaniyorsa bekleyen var demektir kucuk hanim." ============
def scene16(cv, t):
    ts, k = step(t), kk(t)
    C_ = ('mutlu' if ts >= frac('c7', 0.4) else 'sakin', dict(lean=6, aR=(110, 60, 150, -30)) if ts >= frac('c7', 0.4) else {}, 2, dict(prop='lantern'))
    M_ = ('merak' if ts >= frac('c7', 0.5) else 'uzgun', dict(CHEST), -2, dict(prop='carry'))
    with zoom(cv, *z2c(1.25)): cabp(cv, ts, k, {'M': (MIAC, M_), 'C': (CONC, C_)})
    fb_in(cv, t, 16)


# ============ SAHNE 17: on cam: karanligin icinde Son Durak'in isiklari; "Kalem sizde." ============
def scene17(cv, t):
    ts, k = step(t), kk(t)
    nb = B('near')
    if ts < frac('c8', 0.5):
        nr = seg(ts, nb[0] + 0.15, frac('c8', 0.5)) * 0.9
        front_view(cv, k, SC(ts) * 1.4, near=nr)
        with stage(cv):
            gy_ = 1790 if V else 1760
            actor(cv, ts, 'C', 'sakin', dict(LANT), 0, place=(250 if V else 150, gy_, 1.0), back=True, prop='lantern')
            actor(cv, ts, 'M', 'sakin', dict(aR=(120, 60, 160, -60)) if ts >= nb[0] + 1.0 else {}, 0, place=(820 if V else 930, gy_ + 30, 0.96), back=True)
    else:
        C_ = ('sakin', dict(FWD, lean=6), 2, dict(prop='lantern'))
        M_ = ('endise', mixpose({}, dict(aR=(130, 150, 60, 236)), seg(ts, frac('c8', 0.5), frac('c8', 0.8))), 0, dict(prop='carry'))
        with zoom(cv, *z2c(1.25)): cabp(cv, ts, k, {'M': (MIAC, M_), 'C': (CONC, C_)})


# ============ SAHNE 18: "Ya yanlis yazarsam?" "Yanlis durak olmaz. Yalnizca gidilmemis durak olur." ============
def scene18(cv, t):
    ts, k = step(t), kk(t)
    if ts < S('c9') - 0.12:
        M_ = ('endise', dict(lean=alt(k, -2, 2, 4)), -2 if ts >= frac('m10', 0.3) else 0, dict(prop='pen'))
        with zoom(cv, *zMc(1.55)): cabp(cv, ts, k, {'M': (MIAC, M_), 'C': (CONC, ('sakin', {}, 2, dict(prop='lantern')))})
    else:
        C_ = ('sakin', dict(OPENR, lean=alt(k, 2, 5, 4)) if ts < frac('c9', 0.45) else dict(lean=8, aR=(110, 60, 150, -30)), 2, dict(prop='lantern'))
        with zoom(cv, *zCc(1.5)): cabp(cv, ts, k, {'M': (MIAC, ('merak', {}, -2, dict(prop='pen'))), 'C': (CONC, C_)})


# ============ SAHNE 19: Mia karar verir: "Ada hakliydi. Ne yazacagima ben karar veririm." (kosede Ada'nin kasnagi) ============
def scene19(cv, t):
    ts, k = step(t), kk(t)
    M_ = ('kararli', dict(lean=alt(k, 0, 3, 4)), 0 if ts >= frac('m11', 0.4) else 1.5, dict(prop='pen'))
    with zoom(cv, 1.5 if V else 1.55, (MIAC[0] + 20, 950), QC): cabp(cv, ts, k, {'M': (MIAC, M_)})


# ============ SAHNE 20: bilet (cok yakin): kalem INIS satirina EV yazar ============
def scene20(cv, t):
    ts, k = step(t), kk(t)
    wb = B('write'); o = ts - wb[0]
    eu, vu = seg(o, WRITE[0], WRITE[1]), seg(o, WRITE[2], WRITE[3])
    done = o >= WRITE[3]
    if ts >= frac('m12', 0.42):
        M_ = ('mutlu', dict(SHOWB, lean=alt(k, 0, 3, 5)), 1.4, dict(prop='tk'))
        with zoom(cv, *zMc(1.55)): cabp(cv, ts, k, {'M': (MIAC, M_), 'C': (CONC, ('mutlu', {}, 2, dict(prop='lantern')))})
        return
    bgC(cv, ts, k, MIAC[0]); dim(cv, 0.66)
    writing = (WRITE[0] <= o < WRITE[1]) or (WRITE[2] <= o < WRITE[3])
    hv = 0 if writing else (lerp(70, 0, smooth(seg(o, 0.0, WRITE[0]))) if o < WRITE[0] else (16 if not done else lerp(16, 150, smooth(seg(o, WRITE[3], WRITE[3] + 0.4)))))
    cx, cy, w = TKV
    if done: glow(cv, cx + w * 0.2, cy + w * 0.12, w * 0.3, (255, 226, 130), 120 * seg(o, WRITE[3], WRITE[3] + 0.2), w * 0.12)
    ticket_ev(cv, cx, cy, w, eu, vu, k, hover=hv)
    if done:
        for sd in (-1, 1): star(cv, cx + w * (0.2 + sd * 0.19), cy + w * 0.01 - 20 * sd, 20 + 6 * math.sin(k * 0.8 + sd), YEL)


# ============ SAHNE 21: Konduktor bileti okur: "Ev. Otuz yildir bu satirda gordugum en guzel durak." ============
def scene21(cv, t):
    ts, k = step(t), kk(t)
    if ts < frac('c10', 0.2):
        bgC(cv, ts, k, CONC[0]); dim(cv, 0.66)
        cx, cy, w = TKV
        ticket_ev(cv, cx + (30 if V else 0), cy, w * 0.96, 1, 1, k, rot=3)
        yarn_limb(cv, [(cx - w * 0.9, cy + w * 1.0), (cx - w * 0.74, cy + w * 0.62), (cx - w * 0.5, cy + w * 0.3)], w * 0.14, CNAVY); hand_ball(cv, cx - w * 0.47, cy + w * 0.25, w * 0.085, CNAVY, seed=7)
    else:
        C_ = ('mutlu', dict(SHOWB, lean=alt(k, 0, 2, 5)), 1.4 if ts < frac('c10', 0.55) else 2, dict(prop='lt'))
        with zoom(cv, *zCc(1.55)): cabp(cv, ts, k, {'M': (MIAC, ('mutlu', dict(CHEST), -2, dict(prop='carry'))), 'C': (CONC, C_)})


# ============ SAHNE 22: zimba (cok yakin): bu kez deler. "Zimba deldi! Ama ev istasyon degil ki." ============
def scene22(cv, t):
    ts, k = step(t), kk(t)
    pb = B('punch'); o = ts - pb[0]
    if ts >= frac('m13', 0.36):
        M_ = ('saskin', dict(SHOWB, lean=alt(k, 0, 3, 4)), -2, dict(prop='tk'))
        with zoom(cv, *zMc(1.55)): cabp(cv, ts, k, {'M': (MIAC, M_), 'C': (CONC, ('mutlu', {}, 2, dict(prop='lp')))})
        return
    hit = 0 <= o - PUNCH < 0.2; holed = o >= PUNCH
    bgC(cv, ts, k, CONC[0]); dim(cv, 0.66)
    cx, cy, w = TKV; u = w / 760.0
    sh = jit(k, 4) if hit else (0, 0)
    ticket_ev(cv, cx + sh[0], cy + sh[1], w, 1, 1, k, hole=1.0 if holed else 0.0)
    inn = smooth(seg(o, 0.0, 0.4)); out_ = smooth(seg(o, PUNCH + 0.35, PUNCH + 0.8)); cl = 1.0 if hit else 0.0
    s_ = 3.4 if V else 3.2
    tx_, ty_ = cx + 296 * u + 20 + 460 * (1 - inn) + 300 * out_, cy - 100 * u + 6 + 80 * out_
    hx_, hy_ = tx_ + 74 * s_, ty_ + 30
    yarn_limb(cv, [(hx_ + 520, hy_ + 560), (hx_ + 300, hy_ + 300), (hx_ + 110, hy_ + 60)], 110, CNAVY)
    punch_tool(cv, hx_, hy_, s_, rot=180 + 8, close=cl)
    hand_ball(cv, hx_ + 120, hy_ + 30, 70, CNAVY, seed=7)
    if 0 <= o - PUNCH < 0.6: sfx_text(cv, cx + 150 * u, cy - 250 * u, 'ÇIT!', 90, c=YEL, a=1 - seg(o - PUNCH, 0.4, 0.6))
    if holed:
        for sd in (-1, 1): star(cv, cx + 296 * u + sd * 70, cy - 100 * u - 60 - 20 * sd, 18 + 6 * math.sin(k * 0.8 + sd), YEL)


# ============ SAHNE 23: "Eve trenle varilmaz, yurunur. Onun icin kapiyi aciyorum." ============
def scene23(cv, t):
    ts, k = step(t), kk(t)
    op = ts >= frac('c11', 0.52)
    C_ = ('mutlu', dict(LANTUP, lean=-4) if op else dict(OPENR, lean=alt(k, 0, 3, 4)), -2 if op else 2, dict(prop='lp'))
    M_ = ('saskin' if not op else 'mutlu', dict(CHEST) if not op else {}, -2, dict(prop='tk'))
    with zoom(cv, *z2c(1.2)): cabp(cv, ts, k, {'M': (MIAC, M_), 'C': (CONC, C_)})


# ============ SAHNE 24: Son Durak peronu: tren durur ============
def scene24(cv, t):
    ts, k = step(t), kk(t)
    s0 = B('stop')[0]; u = seg(ts, s0, s0 + HALT); tx = -760 * (1 - u) ** 2
    sh = jit(k, 3) if s0 + HALT - 0.05 <= ts < s0 + HALT + 0.3 else (0, 0)
    cv.save(); cv.translate(sh[0] * K, 0)
    son_durak(cv, ts, k, tx, heads=[None, MUSTARD, None, CNAVY, None])
    cv.restore()


# ============ SAHNE 25: vagonun kapisi ilk kez acilir; Mia perona iner ============
PLAT_M = (790, 1470, 0.64)
def scene25(cv, t):
    ts, k = step(t), kk(t)
    db = B('door'); o = ts - db[0]
    du = smooth(seg(o, DOOR[0], DOOR[1]))
    dn = smooth(seg(ts, frac('n2', 0.35), frac('n2', 0.95)))
    if dn <= 0: pl = (DOORC[0] + 10, DOORC[1], DOORC[2]); M_ = ('saskin' if o < DOOR[1] + 0.4 else 'merak', {}, 0, dict(prop='tk'))
    else:
        pl = (lerp(DOORC[0] + 10, PLAT_M[0], dn), lerp(DOORC[1], PLAT_M[1], dn), lerp(DOORC[2] + 0.004, PLAT_M[2], dn))
        M_ = ('merak', walk(260 * dn, pl[2], 1, hold=True) if dn < 1 else dict(LOOKUP), 1 if dn < 1 else -1, dict(prop='tk'))
    z = lerp(1.5, 1.2, smooth(seg(ts, S('n2') - 0.2, S('n2') + 0.8)))
    def ex(f):
        if 0 <= o - DOOR[0] < 0.7: sfx_text(cv, DX1 + 110, DTOP + 70, 'KAYYY', 56, a=1 - seg(o - DOOR[0], 0.5, 0.7), rot=-4)
    with zoom(cv, z, (DOORC[0] + 40, 1080), (540, 1000) if V else (540, 1010)):
        son_durak(cv, ts, k, 0.0, door_u=du, st={'M': (pl, M_)}, heads=[None, None, None, CNAVY, None], extra=ex)


# ============ SAHNE 26: istasyon salonu: ayni saat, ayni gise. "Burasi trene bindigim istasyon!" ============
def scene26(cv, t):
    ts, k = step(t), kk(t)
    pt = ts < frac('m14', 0.48)
    M_ = ('saskin' if pt else 'heyecan', dict(aR=(130, 20, 200, -150)) if ts < frac('m14', 0.2) else (dict(FWD) if pt else dict(RANT, lean=alt(k, -4, 3, 3))), 2 if pt else 0, dict(prop='tk'))
    with zoom(cv, 1.0 if V else 1.05, (540, 960), QW):
        gise(cv, k, hours=1.2, sign=True)
        with stage(cv): actor(cv, ts, 'M', M_[0], M_[1], M_[2], place=(262, NEAR + 60, 0.74), prop='tk')


# ============ SAHNE 27: peron: "Raylar daire cizer. Son durak, ilk duraktir." Yarim orgu Konduktor'e verilir ============
def scene27(cv, t):
    ts, k = step(t), kk(t)
    gave = ts >= frac('m15', 0.5)
    if ts < S('m15') - 0.12:
        circ = ts >= frac('c12', 0.1) and ts < frac('c12', 0.5)
        C_ = ('sakin' if ts < frac('c12', 0.55) else 'mutlu', dict(aR=(120, 60, 150 + 30 * math.cos(k * 0.9), -30 + 30 * math.sin(k * 0.9))) if circ else {}, 1.5, dict(prop='lantern'))
        M_ = ('merak', dict(LOOKUP), -1.5, dict(prop='tk'))
    elif ts < S('c13') - 0.12:
        M_ = ('mutlu', mixpose({}, GIVEL, seg(ts, S('m15'), frac('m15', 0.4))), -2, dict(prop='carry' if not gave else 'tko'))
        C_ = ('sakin', mixpose({}, dict(aR=(110, 120, 180, 170)), seg(ts, frac('m15', 0.2), frac('m15', 0.5))), 1.5, dict(prop='lk' if gave else 'lantern'))
    else:
        C_ = ('mutlu', dict(SALUTE) if ts >= frac('c13', 0.5) else {}, 1.5, dict(prop='lantern' if ts >= frac('c13', 0.5) else 'lk'))
        M_ = ('mutlu', dict(WAVE) if ts >= frac('c13', 0.5) else {}, -1.5, dict(prop='tko'))
    close = S('m15') - 0.12 <= ts < S('c13') - 0.12
    zz = (1.5 if close else 1.25, (DOORC[0] + 110, 1100), (540, 940) if V else (540, 1010))
    with zoom(cv, *zz):
        son_durak(cv, ts, k, 0.0, door_u=1.0, st={'M': (PLAT_M, M_), 'C': ((DOORC[0] - 6, DOORC[1], DOORC[2]), C_)})


# ============ SAHNE 28: SABAH. Karakopru: Eli evine yurur; Degirmen: kardesi Ren'e kosar ============
CUT28 = 0.60                                                # n3 icinde Degirmen'e gecilen an
def scene28(cv, t):
    ts, k = step(t), kk(t)
    tc = frac('n3', CUT28); hb = B('hug'); a0 = TL.span(28)[0]
    if ts < tc:
        x = lerp(330, 700, seg(ts, a0, tc)) if V else lerp(300, 820, seg(ts, a0, tc))
        karakopru(cv, k)
        with stage(cv): actor(cv, ts, 'E', 'mutlu', walk(x - 250, 0.70, 1, hold=True), 2, place=(x, NEAR, 0.70), prop='case')
    else:
        u = seg(ts, tc + 0.1, hb[0] + HUG) ** 0.9
        kx = lerp(1040, 520, u); met = u >= 1
        degirmen(cv, k)
        with stage(cv):
            R_ = ('mutlu', dict(RANT, lean=6) if not met else dict(aL=(-80, 110, -20, 190), aR=(110, 130, 150, 200), lean=10, crouch=14), 2)
            actor(cv, ts, 'R', R_[0], R_[1], R_[2], place=(370, NEAR, 0.74))
            f = actor(cv, ts, 'K', 'mutlu', walk(1040 - kx, 0.52, -1, run=True) if not met else dict(UP, bob=alt(k, 0, -10, 2)), -2, place=(kx, NEAR, 0.52))
            if f: headphones(cv, f['head'][0], f['head'][1], f['HR'], 255)
            if met:
                for j in range(3): star(cv, 450 + j * 60, 800 - 40 * (j % 2) - 60 * seg(ts, hb[0] + HUG, hb[1]), 18 + 6 * math.sin(k * 0.8 + j), YEL)


# ============ SAHNE 29: Yedigol: Ada bankta orgusunu bitirir; en ustte EV ============
def scene29(cv, t):
    ts, k = step(t), kk(t)
    tm = frac('d1', 0.58)
    if ts < tm:
        up = ts >= frac('d1', 0.3)
        D_ = ('mutlu', dict(SIT, aL=(-84, 110 + alt(k, 0, 8, 2), -40, 180 + alt(k, 0, 10, 2)), aR=(84, 110 + alt(k, 8, 0, 2), 40, 180 + alt(k, 10, 0, 2))), 0, dict(prop='knit'))
        with zoom(cv, 1.2 if V else 1.25, (BENX, 980), (540, 905) if V else (540, 1010)):
            yedigol(cv, k)
            with stage(cv):
                bench(cv)
                glow(cv, BENX + 190, BENY - 60, 60, (255, 214, 130), 130, 26)
                cv.drawRRect(RRXY(LTRB(BENX + 168, BENY - 82, BENX + 212, BENY - 8), 8, 8), fill((255, 226, 150))); cv.drawRRect(RRXY(LTRB(BENX + 168, BENY - 82, BENX + 212, BENY - 8), 8, 8), stroke((50, 44, 40), 6))
                actor(cv, ts, 'D', D_[0], D_[1], D_[2], place=(BENX - 40, BENY + 62, 0.64), prop='knit')
    else:
        def bgf():
            with zoom(cv, 2.2, (BENX, 1000), (540, 1000)): yedigol(cv, k)
        bgf(); dim(cv, 0.45)
        knit_done(cv, ts, k, seg(ts, tm + 0.15, tm + 0.5))


# ============ SAHNE 30: ev (sabah): Mia eve yurur; mutfagin isigi yaniyor; kapi acilir ============
def scene30(cv, t):
    ts, k = step(t), kk(t)
    hb = B('home'); o = ts - hb[0]; a0 = TL.span(30)[0]
    x = lerp(1010, 470, smooth(seg(ts, a0, hb[0] + HOME[0])))
    du = smooth(seg(o, HOME[0], HOME[1]))
    if x > 471: M_ = ('merak', walk(1010 - x, 0.70, -1, hold=False), -2)
    else: M_ = ('mutlu', dict(UP, bob=alt(k, 0, -8, 3)) if du > 0.6 else {}, -2)
    with zoom(cv, 1.0 if V else 1.05, (560, 1000), QW):
        home(cv, k, morning=True, door_u=du, sil=1 - seg(o, HOME[0] - 0.5, HOME[0] - 0.2), arms=seg(o, HOME[1], HOME[1] + 0.4))
        with stage(cv): actor(cv, ts, 'M', M_[0], M_[1], M_[2], place=(x, NEAR, 0.70))


# ============ SAHNE 31: gece: Gece Ekspresi bes vagonuyla yeniden yolda; dort yolcu da indi ============
QUAD = TRIO + ((MUSTARD, 'MIA'),)
def scene31(cv, t):
    ts, k = step(t), kk(t)
    a0 = TL.span(31)[0]
    xr = ((960 if V else 1380) + 26 * (ts - a0))
    ext(cv, ts, k, xr, 5, heads={}, fog_a=0.5, moon=(880, 760) if V else (-160, 600))
    al = [seg(ts, frac('n5', f_), frac('n5', f_) + 0.15) for f_ in (0.34, 0.4, 0.46, 0.52)]
    medals(cv, k, QUAD, al, ok=seg(ts, frac('n5', 0.78), frac('n5', 0.78) + 0.5))


# ============ SAHNE 32: gise: yeni bir yolcu. "Nereye?" ============
def scene32(cv, t):
    ts, k = step(t), kk(t)
    nb = B('new'); o = ts - nb[0]; lv = TL.talk('A', ts)
    x = lerp(60, 400, smooth(seg(o, -0.1, 0.9)))
    Y_ = walk(x - 60, 0.80, 1, hold=True) if x < 399 else (dict(aR=(110, 60, 150, -40)) if ts >= S('a2') else {})
    with zoom(cv, 1.0 if V else 1.05, (540, 960), QW):
        gise(cv, k, hours=22.92, sign=True, spk=lv)
        with stage(cv):
            f = actor(cv, ts, 'Y', 'sakin', dict(Y_, aL=(-110, 150, -130, 280)), 2, place=(x, NEAR + 110, 0.80), back=True)
            if f:
                hx_, hy_, u = f['head'][0], f['head'][1], f['HR']
                cv.drawOval(LTRB(hx_ - u * 1.06, hy_ - u * 1.3, hx_ + u * 1.06, hy_ - u * 0.5), fill((96, 70, 150))); cv.drawCircle(hx_ + u * 0.1, hy_ - u * 1.32, u * 0.14, fill((96, 70, 150)))
                briefcase(cv, f['handL'][0] - 6, f['handL'][1] + 70, 0.9)
            bubble(cv, 780, 760, 'NEREYE?', 58, a=seg(o, NEW + 0.55, NEW + 0.7), tail=-1)


# ============ SAHNE 33: kapanis karti ============
def scene33(cv, t):
    ts, k = step(t), kk(t)
    a0 = END0
    ext(cv, ts, k, (900 if V else 1300) + 40 * (ts - a0), 5, heads={}, fog_a=0.6, moon=(840, 380) if V else (1300, 640))
    dim(cv, 0.55)
    c_ = seg(t, a0 + 0.3, a0 + 0.8)
    card(cv, [('Son Vagon bitti', 84, RED), ('Herkes durağında indi', 44, CREAM), ('Yeni dizi yakında', 54, YEL), ('Tüm bölümler oynatma listesinde', 32, (176, 190, 232))],
         c_, cy=640 if V else 330)


SINE = {1: dict(zmax=1.12), 2: dict(mood='gece'), 7: dict(zmax=1.12), 9: dict(zmax=1.08, rays=False), 10: dict(mood='gece', zmax=1.12),
        12: dict(mood='sepya'), 13: dict(mood='sepya', zmax=1.1), 15: dict(mood='sepya'), 17: dict(mood='gece', zmax=1.1),
        20: dict(zmax=1.08, rays=False), 21: dict(zmax=1.1), 22: dict(zmax=1.08, rays=False), 24: dict(mood='soguk'), 25: dict(zmax=1.1), 27: dict(zmax=1.1),
        28: dict(mood='sicak'), 29: dict(mood='sicak', zmax=1.12), 30: dict(mood='sicak'), 31: dict(mood='gece'), 33: dict(mood='gece')}

if __name__ == '__main__':
    DRAW = {i: globals()[f'scene{i}'] for i in range(1, 34)}
    soft = {(27, 28), (30, 31), (32, 33)}                   # geceden sabaha, sabahtan geceye: yumusak gecis
    run(DRAW, white=tuple((i, i + 1) for i in range(1, 33) if (i, i + 1) not in soft), sine=SINE, hud=hud)
