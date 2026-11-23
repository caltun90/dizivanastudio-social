"""Son Vagon, 3. Bolum: Yedigol. Yalnizca sahneler; ortak parcalar ../ortak.py icinde.
Yapi: TERSTEN ANLATIM. Bolum sondan (SIMDI 00:00) baslar; her geri sarista bant geri sarma efekti, donen saat ve
"N DAKIKA ONCE" damgasi gelir; sag ustte kucuk saat hep durur.
SIMDI: iki numarada Mia tek basina (kanca) -> disaridan: iki vagon -> baslik -> geri sarma (uc numara sisten geri gelir) ->
23:58 Yedigol peronu; on kapida orgu el degistirir; kapi; camin ardinda Ada (sessiz); lambalar, sis, bos ray ->
23:55 katlanir koltuk; biletler; pencereden yedi gol -> 23:50 orgudeki istasyon adlari; biten yumak ->
23:45 anons ve levha; Ada oturur -> 23:05 bes numara, ilk anons (sepya): herkes korkar, Ada gulumser ->
23:58 camin ardi, bu kez sesli -> SIMDI -> kapanis.
Yeni mekanlar: Yedigol (pencereden goller ve peron), katlanir koltuklu pencere kosesi, camin ardindan uc numara.
Yeni gorsel fikirler: geri sayan saat ve geri sarma, orgudeki yazilar (cok yakin), camin ardinda sessiz konusma, biten yumak."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import *
from senaryo import ABONE_END, BRAKE, HALT, SHUT, OUT_OFF, GONE, SIT, NAMES_AT, G_OFF

V = FMT == 'v'
QW = (540, 1060) if V else (540, 1000)                     # genis vagon planlarinda sahnenin oturdugu yer
STN = 'YEDİGÖL'
RED = (255, 110, 96)
KS_ = sorted(TL.scenes)
END0 = TL.span(26)[0]
HK = TL.span(2)[0]                                         # kancadan disari plana kesme ani

# ---------- pozlar ----------
SHOWB = dict(aR=(150, 70, 196, -40))                        # elindekini yuzunun yaninda gosterir (buyuk kafa)
FWD = dict(aR=(110, 70, 214, 50))                           # ileriyi (sagi) gosterir
UPR = dict(aR=(130, 20, 200, -110))                         # sag yukariyi gosterir
BACKP = dict(aL=(-120, 40, -200, -20))                      # arkasini (solu) gosterir
PULL = dict(aR=(110, 80, 214, 70), aL=(-40, 110, 60, 130), lean=12)      # iki eliyle saga uzanir
GIVE = dict(aL=(-30, 110, 70, 150), aR=(110, 110, 180, 150), lean=8)     # elindekini saga uzatir
PUSHB = dict(aL=(-110, 90, -176, 70), aR=(40, 110, -60, 120), lean=-8)   # iki eliyle sola iter (almaz)
CHEST = dict(aL=(-70, 110, -12, 160), aR=(70, 110, 12, 160))              # eller goguste
KNITUP = dict(aL=(-84, 70, -40, 110), aR=(84, 70, 40, 110))              # orguyu kaldirip gosterir
SEATP = dict(crouch=70, kL=(-66, -150), kR=(66, -150), fL=(-72, -18), fR=(72, -18))   # katlanir koltukta oturur
WAVE = dict(aR=(100, 40, 130, -70))
GLASSH = dict(aR=(90, 60, 70, -40))
HOLDK = dict(aR=(160, 30, 214, -120))                       # orguyu basinin yaninda, yukarida tutar                         # eli camda


# ---------- trenin aldigi yol (sahne sirasi geriye gider; hiz sahneye gore) ----------
SPEED = {4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 250, 11: 250, 12: 250, 13: 230, 14: 200, 24: 0}
def _speed(t):
    k = KS_[0]
    for s_ in KS_:
        if t >= TL.scenes[s_] - 1e-6: k = s_
    return SPEED.get(k, 420)
_T = np.arange(0, TL.total + 3, 1 / 24.0); _D = np.concatenate([[0], np.cumsum(np.array([_speed(x) for x in _T[:-1]]) / 24.0)])
def SC(t): return float(np.interp(t, _T, _D))


def pl(cam, **xs): return {w: (x - cam, CAST[w]['gy'], CAST[w]['s']) for w, x in xs.items()}
def yarn_strand(cv, pts, w=6):
    p = skia.Path(); p.moveTo(*pts[0])
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]; p.quadTo((x0 + x1) / 2, (y0 + y1) / 2 + (9 if i % 2 else -9), x1, y1)
    cv.drawPath(p, stroke(shade(CORAL, 0.7), w + 3)); cv.drawPath(p, stroke(CORAL, w)); cv.drawPath(p, dashed(shade(CORAL, 1.35), 2, 200, (8, 7)))


# ---------- saat, damga ve geri sarma (kameradan sonra, ekran koordinatinda) ----------
def _mins(hm): return ((hm[0] - 22) % 24) * 60 + hm[1]      # 22:00'dan beri dakika (gece yarisini duz gecer)
def _clock(m): m = int(round(m)); return f'{(22 + m // 60) % 24:02d}:{m % 60:02d}'
NOW_ = (0, 0)
CLOCKS = {}
for _a, _b, _c in ((1, 4, NOW_), (5, 9, (23, 58)), (10, 14, (23, 55)), (15, 18, (23, 50)), (19, 21, (23, 45)), (22, 23, (23, 5)), (24, 24, (23, 58)), (25, 26, NOW_)):
    for _k in range(_a, _b + 1): CLOCKS[_k] = _c
# vurus -> (damga yazisi, onceki saat, yeni saat, kucuk etiket, ileri mi)
JUMPS = {'rw1': ('2 DAKİKA ÖNCE', NOW_, (23, 58), '2 DK ÖNCE', False), 'rw2': ('5 DAKİKA ÖNCE', (23, 58), (23, 55), '5 DK ÖNCE', False),
         'rw3': ('10 DAKİKA ÖNCE', (23, 55), (23, 50), '10 DK ÖNCE', False), 'rw4': ('15 DAKİKA ÖNCE', (23, 50), (23, 45), '15 DK ÖNCE', False),
         'rw5': ('GECENİN BAŞI', (23, 45), (23, 5), 'İLK ANONS', False), 'ff': ('KAPININ ARDINDA', (23, 5), (23, 58), '2 DK ÖNCE', True)}
SUB = {}
for _n, _v in JUMPS.items():
    _k0 = max(s_ for s_ in KS_ if TL.scenes[s_] <= B(_n)[1] + 1e-6) if _n != 'rw1' else 5
    for _k in range(_k0, 27):
        if CLOCKS[_k] == _v[2]: SUB[_k] = _v[3]
        else: break
for _k in (1, 2, 3, 4, 25): SUB[_k] = 'ŞİMDİ'


def otext(cv, s, x, y, size, c=(255, 255, 255), a=1.0, tf=None, bold=True, align='c'):
    f = skia.Font(tf or TFB, size); f.setEmbolden(bold); w = f.measureText(s)
    x0 = x - w / 2 if align == 'c' else (x - w if align == 'r' else x)
    st = stroke((0, 0, 0), size * 0.2, 255 * a); st.setStrokeJoin(skia.Paint.kRound_Join)
    cv.drawString(s, x0 + 3, y + 6, f, fill((0, 0, 0), 110 * a)); cv.drawString(s, x0, y, f, st); cv.drawString(s, x0, y, f, fill(c, 255 * a)); return w


def tri2(cv, x, y, r, c, a=1.0, fwd=False):
    """geri (ya da ileri) sarma isareti: iki ucgen"""
    for j in (0, 1):
        x0 = x + (j - 0.5) * r * 1.5; d = 1 if fwd else -1
        p = skia.Path(); p.moveTo(x0 + d * r * 0.7, y); p.lineTo(x0 - d * r * 0.7, y - r * 0.8); p.lineTo(x0 - d * r * 0.7, y + r * 0.8); p.close()
        st = stroke((0, 0, 0), r * 0.22, 255 * a); st.setStrokeJoin(skia.Paint.kRound_Join); cv.drawPath(p, st); cv.drawPath(p, fill(c, 255 * a))


def chip(cv, t, k):
    """sag ustte kucuk saat + alt etiket"""
    hm = CLOCKS[k]; txt = _clock(_mins(hm)); past = hm != NOW_
    for n, v in JUMPS.items():                               # geri sarilirken saat doner
        a, b = B(n)
        if a <= t < b: txt = _clock(lerp(_mins(v[1]), _mins(v[2]), smooth(seg(t, a, b)))); past = True
    fs = 40 if V else 32; hgt = fs * 1.6
    f = skia.Font(TFB, fs); w = f.measureText('00:00') + (58 if past else 30) * fs / 40
    x1 = W - (40 if V else 56); y0 = 150 if V else 44; x0 = x1 - w - 28
    cv.drawRRect(RRXY(LTRB(x0, y0, x1, y0 + hgt), hgt / 2, hgt / 2), fill((22, 26, 44), 235))
    cv.drawRRect(RRXY(LTRB(x0, y0, x1, y0 + hgt), hgt / 2, hgt / 2), stroke(YEL if past else CREAM, 3, 220))
    if past: tri2(cv, x0 + 30 * fs / 40, y0 + hgt / 2, 9 * fs / 40, YEL)
    cv.drawString(txt, x1 - 16 - f.measureText(txt), y0 + hgt * 0.7, f, fill(YEL if past else CREAM))
    s = SUB.get(k)
    if s:
        f2 = skia.Font(TFB, fs * 0.6); cv.drawString(s, x1 - 8 - f2.measureText(s), y0 + hgt + fs * 0.78, f2, stroke((0, 0, 0), fs * 0.12, 200))
        cv.drawString(s, x1 - 8 - f2.measureText(s), y0 + hgt + fs * 0.78, f2, fill(CREAM))


def rewind_fx(cv, t):
    """geri sarma vurusu: seritler, isaret ve donen saat; sonra damga (etiket + saat)"""
    for n, (label, c0, c1, _s, fwd_) in JUMPS.items():
        a, b = B(n)
        y1, y2, s1, s2 = (336, 462, 76, 124) if V else (250, 336, 50, 80)
        sx_ = W / 2 if V else W - 300
        if a - 0.05 <= t < b:
            u = seg(t, a, b)
            dim(cv, 0.22, (10, 12, 30))
            n_ = int(t * 24)
            for j in range(9):                               # yatay bant seritleri
                y = (j * 233 + n_ * (171 if not fwd_ else -171) + int(a * 100) * 7) % H; h = 6 + (j * 29 + n_ * 7) % 34
                cv.drawRect(LTRB(0, y, W, y + h), fill((255, 255, 255) if j % 3 else (8, 10, 22), 70 if j % 3 else 150))
            tri2(cv, sx_, y1 - s1 * 0.36, s1 * 0.5, YEL, fwd=fwd_)
            otext(cv, _clock(lerp(_mins(c0), _mins(c1), smooth(u))), sx_, y2, s2, YEL, tf=TFB)
        elif b <= t < b + 1.9:
            al = min(1.0, 1 - seg(t, b + 1.5, b + 1.9)); sc_ = lerp(1.18, 1.0, smooth(seg(t, b, b + 0.22)))
            otext(cv, label, sx_, y1, s1 * sc_, CREAM, al)
            otext(cv, _clock(_mins(c1)), sx_, y2, s2 * sc_, YEL, al)


def hud(cv, t, k):
    if t < HK: hook_text(cv, t, 'ADA BİLEREK KALDI', 1 - seg(t, HK - 0.12, HK))
    tb = B('title')
    if k != 26 and not (tb[0] <= t < tb[1]):
        chip(cv, t, k); rewind_fx(cv, t)
    if k == 26: abone(cv, t, END0 + ABONE_END, pos=(W / 2, 1500) if V else (W / 2, 800))


def title_card(cv, t):
    tb = B('title'); a = seg(t, tb[0], tb[0] + 0.35)
    if a > 0:
        dim(cv, 0.5 * a)
        card(cv, [(TITLE, 112, RED), (f'{EP.title()}: {EP_NAME}', 48, CREAM)], a, lerp(0.9, 1.0, smooth(seg(t, tb[0], tb[0] + 0.5))))


# ---------- dekor: katlanir koltuk (uc numara, besinci pencerenin alti) ----------
JX, CAMJ = 2170, 1600                                      # koltugun vagon x'i; bu kosedeki planlarin kamerasi
XMJ = 1900                                                 # Mia'nin durdugu yer
def jump_seat(cv, x, down=1.0):
    """duvara bagli katlanir koltuk (sahne koordinati). down 0: kapali (minder duvara yatik), 1: acik"""
    rc = LTRB(x - 82, 1040, x + 82, 1150)
    cv.drawRRect(RRXY(rc.makeOffset(4, 6), 14, 14), fill((4, 6, 20), 80)); cv.drawRRect(RRXY(rc, 14, 14), fill(SEATC))
    cv.drawRRect(RRXY(rc.makeInset(9, 9), 8, 8), dashed(shade(SEATC, 1.6), 3, 170, (10, 8)))
    if down < 0.5:
        r2 = LTRB(x - 92, 1058, x + 92, 1156); cv.drawRRect(RRXY(r2, 14, 14), fill(shade(SEATC, 1.16)))
        cv.drawRRect(RRXY(r2.makeInset(9, 9), 8, 8), dashed(shade(SEATC, 1.7), 3, 170, (10, 8))); cv.drawRRect(RRXY(LTRB(x - 22, 1066, x + 22, 1078), 6, 6), fill(BRASS))
    else:
        for sd in (-1, 1): cv.drawLine(x + sd * 74, 1176, x + sd * 54, 1214, stroke(BRASS, 6))
        cv.drawRect(LTRB(x - 92, 1162, x + 92, 1184), fill(shade(SEATC, 0.7)))
        r2 = LTRB(x - 96, 1142, x + 96, 1174); cv.drawRRect(RRXY(r2, 14, 14), fill(shade(SEATC, 1.16))); cv.drawLine(x - 82, 1158, x + 82, 1158, dashed(shade(SEATC, 1.7), 3, 170, (10, 8)))


def nook(cv, ts, k, st, out=None, seat=1.0, plate_hi=1.0, spk=None, cam=CAMJ, extra=None):
    """uc numaranin pencere kosesi: katlanir koltuk, sagda on kapi ve levha. st: {kim: ((x, gy, s), (ifade, poz, bakis[, ek]))}"""
    wagon(cv, cam, 3, k, scroll=SC(ts), last=True, out=out, plate_hi=plate_hi, spk=spk)
    with stage(cv):
        jump_seat(cv, JX - cam, seat)
        f = people(cv, ts, {w: v[0] for w, v in st.items()}, {w: v[1] for w, v in st.items()})
        if extra: extra(f)
    return f
ADA_SIT = (JX - CAMJ, FAR, 0.64)
MIA_J = (XMJ - CAMJ, NEAR, 0.70)
def sit(expr='sakin', look=0.0, pose=None, prop='knit', k=0):
    return (expr, dict(SEATP, **(pose or dict(KNIT, lean=alt(k, 0, 3, 4)))), look, dict(prop=prop))


# ---------- dekor: Yedigol (pencereden) ----------
LAKES = [(300, 846, 86, 13), (770, 872, 118, 17), (470, 922, 150, 23), (150, 990, 190, 31), (840, 1024, 214, 36), (420, 1128, 270, 50), (880, 1262, 330, 66)]
def lakes_view(cv, ts, k, count=0.0):
    """pencerenin tam karsidan gorunusu: yedi gol, her birinde ay; uzakta istasyonun isiklari. count: 0..7 sayi rozetleri"""
    a0 = TL.span(13)[0]; pr = ts - a0
    cv.clear(col((8, 12, 24)))
    with stage(cv):
        sx = 1.0 if V else 1.72
        night(cv, 0, k, y_h=812, moon=(560, 560) if V else (640, 590), poles=False)
        g = skia.Paint(); g.setShader(skia.GradientShader.MakeLinear([skia.Point(0, 812), skia.Point(0, 1500)], [col((16, 28, 52)), col((10, 16, 30))]))
        cv.drawRect(LTRB(-700, 812, 1800, 2600), g)
        stx = (930 if V else 1280) - 16 * pr                                   # uzakta istasyon: bina, isikli pencere, lambalar
        cv.drawRect(LTRB(stx - 60, 772, stx + 60, 816), fill((20, 28, 50))); poly(cv, [(stx - 72, 774), (stx + 72, 774), (stx, 746)], (30, 38, 62))
        for wx_ in (-30, 14): cv.drawRRect(RRXY(LTRB(stx + wx_, 786, stx + wx_ + 18, 806), 3, 3), fill((250, 214, 120)))
        for j in range(5):
            lx_ = stx - 96 - j * 42
            gl = fill((255, 226, 150), 130); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)); cv.drawCircle(lx_, 800, 10, gl); cv.drawCircle(lx_, 800, 3.6, fill((255, 240, 200)))
            cv.drawLine(lx_, 803, lx_, 818, stroke((14, 18, 30), 2.5, cap=False))
        for i, (x, y, rx, ry) in enumerate(LAKES):
            dep = (y - 812) / 450.0
            cx = 540 + (x - 540) * sx - pr * (10 + 46 * dep); rx = rx * (1.0 if V else 1.25)
            rc = LTRB(cx - rx, y - ry, cx + rx, y + ry)
            sh = fill((4, 6, 20), 120); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10)); cv.drawOval(rc.makeOffset(0, 6), sh)
            p = skia.Paint(AntiAlias=True); p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y - ry), skia.Point(0, y + ry)], [col((44, 78, 140)), col((22, 40, 92))]))
            cv.drawOval(rc, p); cv.drawOval(rc.makeInset(rx * 0.06, ry * 0.12), dashed((130, 160, 216), 2 + 2 * dep, 170, (10 + 8 * dep, 8 + 6 * dep)))
            mr = ry * 0.52; wob = 1.5 * math.sin(k * 0.3 + i)
            gl = fill((240, 226, 170), 90); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, mr * 0.8)); cv.drawOval(LTRB(cx - mr * 1.9, y - mr, cx + mr * 1.9, y + mr), gl)
            cv.drawOval(LTRB(cx - mr * 1.25 + wob, y - mr * 0.62, cx + mr * 1.25 + wob, y + mr * 0.62), fill((244, 232, 184)))
            for j in (-1, 1): cv.drawLine(cx - mr * 1.6, y + j * mr * 1.05, cx + mr * 1.6, y + j * mr * 1.05, stroke((244, 232, 184), max(1.5, mr * 0.12), 120))
            a = clamp(count - i)
            if a > 0: badge_at(cv, cx, y - ry - 34 - 10 * dep + 12 * (1 - a), str(i + 1), a=a, r=22 + 12 * dep)
        fog(cv, 0.35, k, y=1420, h=300)
        # pencere cercevesi: duvar, perdeler, pirinc cita
        o_ = LTRB(60, 500, 1020, 1470) if V else LTRB(-330, 486, 1410, 1404)
        wall = skia.Path(); wall.addRect(LTRB(-700, -400, 1800, 2600)); wall.addRRect(RRXY(o_, 56, 56)); wall.setFillType(skia.PathFillType.kEvenOdd)
        cv.drawPath(wall, fill(WALLC))
        cv.drawRRect(RRXY(o_.makeOutset(26, 26), 76, 76), dashed(shade(WALLC, 1.5), 4, 170, (16, 12)))
        for sd, xx in ((1, o_.left()), (-1, o_.right())):
            cv.save(); cv.clipRRect(RRXY(o_, 56, 56), True)
            poly(cv, [(xx, o_.top()), (xx + sd * 210, o_.top()), (xx + sd * 70, o_.top() + 420), (xx, o_.top() + 500)], shade(WAINS, 1.12), 245)
            cv.drawLine(xx + sd * 200, o_.top() + 6, xx + sd * 66, o_.top() + 414, dashed(shade(WAINS, 1.6), 4, 190, (14, 10))); cv.restore()
        cv.drawRRect(RRXY(o_, 56, 56), stroke(BRASS, 18)); cv.drawRRect(RRXY(o_.makeInset(9, 9), 48, 48), stroke(shade(BRASS, 0.7), 3))
        cv.drawRect(LTRB(-700, o_.bottom() + 60, 1800, 2600), fill(WAINS)); cv.drawLine(-700, o_.bottom() + 74, 1800, o_.bottom() + 74, dashed(shade(WAINS, 1.5), 4, 190, (18, 14)))
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kSoftLight); p.setAlphaf(0.4); cv.drawImage(noise_img(), 0, 0, LIN, p)


def win_lakes(cv, ts, k, near=0.0):
    """vagon pencerelerinin ardi: goller (kucuk) ve yaklasan istasyon lambalari. near 0..1"""
    night(cv, SC(ts), k, y_h=900, moon=None, poles=False)
    cv.drawRect(LTRB(-700, 900, 1800, 1300), fill((14, 24, 46)))
    off = (SC(ts) * 0.10) % 520
    for i in range(7):
        cx = -560 + i * 520 - off + (i % 2) * 130; y = 918 + (i % 3) * 16; rx = 120 + (i % 3) * 40
        p = skia.Paint(AntiAlias=True); p.setShader(skia.GradientShader.MakeLinear([skia.Point(0, y - 12), skia.Point(0, y + 12)], [col((44, 78, 140)), col((22, 40, 92))]))
        cv.drawOval(LTRB(cx - rx, y - 11, cx + rx, y + 11), p); cv.drawOval(LTRB(cx - 22, y - 5, cx + 22, y + 5), fill((244, 232, 184)))
    if near > 0:
        bx = lerp(1700, 620, near)
        for j in range(6):
            lx_ = bx + j * 64
            gl = fill((255, 226, 150), 150); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10)); cv.drawCircle(lx_, 842, 13, gl)
            cv.drawCircle(lx_, 842, 5, fill((255, 240, 200))); cv.drawLine(lx_, 846, lx_, 900, stroke((14, 18, 30), 3, cap=False))
        cv.drawRect(LTRB(bx - 20, 892, bx + 400, 904), fill((60, 62, 80)))


# ---------- orgu (cok yakin) ----------
KNAMES = ('YEDİGÖL', 'DEĞİRMEN', 'KARAKÖPRÜ')              # ustten alta (en yeni ustte, sisin ucunda)
FW, FH, BH = 800, 588, 196
def _fabric(c):
    rc = LTRB(20, 40, 20 + FW, 40 + FH + 34)
    c.drawRRect(RRXY(rc, 20, 20), fill(CREAM))
    for j, nm in enumerate(KNAMES):
        y0 = 40 + j * BH
        if j: c.drawLine(34, y0, 6 + FW, y0, dashed(CORAL, 5, 230, (16, 12)))
        f = skia.Font(TFB, 104); f.setEmbolden(True); w = f.measureText(nm)
        if w > FW - 110: f.setSize(104 * (FW - 110) / w); w = f.measureText(nm)
        c.drawString(nm, 20 + FW / 2 - w / 2 + 3, y0 + BH * 0.5 + f.getSize() * 0.36 + 4, f, fill(shade(CORAL, 0.62), 150))
        c.drawString(nm, 20 + FW / 2 - w / 2, y0 + BH * 0.5 + f.getSize() * 0.36, f, fill(CORAL))
    c.drawLine(34, 40 + FH, 6 + FW, 40 + FH, dashed(CORAL, 5, 230, (16, 12)))
    c.save(); c.clipRRect(RRXY(rc, 20, 20), True)
    vs = stroke(shade(CREAM, 0.74), 2.6, 96)
    for r in range(int((FH + 34) / 20) + 1):                 # orgu ilmekleri: 'v' dizileri
        y = 46 + r * 20
        for q in range(int(FW / 22) + 1):
            x = 24 + q * 22; c.drawLine(x, y, x + 9, y + 14, vs); c.drawLine(x + 18, y, x + 9, y + 14, vs)
    for q in range(int(FW / 16) + 1):                        # alt kenar: lastik orgu
        c.drawLine(24 + q * 16, 40 + FH + 4, 24 + q * 16, 40 + FH + 30, stroke(shade(CREAM, 0.7), 4, 150))
    c.restore()
    c.drawRRect(RRXY(rc, 20, 20), stroke(shade(CREAM, 0.66), 4))


def knit_macro(cv, ts, k, hi=(0, 0, 0), ghost=(0, 0), dy=0.0, sc_=1.0):
    """Ada'nin orgusu cok yakindan (sahne koordinati): uc sira, her sirada bir istasyon adi. hi: (Karakopru, Degirmen, Yedigol) parlama 0..1.
    ghost: (Sarnic, Son Durak) orulmemis siralarin hayali 0..1"""
    with zoom(cv, 2.3, (JX - CAMJ, 1000), (540, 1000)):
        wagon(cv, CAMJ, 3, k, scroll=SC(ts), last=True, plate_hi=1.0)
    dim(cv, 0.62)
    x0 = 540 - FW / 2; y0 = (470 if V else 610) + dy; sway = 3 * math.sin(k * 0.25)
    with stage(cv):
        cv.save(); cv.translate(sway + 540, y0); cv.scale(sc_, sc_); cv.translate(-540, -y0)
        if any(ghost):                                       # orulmemis siralar: kesik cizgili bos bantlar
            for j, (nm, a) in enumerate(zip(('SON DURAK', 'SARNIÇ'), (ghost[1], ghost[0]))):
                if a <= 0: continue
                gy_ = y0 - 300 + j * 140; rc = LTRB(x0 + 20, gy_, x0 + FW - 20, gy_ + 122)
                cv.drawRRect(RRXY(rc, 16, 16), dashed(CREAM, 4, 170 * a, (16, 12)))
                text(cv, nm, 540 - 40, gy_ + 86, 72, CREAM, a=110 * a)
                text(cv, '?', x0 + FW - 96, gy_ + 90, 84, RED, a=255 * a * (1.0 if (k // 3) % 2 else 0.6))
        for sd in (-1, 1):                                   # Ada'nin elleri ve sisler
            hx_, hy_ = 540 + sd * (FW / 2 + 36), y0 - 4 + alt(k, 0, 5, 4) * sd
            yarn_limb(cv, [(hx_ + sd * 330, y0 + 500), (hx_ + sd * 170, y0 + 190), (hx_ + sd * 10, hy_ + 30)], 110, ROSE)
        cv.drawLine(x0 - 150, y0 - 14, x0 + FW + 120, y0 - 2, stroke((70, 64, 84), 20)); cv.drawLine(x0 - 150, y0 - 14, x0 + FW + 120, y0 - 2, stroke((150, 142, 166), 13))
        cv.drawCircle(x0 - 156, y0 - 14, 20, fill((150, 142, 166)))
        blit(cv, sprite(('fabric', FMT), FW + 40, FH + 120, _fabric), x0 - 20, y0 - 40)
        for q_ in range(int(FW / 34)):                       # sisteki ilmekler
            cv.drawOval(LTRB(x0 + 8 + q_ * 34, y0 - 24, x0 + 34 + q_ * 34, y0 + 12), stroke(shade(CREAM, 0.9), 7)); cv.drawOval(LTRB(x0 + 8 + q_ * 34, y0 - 24, x0 + 34 + q_ * 34, y0 + 12), stroke(CREAM, 4))
        for j, nm in enumerate(KNAMES):
            a = hi[2 - j]
            if a > 0:
                f = skia.Font(TFB, 104); f.setEmbolden(True); w = f.measureText(nm)
                if w > FW - 110: f.setSize(104 * (FW - 110) / w); w = f.measureText(nm)
                yy = y0 + j * BH + BH * 0.5 + f.getSize() * 0.36
                gl = fill((255, 214, 80), 120 * a); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26)); cv.drawRect(LTRB(540 - w / 2 - 20, yy - f.getSize() * 0.86, 540 + w / 2 + 20, yy + 16), gl)
                cv.drawString(nm, 540 - w / 2, yy, f, fill((150, 30, 40), 255 * a))
        for sd in (-1, 1): hand_ball(cv, 540 + sd * (FW / 2 + 36), y0 - 4 + alt(k, 0, 5, 4) * sd, 64, ROSE, seed=5 + sd)
        yarn_strand(cv, [(x0 + FW - 30, y0 + 6), (x0 + FW + 70, y0 + 150), (x0 + FW + 40, y0 + 420), (x0 + FW + 150, y0 + 760)], 9)
        cv.restore()


# ---------- iki numaranin arka kapisi: caminin ardinda uc numara ve Ada ----------
GLS = LTRB(D0 + 56, DT + 50, D1 - 56, 1010)
def door_shot(cv, ts, k, z=1.0, p=(540, 1000), q=(540, 1000), lamp=1.0, gone=False, fog_a=0.0, sc=0.0, ada=None, mia=None, shake=(0, 0), mute=0.0, hand=None):
    """z, p, q: yakinlasma (p sahne noktasi q'ya oturur). lamp 0..1: uc numaranin isigi. gone: vagon yok (bos ray). ada: (ifade, poz, bakis[, ek]).
    mia: (x, ifade, poz, bakis). mute 0..1: 'duyulmuyor' balonu. hand: Mia'nin camdaki eli (x, y) cam koordinatinda"""
    def glass(c, g_, k_):
        if gone: rear_view(c, g_, 1.0, 0.0, sc, k_)
        else: fwd_glass(c, g_, k_)
    with zoom(cv, z, p, q): door_view(cv, k, plate_hi=1.0, no=3, glass=glass, shake=shake)
    Z = lambda x, y: (q[0] + z * (x - p[0]) + shake[0], q[1] + z * (y - p[1]) + shake[1])
    with stage(cv):
        l_, t_ = Z(GLS.left() + 6, GLS.top() + 6); r_, b_ = Z(GLS.right() - 6, GLS.bottom() - 6)
        cv.save(); cv.clipRRect(RRXY(LTRB(l_, t_, r_, b_), 16 * z, 16 * z), True)
        if not gone:
            if ada:
                ax, ay = Z(540, 1112); kw = dict(ada[3]) if len(ada) > 3 else {}
                actor(cv, ts, 'D', ada[0], ada[1], ada[2], place=(ax, ay, 0.36 * z), **kw)
            if lamp < 1: cv.drawRect(LTRB(l_, t_, r_, b_), fill((5, 7, 20), 238 * (1 - lamp)))
        if fog_a > 0:
            cv.drawRect(LTRB(l_, t_, r_, b_), fill((178, 190, 214), 225 * clamp(fog_a)))
            for i in range(5):
                pf = fill((226, 232, 244), 120 * clamp(fog_a)); pf.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 26 * z))
                cv.drawCircle(l_ + ((i * 97 + k * 3) % int(r_ - l_ + 120)) - 60, t_ + 60 * z + (i * 71 * z) % int(b_ - t_ - 60 * z), 70 * z, pf)
        cv.drawLine(l_ + 30 * z, t_ + 84 * z, l_ + 90 * z, t_ + 24 * z, stroke((255, 255, 255), 7 * z, 40))
        cv.restore()
        if hand:                                             # Mia'nin camdaki eli (kolu kadrajin altindan gelir)
            hx_, hy_ = Z(*hand)
            yarn_limb(cv, [(hx_ - 170 * z, hy_ + 520 * z), (hx_ - 70 * z, hy_ + 220 * z), (hx_ - 6 * z, hy_ + 26 * z)], 62 * z, MUSTARD); hand_ball(cv, hx_, hy_, 33 * z, MUSTARD)
        if mute > 0:                                         # balon: ses duyulmuyor
            bx, by = Z(GLS.right() + 96, GLS.top() + 60); r = 62 * z ** 0.5
            cv.drawOval(LTRB(bx - r * 1.5, by - r, bx + r * 1.5, by + r), fill(CREAM, 245 * mute)); poly(cv, [(bx - r * 1.2, by + r * 0.2), (bx - r * 2.0, by + r * 1.1), (bx - r * 0.5, by + r * 0.8)], CREAM, 245 * mute)
            for j in range(3): cv.drawCircle(bx + (j - 1) * r * 0.62, by, r * (0.2 if (k // 3) % 3 == j else 0.13), fill(INKBLUE, 255 * mute))
            cv.drawLine(bx - r * 1.2, by + r * 0.9, bx + r * 1.2, by - r * 0.9, stroke(RED, 9, 255 * mute))
        if mia:
            mx, my = Z(mia[0], NEAR)
            actor(cv, ts, 'M', mia[1], mia[2], mia[3], place=(mx, my, 0.70 * z), back=True)


def hold_knit(cv, f, u=1.3):
    """elde, yuzun yaninda tutulan yarim orgu: sis, krem parca, mercan siralar, sarkan ip"""
    (hx, hy), s = f['handR'], f['s'] * u
    yarn_strand(cv, [(hx + 40 * s, hy + 40 * s), (hx + 96 * s, hy + 150 * s), (hx + 70 * s, hy + 250 * s)], 5 * s)
    poly(cv, [(hx - 62 * s, hy + 2 * s), (hx + 66 * s, hy - 8 * s), (hx + 60 * s, hy + 128 * s), (hx - 56 * s, hy + 138 * s)], (4, 6, 20), 70)
    poly(cv, [(hx - 66 * s, hy - 4 * s), (hx + 62 * s, hy - 14 * s), (hx + 56 * s, hy + 122 * s), (hx - 60 * s, hy + 132 * s)], CREAM)
    for j in range(1, 5): cv.drawLine(hx - 58 * s, hy - 4 * s + j * 26 * s, hx + 54 * s, hy - 13 * s + j * 26 * s, dashed(CORAL, 4.5 * s, 230, (10 * s, 8 * s)))
    cv.drawLine(hx - 96 * s, hy + 2 * s, hx + 100 * s, hy - 22 * s, stroke((70, 64, 84), 9 * s)); cv.drawLine(hx - 96 * s, hy + 2 * s, hx + 100 * s, hy - 22 * s, stroke((150, 142, 166), 5.5 * s))
    cv.drawCircle(hx - 98 * s, hy + 2 * s, 8 * s, fill((150, 142, 166)))
    hand_ball(cv, hx, hy, 33 * f['s'], MUSTARD, seed=4)


# ============ SAHNE 1: kanca. SIMDI: iki numara, Mia tek basina, elinde yarim orgu ============
CAM1, XM1 = -180, 400
def scene1(cv, t):
    ts, k = step(t), kk(t)
    turn = smooth(seg(ts, 0.0, 0.35))
    M_ = ('bagir' if on(ts, 'm1', 0.0, 0.1) else 'uzgun', dict(HOLDK, lean=lerp(-10, 4, turn)), lerp(-2, 0, turn))
    with zoom(cv, 1.3, (540, 960), (540, 1000) if V else (540, 1010)):
        wagon(cv, CAM1, 2, k, scroll=SC(ts), last=True)
        with stage(cv): hold_knit(cv, people(cv, ts, {'M': (XM1 - CAM1, NEAR, 0.70)}, {'M': M_})['M'])
    flash(cv, 0.8 * seg(t, HK - 0.12, HK))


# ============ SAHNE 2: disaridan: iki vagon; uc ve dort numaranin yeri bos ============
def ext2(cv, ts, k, xr, fade=1.0, ghost=1.0, sc=None, a_r=0.0, a_d=0.0):
    u, y = (1.25, 1130) if V else (1.5, 1150)
    with stage(cv):
        ext_bg(cv, SC(ts) if sc is None else sc, k, y=y + 21 * u - 22, moon=(800, 520) if V else (1180, 620), fog_a=0.6)
        mid = train_ext(cv, xr, y, u, 3, k, fade=fade, heads={2: [None, None, MUSTARD, None, None], 3: [None, None, None, ROSE, None]})
        yb = y - 170 * u
        for i, (c_, a) in ((3, (ROSE, a_d)), (4, (GREENC, a_r))):                       # kaybolan vagonlarin hayali ve yolcusu
            gx = mid[3] - (i - 3) * PITCH * u
            if ghost > 0 and (i == 4 or fade > 0.5):
                cv.drawRRect(RRXY(LTRB(gx - 82 * u, y - 96 * u, gx + 83 * u, y), 8 * u, 8 * u), dashed(CREAM, 4, 150 * ghost, (14, 10)))
                text(cv, str(i), gx, y - 34 * u, 44 * u, CREAM, a=130 * ghost)
            if a > 0:
                hand_ball(cv, gx, yb + 14 * (1 - a), 36, c_, seed=3 + i)
                for sd in (-1, 1): cv.drawLine(gx - 34, yb - sd * 34, gx + 34, yb + sd * 34, stroke(RED, 9, 255 * a))
        return mid, yb


def scene2(cv, t):
    ts, k = step(t), kk(t)
    a0 = TL.span(2)[0]
    xr = (1210 if V else 1300) + 22 * (ts - a0)
    mid, yb = ext2(cv, ts, k, xr, a_r=seg(ts, frac('n1', 0.22), frac('n1', 0.22) + 0.15), a_d=seg(ts, frac('n1', 0.84), frac('n1', 0.84) + 0.15))
    with stage(cv):
        for i in (1, 2):
            a = seg(ts, frac('n1', 0.5 + 0.08 * (2 - i)), frac('n1', 0.5 + 0.08 * (2 - i)) + 0.12)
            if a > 0: badge_at(cv, mid[i], yb + 14 * (1 - a), str(i), a=a, r=40)
    flash(cv, 0.8 * (1 - seg(t, HK, HK + 0.2)))


# ============ SAHNE 3: SIMDI: iki numara (genis); sonra elindeki orgu; baslik ============
CAM3, XM3 = 760, 1300
def scene3(cv, t):
    ts, k = step(t), kk(t)
    close = ts >= S('m3') - 0.15
    if close: M_ = ('uzgun', dict(HOLDK, lean=alt(k, 0, 3, 5)), 0 if ts < frac('m3', 0.5) else 1.6)
    else: M_ = ('yorgun', dict(KNIT), -1.8 if (k // 12) % 2 == 0 else 1.6, dict(prop='knit'))
    zz = (1.5 if V else 1.55, (540, 960), (540, 1000) if V else (540, 1010)) if close else (0.92 if V else 1.0, (540, 1000), QW)
    with zoom(cv, *zz):
        wagon(cv, CAM3, 2, k, scroll=SC(ts), last=True)
        with stage(cv):
            f = people(cv, ts, {'M': (XM3 - CAM3, NEAR, 0.70)}, {'M': M_})['M']
            if close: hold_knit(cv, f)
    title_card(cv, t)


# ============ SAHNE 4: geri sarma: tren geri geri gider, uc numara sisten geri gelir ============
def scene4(cv, t):
    ts, k = step(t), kk(t)
    a0 = TL.span(4)[0]; rb = B('rw1'); t1 = frac('n2', 0.5)
    back = max(0.0, ts - t1); d = -620 * back ** 1.6 + 22 * min(ts - a0, t1 - a0)
    fade = 1 - smooth(seg(ts, rb[0] + 0.15, rb[1] - 0.2))
    xr = (1210 if V else 1300) + 150 + d * 0.35
    ext2(cv, ts, k, xr, fade=fade, ghost=1 - seg(ts, rb[0], rb[0] + 0.3), sc=SC(a0) + d, a_d=1 - seg(ts, rb[0], rb[0] + 0.3))


# ============ SAHNE 5: 2 DK ONCE: Yedigol peronu, tren durur ============
def scene5(cv, t):
    ts, k = step(t), kk(t)
    s0 = B('stop')[0]; u = seg(ts, s0, s0 + HALT); tx = -700 * (1 - u) ** 2
    sh = jit(k, 3) if s0 + HALT - 0.05 <= ts < s0 + HALT + 0.3 else (0, 0)
    cv.save(); cv.translate(sh[0] * K, 0)
    platform(cv, STN, tx, k, heads4=[None] * 5, heads5=[None, None, None, ROSE, MUSTARD], n_last=3, fog_a=0.5)
    with stage(cv):                                          # bankta yanan fener: istasyon bakimli
        bx, by = (800 if V else 1240), 1232 + 170
        gl = fill((255, 214, 130), 150); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30)); cv.drawCircle(bx - 84, by - 44, 62, gl)
        cv.drawRRect(RRXY(LTRB(bx - 106, by - 74, bx - 62, by - 6), 8, 8), fill((255, 226, 150))); cv.drawRRect(RRXY(LTRB(bx - 106, by - 74, bx - 62, by - 6), 8, 8), stroke((50, 44, 40), 6))
        cv.drawLine(bx - 84, by - 74, bx - 84, by - 6, stroke((50, 44, 40), 4)); hd = skia.Path(); hd.addArc(LTRB(bx - 100, by - 104, bx - 68, by - 66), 180, 180); cv.drawPath(hd, stroke((50, 44, 40), 5))
    cv.restore()


# ============ SAHNE 6: uc numaranin on kapisi (genis): Ada orguyu uzatir ============
CAM6, XM6, XA6 = 1790, 2510, 2250
def stn_out(cv, k, cam): station_bg(cv, STN, WINS[4] + WW / 2 - cam, k, bw=112, by=800)
def scene6(cv, t):
    ts, k = step(t), kk(t)
    xa = lerp(XA6 - 190, XA6, smooth(seg(ts, S('m4') - 0.4, E('m4'))))
    if xa < XA6: D_ = ('sakin', dict(walk(xa - (XA6 - 190), 0.64, 1, hold=True), **KNIT), 2, dict(prop='knit'))
    elif ts < S('d1') - 0.05: D_ = ('sakin', KNIT, 2, dict(prop='knit'))
    else: D_ = ('sakin', mixpose(KNIT, GIVE, seg(ts, S('d1'), S('d1') + 0.35)), 2, dict(prop='knit'))
    M_ = ('bagir' if on(ts, 'm4', 0.0, 0.1) else 'endise', dict(REACH_L, lean=alt(k, -8, -2, 3)) if ts < S('d1') - 0.1 else {}, -2)
    zz = (1.3, (610, 960), (540, 1000) if V else (540, 1010)) if ts >= S('d1') - 0.1 else (0.95 if V else 1.0, (600, 1000), QW)
    with zoom(cv, *zz):
        wagon(cv, CAM6, 3, k, scroll=SC(ts), last=True, plate_hi=1.0, door_f=1.0, out=lambda c: stn_out(c, k, CAM6))
        with stage(cv): people(cv, ts, {'M': (XM6 - CAM6, NEAR, 0.70), 'D': (xa - CAM6, NEAR, 0.64)}, {'M': M_, 'D': D_})


# ============ SAHNE 7: ikisi (yakin); orgu el degistirir; kapi aralarinda kapanir ============
def scene7(cv, t):
    ts, k = step(t), kk(t)
    sb = B('shut'); o = ts - sb[0]
    given = o >= 0.3
    xm = XM6 + 170 * smooth(seg(o, 0.3, 0.9)); am = 1 - seg(xm, XM6 + 70, XM6 + 160)
    if o < 0: M_ = ('bagir' if on(ts, 'm5', 0.0, 0.1) else 'endise', dict(PUSHB, lean=alt(k, -10, -4, 2)) if on(ts, 'm5', 0.0, 0.2) else {}, -2)
    elif not given: M_ = ('saskin', {}, -2)
    else: M_ = ('saskin', dict(walk(xm - XM6, 0.70, -1, hold=True, scared=True), **KNIT) if 0 < xm - XM6 < 170 else KNIT, -2, dict(prop='knit', alpha=am))
    if o < 0.1: D_ = ('sakin', GIVE, 2, dict(prop='knit'))
    elif not given: D_ = ('sakin', dict(aL=(-30, 110, 90, 140), aR=(110, 100, 210, 130), lean=14), 2, dict(prop='knit'))
    elif o < SHUT: D_ = ('sakin', dict(aR=(110, 90, 200, 90), lean=10), 2)
    else: D_ = ('sakin', {}, 2 if o < SHUT + 0.4 else 0)
    if o >= -0.05: zz = (1.1 if V else 1.05, (620, 1000), QW)
    elif on(ts, 'd2', 0.1, 0.3): zz = (1.6, (XA6 - CAM6 + 20, 950), (540, 1000) if V else (540, 1010))
    else: zz = (1.45, (620, 960), (540, 1000) if V else (540, 1010))
    with zoom(cv, *zz):
        wagon(cv, CAM6, 3, k, scroll=SC(ts), last=True, plate_hi=1.0, door_f=1 - smooth(seg(o, SHUT - 0.5, SHUT)), out=lambda c: stn_out(c, k, CAM6))
        with stage(cv):
            people(cv, ts, {'M': (xm - CAM6, NEAR, 0.70), 'D': (XA6 - CAM6, NEAR, 0.64)}, {'M': M_, 'D': D_})
            if o >= SHUT: sfx_text(cv, (FDOOR[0] + FDOOR[1]) / 2 - CAM6, 760, 'TAK', 70, a=1 - seg(o, SHUT + 0.3, SHUT + 0.7))


# ============ SAHNE 8: iki numaradan arka kapiya bakis: Mia kapida, Ada camin ardinda (sessiz) ============
def scene8(cv, t):
    ts, k = step(t), kk(t)
    sy = B('say'); o = ts - sy[0]
    u = smooth(seg(o, 0.0, 1.2)); z = lerp(1.0, 1.55, u)
    talking = 0.35 < o < 1.9
    ada = ('sakin', GLASSH, 0, dict(talk=(0.25 + 0.6 * ((k * 5) % 3) / 2) if talking else None))
    bang = on(ts, 'm6', 0.0, 0.2)
    mia = (262, 'panik', dict(aR=(110, 40, 176, -50 + (alt(k, 0, 40, 2) if bang else 0)), aL=(-40, 60, 60, -20), lean=10), 2)
    door_shot(cv, ts, k, z, (540, lerp(1000, 850, u)), (540, lerp(1000, 900 if V else 960, u)), ada=ada, mia=mia if u < 0.98 else None, mute=seg(o, 0.5, 0.75) * (1 - seg(o, 1.95, 2.15)))


# ============ SAHNE 9: cam (yakin): lambalar soner, sis, bos ray ============
ZG = 2.2 if V else 2.0
PG, QG = (540, 850), ((540, 900) if V else (540, 960))
def scene9(cv, t):
    ts, k = step(t), kk(t)
    ot = B('out'); o = ts - ot[0]
    n_off = sum(1 for x in OUT_OFF if o >= x)
    lamp = 1 - n_off / 3.0
    if n_off < 3 and any(0 <= o - x < 0.16 for x in OUT_OFF) and k % 2: lamp = min(1.0, lamp + 0.2)
    gone = o >= GONE
    fa = smooth(seg(o, 1.5, 2.1)) * (1 - smooth(seg(o, GONE + 0.15, GONE + 0.8)))
    if o < 0.1: ada = ('sakin', GLASSH, 0)
    else: ada = ('sakin', dict(aR=(100, 40, 130 + alt(k, -14, 14, 3), -70)), 0)
    sh = jit(k, 2.5) if GONE - 0.3 <= o < GONE + 0.3 else (0, 0)
    hy = 985 + 40 * smooth(seg(o, GONE, GONE + 0.7))
    door_shot(cv, ts, k, ZG, PG, QG, lamp=lamp, gone=gone, fog_a=fa, sc=240 * max(0.0, o - GONE) ** 1.4, ada=ada, shake=sh, hand=(430 + (alt(k, 0, 6, 2) if on(ts, 'm7', 0.0, 0.1) else 0), hy))


# ============ SAHNE 10: 5 DK ONCE: Ada katlanir koltukta orgu oruyor; Mia yalvarir ============
def scene10(cv, t):
    ts, k = step(t), kk(t)
    M_ = ('bagir' if on(ts, 'm8', 0.0, 0.1) else 'endise', dict(PULL, lean=alt(k, 8, 16, 3)) if on(ts, 'm8', 0.1, 0.3) else {}, 2)
    D_ = sit('sakin', -1.2 if on(ts, 'd3') and ts < frac('d3', 0.45) else 0, k=k)
    zz = (1.4, (JX - CAMJ - 30, 960), (540, 1000) if V else (540, 1010)) if ts >= S('d3') - 0.12 else (0.95 if V else 1.0, (500, 1000), QW)
    with zoom(cv, *zz): nook(cv, ts, k, {'M': (MIA_J, M_), 'D': (ADA_SIT, D_)}, out=lambda c: win_lakes(c, ts, k))


# ============ SAHNE 11: "burasi son vagon"; biletler: Ada'ninki Yedigol, Mia'ninki bos ============
def scene11(cv, t):
    ts, k = step(t), kk(t)
    tk = ts >= S('d4') - 0.1
    M_ = ('panik' if on(ts, 'm9', 0.0, 0.1) else 'endise', RANT if on(ts, 'm9', 0.0, 0.1) and ts < frac('m9', 0.5) else (BACKP if on(ts, 'm9', 0.0, 0.2) else {}), 2)
    D_ = sit('sakin', -1.4, dict(SHOWB) if tk else None, 'ticket' if tk else 'knit', k)
    with zoom(cv, 1.25 if V else 1.3, (430, 965), (540, 1010)):
        nook(cv, ts, k, {'M': ((MIA_J[0] + 40, NEAR, 0.70), M_), 'D': (ADA_SIT, D_)}, out=lambda c: win_lakes(c, ts, k))
    a1 = seg(ts, S('d4') + 0.05, S('d4') + 0.3); a2 = seg(ts, frac('d4', 0.66), frac('d4', 0.66) + 0.25)
    dim(cv, 0.4 * a1)
    if V: s1, s2 = (540, 400, 580), (540, 700, 580)
    else: s1, s2 = (640, 290, 560), (1280, 290, 560)
    ticket(cv, s1[0], s1[1], s1[2], ROSE, 'ADA', STN, a1, rot=-2)
    ticket(cv, s2[0], s2[1], s2[2], MUSTARD, 'MIA', None, a2, rot=2, hi=1.0, k=k)


# ============ SAHNE 12: Mia (yakin): "seni birakmam"; Ada (yakin): "herkesin duragi ayri" ============
def scene12(cv, t):
    ts, k = step(t), kk(t)
    onD = ts >= S('d5') - 0.12
    M_ = ('kararli' if not onD else 'endise', dict(CHEST, lean=alt(k, -3, 4, 3)) if not onD else {}, 2)
    late = ts >= frac('d5', 0.5)
    D_ = sit('sakin', -1.4 if not late else 0.6, k=k)
    px = (JX - CAMJ - 10) if onD else (MIA_J[0] + 30)
    with zoom(cv, 1.6 if V else 1.65, (px, 950), (540, 1000) if V else (540, 1010)):
        nook(cv, ts, k, {'M': (MIA_J, M_), 'D': (ADA_SIT, D_)}, out=lambda c: win_lakes(c, ts, k))


# ============ SAHNE 13: pencere: yedi gol, yedisinde de ay ============
def scene13(cv, t):
    ts, k = step(t), kk(t)
    cnt = 7 * seg(ts, frac('d6', 0.12), frac('d6', 0.46)) if ts >= frac('d6', 0.12) else 0
    lakes_view(cv, ts, k, cnt)
    if ts >= S('d6') - 0.3:                                  # Ada'nin gosteren eli
        u = smooth(seg(ts, S('d6') - 0.3, S('d6') + 0.1))
        with stage(cv):
            hx_, hy_ = (760, 1330 + 300 * (1 - u)) if V else (1120, 1300 + 300 * (1 - u))
            yarn_limb(cv, [(hx_ + 300, hy_ + 430), (hx_ + 160, hy_ + 210), (hx_ + 14, hy_ + 22)], 84, ROSE); hand_ball(cv, hx_, hy_, 48, ROSE)


# ============ SAHNE 14: genis: istasyonun lambalari yaklasir ============
def scene14(cv, t):
    ts, k = step(t), kk(t)
    a0, b0 = TL.span(14); near = seg(ts, a0, b0 + 1.0)
    M_ = ('endise', UPR if on(ts, 'm11', 0.0, 0.3) else {}, 1.6 if ts < S('d7') else 2)
    D_ = sit('sakin', -1.2 if on(ts, 'd7') and ts < frac('d7', 0.6) else 0, k=k)
    zz = (1.3, (JX - CAMJ - 60, 950), (540, 1000) if V else (540, 1010)) if ts >= S('d7') - 0.12 else (0.95 if V else 1.0, (500, 1000), QW)
    with zoom(cv, *zz): nook(cv, ts, k, {'M': (MIA_J, M_), 'D': (ADA_SIT, D_)}, out=lambda c: win_lakes(c, ts, k, near))


# ============ SAHNE 15: 10 DK ONCE: Mia orgudeki yaziyi fark eder ============
def scene15(cv, t):
    ts, k = step(t), kk(t)
    lean = smooth(seg(ts, S('m12') - 0.2, S('m12') + 0.3))
    M_ = ('merak' if ts < frac('m12', 0.3) else 'saskin', mixpose({}, dict(LEAN_IN, aR=(110, 110, 190, 170)), lean), 2)
    D_ = sit('sakin', -1.4 if ts >= S('d8') - 0.1 else 0, dict(KNITUP) if ts >= S('d8') - 0.1 else None, k=k)
    with zoom(cv, 1.3 if V else 1.35, (450, 965), (540, 1010)):
        nook(cv, ts, k, {'M': ((MIA_J[0] + 70, NEAR, 0.70), M_), 'D': (ADA_SIT, D_)})


# ============ SAHNE 16: orgu (cok yakin): Karakopru, Degirmen, Yedigol ============
def scene16(cv, t):
    ts, k = step(t), kk(t)
    kb = B('knit')[0]
    def pulse(t0): return clamp(1 - abs(ts - t0 - 0.3) / 0.55) if ts >= t0 else 0.0
    hi = [max(pulse(kb + NAMES_AT[j]), pulse(frac('m13', (0.0, 0.2, 0.4)[j]))) for j in range(3)]
    knit_macro(cv, ts, k, hi=hi)


# ============ SAHNE 17: Ada (yakin): "her istasyona bir sira" ============
def scene17(cv, t):
    ts, k = step(t), kk(t)
    D_ = sit('sakin', 0 if ts < frac('d9', 0.55) else -1.4, k=k)
    with zoom(cv, 1.6 if V else 1.65, (JX - CAMJ - 10, 950), (540, 1000) if V else (540, 1010)):
        nook(cv, ts, k, {'M': ((MIA_J[0] + 70, NEAR, 0.70), ('merak', LEAN_IN, 2)), 'D': (ADA_SIT, D_)})


# ============ SAHNE 18: orgunun ustu bos (Sarnic? Son Durak?); yumak bitmek uzere ============
def scene18(cv, t):
    ts, k = step(t), kk(t)
    if ts < S('d10') - 0.15:
        knit_macro(cv, ts, k, ghost=(seg(ts, S('m14'), S('m14') + 0.25), seg(ts, frac('m14', 0.36), frac('m14', 0.36) + 0.25)), dy=90 if V else 160, sc_=0.84)
        return
    with zoom(cv, 2.3, (JX - CAMJ, 1000), (540, 1000)): wagon(cv, CAMJ, 3, k, scroll=SC(ts), last=True, plate_hi=1.0)
    dim(cv, 0.6)
    with stage(cv):                                          # Ada'nin avucunda kuculmus yumak; kesik cember: yumagin ilk hali
        cx, cy = 540, 930 if V else 960; bob_ = alt(k, 0, 5, 5)
        yarn_limb(cv, [(cx + 470, cy + 620), (cx + 250, cy + 330), (cx + 20, cy + 150 + bob_)], 150, ROSE)
        hand_ball(cv, cx, cy + 110 + bob_, 150, ROSE, seed=6)
        cv.drawCircle(cx, cy - 60 + bob_, 170, dashed(CREAM, 5, 150, (18, 14)))
        yarn_strand(cv, [(cx - 30, cy - 80 + bob_), (cx - 190, cy - 250), (cx - 120, cy - 420), (cx - 330, cy - 640)], 9)
        hand_ball(cv, cx, cy - 46 + bob_, 58, CORAL, seed=9)


# ============ SAHNE 19: 15 DK ONCE: anons; levha: VAGON 3 kirmizi yanar ============
XA19 = 2140
def scene19(cv, t):
    ts, k = step(t), kk(t)
    lv = TL.talk('A', ts); ch = B('chime'); late = ts >= frac('a1', 0.56)
    sh = jit(k, 2.5) if ch[0] <= ts < ch[0] + 0.8 else (0, 0)
    spk = lv if lv is not None else (0.5 if ch[0] <= ts < ch[0] + 0.8 else None)
    if late:
        with zoom(cv, 2.6 if V else 2.3, (2500 - CAMJ, 612), (540, 800) if V else (540, 950)):
            wagon(cv, CAMJ, 3, k, scroll=SC(ts), last=True, spk=spk, plate_hi=1.0)
        return
    up = ts >= ch[0] + 0.3
    st = {'M': (MIA_J, ('merak' if up else 'yorgun', LOOKUP if up else {}, 2 if up else -1)),
          'D': ((XA19 - CAMJ, NEAR, 0.64), ('merak' if up else 'sakin', dict(KNIT, **LOOKUP) if up else KNIT, 2 if up else 0, dict(prop='knit')))}
    with zoom(cv, 1.0 if V else 1.05, ((660 if V else 560) + sh[0], 960 + sh[1]), (540, 1010)): nook(cv, ts, k, st, seat=0.0, plate_hi=0.0, spk=spk)


# ============ SAHNE 20: Ada biletine bakar: Yedigol; Mia one cagirir; Ada koltugu indirir, oturur ============
def scene20(cv, t):
    ts, k = step(t), kk(t)
    sb = B('sit'); o = ts - sb[0]
    xa = lerp(XA19, JX, smooth(seg(ts, S('d12') - 0.2, sb[0] + 0.5)))
    down = 1.0 if o >= SIT else 0.0
    if ts < S('m15') - 0.15: D_ = ('sakin', SHOWB, 1.2 if ts < frac('d11', 0.5) else 0, dict(prop='ticket'))
    elif ts < S('d12') - 0.2: D_ = ('sakin', KNIT, -1.4, dict(prop='knit'))
    elif xa < JX - 2: D_ = ('sakin', dict(walk(xa - XA19, 0.64, 1, hold=True), **KNIT), 0, dict(prop='knit'))
    elif o < SIT: D_ = ('sakin', dict(aL=(-110, 150, -150, 250), aR=(84, 110, 40, 180), lean=-8), -1.2)
    else: D_ = ('sakin', mixpose(KNIT, dict(SEATP, **KNIT), seg(o, SIT + 0.05, SIT + 0.5)), 0, dict(prop='knit'))
    gyd = lerp(NEAR, FAR, smooth(seg(ts, S('d12') - 0.2, sb[0] + 0.5)))
    if on(ts, 'm15', 0.0, 0.15): M_ = ('bagir', dict(FWD, lean=alt(k, 6, 14, 3)), 2)
    elif o > SIT: M_ = ('saskin', HIP, 2)
    else: M_ = ('endise', {}, 2)
    if ts < S('m15') - 0.15: zz = (1.3, (XA19 - CAMJ - 40, 960), (540, 1000) if V else (540, 1010))
    elif ts < S('d12') - 0.12: zz = (0.95 if V else 1.0, (540, 1000), QW)
    else: zz = (1.2, (500, 980), (540, 1010))
    with zoom(cv, *zz):
        def ex(f):
            if SIT <= o < SIT + 0.5: sfx_text(cv, JX - CAMJ + 130, 1090, 'TIK', 56, a=1 - seg(o, SIT + 0.25, SIT + 0.5))
        nook(cv, ts, k, {'M': (MIA_J, M_), 'D': ((xa - CAMJ, gyd, 0.64), D_)}, seat=down, extra=ex)
    a = seg(ts, S('d11') + 0.05, S('d11') + 0.3) * (1 - seg(ts, S('m15') - 0.4, S('m15') - 0.15))
    if V: ticket(cv, 540, 470, 620, ROSE, 'ADA', STN, a, rot=-3)
    else: ticket(cv, 480, 330, 540, ROSE, 'ADA', STN, a, rot=-3)


# ============ SAHNE 21: "hic korkmuyor musun?" ============
def scene21(cv, t):
    ts, k = step(t), kk(t)
    if on(ts, 'm18', 0.12, 0.3): M_ = ('bagir' if on(ts, 'm18', 0.0, 0.1) else 'endise', BACKP, 2); zz = (1.6 if V else 1.65, (MIA_J[0] + 20, 950), (540, 1000) if V else (540, 1010))
    elif on(ts, 'd13', 0.12, 0.3): M_ = ('endise', {}, 2); zz = (1.6 if V else 1.65, (JX - CAMJ - 10, 950), (540, 1000) if V else (540, 1010))
    else: M_ = ('endise', CHEST if on(ts, 'm16', 0.0, 0.2) else {}, 2); zz = (1.25 if V else 1.3, (430, 965), (540, 1010))
    if on(ts, 'd15', 0.0, 0.3): D_ = sit('sakin', -1.4, dict(CALM), None, k)
    else: D_ = sit('sakin', -1.2 if on(ts, 'd13') and ts > frac('d13', 0.5) else 0, k=k)
    with zoom(cv, *zz): nook(cv, ts, k, {'M': (MIA_J, M_), 'D': (ADA_SIT, D_)})


# ============ SAHNE 22: GECENIN BASI: bes numara, ilk anons (sepya) ============
CAM22 = 1400
P22 = dict(M=1560, R=1790, D=1990, E=2200)
def w5(cv, ts, k, st, **kw):
    wagon(cv, CAM22, 5, k, scroll=SC(ts), **kw)
    with stage(cv):
        briefcase(cv, seat_xy(2)[0] - CAM22, 1120 - 54, 0.9)
        people(cv, ts, pl(CAM22, **P22), st)


def scene22(cv, t):
    ts, k = step(t), kk(t)
    late = ts >= frac('a2', 0.52)
    ex = 'saskin' if late else 'merak'
    st = {'M': (ex, LOOKUP, 2), 'R': (ex, LOOKUP, 2), 'D': ('merak', dict(KNIT, **LOOKUP), 2, dict(prop='knit')), 'E': (ex if late else 'endise', dict(SHOW, **LOOKUP), 2, dict(prop='watch'))}
    with tint(cv, sepia_m(0.5)):
        with zoom(cv, 0.8 if V else 1.0, (560, 1000), QW): w5(cv, ts, k, st, spk=TL.talk('A', ts), plate_hi=1.0 if ts >= frac('a2', 0.8) else 0.0)


# ============ SAHNE 23: herkes korkar; Ada gulumser ============
def scene23(cv, t):
    ts, k = step(t), kk(t)
    a0 = TL.span(23)[0]; u = smooth(seg(ts, a0, a0 + 2.6))
    st = {'M': ('endise', {}, alt(k, 2, -1.5, 8)), 'R': ('panik', RANT, alt(k, 1.5, -1.5, 5)), 'E': ('panik', dict(SHOW, lean=alt(k, -4, 6, 3)), -1.5, dict(prop='watch')),
          'D': ('mutlu', dict(KNIT, lean=alt(k, 0, 3, 4)), 0, dict(prop='knit'))}
    with tint(cv, sepia_m(0.5)):
        with zoom(cv, lerp(1.15, 1.5, u), (P22['D'] - CAM22, 950), (540, 1000) if V else (540, 1010)): w5(cv, ts, k, st, plate_hi=1.0)


# ============ SAHNE 24: 23:58 kapinin ardi, bu kez sesli: "Birakir dedi kizim. Kaybolur demedi." ============
def scene24(cv, t):
    ts, k = step(t), kk(t)
    gb = B('gone'); o = ts - gb[0]
    n_off = sum(1 for x in G_OFF if o >= x); lamp = 1 - n_off / 2.0
    if n_off < 2 and any(0 <= o - x < 0.16 for x in G_OFF) and k % 2: lamp = min(1.0, lamp + 0.25)
    sp = on(ts, 'd14', 0.05, 0.25)
    ada = ('mutlu' if ts >= S('d14') - 0.3 else 'sakin', GLASSH if o < 0.15 else dict(aR=(100, 40, 130 + alt(k, -14, 14, 3), -70)), 0)
    door_shot(cv, ts, k, ZG, PG, QG, lamp=lamp, ada=ada, hand=(430, 985))


# ============ SAHNE 25: SIMDI: Mia ve yarim orgu ============
def scene25(cv, t):
    ts, k = step(t), kk(t)
    M_ = ('uzgun' if ts < frac('m17', 0.5) else 'merak', dict(HOLDK, lean=alt(k, 0, 3, 5)), 0 if ts < frac('m17', 0.5) else 1.6)
    with zoom(cv, 1.5 if V else 1.55, (570, 960), (540, 1000) if V else (540, 1010)):
        wagon(cv, CAM3, 2, k, scroll=SC(ts), last=True)
        with stage(cv): hold_knit(cv, people(cv, ts, {'M': (XM3 - CAM3, NEAR, 0.70)}, {'M': M_})['M'])


# ============ SAHNE 26: kapanis karti ============
def scene26(cv, t):
    ts, k = step(t), kk(t)
    a0 = END0
    u, y = (1.2, 1140) if V else (1.3, 1150)
    with stage(cv):
        ext_bg(cv, SC(ts), k, y=y + 21 * u - 22, moon=(840, 380) if V else (1300, 640), fog_a=0.7)
        train_ext(cv, (700 if V else 860) + 60 * (ts - a0), y, u, 2, k)
    dim(cv, 0.6)
    a = smooth(seg(ts, a0 + 0.5, a0 + 1.1))
    cx, cy, w = (W / 2, 900, 520) if V else (W / 2, 560, 400)
    gl = fill((255, 226, 150), 70 * a); gl.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 60)); cv.drawCircle(cx, cy, w * 0.5, gl)
    ticket(cv, cx, cy + 30 * (1 - a), w, ROSE, 'ADA', STN, a, rot=-4)
    c_ = seg(t, a0 + 0.3, a0 + 0.8)
    card(cv, [('Ada neden', 72, RED), ('kalmayı seçti?', 72, RED), ('Yorumlara yaz', 40, CREAM), ('Sıradaki: 4. Bölüm, Kondüktör', 36, (176, 190, 232))],
         c_, cy=470 if V else 215)


SINE = {2: dict(mood='gece'), 4: dict(mood='gece'), 5: dict(mood='soguk'), 9: dict(mood='soguk'), 11: dict(zmax=1.1), 13: dict(mood='gece'),
        16: dict(zmax=1.1), 18: dict(zmax=1.1), 20: dict(zmax=1.12), 22: dict(mood='sepya'), 23: dict(mood='sepya'), 26: dict(mood='gece')}

if __name__ == '__main__':
    DRAW = {i: globals()[f'scene{i}'] for i in range(1, 27)}
    run(DRAW, white=tuple((i, i + 1) for i in range(1, 26)), sine=SINE, hud=hud)
