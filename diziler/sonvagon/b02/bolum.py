"""Son Vagon, 2. Bolum: Degirmen. Yalnizca sahneler; ortak parcalar ../ortak.py icinde.
Yapi: KAYIT BICIMINDE. Butun bolum Ren'in telefonundan gorunur: REC cercevesi, sayac, pil; kesmeler sert (kayit kesmesi).
Uc tur plan var: OZCEKIM (onde buyuk Ren, arkasinda vagonun arka kapisi ve digerleri), KAMERA KARSIDA (Ren gorunmez; sesi ve eli),
TELEFON YERDE (korukte, egik ve alcak). Kanca (bilet cebinden cikar) -> kayit: Karakopru, biletler -> baslik -> Mia ile Ada, pil ->
anons ve levha: VAGON 4 -> koruk -> plan: bileti yirt, camdan at -> bilet cebinde -> one kosu (kapilar) -> lokomotifin kilitli kapisi ->
pencerede degirmen, yokus -> bos koltuk ve ip -> dort numara, lambalar -> itis, telefon duser, kapi -> Ren iceride sakin -> bos ray ->
Mia telefonu alir, soru -> kapanis.
Yeni mekanlar: lokomotifin kapisi (bir numaranin onu), one bakan kapi gorunumu, pencereden degirmen tepesi.
Yeni gorsel fikirler: REC cercevesi ve pil, yirtilan bilet, yerdeki ip, yere dusen telefonun egik kadraji."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import *
from senaryo import ABONE_END, TEAR, THROW, POCK, RUSH, LOCKS, BRAKE, LAMP_OFF, PUSH, FALL, SHUT, OUT_OFF, GONE, PICK

V = FMT == 'v'
QW = (540, 1060) if V else (540, 1000)                     # genis vagon planlarinda sahnenin oturdugu yer
HK = TL.span(2)[0]                                         # kancadan kayda kesme ani
REC1 = TL.span(28)[0]                                      # kaydin durdugu an
STN = 'DEĞİRMEN'
RS = 1.7                                                   # ozcekimde one gelen karakterin olcegi
RX, RGY = (310, 1900) if V else (40, 1900)                 # ozcekimde one gelen karakterin yeri (govdesi kadrajin altina tasar)
BEHIND = {'M': (735, NEAR, 0.72), 'D': (935, FAR, 0.64)} if V else {'M': (880, NEAR, 0.72), 'D': (1120, FAR, 0.64)}
SELF = dict(aL=(-150, 150, -330, 420))                      # telefonu tutan kol kadrajin disina uzanir
SHOWB = dict(aR=(150, 70, 196, -40))                        # elindekini yuzunun yaninda gosterir (buyuk kafa icin)
FWD = dict(aR=(110, 70, 214, 50))                           # ileriyi (sagi) gosterir
POINTB = dict(aR=(150, 60, 240, -10))                       # sagi isaret eder (buyuk kafa)
UPR = dict(aR=(130, 20, 200, -110))                         # sag yukariyi gosterir
DOWNP = dict(aR=(150, 120, 214, 236))                       # yeri gosterir
BENDL = dict(crouch=120, lean=-26, belly=18, kL=(-110, -100), kR=(110, -100), aL=(-110, 150, -150, 300))   # sola egilir
RED = (255, 110, 96)


# ---------- trenin aldigi yol ----------
def _speed(t):
    ml, st0, fg = B('mill')[0], B('stop')[0], B('fog')[0]
    pts = [(0, 420), (ml, 420), (ml + 2.0, 260), (st0 + BRAKE, 170), (st0 + 2.0, 0), (fg + 0.3, 0), (fg + 5, 330), (fg + 9, 420), (9999, 420)]
    return np.interp(t, [p[0] for p in pts], [p[1] for p in pts])
_T = np.arange(0, TL.total + 3, 1 / 24.0); _D = np.concatenate([[0], np.cumsum(_speed(_T[:-1]) / 24.0)])
def SC(t): return float(np.interp(t, _T, _D))


def pl(cam, **xs): return {w: (x - cam, CAST[w]['gy'], CAST[w]['s']) for w, x in xs.items()}


# ---------- kayit cercevesi (kameradan sonra, ekran koordinatinda) ----------
def htext(cv, s, x, y, size, c=(255, 255, 255), tf=None, a=255, right=False):
    f = skia.Font(tf or TFB, size); w = f.measureText(s); x = x - w if right else x
    st = stroke((0, 0, 0), size * 0.16, 150 * a / 255); st.setStrokeJoin(skia.Paint.kRound_Join)
    cv.drawString(s, x, y, f, st); cv.drawString(s, x, y, f, fill(c, a)); return w


def battery(t):
    if t < HK: t = S('r10') + t
    pts = [(0, 16.4), (S('m1') - 1.5, 15.4), (E('m1') + 1.0, 14.6), (REC1, 3.0)]
    return int(round(float(np.interp(t, [p[0] for p in pts], [p[1] for p in pts]))))


def rec_hud(cv, t):
    rt = (S('r10') - HK + t) if t < HK else t - HK
    wh = (255, 255, 255); m, ln = (30, 92) if V else (24, 72)
    for sx in (0, 1):
        for sy in (0, 1):
            x = m if sx == 0 else W - m; y = m if sy == 0 else H - m
            cv.drawLine(x, y, x + (ln if sx == 0 else -ln), y, stroke(wh, 5, 200)); cv.drawLine(x, y, x, y + (ln if sy == 0 else -ln), stroke(wh, 5, 200))
    x0, y0, fs = (72, 108, 40) if V else (W - 560, 78, 34)
    if int(t * 2) % 2 == 0: cv.drawCircle(x0 + 14, y0 - fs * 0.36, fs * 0.3, fill((255, 60, 50)))
    w = htext(cv, 'REC', x0 + 38, y0, fs)
    htext(cv, f'{int(rt // 60):02d}:{int(rt % 60):02d}', x0 + 52 + w, y0, fs, tf=TFM)
    pct = battery(t); low = pct < 10; c = (255, 84, 70) if low else wh
    bw, bh = (88, 40) if V else (76, 34); bx = W - (72 if V else 64) - bw; by = y0 - bh + 4
    if on(t, 'm1', 0.0, 0.5):                                # Mia pili gosterir
        cv.drawRRect(RRXY(LTRB(bx - 130, by - 16, bx + bw + 24, by + bh + 16), 14, 14), stroke(YEL, 6, 255 if int(t * 5) % 2 == 0 else 120))
    if not (low and int(t * 3) % 2):
        cv.drawRRect(RRXY(LTRB(bx, by, bx + bw, by + bh), 7, 7), stroke(c, 4)); cv.drawRect(LTRB(bx + bw + 3, by + bh * 0.3, bx + bw + 9, by + bh * 0.7), fill(c))
        cv.drawRect(LTRB(bx + 7, by + 7, bx + 7 + (bw - 14) * max(0.06, pct / 100.0), by + bh - 7), fill(c))
    htext(cv, f'%{pct}', bx - 14, y0, fs * 0.86, c, TFM, right=True)


CUTS = sorted(v for n_, v in TL.scenes.items() if 3 <= n_ <= 27)
def glitch(cv, t):
    """kayit kesmesi: iki kare yatay bozulma seritleri"""
    for a in CUTS:
        d = t - a
        if 0 <= d < 0.14:
            n = int(d * 24)
            for j in range(5):
                y = (j * 397 + int(a * 100) * 31 + n * 211) % H; h = 10 + (j * 37 + n * 13) % 46
                cv.drawRect(LTRB(0, y, W, y + h), fill((255, 255, 255) if j % 2 else (8, 10, 22), 60 if j % 2 else 150))


def hook2(cv, t, a=1.0):
    """ilk karedeki iki satirlik kanca yazisi"""
    if a <= 0: return
    size, cx, ys = (124, W / 2, (346, 486)) if V else (80, 1190, (196, 290))
    sc_ = lerp(1.25, 1.0, smooth(seg(t, 0, 0.3)))
    for s, y in zip(('BİLETİ ATTI', 'GERİ GELDİ'), ys):
        f = skia.Font(TFB, size * sc_); f.setEmbolden(True); w = f.measureText(s); x = cx - w / 2
        st = stroke((0, 0, 0), size * 0.2, 255 * a); st.setStrokeJoin(skia.Paint.kRound_Join)
        cv.drawString(s, x + 5, y + 10, f, fill((0, 0, 0), 120 * a)); cv.drawString(s, x, y, f, st); cv.drawString(s, x, y, f, fill((255, 214, 80), 255 * a))


def hud(cv, t, k):
    if t < HK: hook2(cv, t, 1 - seg(t, HK - 0.12, HK))
    if t < REC1: rec_hud(cv, t); glitch(cv, t)
    if k == 28: abone(cv, t, REC1 + ABONE_END, pos=(W / 2, 1500) if V else (W / 2, 800))


def title_card(cv, t):
    tb = B('title'); a = seg(t, tb[0], tb[0] + 0.35)
    if a > 0:
        dim(cv, 0.5 * a)
        card(cv, [(TITLE, 112, RED), (f'{EP.title()}: {EP_NAME}', 48, CREAM)], a, lerp(0.9, 1.0, smooth(seg(t, tb[0], tb[0] + 0.5))))


# ---------- ozcekim: arka plan + arkadakiler + onde buyuk karakter ----------
def sel(cv, ts, k, bg, st, F_, who='R'):
    """bg(): arka plan. st: {kim: (ifade, poz, bakis[, ek])} arkadakiler. F_: ondeki karakter (ifade, poz, bakis[, ek])"""
    bg()
    with stage(cv):
        if st: people(cv, ts, {w: BEHIND[w] for w in st}, st)
        kw = dict(F_[3]) if len(F_) > 3 else {}
        return actor(cv, ts, who, F_[0], dict(SELF, **(F_[1] or {})), F_[2], place=(RX, RGY, RS), **kw)


def rear4(cv, ts, k): door_view(cv, k, gone=1.0, scroll=SC(ts), no=5)                      # dort numaranin arka kapisi: ardi bos ray
def rear3(cv, ts, k, hi=1.0): door_view(cv, k, gone=0.0, scroll=SC(ts), plate_hi=hi, no=4)   # uc numaranin arka kapisi: ardinda dort numara
def rear1(cv, ts, k): door_view(cv, k, gone=0.0, scroll=SC(ts), no=2)                      # bir numaranin arka kapisi
def fwd(cv, ts, k, label, open_u=0.0, loco=False, sh=(0, 0), hi=0.0):
    door_view(cv, k, scroll=-SC(ts), label=label, glass=loco_glass if loco else fwd_glass, open_u=open_u, lock=loco, shake=sh, plate_hi=hi)


def pocket_shot(cv, ts, k):
    """ozcekim, uc numara: el cebe gider, bilet saglam cikar (kancada da kullanilir)"""
    o = ts - B('pocket')[0]; has = o >= POCK
    if o < 0.3: pose = mixpose({}, POCKET, seg(o, 0.05, 0.3))
    else: pose = mixpose(POCKET, SHOWB, seg(o, POCK, POCK + 0.3))
    ex = 'bagir' if on(ts, 'r10', 0.0, 0.1) else ('saskin' if has else 'merak')
    st = {'M': ('saskin' if has else 'endise', LEAN_IN if has else {}, -1.6), 'D': ('sakin', KNIT, -1.4, dict(prop='knit'))}
    sel(cv, ts, k, lambda: rear3(cv, ts, k), st, (ex, pose, 0 if has else 1.2, dict(prop='ticket') if has else {}))


# ============ SAHNE 1: kanca (ozcekim: attigi bilet cebinden cikar) ============
def scene1(cv, t):
    ts, k = step(t), kk(t)
    pocket_shot(cv, S('r10') + min(ts, E('r10') - S('r10') + 0.3), k)
    flash(cv, 0.8 * seg(t, HK - 0.12, HK))


# ============ SAHNE 2: kayit baslar (dort numara); sonra arka kapinin cami: bos ray ============
def scene2(cv, t):
    ts, k = step(t), kk(t)
    cut = frac('r1', 0.37)
    if ts < cut:
        st = {'M': ('endise', {}, -1.2), 'D': ('sakin', KNIT, 0, dict(prop='knit'))}
        sel(cv, ts, k, lambda: rear4(cv, ts, k), st, ('endise', {}, 0))
    else:
        u = smooth(seg(ts, cut, E('r1')))
        with zoom(cv, lerp(1.45, 1.75, u), (540, 840), (540, 880) if V else (540, 960)): rear4(cv, ts, k)
    flash(cv, 0.8 * (1 - seg(t, HK, HK + 0.2)))


# ============ SAHNE 3: biletler kameraya; baslik ============
def scene3(cv, t):
    ts, k = step(t), kk(t)
    st = {'M': ('endise', {}, -1.2), 'D': ('sakin', KNIT, 0, dict(prop='knit'))}
    sel(cv, ts, k, lambda: rear4(cv, ts, k), st, ('endise', {}, 0.8))
    dim(cv, 0.5)
    a1 = seg(ts, S('r2') - 0.1, S('r2') + 0.25); mv = smooth(seg(ts, S('r3') - 0.4, S('r3') - 0.05)); a2 = seg(ts, S('r3') - 0.1, S('r3') + 0.25)
    if V: big, s1, s2 = (540, 620, 820), (540, 440, 620), (540, 790, 620)
    else: big, s1, s2 = (960, 360, 680), (620, 330, 560), (1300, 330, 560)
    cx, cy, w = lerpt(big, s1, mv)
    ticket(cv, cx, cy, w, SKYB, 'ELI', 'KARAKÖPRÜ', a1, rot=lerp(-3, 0, mv))
    ticket(cv, s2[0], s2[1], s2[2], GREENC, 'REN', STN, a2, rot=2)
    title_card(cv, t)


# ============ SAHNE 4: kamera Mia'da, sonra Ada'da (yakin) ============
XM4, XD4, CAM4 = 1500, 1900, 1300
def scene4(cv, t):
    ts, k = step(t), kk(t)
    onM = ts < frac('r4', 0.46)
    st = {'M': ('mutlu' if onM else 'sakin', SHOWB if onM else {}, 0 if onM else 1.5, dict(prop='ticket') if onM else {}),
          'D': ('mutlu' if ts >= frac('r4', 0.46) else 'sakin', dict(KNIT, lean=alt(k, 0, 3, 4)), 0 if ts < S('d1') else -0.5, dict(prop='knit'))}
    with zoom(cv, 1.45 if V else 1.5, ((XM4 if onM else XD4) - CAM4 + (40 if onM else 0), 960), (540, 1000) if V else (540, 1010)):
        wagon(cv, CAM4, 4, k, scroll=SC(ts))
        with stage(cv): people(cv, ts, pl(CAM4, M=XM4, D=XD4), st)


# ============ SAHNE 5: ikisi birden: pil ============
def scene5(cv, t):
    ts, k = step(t), kk(t)
    st = {'M': ('endise' if on(ts, 'm1') else 'yorgun', UPR if on(ts, 'm1') else HIP, 1.0 if on(ts, 'm1') else 0),
          'D': ('sakin', KNIT, -1.2 if on(ts, 'm1') else 0, dict(prop='knit'))}
    with zoom(cv, 1.2 if V else 1.0, (540, 1000), QW):
        wagon(cv, CAM4 - 150, 4, k, scroll=SC(ts))
        with stage(cv): people(cv, ts, pl(CAM4 - 150, M=XM4, D=XD4), st)


# ============ SAHNE 6: anons: hoparlor ve levha (VAGON 4 kirmizi yanar) ============
def scene6(cv, t):
    ts, k = step(t), kk(t)
    lv = TL.talk('A', ts); ch = B('chime'); late = ts >= frac('a1', 0.56)
    sh = jit(k, 2.5) if ch[0] <= ts < ch[0] + 0.8 else (0, 0)
    z, p = ((2.75, (640, 615)) if V else (2.4, (640, 630))) if late else ((2.1, (560, 650)) if V else (1.9, (560, 650)))
    with zoom(cv, z, p, (540 + sh[0], 800 + sh[1]) if V else (540 + sh[0], 960 + sh[1])):
        wagon(cv, 1900, 4, k, scroll=SC(ts), spk=lv if lv is not None else (0.5 if ch[0] <= ts < ch[0] + 0.8 else None), plate_hi=1.0 if late else 0.0)


# ============ SAHNE 7: ozcekim: dort numara bizim vagon ============
def scene7(cv, t):
    ts, k = step(t), kk(t)
    first = ts < frac('r6', 0.3)
    st = {'M': ('endise', {}, 1.5), 'D': ('sakin', KNIT, 0, dict(prop='knit'))}
    sel(cv, ts, k, lambda: rear4(cv, ts, k), st, ('saskin' if first else 'endise', {} if first else DOWNP, 0))


# ============ SAHNE 8: kural; one yururler ============
XM8, XD8, CAM8 = 2100, 1750, 1560
def scene8(cv, t):
    ts, k = step(t), kk(t)
    go = max(0.0, ts - frac('m2', 0.5)); xm = XM8 + 320 * go; xd = XD8 + 210 * max(0.0, go - 0.3)
    if on(ts, 'd2'): D_ = ('kararli', POINTUP, 1.2)
    elif xd > XD8: D_ = ('kararli', walk(xd - XD8, 0.64, 1), 2)
    else: D_ = ('sakin', KNIT, 1.5, dict(prop='knit'))
    if xm > XM8: M_ = ('kararli', walk(xm - XM8, 0.70, 1, run=True), 2, dict(alpha=1 - seg(xm, 2440, 2540)))
    else: M_ = ('kararli' if on(ts, 'm2') else 'endise', FWD if on(ts, 'm2') else {}, 1.6 if on(ts, 'm2') else -1.5)
    with zoom(cv, 0.9 if V else 1.0, (540, 1000), QW):
        wagon(cv, CAM8, 4, k, scroll=SC(ts), plate_hi=1.0, door_f=smooth(seg(ts, S('m2'), frac('m2', 0.6))))
        with stage(cv): people(cv, ts, pl(CAM8, M=xm, D=xd), {'M': M_, 'D': D_})
    a = min(seg(ts, frac('d2', 0.3), frac('d2', 0.3) + 0.3), 1 - seg(ts, E('d2') + 0.2, E('d2') + 0.5))
    card(cv, [('KURAL', 38, AMBER), ('Tren durduğunda', 54, CREAM), ('son vagonda olma', 54, RED)], a, lerp(0.92, 1.0, smooth(a)), cy=560 if V else 250)


# ============ SAHNE 9: koruk (dortten uce) ============
def scene9(cv, t):
    ts, k = step(t), kk(t)
    o = ts - B('gang')[0]; gy = NEAR - 10
    def cross(x0, x1, a, b, s, run=False):
        u = seg(o, a, b); x = lerp(x0, x1, u); return x, (walk(x - x0, s, 1, run=run) if 0 < u < 1 else {})
    xm, Wm = cross(260, 1180, 0.0, 2.0, 0.70, True); xd, Wd = cross(-170, 760, 0.15, 2.8, 0.64)
    gangway(cv, k, SC(ts), 3, nos=(4, 3), hi=(1.0, 0.0))
    with stage(cv):
        people(cv, ts, {'M': (xm, gy, 0.70), 'D': (xd, FAR + 38, 0.64)},
               {'M': ('kararli', Wm, 2, dict(alpha=1 - seg(xm, 1060, 1170))), 'D': ('kararli', Wd, 2)})


# ============ SAHNE 10: uc numara (ozcekim): plan; bileti yirtar ============
def torn_ticket(cv, cx, cy, w, sp):
    """ikiye yirtilan bilet (ekran koordinati). sp 0..1: parcalar ayrilir"""
    h = 380 * w / 760
    zig = [(cx + (16 if j % 2 else -16), cy - h / 2 - 30 + j * (h + 60) / 8) for j in range(9)]
    for sd in (-1, 1):
        cv.save(); cv.translate(sd * 70 * sp, 14 * sp); cv.rotate(sd * 10 * sp, cx + sd * w / 4, cy)
        p = skia.Path(); p.moveTo(*zig[0])
        for q in zig[1:]: p.lineTo(*q)
        p.lineTo(cx + sd * (w / 2 + 60), cy + h / 2 + 30); p.lineTo(cx + sd * (w / 2 + 60), cy - h / 2 - 30); p.close()
        cv.clipPath(p, True); ticket(cv, cx, cy, w, GREENC, 'REN', STN, 1.0); cv.restore()


def scene10(cv, t):
    ts, k = step(t), kk(t)
    tr = B('tear'); o = ts - tr[0]
    if tr[0] <= ts < tr[1]:                                  # yakin: iki el, bilet ikiye ayrilir
        sp = smooth(seg(o, TEAR, TEAR + 0.35))
        with zoom(cv, 2.2, (540, 1500), (540, 1100) if V else (540, 1150)): rear3(cv, ts, k)
        dim(cv, 0.35)
        cx, cy, w = (540, 760, 780) if V else (960, 500, 760)
        sh = jit(k, 5) if TEAR - 0.25 <= o < TEAR else (0, 0)
        cv.save(); cv.translate(*sh)
        if o < TEAR: ticket(cv, cx, cy, w, GREENC, 'REN', STN, 1.0, rot=-2)
        else: torn_ticket(cv, cx, cy, w, sp)
        hh = 380 * w / 760
        for sd in (-1, 1):                                   # eller: biletin alt koselerinde
            hx_, hy_ = cx + sd * (w * 0.33 + 70 * sp), cy + hh * 0.42 + 14 * sp
            yarn_limb(cv, [(cx + sd * w * 0.62, H + 60), (cx + sd * (w * 0.5 + 40 * sp), cy + hh * 1.1), (hx_, hy_ + 30)], 96, GREENC)
            hand_ball(cv, hx_, hy_, 62, GREENC, seed=5 + sd)
        cv.restore()
        if TEAR <= o < TEAR + 0.6: sfx_text(cv, cx, cy - hh * 0.72, 'CIRT', 92, a=1 - seg(o, TEAR + 0.3, TEAR + 0.6))
        return
    torn = ts >= tr[1]
    if not torn: R_ = ('kararli', SHOWB, 0, dict(prop='ticket'))
    elif ts < S('r8') - 0.1: R_ = ('kararli', SHOWB, 0.8)
    else: R_ = ('kararli', POINTB, 2 if ts >= frac('r8', 0.45) else 0)
    st = {'M': ('merak', HIP if on(ts, 'm3') else {}, -1.5), 'D': ('sakin', KNIT, -1.2, dict(prop='knit'))}
    f = sel(cv, ts, k, lambda: rear3(cv, ts, k), st, R_)
    if torn and ts < S('r8') - 0.1:                          # elinde iki parca
        with stage(cv):
            hx_, hy_ = f['handR']
            mini_ticket(cv, hx_ - 26, hy_ - 64, 1.5, rot=-24, c=GREENC); mini_ticket(cv, hx_ + 70, hy_ - 50, 1.5, rot=18, c=GREENC)


# ============ SAHNE 11: pencere: parcalar camdan ucar ============
CAM11 = 770                                                # ortadaki pencere sahnede x 400-680
def scene11(cv, t):
    ts, k = step(t), kk(t)
    th = B('throw'); o = ts - th[0]
    u_in = smooth(seg(o, 0.15, 0.7)); fl = smooth(seg(o, THROW - 0.12, THROW + 0.1))
    wave = alt(k, -16, 16, 3) if on(ts, 'r9', 0.0, 0.0) and ts < frac('r9', 0.6) else 0
    hx_, hy_ = 640 + 150 * (1 - u_in) - 50 * fl + wave, 900 + 210 * (1 - u_in) - 26 * fl - abs(wave) * 0.6
    with zoom(cv, 2.0 if V else 1.7, (540, 840), (540, 820) if V else (540, 990)):
        wagon(cv, CAM11, 3, k, scroll=SC(ts), last=False)
        with stage(cv):
            cv.save(); cv.clipRect(LTRB(404, 694, 676, 956))
            for j in range(6):                               # ruzgar cizgileri: cam acik
                x = 700 - ((k * 46 + j * 97) % 330); y = 716 + j * 41
                cv.drawLine(x, y, x - 60, y, stroke((226, 232, 244), 4, 110))
            if o >= THROW:                                   # parcalar geriye (sola) savrulur
                tau = o - THROW
                for j in range(7):
                    px = 590 - (430 + 70 * j) * tau; py = 874 + (-60 + 34 * j) * tau + 16 * math.sin(tau * 9 + j)
                    cv.save(); cv.translate(px, py); cv.rotate(j * 50 + tau * 420)
                    cv.drawRect(LTRB(-16, -10, 16, 10), fill(PAPER, 255 * (1 - seg(tau, 0.5, 0.95)))); cv.drawRect(LTRB(-16, -10, -8, 10), fill(GREENC, 255 * (1 - seg(tau, 0.5, 0.95)))); cv.restore()
            cv.restore()
            yarn_limb(cv, [(hx_ + 250, 1260), (hx_ + 130, 1060), (hx_ + 14, hy_ + 16)], 54, GREENC)
            hand_ball(cv, hx_, hy_, 34, GREENC)
            if o < THROW:
                mini_ticket(cv, hx_ - 24, hy_ - 30, 0.9, rot=-24, c=GREENC); mini_ticket(cv, hx_ + 22, hy_ - 36, 0.9, rot=16, c=GREENC)


# ============ SAHNE 12: Mia: "cebine bak" ============
def scene12(cv, t):
    ts, k = step(t), kk(t)
    st = {'M': ('saskin', dict(aR=(110, 100, 204, 150)), 1.6), 'D': ('merak', KNIT, 1.5, dict(prop='knit'))}
    with zoom(cv, 1.45 if V else 1.5, (XM4 - CAM4 + 90, 960), (540, 1000) if V else (540, 1010)):
        wagon(cv, CAM4, 3, k, scroll=SC(ts), last=False)
        with stage(cv): people(cv, ts, {'M': (XM4 - CAM4, NEAR, 0.70), 'D': (XM4 - CAM4 - 330, FAR, 0.64)}, st)


# ============ SAHNE 13: ozcekim: bilet cebinde ============
def scene13(cv, t):
    ts, k = step(t), kk(t)
    pocket_shot(cv, ts, k)


# ============ SAHNE 14: Ada (yakin) ve saglam bilet ============
def scene14(cv, t):
    ts, k = step(t), kk(t)
    st = {'D': ('sakin', dict(KNIT, lean=alt(k, 0, 3, 4)), 1.2, dict(prop='knit')), 'M': ('endise', {}, 1.6)}
    with zoom(cv, 1.45 if V else 1.5, (XM4 - CAM4 - 330 + 60, 950), (540, 1010) if V else (540, 1010)):
        wagon(cv, CAM4, 3, k, scroll=SC(ts), last=False)
        with stage(cv): people(cv, ts, {'M': (XM4 - CAM4 + 60, NEAR, 0.70), 'D': (XM4 - CAM4 - 330, FAR + 60, 0.64)}, st)
    a = seg(ts, frac('d3', 0.42), frac('d3', 0.42) + 0.25)
    if V: ticket(cv, 540, 500, 640, GREENC, 'REN', STN, a, rot=-3)
    else: ticket(cv, 440, 340, 540, GREENC, 'REN', STN, a, rot=-3)


# ============ SAHNE 15: ozcekim: kacis karari ============
def scene15(cv, t):
    ts, k = step(t), kk(t)
    late = ts >= frac('r11', 0.42)
    st = {'M': ('endise', REACH_L if late else {}, -1.6), 'D': ('endise', KNIT, -1.4, dict(prop='knit'))}
    sel(cv, ts, k, lambda: rear3(cv, ts, k), st, ('panik' if not late else 'kararli', POINTB if late else dict(SHOWB), 2 if late else 0, {} if late else dict(prop='ticket')))


# ============ SAHNE 16: one kosu: kapilar (VAGON 2, VAGON 1), sonra lokomotif ============
def scene16(cv, t):
    ts, k = step(t), kk(t)
    o = ts - B('run')[0]; bob = (0, 7 * math.sin(ts * 15)) if o > 0 else (0, 0)
    if o < RUSH[0][1]: lab, op, u = 'VAGON 2', smooth(seg(ts, S('m5') + 0.15, S('m5') + 0.8)), seg(o, *RUSH[0])
    elif o < RUSH[1][1]: lab, op, u = 'VAGON 1', smooth(seg(o, RUSH[0][1] + 0.05, RUSH[0][1] + 0.4)), seg(o, *RUSH[1])
    else: lab = None
    if lab:
        with zoom(cv, 1 + 2.6 * u * u, (540, 930)): fwd(cv, ts, k, lab, op, sh=bob)
        flash(cv, 0.6 * seg(u, 0.8, 1.0))
        if lab == 'VAGON 1': flash(cv, 0.6 * (1 - seg(o, RUSH[0][1], RUSH[0][1] + 0.15)))
    else:
        v = smooth(seg(o, RUSH[1][1], RUSH[1][1] + 0.7))
        with zoom(cv, lerp(1.4, 1.0, v), (540, 930)): fwd(cv, ts, k, 'LOKOMOTİF', loco=True, sh=(0, bob[1] * (1 - v)))
        flash(cv, 0.6 * (1 - seg(o, RUSH[1][1], RUSH[1][1] + 0.15)))


# ============ SAHNE 17: lokomotifin kapisi: kilitli ============
def scene17(cv, t):
    ts, k = step(t), kk(t)
    o = ts - B('lock')[0]
    hit = any(0 <= o - x < 0.22 for x in LOCKS)
    sh = jit(k, 5) if hit else (0, 0)
    close = ts >= frac('r12', 0.52)
    def draw():
        fwd(cv, ts, k, 'LOKOMOTİF', loco=True, sh=sh, hi=1.0 if o >= LOCKS[-1] + 0.2 and not close else 0.0)
        with stage(cv, *sh):
            if not close:
                rch = smooth(seg(o, 0.0, 0.35)); hx_, hy_ = 690 + (-8 if hit else 0), 1096 + 420 * (1 - rch) + (6 if hit else 0)
                yarn_limb(cv, [(930, 1700 + 420 * (1 - rch)), (840, 1400 + 420 * (1 - rch)), (hx_ + 20, hy_ + 26)], 84, GREENC)
                hand_ball(cv, hx_, hy_, 46, GREENC)
            for j, x in enumerate(LOCKS):
                if 0 <= o - x < 0.3: sfx_text(cv, 800 + 30 * (j % 2), 1000 - 40 * j, 'TAK', 62, a=1 - seg(o - x, 0.15, 0.3))
            if o >= LOCKS[-1] + 0.2 and not close:
                a = 1.0 if (k // 3) % 2 == 0 else 0.6
                sfx_text(cv, 540, 1056, 'KİLİTLİ', 70, c=RED, rot=-4, a=a, rays=False)
    if close:
        with zoom(cv, 1.55, (540, 850), (540, 880) if V else (540, 960)): draw()
    else: draw()


# ============ SAHNE 18: bir numara (ozcekim): rahatlama ============
def scene18(cv, t):
    ts, k = step(t), kk(t)
    st = {'M': ('sakin', CALM if on(ts, 'm6') else HIP, -1.4)}
    R_ = ('yorgun', SLUMP if ts < S('r13') - 0.1 else dict(aR=(150, 60, 200, -70)), 1.2 if ts < S('r13') - 0.1 else 0)
    sel(cv, ts, k, lambda: rear1(cv, ts, k), st, R_)


# ============ SAHNE 19: pencerede degirmen; yokus ============
CAM19 = 1190                                               # dorduncu pencere sahnede x 400-680
def mill_out(cv, ts, k):
    """pencerenin ardi: tepede yel degirmeni, yamacta istasyonun isiklari"""
    night(cv, SC(ts), k, y_h=940, moon=(450, 742), poles=False)
    hx = 590 - (SC(ts) - SC(B('mill')[0])) * 0.035
    p = skia.Path(); p.moveTo(-600, 1010); p.quadTo(hx - 230, 930, hx, 866); p.quadTo(hx + 250, 920, 1700, 1000); p.lineTo(1700, 1300); p.lineTo(-600, 1300); p.close()
    cv.drawPath(p, fill((14, 22, 46))); cv.drawPath(p, dashed((70, 84, 124), 3, 160, (12, 10)))
    bx, by = hx, 870
    poly(cv, [(bx - 24, by + 4), (bx + 24, by + 4), (bx + 15, by - 70), (bx - 15, by - 70)], (52, 62, 96))
    poly(cv, [(bx - 21, by - 70), (bx + 21, by - 70), (bx, by - 96)], (110, 50, 62))
    cv.drawRRect(RRXY(LTRB(bx - 6, by - 46, bx + 6, by - 26), 3, 3), fill((250, 214, 120)))
    hub = (bx, by - 76)
    for j in range(4):
        a_ = math.radians(k * 2.4 + j * 90); c_, s_ = math.cos(a_), math.sin(a_)
        tip = (hub[0] + c_ * 66, hub[1] + s_ * 66); n_ = (-s_ * 15, c_ * 15)
        poly(cv, [(hub[0] + c_ * 18, hub[1] + s_ * 18), tip, (tip[0] + n_[0], tip[1] + n_[1]), (hub[0] + c_ * 18 + n_[0], hub[1] + s_ * 18 + n_[1])], CREAM, 215)
        cv.drawLine(hub[0], hub[1], tip[0], tip[1], stroke((196, 202, 222), 4))
    cv.drawCircle(hub[0], hub[1], 6, fill(BRASS))
    for j in range(5):                                       # yamacta istasyon lambalari
        lx_, ly_ = hx - 210 + j * 44, 934 - j * 9
        gl = fill((255, 226, 150), 120); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 7)); cv.drawCircle(lx_, ly_, 9, gl); cv.drawCircle(lx_, ly_, 3.5, fill((255, 240, 200)))


def scene19(cv, t):
    ts, k = step(t), kk(t)
    wide = ts >= S('r14') - 0.15
    tilt = -3.2 * smooth(seg(ts, B('mill')[0], B('mill')[0] + 1.4))
    sl = smooth(seg(ts, frac('r14', 0.15), E('r14') + 0.4)); bx = 800 - 520 * sl * sl          # bavul arkaya kayar
    if on(ts, 'm7'): M_ = ('saskin', UPR, 1.6)
    elif wide: M_ = ('endise', dict(REACH_L, lean=-8), 1.0 if sl < 0.3 else -1.4)
    else: M_ = ('merak', {}, 1.6)
    cv.save(); cv.translate(W / 2, H / 2); cv.rotate(tilt); cv.scale(1.07, 1.07); cv.translate(-W / 2, -H / 2)
    zz = (0.95 if V else 1.05, (540, 1000), QW) if wide else ((1.5, (430, 870), (540, 900)) if V else (1.5, (470, 880), (540, 980)))
    with zoom(cv, *zz):
        wagon(cv, CAM19, 1, k, scroll=SC(ts), last=False, out=lambda c: mill_out(c, ts, k))
        with stage(cv):
            people(cv, ts, {'M': (215, NEAR, 0.70)}, {'M': M_})
            if wide:                                         # yolluk halida kayan bavul
                y = NEAR + 6; rc = LTRB(bx - 70, y - 96, bx + 70, y)
                cv.drawRRect(RRXY(rc.makeOffset(5, 6), 12, 12), fill((4, 6, 20), 90)); cv.drawRRect(RRXY(rc, 12, 12), fill((70, 110, 100)))
                cv.drawRRect(RRXY(rc.makeInset(9, 9), 7, 7), dashed((150, 190, 180), 2.5, 200, (10, 8)))
                hd = skia.Path(); hd.addArc(LTRB(bx - 26, y - 122, bx + 26, y - 78), 180, 180); cv.drawPath(hd, stroke((40, 66, 60), 8))
                for j in range(3): cv.drawLine(bx + 84 + j * 26, y - 70 + j * 24, bx + 124 + j * 26, y - 70 + j * 24, stroke(CREAM, 4, 150 * sl * (1 - sl) * 4))
    cv.restore()


# ============ SAHNE 20: ozcekim: Ada yok ============
def scene20(cv, t):
    ts, k = step(t), kk(t)
    st = {'M': ('endise', {}, -2 if (k // 8) % 2 == 0 else 1.6)}
    sel(cv, ts, k, lambda: rear1(cv, ts, k), st, ('endise' if ts < frac('m8', 0.5) else 'saskin', {}, 1.4 if ts < frac('m8', 0.5) else -1.2))


# ============ SAHNE 21: uc numara: bos koltuk, ip arka kapiya (dort numaraya) gidiyor ============
def yarn_strand(cv, pts, w=6):
    p = skia.Path(); p.moveTo(*pts[0])
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]; p.quadTo((x0 + x1) / 2, (y0 + y1) / 2 + (9 if i % 2 else -9), x1, y1)
    cv.drawPath(p, stroke(shade(CORAL, 0.7), w + 3)); cv.drawPath(p, stroke(CORAL, w)); cv.drawPath(p, dashed(shade(CORAL, 1.35), 2, 200, (8, 7)))


def scene21(cv, t):
    ts, k = step(t), kk(t)
    yn = B('yarn'); cam = lerp(1100, -60, smooth(seg(ts, yn[0] + 0.25, yn[0] + 2.3)))
    X = lambda x: x - cam
    close = frac('r15', 0.5) <= ts < S('m9') - 0.1
    om = ts - S('m9'); xm = lerp(1180, 520, smooth(seg(om, -0.5, 0.35))) if om < frac('m9', 0.62) - S('m9') else 520 - 330 * (ts - frac('m9', 0.62))
    if om < -0.5: M_ = None
    elif xm > 520 and om < 0.35: M_ = ('panik', walk(1180 - xm, 0.70, -1, run=True), -2)
    elif xm < 520: M_ = ('panik', walk(520 - xm, 0.70, -1, run=True), -2, dict(alpha=1 - seg(xm, 300, 200) if xm < 300 else 1.0))
    else: M_ = ('panik', REACH_L, -2)
    def draw():
        wagon(cv, cam, 3, k, scroll=SC(ts), last=False, door_r=1.0)
        with stage(cv):
            plate(cv, X(145), 598, 'VAGON 4', 1.0, k)
            sx_, sy_ = seat_xy(2, 1)                           # koltukta yarim orgu ve sisler
            poly(cv, [(X(sx_) - 54, sy_ - 70), (X(sx_) + 40, sy_ - 78), (X(sx_) + 52, sy_ - 2), (X(sx_) - 46, sy_ + 2)], CREAM)
            for j in range(1, 4): cv.drawLine(X(sx_) - 48, sy_ - 70 + j * 18, X(sx_) + 44, sy_ - 76 + j * 18, dashed(CORAL, 3, 210, (7, 6)))
            cv.drawLine(X(sx_) - 70, sy_ - 50, X(sx_) + 60, sy_ - 96, stroke((120, 110, 130), 5)); cv.drawLine(X(sx_) + 70, sy_ - 44, X(sx_) - 50, sy_ - 100, stroke((120, 110, 130), 5))
            pts = [(X(sx_) - 40, sy_), (X(sx_) - 90, 1200), (X(sx_) - 130, 1296)] + [(X(x), 1296 + (6 if (x // 160) % 2 else -4)) for x in range(int(sx_) - 290, 120, -160)] + [(X(120), 1288)]
            yarn_strand(cv, pts)
            if M_: people(cv, ts, {'M': (xm, NEAR, 0.70)}, {'M': M_})
    if close:
        with zoom(cv, 1.5 if V else 1.25, (X(170), 1010 if V else 930), (540, 1000) if V else (540, 1010)): draw()
    else:
        with zoom(cv, 1.15 if V else 1.0, (540, 1000), QW): draw()


# ============ SAHNE 22: dort numara: Ada yumagin pesinde; fren, lambalar soner ============
CAM22, XA22 = 1500, 2085
def scene22(cv, t):
    ts, k = step(t), kk(t)
    st0 = B('stop')[0]; o = ts - st0
    offs = [st0 + LAMP_OFF[0], st0 + LAMP_OFF[0], st0 + LAMP_OFF[1], st0 + LAMP_OFF[2], 1e9]
    def Lf(i):
        d = ts - offs[i]
        return 1.0 if d < 0 else (0.55 if d < 0.16 and (k % 2) else 0.0)
    X = lambda x: x - CAM22
    got = ts >= frac('d4', 0.3)                              # yumagi yerden aldi
    pull = smooth(seg(ts, S('r17') + 0.1, S('r17') + 0.5))   # Ren'in kolu uzanir
    xa = XA22 + 250 * smooth(seg(o, 0.2, 2.0))
    if not got: D_ = ('merak', BENDL, -2)
    elif ts < S('r17'): D_ = ('sakin', dict(aL=(-110, 70, -176, -30)), 1.5)
    elif o < 0.2: D_ = ('saskin', dict(aL=(-110, 70, -176, -30), aR=(110, 100, 190, 60)), 1.5)
    else: D_ = ('endise', dict(walk(xa - XA22, 0.64, 1, scared=True), aR=(110, 100, 190, 60)), 2 if o < LAMP_OFF[1] else -2)
    sh = jit(k, 4) if 1.65 <= o < 1.95 else (0, 0)
    def draw():
        wagon(cv, CAM22, 4, k, scroll=SC(ts), lamps=Lf, door_f=1.0, plate_hi=1.0)
        with stage(cv):
            bx_, by_ = X(1965), 1316
            yarn_strand(cv, [(X(2470), 1290)] + [(X(x), 1296 + (6 if (x // 150) % 2 else -4)) for x in range(2380, 2010, -150)] + ([(bx_ + 10, by_)] if not got else []))
            f = people(cv, ts, {'D': (X(xa), NEAR, 0.64)}, {'D': D_})['D']
            if got: hand_ball(cv, f['handL'][0] - 6, f['handL'][1] - 10, 26, CORAL, seed=9)
            else: hand_ball(cv, bx_, by_, 26, CORAL, seed=9)
            if pull > 0:                                     # Ren'in kolu (kamera onda): Ada'yi kolundan ceker
                hx_, hy_ = f['handR'][0] + 20, f['handR'][1] + 4
                ex = hx_ + 620 * (1 - pull)
                yarn_limb(cv, [(ex + 760, hy_ + 330), (ex + 360, hy_ + 150), (ex + 34, hy_ + 10)], 60, GREENC); hand_ball(cv, ex, hy_, 36, GREENC)
        wagon_dark(cv, CAM22, Lf)
    cv.save(); cv.translate(sh[0], sh[1])
    if S('d4') - 0.1 <= ts < st0:
        with zoom(cv, 1.4 if V else 1.45, (X(XA22) + 40, 960), (540, 1000) if V else (540, 1010)): draw()
    else:
        with zoom(cv, 1.1 if V else 1.0, (560, 1000), QW): draw()
    cv.restore()


# ============ telefon yerde: egik ve alcak kadraj (koruk) ============
TILT = -8.0
class floorcam:
    """yere dusen telefonun kadraji. sx, sy: sahnenin kaydirilmasi (ekran pikseli)"""
    def __init__(s, cv, sx=0.0, z=1.16, ang=TILT, sy=None): s.cv, s.sx, s.z, s.ang, s.sy = cv, sx, z, ang, (-170 if V else -40) if sy is None else sy
    def __enter__(s):
        s.cv.save(); s.cv.translate(W / 2, H / 2); s.cv.rotate(s.ang); s.cv.scale(s.z, s.z); s.cv.translate(-W / 2 + s.sx, -H / 2 + s.sy)
    def __exit__(s, *a): s.cv.restore()
SX0 = 360 if V else 60                                     # Ren, kapi ve pencere kadrajda
SX1 = 0 if V else 20                                       # vagon gidince: Mia ile Ada kadrajda
GYG = NEAR - 10


def stn_out(cv, k): station_bg(cv, STN, -140, k, bw=112, by=800)
def stn_out_r(cv, k): station_bg(cv, STN, 2400, k, bw=112, by=800)


def left_dark(cv, a):
    """kapinin ardindaki (soldaki) vagon kararir"""
    if a <= 0: return
    p = fill((5, 7, 20), 255 * clamp(a)); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26))
    cv.drawRect(LTRB(-900, ROOF - 60, GL - 30, FEDGE + 90), p)


# ============ SAHNE 23: itis; telefon yere duser; kapi kapanir ============
def scene23(cv, t):
    ts, k = step(t), kk(t)
    ps, dr = B('push')[0], B('door')[0]; o, od = ts - ps, ts - dr
    fall = seg(o, 0.0, FALL)
    ang = lerp(64, TILT, 1 - (1 - fall) ** 2) + (5 * math.sin((o - FALL) * 30) * math.exp(-(o - FALL) * 9) if o >= FALL else 0)
    z = lerp(1.7, 1.16, smooth(fall))
    closed = seg(od, 0.1, SHUT)
    xa = lerp(240, 560, smooth(seg(o, 0.0, 1.2)))
    if o < 1.2: D_ = ('panik', walk(xa - 240, 0.64, 1, scared=True), 2)
    elif ts < dr + SHUT: D_ = ('bagir' if on(ts, 'd5', 0, 0.05) else 'panik', REACH_L, -2)
    else: D_ = ('panik', COWER, -2)
    if o < 1.0: R_ = ('kararli', dict(aR=(130, 50, 236, 40), aL=(60, 80, 214, 70), lean=16), 2)
    elif ts < dr + 0.1: R_ = ('endise', {}, 2)
    elif ts < S('m10'): R_ = ('saskin', dict(aR=(120, 70, 170, 20)), 2)
    else: R_ = ('endise', dict(aR=(120, 90, 180, 60), lean=alt(k, 4, 9, 2)), 2)             # kolu cevirir
    xm = lerp(1000, 690, smooth(seg(o, 0.3, 1.2))) if ts < dr + 0.3 else lerp(690, 380, smooth(seg(od, 0.3, 1.1)))
    if 0.3 < o < 1.2: M_ = ('panik', walk(1000 - xm, 0.70, -1, run=True), -2)
    elif ts < dr + 0.3: M_ = ('panik', REACH_L, -2)
    elif od < 1.1: M_ = ('panik', walk(690 - xm, 0.70, -1, run=True), -2)
    else: M_ = ('bagir' if on(ts, 'm10', 0, 0.05) else 'panik', dict(aL=(-100, 60, -170, 10 + alt(k, 0, 26, 2)), aR=(-30, 70, -150, 50), lean=-10), -2)
    with floorcam(cv, SX0, z, ang):
        gangway(cv, k, SC(ts), 0, closed=closed, nos=(4, 3), hi=(1.0, 0.0), out_l=lambda c: stn_out(c, k), out_r=lambda c: stn_out_r(c, k),
                lamp_l=1.0 if (k // 5) % 3 else 0.6)
        with stage(cv):
            people(cv, ts, {'R': (150, GYG, 0.74), 'D': (xa, FAR + 38, 0.64), 'M': (xm, GYG, 0.70)}, {'R': R_, 'D': D_, 'M': M_})
            if od >= SHUT: sfx_text(cv, GL + 70, 740, 'TAK', 70, a=1 - seg(od, SHUT + 0.3, SHUT + 0.7))
    dim(cv, 0.55 * (1 - fall))


# ============ SAHNE 24: kapinin ardinda Ren: "burasi tanidik geliyor"; lambalar soner ============
def scene24(cv, t):
    ts, k = step(t), kk(t)
    ot = B('out')[0]; o = ts - ot
    lamp = 1.0 if o < OUT_OFF[0] else (0.5 if o < OUT_OFF[0] + 0.16 and k % 2 else (0.3 if o < OUT_OFF[1] else 0.0))
    dark = 0.0 if o < OUT_OFF[0] else (0.5 if o < OUT_OFF[1] else 0.93)
    calm = ts >= frac('r18', 0.42)
    R_ = ('sakin' if calm else 'saskin', dict(aL=(-110, 60, -176, -20)) if calm and ts >= frac('r18', 0.6) else {}, -2)
    M_ = ('panik', dict(aL=(-100, 60, -170, 10 + (alt(k, 0, 26, 2) if not calm else 0)), aR=(-30, 70, -150, 50), lean=-10), -2)
    with floorcam(cv, SX0, 1.2):
        gangway(cv, k, SC(ts), 0, closed=1.0, nos=(4, 3), hi=(1.0, 0.0), out_l=lambda c: stn_out(c, k), out_r=lambda c: stn_out_r(c, k), lamp_l=lamp)
        with stage(cv):
            people(cv, ts, {'R': (120, GYG, 0.74), 'D': (560, FAR + 38, 0.64), 'M': (380, GYG, 0.70)}, {'R': R_, 'D': ('endise', COWER, -2), 'M': M_})
            left_dark(cv, dark)


# ============ SAHNE 25: sis dagilir: kapinin ardinda vagon yok ============
def gone_shot(cv, ts, k, st, z=1.16, sx=None, sy=None):
    fg = B('fog')[0]; o = ts - fg
    gone = o >= GONE
    fa = smooth(seg(o, 0.0, 0.9)) * (1 - smooth(seg(o, 1.7, 2.7)))
    sxx = lerp(SX0, SX1, smooth(seg(o, 0.7, 2.2))) if sx is None else sx
    with floorcam(cv, sxx, z, sy=sy):
        if gone: gangway(cv, k, SC(ts), 0, nos=(4, 3), gone_l=True)
        else: gangway(cv, k, SC(ts), 0, closed=1.0, nos=(4, 3), hi=(1.0, 0.0), out_l=lambda c: stn_out(c, k), out_r=lambda c: stn_out_r(c, k), lamp_l=0.0)
        with stage(cv):
            if not gone: left_dark(cv, 0.93)
            people(cv, ts, {w: v[0] for w, v in st.items()}, {w: v[1] for w, v in st.items()})
            if fa > 0:                                       # sis: soldaki vagonu orter
                p = fill((196, 206, 228), 240 * fa); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60))
                cv.drawRect(LTRB(-1100, 300, GL + 40, 1700), p)
                fog(cv, fa * 1.6, k, y=1050, x0=-900, x1=GL + 200, h=700)


def scene25(cv, t):
    ts, k = step(t), kk(t)
    o = ts - B('fog')[0]
    xm = lerp(380, 690, smooth(seg(o, 0.2, 1.1)))
    if 0.2 < o < 1.1: M_ = ('panik', dict(walk(xm - 380, 0.70, 1, scared=True)), -2)
    else: M_ = ('saskin' if o >= GONE else 'panik', BACKP if on(ts, 'm11') else {}, -2)
    gone_shot(cv, ts, k, {'M': ((xm, GYG, 0.70), M_), 'D': ((lerp(560, 880, smooth(seg(o, 0.3, 1.2))), FAR + 38, 0.64), ('endise', COWER if o < 1.6 else {}, -2))})
BACKP = dict(aL=(-120, 40, -200, -20))                      # arkasini (solu) gosterir


# ============ SAHNE 26: Ada ile Mia (yakin) ============
def scene26(cv, t):
    ts, k = step(t), kk(t)
    gone_shot(cv, ts, k, {'M': ((690, GYG, 0.70), ('uzgun', {}, 1.6)), 'D': ((880, FAR + 38, 0.64), ('uzgun', CALM if on(ts, 'd6') else {}, -1.5))},
              z=1.5 if V else 1.45, sx=-250 if V else -240, sy=-60 if V else 20)


# ============ SAHNE 27: Mia telefonu alir; soruyu sorar ============
def scene27(cv, t):
    ts, k = step(t), kk(t)
    pc = B('pick')[0]; o = ts - pc
    if o < PICK:                                             # telefon hala yerde: Mia ona yaklasir, egilir
        ap = smooth(seg(ts, frac('m12', 0.55), pc + PICK))
        s = lerp(0.70, 1.08, ap); xm = lerp(690, 560, ap); gy = lerp(GYG, GYG + 300, ap)
        M_ = ('saskin' if ap < 0.05 else 'endise', mixpose(dict(aR=(110, 100, 204, 150)), dict(aR=(60, 150, 30, 300), lean=10, crouch=40), ap), 0 if ap > 0.3 else -1.2)
        gone_shot(cv, ts, k, {'M': ((xm, gy, s), M_), 'D': ((880, FAR + 38, 0.64), ('uzgun', {}, -1.5))}, sx=SX1)
        dim(cv, 0.92 * seg(o, PICK - 0.3, PICK), (0, 0, 0))
        return
    up = smooth(seg(o, PICK, PICK + 0.6))                    # telefon elde: kadraj duzelir
    q = ts >= frac('m13', 0.56)                              # soru
    F_ = ('merak' if q else 'uzgun', {}, 0)
    st = {'D': ('uzgun', {}, -1.2)}
    zq = lerp(1.0, 1.08, smooth(seg(ts, frac('m13', 0.5), frac('m13', 0.75)))); zz = lerp(1.3, 1.0, up) * zq
    cv.save(); cv.translate(W / 2, H / 2); cv.rotate(TILT * (1 - up)); cv.scale(zz, zz); cv.translate(-W / 2, -H / 2)
    sel(cv, ts, k, lambda: door_view(cv, k, gone=1.0, scroll=SC(ts), no=4), st, F_, who='M')
    cv.restore()
    dim(cv, 0.92 * (1 - seg(o, PICK, PICK + 0.25)), (0, 0, 0))


# ============ SAHNE 28: kayit durdu; kapanis karti ============
def scene28(cv, t):
    ts, k = step(t), kk(t)
    a0 = REC1
    u, y = (1.2, 1140) if V else (1.3, 1150)
    with stage(cv):
        ext_bg(cv, SC(ts), k, y=y + 21 * u - 22, moon=(840, 380) if V else (1300, 640), fog_a=0.7)
        train_ext(cv, (760 if V else 900) + 60 * (ts - a0), y, u, 3, k)
    dim(cv, 0.6)
    a = smooth(seg(ts, a0 + 0.9, a0 + 1.5))
    cx, cy, w = (W / 2, 900, 520) if V else (W / 2, 560, 400)
    gl = fill((255, 226, 150), 70 * a); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60)); cv.drawCircle(cx, cy, w * 0.5, gl)
    ticket(cv, cx, cy + 30 * (1 - a), w, GREENC, 'REN', STN, a, rot=-4)
    c_ = seg(t, a0 + 0.8, a0 + 1.3)
    card(cv, [('Biletinden', 72, RED), ('kaçabilir misin?', 72, RED), ('Yorumlara yaz', 40, CREAM), ('Sıradaki: 3. Bölüm, Yedigöl', 36, (176, 190, 232))],
         c_, cy=470 if V else 215)
    b = 1 - seg(t, a0 + 0.55, a0 + 0.95)                      # kayit durdu: siyah ekran
    if b > 0:
        dim(cv, b, (0, 0, 0))
        fs = 54 if V else 44; f = skia.Font(TFB, fs); s = 'KAYIT DURDU'; w_ = f.measureText(s)
        cv.drawRect(LTRB(W / 2 - w_ / 2 - fs * 1.0, H / 2 - fs * 0.78, W / 2 - w_ / 2 - fs * 0.3, H / 2 - fs * 0.08), fill((255, 255, 255), 255 * b))
        cv.drawString(s, W / 2 - w_ / 2, H / 2, f, fill((255, 255, 255), 255 * b))


SINE = {3: dict(zmax=1.1), 10: dict(zmax=1.12), 14: dict(zmax=1.1), 16: dict(cam='sabit'), 23: dict(cam='sabit'), 24: dict(mood='soguk'),
        25: dict(mood='soguk'), 26: dict(mood='soguk'), 28: dict(mood='gece')}

if __name__ == '__main__':
    DRAW = {i: globals()[f'scene{i}'] for i in range(1, 29)}
    run(DRAW, white=tuple((i, i + 1) for i in range(1, 28)), sine=SINE, hud=hud)
