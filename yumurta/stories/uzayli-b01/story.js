// Kiracı Uzaylı, 1. bölüm: Kiralık Oda. Yapı: düz anlatım (kanca -> gündüz: kira, ilan, Zip gelir, çay, bozuk para ->
// "ÜÇ SAAT SONRA" gece: karnım zil çalıyor bloğu -> Hugo -> düğme).
// Yeni görsel fikirler: gündüzden geceye dönen pencere, sehpada bozuk para yığını, KİRALIK ODA ilanı, kılavuz ve sözleşme kartları.
import { CamPath } from '/engine/src/camera.js';
import * as O from '/diziler/uzayli/ortak.js';
export { TOON, LOOK } from '/diziler/uzayli/ortak.js';

export const NAME = 'uzayli-b01';
export const FPS = 30;
export let DUR = 10;
export const CUES = [];
export const CAPTION = { colors: O.COLORS, names: O.NAMES, font: O.FONT };
let K, Z, cp;

// ---- yerler (ev seti)
const LM = [1.55, 0, -.4], TM = [2.55, 0, -.4];                                   // gündüz, masa önü: Luna, Tobi
const LS = [-1.85, 0, .3], LK = [-3.0, 0, .4], TS = [-1.2, 0, -.55], TK = [-2.3, 0, -.3];   // kapıya yürüyüş
const ESIK = [-3.95, 0, .5];                                                      // kapı eşiği (Zip, sonra Hugo)
const Z4 = [-1.75, 0, -.75], L4 = [-.85, 0, -.8], T4 = [-2.7, 0, -.85];           // içeride: çay
const ZS = [-1.4, 0, -1.85], T5 = [-2.6, 0, -1.55], L5 = [-.25, 0, -1.5];         // sehpanın arkası ve iki yanı: bozuk para
const T0 = [-2.15, 0, -.45], Z8 = [-1.2, 0, -.5], ZIP_ARKA = [-2.1, 0, -.9], ZIP_KOS = [-2.3, 0, .35], KAPIDA = [-3.6, 0, .95];   // gece
const HUGO_IC = [-2.95, 0, -.55], L9A = [.6, 0, -.4], L9 = [-.55, 0, -.6];
const clamp01 = x => Math.max(0, Math.min(1, x));
const dec = (t, t0, k = 4) => t < t0 ? 0 : Math.exp(-(t - t0) * k);               // vuruştan sonra sönen etki
const mix3 = (a, b, u) => a.map((v, i) => v + (b[i] - v) * u);

export async function setup(ctx) {
  K = await O.kur(ctx); Z = O.zaman(ctx); DUR = O.sure(ctx);
  const { S, E, SC, B } = Z;
  const Y = (p, o) => O.yakin('ev', p, ctx, o);
  const iki6 = (o = {}) => O.ikili('ev', [T0[0] - .2, 0, T0[2]], ZS, ctx, { uzak: 3.9, h: 1.35, ...o });               // Tobi önde, Zip sehpanın arkasında
  const iki8 = (o = {}) => O.ikili('ev', [T0[0] - .1, 0, T0[2]], Z8, ctx, { uzak: 4.0, h: 1.3, ...o });
  const ikiM = (o = {}) => O.ikili('ev', LM, TM, ctx, { uzak: 3.6, h: 1.4, ...o });
  const iki4 = (o = {}) => O.ikili('ev', Z4, L4, ctx, { uzak: 3.5, h: 1.3, ...o });
  const ikiHT = (o = {}) => O.ikili('ev', HUGO_IC, T0, ctx, { uzak: 3.3, h: 1.25, ...o });
  const L = ctx.LAND ? .8 : 1;
  const SEHPA = { pos: [-1.1, 1.5, 1.0], look: [-1.4, .9, -1.6], fov: 42 * L };                    // Zip sehpanın arkasında, önünde paralar
  const PARA = { pos: [-1.2, 1.5, .25], look: [-1.38, .7, -1.3], fov: 36 * L };                   // yalnızca para yığını
  const PENCERE = { pos: [-1.6, 1.78, -.85], look: [-1.6, 1.74, -3.6], fov: 42 * L };              // pencere: gündüz geceye döner
  const KAPI_L = { pos: [-1.5, 1.5, 2.7], look: [-3.65, 1.1, .45], fov: 54 * L };                  // kapı ve kapıya yürüyen Luna
  const GENIS = { pos: [-1.5, 1.5, 3.3], look: [-1.5, 1.0, -1.6], fov: 50 * L };
  const SON = { pos: [-1.45, 1.35, 3.6], look: [-1.45, ctx.LAND ? 1.55 : 1.3, -1.6], fov: 48 * L };                    // bitiş ve başlık kartı: oyuncular kadrajın alt yarısında                   // salonun bu köşesi, boydan
  cp = new CamPath([
    // 1 KANCA: karın zil çalar, Zip fırlar
    { t: 0, ...iki6({ uzak: 4.3 }), creep: 1.1 },
    { t: S('z0') - .02, move: 'whip', dur: .25, ...Y(ZS, { h: 1.22, uzak: 2.6, yan: .3 }), creep: .5 },
    { t: B('title')[0] + .15, move: 'cut', ...SON, creep: .3 },
    // 2 gündüz, masa: kira yetmiyor
    { t: SC(2), move: 'cut', ...ikiM(), creep: .25 },
    { t: S('t1') - .05, move: 'cut', ...Y(TM, { h: 1.35, uzak: 2.8, yan: -.25 }), creep: .3 },
    { t: B('soguk')[0] + .2, move: 'cut', ...ikiM({ uzak: 3.2 }), creep: .5 },
    { t: S('t2') - .05, move: 'cut', ...Y(TM, { h: 1.35, uzak: 2.4, yan: .3 }), creep: .3 },
    { t: S('l9') - .05, move: 'cut', ...Y(LM, { h: 1.38, uzak: 2.8, yan: .25 }), creep: .3 },
    { t: S('t15') - .05, move: 'cut', ...ikiM({ uzak: 3.4 }), creep: .3 },
    // 3 kapı: ilan, tak tak, Zip
    { t: SC(3), move: 'cut', ...KAPI_L, creep: .2 },
    { t: S('l2') - .1, move: 'cut', ...Y([LK[0] - .28, 0, LK[2]], { h: 1.38, uzak: 2.8, yan: .25 }), creep: .3 },
    { t: B('ac')[0], move: 'cut', ...Y(ESIK, { h: 1.2, uzak: 3.6, yan: 1.1 }), creep: .5 },
    { t: S('z1') - .05, move: 'cut', ...Y(ESIK, { h: 1.25, uzak: 2.5, yan: .8 }), creep: .3 },
    { t: S('l3') - .05, move: 'cut', ...Y(LK, { h: 1.4, uzak: 2.8, yan: .4 }), creep: .3 },
    { t: S('z2') - .05, move: 'cut', ...Y(ESIK, { h: 1.32, uzak: 3.0, yan: .9 }), creep: .3 },
    { t: S('t3') - .05, move: 'cut', ...Y(TK, { h: 1.5, uzak: 2.8, yan: -.3 }), creep: .3 },
    { t: S('z3') - .05, move: 'cut', ...Y(ESIK, { h: 1.32, uzak: 2.6, yan: .7 }), creep: .3 },
    { t: B('antenbak')[0], move: 'cut', ...Y(TK, { h: 1.4, uzak: 2.3, yan: .2 }), creep: .4 },
    { t: B('antenbak')[0] + .6, move: 'cut', ...Y(ESIK, { h: 1.2, uzak: 2.2, yan: .6 }), creep: .4 },
    { t: S('t4') - .05, move: 'cut', ...Y(TK, { h: 1.35, uzak: 2.8, yan: -.2 }), creep: .3 },
    { t: S('z4') - .05, move: 'cut', ...Y(ESIK, { h: 1.25, uzak: 2.7, yan: .8 }), creep: .3 },
    { t: B('gecmis')[0] + .1, move: 'cut', ...Y([LK[0] - .25, 0, LK[2]], { h: 1.42, uzak: 2.6, yan: .2 }), creep: .5 },
    // 4 içeride: çay ısrarı
    { t: SC(4), move: 'cut', ...iki4(), creep: .25 },
    { t: S('z5') - .05, move: 'cut', ...Y(Z4, { h: 1.38, uzak: 2.9, yan: .25 }), creep: .3 },
    { t: S('l5') - .05, move: 'cut', ...Y(L4, { h: 1.4, uzak: 2.6, yan: -.3 }), creep: .3 },
    { t: B('bekle')[0] + .1, move: 'cut', ...iki4({ uzak: 3.7 }), creep: .3 },
    { t: B('bekle')[0] + 1.4, move: 'cut', ...Y(Z4, { h: 1.25, uzak: 2.4, yan: -.2 }), creep: .5 },
    { t: S('t5') - .05, move: 'cut', ...Y(T4, { h: 1.35, uzak: 2.6, yan: .3 }), creep: .3 },
    // 5 kira: bozuk para
    { t: SC(5), move: 'cut', ...Y(L4, { h: 1.4, uzak: 2.9, yan: .3 }), creep: .3 },
    { t: S('z7') - .05, move: 'cut', ...Y(Z4, { h: 1.25, uzak: 2.5, yan: .3 }), creep: .3 },
    { t: B('para')[0], move: 'cut', ...SEHPA, creep: .5 },
    { t: S('z8') - .05, move: 'cut', ...Y(ZS, { h: 1.22, uzak: 2.5, yan: -.3 }), creep: .3 },
    { t: S('t6') - .05, move: 'cut', ...Y(T5, { h: 1.35, uzak: 2.7, yan: -.3 }), creep: .3 },
    { t: S('z9') - .05, move: 'cut', ...Y(ZS, { h: 1.22, uzak: 2.8, yan: .3 }), creep: .3 },
    { t: B('lunacam')[0], move: 'cut', ...Y(L5, { h: 1.42, uzak: 2.3, yan: .2 }), creep: .5 },
    { t: B('saat')[0], move: 'cut', ...PENCERE, creep: .25 },
    // 6 gece: karnım zil çalıyor
    { t: SC(6), move: 'cut', ...Y(ZS, { h: 1.22, uzak: 2.6, yan: -.35 }), creep: .3 },
    { t: S('t7') - .05, move: 'cut', ...Y(T0, { h: 1.35, uzak: 2.7, yan: -.25 }), creep: .3 },
    { t: B('zil1')[0], move: 'cut', ...iki6(), creep: .35 },
    { t: S('z11') - .02, move: 'whip', dur: .25, ...Y(ZS, { h: 1.22, uzak: 2.4, yan: .3 }), creep: .5 },
    // 7 Zip kapıya koşar, boş koridor
    { t: SC(7), move: 'cut', ...KAPI_L, creep: .2 },
    { t: S('z12'), move: 'cut', ...Y(KAPIDA, { h: 1.25, uzak: 2.3, yan: .9 }), creep: .3 },
    // 8 açıklama, yeni kural, karın yine, göbeğe konuşma
    { t: SC(8), move: 'cut', ...iki8(), creep: .25 },
    { t: S('z13'), move: 'whip', dur: .25, ...Y(Z8, { h: 1.38, uzak: 2.9, yan: .25 }), creep: .3 },
    { t: B('zil2')[0], move: 'cut', ...iki8({ uzak: 3.9 }), creep: .4 },
    { t: B('bakis')[0], move: 'cut', ...Y(T0, { h: 1.35, uzak: 2.4, yan: -.25 }), creep: .5 },
    { t: B('zil3')[0], move: 'cut', ...iki8({ uzak: 3.7 }), creep: .3 },
    { t: S('t10'), move: 'cut', ...Y(T0, { h: 1.35, uzak: 2.5, yan: .3 }), creep: .3 },
    { t: B('donma')[0] + .2, move: 'cut', ...iki8({ uzak: 4.4 }), creep: .7 },
    // 9 önce burun
    { t: SC(9), move: 'cut', ...Y(ESIK, { h: 1.5, uzak: 1.15, yan: .35, fov: 34 }), creep: .6 },
    { t: S('h1') - .1, move: 'cut', ...Y(ESIK, { h: 1.45, uzak: 3.0, yan: .9 }), creep: .3 },
    { t: B('sakla')[0], move: 'cut', ...iki8({ uzak: 3.8 }), creep: .2 },
    { t: S('l7') - .05, move: 'cut', ...Y(L9, { h: 1.4, uzak: 2.8, yan: .3 }), creep: .3 },
    { t: S('h8') - .05, move: 'cut', ...Y(ESIK, { h: 1.45, uzak: 2.6, yan: .8 }), creep: .3 },
    { t: S('l10') - .05, move: 'cut', ...Y(L9, { h: 1.42, uzak: 2.3, yan: -.2 }), creep: .4 },
    { t: S('h2') - .1, move: 'cut', ...O.ikili('ev', ESIK, HUGO_IC, ctx, { uzak: 4.2, h: 1.45 }), creep: .25 },
    { t: Z.W('Çilek') - .2, move: 'cut', ...Y(HUGO_IC, { h: 1.45, uzak: 2.6, yan: .4 }), creep: .4 },
    { t: S('t11') - .05, move: 'cut', ...Y(T0, { h: 1.4, uzak: 2.9, yan: -.2 }), creep: .3 },
    { t: S('h3') - .05, move: 'cut', ...Y(HUGO_IC, { h: 1.45, uzak: 2.6, yan: .45 }), creep: .4 },
    { t: S('t12') - .05, move: 'cut', ...Y(T0, { h: 1.55, uzak: 3.2, yan: -.2 }), creep: .25 },
    { t: S('h9') - .05, move: 'cut', ...Y(HUGO_IC, { h: 1.45, uzak: 2.7, yan: .45 }), creep: .3 },
    { t: S('t16') - .05, move: 'cut', ...Y(T0, { h: 1.4, uzak: 2.4, yan: .25 }), creep: .3 },
    { t: S('h4') - .05, move: 'cut', ...PARA, creep: .5 },
    { t: S('l8') - .05, move: 'cut', ...Y(L9, { h: 1.4, uzak: 2.7, yan: .3 }), creep: .3 },
    { t: S('z16') - .05, move: 'cut', ...Y([T0[0] + .15, 0, T0[2]], { h: 1.3, uzak: 2.9, yan: -.25 }), creep: .3 },
    { t: B('duy')[0] + .1, move: 'cut', ...Y(HUGO_IC, { h: 1.45, uzak: 2.3, yan: .3 }), creep: .5 },
    { t: S('t13') - .05, move: 'cut', ...Y(T0, { h: 1.3, uzak: 2.7, yan: -.2 }), creep: .3 },
    { t: B('egil')[0], move: 'cut', ...ikiHT(), creep: .3 },
    { t: S('h10') - .05, move: 'cut', ...ikiHT({ uzak: 2.7, h: 1.15 }), creep: .4 },
    { t: S('t17') - .05, move: 'cut', ...Y(T0, { h: 1.35, uzak: 2.3, yan: .2 }), creep: .3 },
    { t: S('h6') - .05, move: 'cut', ...Y(HUGO_IC, { h: 1.75, uzak: 3.2, yan: .5 }), creep: .3 },
    { t: S('t14') - .05, move: 'cut', ...Y(T0, { h: 1.35, uzak: 2.8, yan: -.3 }), creep: .3 },
    { t: S('h7') - .05, move: 'cut', ...Y(HUGO_IC, { h: 1.45, uzak: 2.6, yan: .45 }), creep: .2 },
    { t: B('kapat')[0], move: 'cut', ...KAPI_L, creep: .2 },
    { t: B('sessiz')[0], move: 'cut', ...GENIS, creep: .3 },
    // düğme
    { t: B('zil4')[0], move: 'cut', ...Y(T0, { h: 1.15, uzak: 2.7, yan: -.2 }), creep: .4 },
    { t: S('z17'), move: 'whip', dur: .25, ...Y([T0[0] + .5, 0, T0[2] - .4], { h: 1.25, uzak: 2.6, yan: .3 }), creep: .4 },
    // 10 bitiş
    { t: SC(10), move: 'cut', ...SON, creep: .2 },
  ], { fps: FPS });
  cp.k.forEach((k, i) => { const d = (i + 1 < cp.k.length ? cp.k[i + 1].t : DUR) - k.t; if (i > 0) k.creep = Math.min(k.creep ?? .25, .43 / Math.max(.5, d)); });   // uzun planda yakınlaşma sınırlı
  cp.kick(B('kzil')[0] + .05, .7).kick(B('kzil')[0] + .4, .8).kick(B('tak')[0] + .12, .5).kick(B('ac')[0] + .65, .6).kick(B('para')[0] + .45, .7)
    .kick(B('zil1')[0] + .05, .6).kick(B('zil1')[0] + .55, .8).kick(B('kos1')[0] + .9, .6).kick(B('zil2')[0] + .05, .5)
    .kick(B('zil3')[0] + .05, 1.0).kick(B('donma')[0] + .1, .5).kick(B('sakla')[0] + .1, .9).kick(B('anten')[0] + 1.05, .5).kick(B('zil4')[0] + .05, .5);
}

export function frame(t, ctx) {
  const { cam } = ctx, { S, E, B, SC, on } = Z;
  const c = cp.apply(cam, t);
  O.mekan(K, O.mekanOf(cam));
  const fr = (id, f) => S(id) + (E(id) - S(id)) * f;
  const gece2 = B('saat')[0] + 1.25;                                    // pencere geceye döner (kartın arkasında)
  const day = t >= SC(2) && t < gece2;
  O.gunduz(K, day ? 1 : 0);
  // bozuk para: kancada ve gecede sehpada; gündüz 'para' vuruşunda dökülür
  O.para(K, t < SC(2) ? 1 : t < B('para')[0] + .35 ? 0 : O.backOut(clamp01((t - B('para')[0] - .35) / .55)));
  // kapı: Zip gelince açık, içeri girince kapalı; koşuda açılır; Hugo'yla açık, "kapat" vuruşunda kapanır
  const ac = B('ac')[0], k1 = B('kos1')[0], kp = B('kapat')[0];
  O.kapi(K, t < ac + .05 ? 0 : t < SC(4) ? O.backOut(clamp01((t - ac - .05) / .4))
    : t < k1 + .8 ? 0 : t < SC(8) ? O.backOut(clamp01((t - k1 - .8) / .35))
    : t < SC(9) ? 0 : t < kp + .6 ? 1 : .8 * (1 - clamp01((t - kp - .6) / .4)));
  const zil = n => B('zil' + n)[0];

  // ================= TOBİ =================
  {
    let pos = T0;
    const belly = Math.max(dec(t, B('kzil')[0] + .03, 3), dec(t, zil(1), 3), dec(t, zil(2), 3), dec(t, zil(4), 3)) * 7;
    const tp = { ...O.canli(Z, 'tobi', t), jiggle: .6 + belly, expr: 'neutral', look: .55, lid: .15, propR: 'cips', armR: [40, 70] };
    if (t < SC(2)) {                                                               // KANCA
      Object.assign(tp, { expr: 'surprised', lookY: .9, look: .1, blink: 0 });
      if (t > B('title')[0] + .15) Object.assign(tp, { expr: 'worried', lookY: .3, look: .7 });
    } else if (t < SC(3)) {                                                        // masa
      pos = TM; Object.assign(tp, { look: -.7 });
      if (t >= S('t1') - .05 && t < B('soguk')[0]) Object.assign(tp, { armR: [70, 50] });
      else if (t >= B('soguk')[0] && t < S('t2')) { const u = t - B('soguk')[0];
        Object.assign(tp, { expr: u < .35 ? 'neutral' : 'surprised', blink: 0, look: u < .35 ? -.7 : 0, lookY: u < .35 ? 0 : .6, sweat: u > .5 ? 1 : 0, armR: u > .5 ? [95, 25] : [70, 50], squash: u > .35 ? -.08 * dec(t, B('soguk')[0] + .35, 5) : 0 }); }
      else if (t >= S('t2') && t < S('l9')) Object.assign(tp, { expr: t < fr('t2', .35) ? 'worried' : 'neutral', armR: [95, 25], look: t < fr('t2', .35) ? 0 : -.6 });
      else if (t >= S('l9') && t < S('t15')) Object.assign(tp, { look: -.7, lid: .2 });
      else if (t >= S('t15')) Object.assign(tp, { expr: 'focused', armR: [95, 25], look: -.5 });
    } else if (t < SC(4)) {                                                        // kapı
      const w = O.yuru(t, B('yuru')[0] + .3, B('yuru')[1] + .3, TS, TK); pos = w.pos;
      Object.assign(tp, { walk: w.walk, look: -.85, lean: w.moving ? -3 : 0 });
      if (t >= B('tak')[0] + .1 && t < S('l2')) Object.assign(tp, { expr: 'surprised', blink: 0 });
      if (t >= ac && t < S('z1')) Object.assign(tp, { expr: 'surprised', lookY: .35 });
      else if (t >= S('z1')) Object.assign(tp, { lookY: .35, lid: on('t3', t) ? .3 : .15 });
      if (t >= B('antenbak')[0] && t < S('t4')) Object.assign(tp, { lookY: O.lerp(.4, -.25, O.ramp(t, B('antenbak')[0] + .1, B('antenbak')[0] + .55)), blink: 0, expr: 'focused' });
      if (t >= S('t4') && t < S('z4')) Object.assign(tp, { lookY: -.1, lid: .3 });
      if (t >= B('gecmis')[0]) tp.mouth = Math.max(tp.mouth || 0, .25 + .25 * Math.sin(t * 22));
    } else if (t < B('para')[0]) {                                                 // çay
      pos = T4; Object.assign(tp, { look: .75, lid: .2 });
      if (t >= B('bekle')[0] && t < S('z6')) tp.mouth = Math.max(tp.mouth || 0, .2 + .25 * Math.sin(t * 20));        // çiğner
      if (t >= S('t5') - .05 && t < SC(5)) Object.assign(tp, { lid: .45, armR: [85, 30], look: .5 });
    } else if (t < gece2) {                                                        // bozuk para
      pos = T5; Object.assign(tp, { look: .8, lookY: .45 });
      if (t < S('z8')) Object.assign(tp, { expr: 'surprised', blink: 0 });
      if (on('t6', t)) Object.assign(tp, { lookY: .1, expr: 'worried' });
      if (t >= S('z9')) Object.assign(tp, { expr: t > fr('z9', .55) ? 'surprised' : 'neutral', lookY: .2 });
    } else if (t < zil(1)) Object.assign(tp, { expr: 'worried', lookY: .7, look: .2 });                             // boş pakete bakar
    else if (t < SC(7)) Object.assign(tp, { expr: 'surprised', lookY: .9, look: .1 });                              // karnına bakar
    else if (t < zil(2)) Object.assign(tp, { look: .7 });
    else if (t < B('bakis')[0]) Object.assign(tp, { expr: 'worried', lookY: .8, look: .1 });
    else if (t < zil(3)) Object.assign(tp, { look: .55, lookY: .55, lid: .45 });                                    // yavaş, kabullenmiş bakış
    else if (t < B('donma')[0]) Object.assign(tp, { look: .55, lookY: .5, lid: .35 });
    else if (t < SC(9)) Object.assign(tp, { expr: 'surprised', look: t > B('donma')[0] + .55 ? -1 : .4, lookY: 0, sweat: t > B('donma')[0] + .55 ? 1 : 0, blink: 0 });
    else if (t < S('t11')) Object.assign(tp, { look: -.9, lid: .25 });
    else if (t < B('anten')[0] + .85) Object.assign(tp, { look: -.8, lid: .35, armR: on('t11', t) || on('h3', t) ? [80, 30] : [40, 70] });
    else if (t < S('h9')) Object.assign(tp, { look: -.8, lid: .5, squash: -.22 * O.ramp(t, B('anten')[0] + .85, B('anten')[0] + 1.1) });   // bakmadan uzayıp antenleri kafasıyla ezer
    else if (t < S('z16')) Object.assign(tp, { look: -.8, lid: on('t16', t) ? .5 : .3, squash: -.22 * (1 - O.ramp(t, S('h9'), S('h9') + .4)) });
    else if (t < S('h5')) Object.assign(tp, { expr: 'surprised', blink: 0, look: t < B('duy')[0] + .4 ? .6 : -.8, sweat: 1 });       // fısıltı arkadan geldi
    else if (t < B('egil')[0]) Object.assign(tp, { look: -.8, lid: .4, armL: on('t13', t) ? [58, 62] : [16, 8], jiggle: on('t13', t) ? 2.5 : .6 });
    else if (t < S('t17')) Object.assign(tp, { look: -.6, lookY: .7, expr: 'worried', sweat: 1, lean: 5, blink: t < B('egil')[0] + .5 ? 0 : tp.blink });
    else if (t < S('h6')) Object.assign(tp, { look: -.7, lookY: .5, lid: .5 });
    else if (t < B('zil4')[0]) Object.assign(tp, { look: -.9, lid: .3, blink: t > B('sessiz')[0] ? 0 : tp.blink });
    else if (t < SC(10)) Object.assign(tp, { look: .2, lookY: .85, lid: .5, expr: 'worried', armR: [16, 8] });
    else { tp.look = .6; tp.mouth = Math.max(tp.mouth || 0, .2 + .25 * Math.sin(t * 20)); tp.armR = [85, 30]; }
    if (t > S('t12') && t < E('t12') + .4) tp.mouth = Math.max(tp.mouth || 0, .25 + .25 * Math.sin(t * 22));          // çiğner
    O.oyna(K, 'tobi', pos, cam, tp);
  }

  // ================= LUNA =================
  if ((t >= SC(2) && t < gece2) || t >= B('sakla')[0]) {
    let pos = LM;
    const lp = { ...O.canli(Z, 'luna', t), expr: 'neutral', look: .6 };
    if (t < SC(3)) {                                                               // masa: fatura
      Object.assign(lp, { propR: 'scroll', armR: [55, 60], expr: 'worried', look: t < S('l1') + .5 ? .1 : .7, lookY: t < S('l1') + .5 ? .5 : 0 });
      if (t >= S('t1') && t < S('t2')) Object.assign(lp, { expr: 'neutral', lid: t > B('soguk')[0] ? .45 : .1, blink: t > B('soguk')[0] ? 0 : lp.blink, look: .8 });
      if (t >= S('t2') && t < S('l9')) Object.assign(lp, { expr: 'smile', look: .7 });
      if (on('l9', t)) Object.assign(lp, { expr: 'focused', look: .2, armL: [120 + Math.sin(t * 5) * 8, 40] });
      if (t >= S('t15') - .05) Object.assign(lp, { expr: 'neutral', look: t > fr('t15', .6) ? 0 : .7, lookY: t > fr('t15', .6) ? -.6 : 0, lid: .35 });      // göz devirir
    } else if (t < SC(4)) {                                                        // kapı: ilan elde
      const w = O.yuru(t, B('yuru')[0] + .1, B('yuru')[1] - .1, LS, LK); pos = w.pos;
      Object.assign(lp, { walk: w.walk, lean: w.moving ? -3 : 0, look: -.85, propL: 'ilan', armL: [70, 50], expr: 'neutral' });
      if (t >= B('tak')[0] + .1 && t < S('l2')) Object.assign(lp, { expr: 'surprised', blink: 0, armL: [100, 40], squash: -.1 * dec(t, B('tak')[0] + .1, 6) });
      if (t >= S('l2') - .1 && t < ac) Object.assign(lp, { look: 0, lid: .45, expr: 'neutral', armL: [70, 50] });                                           // kameraya
      if (t >= ac && t < S('l3')) Object.assign(lp, { expr: 'surprised', lookY: .5, blink: t < ac + .9 ? 0 : lp.blink });
      if (t >= S('l3')) Object.assign(lp, { expr: on('l3', t) ? 'worried' : 'neutral', lookY: .45, lid: .15 });
      if (t >= B('antenbak')[0] && t < B('gecmis')[0]) Object.assign(lp, { lookY: .15, expr: 'worried' });
      if (t >= B('gecmis')[0] + .1) Object.assign(lp, { look: O.lerp(-.85, 0, O.ramp(t, B('gecmis')[0] + .15, B('gecmis')[0] + .5)), lookY: 0, lid: .5, expr: 'neutral', blink: 0 });   // kameraya bakış
    } else if (t < B('para')[0]) {                                                 // çay
      pos = L4; Object.assign(lp, { look: -.8, lookY: .35 });
      if (on('l4', t)) Object.assign(lp, { expr: 'smile', armR: [70, 45] });
      if (t >= S('z5') && t < S('l5')) Object.assign(lp, { expr: t > fr('z5', .25) ? 'surprised' : 'smile' });
      if (t >= S('l5') && t < S('z6')) { const u = t - S('l5');                                                      // "Peki." omuz silker, döner, başka işe bakar
        Object.assign(lp, { expr: 'neutral', armR: u < .5 ? [70, 70] : [16, 8], armL: u < .5 ? [70, 70] : [16, 8], look: u < .8 ? -.6 : .8, lookY: u < .8 ? .3 : -.1, tilt: u > 1 ? Math.sin(t * 3) * 4 : 0 }); }
      if (t >= S('z6') && t < SC(5)) Object.assign(lp, { look: t < S('t5') ? -.8 : -1, lookY: .3, expr: t < S('t5') ? 'surprised' : 'neutral', lid: t < S('t5') ? 0 : .4 });
      if (t >= SC(5)) Object.assign(lp, { expr: on('l6', t) ? 'focused' : 'neutral', armR: t < S('z7') ? [62, 48] : [16, 8], look: -.8, lookY: .35 });
    } else if (t < gece2) {                                                        // bozuk para
      pos = L5; Object.assign(lp, { look: -.85, lookY: .5, expr: t < S('z8') ? 'surprised' : 'worried', blink: t < S('z8') ? 0 : lp.blink });
      if (t >= B('lunacam')[0]) Object.assign(lp, { look: O.lerp(-.85, 0, O.ramp(t, B('lunacam')[0] + .2, B('lunacam')[0] + .7)), lookY: O.lerp(.5, 0, O.ramp(t, B('lunacam')[0] + .2, B('lunacam')[0] + .7)), lid: .5, expr: 'neutral', blink: 0 });
    } else if (t < SC(10)) {                                                       // Hugo: odasından gelir
      const w = O.yuru(t, B('sakla')[0] + .1, S('l7') - .1, L9A, L9); pos = w.pos;
      Object.assign(lp, { walk: w.walk, look: -.9, expr: 'worried' });
      if (on('l7', t)) Object.assign(lp, { expr: 'grin', armR: [110, 40], armL: [110, 40], sweat: 1 });
      else if (t >= E('l7') && t < S('l10')) Object.assign(lp, { expr: 'worried', sweat: 1 });
      else if (t >= S('l10') && t < S('h2')) Object.assign(lp, { expr: 'neutral', lid: .45, look: t > E('l10') + .15 ? 0 : -.9, blink: 0 });                // "On iki oldu." sonra kameraya
      else if (on('l8', t)) Object.assign(lp, { expr: 'grin', armR: [70, 45], sweat: 1 });
      else if (t >= S('z16') && t < S('h5')) Object.assign(lp, { expr: 'surprised', blink: 0, sweat: 1, look: t < B('duy')[0] + .4 ? -.5 : -.9 });
      else if (t >= B('sessiz')[0] && t < B('zil4')[0]) Object.assign(lp, { blink: 0, expr: 'worried' });
      else if (t >= B('zil4')[0]) Object.assign(lp, { look: -.9, lookY: .5, lid: .5, expr: 'neutral' });
    } else Object.assign(lp, { look: O.lerp(-.9, 0, O.ramp(t, SC(10) + .3, SC(10) + .9)), lid: .5, expr: 'neutral' }), pos = L9;                              // bitiş: kameraya
    O.oyna(K, 'luna', pos, cam, lp);
  }

  // ================= ZİP =================
  const zipVar = t < SC(2) || (t >= ac + .08 && t < SC(9)) || t >= B('sakla')[0];
  if (zipVar) {
    let pos = ZS, zp = { ...O.canli(Z, 'zip', t), expr: 'happy', look: -.6 };
    const say = (a, b, n) => { const u = clamp01((t - a) / (b - a)) * n, k = Math.sin((u % 1) * Math.PI); return { armR: [60 + 55 * k, 50 - 20 * k], lookY: .6, look: 0, expr: 'focused', tilt: Math.sin(t * 6) * 2 }; };   // para sayar
    if (t < SC(2)) {                                                               // KANCA
      const z0 = B('kzil')[0] + .35, snap = t > z0;
      Object.assign(zp, { expr: snap ? 'surprised' : 'focused', look: snap ? -.9 : 0, lookY: snap ? .4 : .6, blink: snap ? 0 : zp.blink,
        antUp: dec(t, z0, 2.2) * 1.2 + (snap ? .3 : 0), antWob: dec(t, z0, 1.8), squash: snap ? -.15 * dec(t, z0, 6) : 0 });
      if (t > S('z0') - .05) Object.assign(zp, { expr: 'grin', look: -.3, lookY: 0, armR: [150, 20], antUp: .6, antWob: .6 });
    } else if (t < SC(4)) {                                                        // eşikte
      pos = ESIK; const u = t - ac - .08;
      Object.assign(zp, { expr: 'happy', look: .7, lookY: -.25, propL: 'kilavuz', armL: [40, 60], antUp: dec(t, ac + .6, 2) * 1.0, antWob: dec(t, ac + .6, 1.6), squash: -.14 * dec(t, ac + .6, 6) });
      if (on('z1', t)) Object.assign(zp, { expr: 'grin', armR: [150 + Math.sin(t * 9) * 12, 20] });
      if (t > fr('z1', .42) && t < S('l3')) Object.assign(zp, { armR: [16, 8], armL: [62, 62], look: .2, lookY: .5, expr: 'focused' });                     // kılavuzdan okur
      if (on('z2', t)) Object.assign(zp, { expr: 'proud' });
      if (on('z3', t)) Object.assign(zp, { armR: [168, 8], lookY: -.7, look: .2, expr: 'smile' });                                                         // yukarıyı gösterir
      if (t >= B('antenbak')[0] && t < S('t4')) Object.assign(zp, { antUp: .5, antWob: 1, expr: 'happy' });                                                // antenler el sallar
      if (t >= S('z4')) Object.assign(zp, { expr: t > Z.W('Geçmiş') - .1 ? 'worried' : 'happy', antUp: t > Z.W('Sizin') ? .5 : 0, lookY: t > Z.W('Sizin') && t < Z.W('Geçmiş') ? -.5 : -.25 });
    } else if (t < B('para')[0]) {                                                 // çay
      pos = Z4; Object.assign(zp, { look: .8, lookY: -.3, expr: 'happy' });
      if (t >= S('z5') && t < S('l5')) Object.assign(zp, { expr: t < fr('z5', .2) ? 'focused' : 'proud', propL: 'kilavuz', armL: [62, 62], armR: t < fr('z5', .2) ? [120, 30] : [16, 8], look: t < fr('z5', .2) ? .8 : .3, lookY: t < fr('z5', .2) ? -.3 : .4 });
      if (t >= S('l5') && t < S('z6')) { const u = clamp01((t - B('bekle')[0]) / 2.4);                                                                     // bekler; umut söner
        Object.assign(zp, { expr: u < .3 ? 'happy' : u < .65 ? 'neutral' : 'worried', antUp: .35 - .95 * u, look: u > .82 ? 0 : .8, lookY: u > .82 ? 0 : -.3, blink: u > .3 && u < .6 ? 0 : zp.blink, tilt: u > .65 ? -5 : 0 }); }
      if (t >= S('z6') && t < SC(5)) Object.assign(zp, { expr: 'worried', antUp: -.6, look: t < E('z6') + .1 ? .8 : -.8, lookY: -.3 });
      if (t >= SC(5)) Object.assign(zp, { expr: on('z7', t) ? 'grin' : 'neutral', antUp: on('z7', t) ? .4 : 0, armR: on('z7', t) ? [140, 25] : [16, 8], look: .8, lookY: -.3 });
    } else if (t < gece2) {                                                        // parayı döker ve sayar
      const u = t - B('para')[0];
      Object.assign(zp, { expr: 'grin', look: 0, lookY: .55, armR: u < 1.1 ? [120, 30 + Math.sin(t * 30) * 14] : [16, 8], armL: u < 1.1 ? [120, 30 + Math.cos(t * 30) * 14] : [16, 8], antWob: dec(t, B('para')[0] + .4, 1.5), antUp: .3 });
      if (t >= S('z8') - .05 && t < S('t6')) Object.assign(zp, say(S('z8'), E('z8'), 3));
      if (t >= S('t6') && t < S('z9')) Object.assign(zp, { look: -.8, lookY: -.2, expr: 'happy' });
      if (t >= S('z9')) Object.assign(zp, t < fr('z9', .55) ? { look: -.8, lookY: -.2, expr: 'proud' } : say(fr('z9', .55), E('z9'), 1));
      if (t >= B('lunacam')[0]) Object.assign(zp, say(B('lunacam')[0], gece2, 5));
    } else if (t < zil(1) + .5) Object.assign(zp, say(SC(6), zil(1) + .5, 7), { lid: .2 });
    else if (t < SC(7)) {                                                          // çifte bakış: göbeğe, öne, hızla göbeğe
      const u = t - zil(1) - .5, snap = u > .45;
      Object.assign(zp, { expr: snap ? 'surprised' : 'neutral', look: u < .2 ? -.8 : u < .45 ? 0 : -.9, lookY: u < .2 ? .4 : u < .45 ? 0 : .4,
        antUp: dec(t, zil(1) + .95, 2.2) * 1.2 + (snap ? .3 : 0), antWob: dec(t, zil(1) + .95, 1.8), squash: snap ? -.15 * dec(t, zil(1) + .95, 6) : 0 });
      if (t > S('z11') - .02) Object.assign(zp, { expr: 'grin', look: -.3, lookY: 0, armR: [150, 20], antUp: .6, antWob: .6 });
    } else if (t < SC(8)) {                                                        // koşu ve kapı
      const w = O.yuru(t, k1, k1 + .8, ZIP_KOS, KAPIDA, { adim: 3.2 });
      pos = w.pos; Object.assign(zp, { walk: w.walk, flip: true, lean: w.moving ? 14 : 0, expr: 'grin', look: -.6, armR: t > k1 + .7 ? [70, 40] : [40, 60] });
      if (t > B('bos1')[0]) Object.assign(zp, { expr: 'surprised', armR: [70, 40], blink: 0, antUp: -.2 });
      if (t > S('z12') - .1) Object.assign(zp, { flip: false, expr: 'neutral', lid: .45, look: .35, armR: [16, 8], antUp: -.35 });
    } else if (t < zil(2)) {
      pos = Z8; Object.assign(zp, { look: -.6, expr: on('t8', t) ? 'focused' : 'proud' });
      if (t > S('z13') - .2) Object.assign(zp, { propL: 'kilavuz', propR: 'pen', armL: [50, 60], armR: [55, 60], lookY: .55, look: -.1, expr: 'focused', tilt: Math.sin(t * 9) * 4 });
    } else if (t < B('bakis')[0]) {                                                // kapıya çekilir, direnir, göbeğe döner
      const u = t - zil(2); pos = Z8;
      if (u < .9) Object.assign(zp, { expr: 'worried', look: -1, lean: -14 * clamp01(u / .5), tilt: Math.sin(t * 40) * 3, sweat: 1, antWob: .5 });
      else { pos = [Z8[0] - .15, 0, Z8[2]]; Object.assign(zp, { expr: on('z14', t) ? 'angry' : 'focused', look: -.8, lookY: .5, lean: -8, armL: [70, 40], armR: [70, 40] }); }
    } else if (t < zil(3)) { pos = Z8; Object.assign(zp, { expr: 'neutral', look: -.6, lid: .3, antUp: -.1 }); }
    else if (t < B('donma')[0]) { pos = [Z8[0] - .15, 0, Z8[2]]; Object.assign(zp, { expr: on('t10', t) ? 'neutral' : 'angry', look: -.8, lookY: .5, lean: -8, armR: on('z15', t) ? [150, 25] : [16, 8], blink: on('t10', t) ? 0 : zp.blink }); }
    else if (t < SC(9)) { pos = Z8; Object.assign(zp, { expr: 'surprised', look: t > B('donma')[0] + .55 ? -1 : -.5, blink: 0, sweat: 1, antUp: t > B('donma')[0] + .55 ? .4 : 0 }); }
    else if (t < SC(10)) {                                                         // saklanma, anten, fısıltı, düğme
      const u = clamp01((t - B('sakla')[0]) / .22); pos = mix3(Z8, ZIP_ARKA, u);
      Object.assign(zp, { expr: 'worried', look: -.4, lean: u < 1 ? -20 : 0, squash: u > 0 && u < 1 ? -.2 : 0, antUp: -.3 });
      const an = B('anten')[0], ra = clamp01((t - an - .05) / .6), bas = clamp01((t - an - 1.1) / .12);                // antenler yükselir; Tobi kafasıyla ezer
      if (t > an && t < S('h9') + .5) { pos = [pos[0], .2 * ra * (1 - bas), pos[2]];
        Object.assign(zp, { antUp: (-.3 + 1.3 * ra) * (1 - bas) - .4 * bas, antWob: .4 * dec(t, an + .5, 2) + .8 * dec(t, an + 1.2, 3), squash: .2 * dec(t, an + 1.2, 6) }); }
      if (t >= S('z16') - .25 && t < B('duy')[0] + .35) { const p2 = Math.min(clamp01((t - S('z16') + .25) / .2), 1 - clamp01((t - B('duy')[0] - .15) / .15));   // sağdan başını uzatır, fısıldar, geri kaçar
        pos = [ZIP_ARKA[0] + .62 * p2, 0, ZIP_ARKA[2] + .1]; Object.assign(zp, { expr: 'focused', look: -.2, lookY: .4, antUp: -.4, tilt: 8, armR: [120, 30] }); }
      if (t > B('zil4')[0] + .5) { const p2 = clamp01((t - B('zil4')[0] - .5) / .3); pos = [ZIP_ARKA[0] + .62 * p2, 0, ZIP_ARKA[2] + .1];        // kenardan çıkar, gözler sıkı kapalı
        Object.assign(zp, { expr: on('z17', t) ? 'worried' : 'neutral', blink: 1, look: .6, antUp: -.4, tilt: -6 }); }
    } else Object.assign(zp, say(SC(10), DUR, 9));                                 // bitiş: saymaya devam
    O.oyna(K, 'zip', pos, cam, zp);
  }

  // ================= HUGO =================
  if (t >= SC(9) && t < kp + .75) {
    let pos = ESIK, hp = { ...O.canli(Z, 'hugo', t), expr: 'smug', look: .7, sniff: 0, brow: .3 };
    if (t < S('h1')) Object.assign(hp, { sniff: 1, expr: 'focused', lid: .45, look: .3, lookY: -.1, tilt: Math.sin(t * 7) * 2 });
    else if (t < S('h8') - .3) Object.assign(hp, { expr: 'smug', brow: .6, armR: on('h1', t) ? [120, 50] : [16, 8] });
    else if (t < S('h2')) Object.assign(hp, { expr: 'smug', brow: .8, propL: 'scroll', propR: 'pen', armL: [30, 95], armR: [30, 95],              // defterinden okur, sonra yazar
      lookY: on('h8', t) && t < fr('h8', .7) ? .5 : t > S('l10') ? .55 : 0, look: on('h8', t) && t < fr('h8', .7) ? .2 : t > S('l10') ? .1 : .8, tilt: t > E('l10') ? Math.sin(t * 10) * 3 : 0 });
    else if (t < S('t11')) {                                                       // "Kira değil." eşikte; "Koku." içeri yürür, koklar
      const w0 = Z.W('Koku') - .1, w = O.yuru(t, w0, w0 + 1.3, ESIK, HUGO_IC); pos = w.pos;
      Object.assign(hp, { walk: w.walk, lean: w.moving ? 6 : 0, sniff: t > w0 ? 1 : 0, expr: t > w0 ? 'focused' : 'smug', lid: .4, look: .8, brow: .5 });
    } else {
      pos = HUGO_IC; Object.assign(hp, { expr: 'smug', brow: .9, lid: .3, look: .9 });
      if (t > B('anten')[0] + .3 && t < S('h4')) Object.assign(hp, { expr: 'angry', lid: .5, brow: 0, sniff: .5, lookY: t < S('t16') ? -.45 : -.1, armR: on('h9', t) ? [140, 25] : [16, 8] });
      if (t >= S('h4') && t < S('z16')) Object.assign(hp, { expr: 'smug', look: .9, lookY: .4, armR: on('h4', t) ? [75, 40] : [16, 8], propL: 'scroll', armL: [50, 60] });
      if (t >= S('z16') && t < S('h5')) { const u = clamp01((t - B('duy')[0] - .15) / .7);                              // donar, yavaşça döner
        Object.assign(hp, { expr: 'surprised', blink: 0, lid: .1, look: O.lerp(.2, .95, u * u * (3 - 2 * u)), lookY: .2 * u, brow: 1, propL: 'scroll', armL: [50, 60] }); }
      if (t >= S('h5') && t < B('egil')[0]) Object.assign(hp, { expr: 'angry', brow: .2, lid: .4, look: .95, lookY: .2 });
      if (t >= B('egil')[0] && t < S('h6')) { const u = O.ramp(t, B('egil')[0] + .1, B('egil')[0] + .6) * (1 - O.ramp(t, E('h10') + .1, S('h6')));   // eğilir, göbeği koklar
        Object.assign(hp, { lean: 24 * u, squash: .1 * u, look: .95, lookY: .75 * u, sniff: 1, expr: 'focused', lid: .5, tilt: Math.sin(t * 8) * 2 * u }); }
      if (t >= S('h6') && t < S('h7')) Object.assign(hp, { expr: 'smug', brow: .7, propL: 'scroll', armL: [85, 35], look: .85, lid: .3 });
      if (t >= S('h7')) {                                                          // geri geri çıkar, gözü Tobi'de
        const w = O.yuru(t, E('h7') - .9, kp + .55, HUGO_IC, [ESIK[0] - .35, 0, ESIK[2]]); pos = w.pos;
        Object.assign(hp, { walk: w.walk, flip: false, lean: w.moving ? -5 : 0, expr: 'smug', lid: .5, look: .9, sniff: .8, armR: on('h7', t) && t < fr('h7', .5) ? [120, 40] : [16, 8] });
      }
    }
    O.oyna(K, 'hugo', pos, cam, hp);
  }
  return O.bak(K, cam, c);
}

export function overlay(g, t, ctx) {
  const { S, E, B, SC } = Z, H = ctx.H;
  O.ustKatman(g, t, ctx, {
    kanca: 'BU ZİL NEREDEN ÇALIYOR?', bolum: 1,
    abone: [S('z2') + .3],
    aboneSon: [SC(10) + 1.6, (W, H) => [W / 2, H * (W > H ? .84 : .8)]],
    kartlar: [
      { t0: B('title')[0] + .1, t1: B('title')[1] - .05, cy: H * .27, lines: [['Kiracı Uzaylı', 78, O.KART.baslik], ['1. Bölüm: Kiralık Oda', 42, O.KART.alt]] },
      { t0: S('z5') + .9, t1: E('z5') + .5, cy: H * .22, lines: [['DÜNYALI KILAVUZU · KURAL 12', 34, O.KART.not], ['İlk teklif reddedilir.', 50, O.KART.alt]] },
      { t0: B('saat')[0] + .15, t1: B('saat')[1] - .1, lines: [['ÜÇ SAAT SONRA', 72, O.KART.soru]] },
      { t0: S('z13') + .5, t1: E('z13') + .9, cy: H * .22, lines: [['DÜNYALI KILAVUZU · YENİ KURAL', 34, O.KART.not], ['Zil çalarsa kapıya bakılmaz.', 50, O.KART.alt]] },
      { t0: S('h6') + .3, t1: E('h6') + .4, cy: H * .22, lines: [['KİRA SÖZLEŞMESİ · 7. MADDE', 34, O.KART.not], ['Evcil hayvan, gürültü ve', 44, O.KART.alt], ['tuhaf koku yasaktır.', 44, O.KART.alt]] },
      { t0: SC(10) + .3, t1: DUR, cy: H * (ctx.W > H ? .27 : .27), lines: [['Hugo bu kokunun peşini', 46, O.KART.soru], ['bırakacak mı?', 46, O.KART.soru], ['Bir sonraki bölümde', 32, O.KART.not], ['Günaydın Komşu', 66, O.KART.baslik]] },
    ],
  });
}
