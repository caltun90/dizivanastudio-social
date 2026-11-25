// Kiracı Uzaylı, 0. bölüm: DENEME (yayınlanmaz). Yeni bölümün story.js dosyası bu iskeletle yazılır:
//   1) zaman: replik ve vuruş saatleri Z.S('h1'), Z.E('t1'), Z.B('pop'), Z.SC(3); hiçbir saniye elle yazılmaz
//   2) kamera: CamPath anahtarları O.plan / O.yakin / O.ikili ile, sahne ve replik başlarına bağlı
//   3) frame(): mekân kameradan bulunur; her oyuncu O.oyna(K, ad, yer, cam, { ...O.canli(Z, ad, t), ifade ve poz })
//   4) overlay(): kanca yazısı (ilk 2 sn), dizi etiketi, abone bandı, kartlar
import * as THREE from 'three';
import { CamPath } from '/engine/src/camera.js';
import * as O from '/diziler/uzayli/ortak.js';
export { TOON, LOOK } from '/diziler/uzayli/ortak.js';

export const NAME = 'uzayli-b00';
export const FPS = 30;
export let DUR = 10;
export const CUES = [];
export const CAPTION = { colors: O.COLORS, names: O.NAMES, font: O.FONT };
let K, Z, cp;
const { EV, MERDIVEN } = O;

export async function setup(ctx) {
  K = await O.kur(ctx); Z = O.zaman(ctx); DUR = O.sure(ctx);
  const { S, SC, B } = Z;
  cp = new CamPath([
    // 1 kanca: Hugo kapıda koklar (ilk 2 sn içinde itme + vuruş sarsıntısı)
    { t: 0, ...O.yakin('merdiven', MERDIVEN.hugoKapi, ctx, { h: 1.45, uzak: 2.6, yan: -.3, fov: 42 }), creep: .45 },
    // 2 ev: kanepe, Tobi cips yiyor; Luna'ya yakın
    { t: SC(2), move: 'cut', ...O.ikili('ev', EV.kanepe1, EV.kanepe2, ctx), creep: .3 },
    { t: S('l1') + .05, move: 'whip', dur: .3, ...O.yakin('ev', EV.kanepe2, ctx, { yan: .3 }) },
    // 3 mutfak: Zip buzdolabının önünde fırlar
    { t: SC(3) + .05, move: 'whip', dur: .3, ...O.plan('ev.mutfak', ctx, { dx: .5 }) },
    { t: S('z1'), dur: .5, ...O.yakin('ev', EV.buzdolabi, ctx, { h: 1.15, uzak: 2.5, yan: -.3 }) },
    // 4 merdiven: Hugo koklar
    { t: SC(4), move: 'cut', ...O.yakin('merdiven', MERDIVEN.hugoKapi, ctx, { h: 1.45, uzak: 2.8, yan: .4 }), creep: .35 },
  ], { fps: FPS });
  cp.kick(.05, .6).kick(B('pop')[0] + .25, .9);
}

export function frame(t, ctx) {
  const { cam } = ctx, { S, E, B, SC, on } = Z;
  const c = cp.apply(cam, t);
  O.mekan(K, O.mekanOf(cam));
  if (K.where === 'merdiven') {
    const sniff = t < S('t1') ? 1 : on('h2', t) || t > E('h2') ? .7 : 0;
    O.oyna(K, 'hugo', MERDIVEN.hugoKapi, cam, { ...O.canli(Z, 'hugo', t), expr: t < SC(2) ? 'surprised' : 'smug', look: .7, sniff, brow: t < SC(2) ? .8 : 0 });
  } else if (t < SC(3)) {
    const lunaTalk = on('l1', t);
    O.oyna(K, 'tobi', EV.kanepe1, cam, { ...O.canli(Z, 'tobi', t), expr: on('t1', t) ? 'grin' : lunaTalk ? 'surprised' : 'happy', look: .5, propR: 'cips', armR: [40, 70] });
    O.oyna(K, 'luna', EV.kanepe2, cam, { ...O.canli(Z, 'luna', t), expr: lunaTalk ? 'angry' : 'worried', look: -.6, armL: lunaTalk ? [150, 30] : [16, 8], sweat: lunaTalk ? 1 : 0 });
  } else {
    const u = Math.min(1, Math.max(0, (t - B('pop')[0] - .2) / .35)), jump = O.backOut(u);
    const sq = u > 0 && u < 1 ? -.18 * Math.sin(u * Math.PI) : 0;
    O.oyna(K, 'zip', [EV.buzdolabi[0] - .2, 0, EV.buzdolabi[2] + .5 * jump], cam, { ...O.canli(Z, 'zip', t), expr: on('z1', t) ? 'grin' : 'happy', look: -.4, squash: sq, propR: on('z1', t) ? 'kilavuz' : null, armR: [60, 50] }, { scale: .3 + .7 * jump });
    O.oyna(K, 'luna', [EV.mutfak[0] - 1.3, 0, EV.mutfak[2] + .6], cam, { ...O.canli(Z, 'luna', t), expr: 'surprised', look: .6, sweat: 1 });
  }
  return O.bak(K, cam, c);
}

export function overlay(g, t, ctx) {
  const { B } = Z;
  O.ustKatman(g, t, ctx, {
    kanca: 'BU KOKU NEREDEN?', bolum: 0, abone: [8.2],
    kartlar: [{ t0: B('end')[0] - .2, t1: DUR, lines: [['Kiracı Uzaylı', 74, O.KART.baslik], ['Deneme sahnesi', 40, O.KART.alt]] }],
  });
}
