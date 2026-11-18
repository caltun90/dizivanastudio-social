"""13. Kat, 4. Bolum: Lobi. Yalnizca sahneler; ortak parcalar ../ortak.py icinde.
Yapi: GERI DONUSLU. Kanca (son kapi, Leo cevabi bilmiyor) -> asansorde iki kisi ve kural -> birinci oda: kucuk bir yalan
(isik kizarir, karalti gelir), birinci soru -> GERI DONUS 1 (bir yil once, sepya: anne asansore biner, 13'te kalir) ->
birinci kapi acilir -> ikinci oda, ikinci soru -> GERI DONUS 2 (o aksam, renkli ve net: dort kisi biner; geri sarilir,
kapi acilir: Leo zaten iceride) -> Leo itiraz eder (ikinci yalan), kapi acilir -> ucuncu oda: Leo hatirlamiyor, bu dogru,
kapi acilir -> asansor: besinci kisi hep iceride -> bitis karti.
Yeni mekan: sorgu salonu (uc oda, uc numarali kapi, sarkan lamba). Yeni gorsel fikirler: geri donus rengi ve cercevesi
(sepya / canli), geri sarma, yalan isigi (kirmizi) ve kapinin ustundeki DOGRU / YALAN gostergesi, anne karakteri."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import *
from senaryo import ABONE_END, RED_ON, SHADOW_IN, SHUT, STOP13, FB_DING, GREEN

# kabinde iki kisi: Leo solda, Luna sagda
CAST['L'] = dict(CAST['L'], x=330); CAST['U'] = dict(CAST['U'], x=770)
CAB = {w: (CAST[w]['x'], CAST[w]['gy'], CAST[w]['s']) for w in ('L', 'U')}
LTRB = skia.Rect.MakeLTRB
RRXY = skia.RRect.MakeRectXY
RED, GRN, AMB = (255, 86, 74), (110, 224, 146), (255, 182, 70)

# ---------- sorgu salonu: olculer ----------
WQ, WQ2 = (34, 58, 66), (26, 44, 52)                       # duvar, alt duvar
FLQ, FLQ2 = (58, 42, 62), (80, 58, 82)                     # karo zemin
DX, DW, DT = 730, 230, 720                                 # kapinin sol kenari, genisligi, ust kenari (alti CFLOOR)
DMID = DX + DW / 2
DOORC = {1: (206, 190, 150), 2: (233, 180, 70), 3: (204, 54, 58)}
LAMPX = 450
PL, PU = (300, FAR, 0.70), (548, NEAR, 0.54)               # odada Leo ve Luna'nin durdugu yer
PKG = (300, 1092)                                          # Leo'nun paketi (ayakta, odada)

# ---------- bu bolumun pozlari ----------
HOLDB = dict(aL=(-80, 90, -34, 150), aR=(80, 90, 34, 150))      # Luna bereyi gogsunde tutar
HEAD_R = dict(aR=(104, -4, 58, -100))
SELF = dict(aR=(104, 112, 30, 150))                             # eli gogsunde
MOUTH = dict(aR=(92, 30, 26, -40), lean=-4, belly=8)            # eli agzinda
POINT_LEO = dict(aL=(-126, 96, -206, 70), aR=HOLDB['aR'])       # Luna solundaki Leo'yu gosterir
POINT_PK = dict(aL=(-110, 130, -196, 176), aR=HOLDB['aR'])      # Luna paketi gosterir
WAVE_A = dict(aR=(120, 30, 170, -100)); WAVE_B = dict(aR=(130, 40, 204, -72))
OBJECT = dict(aR=(130, 60, 196, -30), lean=10, belly=-8)        # itiraz


def people(cv, ts, P, st, order=('L', 'U')):
    """P: {kim: (x, gy, s)}; st: {kim: (ifade, poz, bakis[, ek])}. ek: down (goz kapaklari inik), gl (pakette Zoe'nin gozlugu),
    ber (Luna'nin elinde Sam'in beresi: True | 'R' sag elde | False)"""
    out = {}
    for w in order:
        if w not in st: continue
        v = st[w]; kw = dict(v[3]) if len(v) > 3 else {}
        down = kw.pop('down', False); gl = kw.pop('gl', True); ber = kw.pop('ber', True)
        if w == 'L': kw.setdefault('tie', True)
        a = kw.get('alpha', 1.0)
        if a <= 0.01: continue
        f = actor(cv, ts, w, v[0], v[1], v[2], place=P[w], **kw)
        s = P[w][2]
        if down and not kw.get('back'): lids(cv, f)
        if w == 'U' and ber and not kw.get('back'):
            h = f['handR'] if ber == 'R' else ((f['handL'][0] + f['handR'][0]) / 2, f['handL'][1])
            beret_at(cv, h[0], h[1] + 12, 0.5 * s / 0.54, a=a)
        if w == 'L' and gl:
            x = (f['handL'][0] + f['handR'][0]) / 2 if not kw.get('pkg_left') else f['handL'][0] + 40 * s
            glasses_at(cv, x + 34 * s, f['handL'][1] + 4 * s - 82 * s, 0.6 * s / 0.7, rot=-6, a=a)
        out[w] = f
    return out


def bubble_q(cv, x, y, a, top='LOBİ', side=1):
    """bos dusunce balonu. side: kuyruk hangi yana (1: balon basin saginda)"""
    if a <= 0: return
    r = 96 * lerp(0.7, 1.0, smooth(a)); A = 255 * clamp(a)
    for dx_, dy_, rr in ((-58, 150, 13), (-34, 116, 19)): cv.drawCircle(x + side * dx_, y + dy_, rr, fill(CREAM, A))
    cv.drawCircle(x + 3, y + 6, r, fill((4, 6, 20), 110 * clamp(a))); cv.drawCircle(x, y, r, fill(CREAM, A)); cv.drawCircle(x, y, r - 9, dashed(INKBLUE, 2.5, 150 * clamp(a), (8, 7)))
    if top: text(cv, top, x, y - 22, 40, INKBLUE, a=A); text(cv, '?', x, y + 62, 84, RED, a=A)
    else: text(cv, '?', x, y + 44, 124, RED, a=A)


def title_card(cv, t):
    tb = B('title'); a = seg(t, tb[0], tb[0] + 0.35)
    if a > 0:
        dim(cv, 0.45 * a)
        card(cv, [(TITLE, 130, (255, 110, 96)), (f'{EP.title()}: {EP_NAME}', 48, CREAM)], a, lerp(0.9, 1.0, smooth(seg(t, tb[0], tb[0] + 0.5))))


# ---------- dekor: sorgu salonu (uc oda ayni kalipta; kapinin numarasi ve rengi degisir) ----------
def _hang_lamp(cv, x, lc, fl, cone=True):
    if cone: poly(cv, [(x - 64, 628), (x + 64, 628), (x + 480, CFLOOR + 250), (x - 480, CFLOOR + 250)], lc, 26 * fl)
    cv.drawLine(x, 300, x, 560, stroke((14, 18, 26), 6, cap=False))
    poly(cv, [(x - 30, 556), (x + 30, 556), (x + 84, 630), (x - 84, 630)], (20, 26, 36))
    cv.drawLine(x - 76, 624, x + 76, 624, dashed((96, 116, 136), 3, 200, (9, 7)))
    gl = fill(lc, 96 * fl); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26)); cv.drawCircle(x, 648, 62, gl)
    cv.drawOval(LTRB(x - 40, 626, x + 40, 662), fill(lc, 255 * (0.3 + 0.7 * fl)))


def room(cv, n, k=0, open_u=0.0, state='red', level=None, msg=None, red=0.0, lamp=1.0, beyond='dark'):
    """n: kapi no (1, 2, 3). open_u: kapi acikligi (kanat yukari kayar). state: kapinin isigi 'red' | 'blink' | 'green'.
    level: asansorun sesi konusuyor (ses cubuklari). msg: gostergedeki yazi ('YALAN', 'DOĞRU', '?').
    red 0..1: yalan isigi. beyond: kapinin ardi 'dark' (siradaki oda) | 'lift' (asansor)"""
    cv.clear(col((12, 16, 24)))
    with stage(cv):
        x0, x1 = -520, 1620
        cv.drawRect(LTRB(x0, 300, x1, CFLOOR), fill(WQ))
        cv.drawRect(LTRB(x0, 250, x1, 440), fill((18, 28, 36)))                              # tavan bandi
        cv.drawLine(x0, 440, x1, 440, stroke((54, 84, 92), 6, cap=False))
        for j in range(-1, 7):                                                               # duvar panelleri
            px = -500 + 330 * j
            cv.drawRRect(RRXY(LTRB(px + 22, 486, px + 308, 984), 10, 10), dashed(shade(WQ, 1.5), 3, 140, (16, 12)))
        cv.drawRect(LTRB(x0, 1010, x1, CFLOOR), fill(WQ2))
        cv.drawLine(x0, 1010, x1, 1010, dashed(shade(WQ, 1.75), 4, 180, (18, 14)))
        cv.drawRect(LTRB(x0, CFLOOR, x1, 5000), fill(FLQ))                                   # karo zemin
        for r_ in range(2):
            for j in range(-4, 14):
                if (j + r_) % 2 == 0: cv.drawRect(LTRB(-600 + j * 160, CFLOOR + 8 + r_ * 124, -440 + j * 160, CFLOOR + 132 + r_ * 124), fill(FLQ2))
        cv.drawLine(x0, CFLOOR + 8, x1, CFLOOR + 8, dashed((150, 122, 152), 3.5, 170, (16, 12)))
        # sol: geldikleri kapi (1. odada asansor; sonrakilerde bir onceki kapi, acik)
        a0, a1 = -400, -150; am = (a0 + a1) / 2
        cv.drawRect(LTRB(a0 - 22, 668, a1 + 22, CFLOOR), fill((16, 20, 30)))
        cv.drawRRect(RRXY(LTRB(am - 62, 598, am + 62, 656), 10, 10), fill((16, 20, 30)))
        if n == 1:
            cv.drawRect(LTRB(a0, 690, a1, CFLOOR), fill((250, 228, 156)))
            cv.drawRect(LTRB(a0 + 14, 706, a1 - 14, CFLOOR), dashed((214, 180, 96), 3, 220))
            cv.drawLine(a0 + 6, 1040, a1 - 6, 1040, stroke((200, 170, 100), 10, cap=False))
            text(cv, '16', am, 644, 44, RED)
            poly(cv, [(a0, CFLOOR), (a1, CFLOOR), (a1 + 200, CFLOOR + 260), (a0 - 60, CFLOOR + 260)], (250, 228, 156), 34)
        else:
            cv.drawRect(LTRB(a0, 690, a1, CFLOOR), fill((8, 10, 20)))
            poly(cv, [(am - 30, 690), (am + 30, 690), (am + 110, CFLOOR), (am - 110, CFLOOR)], (250, 236, 190), 16)
            cv.drawRect(LTRB(a0, 690, a1, 742), fill(shade(DOORC[n - 1], 0.7)))              # yukari kaymis kanadin alt ucu
            text(cv, str(n - 1), am, 644, 44, GRN)
        # sag: kural levhasi ve ikinci lamba (yatayda gorunur)
        rc = LTRB(1112, 742, 1478, 916)
        cv.drawRRect(RRXY(rc.makeOffset(5, 8), 16, 16), fill((6, 8, 18), 140)); cv.drawRRect(RRXY(rc, 16, 16), fill((18, 24, 34)))
        cv.drawRRect(RRXY(rc.makeInset(10, 10), 10, 10), dashed((120, 136, 160), 2.5, 200, (10, 8)))
        text(cv, 'KURAL', 1295, 800, 34, (176, 190, 232)); text(cv, 'YALAN SÖYLEME', 1295, 872, 42, RED)
        lc = lerpt((250, 236, 190), (255, 64, 54), red)
        fl = lamp * ((0.5 + 0.5 * ((k * 7) % 5 >= 2)) if red > 0.5 else 1.0)
        _hang_lamp(cv, 1295, lc, fl * 0.7, cone=False)
        _hang_lamp(cv, LAMPX, lc, fl)
        # kapi
        cv.drawRect(LTRB(DX - 24, DT - 24, DX + DW + 24, CFLOOR), fill((16, 20, 30)))
        cv.save(); cv.clipRect(LTRB(DX, DT, DX + DW, CFLOOR))
        if beyond == 'lift':
            cv.drawRect(LTRB(DX, DT, DX + DW, CFLOOR), fill((250, 228, 156)))
            cv.drawRect(LTRB(DX + 14, DT + 16, DX + DW - 14, CFLOOR), dashed((214, 180, 96), 3, 220))
            cv.drawLine(DX + 6, 1040, DX + DW - 6, 1040, stroke((200, 170, 100), 10, cap=False))
        else:
            cv.drawRect(LTRB(DX, DT, DX + DW, CFLOOR), fill((8, 10, 20)))
            poly(cv, [(DMID - 26, DT + 60), (DMID + 26, DT + 60), (DMID + 100, CFLOOR), (DMID - 100, CFLOOR)], (250, 236, 190), 22)
            cv.drawOval(LTRB(DMID - 26, DT + 46, DMID + 26, DT + 70), fill((250, 236, 190), 150))
        c = DOORC[n]; dy = -(CFLOOR - DT) * open_u
        cv.drawRect(LTRB(DX, DT + dy, DX + DW, CFLOOR + dy), fill(shade(c, 1 - 0.2 * open_u)))
        cv.drawRect(LTRB(DX + 16, DT + 18 + dy, DX + DW - 16, CFLOOR - 16 + dy), dashed(shade(c, 1.45), 3.5, 220))
        text(cv, str(n), DMID, DT + 300 + dy, 200, shade(c, 0.6))
        cv.drawRRect(RRXY(LTRB(DMID - 46, CFLOOR - 62 + dy, DMID + 46, CFLOOR - 40 + dy), 9, 9), fill(shade(c, 0.6)))   # tutamak
        cv.restore()
        if open_u > 0 and beyond == 'lift':
            poly(cv, [(DX, CFLOOR), (DX + DW, CFLOOR), (DX + DW + 70, CFLOOR + 260), (DX - 190, CFLOOR + 260)], (250, 228, 156), 44 * open_u)
        # kapinin ustu: gosterge ve isik
        py = DT - 88
        cv.drawRRect(RRXY(LTRB(DMID - 126, py - 42, DMID + 126, py + 42), 14, 14), fill((14, 18, 28)))
        cv.drawRRect(RRXY(LTRB(DMID - 116, py - 33, DMID + 116, py + 33), 9, 9), dashed((90, 100, 130), 2.5, 200, (9, 7)))
        if msg:
            mc = RED if msg in ('YALAN', '?') else GRN
            gl = fill(mc, 80); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 20)); cv.drawRRect(RRXY(LTRB(DMID - 104, py - 28, DMID + 104, py + 28), 10, 10), gl)
            text(cv, msg, DMID, py + 18, 50 if len(msg) > 1 else 62, mc)
        elif level is not None:
            for i in range(9):
                h = 8 + 44 * level * (0.45 + 0.55 * abs(math.sin(i * 1.9 + k * 1.3)))
                cv.drawRRect(RRXY(LTRB(DMID - 92 + i * 22, py - h / 2, DMID - 80 + i * 22, py + h / 2), 5, 5), fill(AMB))
        sc_ = GRN if state == 'green' else RED
        br = 1.0 if state != 'blink' else alt(k, 1.0, 0.25, 3)
        gl = fill(sc_, 150 * br); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18)); cv.drawCircle(DMID, py - 82, 34, gl)
        cv.drawCircle(DMID, py - 82, 21, fill((14, 18, 28))); cv.drawCircle(DMID, py - 82, 15, fill(shade(sc_, 0.35 + 0.65 * br)))
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, GY + 60), skia.Point(0, GY + 430)], [skia.Color(10, 8, 26, 0), skia.Color(10, 8, 26, 225)]))
        cv.drawRect(LTRB(x0, GY, x1, 5000), g)
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kSoftLight); p.setAlphaf(0.4); cv.drawImage(noise_img(), 0, 0, LIN, p)


def red_wash(cv, a):
    """yalan isigi: butun oda kizarir"""
    if a <= 0: return
    cv.drawRect(skia.Rect.MakeWH(W, H), fill((255, 30, 24), 44 * a))
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.5), max(W, H) * 0.7, [skia.Color(120, 0, 0, 0), skia.Color(120, 0, 0, int(120 * a))]))
    cv.drawRect(skia.Rect.MakeWH(W, H), g)


# ---------- kabin kapisinin ardi: sorgu salonu, karsida 1 numarali kapi ----------
_VIEW = dict(glow=0.0)
def room_view(cv, near, far, lamp):
    nx0, ny0, nx1, ny1 = near; fx0, fy0, fx1, fy1 = far
    poly(cv, [(nx0, ny0), (nx1, ny0), (fx1, fy0), (fx0, fy0)], (18, 28, 36))
    poly(cv, [(nx0, ny1), (nx1, ny1), (fx1, fy1), (fx0, fy1)], FLQ)
    poly(cv, [(lerp(nx0, nx1, .3), ny1), (lerp(nx0, nx1, .7), ny1), (lerp(fx0, fx1, .74), fy1), (lerp(fx0, fx1, .26), fy1)], FLQ2)
    poly(cv, [(nx0, ny0), (fx0, fy0), (fx0, fy1), (nx0, ny1)], WQ)
    poly(cv, [(nx1, ny0), (fx1, fy0), (fx1, fy1), (nx1, ny1)], shade(WQ, 0.84))
    for f in (0.34, 0.6, 0.8, 0.92):
        x0, y0, x1, y1 = lerp(nx0, fx0, f), lerp(ny0, fy0, f), lerp(nx1, fx1, f), lerp(ny1, fy1, f)
        cv.drawRect(LTRB(x0, y0, x1, y1), dashed(shade(WQ, 1.7), max(1.2, 4 * (1 - f) + 1), 130, (14 * (1 - f) + 3, 10 * (1 - f) + 2)))
    f = 0.5; xm, y0 = (lerp(nx0, fx0, f) + lerp(nx1, fx1, f)) / 2, lerp(ny0, fy0, f)          # sarkan lamba
    cv.drawLine(xm, y0, xm, y0 + 44, stroke((14, 18, 26), 4, cap=False))
    poly(cv, [(xm - 16, y0 + 40), (xm + 16, y0 + 40), (xm + 40, y0 + 72), (xm - 40, y0 + 72)], (20, 26, 36))
    poly(cv, [(xm - 34, y0 + 72), (xm + 34, y0 + 72), (xm + 170, ny1), (xm - 170, ny1)], (250, 236, 190), 26 * lamp)
    cv.drawOval(LTRB(xm - 22, y0 + 68, xm + 22, y0 + 84), fill((250, 236, 190), 240 * lamp))
    cxm, cym = (fx0 + fx1) / 2, (fy0 + fy1) / 2
    g = skia.Paint(); g.setShader(skia.GradientShader.MakeRadial(skia.Point(cxm, cym), (ny1 - ny0) * 0.52, [skia.Color(6, 8, 20, 190), skia.Color(6, 8, 20, 0)]))
    cv.drawRect(LTRB(nx0, ny0, nx1, ny1), g)
    rc = LTRB(fx0, fy0, fx1, fy1); gw = _VIEW['glow']
    cv.drawRect(rc.makeOutset(7, 7), fill((14, 18, 28)))
    cv.drawRect(rc, fill(DOORC[1])); cv.drawRect(rc.makeInset(8, 9), dashed(shade(DOORC[1], 1.45), 2, 220, (6, 5)))
    text(cv, '1', cxm, cym + 30, 84, shade(DOORC[1], 0.55))
    gl = fill(RED, 170 * gw); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12)); cv.drawCircle(cxm, fy0 - 26, 24, gl)
    cv.drawCircle(cxm, fy0 - 26, 10, fill(shade(RED, 0.4 + 0.6 * gw)))


# ============ SAHNE 1: kanca (ileriden bir an: son kapi) ============
def scene1(cv, t):
    ts, k = step(t), kk(t)
    q0, b0 = frac('n2', 0.40), frac('n2', 0.74)
    u_ = smooth(seg(ts, q0, E('n2'))); z = 1 + 0.16 * u_
    hd = (PL[0], 840)
    with zoom(cv, z, hd, (lerp(hd[0], 286, u_), hd[1])):
        room(cv, 3, k, state='blink', msg='?' if ts >= q0 else None, beyond='lift')
        if ts < S('n2') - 0.1: L_ = ('endise', {}, 2.0); U_ = ('sakin', HOLDB, 2.0)
        elif ts < b0: L_ = ('endise', dict(crouch=14, bob=alt(k, 0, 5, 2)), alt(k, 2.0, -1.0, 6)); U_ = ('sakin', HOLDB, -2.0)
        else: L_ = ('uzgun', dict(HEAD_R, crouch=18, lean=6), 0, dict(pkg_left=True, down=True)); U_ = ('merak', HOLDB, -2.0)
        with stage(cv):
            fs = people(cv, ts, {'L': PL, 'U': PU}, {'L': L_, 'U': U_})
            bo = (-76, -246) if FMT == 'v' else (-204, -150)        # yatayda ust kenar yakin: balon basin soluna
            bubble_q(cv, fs['L']['head'][0] + bo[0], fs['L']['head'][1] + bo[1], smooth(seg(ts, b0, b0 + 0.3)), top=None, side=-1)
    dim(cv, 0.24)
    title_card(cv, t)


# ============ SAHNE 2: asansor (hatirlatma, sayim, kural) ============
def scene2(cv, t):
    ts, k = step(t), kk(t)
    dg = B('ding')
    dark = ts < S('n3') - 0.05
    flick = S('n3') - 0.05 <= ts < S('n3') + 0.55
    u = smooth(seg(ts, dg[0] + 0.6, dg[0] + 1.8))
    sh = jit(k, 5 if S('l2') + 0.3 <= ts < dg[0] + 0.15 else 0)
    vt = TL.talk('V', ts); look3 = ts >= frac('v3', 0.08)
    _VIEW['glow'] = (0.5 + 0.5 * alt(k, 0, 1, 2)) if look3 else 0.35
    cabin(cv, sh, u, lamp=0.9, view=room_view)
    LK = dict(lean=-6, belly=-14); UL = dict(HOLDB, **LOOKUP); q = []
    if ts < frac('n4', 0.6): L_ = ('uzgun', {}, 0, dict(down=ts < frac('n3', 0.9))); U_ = ('uzgun', HOLDB, 0)
    elif ts < S('l1') - 0.1: L_ = ('endise', {}, 1.5); U_ = ('sakin', HOLDB, -2.0)                        # iki kisi: birbirlerine bakarlar
    elif on(ts, 'l1', 0.1, 0.15): L_ = ('uzgun', {}, 1.5); U_ = ('sakin', HOLDB, -2.0)
    elif on(ts, 'u1', 0.15, 0.15):
        L_ = ('endise', {}, 1.5); U_ = ('sakin', HOLDB, -2.0)
        if ts >= frac('u1', 0.5): q = ['L', 'U']
    elif on(ts, 'l2', 0.15, 0.1): L_ = ('kararli', SELF, 1.5, dict(pkg_left=True)); U_ = ('sakin', HOLDB, -2.0)
    elif ts < dg[0] + 0.5: L_ = ('endise', LK, 0); U_ = ('sakin', UL, 0)
    elif ts < S('v1') - 0.1: L_ = ('saskin', {}, 0.6); U_ = ('sakin', {}, 0, dict(back=True))             # kapi acilir
    elif on(ts, 'v1', 0.1, 0.2): L_ = ('saskin' if ts >= frac('v1', 0.72) else 'endise', LK, 0); U_ = ('sakin', UL, 0)
    elif on(ts, 'v2', 0.1, 0.2): L_ = ('endise', COWER_HOLD, 0); U_ = ('sakin', UL, 0)
    elif not look3: L_ = ('endise', LK, 0); U_ = ('sakin', UL, 0)
    else: L_ = ('endise', THUMB, 0.8, dict(pkg_left=True)); U_ = ('sakin', {}, 0, dict(back=True))        # karsidaki kapiya bakarlar
    with stage(cv, *sh):
        people(cv, ts, CAB, {'L': L_, 'U': U_})
        for w in q: badge(cv, w, '?', red=True)
    if dark: dim(cv, 0.94)
    elif flick: dim(cv, 0.94 if (k * 5) % 7 < 3 else 0.3)
    else: dim(cv, 0.2)
    display(cv, sh, '16', red=True, level=vt, k=k)
    if dark or (flick and (k * 5) % 7 < 3):
        with stage(cv): dark_eyes(cv, ('L', 'U'), red=('L', 'U')[(k // 5) % 2])
    if S('n3') + 0.6 <= ts < S('l1') - 0.25:                 # dort kisi bindi, ucu gitti; ama iki kisi var
        marks = [(CREAM, 'on'), (NAVY, 'x'), (TAN, 'x'), (CORAL, 'x' if ts >= frac('n3', 0.78) else 'on')]
        if ts >= frac('n4', 0.8): marks.append((RED, 'on'))
        tally(cv, marks)


# ============ SAHNE 3: birinci oda: kucuk bir yalan; birinci soru ============
def scene3(cv, t):
    ts, k = step(t), kk(t)
    a0, a1 = TL.span(3); ob, li, tr = B('out'), B('lie'), B('truth')
    off = -340 * (1 - seg(ts, ob[0] + 0.1, ob[1] - 0.05))
    red_on, red_off = li[0] + RED_ON, tr[0] + 0.25
    red = seg(ts, red_on, red_on + 0.12) * (1 - smooth(seg(ts, red_off, red_off + 0.5)))
    sh_in = li[0] + SHADOW_IN
    sa = smooth(seg(ts, sh_in, sh_in + 0.5)) * (1 - smooth(seg(ts, tr[0] + 0.2, tr[0] + 0.9)))
    sx = lerp(-40, 112, smooth(seg(ts, sh_in, sh_in + 1.4))) - 130 * smooth(seg(ts, tr[0] + 0.2, tr[0] + 1.0))
    reach = 0.7 * smooth(seg(ts, S('u3'), S('u3') + 1.0)) * (1 - smooth(seg(ts, tr[0], tr[0] + 0.5)))
    vt = TL.talk('V', ts)
    msg = 'YALAN' if red_on <= ts < red_off else ('DOĞRU' if red_off + 0.1 <= ts < tr[1] - 0.1 else None)
    room(cv, 1, k, state='blink' if ts >= S('v4') - 0.2 else 'red', level=vt, msg=msg, red=red)
    P = {'L': (PL[0] + off, PL[1], PL[2]), 'U': (PU[0] + off, PU[1], PU[2])}
    BRAVE = dict(HIP, lean=-6, belly=-10)
    if ts < ob[1] - 0.05:                                    # asansorden cikarlar
        L_ = ('endise', walk(off + 400, PL[2], 1, hold=True, off=0.7), 0); U_ = ('sakin', dict(walk(off + 400, PU[2], 1, hold=True, off=0.3), **HOLDB), 0)
    elif ts < S('l3') - 0.15: L_ = ('endise', dict(crouch=12), alt(k, -1.5, 1.5, 5)); U_ = ('merak', HOLDB, -2.0)
    elif ts < red_on: L_ = ('kararli', dict(BRAVE, bob=alt(k, 0, 6, 1)), 1.5, dict(pkg_left=True)); U_ = ('merak', HOLDB, -2.0)     # dizleri titrer
    elif ts < sh_in + 0.4: L_ = ('saskin', LOOKUP, 0.8); U_ = ('saskin', dict(HOLDB, **LOOKUP), -0.6)     # isik kizarir: yukari bakarlar
    elif ts < S('u3') - 0.1: L_ = ('panik', COWER_HOLD, -1.5); U_ = ('saskin', HOLDB, -2.0)               # karalti
    elif on(ts, 'u3', 0.1, 0.15): L_ = ('panik', COWER_HOLD, alt(k, -1.5, 0, 3)); U_ = ('bagir', POINT_LEO, -2.0, dict(ber='R'))
    elif ts < tr[0] + 0.3: L_ = ('bagir' if on(ts, 'l4', 0.05, 0.1) else 'panik', COWER_HOLD, 0); U_ = ('endise', HOLDB, -2.0)
    elif ts < S('v4') - 0.2: L_ = ('yorgun', SLUMP, 0); U_ = ('sakin', HOLDB, -2.0 if ts < tr[0] + 1.0 else 0)
    elif on(ts, 'v4', 0.2, 0.3): L_ = ('endise', {}, 2.0); U_ = ('sakin', HOLDB, 2.0)
    else: L_ = ('merak', {}, 1.5); U_ = ('kararli', HOLDB, 2.0)
    with stage(cv):
        if sa > 0: shadow(cv, sx, 0.74, sa * 0.96, reach, k)
        people(cv, ts, P, {'L': L_, 'U': U_})
    red_wash(cv, red)
    dim(cv, 0.24)
    flash(cv, seg(ts, a1 - 0.4, a1 - 0.12))


# ---------- geri donusler: lobi ----------
def lobby_extra(cv):
    """lobinin yanlari (yatayda gorunur): saksi ve kat rehberi (bina 12 katli)"""
    with stage(cv):
        px = -250
        for dx_, dy_, r_ in ((0, -214, 64), (-56, -168, 46), (58, -174, 48), (-20, -282, 42), (34, -270, 38)):
            def d(c_, r_=r_): stil.R.seed(40 + r_); yarn_ball(c_, r_ + 12, r_ + 12, r_, (86, 140, 100), rows=5)
            blit(cv, sprite(('leaf', r_), 2 * r_ + 40, 2 * r_ + 44, d), px + dx_ - r_ - 12, FLOOR + dy_ - r_ - 12)
        poly(cv, [(px - 62, FLOOR - 132), (px + 62, FLOOR - 132), (px + 44, FLOOR), (px - 44, FLOOR)], (168, 96, 70))
        cv.drawLine(px - 56, FLOOR - 112, px + 56, FLOOR - 112, dashed((226, 170, 140), 3, 210, (10, 8)))
        rc = LTRB(1160, 640, 1450, 1000)
        cv.drawRRect(RRXY(rc.makeOffset(5, 8), 14, 14), fill((6, 8, 18), 120)); cv.drawRRect(RRXY(rc, 14, 14), fill((44, 50, 62)))
        cv.drawRRect(RRXY(rc.makeInset(10, 10), 9, 9), dashed((150, 160, 190), 2.5, 200, (9, 7)))
        text(cv, 'KATLAR', 1305, 708, 40, CREAM)
        for i in range(12): text(cv, str(i + 1), 1225 + 80 * (i % 3), 778 + 62 * (i // 3), 38, (214, 222, 236))


def no13(cv, x, y, a, side=1):
    """konusma balonu: ustu cizili 13 ('boyle bir kat yok')"""
    if a <= 0: return
    r = 72; A = 255 * clamp(a)
    poly(cv, [(x - side * 10, y + r - 14), (x + side * 34, y + r - 22), (x + side * 44, y + r + 34)], CREAM, A)
    cv.drawCircle(x + 3, y + 5, r, fill((4, 6, 20), 100 * clamp(a))); cv.drawCircle(x, y, r, fill(CREAM, A)); cv.drawCircle(x, y, r - 8, dashed(INKBLUE, 2.5, 150 * clamp(a), (8, 7)))
    text(cv, '13', x, y + 24, 68, INKBLUE, a=A)
    cv.drawLine(x - 46, y + 38, x + 46, y - 38, stroke(RED, 11, A))


def rewind_fx(cv, a, k):
    """geri sarma: yatay tarama cizgileri ve geri sar isareti (ekran koordinati)"""
    if a <= 0: return
    for y in range((k * 23) % 38, H, 38): cv.drawRect(skia.Rect.MakeLTRB(0, y, W, y + 5), fill((255, 255, 255), 34 * a))
    for y, hh in ((H * 0.31 + (k * 61) % 90, 26), (H * 0.66 - (k * 47) % 110, 18)): cv.drawRect(skia.Rect.MakeLTRB(0, y, W, y + hh), fill((255, 255, 255), 46 * a))
    x, y, u = (W - 196, 600, 1.0) if FMT == 'v' else (330, 300, 0.86)
    cv.drawRRect(RRXY(skia.Rect.MakeLTRB(x - 96 * u, y - 60 * u, x + 96 * u, y + 60 * u), 26 * u, 26 * u), fill(INKBLUE, 215 * a))
    for i in (0, 1):
        ox = x - 58 * u + i * 62 * u
        poly(cv, [(ox, y), (ox + 54 * u, y - 34 * u), (ox + 54 * u, y + 34 * u)], CREAM, 255 * a)


# ============ SAHNE 4: geri donus 1: bir yil once (sepya) ============
def scene4(cv, t):
    ts, k = step(t), kk(t)
    a0, a1 = TL.span(4); up = B('up')
    go0, go1 = frac('u5', 0.6), E('u5') + 0.15               # anne asansore yurur
    mx = lerp(330, 540, seg(ts, go0, go1)); ins = seg(mx, 455, 540)
    shut0, stop, ret0 = up[0] + SHUT, up[0] + STOP13, frac('u7', 0.6)
    u = (1 - smooth(seg(ts, shut0, shut0 + 0.9))) if ts < ret0 else smooth(seg(ts, ret0 + 0.45, ret0 + 1.3))
    if ts < shut0 + 0.9: num, nred = '1', False
    elif ts < stop: num, nred = str(2 + int(10.99 * seg(ts, shut0 + 0.9, stop))), False
    elif ts < ret0: num, nred = '13', True
    elif ts < ret0 + 0.45: num, nred = str(max(1, 12 - int(11.99 * seg(ts, ret0, ret0 + 0.45)))), False
    else: num, nred = '1', False
    w0, w1 = stop + 0.3, frac('u7', 0.42)                    # Luna kapinin onune yurur
    lx = lerp(180, 540, seg(ts, w0, w1)); adults = S('u7b') - 0.3
    ad = smooth(seg(ts, adults, adults + 0.4))

    def inside(c):
        if ts < ret0 and ins > 0:
            wv = alt(k, WAVE_A, WAVE_B, 2) if on(ts, 'u6', 0.1, 0.5) else {}
            actor(c, ts, 'M', 'mutlu', wv, -1.5, place=(540, FLOOR - 6, 0.60), alpha=ins, talk=None)
    with tint(cv, sepia_m(0.84, 0.08)):
        lobby(cv, u, inside=inside); lobby_extra(cv)
        with stage(cv):
            if ins < 1:                                      # anne disarida: Luna'ya bakar, sonra kapiya yurur
                P = walk(mx - 330, 0.66, 1) if ts > go0 else {}
                actor(cv, ts, 'M', 'mutlu', P, -1.5 if ts <= go0 else 1.0, place=(mx, GY - 20, 0.66), alpha=1 - ins, talk=None)
            gy = GY + 6
            if ts < go0: U_ = ('mutlu', {}, 1.5)
            elif ts < S('u6') - 0.1: U_ = ('mutlu', {}, 2.0)
            elif ts < shut0 + 0.9: U_ = ('mutlu', alt(k, WAVE_A, WAVE_B, 2), 2.0)                        # el sallar
            elif ts < stop: U_ = ('merak', LOOKUP, 1.5)                                                   # gostergeye bakar
            elif ts < w0: U_ = ('saskin', LOOKUP, 1.5)
            elif ts < w1: U_ = ('endise', walk(lx - 180, 0.5, 1), 1.0)
            elif ts < adults: U_ = ('sakin', {}, 0, dict(back=True))                                      # kapinin onunde bekler
            else: U_ = ('uzgun', LOOKUP, alt(k, -1.5, 1.5, 7))
            kw = dict(U_[3]) if len(U_) > 3 else {}
            if ad > 0:                                       # buyukler: 'bu binada 13. kat yok'
                figure(cv, 250, GY - 20, 0.66, (150, 140, 128), 'sakin', dict(lean=14, belly=-8, aR=(120, 110, 176, 60)), 51, look=1.5, alpha=ad)
                figure(cv, 850, GY - 20, 0.66, (124, 134, 150), 'yorgun', dict(lean=-14, belly=8, aL=(-120, 110, -176, 60)), 53, look=-1.5, alpha=ad)
            actor(cv, ts, 'U', U_[0], U_[1], U_[2], place=(lx, gy, 0.5), talk=None, **kw)
            if ad > 0:
                no13(cv, 334, 664, smooth(seg(ts, frac('u7b', 0.2), frac('u7b', 0.2) + 0.2)), -1)
                no13(cv, 766, 664, smooth(seg(ts, frac('u7b', 0.55), frac('u7b', 0.55) + 0.2)), 1)
        dim(cv, lerp(0.08, 0.36, smooth(seg(ts, stop, S('u7b')))))
        display(cv, (0, 0), num, red=nred)
    memory_frame(cv, 'BİR YIL ÖNCE', (246, 232, 200))
    flash(cv, max(1 - seg(ts, a0 + 0.1, a0 + 0.55), seg(ts, a1 - 0.4, a1 - 0.12)))


# ============ SAHNE 5: birinci kapi acilir ============
def scene5(cv, t):
    ts, k = step(t), kk(t)
    a0, a1 = TL.span(5); op, th = B('open1'), B('thru1')
    ok0 = op[0] + 0.5
    open_u = smooth(seg(ts, op[0] + 0.8, op[0] + 1.7))
    room(cv, 1, k, open_u=open_u, state='green' if ts >= ok0 else 'blink', msg='DOĞRU' if ok0 <= ts < S('l5') + 0.5 else None)
    xu = lerp(PU[0], DMID, seg(ts, th[0] + 0.05, th[1] - 0.25)); xl = lerp(PL[0], 660, seg(ts, th[0] + 0.2, th[1]))
    P = {'L': (xl, PL[1], PL[2]), 'U': (xu, PU[1], PU[2])}; n = 0
    if ts < ok0: L_ = ('uzgun', {}, 1.5); U_ = ('uzgun', HOLDB, 2.0)
    elif ts < S('l5') - 0.1: L_ = ('saskin', {}, 2.0); U_ = ('sakin', HOLDB, 2.0)                         # kapi acilir
    elif on(ts, 'l5', 0.1, 0.15): L_ = ('uzgun', {}, 1.5); U_ = ('sakin', HOLDB, -2.0)
    elif ts < th[0] + 0.05:
        L_ = ('merak', {}, 1.5); U_ = ('sakin', HOLDB, -2.0)
        n = sum(ts >= frac('u8', f) for f in (0.45, 0.6, 0.75, 0.9))
    else:
        L_ = ('endise', walk(xl - PL[0], PL[2], 1, hold=True, off=0.7) if ts >= th[0] + 0.2 else {}, 2.0)
        U_ = ('sakin', dict(walk(xu - PU[0], PU[2], 1, hold=True, off=0.3), **HOLDB), 2.0, dict(alpha=1 - seg(xu, 770, DMID)))
    with stage(cv):
        fs = people(cv, ts, P, {'L': L_, 'U': U_})
        if n: fingers(cv, fs['U']['head'][0] + 108, fs['U']['head'][1] - 150, n, LILAC, r=62)
    dim(cv, 0.24)
    flash(cv, 1 - seg(ts, a0 + 0.1, a0 + 0.5))


# ============ SAHNE 6: ikinci oda: ikinci soru ============
def scene6(cv, t):
    ts, k = step(t), kk(t)
    a0, a1 = TL.span(6); ib = B('in2')
    off = -250 * (1 - seg(ts, ib[0], ib[1] - 0.05))
    vt = TL.talk('V', ts)
    room(cv, 2, k, state='blink' if ts >= S('v5') - 0.2 else 'red', level=vt)
    P = {'L': (PL[0] + off, PL[1], PL[2]), 'U': (PU[0] + off, PU[1], PU[2])}; n = 0
    if off < 0: L_ = ('endise', walk(off + 300, PL[2], 1, hold=True, off=0.7), 0); U_ = ('sakin', dict(walk(off + 300, PU[2], 1, hold=True, off=0.3), **HOLDB), 0)
    elif ts < S('u9') - 0.15: L_ = ('endise', {}, 1.5 if ts >= frac('v5', 0.3) else 2.0); U_ = ('sakin', HOLDB, 2.0)
    else:
        L_ = ('merak', {}, 1.5); U_ = ('kararli', HOLDB, 2.0 if ts < frac('u9', 0.5) else -2.0)
        n = 4 if ts < frac('u9', 0.5) else 1 + sum(ts >= frac('u9', f) for f in (0.72, 0.84, 0.96))
    with stage(cv):
        fs = people(cv, ts, P, {'L': L_, 'U': U_})
        if n: fingers(cv, fs['U']['head'][0] + 108, fs['U']['head'][1] - 150, n, LILAC, r=62)
    dim(cv, 0.24)
    flash(cv, seg(ts, a1 - 0.4, a1 - 0.12))


# ============ SAHNE 7: geri donus 2: o aksam, lobi (renkli ve net) ============
BOARD = (('K', 0.62, GY - 20, 'yorgun'), ('Z', 0.62, GY - 20, 'sakin'), ('S', 0.62, GY - 20, 'mutlu'), ('U', 0.50, GY - 4, 'mutlu'))
BCOL = (NAVY, CORAL, TAN, LILAC)
WAITP = {'S': (112, GY - 20, 0.62), 'Z': (318, GY - 20, 0.62), 'K': (846, GY - 20, 0.62), 'U': (694, GY + 26, 0.50)}


def scene7(cv, t):
    ts, k = step(t), kk(t)
    a0, a1 = TL.span(7); df = B('doorfb')
    marks = []; rew = 0.0
    with tint(cv, sat_m(1.22, 1.05)):
        if ts < df[0]:                                       # dort kisi sirayla biner; Leo sorunca goruntu geri sarilir
            f0 = S('u10') - 0.15; v = 775 / (E('u10') - f0 - 0.1)
            rew = seg(ts, S('l6') + 0.05, E('l6'))
            tau = max(0.0, min(ts, S('l6')) - f0) * (1 - rew)
            lobby(cv, 1.0, glow=1.0); lobby_extra(cv)
            n_in = 0
            with stage(cv):
                for i in range(3, -1, -1):
                    w, s, gy, ex = BOARD[i]; x0 = 300 - 170 * i; x = x0 + v * tau
                    if x >= 515: n_in += 1
                    if x >= 560: continue
                    P = walk(x - x0, s, 1, off=i * 0.27) if tau > 0 else {}
                    actor(cv, ts, w, ex, P, 1.0, place=(x, gy, s), alpha=1 - seg(x, 470, 560), talk=None)
            dim(cv, 0.06)
            display(cv, (0, 0), '1')
            marks = [(BCOL[i], 'on') for i in range(n_in)]
        else:                                                # o an: asansor gelir, kapi acilir. Leo zaten iceride
            dg = df[0] + FB_DING
            u = smooth(seg(ts, dg + 0.5, dg + 1.7)); turned = ts >= dg + 0.3
            def inside(c): actor(c, ts, 'L', 'sakin', {}, 0, place=(540, FLOOR - 6, 0.60), talk=None)    # elinde paket; kravat ve gozluk henuz yok
            zu = smooth(seg(ts, S('u11'), E('u11')))
            with zoom(cv, 1 + 0.2 * zu, (540, 900)):
                lobby(cv, u, inside=inside); lobby_extra(cv)
                with stage(cv):
                    for i, w in enumerate(('S', 'Z', 'K', 'U')):
                        if turned: actor(cv, ts, w, 'sakin', {}, 0, place=WAITP[w], back=True, talk=None)
                        elif w == 'K': actor(cv, ts, w, 'yorgun', alt(k, PRESS_A, PRESS_B, 2), 1.5, place=WAITP[w], talk=None)   # cagri dugmesine basip durur
                        elif w == 'S': actor(cv, ts, w, 'mutlu', {}, 2.0, place=WAITP[w], talk=None)
                        elif w == 'Z': actor(cv, ts, w, 'sakin', {}, 1.0, place=WAITP[w], talk=None)
                        else: actor(cv, ts, w, 'mutlu', {}, 0, place=WAITP[w], talk=None)
                    if u > 0.9: badge_at(cv, 540, 700, '5', red=True, a=seg(u, 0.9, 1.0), r=40)
                dim(cv, 0.06)
                display(cv, (0, 0), '1')
            marks = [(c, 'on') for c in BCOL] + ([(RED, 'on')] if u > 0.9 else [])
    rewind_fx(cv, min(seg(rew, 0, 0.12), 1 - seg(rew, 0.92, 1.0)) if 0 < rew < 1 else 0, k)
    memory_frame(cv, 'O AKŞAM', (255, 246, 222))
    tally(cv, marks)
    flash(cv, max(1 - seg(ts, a0 + 0.1, a0 + 0.55), 0.8 * (1 - seg(ts, df[0], df[0] + 0.35)) if ts >= df[0] else 0, seg(ts, a1 - 0.4, a1 - 0.12)))


# ============ SAHNE 8: ikinci oda: kapi acilir; Leo itiraz eder (ikinci yalan) ============
def scene8(cv, t):
    ts, k = step(t), kk(t)
    a0, a1 = TL.span(8); bk, li, hs, th = B('back'), B('lie2'), B('hush'), B('thru2')
    ok0 = bk[0] + 0.4
    open_u = smooth(seg(ts, bk[0] + 0.7, bk[0] + 1.5))
    red_on, red_off = li[0] + RED_ON, hs[0] + 0.9
    red = seg(ts, red_on, red_on + 0.12) * (1 - smooth(seg(ts, red_off, red_off + 0.5)))
    sh_in = li[0] + SHADOW_IN
    sa = smooth(seg(ts, sh_in, sh_in + 0.4)) * (1 - smooth(seg(ts, hs[0] + 0.7, hs[0] + 1.4)))
    sx = lerp(-20, 150, smooth(seg(ts, sh_in, sh_in + 0.9))) - 160 * smooth(seg(ts, hs[0] + 0.7, hs[0] + 1.5))
    reach = smooth(seg(ts, sh_in + 0.5, li[0] + 1.7)) * (1 - smooth(seg(ts, hs[0] + 0.5, hs[0] + 0.9)))
    msg = 'DOĞRU' if ok0 <= ts < S('l7') - 0.05 else ('YALAN' if red_on <= ts < red_off else None)
    room(cv, 2, k, open_u=open_u, state='green' if ts >= ok0 else 'blink', msg=msg, red=red)
    xu = lerp(PU[0], DMID, seg(ts, th[0] + 0.05, th[1] - 0.25)); xl = lerp(PL[0], 660, seg(ts, th[0] + 0.2, th[1]))
    P = {'L': (xl, PL[1], PL[2]), 'U': (xu, PU[1], PU[2])}; hand = False
    if ts < ok0: L_ = ('saskin', {}, 1.5); U_ = ('sakin', HOLDB, -2.0)
    elif ts < S('l7') - 0.1: L_ = ('saskin', dict(lean=-10, belly=10), 2.0); U_ = ('sakin', HOLDB, 2.0)   # kapi acilir: Luna dogru soyledi
    elif ts < red_on: L_ = ('bagir' if on(ts, 'l7', 0.1, 0.05) else 'kararli', OBJECT, 1.5, dict(pkg_left=True)); U_ = ('saskin', HOLDB, -2.0)
    elif ts < sh_in + 0.5: L_ = ('saskin', LOOKUP, 0.8); U_ = ('saskin', dict(HOLDB, **LOOKUP), -0.6)
    elif ts < S('u12') - 0.1: L_ = ('panik', COWER_HOLD, -1.5); U_ = ('saskin', HOLDB, -2.0)              # el omzunda
    elif ts < hs[0] + 0.15: L_ = ('panik', COWER_HOLD, 0); U_ = ('bagir', POINT_LEO, -2.0, dict(ber='R'))
    elif ts < S('l7b') - 0.1: L_ = ('panik' if ts < hs[0] + 1.0 else 'endise', dict(MOUTH, crouch=16), 0, dict(pkg_left=True)); U_ = ('endise', HOLDB, -2.0); hand = True
    elif ts < th[0] + 0.05: L_ = ('uzgun', dict(crouch=14, lean=8), 2.0 if ts < frac('l7b', 0.4) else 1.5); U_ = ('sakin', HOLDB, -2.0)
    else:
        L_ = ('uzgun', walk(xl - PL[0], PL[2], 1, hold=True, off=0.7) if ts >= th[0] + 0.2 else {}, 2.0)
        U_ = ('sakin', dict(walk(xu - PU[0], PU[2], 1, hold=True, off=0.3), **HOLDB), 2.0, dict(alpha=1 - seg(xu, 770, DMID)))
    with stage(cv):
        if sa > 0: shadow(cv, sx, 0.74, sa * 0.96, reach, k)
        fs = people(cv, ts, P, {'L': L_, 'U': U_})
        if hand:                                             # eli agzinda: sustu
            f = fs['L']; mx_, my_ = mouth_of(f); hand_ball(cv, mx_ + 4, my_ + 6, 36 * f['s'], TEAL, 4)
    red_wash(cv, red)
    dim(cv, 0.24)
    flash(cv, 1 - seg(ts, a0 + 0.1, a0 + 0.5))


# ============ SAHNE 9: ucuncu oda: son soru ============
def scene9(cv, t):
    ts, k = step(t), kk(t)
    ib, tk, wt, lv = B('in3'), B('think'), B('wait'), B('leave')
    off = -250 * (1 - seg(ts, ib[0], ib[1] - 0.05))
    grn = wt[0] + GREEN
    open_u = smooth(seg(ts, grn + 0.25, grn + 1.3))
    vt = TL.talk('V', ts)
    xu = lerp(PU[0], DMID, seg(ts, lv[0] + 0.15, lv[0] + 1.5)); xl = lerp(PL[0], DMID, seg(ts, lv[0] + 0.3, lv[0] + 2.3))
    P = {'L': (xl + off, PL[1], PL[2]), 'U': (xu + off, PU[1], PU[2])}
    zu = smooth(seg(ts, frac('u13', 0.3), E('u13') - 0.1)) * (1 - smooth(seg(ts, lv[0], lv[0] + 0.4)))
    ba = smooth(seg(ts, tk[0] + 0.7, tk[0] + 1.0)) * (1 - smooth(seg(ts, frac('l8', 0.6), E('l8'))))
    ring = False
    with zoom(cv, 1 + 0.32 * zu, PKG, (lerp(PKG[0], 440, zu), lerp(PKG[1], 1010, zu))):
        room(cv, 3, k, open_u=open_u, state='green' if ts >= grn else 'blink', level=vt, msg='DOĞRU' if grn <= ts < S('l9') - 0.2 else None, beyond='lift')
        if off < 0: L_ = ('endise', walk(off + 300, PL[2], 1, hold=True, off=0.7), 0); U_ = ('sakin', dict(walk(off + 300, PU[2], 1, hold=True, off=0.3), **HOLDB), 0)
        elif ts < tk[0] - 0.05: L_ = ('endise', {}, 2.0); U_ = ('merak', HOLDB, -2.0)
        elif ts < S('l8') - 0.1: L_ = ('endise', dict(HEAD_R, crouch=14), alt(k, -1.0, 1.0, 5), dict(pkg_left=True)); U_ = ('merak', HOLDB, -2.0)      # hatirlamaya calisir
        elif ts < wt[0]: L_ = ('uzgun', dict(crouch=20, lean=6), 0, dict(down=True)); U_ = ('merak', HOLDB, -2.0)
        elif ts < grn: L_ = ('endise', COWER_HOLD, 2.0); U_ = ('endise', HOLDB, 2.0)                      # bekleyis
        elif ts < S('l9') - 0.1: L_ = ('saskin', {}, 2.0); U_ = ('sakin', HOLDB, 2.0 if ts < E('n7') else -2.0)
        elif ts < S('u13') - 0.1: L_ = ('uzgun', dict(crouch=10), 1.5); U_ = ('sakin', HOLDB, -2.0)
        elif ts < lv[0] + 0.15: L_ = ('uzgun', dict(crouch=10, lean=4), 0, dict(down=True)); U_ = ('sakin', POINT_PK, -2.0, dict(ber='R')); ring = True
        else:
            L_ = ('uzgun', walk(xl - PL[0], PL[2], 1, hold=True, off=0.7) if ts >= lv[0] + 0.3 else {}, 2.0, dict(alpha=1 - seg(xl, 760, DMID)))
            U_ = ('sakin', dict(walk(xu - PU[0], PU[2], 1, hold=True, off=0.3), **HOLDB), 2.0, dict(alpha=1 - seg(xu, 770, DMID)))
        with stage(cv):
            if ring:                                         # paket: icindeki cevap
                gl = fill((255, 226, 150), 90 + 50 * alt(k, 0, 1, 3)); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 34))
                cv.drawOval(LTRB(PKG[0] - 120, PKG[1] - 96, PKG[0] + 120, PKG[1] + 92), gl)
            fs = people(cv, ts, P, {'L': L_, 'U': U_})
            if ba > 0: bubble_q(cv, fs['L']['head'][0] - 76, fs['L']['head'][1] - 246, ba, side=-1)
    dim(cv, 0.24)


# ============ SAHNE 10: yine asansor: besinci kisi ============
def scene10(cv, t):
    ts, k = step(t), kk(t)
    vt = TL.talk('V', ts); mv = E('v7') + 0.1
    sh = jit(k, 4 if mv <= ts < mv + 1.6 else 0)
    cabin(cv, sh, 0.0)
    five = frac('n8', 0.64)
    if ts < S('v7') - 0.05: L_ = ('uzgun', {}, 0, dict(down=True)); U_ = ('sakin', HOLDB, -2.0)
    elif on(ts, 'v7', 0.05, 0.2): L_ = ('endise', dict(lean=-6, belly=-14), 0); U_ = ('sakin', dict(HOLDB, **LOOKUP), 0)
    elif ts < five: L_ = ('uzgun', {}, 0, dict(down=True)); U_ = ('sakin', HOLDB, -2.0)                   # Leo paketine bakar
    else: L_ = ('endise', {}, 0); U_ = ('sakin', HOLDB, -2.0)
    with stage(cv, *sh):
        people(cv, ts, CAB, {'L': L_, 'U': U_})
        if ts >= five: badge(cv, 'L', '5', red=True)
    dim(cv, lerp(0.2, 0.42, smooth(seg(ts, five, E('n8') + 0.4))))
    display(cv, sh, '17' if ts >= frac('v7', 0.72) else '16', red=True, level=vt, k=k)
    if ts >= S('n8') - 0.1:                                  # dort kisi bindi; besinci hep icerideydi
        marks = [(c, 'on') for c, f in zip(BCOL, (0.26, 0.32, 0.38, 0.44)) if ts >= frac('n8', f)]
        if ts >= five: marks.append((TEAL, 'on'))
        tally(cv, marks)


# ============ SAHNE 11: bitis karti ============
def scene11(cv, t):
    ts, k = step(t), kk(t)
    a0, _ = TL.span(11)
    cabin(cv, (0, 0), 0.0); dim(cv, 0.88)
    cx, cy, s = (W / 2, 880, 1.9) if FMT == 'v' else (W / 2, 506, 1.3)
    a = smooth(seg(ts, a0 + 0.4, a0 + 1.0))
    gl = fill((255, 226, 150), (70 + 26 * alt(k, 0, 1, 5)) * a); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 50 * s / 1.9))
    cv.drawOval(LTRB(cx - 210 * s / 1.9 * 1.9, cy - 150 * s / 1.9 * 1.4, cx + 210 * s / 1.9 * 1.9, cy + 150 * s / 1.9 * 1.4), gl)
    package(cv, {'handL': (cx, cy), 'handR': (cx, cy)}, s, alpha=a)                                       # gonderensiz paket: cevap icinde
    badge_at(cv, cx + 88 * s, cy - 70 * s, '?', red=True, a=a, r=30 * s / 1.3 if FMT == 'h' else 46)
    c_ = seg(t, a0 + 0.3, a0 + 0.8)
    card(cv, [('Leo kim?', 62 if FMT == 'v' else 70, CREAM), ('Yorumlara yaz', 40, (176, 190, 232)), ('5. Bölüm: Paket', 46, (255, 110, 96))], c_, cy=450 if FMT == 'v' else 168)
    abone(cv, t, a0 + ABONE_END, pos=(W / 2, 1235) if FMT == 'v' else (W / 2, 770))


if __name__ == '__main__':
    run({1: scene1, 2: scene2, 3: scene3, 4: scene4, 5: scene5, 6: scene6, 7: scene7, 8: scene8, 9: scene9, 10: scene10, 11: scene11},
        white=((3, 4), (4, 5), (6, 7), (7, 8)))
