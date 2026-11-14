"""13. Kat, 1. Bolum: Asansor. Yalnizca sahneler; ortak parcalar ../ortak.py icinde.
Yapi: soguk acilis (lobide dort golge) -> asansor -> 13. kat ve kurali -> yandan koridor -> asansore donus ve sayim -> bitis karti."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ortak import *
from senaryo import feet_plan, ABONE_END


# ============ SAHNE 1: kanca ============
def scene1(cv, t):
    ts, k = step(t), kk(t)
    f0, v, arr = feet_plan(B('feet')[0], E('n1'))
    sb = B('shut'); inside = sb[1]
    if ts < inside:                                          # lobi: dort golge asansore biner, kapi kapanir
        lobby(cv, 1 - smooth(seg(ts, sb[0] + 0.1, sb[0] + 1.1)))
        with stage(cv):
            for i in range(3, -1, -1):
                x0 = 300 - 170 * i; x = x0 + v * max(0.0, ts - f0)
                if x >= 560: continue
                P = walk(x - x0, 0.62, 1, off=i * 0.27) if ts > f0 else dict(lean=8)
                figure(cv, x, GY - 20, 0.62, (34, 36, 54), None, P, 31 + i, alpha=1 - seg(x, 470, 560))
        display(cv, (0, 0), '1')
        dim(cv, 0.16)
        tally(cv, [(CREAM, 'on')] * sum(ts >= a for a in arr))
    else:                                                    # iceride bes kisi; asansor 13'te durur, isiklar soner
        m13 = frac('n3', 0.7); dark_t = E('n3') + 0.1
        num = str(2 + int(10.99 * seg(ts, inside, m13))) if ts < m13 else '13'
        jolt = m13 <= ts < m13 + 0.8
        sh = jit(k, 5 if jolt else 0)
        cabin(cv, sh)
        ex = 'sakin' if ts < m13 else 'saskin'
        with stage(cv, *sh):
            cast(cv, ts, {'Z': (ex, {}, 0), 'S': (ex, {}, 0), 'K': ('yorgun' if ts < m13 else ex, {}, 0), 'L': (ex, {}, 0), 'U': ('sakin', {}, 0)})
        off = ts >= dark_t
        dim(cv, 0.93 if off else (alt(k, 0.4, 0.64, 1) if jolt else 0.4))
        display(cv, sh, num, red=num == '13')
        if off:
            with stage(cv): dark_eyes(cv, ORDER)
        else:
            tally(cv, [(CREAM, 'on')] * 4 + ([((255, 86, 74), 'on')] if ts >= frac('n2', 0.62) else []))
    tb = B('title'); a = seg(t, tb[0], tb[0] + 0.35)
    if a > 0:
        dim(cv, 0.4 * a)
        card(cv, [(TITLE, 130, (255, 110, 96)), (f'{EP.title()}: {EP_NAME}', 48, CREAM)], a, lerp(0.9, 1.0, smooth(seg(t, tb[0], tb[0] + 0.5))))


# ============ SAHNE 2: asansor ============
def scene2(cv, t):
    ts, k = step(t), kk(t)
    f1, f2, odd = B('flick1'), B('flick2'), B('odd')
    ding = f2[0] + 2.0
    if ts < f1[0] + 1.0: num = str(1 + min(10, int(10 * seg(ts, S('n4'), f1[0] - 0.5))))
    elif ts < ding: num = '12'
    else: num = '13'
    fl = (f1[0] + 0.2 <= ts < f1[0] + 1.5) or (f2[0] + 0.2 <= ts < ding)
    light = (0.25 if (k * 7) % 5 < 2 else 1.0) if fl else (0.72 if ts >= ding else 1.0)
    sh = jit(k, 6 if f2[0] + 0.3 <= ts < ding else 0)
    scared = ts >= f1[0] + 0.2
    cabin(cv, sh)
    # --- Kai ---
    if on(ts, 'k1'): K_ = ('kararli', alt(k, PRESS_A, PRESS_B, 1), 1)
    elif ts < S('k1'): K_ = ('yorgun', alt(k, PRESS_A, PRESS_B, 2), 1)
    elif on(ts, 's1'): K_ = ('yorgun', PRESS_B, -1)
    elif scared: K_ = ('saskin' if ts < S('l2') else 'endise', COWER if ts >= f2[0] else LOOKUP, 0)
    else: K_ = ('yorgun', HIP, 0)
    # --- Sam ---
    if on(ts, 's1'): S_ = ('yorgun', {}, 1)
    elif S('u1b') <= ts < odd[1]: S_ = ('merak', {}, 1)
    elif on(ts, 's5', 0.3, 0.3): S_ = ('mutlu', CALM, 0)
    elif scared: S_ = ('endise' if ts < ding else 'saskin', COWER if ts >= f2[0] else LOOKUP, 0)
    else: S_ = ('mutlu', {}, 0)
    # --- Luna ---
    if on(ts, 'u1'): U_ = ('heyecan', alt(k, UP, {}, 2), 0)
    elif on(ts, 'z1'): U_ = ('mutlu', {}, -1)
    elif on(ts, 'u1b', 0.05, 0.0): U_ = ('mutlu', POINTUP, 0)
    elif ts < odd[1] and ts >= E('u1b'): U_ = ('mutlu', POINTUP, 0)
    else: U_ = ('sakin' if scared else 'mutlu', LOOKUP if scared else {}, 0)
    # --- Zoe ---
    if on(ts, 'z1'): Z_ = ('merak', LEAN_IN, 1)
    elif S('u1b') <= ts < odd[1]: Z_ = ('saskin' if ts > frac('u1b', 0.5) else 'merak', {}, 1)
    elif on(ts, 'z1c') or on(ts, 'l1'): Z_ = ('merak', POINT_R if on(ts, 'z1c') else {}, 0.7)
    elif on(ts, 'z2') or on(ts, 'l1b'): Z_ = ('yorgun', HIP, 0.7)
    elif scared: Z_ = ('saskin' if ts < S('l2') else 'endise', COWER if ts >= f2[0] else LOOKUP, 0)
    else: Z_ = ('mutlu', {}, 0)
    # --- Leo ---
    if S('u1b') <= ts < odd[1]: L_ = ('merak', {}, 1)
    elif on(ts, 'z1c'): L_ = ('mutlu', {}, -1)
    elif on(ts, 'l1'): L_ = ('merak', HOLDUP, 0)
    elif on(ts, 'z2'): L_ = ('saskin', {}, -1)
    elif on(ts, 'l1b'): L_ = ('endise', {}, -1)
    elif scared: L_ = ('saskin' if ts < S('l2') else 'endise', COWER_HOLD if ts >= f2[0] else LOOKUP, 0)
    else: L_ = ('mutlu', {}, 0)
    with stage(cv, *sh):
        cast(cv, ts, {'Z': Z_, 'S': S_, 'K': K_, 'L': L_, 'U': U_})
    dim(cv, (1 - light) * 0.78)
    display(cv, sh, num, red=num == '13')


# ============ SAHNE 3: kapi acilir, kural ============
def scene3(cv, t):
    ts, k = step(t), kk(t)
    d = B('doors'); u = smooth(seg(ts, d[0] + 0.5, d[0] + 2.4))
    pr = B('press')
    turned = d[0] + 0.7 <= ts < frac('v2', 0.5)
    vt = TL.talk('V', ts)
    cabin(cv, (0, 0), u, lamp=alt(k, 1.0, 0.6, 4))
    look_k = S('k2') - 0.1 <= ts < pr[1]                     # herkes Kai'ye, sonra dugmelere bakar
    pi = int((ts - pr[0] - 0.45) / 0.5) if ts >= pr[0] + 0.45 else -1
    hit = 0 <= pi < 4 and (ts - pr[0] - 0.45) % 0.5 < 0.26   # dugmeye basildigi an
    def base(w):
        if turned: return ('sakin', {}, 0, dict(back=True))
        if ts < S('k2') - 0.1: return ('saskin' if ts < S('v3') else 'endise', (COWER_HOLD if w == 'L' else COWER), 0)
        return ('endise', {}, 1 if (look_k and w != 'K') else 0)
    st = {w: base(w) for w in ORDER}
    if not turned:
        if on(ts, 'k2'): st['K'] = ('kararli', alt(k, RANT, HIP, 2), 0)
        elif E('k2') <= ts < pr[1] - 0.2: st['K'] = ('kararli' if pi < 2 else 'endise', PRESS_A if hit else PRESS_B, 1)
        elif ts >= pr[1] - 0.2: st['K'] = ('saskin' if ts < E('l3') else 'endise', {} if ts < E('l3') else SLUMP, 1 if ts < E('l3') else 0)
        if on(ts, 'l3'): st['L'] = ('endise', {}, 1)
        if on(ts, 's2'): st['S'] = ('endise', alt(k, CALM, {}, 3), 0)
        if on(ts, 'z3'): st['Z'] = ('endise', THUMB, 1)
        if on(ts, 'u2'): st['U'] = ('kararli', {}, 0)
        elif ts >= S('k2'): st['U'] = ('sakin', {}, 1 if look_k else 0)
    with stage(cv):
        cast(cv, ts, st)
    if hit: panel_flash(cv, (0, 0), (1, 2, 4, 5)[pi], pi % 2)
    dim(cv, 0.22)
    display(cv, (0, 0), '13', red=True, level=vt, k=k)


# ============ SAHNE 4: koridor (yandan: soldaki asansorden sagdaki kirmizi kapiya) ============
CORR = {'K': (-270, FAR, 0.62), 'U': (-140, NEAR, 0.54), 'S': (-10, FAR, 0.62), 'Z': (125, NEAR, 0.62), 'L': (265, FAR, 0.70)}
C_ORDER = ('K', 'S', 'L', 'U', 'Z')                        # once uzak serit, sonra yakin
PHASE = {'K': 0.0, 'U': 0.3, 'S': 0.55, 'Z': 0.15, 'L': 0.7}
V_WALK, V_RUN, G0 = 230.0, 340.0, 640.0
TURNED = dict(lean=-22, belly=18, aL=(-110, 60, -150, -40), aR=(60, 100, 20, 40))


def _c4():
    tn = B('turn'); a4, b4 = TL.span(4)
    W0 = frac('n5', 0.62); WK = tn[0] + 0.2; W1 = tn[0] + 0.5; W2 = frac('l5', 0.55); W3 = B('opendoor')[0] - 0.2   # W3: kirmizi kapiya varis
    dist = lambda t: V_WALK * (clamp(t, W0, W1) - W0) + V_RUN * (clamp(t, W2, W3) - W2)
    distK = lambda t: V_WALK * (clamp(t, W0, WK) - W0)
    return W0, WK, W1, W2, W3, dist, distK, G0 + dist(b4) + 430


def scene4(cv, t):
    ts, k = step(t), kk(t)
    st_, rg, tn, af = B('steps'), B('ring'), B('turn'), B('after')
    W0, WK, W1, W2, W3, dist, distK, door = _c4()
    d = dist(ts); gx = G0 + d
    # kamera grubu izler; basta kirmizi kapiya gidip doner; Kai donunce ona kayar
    P0 = S('n5') + 0.15
    pan = smooth(seg(ts, P0, P0 + 0.9)) * (1 - smooth(seg(ts, P0 + 1.7, P0 + 2.5)))
    foc = smooth(seg(ts, tn[0] + 0.5, tn[0] + 1.1)) * (1 - smooth(seg(ts, tn[0] + 3.4, tn[0] + 4.2)))
    back = 125 * smooth(seg(ts, st_[0], st_[0] + 1.2))      # karaltiya yer acmak icin grup kadrajda saga kayar
    od = B('opendoor')
    endp = (330 if FMT == 'v' else 150) * smooth(seg(ts, W3 - 1.4, W3))   # sonda kapi kadraja girsin
    cam = lerp(gx - 540 - back, door - 700, pan) - 200 * foc + endp
    open_u = smooth(seg(ts, od[0] + 0.8, od[0] + 2.0))
    reach = smooth(seg(ts, od[0] + 0.1, od[0] + 0.6)) * (1 - smooth(seg(ts, od[0] + 1.3, od[0] + 1.8)))   # Leo kola uzanir
    shocked = ts >= od[0] + 1.5
    gone = tn[0] + 3.0
    sh = jit(k, 7 if tn[0] + 1.5 <= ts < gone else 0)
    side_corridor(cv, cam, door, lamp=alt(k, 1.0, 0.5, 2) if on(ts, 'v4', 0.1, 0.4) else 1.0, k=k, open_u=open_u)
    moving = W0 <= ts < W1 or W2 <= ts < W3
    run = W2 <= ts < W3
    fear = ts >= st_[0] + 0.6
    frozen = W1 <= ts < W2
    with stage(cv, *sh):
        kx = G0 + CORR['K'][0] + distK(ts) - cam            # Kai'nin ekrandaki yeri
        # karalti soldan yaklasir, elinde calan telefon
        if ts < st_[0] + 0.4 or ts >= tn[0] + 3.9: sx = None
        elif ts < tn[0] + 0.5: sx = kx - lerp(540, 240, seg(ts, st_[0] + 0.4, tn[0] + 0.5) ** 0.8)
        elif ts < gone: sx = kx - lerp(240, 130, smooth(seg(ts, tn[0] + 0.5, tn[0] + 1.3)))
        else: sx = kx - lerp(130, 1200, smooth(seg(ts, gone, tn[0] + 3.9)))
        if sx is not None:
            shadow(cv, sx, reach=smooth(seg(ts, tn[0] + 0.9, tn[0] + 1.5)) if ts < gone else 0.0, k=k, ring=rg[0] + 0.2 <= ts < tn[0] + 0.9)
        if tn[0] + 1.6 <= ts < gone + 0.3 and sx is not None:  # sokulen iplik karaltiya cekilir
            al = 255 * (1 - seg(ts, gone - 0.2, gone + 0.3)); y0 = FAR - 330 * 0.62
            pth = skia.Path(); pth.moveTo(kx, y0)
            for i in range(1, 7):
                u_ = i / 6; pth.lineTo(lerp(kx, sx + 60, u_), y0 + (26 if (i + k) % 2 else -26) * (1 - u_) - 20 * u_)
            cv.drawPath(pth, stroke(NAVY, 9, al))
        for i, w in enumerate(C_ORDER):
            off, gy, s = CORR[w]
            if w == 'K':
                if ts >= gone: continue
                x, dd, mv = kx, distK(ts), W0 <= ts < WK
            else:
                x, dd, mv = gx + off - cam, d, moving
            hold = w == 'L'; look = 2.0; alpha = 1.0
            ex = 'endise' if (fear or w in 'ZL') else ('yorgun' if w == 'K' else 'sakin')
            if w == 'U' and not fear: ex = 'sakin'
            if w == 'Z' and st_[0] + 0.6 <= ts < S('z4'): ex = 'saskin'
            if w == 'L' and (on(ts, 'l4') or on(ts, 'l5') or run): ex = 'kararli'
            if w == 'S' and (on(ts, 's3') or on(ts, 's4')): ex = 'kararli'
            if w == 'Z' and on(ts, 'l4'): ex = 'panik'
            if run and w in 'ZSU': ex = 'panik' if ts < af[0] else 'endise'
            if ts >= W3: ex = 'saskin' if shocked else ('kararli' if w == 'L' else 'endise')
            if w == 'K':
                if rg[0] + 0.2 <= ts < S('k3'): ex, look = 'saskin', 1.0
                elif on(ts, 'k3'): ex, look = 'panik', 1.2
                elif S('s4') - 0.1 <= ts < S('k4'): ex, look = 'endise', 0.4
                elif S('k4') <= ts < WK: ex, look = 'endise', -0.6
            if frozen or (S('u3') <= ts < W2):
                if w != 'K': ex = 'panik'
                if w == 'U' and on(ts, 'u3', 0.05, 0.3): ex = 'bagir'
                if w == 'Z' and on(ts, 'z5'): look = 0.8
                if w == 'L' and on(ts, 'l5'): ex = 'kararli'
            if mv:
                pose = walk(dd, s, 1, scared=fear and not run, hold=hold, run=run, off=PHASE[w])
            elif w == 'K' and ts >= WK:
                turned = ts >= tn[0] + 0.6
                look = -2.5 if turned else -1.4
                ex = ('bagir' if ts >= tn[0] + 1.3 else 'saskin') if turned else 'endise'
                pose = TURNED if turned else dict(lean=-8)
                alpha = 1 - seg(ts, tn[0] + 1.7, gone)
            elif ts >= W3 and shocked: pose = dict(lean=-14, belly=12, crouch=10, kL=(-84, -124), kR=(84, -124))   # irkilip geri cekilir
            elif ts >= W3 and w == 'L': pose = mixpose(dict(HOLD, lean=10, belly=-6), dict(aL=HOLD['aL'], aR=(150, 50, 285, 115), lean=18, belly=-8), reach)
            elif ts >= W3: pose = dict(lean=10, belly=-6)
            elif frozen or ts >= W1: pose = COWER_HOLD if hold else COWER
            else: pose = dict(lean=8)
            actor(cv, ts, w, ex, pose, look, alpha=alpha, place=(x, gy, s), pkg_left=(w == 'L' and reach > 0.25))
        if ts >= tn[0] + 2.6:                               # yere dusen kravat
            fall = smooth(seg(ts, tn[0] + 2.6, tn[0] + 3.3))
            tie_at(cv, kx + 24 * fall, lerp(FAR - 500 * 0.62, FAR - 26, fall), 0.62, 1.0, rot=78 * fall)


# ============ SAHNE 5: sayim ============
def scene5(cv, t):
    ts, k = step(t), kk(t)
    cl, rs, ct = B('close'), B('rise'), B('count')
    u = 1 - smooth(seg(ts, cl[0] + 0.2, cl[0] + 1.6))
    up = rs[0] + 0.6                                        # asansor 14'e cikar
    num = '13' if ts < up else '14'
    sh = jit(k, 4 if rs[0] + 0.1 <= ts < up + 0.3 else 0)
    vt = TL.talk('V', ts)
    cabin(cv, sh, u, lamp=0.7)
    who = ('Z', 'S', 'L', 'U')
    n = len(who); stp = (ct[1] - ct[0] - 0.4) / n
    cnt = ('Z', 'L', 'S', 'U')                                # sayim soldan saga
    idx = min(n - 1, int((ts - ct[0] - 0.2) / stp)) if ct[0] + 0.2 <= ts < ct[1] else None
    hi = cnt[idx] if idx is not None else None
    lookmap = {'Z': -1.0, 'S': 0.4, 'L': 0.0, 'U': 1.0}
    T_ = dict(tie=True)
    if ts < frac('n6', 0.45):                                # once sok: yine asansordeler
        st = {w: ('saskin', {} if w == 'L' else LOOKUP, alt(k, -1, 1, 8) if w in 'ZS' else 0) for w in who}
    else:
        st = {w: ('uzgun', {} if w == 'L' else SLUMP, 0) for w in who}
    if S('v5') - 0.2 <= ts < rs[1]:                          # anonsu dinlerler, asansor kalkar
        st = {w: ('endise', {} if w == 'L' else LOOKUP, 0) for w in who}
    if ts >= S('u4') - 0.4:
        st['U'] = ('endise', REACH_L if ts < E('u4') + 0.2 else {}, -1)
        st['L'] = ('merak', {}, 1)
        st['Z'] = ('uzgun', SLUMP, 0); st['S'] = ('uzgun', SLUMP, 0)
    if on(ts, 'l7'): st['L'] = ('yorgun', {}, 1)
    if ts >= frac('u6', 0.45): st['L'] = ('saskin', {}, 1)
    if hi: st['L'] = ('saskin' if hi != 'L' else 'endise', {}, lookmap[hi])
    if ts >= ct[1]:
        st = {w: ('endise', {} if w == 'L' else COWER, lookmap[w] * -0.8) for w in who}   # birbirlerine bakarlar
    st['L'] = st['L'][:3] + (T_,)
    off = ts >= frac('n7b', 0.62)
    with stage(cv, *sh):
        cast(cv, ts, st, who=who)
    if hi:
        dim(cv, 0.62)
        with stage(cv):
            v = ('sakin', {}, 0, dict(talk=None)) if hi != 'L' else st['L']
            cast(cv, ts, {hi: v}, who=(hi,))
    elif ts >= ct[1] and not off: dim(cv, 0.45)
    else: dim(cv, 0.2)
    if off: dim(cv, 0.94)
    display(cv, sh, num, red=True, level=vt, k=k)
    if off:
        with stage(cv): dark_eyes(cv, who, red=who[(k // 5) % n])
        return
    if ts >= ct[0] + 0.2:                                    # sayim rozetleri: 1, 2, 3, 4
        shown = n if idx is None else idx + 1
        q = ts >= S('n7b')
        with stage(cv):
            for i in range(shown): badge(cv, cnt[i], '?' if q else str(i + 1), red=q)
    if ts >= S('n7'):                                        # dort bindi, biri gitti, uc olmali; ama dort var
        gone = ts >= frac('n7', 0.38)
        marks = [(CREAM, 'on')] * 3 + [(NAVY, 'x' if gone else 'on')]
        if ts >= frac('n7b', 0.22): marks.append(((255, 86, 74), 'on'))
        tally(cv, marks)


# ============ SAHNE 6: bitis karti ============
def scene6(cv, t):
    ts, k = step(t), kk(t)
    a0, _ = TL.span(6); who = ('Z', 'S', 'L', 'U')
    cabin(cv, (0, 0)); dim(cv, 0.94)
    display(cv, (0, 0), '14', red=True)
    with stage(cv): dark_eyes(cv, who, red=who[(k // 7) % 4])
    a = seg(t, a0 + 0.3, a0 + 0.8)
    card(cv, [('Asansöre hiç binmeyen kim?', 60 if FMT == 'v' else 70, CREAM), ('Yorumlara yaz', 40, (176, 190, 232)), ('2. Bölüm: Sessizlik', 46, (255, 110, 96))], a, cy=450 if FMT == 'v' else 168)
    abone(cv, t, a0 + ABONE_END, pos=(W / 2, 1235) if FMT == 'v' else (W / 2, 770))


if __name__ == '__main__':
    run({1: scene1, 2: scene2, 3: scene3, 4: scene4, 5: scene5, 6: scene6})
