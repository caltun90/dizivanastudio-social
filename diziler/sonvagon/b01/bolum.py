"""Son Vagon, 1. Bolum: Bilet. Yalnizca sahneler; ortak parcalar ../ortak.py icinde.
Yapi: DUZ ANLATIM. Kanca (arka kapi: vagon yok) -> trenin disaridan sayimi -> baslik -> son vagon disaridan (dort yolcu) ->
vagonun ici (genis, sonra Mia ile Ada yakin) -> biletler -> anons (hoparlor, sonra herkes yukari bakar) -> levha: VAGON 5 ->
one yuruyus -> koruk (Eli geri doner) -> Karakopru peronu -> dort numarali vagonun penceresi -> Eli karanlikta ->
arka kapi: vagon yok -> disaridan dort vagon -> yerdeki bilet -> anons ve levha: VAGON 4 -> tren geceye karisir (kural) -> kapanis.
Mekanlar: arka kapi (karsidan), tren disaridan (genis ve yakin), vagon kesiti, koruk, peron. Gorsel fikirler: bilet kartlari,
levhanin kirmizi yanmasi, lambalarin sirayla sonmesi, camdaki sisin dagilmasi."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import *
from senaryo import ABONE_END, HOOK_CUT, BRAKE, LAMP_OFF, WHISTLE, PICK

V = FMT == 'v'
QW = (540, 1060) if V else (540, 1000)                     # genis vagon planlarinda sahnenin oturdugu yer (dikeyde biraz asagi)
HK = E('h1') + HOOK_CUT                                    # kancadan disari plana kesme ani
XM, XR, XD, XE = 1450, 1790, 1990, 2200                    # son vagonda duruslar (vagon x'i)
STN = 'KARAKÖPRÜ'
PUP = dict(aR=(110, 20, 200, -70))                          # sag yukariyi gosterir
FWD = dict(aR=(110, 70, 214, 50))                           # ileriyi (sagi) gosterir
BACKP = dict(aR=(120, 30, 200, -40))                        # arkasindaki cami gosterir
WRIST = dict(aL=(-70, 110, 10, 96))                         # bilegine (saate) bakar
SITF = dict(crouch=150, kL=(-124, -96), fL=(-170, -18), kR=(124, -96), fR=(170, -18), lean=6, belly=-10)   # yere coker


# ---------- trenin aldigi yol (disarisi, tekerler ve traversler buna gore akar) ----------
def _speed(t):
    tb, st0, wh = S('m4'), B('stop')[0], B('whistle')[0] + WHISTLE
    pts = [(0, 420), (tb, 420), (tb + 2.5, 190), (st0 + BRAKE, 170), (st0 + 2.5, 0), (wh + 0.3, 0), (wh + 5, 330), (wh + 9, 420), (9999, 420)]
    return np.interp(t, [p[0] for p in pts], [p[1] for p in pts])
_T = np.arange(0, TL.total + 3, 1 / 24.0); _D = np.concatenate([[0], np.cumsum(_speed(_T[:-1]) / 24.0)])
def SC(t): return float(np.interp(t, _T, _D))


def pl(cam, **xs): return {w: (x - cam, CAST[w]['gy'], CAST[w]['s']) for w, x in xs.items()}
def w5(cv, ts, k, cam, case=True, **kw):
    """bes numarali (son) vagon; koltukta Eli'nin cantasi"""
    wagon(cv, cam, 5, k, scroll=SC(ts), **kw)
    if case:
        with stage(cv): briefcase(cv, seat_xy(2)[0] - cam, 1120 - 54, 0.9)


def title_card(cv, t):
    tb = B('title'); a = seg(t, tb[0], tb[0] + 0.35)
    if a > 0:
        dim(cv, 0.5 * a)
        card(cv, [(TITLE, 112, (255, 110, 96)), (f'{EP.title()}: {EP_NAME}', 48, CREAM)], a, lerp(0.9, 1.0, smooth(seg(t, tb[0], tb[0] + 0.5))))


def hud(cv, t, k):
    if t < HK: hook_text(cv, t, 'VAGON NEREDE?', 1 - seg(t, HK - 0.2, HK))
    if k == 19: abone(cv, t, TL.span(19)[0] + ABONE_END, pos=(W / 2, 1500) if V else (W / 2, 800))   # kameradan sonra: kirpilmaz


# ============ arka kapi (kancada da kullanilir): Mia kapida -> sis dagilir -> vagon yok ============
def rear_scene(cv, ts, k, hook=False):
    wh, fg = B('whistle'), B('fog')
    gone = 1.0 if ts >= fg[0] else 0.0                       # arkadaki vagon, cam sisle kapaliyken kaybolur
    fa = smooth(seg(ts, wh[0] + 0.5, wh[0] + 1.4)) * (1 - smooth(seg(ts, fg[0] + 0.4, fg[1] - 0.2)))
    sh = jit(k, 3.5 * (1 - seg(ts, wh[0] + 0.5, wh[0] + 1.8))) if ts > wh[0] + WHISTLE else (0, 0)   # kalkis sarsintisi
    after = ts >= S('m7') - 0.05
    door_view(cv, k, gone=gone, fog_a=fa, scroll=SC(ts), plate_hi=1.0 if after and not hook else 0.0, plate_on=0.0 if hook else 1.0, shake=sh)
    run_u = seg(ts, wh[0] + 0.3, wh[0] + 1.3); side = smooth(seg(ts, fg[0] + 0.2, fg[0] + 1.2))
    if run_u < 1: mx = lerp(1000, 540, run_u); M = ('panik', walk(1000 - mx, 0.72, -1, run=True), -2)
    elif ts < fg[0] + 0.2: mx = 540; M = ('panik', dict(DOORP, lean=alt(k, -5, 5, 2)), 0, dict(back=True))   # kapiyi zorlar
    elif side < 1: mx = lerp(540, 240, side); M = ('panik', walk(540 - mx, 0.72, -1), 1.5)                   # yana cekilir, cama bakar
    else: mx = 240; M = ('bagir' if on(ts, 'm7', 0.0, 0.05) else 'panik', BACKP, 0 if on(ts, 'm7', 0.1, 0.3) else 1.6)
    if on(ts, 'r5'): R_ = ('saskin', dict(aL=(-120, 40, -196, -30)), -2)
    elif after: R_ = ('panik', COWER, -2)
    else: R_ = ('endise', {}, -1.6)
    D_ = ('uzgun', CALM if on(ts, 'd6') else {}, -1) if ts >= S('d6') - 0.1 else ('endise', {}, -1.4)
    with stage(cv, *sh):
        people(cv, ts, {'M': (mx, NEAR, 0.72), 'D': (730, FAR, 0.64), 'R': (900, NEAR, 0.74)}, {'M': M, 'D': D_, 'R': R_})


# ---------- disaridan sayim ----------
def ext_count(cv, ts, k):
    u, y = (1.55, 1130) if V else (1.5, 1150)
    L_ = train_len(5) * u
    if V: xr = lerp(1010, 1010 + L_ - 800, smooth(seg(ts, S('n1') - 0.1, frac('n1', 0.95))))     # kamera lokomotiften kuyruga kayar
    else: xr = 540 + L_ / 2 + 14 * math.sin(ts * 0.6)
    fade = smooth(seg(ts, frac('n2', 0.24), frac('n2', 0.5)))
    with stage(cv):
        ext_bg(cv, SC(ts), k, y=y + 21 * u - 22, moon=(800, 520) if V else (1180, 620))
        mid = train_ext(cv, xr, y, u, 5, k, fade=fade, heads={5: [None, None, SKYB, None, None]})
        for i in range(1, 6):
            a = seg(ts, frac('n1', 0.30 + 0.12 * (i - 1)), frac('n1', 0.30 + 0.12 * (i - 1)) + 0.12)
            if a > 0: badge_at(cv, mid[i], y - 170 * u + 14 * (1 - a), str(i), red=(i == 5 and fade > 0.5), a=a, r=40)
        if fade > 0.6:                                      # kaybolan vagonun yerinde carpi
            x5, yb = mid[5], y - 170 * u
            for sd in (-1, 1): cv.drawLine(x5 - 30, yb - sd * 30, x5 + 30, yb + sd * 30, stroke(CREAM, 9))


# ============ SAHNE 1: kanca + sayim + baslik ============
def scene1(cv, t):
    ts, k = step(t), kk(t)
    if ts < HK:
        rear_scene(cv, S('m7') + min(ts, E('m7') - S('m7') + 0.25), k, hook=True)
        flash(cv, 0.8 * seg(t, HK - 0.15, HK)); return
    ext_count(cv, ts, k)
    flash(cv, 0.8 * (1 - seg(t, HK, HK + 0.25)))
    title_card(cv, t)


# ============ SAHNE 2: son vagon disaridan: dort yolcu ============
def scene2(cv, t):
    ts, k = step(t), kk(t)
    a0, _ = TL.span(2)
    u, y = (3.3, 1150) if V else (3.4, 1180)
    xr = 540 + 993 * u + 26 * (ts - a0) - 60
    shown = 1 + int(4 * seg(ts, frac('n3', 0.55), frac('n3', 0.86)) - 1e-6) if ts >= frac('n3', 0.55) else 0
    hd = [c if i < shown else None for i, c in enumerate((MUSTARD, GREENC, ROSE, SKYB))]
    with stage(cv, 0, alt(k, 0, 3, 3)):
        ext_bg(cv, SC(ts), k, y=y + 21 * u - 22, moon=(830, 430) if V else (1240, 600), fog_a=0.35)
        mid = train_ext(cv, xr, y, u, 5, k, heads={5: hd, 4: [None] * 5})
        if shown:
            wx = mid[5] - 82 * u
            for i in range(shown): badge_at(cv, wx + (13 + i * 29 + 11.5) * u, y - 96 * u - 78, str(i + 1), r=32)


# ============ SAHNE 3: son vagon (genis) ============
Z3, CAM3 = (0.82 if V else 1.0), 1300
def scene3(cv, t):
    ts, k = step(t), kk(t)
    st = {'M': ('merak', {}, 1.5 if on(ts, 'r1', 0, 0.6) else -1.6),
          'R': ('mutlu', RANT if on(ts, 'r1', 0, 0) and ts < frac('r1', 0.5) else HIP, alt(k, -1.5, 1.5, 9) if ts < S('d1') else 1.5),
          'D': ('mutlu' if on(ts, 'd1') else 'sakin', dict(KNIT, lean=alt(k, 0, 3, 4)), -1.4 if on(ts, 'd1') else 0, dict(prop='knit')),
          'E': ('endise', SHOW, 0.6, dict(prop='watch'))}
    zz = (0.92 if V else 1.18, (560 if V else 640, 1000), (540, 1050) if V else (540, 1010)) if ts >= S('d1') - 0.15 else (Z3, (540, 1000), QW)   # d1: orta plan
    with zoom(cv, *zz):
        w5(cv, ts, k, CAM3)
        with stage(cv): people(cv, ts, pl(CAM3, M=XM, R=XR, D=XD, E=XE), st)


# ============ SAHNE 4: Mia ile Ada (yakin) ============
def scene4(cv, t):
    ts, k = step(t), kk(t)
    if on(ts, 'm2') and ts < frac('m2', 0.34): M = ('merak', CALM, 1.5)                      # "Bilmiyorum."
    elif ts >= frac('m2', 0.34): M = ('mutlu', SHOW, 1.5, dict(prop='ticket'))               # bileti gosterir
    else: M = ('mutlu', HIP if on(ts, 'm1') else {}, 1.5)
    st = {'M': M, 'R': ('sakin', {}, 0, dict(back=True)),
          'D': ('merak' if ts >= S('d2') - 0.2 else 'mutlu', dict(KNIT, lean=-6 if on(ts, 'd2') else 0), -1.6, dict(prop='knit')),
          'E': ('endise', SHOW, 0.6, dict(prop='watch'))}
    with zoom(cv, 1.22 if V else 1.3, (420, 1000), (540, 1010) if V else (540, 1020)):
        w5(cv, ts, k, CAM3)
        with stage(cv): people(cv, ts, pl(CAM3, M=XM, R=XR, D=XD, E=XE), st)


# ============ SAHNE 5: biletler ============
def scene5(cv, t):
    ts, k = step(t), kk(t)
    tb = B('ticket')
    st = {'M': ('merak' if ts < S('r2') else 'endise', SHOW, 0 if ts < S('r2') else 1.5, dict(prop='ticket')),
          'R': ('mutlu', SHOW if ts >= S('r2') - 0.3 else HIP, -1.5, dict(prop='ticket') if ts >= S('r2') - 0.3 else {}),
          'D': ('sakin', KNIT, -1.4, dict(prop='knit')),
          'E': ('kararli' if on(ts, 'e1') else 'endise', SHOW, -1.5 if ts >= S('e1') - 0.2 else 0.6, dict(prop='ticket' if ts >= S('e1') - 0.2 else 'watch'))}
    with zoom(cv, Z3, (540, 1000), QW):
        w5(cv, ts, k, CAM3)
        with stage(cv): people(cv, ts, pl(CAM3, M=XM, R=XR, D=XD, E=XE), st)
    a1 = seg(ts, tb[0] + 0.3, tb[0] + 0.7); dim(cv, 0.5 * a1)
    mv = smooth(seg(ts, S('r2') - 0.4, S('r2') - 0.05)); a2 = seg(ts, S('r2') - 0.1, S('r2') + 0.25); a3 = seg(ts, S('e1') - 0.1, S('e1') + 0.25)
    if V: big, sl = (540, 640, 820), [(540, 350, 540), (540, 630, 540), (540, 910, 540)]
    else: big, sl = (960, 470, 880), [(430, 470, 500), (960, 470, 500), (1490, 470, 500)]
    cx, cy, w = lerpt(big, sl[0], mv)
    ticket(cv, cx, cy, w, MUSTARD, 'MIA', None, a1, rot=lerp(-3, 0, mv), hi=1.0 if ts >= frac('m3', 0.4) else 0.0, k=k)
    ticket(cv, sl[1][0], sl[1][1], sl[1][2], GREENC, 'REN', 'DEĞİRMEN', a2, rot=2)
    ticket(cv, sl[2][0], sl[2][1], sl[2][2], SKYB, 'ELI', STN, a3, rot=-2)


# ============ SAHNE 6: anons ============
def spk_close(cv, ts, k, no, hi=0.0, case=True):
    """hoparlor ve on kapinin ustundeki levha (yakin)"""
    lv = TL.talk('A', ts); ch = B('chime' if no == 5 else 'chime2')
    sh = jit(k, 2.5) if ch[0] <= ts < ch[0] + 0.8 else (0, 0)
    with zoom(cv, 2.1 if V else 1.9, (560, 650), (540 + sh[0], 800 + sh[1]) if V else (540 + sh[0], 960 + sh[1])):
        wagon(cv, 1900, no, k, scroll=SC(ts), spk=lv if lv is not None else (0.5 if ch[0] <= ts < ch[0] + 0.8 else None), plate_hi=hi, last=(no == 5 or ts > B('fog')[0]))


def scene6(cv, t):
    ts, k = step(t), kk(t)
    if ts < S('a2') - 0.2: spk_close(cv, ts, k, 5); return
    cam = 1400; xm = lerp(XM, 1720, smooth(seg(ts, S('a2'), S('a2') + 1.5)))
    late = ts >= frac('a2', 0.6)                             # "bes numara"
    st = {'M': ('saskin' if late else 'merak', dict(walk(xm - XM, 0.70, 1), **LOOKUP) if XM < xm < 1720 else LOOKUP, 2),
          'R': ('saskin' if late else 'merak', LOOKUP, 2), 'D': ('merak', dict(KNIT, **LOOKUP), 2, dict(prop='knit')),
          'E': ('saskin' if late else 'endise', dict(SHOW, **LOOKUP), 2, dict(prop='watch'))}
    with zoom(cv, 0.78 if V else 1.0, (540, 1000), QW):
        w5(cv, ts, k, cam, spk=TL.talk('A', ts))
        with stage(cv): people(cv, ts, pl(cam, M=xm, R=XR, D=XD, E=XE), st)


# ============ SAHNE 7: levha: VAGON 5 ============
Z7, CAM7 = (0.86 if V else 1.0), 1500
def scene7(cv, t):
    ts, k = step(t), kk(t)
    pb = B('plate')
    if ts < S('r3') - 0.15:                                  # levhaya yakin plan: kirmizi yanip soner
        with zoom(cv, 2.0 if V else 1.9, (540, 640), (540, 800) if V else (540, 950)):
            wagon(cv, 2015, 5, k, scroll=SC(ts), plate_hi=seg(ts, pb[0] + 0.5, pb[0] + 0.7))
        return
    if on(ts, 'r3'): R_ = ('saskin', PUP, 2)
    else: R_ = ('endise', {}, 2 if ts < S('d3') else 1.5)
    if on(ts, 'e2'): E_ = ('kararli', RANT, -1.5 if ts < frac('e2', 0.5) else 2, dict(prop=None))
    else: E_ = ('endise', SHOW, 2 if ts < S('e2') else -1, dict(prop='watch'))
    if on(ts, 'd3'): D_ = ('sakin', FWD if ts >= frac('d3', 0.62) else CALM, -1 if ts < frac('d3', 0.3) else 1.5)
    else: D_ = ('endise', {}, 2)
    st = {'M': ('endise', {}, 2 if ts < S('d3') else 1.5), 'R': R_, 'D': D_, 'E': E_}
    zz = ((1.5, (700, 960), (540, 1000)) if V else (1.2, (560, 990), (540, 1010))) if on(ts, 'e2', 0.1, 0.1) else (Z7, (540, 1000), QW)   # e2: Eli ile Ada'ya yakin
    with zoom(cv, *zz):
        w5(cv, ts, k, CAM7, plate_hi=1.0)
        with stage(cv): people(cv, ts, pl(CAM7, M=1720, R=XR, D=XD, E=XE), st)


# ============ SAHNE 8: one yuruyus ============
def scene8(cv, t):
    ts, k = step(t), kk(t)
    t0 = S('m4'); o = ts - t0
    cam = lerp(CAM7, 1790, smooth(seg(o, 1.0, 5.6)))
    lurch = 14 * math.sin(clamp(o / 1.2) * math.pi)          # fren: herkes one savrulur
    def mover(w, x0, start, v, run=False, sc=False):
        s = CAST[w]['s']; d = max(0.0, o - start) * v; x = min(x0 + d, 2570); moving = 0 < d and x < 2570
        P = walk(d, s, 1, run=run, scared=sc) if moving else dict(lean=lurch, belly=-lurch * 0.5)
        return x, P, 1 - seg(x, 2480, 2565)
    xm, Pm, am = mover('M', 1720, 1.2, 300, run=True); xr, Pr, ar = mover('R', XR, 1.6, 260)
    xd, Pd, ad = mover('D', XD, 1.5, 190); xe, Pe, ae = mover('E', XE, 3.6, 205, sc=True)
    if o < 1.2: Pm = dict(FWD, lean=lurch)
    st = {'M': ('bagir' if on(ts, 'm4', 0, 0) else 'kararli', Pm, 2, dict(alpha=am)), 'R': ('endise', Pr, 2, dict(alpha=ar)),
          'D': ('kararli', Pd, 2, dict(alpha=ad)), 'E': ('endise', Pe if o >= 3.6 else dict(SHOW, lean=lurch), 2 if o > 2.2 else -1, dict(alpha=ae, prop='watch' if o < 3.6 else None))}
    with zoom(cv, Z7, (540, 1000), QW):
        w5(cv, ts, k, cam, plate_hi=1.0, door_f=smooth(seg(o, 0.7, 1.7)))
        with stage(cv): people(cv, ts, pl(cam, M=xm, R=xr, D=xd, E=xe), st)


# ============ SAHNE 9: koruk ============
def scene9(cv, t):
    ts, k = step(t), kk(t)
    g0 = B('gang')[0]; bk = B('back'); o = ts - g0
    gy = NEAR - 10
    def cross(x0, x1, a, b, s, run=False):
        u = seg(o, a, b); x = lerp(x0, x1, u); return x, (walk(x - x0, s, 1, run=run) if 0 < u < 1 else None)
    xm, Wm = cross(420, 880, 0.0, 1.3, 0.70, True); xd, Wd = cross(330, 720, 0.1, 2.1, 0.64); xr, Wr = cross(60, 560, 0.2, 2.2, 0.74)
    xe, We = cross(-140, 180, 0.9, 2.3, 0.70)
    ob = ts - bk[0]
    if ob > 0.1:                                             # Eli geri doner
        xe2 = lerp(180, -330, seg(ob, 0.1, 1.25)); We = walk(180 - xe2, 0.70, -1) if xe2 > -330 else None; xe = xe2
    if We: E_ = ('endise', We, 2 if ob <= 0.1 else -2)
    elif on(ts, 'e3'): E_ = ('panik', UP if ts < frac('e3', 0.25) else dict(aL=(-70, 110, -20, 190), aR=(70, 110, 20, 190)), 2 if ts < frac('e3', 0.25) else -2)
    elif on(ts, 'e4') or ts >= S('e4'): E_ = ('kararli', SHOW, 2, dict(prop='watch'))
    else: E_ = ('endise', {}, 2)
    M_ = ('endise', Wm, 2) if Wm else (('bagir', REACH_L, -2) if on(ts, 'm5') else ('endise' if ts < bk[0] + 1.4 else 'saskin', {}, -2))
    R_ = ('endise', Wr, 2) if Wr else ('endise' if ts < bk[0] + 1.4 else 'saskin', {}, -2 if ts >= S('e3') else 2)
    D_ = ('kararli', Wd, 2) if Wd else ('endise', {}, -2 if ts >= S('e3') else 2)
    closed = seg(ob, 1.05, 1.5)
    def draw():
        gangway(cv, k, SC(ts), 5 if o < 2.3 else 3, closed=closed)
        with stage(cv):
            people(cv, ts, {'M': (xm, gy, 0.70), 'R': (xr, gy, 0.74), 'D': (xd, FAR + 38, 0.64), 'E': (xe, gy, 0.70)}, {'D': D_, 'E': E_, 'R': R_, 'M': M_})
            if ob >= 1.5: sfx_text(cv, GL + 10, 600, 'TAK', 64, a=1 - seg(ob, 1.5, 2.2))
    if on(ts, 'e4', 0.1, 0.1):                               # yakin: Eli ve saati
        with zoom(cv, 1.5, (250, 960), (540, 1000)): draw()
    else: draw()


# ============ SAHNE 10: Karakopru (peron) ============
def scene10(cv, t):
    ts, k = step(t), kk(t)
    s0 = B('stop')[0]; a0, b0 = TL.span(10)
    u = seg(ts, s0, s0 + 2.5); tx = -760 * (1 - u) ** 2
    h5 = [None] * 5; h5[4 - min(2, int(seg(ts, s0 + 1.0, b0) * 3))] = SKYB       # Eli vagonun arkasina dogru yurur
    sh = jit(k, 3) if s0 + 2.4 <= ts < s0 + 2.75 else (0, 0)
    cv.save(); cv.translate(sh[0] * K, 0)
    platform(cv, STN, tx, k, heads4=[MUSTARD, GREENC, ROSE, None, None], heads5=h5)
    cv.restore()


# ============ SAHNE 11: dort numarali vagon: pencerede istasyon ============
CAM11 = -60
def scene11(cv, t):
    ts, k = step(t), kk(t)
    sx = WINS[0] + WW / 2 - CAM11
    st = {'M': ('endise', {}, -2 if (k // 14) % 2 == 0 else 1.2),
          'D': ('merak', dict(aL=(-110, 60, -196, 10)) if on(ts, 'd4') and ts < frac('d4', 0.5) else CALM if on(ts, 'd4') else {}, -1.8),
          'R': ('endise', WRIST if on(ts, 'r4') and ts >= frac('r4', 0.45) else {}, -2 if on(ts, 'r4') and ts < frac('r4', 0.45) else (-0.6 if on(ts, 'r4') else -1.6))}
    with zoom(cv, 0.86 if V else 1.0, (540, 1000), QW):
        wagon(cv, CAM11, 4, k, scroll=SC(ts), last=False, out=lambda c: station_bg(c, STN, sx, k, bw=112, by=800))
        with stage(cv): people(cv, ts, {'M': (230, NEAR, 0.70), 'D': (800, NEAR, 0.64), 'R': (950, FAR, 0.74)}, st)


# ============ SAHNE 12: son vagon: Eli tek basina ============
CAM12 = 900
def scene12(cv, t):
    ts, k = step(t), kk(t)
    dk, sg, ot = B('dark'), B('sign'), B('out'); o = ts - dk[0]
    offs = [dk[0] + LAMP_OFF[0], dk[0] + LAMP_OFF[1], dk[0] + LAMP_OFF[2], ot[0] + 0.3, ot[0] + 0.55]
    def Lf(i):
        d = ts - offs[i]
        return 1.0 if d < 0 else (0.55 if d < 0.16 and (k % 2) else 0.0)
    sx = WINS[3] + WW / 2 - CAM12; ex = 1400 - CAM12
    got = o >= 0.7
    if not got: E_ = ('sakin', dict(aR=(120, 90, 250, 130), lean=14), 0, dict(back=True))                  # koltuktaki cantaya uzanir
    elif ts < S('e5'): E_ = ('mutlu' if o < LAMP_OFF[2] else 'saskin', {}, 2 if o < LAMP_OFF[2] else -2, dict(prop='case'))
    elif on(ts, 'e5') and ts < frac('e5', 0.5): E_ = ('mutlu', {}, 2, dict(prop='case'))
    elif ts < sg[0] + 0.3: E_ = ('saskin', {}, -2, dict(prop='case'))
    elif ts < S('e6') + 0.1: E_ = ('saskin', {}, 2, dict(prop='case'))                             # pencerede tabela
    else: E_ = ('saskin' if ts < frac('e6', 0.45) else 'sakin', SHOW, 1.6 if ts < frac('e6', 0.45) else 0.6, dict(prop='ticket'))
    floor_case = ts >= S('e6') + 0.1
    def draw():
        wagon(cv, CAM12, 5, k, scroll=SC(ts), lamps=Lf, out=lambda c: station_bg(c, STN, sx, k, bw=112, by=800))
        with stage(cv):
            if not got: briefcase(cv, seat_xy(2)[0] - CAM12, 1120 - 54, 0.9)
            if floor_case: briefcase(cv, ex - 150, NEAR - 40, 0.9)
            actor(cv, ts, 'E', E_[0], E_[1], E_[2], place=(ex, FAR + 30, 0.70), **(E_[3] if len(E_) > 3 else {}))
        wagon_dark(cv, CAM12, Lf)
    if ts >= sg[0] + 0.3:                                    # yakin: Eli ve penceredeki tabela
        with zoom(cv, 1.42 if V else 1.5, (680, 930), (540, 1000) if V else (540, 1010)): draw()
    else:
        with zoom(cv, 0.9 if V else 1.0, (540, 1000), QW): draw()


# ============ SAHNE 13: arka kapi ============
def scene13(cv, t):
    ts, k = step(t), kk(t)
    if on(ts, 'r5', 0.1, 0.15):                              # yakin: bos ray ve Ren
        with zoom(cv, 1.4, (700, 900), (540, 960)): rear_scene(cv, ts, k)
    else: rear_scene(cv, ts, k)


# ============ SAHNE 14: disaridan: dort vagon ============
def scene14(cv, t):
    ts, k = step(t), kk(t)
    a0, _ = TL.span(14)
    u, y = (1.55, 1130) if V else (1.5, 1150)
    xr = (1954 if V else 540 + train_len(4) * u / 2 + 150) + 22 * (ts - a0)
    with stage(cv):
        ext_bg(cv, SC(ts), k, y=y + 21 * u - 22, moon=(800, 520) if V else (1180, 620), fog_a=0.7)
        mid = train_ext(cv, xr, y, u, 4, k)
        x5 = mid[4] - PITCH * u; yb = y - 170 * u
        fog(cv, 0.9, k, y=y - 40, x0=x5 - 420, x1=x5 + 260, h=200)
        for i in (1, 2, 3, 4):
            a = seg(ts, frac('n5', 0.1 + 0.1 * (i - 1)), frac('n5', 0.1 + 0.1 * (i - 1)) + 0.12)
            if a > 0: badge_at(cv, mid[i], yb + 14 * (1 - a), str(i), a=a, r=40)
        a = seg(ts, frac('n5', 0.5), frac('n5', 0.5) + 0.15)
        if a > 0:
            badge_at(cv, x5, yb, '5', red=True, a=a, r=44)
            for sd in (-1, 1): cv.drawLine(x5 - 32, yb - sd * 32, x5 + 32, yb + sd * 32, stroke(CREAM, 9, 255 * a))


# ============ SAHNE 15: yerdeki bilet ============
def scene15(cv, t):
    ts, k = step(t), kk(t)
    fd = B('find'); o = ts - fd[0]
    bend = smooth(seg(o, 0.35, PICK)) * (1 - smooth(seg(o, PICK + 0.15, PICK + 0.75)))
    BL = dict(crouch=120, lean=-26, belly=18, kL=(-110, -100), kR=(110, -100), aL=(-110, 150, -150, 300))
    has = o >= PICK
    if o < PICK + 0.75: R_ = ('merak', mixpose({}, BL, bend), -2)
    elif ts < S('m8'): R_ = ('merak', SHOW, 1.5 if on(ts, 'r6') and ts > frac('r6', 0.5) else 0)
    elif ts < S('r7') - 0.2: R_ = ('endise', SHOW, 1.5)
    else: R_ = ('yorgun', SHOW, 0 if ts < frac('r7', 0.3) else 0.4, dict(prop='ticket'))
    M_ = ('saskin' if ts >= frac('m8', 0.3) else 'merak', LEAN_IN if S('r6') <= ts < S('r7') else {}, -2)
    D_ = ('endise' if ts < S('r7') else 'uzgun', {}, -2)
    P = {'R': (500, NEAR, 0.74), 'M': (720, NEAR, 0.70), 'D': (900, FAR, 0.64)}
    with zoom(cv, 0.86 if V else 1.0, (540, 1000), QW):
        wagon(cv, CAM11, 4, k, scroll=SC(ts), last=True)
        with stage(cv):
            if not has: mini_ticket(cv, 372, NEAR + 6, 1.0, rot=14, c=SKYB)
            f = people(cv, ts, P, {'R': R_, 'M': M_, 'D': D_})
            if has and ts < S('r7') - 0.2:
                h = f['R']['handL'] if o < PICK + 0.75 else f['R']['handR']
                mini_ticket(cv, h[0] + (-6 if o < PICK + 0.75 else 8), h[1] - (10 if o < PICK + 0.75 else 30), 1.06, c=SKYB)
    a1 = seg(ts, S('m8') - 0.15, S('m8') + 0.25); a2 = seg(ts, S('r7') + 0.2, S('r7') + 0.55); mv = smooth(seg(ts, S('r7') - 0.2, S('r7') + 0.2))
    dim(cv, 0.4 * a1)
    if V: big, s1, s2 = (540, 540, 800), (540, 400, 580), (540, 700, 580)
    else: big, s1, s2 = (960, 280, 640), (640, 280, 580), (1280, 280, 580)
    cx, cy, w = lerpt(big, s1, mv)
    ticket(cv, cx, cy, w, SKYB, 'ELI', STN, a1, rot=lerp(-2, 0, mv))
    ticket(cv, s2[0], s2[1], s2[2], GREENC, 'REN', 'DEĞİRMEN', a2, rot=2)


# ============ SAHNE 16: anons ============
def scene16(cv, t):
    ts, k = step(t), kk(t)
    spk_close(cv, ts, k, 4, hi=1.0 if ts >= frac('a3', 0.62) else 0.0)


# ============ SAHNE 17: levha: VAGON 4; "one yuruyoruz" ============
CAM17 = 300
def scene17(cv, t):
    ts, k = step(t), kk(t)
    pb = B('plate4')
    if ts < pb[1] - 0.1:
        with zoom(cv, 2.0 if V else 1.9, (540, 640), (540, 800) if V else (540, 950)):
            wagon(cv, 2015, 4, k, scroll=SC(ts), plate_hi=1.0, last=True)
        return
    up = smooth(seg(ts, frac('d5', 0.35), frac('d5', 0.85)))  # Ren kalkar
    xd = 960 + 230 * max(0.0, ts - frac('d5', 0.55))
    Dw = walk(xd - 960, 0.64, 1) if xd > 960 else (dict(aL=(-110, 70, -190, 110)) if on(ts, 'd5') else {})
    st = {'R': ('panik' if up < 0.5 else 'endise', mixpose(dict(SITF, aR=(84, 96, 40, 168)), SHOW, up), 1.5, dict(prop='ticket')),
          'M': ('endise', REACH_L if up < 1 else {}, -2 if up < 1 else 2),
          'D': ('kararli', Dw, -1.6 if xd <= 960 else 2)}
    with zoom(cv, 0.86 if V else 1.0, (540, 1000), QW):
        wagon(cv, CAM17, 4, k, scroll=SC(ts), plate_hi=1.0, last=True)
        with stage(cv): people(cv, ts, {'R': (460 - CAM17 + 60, NEAR, 0.74), 'M': (780 - CAM17 - 20, NEAR, 0.70), 'D': (xd - CAM17, FAR, 0.64)}, st)


# ============ SAHNE 18: tren geceye karisir; kural ============
def scene18(cv, t):
    ts, k = step(t), kk(t)
    a0, _ = TL.span(18)
    u, y = (1.2, 1140) if V else (1.3, 1150)
    xr = (980 if V else 1180) + 150 * (ts - a0)
    with stage(cv):
        ext_bg(cv, SC(ts), k, y=y + 21 * u - 22, moon=(260, 560) if V else (-120, 600), fog_a=0.6)
        train_ext(cv, xr, y, u, 4, k)
    a = seg(ts, frac('n6', 0.42), frac('n6', 0.42) + 0.3)
    card(cv, [('KURAL', 38, AMBER), ('Tren durduğunda', 56, CREAM), ('son vagonda olma', 56, (255, 110, 96))], a, lerp(0.92, 1.0, smooth(a)), cy=620 if V else 300)


# ============ SAHNE 19: kapanis karti ============
def scene19(cv, t):
    ts, k = step(t), kk(t)
    a0, _ = TL.span(19)
    with stage(cv): ext_bg(cv, SC(ts), k, y=1150, moon=(840, 380) if V else (1300, 640), fog_a=0.7)
    dim(cv, 0.62)
    a = smooth(seg(ts, a0 + 0.4, a0 + 1.0))
    cx, cy, w = (W / 2, 900, 520) if V else (W / 2, 560, 400)
    gl = fill((255, 226, 150), 70 * a); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60)); cv.drawCircle(cx, cy, w * 0.5, gl)
    ticket(cv, cx, cy + 30 * (1 - a), w, MUSTARD, 'MIA', None, a, rot=-4, hi=1.0, k=k)
    c_ = seg(t, a0 + 0.3, a0 + 0.8)
    card(cv, [("Mia'nın bileti", 72, (255, 110, 96)), ('neden boş?', 72, (255, 110, 96)), ('Yorumlara yaz', 40, CREAM), ('Sıradaki: 2. Bölüm, Değirmen', 36, (176, 190, 232))],
         c_, cy=470 if V else 215)


SINE = {1: dict(), 2: dict(mood='gece'), 5: dict(zmax=1.1), 10: dict(mood='soguk'), 12: dict(mood='soguk'), 14: dict(mood='gece'),
        15: dict(zmax=1.1), 18: dict(mood='gece'), 19: dict(mood='gece')}

if __name__ == '__main__':
    run({1: scene1, 2: scene2, 3: scene3, 4: scene4, 5: scene5, 6: scene6, 7: scene7, 8: scene8, 9: scene9, 10: scene10, 11: scene11,
         12: scene12, 13: scene13, 14: scene14, 15: scene15, 16: scene16, 17: scene17, 18: scene18, 19: scene19},
        white=((3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (10, 11), (11, 12), (12, 13), (13, 14), (15, 16), (16, 17)), sine=SINE, hud=hud)
