"""Orgu (amigurumi) gorunumlu cizgi adam stil denemesi. Tek kare uretir."""
import math, random, os, sys
import skia

W, H = 1080, 1920
THREAD = (34, 28, 40)
CREAM = (246, 236, 214)
TEAL = (52, 176, 164)
CORAL = (238, 108, 84)
LILAC = (165, 140, 222)
MUSTARD = (233, 180, 70)
PINK = (244, 120, 140)

def _font(name, fallback):
    here = os.path.dirname(os.path.abspath(__file__))
    for d in (os.path.join(here, 'fonts'), '/usr/share/fonts/truetype/google-fonts', 'C:/Windows/Fonts',
              os.path.expandvars('%LOCALAPPDATA%/Microsoft/Windows/Fonts')):
        for n in (name, fallback):
            p = os.path.join(d, n)
            if os.path.exists(p): return skia.Typeface.MakeFromFile(p)
    return skia.Typeface('Arial', skia.FontStyle.Bold())


TFB = _font('Poppins-Bold.ttf', 'segoeuib.ttf')        # Poppins yoksa (Windows) Segoe UI
TFM = _font('Poppins-Medium.ttf', 'seguisb.ttf')

R = random.Random(11)


def col(c, a=255):
    return skia.Color(int(c[0]), int(c[1]), int(c[2]), int(a))


def shade(c, f):
    if f >= 1:
        return tuple(min(255, x + (255 - x) * (f - 1)) for x in c)
    return tuple(x * f for x in c)


def stroke(c, w, a=255, cap=True):
    p = skia.Paint(AntiAlias=True, Color=col(c, a))
    p.setStyle(skia.Paint.kStroke_Style)
    p.setStrokeWidth(w)
    if cap:
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def fill(c, a=255):
    return skia.Paint(AntiAlias=True, Color=col(c, a))


def qpath(pts):
    """smooth path through points"""
    p = skia.Path()
    p.moveTo(*pts[0])
    if len(pts) == 2:
        p.lineTo(*pts[1])
        return p
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        p.quadTo(pts[i][0], pts[i][1], mx, my)
    p.lineTo(*pts[-1])
    return p


# ---------- yarn primitives (v3: gercek tig isi gorunumu) ----------
# Her ilmek kucuk bir V'dir; ilmekler uzuv boyunca sira sira dizilir. Isik sol ustten gelir:
# her ilmegin tonu, silindir/kure yuzeyindeki yerine gore hesaplanir (ortasi acik, kenari koyu).
LDIR = (-0.50, -0.78)


def _flush(cv, buckets, c):
    for (lv, sw2), p in sorted(buckets.items()):
        cv.drawPath(p, stroke(shade(c, lv / 20.0), max(1.2, sw2 / 2.0)))


def _fuzz_line(cv, x0, y0, dx, dy, c):
    cv.drawLine(x0, y0, x0 + dx, y0 + dy, stroke(shade(c, 1.12), 1.1, 105))


def yarn_limb(cv, pts, width, c):
    """tig isi tup: yol boyunca V ilmek siralari, silindir golgelendirmesi, hafif tuy"""
    path = qpath(pts)
    cv.drawPath(path, stroke(shade(c, 0.56), width))
    cv.drawPath(path, stroke(shade(c, 0.74), width * 0.93))
    pm = skia.PathMeasure(path, False)
    L = pm.getLength()
    hw = width * 0.5
    dphi = math.pi / 5.0
    rs = hw * 0.52                      # sira araligi
    h = rs * 0.36
    buckets = {}
    d, i = rs * 0.2, 0
    while d < L - rs * 0.1:
        pos, tan = pm.getPosTan(d)
        tx, ty = tan.x(), tan.y(); nx, ny = -ty, tx
        nl = nx * LDIR[0] + ny * LDIR[1]
        off = 0.5 if i % 2 else 0.0
        for j in range(-3, 3):
            phi = (j + off + 0.25) * dphi
            if abs(phi) > 1.40: continue
            sp, cp = math.sin(phi), math.cos(phi)
            bb = hw * 0.86 * sp
            q = hw * 0.20 * cp + 0.3
            lv = 0.74 + 0.30 * cp + 0.26 * sp * nl
            x, y = pos.x() + nx * bb, pos.y() + ny * bb
            key = (int(round(lv * 20)), int(round(q * 2.6)))
            p = buckets.get(key)
            if p is None: p = buckets[key] = skia.Path()
            p.moveTo(x - nx * q - tx * h, y - ny * q - ty * h)
            p.lineTo(x + tx * h, y + ty * h)
            p.lineTo(x + nx * q - tx * h, y + ny * q - ty * h)
        d += rs; i += 1
    _flush(cv, buckets, c)
    for _ in range(int(L / 16)):
        dd = R.uniform(0, L)
        pos, tan = pm.getPosTan(dd)
        nx, ny = -tan.y(), tan.x()
        s = R.choice((-1, 1)); ln = R.uniform(1.5, 3.6) * (width / 46) ** 0.5; ax = R.uniform(-0.6, 0.6)
        _fuzz_line(cv, pos.x() + nx * s * hw * 0.97, pos.y() + ny * s * hw * 0.97, (nx * s + tan.x() * ax) * ln, (ny * s + tan.y() * ax) * ln, c)


def yarn_ball(cv, cx, cy, r, c, rows=None):
    """tig isi kure: yatay siralar halinde V ilmekler (tepeden asagi orulmus gibi)"""
    cv.drawCircle(cx, cy, r, fill(shade(c, 0.56)))
    cv.drawCircle(cx, cy, r * 0.975, fill(shade(c, 0.74)))
    circ = skia.Path(); circ.addCircle(cx, cy, r * 0.985)
    cv.save(); cv.clipPath(circ, True)
    rows = rows or 17
    dth = math.pi / rows
    R0 = r * 0.975
    buckets = {}
    for k in range(rows):
        th = -math.pi / 2 + (k + 0.5) * dth
        st, ct = math.sin(th), math.cos(th)
        y = cy + R0 * st; rr = R0 * ct
        h = max(0.6, R0 * dth * 0.20 * (0.35 + 0.65 * ct))
        n = max(2, int(round(math.pi * rr / (R0 * dth))))
        dphi = math.pi / n
        for j in range(n + 1):
            phi = -math.pi / 2 + (j + (0.0 if k % 2 else 0.5)) * dphi
            if abs(phi) > 1.46: continue
            sp, cp = math.sin(phi), math.cos(phi)
            x = cx + rr * sp
            q = rr * dphi * 0.5 * cp * 0.62 + 0.3
            lv = 0.72 + 0.32 * ct * cp + 0.28 * (ct * sp * LDIR[0] + st * LDIR[1])
            key = (int(round(lv * 20)), int(round(q * 2.6)))
            p = buckets.get(key)
            if p is None: p = buckets[key] = skia.Path()
            p.moveTo(x - q, y - h); p.lineTo(x, y + h); p.lineTo(x + q, y - h)
    _flush(cv, buckets, c)
    cv.restore()
    for _ in range(int(r * 0.35)):
        a = R.uniform(0, 2 * math.pi)
        ln = R.uniform(1.5, 4.0) * (r / 110) ** 0.5
        tw = R.uniform(-0.5, 0.5)
        _fuzz_line(cv, cx + math.cos(a) * r * 0.99, cy + math.sin(a) * r * 0.99, math.cos(a + tw) * ln, math.sin(a + tw) * ln, c)


# ---------- embroidered face ----------
def thread(cv, path, w, c=THREAD):
    cv.drawPath(path, stroke(c, w))
    hl = stroke((255, 255, 255), max(1.0, w * 0.22), 55)
    hl.setPathEffect(skia.DashPathEffect.Make([w * 0.9, w * 1.1], 0))
    cv.drawPath(path, hl)


def blush(cv, x, y, r):
    p = fill(PINK, 150)
    p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r * 0.28))
    cv.drawOval(skia.Rect.MakeLTRB(x - r, y - r * 0.6, x + r, y + r * 0.6), p)


def eye_line(cv, x, y, s):
    cv.drawOval(skia.Rect.MakeLTRB(x - 10 * s, y - 17 * s, x + 10 * s, y + 17 * s), fill(THREAD))
    cv.drawCircle(x - 3 * s, y - 8 * s, 3.6 * s, fill((255, 255, 255), 220))


def teeth_mouth(cv, cx, cy, w, h, s, closed=False):
    m = skia.Path()
    m.moveTo(cx - w, cy)
    m.quadTo(cx, cy - h * 0.25, cx + w, cy)
    m.quadTo(cx + w * 0.75, cy + h, cx, cy + h)
    m.quadTo(cx - w * 0.75, cy + h, cx - w, cy)
    m.close()
    cv.drawPath(m, fill(THREAD if not closed else (250, 248, 240)))
    cv.save(); cv.clipPath(m, True)
    if closed:
        for k in range(-3, 4):
            cv.drawLine(cx + k * w / 3.2, cy - h, cx + k * w / 3.2, cy + h * 2, stroke(THREAD, 4 * s))
        cv.drawLine(cx - w, cy + h * 0.45, cx + w, cy + h * 0.45, stroke(THREAD, 4 * s))
    else:
        cv.drawRect(skia.Rect.MakeLTRB(cx - w, cy - h, cx + w, cy + h * 0.34), fill((250, 248, 240)))
        for k in (-1, 0, 1):
            cv.drawLine(cx + k * w * 0.42, cy - h, cx + k * w * 0.42, cy + h * 0.34, stroke(THREAD, 3 * s, 120))
        t = fill((236, 96, 110))
        cv.drawOval(skia.Rect.MakeLTRB(cx - w * 0.45, cy + h * 0.62, cx + w * 0.45, cy + h * 1.5), t)
    cv.restore()
    cv.drawPath(m, stroke(THREAD, 6 * s))


def face(cv, cx, cy, r, expr):
    s = r / 110.0
    ex, ey = 34 * s, -12 * s
    lx, rx, y = cx - ex, cx + ex, cy + ey
    my = cy + 40 * s
    if expr == 'mutlu':
        eye_line(cv, lx, y, s); eye_line(cv, rx, y, s)
        blush(cv, cx - 62 * s, cy + 22 * s, 20 * s); blush(cv, cx + 62 * s, cy + 22 * s, 20 * s)
        p = skia.Path(); p.moveTo(cx - 30 * s, my - 6 * s); p.quadTo(cx, my + 24 * s, cx + 30 * s, my - 6 * s)
        thread(cv, p, 9 * s)
    elif expr == 'kahkaha':
        for x in (lx, rx):
            p = skia.Path(); p.moveTo(x - 17 * s, y + 8 * s); p.quadTo(x, y - 20 * s, x + 17 * s, y + 8 * s)
            thread(cv, p, 10 * s)
        blush(cv, cx - 66 * s, cy + 18 * s, 22 * s); blush(cv, cx + 66 * s, cy + 18 * s, 22 * s)
        teeth_mouth(cv, cx, my - 12 * s, 44 * s, 46 * s, s)
    elif expr == 'endişeli':
        for x, d in ((lx, 1), (rx, -1)):
            cv.drawCircle(x, y + 4 * s, 9 * s, fill(THREAD))
            b = skia.Path(); b.moveTo(x - 18 * s * d, y - 22 * s); b.lineTo(x + 16 * s * d, y - 36 * s)
            thread(cv, b, 8 * s)
        p = skia.Path(); p.moveTo(cx - 34 * s, my + 4 * s)
        p.quadTo(cx - 22 * s, my - 12 * s, cx - 11 * s, my + 4 * s)
        p.quadTo(cx, my + 18 * s, cx + 11 * s, my + 4 * s)
        p.quadTo(cx + 22 * s, my - 12 * s, cx + 34 * s, my + 4 * s)
        thread(cv, p, 8 * s)
        d = skia.Path(); dx, dy = cx + 78 * s, cy - 48 * s
        d.moveTo(dx, dy - 20 * s); d.quadTo(dx + 15 * s, dy + 6 * s, dx, dy + 12 * s); d.quadTo(dx - 15 * s, dy + 6 * s, dx, dy - 20 * s)
        cv.drawPath(d, fill((150, 215, 245))); cv.drawPath(d, stroke(THREAD, 3.5 * s))
    elif expr == 'kızgın':
        for x, d in ((lx, 1), (rx, -1)):
            cv.drawOval(skia.Rect.MakeLTRB(x - 8 * s, y - 6 * s, x + 8 * s, y + 14 * s), fill(THREAD))
            b = skia.Path(); b.moveTo(x - 22 * s * d, y - 34 * s); b.lineTo(x + 20 * s * d, y - 12 * s)
            thread(cv, b, 10 * s)
        blush(cv, cx - 60 * s, cy + 24 * s, 24 * s); blush(cv, cx + 60 * s, cy + 24 * s, 24 * s)
        teeth_mouth(cv, cx, my - 4 * s, 34 * s, 26 * s, s, closed=True)
    elif expr == 'şaşkın':
        for x in (lx, rx):
            cv.drawCircle(x, y, 22 * s, fill((250, 248, 240)))
            cv.drawCircle(x, y, 22 * s, stroke(THREAD, 6 * s))
            cv.drawCircle(x, y + 1 * s, 8 * s, fill(THREAD))
        cv.drawOval(skia.Rect.MakeLTRB(cx - 15 * s, my - 4 * s, cx + 15 * s, my + 34 * s), fill(THREAD))
        cv.drawOval(skia.Rect.MakeLTRB(cx - 8 * s, my + 14 * s, cx + 8 * s, my + 32 * s), fill((236, 96, 110)))
    elif expr == 'kurnaz':
        for x in (lx, rx):
            p = skia.Path(); p.moveTo(x - 17 * s, y); p.lineTo(x + 17 * s, y)
            thread(cv, p, 10 * s)
            cv.drawCircle(x + 6 * s, y + 9 * s, 6 * s, fill(THREAD))
        b = skia.Path(); b.moveTo(rx - 18 * s, y - 30 * s); b.lineTo(rx + 20 * s, y - 38 * s)
        thread(cv, b, 8 * s)
        p = skia.Path(); p.moveTo(cx - 22 * s, my + 6 * s); p.quadTo(cx + 10 * s, my + 16 * s, cx + 38 * s, my - 14 * s)
        thread(cv, p, 9 * s)


# ---------- figure ----------
def figure(cv, x, gy, s, c, expr, pose='stand', scarf=None, antenna=None):
    HR = 118 * s
    lw = 46 * s
    hip = (x, gy - 250 * s)
    neck = (x, gy - 520 * s)
    hc = (x, neck[1] - HR * 0.88)
    layer = skia.Paint()
    layer.setImageFilter(skia.ImageFilters.DropShadow(10 * s + 4, 16 * s + 6, 12, 12, skia.Color(4, 6, 20, 130)))
    cv.saveLayer(None, layer)
    if pose == 'wave':
        armL = [(x - 6 * s, neck[1] + 40 * s), (x - 110 * s, neck[1] + 150 * s), (x - 90 * s, neck[1] + 290 * s)]
        armR = [(x + 6 * s, neck[1] + 40 * s), (x + 130 * s, neck[1] + 30 * s), (x + 190 * s, neck[1] - 130 * s)]
    elif pose == 'hips':
        armL = [(x - 6 * s, neck[1] + 40 * s), (x - 150 * s, neck[1] + 150 * s), (x - 30 * s, hip[1] - 20 * s)]
        armR = [(x + 6 * s, neck[1] + 40 * s), (x + 150 * s, neck[1] + 150 * s), (x + 30 * s, hip[1] - 20 * s)]
    else:
        armL = [(x - 6 * s, neck[1] + 40 * s), (x - 100 * s, neck[1] + 170 * s), (x - 120 * s, neck[1] + 300 * s)]
        armR = [(x + 6 * s, neck[1] + 40 * s), (x + 100 * s, neck[1] + 170 * s), (x + 120 * s, neck[1] + 300 * s)]
    legL = [hip, (x - 70 * s, gy - 130 * s), (x - 84 * s, gy - 18 * s)]
    legR = [hip, (x + 70 * s, gy - 130 * s), (x + 84 * s, gy - 18 * s)]
    yarn_limb(cv, [(x, neck[1] - 10 * s), (x, hip[1] - 4 * s)], lw * 1.12, c)
    yarn_limb(cv, legL, lw, c); yarn_limb(cv, legR, lw, c)
    yarn_ball(cv, legL[-1][0] - 14 * s, gy - 16 * s, 30 * s, shade(c, 0.9), rows=5)
    yarn_ball(cv, legR[-1][0] + 14 * s, gy - 16 * s, 30 * s, shade(c, 0.9), rows=5)
    yarn_limb(cv, armL, lw * 0.9, c)
    yarn_limb(cv, armR, lw * 0.9, c)
    yarn_ball(cv, armL[-1][0], armL[-1][1], 27 * s, shade(c, 1.08), rows=5)
    yarn_ball(cv, armR[-1][0], armR[-1][1], 27 * s, shade(c, 1.08), rows=5)
    if antenna:
        ax, ay = hc[0] + 20 * s, hc[1] - HR * 0.9
        yarn_limb(cv, [(ax, ay), (ax + 26 * s, ay - 70 * s), (ax + 70 * s, ay - 96 * s)], 16 * s, shade(c, 0.85))
        yarn_ball(cv, ax + 74 * s, ay - 98 * s, 24 * s, antenna, rows=5)
    yarn_ball(cv, hc[0], hc[1], HR, c)
    if scarf:
        yarn_limb(cv, [(x - 62 * s, neck[1] + 6 * s), (x, neck[1] + 34 * s), (x + 62 * s, neck[1] + 6 * s)], 40 * s, scarf)
        yarn_limb(cv, [(x + 40 * s, neck[1] + 26 * s), (x + 66 * s, neck[1] + 110 * s), (x + 52 * s, neck[1] + 170 * s)], 34 * s, scarf)
    face(cv, hc[0], hc[1] + 6 * s, HR, expr)
    cv.restore()
    return hc


def star(cv, x, y, r, c=CREAM, rot=0):
    p = skia.Path()
    for i in range(8):
        a = math.radians(rot + i * 45)
        rr = r if i % 2 == 0 else r * 0.38
        px, py = x + rr * math.sin(a), y - rr * math.cos(a)
        p.moveTo(px, py) if i == 0 else p.lineTo(px, py)
    p.close()
    cv.drawPath(p, fill(c))
    st = stroke(shade(c, 0.62), 2.2, 200, cap=False)
    st.setPathEffect(skia.DashPathEffect.Make([5, 5], 0))
    cv.save(); cv.translate(x, y); cv.scale(0.72, 0.72); cv.translate(-x, -y); cv.drawPath(p, st); cv.restore()


def text(cv, s, x, y, size, c=CREAM, tf=None, a=255):
    f = skia.Font(tf or TFB, size)
    w = f.measureText(s)
    cv.drawString(s, x - w / 2, y, f, fill(c, a))


def felt(cv):
    cv.clear(col((22, 34, 72)))
    g = skia.Paint()
    g.setShader(skia.GradientShader.MakeRadial(skia.Point(W * 0.5, H * 0.55), H * 0.75,
                                               [skia.Color(54, 84, 150, 255), skia.Color(16, 22, 52, 255)]))
    cv.drawRect(skia.Rect.MakeWH(W, H), g)
    n = skia.Paint()
    n.setShader(skia.PerlinNoiseShader.MakeFractalNoise(0.9, 0.9, 3, 4.0))
    n.setBlendMode(skia.BlendMode.kSoftLight)
    n.setAlphaf(0.55)
    cv.drawRect(skia.Rect.MakeWH(W, H), n)
    # felt fibres
    for _ in range(2600):
        x, y = R.uniform(0, W), R.uniform(0, H)
        a = R.uniform(0, math.pi); ln = R.uniform(4, 13)
        cv.drawLine(x, y, x + math.cos(a) * ln, y + math.sin(a) * ln, stroke((190, 205, 255), 1.0, R.randint(10, 30)))


def main(out):
    surf = skia.Surface(W, H)
    cv = surf.getCanvas()
    felt(cv)
    for (x, y, r, rot) in ((120, 1010, 26, 10), (980, 1120, 20, 30), (840, 930, 14, 0), (250, 1150, 13, 20), (930, 1560, 16, 15), (90, 1500, 18, 40)):
        star(cv, x, y, r, rot=rot)
    # title
    text(cv, 'STİL DENEMESİ', W / 2, 120, 46, CREAM)
    text(cv, 'örgü çizgi adam + yüz ifadeleri', W / 2, 172, 30, (176, 190, 232), TFM)
    # expression grid
    names = ['mutlu', 'kahkaha', 'endişeli', 'kızgın', 'şaşkın', 'kurnaz']
    cols = [TEAL, TEAL, TEAL, CORAL, CORAL, CORAL]
    for i, (nm, c) in enumerate(zip(names, cols)):
        cx = 200 + (i % 3) * 340; cy = 350 + (i // 3) * 300
        layer = skia.Paint()
        layer.setImageFilter(skia.ImageFilters.DropShadow(10, 14, 10, 10, skia.Color(4, 6, 20, 120)))
        cv.saveLayer(None, layer)
        yarn_ball(cv, cx, cy, 104, c)
        face(cv, cx, cy + 6, 104, nm)
        cv.restore()
        text(cv, nm, cx, cy + 156, 30, CREAM, TFM)
    # ground strip (felt hill)
    gy = 1790
    hill = skia.Path(); hill.moveTo(0, gy - 40); hill.quadTo(W / 2, gy - 120, W, gy - 40); hill.lineTo(W, H); hill.lineTo(0, H); hill.close()
    cv.drawPath(hill, fill((120, 104, 178)))
    hs = stroke((226, 216, 250), 4, 200, cap=False); hs.setPathEffect(skia.DashPathEffect.Make([16, 12], 0))
    h2 = skia.Path(); h2.moveTo(0, gy - 14); h2.quadTo(W / 2, gy - 94, W, gy - 14)
    cv.drawPath(h2, hs)
    # planet
    layer = skia.Paint(); layer.setImageFilter(skia.ImageFilters.DropShadow(8, 12, 10, 10, skia.Color(4, 6, 20, 120)))
    cv.saveLayer(None, layer)
    yarn_limb(cv, [(790, 1010), (880, 975), (1010, 1000)], 16, MUSTARD)
    yarn_ball(cv, 900, 1010, 62, (236, 150, 96))
    yarn_limb(cv, [(800, 1040), (900, 1062), (1004, 1022)], 16, MUSTARD)
    cv.restore()
    # characters
    figure(cv, 400, gy - 60, 1.0, TEAL, 'mutlu', pose='wave', scarf=CORAL)
    figure(cv, 800, gy - 50, 0.72, LILAC, 'şaşkın', pose='stand', antenna=MUSTARD)
    surf.makeImageSnapshot().save(out, skia.kPNG)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'stil.png')
