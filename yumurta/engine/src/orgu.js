// orgu.js: crochet (amigurumi) characters for dizivanastudio, a drop-in replacement for Toon.
// Same draw() parameters as Toon (expr, mouth, blink, look, lookY, gazeX, gazeY, lid, brow, lean, bob, tilt, armL, armR,
// propL, propR, flip, sweat, laughMarks, lit, rim, noArmL, noArmR), so every pose and expression of the egg-head kit
// works with yarn characters. Extra: walk (step phase, radians), squash (-.2..+.2, + = flattened), blush (0..1).
// The channel's identity is kept: a stitched yarn ball head, yarn-tube body and limbs, ball hands and feet,
// an embroidered face; what comes from the egg-head kit is the acting (lids, brows, laughs, sweat, lip flap).
//
// look: { yarn: body colour, head: head colour (default yarn), headR: head radius (design units, default 150),
//   hair: { style: 'bob' | 'kisa' | 'kivircik' | 'topuz', color }, lashes: true,
//   hat: 'bere' | 'kasket' | 'kulah' | 'cook' | 'sarik', hatColor, pompom, badge,
//   scarf, tie, buttons, belly: true | rx (round tummy: the boss), fat: true (a really round body, thick short limbs, double chin),
//   nose: { len: 1..2.2, color } (a long crocheted nose that points where the face turns; p.sniff 0..1 wiggles it),
//   antenna: colour (two yarn antennae with balls: aliens), bigEyes: true (shiny ovals in calm expressions), glasses, mustache, beard, beardLen, height }
import * as THREE from 'three';
import { Toon, PLUM, toonHat, toonBeard, TOON_PROPS } from './toon.js';

const CW = 768, CH = 1184, TOP = 160, SOLE = 1000, RES = 1.5;     // must match toon.js
const D2R = Math.PI / 180;
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));

// ---------- colour ----------
const CC = new Map();
function shade(hex, k) {
  const key = hex + k.toFixed(2); let v = CC.get(key);
  if (!v) { const c = new THREE.Color(hex); c.r = Math.min(1, c.r * k); c.g = Math.min(1, c.g * k); c.b = Math.min(1, c.b * k); v = '#' + c.getHexString(); CC.set(key, v); }
  return v;
}
function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

// ---------- yarn primitives (ported from dizivanastudio motor/stil.py: every stitch is a small V, lit from the key light) ----------
// buckets: stitches of the same tone and thickness are stroked together (one path per bucket)
function flush(g, buckets, c) {
  g.lineCap = 'round'; g.lineJoin = 'round';
  for (const [k, P] of [...buckets.entries()].sort((a, b) => a[0] - b[0])) {
    const lv = Math.floor(k / 100), sw = k % 100;
    g.strokeStyle = shade(c, lv / 20); g.lineWidth = Math.max(1.2, sw / 2); g.stroke(P);
  }
}
function bucket(B, lv, q) { const k = Math.round(clamp(lv, 0, 1.6) * 20) * 100 + Math.min(99, Math.round(q * 2.6)); let P = B.get(k); if (!P) B.set(k, P = new Path2D()); return P; }

// a quadratic Bézier sampled by arc length: pos(d), tan(d)
function curve(p0, p1, p2) {
  const N = 40, pts = [], acc = [0];
  for (let i = 0; i <= N; i++) { const t = i / N, u = 1 - t; pts.push([u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]]); }
  for (let i = 1; i <= N; i++) acc.push(acc[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const L = acc[N];
  const at = d => { d = clamp(d, 0, L); let i = 1; while (i < N && acc[i] < d) i++; const a = acc[i - 1], b = acc[i], k = b > a ? (d - a) / (b - a) : 0;
    const x = pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * k, y = pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * k, l = b - a || 1;
    return [x, y, (pts[i][0] - pts[i - 1][0]) / l, (pts[i][1] - pts[i - 1][1]) / l]; };
  return { L, at, path: () => { const P = new Path2D(); P.moveTo(...p0); P.quadraticCurveTo(...p1, ...p2); return P; } };
}

// crochet tube along p0 -> (p1) -> p2: rows of V stitches across the tube, cylinder shading, a little fuzz
function yarnTube(g, p0, p1, p2, w, c, lit, seed) {
  const C = curve(p0, p1, p2), P = C.path(), hw = w / 2, LD = [lit * .5, -.78];
  g.lineCap = 'round'; g.lineJoin = 'round';
  g.strokeStyle = shade(c, .56); g.lineWidth = w; g.stroke(P);
  g.strokeStyle = shade(c, .74); g.lineWidth = w * .93; g.stroke(P);
  const dphi = Math.PI / 5, rs = hw * .52, h = rs * .36, B = new Map();
  for (let d = rs * .2, i = 0; d < C.L - rs * .1; d += rs, i++) {
    const [x0, y0, tx, ty] = C.at(d), nx = -ty, ny = tx, nl = nx * LD[0] + ny * LD[1], off = i % 2 ? .5 : 0;
    for (let j = -3; j < 3; j++) {
      const phi = (j + off + .25) * dphi; if (Math.abs(phi) > 1.4) continue;
      const sp = Math.sin(phi), cp = Math.cos(phi), bb = hw * .86 * sp, q = hw * .2 * cp + .3, lv = .74 + .3 * cp + .26 * sp * nl;
      const x = x0 + nx * bb, y = y0 + ny * bb, Q = bucket(B, lv, q);
      Q.moveTo(x - nx * q - tx * h, y - ny * q - ty * h); Q.lineTo(x + tx * h, y + ty * h); Q.lineTo(x + nx * q - tx * h, y + ny * q - ty * h);
    }
  }
  flush(g, B, c);
  const R = rng(seed); g.strokeStyle = shade(c, 1.12); g.globalAlpha = .42; g.lineWidth = 1.1; g.beginPath();
  for (let k = 0, n = Math.floor(C.L / 14); k < n; k++) {
    const [x, y, tx, ty] = C.at(R() * C.L), s = R() < .5 ? -1 : 1, ln = (1.5 + R() * 2.4) * Math.sqrt(w / 46), ax = R() * 1.2 - .6;
    const sx = x - ty * s * hw * .97, sy = y + tx * s * hw * .97; g.moveTo(sx, sy); g.lineTo(sx + (-ty * s + tx * ax) * ln, sy + (tx * s + ty * ax) * ln);
  }
  g.stroke(); g.globalAlpha = 1;
  return C;
}

// crochet ball / egg: horizontal rows of V stitches (crocheted top-down). spin (rad) slides the stitch columns
// sideways: the head seems to turn with its face.
function yarnBall(g, cx, cy, rx, ry, c, lit, { rows, spin = 0, seed = 1, fuzz = true } = {}) {
  const LD = [lit * .5, -.78];
  g.fillStyle = shade(c, .56); g.beginPath(); g.ellipse(cx, cy, rx, ry, 0, 0, 6.29); g.fill();
  g.fillStyle = shade(c, .74); g.beginPath(); g.ellipse(cx, cy, rx * .975, ry * .975, 0, 0, 6.29); g.fill();
  g.save(); g.beginPath(); g.ellipse(cx, cy, rx * .985, ry * .985, 0, 0, 6.29); g.clip();
  rows = rows || Math.max(4, Math.round(ry / 8.6));
  const dth = Math.PI / rows, Rx = rx * .975, Ry = ry * .975, B = new Map();
  for (let k = 0; k < rows; k++) {
    const th = -Math.PI / 2 + (k + .5) * dth, st = Math.sin(th), ct = Math.cos(th), y = cy + Ry * st, rr = Rx * ct;
    const h = Math.max(.6, Ry * dth * .2 * (.35 + .65 * ct)), n = Math.max(2, Math.round(Math.PI * rr / (Ry * dth))), dp = Math.PI / n;
    const sh = ((spin / dp) % 1 + 1) % 1;
    for (let j = -1; j <= n + 1; j++) {
      const phi = -Math.PI / 2 + (j + (k % 2 ? 0 : .5) + sh) * dp; if (Math.abs(phi) > 1.46) continue;
      const sp = Math.sin(phi), cp = Math.cos(phi), x = cx + rr * sp, q = rr * dp * .5 * cp * .62 + .3;
      const lv = .72 + .32 * ct * cp + .28 * (ct * sp * LD[0] + st * LD[1]), Q = bucket(B, lv, q);
      Q.moveTo(x - q, y - h); Q.lineTo(x, y + h); Q.lineTo(x + q, y - h);
    }
  }
  flush(g, B, c); g.restore();
  if (!fuzz) return;
  const R = rng(seed); g.strokeStyle = shade(c, 1.12); g.globalAlpha = .42; g.lineWidth = 1.1; g.beginPath();
  for (let k = 0, n = Math.floor((rx + ry) * .18); k < n; k++) {
    const a = R() * 6.283, ln = (1.5 + R() * 2.5) * Math.sqrt((rx + ry) / 220), tw = R() - .5;
    const x = cx + Math.cos(a) * rx * .99, y = cy + Math.sin(a) * ry * .99; g.moveTo(x, y); g.lineTo(x + Math.cos(a + tw) * ln, y + Math.sin(a + tw) * ln);
  }
  g.stroke(); g.globalAlpha = 1;
}
// soft plum shadow pushed away from the light, behind a part: the figure sits in the world like the egg-heads do
function under(g, fn, lit, k = 1) { g.save(); g.translate(-lit * 6 * k, 8 * k); g.globalAlpha = .38; fn(); g.restore(); }
function rimLight(g, clipFn, b, rim, lit) {
  if (!rim || !rim.a) return;
  g.save(); clipFn(); g.clip();
  const x0 = b.cx + lit * b.w * .5, x1 = b.cx + lit * b.w * (.5 - (rim.w ?? .45));
  const gr = g.createLinearGradient(x0, 0, x1, 0); gr.addColorStop(0, rim.color); gr.addColorStop(1, 'rgba(0,0,0,0)');
  g.globalAlpha = rim.a * .85; g.globalCompositeOperation = 'screen'; g.fillStyle = gr; g.fillRect(b.cx - b.w, b.cy - b.h, b.w * 2, b.h * 2);
  g.restore();
}

// ---------- embroidered face (the egg-head kit's acting, sewn with dark thread) ----------
const EXPR = {
  neutral:   { eye: 'lid', lid: .30, lt: 0,    by: -.27, bt: 0,    bc: .5,  mouth: 'flat' },
  smile:     { eye: 'lid', lid: .22, lt: -.03, by: -.29, bt: -.06, bc: .9,  mouth: 'smile' },
  smug:      { eye: 'lid', lid: .47, lt: -.03, by: -.26, bt: -.04, bc: .6,  mouth: 'smirk', browUp: 1 },
  focused:   { eye: 'lid', lid: .40, lt: .10,  by: -.21, bt: .17,  bc: .3,  mouth: 'flat' },
  angry:     { eye: 'lid', lid: .38, lt: .24,  by: -.18, bt: .38,  bc: .2,  mouth: 'frown' },
  proud:     { eye: 'lid', lid: .36, lt: -.05, by: -.3,  bt: -.1,  bc: .9,  mouth: 'smile' },
  surprised: { eye: 'round', r: .108, by: -.37, bt: -.06, bc: 1.3, mouth: 'o' },
  worried:   { eye: 'round', r: .09, by: -.33, bt: -.34, bc: .4,  mouth: 'wavy' },
  laugh:     { eye: 'arc',  by: -.3,  bt: -.12, bc: 1.0, mouth: 'grin' },
  grin:      { eye: 'oval', by: -.33, bt: -.08, bc: 1.0, mouth: 'grin' },
  happy:     { eye: 'oval', by: -.31, bt: -.06, bc: .9,  mouth: 'smile' },
};
// the channel's Turkish expression names keep working
const ALIAS = { sakin: 'neutral', mutlu: 'happy', kahkaha: 'laugh', 'endişeli': 'worried', 'kızgın': 'angry', 'şaşkın': 'surprised', kurnaz: 'smug',
  gururlu: 'proud', 'odaklı': 'focused', 'sırıtma': 'grin', 'gülümseme': 'smile' };
// a line sewn with thread: dark stroke + a dashed glint along it
function sew(g, lw) {
  g.strokeStyle = PLUM; g.lineWidth = lw; g.stroke();
  g.save(); g.strokeStyle = 'rgba(255,255,255,.22)'; g.lineWidth = Math.max(1, lw * .24); g.setLineDash([lw * .9, lw * 1.1]); g.stroke(); g.restore();
}
function glint(g, x, y, r, a = .9) { g.fillStyle = `rgba(255,255,255,${a})`; g.beginPath(); g.arc(x, y, r, 0, 6.29); g.fill(); }

function face(g, w, h, f, L, exprName) {
  let E = EXPR[exprName] || EXPR.neutral;
  if (L.bigEyes && E.eye === 'lid' && /neutral|smile|proud|happy/.test(exprName)) E = { ...E, eye: 'oval', big: 1.35 };
  const turn = clamp(f.look || 0, -1, 1), tv = clamp(f.lookY || 0, -1, 1);
  const fx = turn * w * .12, fy = tv * h * .05 + h * .05 + (L.hat === 'kasket' || L.hat === 'bere' ? h * .03 : 0);
  const gx = (f.gazeX ?? turn) * w * .014, gy = (f.gazeY ?? tv) * w * .012;
  const lw = w * .036, ey = fy - h * .04, bk = f.blink || 0, shut = bk > .75, half = bk > .25 && !shut;
  g.lineCap = 'round'; g.lineJoin = 'round';
  // cheeks: pink felt circles (always; brighter when laughing, angry or shy)
  const bl = clamp(.55 + (f.blush || 0) * .45 + (exprName === 'laugh' || exprName === 'angry' ? .25 : 0), 0, 1);
  g.save(); g.filter = `blur(${w * .022 * RES}px)`; g.fillStyle = `rgba(244,120,140,${bl * .85})`;
  for (const s of [-1, 1]) { const far = Math.max(0, s * turn); g.beginPath(); g.ellipse(fx + s * w * (.29 - .06 * far), fy + h * .13, w * .075 * (1 - .3 * far), w * .045, 0, 0, 6.29); g.fill(); }
  g.restore();
  for (const s of [-1, 1]) {
    const far = Math.max(0, s * turn), q = 1 - .2 * far, x = fx + s * w * (.155 - .025 * far);
    // brow
    const up = E.browUp && s === (turn < 0 ? -1 : 1) ? 1 : 0;
    const by = fy + h * (E.by - .06 * up) + (f.brow || 0) * h * -.04, bl2 = w * .085 * q, bt = E.bt * (up ? -.5 : 1);
    const xi = x - s * bl2, xo = x + s * bl2, yi = by + bt * bl2 * 1.1, yo = by - bt * bl2 * .5;
    const cxm = (xi + xo) / 2, cym = (yi + yo) / 2 - w * .024 * (E.bc + up * .8);
    g.beginPath(); g.moveTo(xi, yi); g.quadraticCurveTo(cxm, cym, xo, yo); sew(g, lw * 1.15);
    // eye
    if (shut || E.eye === 'lid') {
      const lid = clamp((E.lid == null ? .3 : E.lid) + (f.lid || 0) + (half ? .38 : 0), 0, .95);
      const rx = w * .07 * q, ry = w * (.13 - .1 * lid), hl = w * .088 * q;
      g.save(); g.translate(x, ey - w * .03); g.rotate(-s * (E.lt || 0));
      if (shut) { g.beginPath(); g.moveTo(-hl, w * .03); g.quadraticCurveTo(0, w * .058, hl, w * .03); sew(g, lw); }
      else {
        g.save(); g.beginPath(); g.rect(-rx * 3, 0, rx * 6, ry * 3); g.clip();
        g.fillStyle = PLUM; g.beginPath(); g.ellipse(gx * q * 1.4, gy * .5, rx, ry, 0, 0, 6.29); g.fill();
        glint(g, gx * q * 1.4 - rx * .38, ry * .38 + gy * .5, w * .017); g.restore();       // a safety-eye bead: one bright glint
        g.beginPath(); g.moveTo(-hl, 0); g.lineTo(hl, 0); sew(g, lw);
        if (L.lashes) { g.beginPath(); g.moveTo(s * hl * .7, 0); g.lineTo(s * hl * 1.25, -w * .03); g.moveTo(s * hl * .95, w * .012); g.lineTo(s * hl * 1.45, -w * .006); sew(g, lw * .7); }
      }
      g.restore();
    } else if (E.eye === 'round') {
      const r = w * E.r * (1 - .1 * far), xr = fx + s * r * 1.02 + turn * w * .01;
      g.fillStyle = '#fbf6ea'; g.beginPath(); g.arc(xr, ey, r, 0, 6.29); g.fill(); sew(g, lw * .8);
      g.fillStyle = PLUM; g.beginPath(); g.arc(xr + gx * 1.8, ey + gy * 1.8 + w * .004, w * .034, 0, 6.29); g.fill();
      glint(g, xr + gx * 1.8 - w * .012, ey + gy * 1.8 - w * .01, w * .011);
      if (L.lashes) { g.beginPath(); g.moveTo(xr + s * r * .7, ey - r * .7); g.lineTo(xr + s * r * 1.15, ey - r * 1.1); sew(g, lw * .7); }
    } else if (E.eye === 'arc') {
      g.beginPath(); g.moveTo(x - w * .064 * q, ey + w * .014); g.quadraticCurveTo(x, ey - w * .075, x + w * .064 * q, ey + w * .014); sew(g, lw * 1.1);
    } else {
      const bg = E.big || 1;
      g.fillStyle = PLUM; g.beginPath(); g.ellipse(x + gx, ey + gy, w * .05 * q * bg, w * .08 * bg, 0, 0, 6.29); g.fill();
      glint(g, x + gx - w * .016 * bg, ey + gy - w * .03 * bg, w * .018 * bg); if (bg > 1) glint(g, x + gx + w * .02, ey + gy + w * .04, w * .009, .7);
      if (L.lashes) { g.beginPath(); g.moveTo(x + s * w * .04, ey - w * .06); g.lineTo(x + s * w * .085, ey - w * .095); sew(g, lw * .7); }
    }
  }
  // mouth
  const mx = fx + turn * w * .03, my = fy + h * .19, m = clamp(f.mouth || 0, 0, 1), sg = turn < 0 ? -1 : 1, kind = E.mouth;
  if (kind === 'grin') {
    const k = .55 + .45 * Math.max(m, exprName === 'laugh' ? .5 : .3), mw = w * .13, mh = w * .13 * k;
    const shp = () => { g.beginPath(); g.moveTo(mx - mw, my - w * .03); g.lineTo(mx + mw, my - w * .03); g.quadraticCurveTo(mx + mw * .92, my + mh, mx, my + mh); g.quadraticCurveTo(mx - mw * .92, my + mh, mx - mw, my - w * .03); g.closePath(); };
    shp(); g.fillStyle = '#4a1826'; g.fill();
    g.save(); shp(); g.clip();
    g.fillStyle = '#ec6a7a'; g.beginPath(); g.ellipse(mx, my + mh * 1.05, mw * .6, mh * .5, 0, 0, 6.29); g.fill();
    g.fillStyle = '#fbf6ea'; g.fillRect(mx - mw, my - w * .04, mw * 2, w * .055);
    g.strokeStyle = 'rgba(42,26,44,.55)'; g.lineWidth = lw * .4; for (let i = -2; i <= 2; i++) { g.beginPath(); g.moveTo(mx + i * mw * .36, my - w * .04); g.lineTo(mx + i * mw * .36, my + w * .015); g.stroke(); }
    g.restore(); shp(); sew(g, lw * .95);
  } else if (m > .08 || kind === 'o') {
    const k = kind === 'o' ? Math.max(.75, m) : m;
    g.fillStyle = '#4a1826'; g.beginPath(); g.ellipse(mx, my + w * .012, w * (.04 + k * .022), w * (.016 + k * .05), 0, 0, 6.29); g.fill();
    if (k > .45) { g.save(); g.clip(); g.fillStyle = '#ec6a7a'; g.beginPath(); g.ellipse(mx, my + w * (.03 + k * .05), w * .045, w * .034, 0, 0, 6.29); g.fill(); g.restore(); }
    g.beginPath(); g.ellipse(mx, my + w * .012, w * (.04 + k * .022), w * (.016 + k * .05), 0, 0, 6.29); sew(g, lw * .85);
  } else {
    g.beginPath();
    if (kind === 'smile') { g.moveTo(mx - w * .08, my - w * .014); g.quadraticCurveTo(mx, my + w * .065, mx + w * .08, my - w * .014); }
    else if (kind === 'smirk') { g.moveTo(mx - sg * w * .035, my + w * .012); g.quadraticCurveTo(mx + sg * w * .04, my + w * .05, mx + sg * w * .09, my - w * .028);
      g.moveTo(mx + sg * w * .077, my - w * .046); g.lineTo(mx + sg * w * .106, my - w * .012); }
    else if (kind === 'frown') { g.moveTo(mx - w * .06, my + w * .022); g.quadraticCurveTo(mx, my - w * .038, mx + w * .06, my + w * .022); }
    else if (kind === 'wavy') { g.moveTo(mx - w * .064, my); g.quadraticCurveTo(mx - w * .032, my - w * .035, mx, my); g.quadraticCurveTo(mx + w * .032, my + w * .035, mx + w * .064, my); }
    else { g.moveTo(mx - sg * w * .052, my + w * .01); g.quadraticCurveTo(mx - sg * w * .01, my - w * .022, mx + sg * w * .052, my + w * .002); }
    sew(g, lw * .95);
  }
  if (L.mustache) {                                       // a yarn moustache: two lobes that sweep out and curl up
    const col = L.mustache === true ? '#3a2a26' : L.mustache, y = my - h * .08;
    g.save(); g.translate(mx, y); g.scale(1.45, 1.45); g.translate(-mx, -y);
    g.fillStyle = col; g.lineWidth = lw * .45;
    for (const s of [-1, 1]) {
      g.beginPath(); g.moveTo(mx, y - w * .014);
      g.bezierCurveTo(mx + s * w * .06, y - w * .05, mx + s * w * .13, y - w * .02, mx + s * w * .16, y - w * .05);
      g.bezierCurveTo(mx + s * w * .15, y + w * .036, mx + s * w * .06, y + w * .044, mx, y + w * .016); g.closePath(); g.fill();
      g.save(); g.clip(); g.strokeStyle = shade(col, 1.45); g.lineWidth = 2.2; g.globalAlpha = .6;
      for (let k = 1; k < 5; k++) { g.beginPath(); g.moveTo(mx + s * w * .02 * k, y - w * .02); g.lineTo(mx + s * w * .03 * k, y + w * .03); g.stroke(); }
      g.restore(); g.strokeStyle = PLUM; g.stroke();
    }
    g.restore();
  }
  if (L.glasses) {                                        // thin wire frames
    g.strokeStyle = L.glasses === true ? '#2a1a2c' : L.glasses; g.lineWidth = lw * .55;
    for (const s of [-1, 1]) { const far = Math.max(0, s * turn); g.beginPath(); g.ellipse(fx + s * w * (.155 - .025 * far), ey - w * .01, w * .09 * (1 - .2 * far), w * .08, 0, 0, 6.29); g.stroke(); }
    g.beginPath(); g.moveTo(fx - w * .07, ey - w * .02); g.quadraticCurveTo(fx, ey - w * .045, fx + w * .07, ey - w * .02); g.stroke();
    g.globalAlpha = .35; glint(g, fx - w * .19, ey - w * .05, w * .018); g.globalAlpha = 1;
  }
  if (L.fat) {                                            // a double chin under the mouth
    g.beginPath(); g.moveTo(mx - w * .14, my + w * .16); g.quadraticCurveTo(mx, my + w * .23, mx + w * .14, my + w * .16); sew(g, lw * .7);
  }
  if (L.nose) {                                           // a long, fat crocheted nose: sticks out to the side the face turns to
    const N = L.nose === true ? {} : L.nose, len = N.len ?? 1.4, nc = N.color || null;
    const sgn = turn < -.05 ? -1 : 1, k = .5 + .5 * Math.abs(turn), wig = (f.sniff || 0) * Math.sin((f.sniffT || 0) * 40) * w * .03;
    const x0 = fx + sgn * w * .02, y0 = ey + w * .085, L1 = len * w * .27 * k + w * .07;
    const x2 = x0 + sgn * L1, y2 = y0 - w * .02 - L1 * .08 + wig;
    const col = nc || f.__head, nw = w * (.12 + .02 * len);
    under(g, () => { g.strokeStyle = PLUM; g.lineWidth = nw; g.lineCap = 'round'; g.beginPath(); g.moveTo(x0, y0); g.quadraticCurveTo(x0 + sgn * L1 * .5, y0 + w * .03, x2, y2); g.stroke(); }, f.lit ?? -1, .5);
    yarnTube(g, [x0, y0], [x0 + sgn * L1 * .5, y0 + w * .03], [x2, y2], nw, col, f.lit ?? -1, 77);
    yarnBall(g, x2 + sgn * w * .02, y2, w * .085, w * .078, shade(col, 1.1), f.lit ?? -1, { rows: 5, seed: 78, fuzz: false });
    g.fillStyle = 'rgba(42,26,44,.5)'; g.beginPath(); g.ellipse(x2 + sgn * w * .045, y2 + w * .04, w * .016, w * .01, 0, 0, 6.29); g.fill();
  }
}

// ---------- hair and hats (drawn around the head centre, R = head radius) ----------
function hairBack(g, R, H, lit, turn) {                    // the part of a bob that hangs behind the head
  if (H.style !== 'bob' && H.style !== 'uzun') return;
  const c = H.color || '#3a3a7a', long = H.style === 'uzun' ? 1.5 : 1;
  const shp = () => { g.beginPath(); g.moveTo(-R * 1.06, -R * .1); g.quadraticCurveTo(-R * 1.18, R * .55 * long, -R * .86, R * .62 * long);
    g.lineTo(R * .86, R * .62 * long); g.quadraticCurveTo(R * 1.18, R * .55 * long, R * 1.06, -R * .1); g.closePath(); };
  shp(); g.fillStyle = shade(c, .62); g.fill();
}
function hairFront(g, R, H, lit, turn, seed) {
  const c = H.color || '#3a3a7a', st = H.style, ox = turn * R * .07;
  if (st === 'bob' || st === 'uzun') {
    const long = st === 'uzun' ? 1.5 : 1;
    const shp = () => { g.beginPath(); g.moveTo(-R * 1.07, R * .52 * long);
      g.bezierCurveTo(-R * 1.2, -R * .2, -R * .9, -R * 1.12, ox, -R * 1.1);
      g.bezierCurveTo(R * .9, -R * 1.12, R * 1.2, -R * .2, R * 1.07, R * .52 * long);
      g.quadraticCurveTo(R * .96, R * .6 * long, R * .82, R * .5 * long); g.quadraticCurveTo(R * .86, -R * .05, R * .66 + ox, -R * .44);
      for (let k = 4; k >= -4; k--) { const x = ox + k * R * .155; g.quadraticCurveTo(x + R * .08, -R * .36, x, -R * .5); }   // a scalloped fringe
      g.quadraticCurveTo(-R * .86, -R * .05, -R * .82, R * .5 * long); g.quadraticCurveTo(-R * .96, R * .6 * long, -R * 1.07, R * .52 * long); g.closePath(); };
    under(g, () => { shp(); g.fillStyle = PLUM; g.fill(); }, lit, .6);
    shp(); g.fillStyle = shade(c, .82); g.fill();
    g.save(); shp(); g.clip(); g.lineCap = 'round';
    for (let k = -9; k <= 9; k++) {                       // yarn strands from the crown
      const x1 = ox + k * R * .12, side = Math.abs(k) > 5;
      g.strokeStyle = shade(c, k % 2 ? .62 : 1.08 + (k * lit > 0 ? .18 : 0)); g.lineWidth = k % 2 ? 5 : 7;
      g.beginPath(); g.moveTo(ox + k * R * .02, -R * 1.08); g.quadraticCurveTo(x1 * 1.05, -R * .7, side ? x1 * 1.12 : x1, side ? R * .55 * long : -R * .42); g.stroke();
    }
    g.restore(); shp(); g.strokeStyle = shade(c, .5); g.lineWidth = 3; g.stroke();
  } else if (st === 'kisa' || st === 'kivircik') {
    const cap = () => { g.beginPath(); g.moveTo(-R * 1.03, -R * .02); g.bezierCurveTo(-R * 1.1, -R * 1.36, R * 1.1, -R * 1.36, R * 1.03, -R * .02);
      g.quadraticCurveTo(R * .9, -R * .4, R * .5 + ox, -R * .55); g.quadraticCurveTo(R * .1 + ox, -R * .5, -R * .18 + ox, -R * .66);
      g.quadraticCurveTo(-R * .55, -R * .5, -R * .88, -R * .4); g.quadraticCurveTo(-R * .96, -R * .22, -R * 1.0, -R * .02); g.closePath(); };
    under(g, () => { cap(); g.fillStyle = PLUM; g.fill(); }, lit, .5);
    cap(); g.fillStyle = shade(c, .85); g.fill();
    g.save(); cap(); g.clip(); g.lineCap = 'round';
    for (let k = -8; k <= 8; k++) { g.strokeStyle = shade(c, k % 2 ? .6 : 1.15 + (k * lit > 0 ? .15 : 0)); g.lineWidth = 5;
      g.beginPath(); g.moveTo(ox - R * .18 + k * R * .02, -R * .66); g.quadraticCurveTo(k * R * .1, -R * 1.0, k * R * .125, -R * .2 - Math.abs(k) * R * .03); g.stroke(); }
    g.restore(); cap(); g.strokeStyle = shade(c, .45); g.lineWidth = 3; g.stroke();
    if (st === 'kivircik') for (let k = 0; k < 11; k++) {
      const a = (-170 + k * 16) * D2R, rr = R * (.14 + .03 * Math.sin(k * 2.3));
      yarnBall(g, ox * .4 + Math.cos(a) * R * .9, Math.sin(a) * R * .92, rr, rr, c, lit, { rows: 3, seed: seed + k, fuzz: false });
    }
  } else if (st === 'topuz') {                             // smooth hair with a bun on top
    yarnBall(g, ox * .5, -R * 1.12, R * .36, R * .32, c, lit, { rows: 6, seed });
    const shp = () => { g.beginPath(); g.moveTo(-R * 1.02, -R * .1); g.bezierCurveTo(-R * 1.08, -R * 1.34, R * 1.08, -R * 1.34, R * 1.02, -R * .1);
      g.quadraticCurveTo(R * .5, -R * .62, ox, -R * .55); g.quadraticCurveTo(-R * .5, -R * .62, -R * .98, -R * .1); g.closePath(); };
    shp(); g.fillStyle = shade(c, .85); g.fill();
    g.save(); shp(); g.clip(); g.lineCap = 'round';
    for (let k = -7; k <= 7; k++) { g.strokeStyle = shade(c, k % 2 ? .6 : 1.15); g.lineWidth = 5; g.beginPath(); g.moveTo(ox + k * R * .03, -R * 1.0); g.quadraticCurveTo(k * R * .13, -R * .85, k * R * .15, -R * .3 - Math.abs(k) * R * .02); g.stroke(); }
    g.restore();
  }
}
function hat(g, R, L, lit, seed) {
  const kind = L.hat, c = L.hatColor || '#c8323a';
  if (kind === 'bere') {                                   // a knitted beanie: ribs, a folded band, a pompom
    const dome = () => { g.beginPath(); g.moveTo(-R * 1.03, -R * .28); g.bezierCurveTo(-R * 1.08, -R * 1.28, R * 1.08, -R * 1.28, R * 1.03, -R * .28); g.closePath(); };
    under(g, () => { dome(); g.fillStyle = PLUM; g.fill(); }, lit, .6);
    g.save(); g.beginPath(); g.rect(-R * 2, -R * 3, R * 4, R * 2.7); g.clip();          // only the dome of the ball
    yarnBall(g, 0, -R * .56, R * 1.04, R * .62, c, lit, { rows: 7, seed, fuzz: false }); g.restore();
    g.save(); g.beginPath(); g.ellipse(0, -R * .56, R * 1.04, R * .62, 0, 0, 6.29); g.clip(); g.lineCap = 'round';
    for (let k = -8; k <= 8; k++) { g.strokeStyle = shade(c, k % 2 ? .62 : 1.12); g.lineWidth = 4; g.beginPath(); g.moveTo(k * R * .05, -R * 1.15); g.quadraticCurveTo(k * R * .1, -R * .8, k * R * .125, -R * .3); g.stroke(); }
    g.restore();
    const band = () => { g.beginPath(); g.roundRect(-R * 1.08, -R * .5, R * 2.16, R * .3, R * .14); };
    band(); g.fillStyle = shade(c, .9); g.fill();
    g.save(); band(); g.clip(); for (let x = -R * 1.1; x < R * 1.1; x += 11) { g.strokeStyle = shade(c, (x / 11 | 0) % 2 ? .62 : 1.18); g.lineWidth = 5; g.beginPath(); g.moveTo(x, -R * .52); g.lineTo(x, -R * .18); g.stroke(); } g.restore();
    band(); g.strokeStyle = shade(c, .5); g.lineWidth = 3; g.stroke();
    const pc = L.pompom || '#fbf3e2'; yarnBall(g, 0, -R * 1.2, R * .26, R * .24, pc, lit, { rows: 5, seed: seed + 9 });
  } else if (kind === 'kasket') {                          // a conductor / porter cap: stitched crown, dark visor, a badge
    const o = -R * .14;
    const crown = () => { g.beginPath(); g.moveTo(-R * .98, o - R * .42); g.bezierCurveTo(-R * 1.1, o - R * 1.18, R * 1.1, o - R * 1.18, R * .98, o - R * .42); g.closePath(); };
    under(g, () => { crown(); g.fillStyle = PLUM; g.fill(); }, lit, .6);
    g.save(); g.beginPath(); g.rect(-R * 2, -R * 3, R * 4, R * 2.58 + o); g.clip();
    yarnBall(g, 0, o - R * .72, R * 1.0, R * .46, c, lit, { rows: 6, seed, fuzz: false }); g.restore();
    g.fillStyle = '#23203a'; g.beginPath(); g.ellipse(0, o - R * .4, R * 1.06, R * .13, 0, 0, 6.29); g.fill();
    g.fillStyle = 'rgba(255,255,255,.18)'; g.beginPath(); g.ellipse(lit * R * .3, o - R * .44, R * .5, R * .035, 0, 0, 6.29); g.fill();
    if (L.badge !== false) { g.fillStyle = L.badge || '#f2c23a'; g.strokeStyle = PLUM; g.lineWidth = 3; g.beginPath(); g.arc(0, o - R * .7, R * .11, 0, 6.29); g.fill(); g.stroke(); glint(g, -R * .03, o - R * .74, R * .03, .7); }
  } else if (kind) {
    toonHat(g, kind, R * 1.9, R * 1.8, L, lit);
  }
}

// ---------- one crochet character card ----------
export class OrguToon extends Toon {
  constructor(look, scene) { super({ height: 1.6, ...look }, scene); this.seed = [...JSON.stringify(look)].reduce((a, ch) => (a * 31 + ch.charCodeAt(0)) % 99991, 7); }
  shoulder(side) { return this.toWorld(side * 22, this.shY ?? 380); }
  draw(p = {}) {
    const key = JSON.stringify(p, (k, v) => typeof v === 'number' ? Math.round(v * 40) / 40 : v);
    if (key === this.key) return; this.key = key;
    const g = this.g, L = this.look, S = this.seed, lit = p.lit ?? -1;
    const exprName = ALIAS[p.expr] || p.expr || 'neutral';
    g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, CW * RES, CH * RES); g.setTransform(RES, 0, 0, RES, 0, TOP * RES);
    const cx = CW / 2, R = L.headR || 150, yarn = L.yarn || '#e8b440', headC = L.head || yarn;
    g.translate(cx, SOLE); if (p.flip) g.scale(-1, 1); g.rotate((p.lean || 0) * D2R);
    const sq = clamp(p.squash || 0, -.25, .25); g.scale(1 + sq * .6, 1 - sq); g.translate(-cx, -SOLE);
    const bob = p.bob || 0, hy = 84 + R + bob, neck = hy + R * .78, hip = 650 + bob * .5;
    const fat = !!L.fat, lw = L.limbW || (fat ? 68 : 54), tw = L.bodyW || 62;
    // legs: a real step cycle when walk (phase) is given; feet are yarn balls
    const wph = p.walk, legs = [];
    for (const s of [-1, 1]) {
      const sw = wph == null ? 0 : Math.sin(wph + (s > 0 ? Math.PI : 0)), lift = wph == null ? 0 : Math.max(0, Math.cos(wph + (s > 0 ? Math.PI : 0))) * 34;
      const spread = fat ? 82 : 56, fx = cx + s * spread + sw * 70, fy = SOLE - 30 - lift;
      legs.push([[cx + s * (fat ? 46 : 16), hip - 10], [cx + s * (spread + 6) + sw * 30, (hip + SOLE) / 2 + 6 - lift * .6], [fx, fy], s]);
    }
    for (const [a, b, c2] of legs) under(g, () => { g.strokeStyle = PLUM; g.lineWidth = lw; g.lineCap = 'round'; g.beginPath(); g.moveTo(...a); g.quadraticCurveTo(...b, ...c2); g.stroke(); }, lit);
    legs.forEach(([a, b, c2, s], i) => { yarnTube(g, a, b, c2, lw, yarn, lit, S + i); yarnBall(g, c2[0] + s * 14, c2[1] + 8, 36, 25, shade(yarn, .88), lit, { rows: 5, seed: S + 5 + i }); });
    // body: a yarn tube (the channel's figures) or a round tummy (the boss)
    const shY = neck + 34;
    if (L.belly || fat) {
      const jig = 1 + (p.jiggle || 0) * .035 * Math.sin((p.jiggleT || 0) * 26);
      const by = (neck + hip) / 2 + (fat ? 40 : 26), rx = (L.belly > 1 ? L.belly : fat ? 168 : 112) / jig, ry = (hip - neck) * (fat ? .66 : .56) * jig;
      under(g, () => { g.fillStyle = PLUM; g.beginPath(); g.ellipse(cx, by, rx, ry, 0, 0, 6.29); g.fill(); }, lit);
      yarnBall(g, cx, by, rx, ry, L.cloth || yarn, lit, { seed: S + 11 });
      rimLight(g, () => { g.beginPath(); g.ellipse(cx, by, rx, ry, 0, 0, 6.29); }, { cx, cy: by, w: rx * 2, h: ry * 2 }, p.rim, lit);
    } else {
      under(g, () => { g.strokeStyle = PLUM; g.lineWidth = tw; g.lineCap = 'round'; g.beginPath(); g.moveTo(cx, neck - 10); g.lineTo(cx, hip); g.stroke(); }, lit);
      yarnTube(g, [cx, neck - 10], [cx + 2, (neck + hip) / 2], [cx, hip], tw, L.cloth || yarn, lit, S + 12);
    }
    if (L.buttons) for (let k = 0; k < 3; k++) {
      const y = neck + 70 + k * 62, x = cx + (L.belly || fat ? 8 : 2);
      g.fillStyle = L.buttons; g.beginPath(); g.arc(x, y, 11, 0, 6.29); g.fill(); g.strokeStyle = shade(L.buttons, .55); g.lineWidth = 2.5; g.stroke();
      g.fillStyle = shade(L.buttons, .5); for (const [dx, dy] of [[-3.5, -3.5], [3.5, -3.5], [-3.5, 3.5], [3.5, 3.5]]) { g.beginPath(); g.arc(x + dx, y + dy, 1.8, 0, 6.29); g.fill(); }
    }
    if (L.tie) {                                           // a felt tie: knot + blade
      const ty = neck + 8, c = L.tie;
      g.fillStyle = c; g.strokeStyle = shade(c, .55); g.lineWidth = 3;
      g.beginPath(); g.moveTo(cx - 12, ty + 22); g.lineTo(cx + 12, ty + 22); g.lineTo(cx + 22, ty + 150); g.lineTo(cx, ty + 176); g.lineTo(cx - 22, ty + 150); g.closePath(); g.fill(); g.stroke();
      g.beginPath(); g.roundRect(cx - 16, ty, 32, 26, 8); g.fillStyle = shade(c, 1.12); g.fill(); g.stroke();
      g.save(); g.strokeStyle = shade(c, 1.4); g.lineWidth = 3; g.setLineDash([5, 6]); g.beginPath(); g.moveTo(cx, ty + 30); g.lineTo(cx, ty + 160); g.stroke(); g.restore();
    }
    // arms (over the body, under the head): same angles as Toon (upper from straight down, + = away; then the bend)
    const arms = {}, aW = lw * .9;
    for (const [side, a, no, prop] of [[-1, p.armL || [14, 8], p.noArmL, p.propL], [1, p.armR || [14, 8], p.noArmR, p.propR]]) {
      if (no) { arms[side] = null; continue; }
      const x0 = cx + side * (fat ? 118 : 20), y0 = shY + (fat ? 40 : 0), l1 = fat ? 112 : 128, l2 = fat ? 104 : 118;
      const x1 = x0 + Math.sin(a[0] * D2R) * l1 * side, y1 = y0 + Math.cos(a[0] * D2R) * l1;
      const x2 = x1 + Math.sin((a[0] + a[1]) * D2R) * l2 * side, y2 = y1 + Math.cos((a[0] + a[1]) * D2R) * l2;
      arms[side] = [[x0, y0], [x1, y1], [x2, y2], prop];
    }
    for (const [side, A] of Object.entries(arms)) if (A) under(g, () => { g.strokeStyle = PLUM; g.lineWidth = aW; g.lineCap = 'round'; g.beginPath(); g.moveTo(...A[0]); g.quadraticCurveTo(...A[1], ...A[2]); g.stroke(); }, lit, .8);
    for (const [side, A] of Object.entries(arms)) {
      if (!A) continue; const s = +side;
      yarnTube(g, A[0], A[1], A[2], aW, L.sleeve || yarn, lit, S + 20 + s);
      if (A[3] && TOON_PROPS[A[3]]) TOON_PROPS[A[3]](g, A[2][0], A[2][1], s, p);
      yarnBall(g, A[2][0], A[2][1], 28, 28, shade(yarn, 1.06), lit, { rows: 5, seed: S + 30 + s });
    }
    this.hands = { L: arms[-1] ? [arms[-1][2][0], arms[-1][2][1]] : null, R: arms[1] ? [arms[1][2][0], arms[1][2][1]] : null }; this.shY = shY;
    if (L.scarf) {
      const c = L.scarf;
      yarnTube(g, [cx - R * .46, neck + 4], [cx, neck + 38], [cx + R * .46, neck + 4], 40, c, lit, S + 40);
      yarnTube(g, [cx + R * .3, neck + 26], [cx + R * .48, neck + 100], [cx + R * .36, neck + 160], 34, c, lit, S + 41);
    }
    // head
    g.save(); g.translate(cx, hy); g.rotate((p.tilt || 0) * D2R);
    const turn = clamp(p.look || 0, -1, 1), H = L.hair || null;
    if (H) hairBack(g, R, H, lit, turn);
    under(g, () => { g.fillStyle = PLUM; g.beginPath(); g.arc(0, 0, R, 0, 6.29); g.fill(); }, lit, 1.1);
    yarnBall(g, 0, 0, R, R * .97, headC, lit, { spin: -turn * .42, seed: S + 50 });
    rimLight(g, () => { g.beginPath(); g.arc(0, 0, R * .985, 0, 6.29); }, { cx: 0, cy: 0, w: R * 2, h: R * 2 }, p.rim, lit);
    if (L.antenna) for (const s of [-1, 1]) {
      const sw = Math.sin((p.antT || 0) * 5 + s) * 8;
      yarnTube(g, [s * R * .32, -R * .82], [s * R * .42 + sw * .3, -R * 1.25], [s * R * .62 + sw, -R * 1.5], 22, shade(headC, .9), lit, S + 80 + s);
      yarnBall(g, s * R * .64 + sw, -R * 1.56, 30, 30, L.antenna, lit, { rows: 5, seed: S + 82 + s });
    }
    if (L.beard) toonBeard(g, R * 1.9, R * 1.8, L, lit);
    if (H) hairFront(g, R, H, lit, turn, S + 60);
    if (L.hat) hat(g, R, L, lit, S + 70);
    face(g, R * 2.25, R * 2.05, { ...p, __head: headC, lit }, L, exprName);
    if (p.sweat) { g.globalAlpha = Math.min(1, p.sweat); g.fillStyle = '#9fd4ff'; g.strokeStyle = PLUM; g.lineWidth = 5; g.beginPath(); g.moveTo(R * .8, -R * .55); g.quadraticCurveTo(R * 1.05, -R * .15, R * .86, -R * .08); g.quadraticCurveTo(R * .64, -R * .15, R * .8, -R * .55); g.fill(); g.stroke(); glint(g, R * .82, -R * .2, 4, .8); g.globalAlpha = 1; }
    if (p.laughMarks) { g.strokeStyle = PLUM; g.lineWidth = 6; g.lineCap = 'round'; g.globalAlpha = p.laughMarks; for (const s of [-1, 1]) for (let k = 0; k < 3; k++) { const a = (-40 + k * 25) * D2R; g.beginPath(); g.moveTo(s * (R * 1.1 + 8), -R * .16 + Math.sin(a) * 64); g.lineTo(s * (R * 1.1 + 40), -R * .16 + Math.sin(a) * 86); g.stroke(); } g.globalAlpha = 1; }
    g.restore();
    this.tex.needsUpdate = true;
  }
}
