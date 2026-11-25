// dizi.js: dizivanastudio's 2D layer, drawn over every frame from story.overlay(g, t, ctx):
// the hook text (first 2 s), the series tag, the subscribe band, title / end cards. All sizes follow the frame
// (vertical 1080x1920 or horizontal 1920x1080). Call `await hazirla()` once in story.setup (fonts and logo).
export { kancaYazisi } from './kanca.js';

const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const seg = (t, a, b) => b > a ? clamp((t - a) / (b - a)) : +(t >= a);
const smooth = u => { u = clamp(u); return u * u * (3 - 2 * u); };
const lerp = (a, b, u) => a + (b - a) * u;
export const FONT = '"Poppins", "Segoe UI Black", "Arial Black", sans-serif';
const CREAM = '#faf6ea', INK = '#1e1a3c', NAVY = 'rgba(30,36,78,.98)', DASH = 'rgba(206,214,246,.86)', YEL = '#ffd23f';

const logo = new Image();
export async function hazirla() {
  logo.src = '/lib/logo.webp';
  const faces = [new FontFace('Poppins', 'url(/lib/fonts/Poppins-Bold.ttf)', { weight: '700' }), new FontFace('Poppins', 'url(/lib/fonts/Poppins-Medium.ttf)', { weight: '500' })];
  for (const f of faces) { try { await f.load(); document.fonts.add(f); } catch (e) { } }
  try { await logo.decode(); } catch (e) { }
}
const U = (W, H) => Math.min(W, H) / 1080;          // 1 in vertical, 1 in horizontal (short side is 1080)

// series tag: "KİRACI UZAYLI · 1. BÖLÜM" (vertical: top centre; horizontal: top left)
export function etiket(g, W, H, text, a = 1) {
  if (a <= 0) return;
  const land = W > H, u = U(W, H), fs = (land ? 28 : 34) * u;
  g.save(); g.globalAlpha = a; g.font = `700 ${fs}px ${FONT}`; g.textBaseline = 'middle'; g.textAlign = 'center';
  const w = g.measureText(text).width, h = fs * 1.9, x = land ? 60 * u + (w + 56 * u) / 2 : W / 2, y = land ? 44 * u : 150 * u;
  g.fillStyle = 'rgba(250,246,234,.93)'; g.beginPath(); g.roundRect(x - w / 2 - 28 * u, y, w + 56 * u, h, h / 2); g.fill();
  g.fillStyle = INK; g.fillText(text, x, y + h * .52); g.restore();
}

// centre card: lines = [[text, size, colour]] (title card, end card, "Bir sonraki bölüm" card)
export function kart(g, W, H, lines, a = 1, { cy = null, sc = 1 } = {}) {
  if (a <= 0) return;
  const land = W > H, u = U(W, H) * (land ? .86 : 1) * sc;
  g.save(); g.globalAlpha = a; g.textAlign = 'center'; g.textBaseline = 'alphabetic';
  let ww = 0; for (const [tx, sz] of lines) { g.font = `700 ${sz * u}px ${FONT}`; ww = Math.max(ww, g.measureText(tx).width); }
  ww += 150 * u; const hh = lines.reduce((s, [, sz]) => s + sz * 1.35, 0) * u + 120 * u;
  const cx = W / 2; cy = cy ?? H * (land ? .45 : .42);
  g.shadowColor = 'rgba(4,6,20,.5)'; g.shadowBlur = 28 * u; g.shadowOffsetY = 16 * u;
  g.fillStyle = NAVY; g.beginPath(); g.roundRect(cx - ww / 2, cy - hh / 2, ww, hh, 34 * u); g.fill(); g.shadowColor = 'transparent';
  g.strokeStyle = DASH; g.lineWidth = 4 * u; g.setLineDash([16 * u, 12 * u]); g.beginPath(); g.roundRect(cx - ww / 2 + 18 * u, cy - hh / 2 + 18 * u, ww - 36 * u, hh - 36 * u, 22 * u); g.stroke(); g.setLineDash([]);
  let y = cy - hh / 2 + 60 * u;
  for (const [tx, sz, col] of lines) { y += sz * u; g.font = `700 ${sz * u}px ${FONT}`; g.fillStyle = col || CREAM; g.fillText(tx, cx, y); y += sz * .35 * u; }
  g.restore();
}
// a card that pops in and fades out: t inside [t0, t1]
export function kartAc(g, t, t0, t1, W, H, lines, opts = {}) {
  if (t < t0 || t > t1) return;
  const a = Math.min(smooth(seg(t, t0, t0 + .25)), 1 - smooth(seg(t, t1 - .3, t1)));
  const pop = 1 + .06 * (1 - smooth(seg(t, t0, t0 + .3)));
  kart(g, W, H, lines, a, { ...opts, sc: (opts.sc || 1) * pop });
}

// subscribe band (4.6 s): channel logo + name, red "ABONE OL" button; a cursor clicks it, it turns into "ABONE OLUNDU", the bell rings.
// Mix plan: a 'tick' at t0 + 2.3 and a short 'chime' at t0 + 2.45 (senaryo.mix_plan).
export const ABONE_DUR = 4.6;
export function abone(g, t, t0, W, H, pos = null) {
  const d = t - t0; if (d < 0 || d > ABONE_DUR) return;
  const land = W > H, u = U(W, H) * (land ? .78 : 1);
  const bw = 880 * u, bh = 150 * u;
  let [cx, cy] = pos || (land ? [56 * U(W, H) + bw / 2, 196 * U(W, H)] : [W / 2, 318 * U(W, H)]);
  const a = Math.min(smooth(seg(d, 0, .4)), 1 - smooth(seg(d, ABONE_DUR - .4, ABONE_DUR)));
  cy -= (1 - a) * 60 * u;
  g.save(); g.globalAlpha = a;
  g.shadowColor = 'rgba(4,6,20,.5)'; g.shadowBlur = 24 * u; g.shadowOffsetX = 8 * u; g.shadowOffsetY = 13 * u;
  g.fillStyle = 'rgb(30,36,78)'; g.beginPath(); g.roundRect(cx - bw / 2, cy - bh / 2, bw, bh, bh / 2); g.fill();
  g.shadowColor = 'transparent';
  g.strokeStyle = DASH; g.lineWidth = 3.5 * u; g.setLineDash([14 * u, 10 * u]); g.beginPath(); g.roundRect(cx - bw / 2 + 10 * u, cy - bh / 2 + 10 * u, bw - 20 * u, bh - 20 * u, bh / 2 - 10 * u); g.stroke(); g.setLineDash([]);
  const lr = bh * .4, lx = cx - bw / 2 + bh * .5;
  g.save(); g.beginPath(); g.arc(lx, cy, lr, 0, 6.29); g.clip();
  if (logo.complete && logo.naturalWidth) g.drawImage(logo, lx - lr * 1.02, cy - lr * 1.02, lr * 2.04, lr * 2.04); else { g.fillStyle = '#e9b446'; g.fill(); }
  g.restore(); g.strokeStyle = CREAM; g.lineWidth = 4 * u; g.beginPath(); g.arc(lx, cy, lr, 0, 6.29); g.stroke();
  const tx = lx + lr + 22 * u; g.textAlign = 'left'; g.textBaseline = 'alphabetic';
  g.font = `700 ${42 * u}px ${FONT}`; g.fillStyle = CREAM; g.fillText('dizivanastudio', tx, cy - 4 * u);
  g.font = `500 ${25 * u}px ${FONT}`; g.fillStyle = '#b0bee8'; g.fillText('Her gün yeni bölüm', tx, cy + 36 * u);
  const clicked = d >= 2.4, sc = 1 + .05 * Math.sin(clamp((d - .6) / .8) * Math.PI) - .09 * Math.sin(clamp((d - 2.2) / .3) * Math.PI);
  const bwid = 292 * u * sc, bhg = 80 * u * sc, bx = cx + bw / 2 - 26 * u - 146 * u;
  g.fillStyle = 'rgba(4,6,20,.43)'; g.beginPath(); g.roundRect(bx - bwid / 2, cy - bhg / 2 + 5 * u, bwid, bhg, bhg / 2); g.fill();
  g.fillStyle = clicked ? '#606680' : '#e43234'; g.beginPath(); g.roundRect(bx - bwid / 2, cy - bhg / 2, bwid, bhg, bhg / 2); g.fill();
  g.textAlign = 'center'; g.fillStyle = '#faf8f0';
  if (clicked) {
    g.font = `700 ${25 * u * sc}px ${FONT}`; g.fillText('ABONE OLUNDU', bx + 16 * u, cy + 10 * u);
    const ang = .38 * Math.sin((d - 2.4) * 24) * Math.exp(-(d - 2.4) * 2.4), s = u * 1.05;
    g.save(); g.translate(bx - 114 * u, cy - 14 * u); g.rotate(ang); g.fillStyle = YEL;
    g.beginPath(); g.moveTo(-13 * s, 24 * s); g.quadraticCurveTo(-11 * s, 2 * s, 0, 0); g.quadraticCurveTo(11 * s, 2 * s, 13 * s, 24 * s); g.lineTo(17 * s, 29 * s); g.lineTo(-17 * s, 29 * s); g.closePath(); g.fill();
    g.beginPath(); g.arc(0, 33 * s, 4.5 * s, 0, 6.29); g.fill(); g.beginPath(); g.arc(0, -2 * s, 3 * s, 0, 6.29); g.fill(); g.restore();
  } else { g.font = `700 ${33 * u * sc}px ${FONT}`; g.fillText('ABONE OL', bx, cy + 12 * u); }
  const mv = smooth(seg(d, 1.3, 2.15)), away = smooth(seg(d, 2.9, 3.5));
  const px = lerp(bx + 250 * u, bx + 46 * u, mv) + 120 * u * away, py = lerp(cy + 200 * u, cy + 10 * u, mv) + 130 * u * away;
  const ca = Math.min(seg(d, 1.2, 1.5), 1 - seg(d, 3.2, 3.5));
  if (ca > 0) {
    g.globalAlpha = a * ca;
    if (d >= 2.25 && d < 2.6) { g.strokeStyle = YEL; g.lineWidth = 5 * u; for (const an of [-150, -105, -60]) { const x = Math.cos(an * Math.PI / 180), y = Math.sin(an * Math.PI / 180); g.beginPath(); g.moveTo(px + x * 22 * u, py + y * 22 * u); g.lineTo(px + x * 40 * u, py + y * 40 * u); g.stroke(); } }
    const k = u * (1.25 - .14 * Math.sin(clamp((d - 2.2) / .3) * Math.PI)), P = [[0, 46], [12, 36], [21, 56], [30, 52], [21, 33], [36, 33]];
    g.beginPath(); g.moveTo(px, py); for (const [qx, qy] of P) g.lineTo(px + qx * k, py + qy * k); g.closePath();
    g.fillStyle = '#ffffff'; g.fill(); g.strokeStyle = '#141834'; g.lineWidth = 4 * u; g.stroke();
  }
  g.restore();
}
