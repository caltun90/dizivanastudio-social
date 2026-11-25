// Kiracı Uzaylı, 0. bölüm: DENEME (yayınlanmaz). KOMEDI.md'nin "Karnım zil çalıyor" bloğu.
// Yeni bölümün story.js dosyası bu iskeletle yazılır:
//   1) zaman: replik ve vuruş saatleri Z.S('h1'), Z.E('t1'), Z.B('zil1'), Z.SC(3); hiçbir saniye elle yazılmaz
//   2) kamera: CamPath anahtarları O.plan / O.yakin / O.ikili ile, sahne, replik ve vuruş başlarına bağlı
//   3) frame(): her oyuncu O.oyna(K, ad, yer, cam, { ...O.canli(Z, ad, t), ifade ve poz })
//   4) overlay(): kanca yazısı (ilk 2 sn), dizi etiketi, kılavuz kartı, kapanış kartı
// Komik zamanlama araçları: çifte bakış (bak, dön, hızla geri bak + boing), donma, vuruştan önce sessiz bakış, tepki yakın planı.
import { CamPath } from '/engine/src/camera.js';
import * as O from '/diziler/uzayli/ortak.js';
export { TOON, LOOK } from '/diziler/uzayli/ortak.js';

export const NAME = 'uzayli-b00';
export const FPS = 30;
export let DUR = 10;
export const CUES = [];
export const CAPTION = { colors: O.COLORS, names: O.NAMES, font: O.FONT };
let K, Z, cp;

// yerler (ev seti)
const TOBI = [-2.55, 0, -.75], ZIP = [-1.6, 0, -.7], ZIP_ARKA = [-2.5, 0, -1.3], ZIP_KOS = [-2.3, 0, .35];
const KAPIDA = [-3.6, 0, .95], HUGO_KAPI = [-3.95, 0, .5], HUGO_IC = [-3.3, 0, -.85];
const clamp01 = x => Math.max(0, Math.min(1, x));
const dec = (t, t0, k = 4) => t < t0 ? 0 : Math.exp(-(t - t0) * k);          // vuruştan sonra sönen etki

export async function setup(ctx) {
  K = await O.kur(ctx); Z = O.zaman(ctx); DUR = O.sure(ctx);
  const { S, E, SC, B } = Z;
  const ikili = (o = {}) => O.ikili('ev', [TOBI[0] - .45, 0, TOBI[2]], ZIP, ctx, { uzak: 3.4, h: 1.3, ...o });
  cp = new CamPath([
    // 1 Tobi boş paketle; karın zil çalar
    { t: 0, ...ikili(), creep: .35 },
    { t: S('z1') - .02, move: 'whip', dur: .25, ...O.yakin('ev', ZIP, ctx, { h: 1.05, uzak: 2.3, yan: .3 }), creep: .5 },
    // 2 Zip kapıya koşar, boş koridor, "Kimse yok."
    { t: SC(2), move: 'cut', ...O.plan('ev.kapi', ctx), creep: .2 },
    { t: S('z2'), move: 'cut', ...O.yakin('ev', KAPIDA, ctx, { h: 1.05, uzak: 2.3, yan: .9 }), creep: .3 },
    // 3 açıklama, yeni kural, karın yine, göbeğe konuşma
    { t: SC(3), move: 'cut', ...ikili(), creep: .25 },
    { t: S('z3'), move: 'whip', dur: .25, ...O.yakin('ev', ZIP, ctx, { h: 1.05, uzak: 2.6, yan: .25 }), creep: .3 },
    { t: B('zil2')[0], move: 'cut', ...ikili({ uzak: 3.0 }), creep: .45 },
    { t: B('bakis')[0], move: 'cut', ...O.yakin('ev', TOBI, ctx, { h: 1.35, uzak: 2.4, yan: -.25 }), creep: .5 },
    { t: B('zil3')[0], move: 'cut', ...ikili({ uzak: 3.0 }), creep: .3 },
    { t: S('t4'), move: 'cut', ...O.yakin('ev', TOBI, ctx, { h: 1.35, uzak: 2.5, yan: .3 }), creep: .3 },
    { t: B('donma')[0] + .2, move: 'cut', ...ikili({ uzak: 3.4 }), creep: .7 },
    // 4 önce burun: kadrajı Hugo'nun burnu doldurur, sonra geri açılır
    { t: SC(4), move: 'cut', ...O.yakin('ev', HUGO_KAPI, ctx, { h: 1.5, uzak: 1.15, yan: .35, fov: 34 }), creep: .6 },
    { t: S('h1') - .1, move: 'cut', ...O.yakin('ev', HUGO_KAPI, ctx, { h: 1.45, uzak: 3.0, yan: .9 }), creep: .3 },
    { t: B('sakla')[0], move: 'cut', ...ikili({ uzak: 3.2 }), creep: .2 },
    { t: S('h2') - .1, move: 'cut', ...O.yakin('ev', HUGO_IC, ctx, { h: 1.45, uzak: 3.0, yan: .5 }), creep: .3 },
    { t: S('t5'), move: 'cut', ...O.yakin('ev', TOBI, ctx, { h: 1.4, uzak: 2.9, yan: -.2 }), creep: .3 },
    { t: S('h3'), move: 'cut', ...O.yakin('ev', HUGO_IC, ctx, { h: 1.45, uzak: 2.5, yan: .4 }), creep: .4 },
    { t: S('t6'), move: 'cut', ...O.yakin('ev', TOBI, ctx, { h: 1.5, uzak: 3.1, yan: -.2 }), creep: .25 },
    { t: S('h4'), move: 'cut', ...O.yakin('ev', HUGO_IC, ctx, { h: 1.45, uzak: 2.6, yan: .45 }), creep: .2 },
    { t: B('kapat')[0], move: 'cut', ...O.plan('ev.kapi', ctx), creep: .2 },
    // düğme
    { t: B('zil4')[0], move: 'cut', ...ikili({ uzak: 3.2 }), creep: .3 },
    { t: S('z6'), move: 'whip', dur: .25, ...O.yakin('ev', [-2.25, 0, -1.2], ctx, { h: 1.1, uzak: 2.6, yan: .3 }), creep: .4 },
  ], { fps: FPS });
  cp.kick(B('zil1')[0] + .05, .6).kick(B('zil1')[0] + .55, .8).kick(B('kos1')[0] + .9, .6).kick(B('zil2')[0] + .05, .5)
    .kick(B('zil3')[0] + .05, 1.0).kick(B('donma')[0] + .1, .5).kick(B('sakla')[0] + .1, .9).kick(B('anten')[0] + .95, .5).kick(B('zil4')[0] + .05, .5);
}

export function frame(t, ctx) {
  const { cam } = ctx, { S, E, B, SC, on } = Z;
  const c = cp.apply(cam, t);
  O.mekan(K, O.mekanOf(cam));
  const zil = n => B('zil' + n)[0];
  // kapı: koşuda açılır, sahne 3'te kapalı, Hugo'yla açık, "kapat" vuruşunda kapanır
  O.kapi(K, t < B('kos1')[0] + .8 ? 0 : t < SC(3) ? O.backOut(clamp01((t - B('kos1')[0] - .8) / .35))
    : t < SC(4) ? 0 : t < B('kapat')[0] + .45 ? 1 : .8 * (1 - clamp01((t - B('kapat')[0] - .45) / .4)));

  // ---- TOBİ
  const belly = Math.max(dec(t, zil(1), 3), dec(t, zil(2), 3), dec(t, zil(4), 3)) * 7;
  const tp = { ...O.canli(Z, 'tobi', t), jiggle: .6 + belly, expr: 'neutral', look: .55, lid: .15, propR: 'cips', armR: [40, 70] };
  if (t < zil(1)) Object.assign(tp, { expr: 'worried', lookY: .7, look: .2 });                                 // boş pakete bakar
  else if (t < SC(2)) Object.assign(tp, { expr: 'surprised', lookY: .9, look: .1 });                            // karnına bakar
  else if (t < zil(2)) Object.assign(tp, { look: .7 });
  else if (t < B('bakis')[0]) Object.assign(tp, { expr: 'worried', lookY: .8, look: .1 });
  else if (t < zil(3)) Object.assign(tp, { look: .55, lookY: .55, lid: .45, expr: on('t3', t) ? 'neutral' : 'neutral' });   // yavaş, kabullenmiş bakış
  else if (t < B('donma')[0]) Object.assign(tp, { look: .55, lookY: .5, lid: .35 });
  else if (t < SC(4)) Object.assign(tp, { expr: 'surprised', look: t > B('donma')[0] + .55 ? -1 : .4, lookY: 0, sweat: t > B('donma')[0] + .55 ? 1 : 0, blink: 0 });
  else if (t < S('t5')) Object.assign(tp, { look: -.9, lid: .25 });
  else if (t < B('anten')[0] + .75) Object.assign(tp, { look: -.8, lid: .35, armR: on('t5', t) || on('h3', t) ? [80, 30] : [40, 70] });
  else if (t < B('zil4')[0]) Object.assign(tp, { look: -.8, lid: .5, squash: -.22 * O.ramp(t, B('anten')[0] + .75, B('anten')[0] + 1.0) });   // bakmadan uzayıp antenleri kafasıyla ezer
  else Object.assign(tp, { look: .2, lookY: .85, lid: .5, expr: 'worried', armR: [16, 8] });
  if (t > S('t6') && t < E('t6') + .4) tp.mouth = Math.max(tp.mouth || 0, .25 + .25 * Math.sin(t * 22));             // çiğner
  O.oyna(K, 'tobi', TOBI, cam, tp);

  // ---- ZİP
  if (t < SC(4) || t >= B('sakla')[0]) {
    let pos = ZIP, zp = { ...O.canli(Z, 'zip', t), expr: 'happy', look: -.6 };
    if (t < zil(1) + .5) Object.assign(zp, { look: -.4, lookY: .2 });
    else if (t < SC(2)) {                                                                           // çifte bakış: göbeğe, öne, hızla göbeğe
      const u = t - zil(1) - .5, snap = u > .45;
      Object.assign(zp, { expr: snap ? 'surprised' : 'neutral', look: u < .2 ? -.8 : u < .45 ? 0 : -.9, lookY: u < .2 ? .6 : u < .45 ? 0 : .5,
        antUp: dec(t, zil(1) + .95, 2.2) * 1.2 + (snap ? .3 : 0), antWob: dec(t, zil(1) + .95, 1.8), squash: snap ? -.15 * dec(t, zil(1) + .95, 6) : 0 });
      if (on('z1', t) || t > S('z1')) Object.assign(zp, { expr: 'grin', look: -.3, lookY: 0, armR: [150, 20], antUp: .6, antWob: .6 });
    } else if (t < SC(3)) {                                                                         // koşu ve kapı
      const w = O.yuru(t, B('kos1')[0], B('kos1')[0] + .8, ZIP_KOS, KAPIDA, { adim: 3.2 });
      pos = w.pos; Object.assign(zp, { walk: w.walk, flip: true, lean: w.moving ? 14 : 0, expr: 'grin', look: -.6, armR: t > B('kos1')[0] + .7 ? [70, 40] : [40, 60] });
      if (t > B('bos1')[0]) Object.assign(zp, { expr: 'surprised', armR: [70, 40], blink: 0, antUp: -.2 });
      if (t > S('z2') - .1) Object.assign(zp, { flip: false, expr: 'neutral', lid: .45, look: .35, armR: [16, 8], antUp: -.35 });
    } else if (t < zil(2)) {
      Object.assign(zp, { look: -.6, expr: on('t2', t) ? 'focused' : 'proud' });
      if (t > S('z3') - .2) Object.assign(zp, { propL: 'kilavuz', propR: 'pen', armL: [50, 60], armR: [55, 60], lookY: .55, look: -.1, expr: 'focused', tilt: Math.sin(t * 9) * 4 });
    } else if (t < B('bakis')[0]) {                                                                 // kapıya çekilir, direnir, göbeğe döner
      const u = t - zil(2);
      if (u < .85) Object.assign(zp, { expr: 'worried', look: -1, lean: -14 * clamp01(u / .5), tilt: Math.sin(t * 40) * 3, sweat: 1, antWob: .5 });
      else { pos = [ZIP[0] - .15, 0, ZIP[2]]; Object.assign(zp, { expr: on('z4', t) ? 'angry' : 'focused', look: -.8, lookY: .5, lean: -8, armL: [70, 40], armR: [70, 40] }); }
    } else if (t < zil(3)) Object.assign(zp, { expr: 'neutral', look: -.6, lid: .3, antUp: -.1 });
    else if (t < B('donma')[0]) { pos = [ZIP[0] - .15, 0, ZIP[2]]; Object.assign(zp, { expr: on('t4', t) ? 'neutral' : 'angry', look: -.8, lookY: .5, lean: -8, armR: on('z5', t) ? [150, 25] : [16, 8], blink: on('t4', t) ? 0 : zp.blink }); }
    else if (t < SC(4)) Object.assign(zp, { expr: 'surprised', look: t > B('donma')[0] + .55 ? -1 : -.5, blink: 0, sweat: 1, antUp: t > B('donma')[0] + .55 ? .4 : 0 });
    else {                                                                                          // saklanma ve anten
      const u = clamp01((t - B('sakla')[0]) / .22); pos = [ZIP[0] + (ZIP_ARKA[0] - ZIP[0]) * u, 0, ZIP[2] + (ZIP_ARKA[2] - ZIP[2]) * u];
      Object.assign(zp, { expr: 'worried', look: -.4, lean: u < 1 ? -20 : 0, squash: u > 0 && u < 1 ? -.2 : 0, antUp: -.3 });
      const ra = clamp01((t - B('anten')[0] - .05) / .55);                                          // antenler Tobi'nin başının üstünden yükselir
      const bas = clamp01((t - B('anten')[0] - 1.0) / .12);                                         // Tobi'nin eli bastırır: antenler ve Zip geri iner
      if (t > B('anten')[0] && t < B('zil4')[0]) { pos = [pos[0], .18 * ra * (1 - bas), pos[2]];
        Object.assign(zp, { antUp: (-.3 + 1.3 * ra) * (1 - bas) - .4 * bas, antWob: .4 * dec(t, B('anten')[0] + .5, 2) + .8 * dec(t, B('anten')[0] + 1.1, 3), squash: .2 * dec(t, B('anten')[0] + 1.1, 6) }); }
      if (t > B('zil4')[0] + .5) { const p2 = clamp01((t - B('zil4')[0] - .5) / .3); pos = [ZIP_ARKA[0] + .5 * p2, 0, ZIP_ARKA[2]];   // kenardan çıkar, gözler sıkı kapalı
        Object.assign(zp, { expr: on('z6', t) ? 'worried' : 'neutral', blink: 1, look: .6, antUp: -.4, tilt: -6 }); }
    }
    O.oyna(K, 'zip', pos, cam, zp);
  }

  // ---- HUGO
  if (t >= SC(4) && t < B('kapat')[0]) {
    let pos = HUGO_KAPI, hp = { ...O.canli(Z, 'hugo', t), expr: 'smug', look: .7, sniff: 0, brow: .3 };
    if (t < S('h1')) Object.assign(hp, { sniff: 1, expr: 'focused', lid: .45, look: .3, lookY: -.1, tilt: Math.sin(t * 7) * 2 });
    else if (t < B('sakla')[0] + .8) Object.assign(hp, { expr: 'smug', brow: .6, armR: on('h1', t) ? [120, 50] : [16, 8] });
    if (t > S('h2') - .7) {
      const w = O.yuru(t, S('h2') - .7, S('h2') + .9, HUGO_KAPI, HUGO_IC); pos = w.pos;
      Object.assign(hp, { walk: w.walk, lean: w.moving ? 6 : 0, sniff: on('h2', t) || w.moving ? 1 : 0, expr: 'focused', lid: .4, look: .8 });
    }
    if (t > S('h3') - .1) Object.assign(hp, { expr: 'smug', brow: .9, lid: .3, sniff: 0, look: .9 });
    if (t > B('anten')[0] + .3) Object.assign(hp, { expr: 'angry', lid: .55, brow: 0, look: .9, sniff: .6 });
    if (t > S('h4')) {                                                                              // geri geri çıkar, gözü Tobi'de
      const w = O.yuru(t, E('h4') - .7, E('h4') + .5, HUGO_IC, [HUGO_KAPI[0] - .3, 0, HUGO_KAPI[2]]); pos = w.pos;
      Object.assign(hp, { walk: w.walk, flip: false, lean: w.moving ? -5 : 0, expr: 'smug', lid: .5, look: .9, sniff: .8 });
    }
    O.oyna(K, 'hugo', pos, cam, hp);
  }
  return O.bak(K, cam, c);
}

export function overlay(g, t, ctx) {
  const { S, E, B } = Z;
  O.ustKatman(g, t, ctx, {
    kanca: 'BU ZİL NEREDEN ÇALIYOR?', bolum: 0,
    kartlar: [
      { t0: S('z3') + .5, t1: E('z3') + .9, cy: ctx.H * .2, lines: [['DÜNYALI KILAVUZU · YENİ KURAL', 34, O.KART.not], ['Zil çalarsa kapıya bakılmaz.', 50, O.KART.alt]] },
      { t0: B('end')[0] + .2, t1: DUR, lines: [['Kiracı Uzaylı', 74, O.KART.baslik], ['Deneme: Karnım Zil Çalıyor', 40, O.KART.alt]] },
    ],
  });
}
