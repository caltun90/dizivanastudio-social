// Kiracı Uzaylı: dizinin ortak dosyası. Üç mekân, oyuncular, zaman çizelgesi, kamera planları, ışık ve üst katman.
// Her bölümün story.js dosyası bunu kullanır (örnek: stories/uzayli-b00/story.js). Bölümde işe yarayan ve başka bölümde
// de kullanılacak her yeni dekor ya da yardımcı BURAYA eklenir.
//
// Mekânlar (dünya koordinatı x ile ayrılır; kamera bir mekândan ötekine 'whip' ya da 'cut' ile geçer):
//   EV       x ≈ 0    Luna ile Tobi'nin öğrenci evi: kanepe ve pencere (sol arka), mutfak ve buzdolabı (sağ arka),
//                     yemek masası (sağ orta), giriş kapısı (sol duvar). Gece: lambalar sıcak, pencereden ay ışığı.
//   MERDIVEN x ≈ 100  apartman sahanlığı: Hugo'nun kapısı (sol), yukarı çıkan merdiven (sağ), duvar lambası, yüksek pencere.
//   SOKAK    x ≈ 200  gün batımı: BAKKAL vitrini, meyve kasaları, sokak lambaları, ev cepheleri.
import * as THREE from 'three';
import { stoneTex, woodTex, carpetTex, tileTex, wallTex, painted, flat, rng } from '/engine/src/paint.js';
import { flap, blinkAt, PLUM, TOON_PROPS } from '/engine/src/toon.js';
import { OrguToon } from '/engine/src/orgu.js';
import { smoother } from '/engine/src/camera.js';
import { glow } from '/engine/src/fx.js';
import { holedWall, vistaMat, nightCityTex, dayGardenTex } from '/engine/src/vista.js';
import * as UK from '/lib/dizi.js';
import { LOOK, SPK, NAMES, COLORS } from './kadro.js';
export { LOOK, SPK, NAMES, COLORS, OrguToon as TOON };
export const FONT = UK.FONT;
export const DIZI = 'KİRACI UZAYLI';

const V = (...a) => new THREE.Vector3(...a);
const HDR = (r, g, b) => new THREE.Color().setRGB(r, g, b);
const DEG = Math.PI / 180;
export const SET_X = { ev: 0, merdiven: 100, sokak: 200 };
export const ramp = (t, a, b) => smoother((t - a) / (b - a));
export const lerp = (a, b, k) => a + (b - a) * k;
export const backOut = x => x <= 0 ? 0 : x >= 1 ? 1 : 1 + 2.70158 * (x - 1) ** 3 + 1.70158 * (x - 1) ** 2;

// ---------------------------------------------------------------- yardımcılar
function shadows(g) {
  g.traverse(o => {
    if (!o.isMesh) return;
    if (o.material.isMeshLambertMaterial) o.receiveShadow = true;
    if (/Box|Cylinder|Sphere|Torus|Lathe/.test(o.geometry.type) && !o.userData.noShadow) o.castShadow = true;
  });
}
export function canvasTex(w, h, draw) { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; }
// a picture that always faces the camera (receipt, list, speech bubble, star). Hidden until frame() shows it.
export function kart3(scene, w, h, draw, { pw = 512, hdr = null } = {}) {
  const t = canvasTex(pw, Math.round(pw * h / w), draw);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false, color: hdr || 0xffffff }));
  m.layers.set(1); m.renderOrder = 20; m.visible = false; scene.add(m); return m;
}
// felt wallpaper: soft vertical stripes with a stitched dashed line (the channel's felt and yarn look)
function duvarKagidi(base, stripe, { rep = [1, 1], dash = '#ffffff' } = {}) {
  const t = canvasTex(256, 256, (c, w, h) => {
    c.fillStyle = base; c.fillRect(0, 0, w, h);
    c.fillStyle = stripe; for (let x = 0; x < w; x += 64) c.fillRect(x, 0, 28, h);
    c.strokeStyle = dash; c.globalAlpha = .28; c.lineWidth = 3; c.setLineDash([10, 9]); for (let x = 32; x < w; x += 64) { c.beginPath(); c.moveTo(x + 14, 0); c.lineTo(x + 14, h); c.stroke(); }
    c.setLineDash([]); c.globalAlpha = .06; for (let i = 0; i < 400; i++) { c.fillStyle = i % 2 ? '#000' : '#fff'; c.fillRect(Math.random() * w, Math.random() * h, 2, 2); }
  });
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...rep); return painted(t);
}
function yaziTex(text, { w = 512, h = 160, bg = '#2a2a4a', fg = '#ffe9b0', font = 'Poppins', size = 92, border = '#ffe9b0' } = {}) {
  return canvasTex(w, h, (c) => {
    c.fillStyle = bg; c.fillRect(0, 0, w, h);
    c.strokeStyle = border; c.lineWidth = 6; c.setLineDash([16, 12]); c.strokeRect(14, 14, w - 28, h - 28); c.setLineDash([]);
    c.fillStyle = fg; c.font = `700 ${size}px ${font}, "Arial Black", sans-serif`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(text, w / 2, h / 2 + 4);
  });
}
const box = (g, sx, sy, sz, x, y, z, m) => { const b = new THREE.Mesh(new THREE.BoxGeometry(sx, sy, sz), m); b.position.set(x, y, z); g.add(b); return b; };
const cyl = (g, r0, r1, h, x, y, z, m, seg = 20) => { const b = new THREE.Mesh(new THREE.CylinderGeometry(r0, r1, h, seg), m); b.position.set(x, y, z); g.add(b); return b; };
const ball = (g, r, x, y, z, m) => { const b = new THREE.Mesh(new THREE.SphereGeometry(r, 18, 14), m); b.position.set(x, y, z); g.add(b); return b; };
function lamba(g, L, x, y, z, { color = '#ffc884', power = 3.4, range = 6, shadeCol = '#c9963e', cord = .6, shadow = true } = {}) {
  const c = cyl(g, .008, .008, cord, x, y + .1 + cord / 2, z, flat('#2a2630'), 4); c.userData.noShadow = true;
  const s = new THREE.Mesh(new THREE.ConeGeometry(.26, .22, 24, 1, true), flat(shadeCol, { side: THREE.DoubleSide })); s.position.set(x, y + .12, z); s.userData.noShadow = true; g.add(s);
  const b = ball(g, .07, x, y, z, new THREE.MeshBasicMaterial({ color: HDR(2.2, 1.7, .8) })); b.userData.noShadow = true;
  const pl = new THREE.PointLight(color, power, range, 1.5); pl.position.set(x, y - .08, z);
  if (shadow) { pl.castShadow = true; pl.shadow.mapSize.set(1024, 1024); pl.shadow.bias = -.003; pl.shadow.radius = 4; }
  L.add(pl); return V(x + g.position.x, y - .08, z);
}

// ---------------------------------------------------------------- EV (x = 0)
export const EV = {
  kanepe1: [-2.1, 0, -2.0], kanepe2: [-1.15, 0, -2.0], sehpa: [-1.6, 0, -1.2], mutfak: [2.0, 0, -2.45], buzdolabi: [3.45, 0, -2.4],
  masa1: [1.35, 0, -1.0], masa2: [2.75, 0, -1.0], kapi: [-3.75, 0, .55], kapiIci: [-3.0, 0, .35], orta: [0, 0, -1.0], on: [0, 0, .6], pencere: [-1.6, 0, -2.75],
};
export const PARA = [-1.4, .45, -1.3];           // bozuk para yığınının yeri (sehpanın üstü)
function buildEv(scene, K) {
  const g = new THREE.Group(); scene.add(g); const L = new THREE.Group(); scene.add(L);
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(9, 8.5), painted(woodTex({ base: '#b07a4a', plank: 64, rep: [7, 7] }))); fl.rotation.x = -Math.PI / 2; fl.position.z = .5; g.add(fl);
  const rug = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 2.4), painted(carpetTex({ base: '#3a6aa8', band: '#f0b84a', rows: 2 }))); rug.rotation.x = -Math.PI / 2; rug.position.set(-1.5, .006, -1.4); g.add(rug);
  const wp = (rx, ry) => duvarKagidi('#b8c6e0', '#a8b8d6', { rep: [rx, ry] });
  const back = holedWall(9, 3.0, [-2.65, 1.0, -.55, 2.45], wp(9 / 1.6, 3 / 1.6)); back.position.set(0, 0, -3.5); g.add(back);
  // the window: night city (or day garden) behind it, frame, sill, felt curtains
  K.dyn.evVista = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 1.7), vistaMat(nightCityTex(), { yaw: Math.PI, az: Math.PI / 2, el: [-8 * DEG, 32 * DEG], gain: 1.15 }));
  K.dyn.evVista.position.set(-1.6, 1.72, -3.62); g.add(K.dyn.evVista);
  K.dyn.evVistaGun = vistaMat(dayGardenTex(), { yaw: Math.PI, az: Math.PI / 2, el: [-8 * DEG, 32 * DEG], gain: 1.05 }); K.dyn.evVistaGece = K.dyn.evVista.material;
  const fr = flat('#f2ead8'); for (const [sx, sy, x, y] of [[2.26, .1, -1.6, 2.5], [2.26, .12, -1.6, .96], [.1, 1.5, -2.7, 1.72], [.1, 1.5, -.5, 1.72], [.05, 1.45, -1.6, 1.72]]) box(g, sx, sy, .12, x, y, -3.46, fr);
  box(g, 2.5, .06, .26, -1.6, .92, -3.38, flat('#d8ccb4'));
  const curt = flat('#c8505a'); for (const s of [-1, 1]) { const c = box(g, .42, 1.9, .06, -1.6 + s * 1.35, 1.65, -3.38, curt); c.userData.noShadow = true; }
  box(g, 3.2, .05, .05, -1.6, 2.62, -3.36, flat('#5e3a26'));
  // wood wainscot, skirting
  const ws = painted(woodTex({ base: '#8f5a34', plank: 64, vertical: true, rep: [6, 1] })), rail = flat('#5e3a26');
  for (const [w, x, z, ry] of [[3.2, 3.0, -3.45, 0], [8.5, 4.45, .5, -Math.PI / 2], [8.5, -4.45, .5, Math.PI / 2]]) {
    const p = new THREE.Mesh(new THREE.PlaneGeometry(w, .9), ws); p.position.set(x, .45, z); p.rotation.y = ry; g.add(p);
    const r = box(g, w, .05, .07, x, .92, z, rail); r.rotation.y = ry;
  }
  const right = new THREE.Mesh(new THREE.PlaneGeometry(8.5, 3.0), wp(8.5 / 1.6, 3 / 1.6)); right.position.set(4.5, 1.5, .5); right.rotation.y = -Math.PI / 2; g.add(right);
  const left = new THREE.Mesh(new THREE.PlaneGeometry(8.5, 3.0), wp(8.5 / 1.6, 3 / 1.6)); left.position.set(-4.5, 1.5, .5); left.rotation.y = Math.PI / 2; g.add(left);
  const ceil = new THREE.Mesh(new THREE.PlaneGeometry(9, 8.5), flat('#c8cce0')); ceil.rotation.x = Math.PI / 2; ceil.position.set(0, 3.0, .5); g.add(ceil);
  // sofa in front of the window (coral felt), cushions, a coffee table with a bowl of crisps
  const sofa = flat('#d8665a'), sofaD = flat('#b04a44');
  box(g, 2.3, .42, .9, -1.6, .21, -2.75, sofaD); box(g, 2.3, .62, .26, -1.6, .63, -3.12, sofa);
  for (const s of [-1, 1]) box(g, .22, .62, .9, -1.6 + s * 1.15, .31, -2.75, sofa);
  for (const [x, c] of [[-2.15, '#f2c64a'], [-1.05, '#5ab0a0']]) { const k = box(g, .5, .4, .14, x, .7, -2.95, flat(c)); k.rotation.x = -.25; }
  box(g, 1.0, .06, .55, -1.6, .42, -1.3, painted(woodTex({ base: '#9a6a40' }))); for (const [dx, dz] of [[-.42, -.22], [.42, -.22], [-.42, .22], [.42, .22]]) box(g, .05, .4, .05, -1.6 + dx, .2, -1.3 + dz, flat('#5e3a26'));
  const bowl = cyl(g, .16, .1, .1, -1.75, .5, -1.3, flat('#e8e0d0')); for (let k = 0; k < 6; k++) ball(g, .045, -1.75 + Math.cos(k) * .08, .56, -1.3 + Math.sin(k) * .08, flat('#f2c64a'));
  // the TV on a low cabinet against the right side of the window wall
  box(g, 1.1, .5, .4, .35, .25, -3.25, painted(woodTex({ base: '#7a4a2e' })));
  box(g, .95, .58, .06, .35, .84, -3.3, flat('#22223a'));
  K.dyn.tv = new THREE.Mesh(new THREE.PlaneGeometry(.86, .48), new THREE.MeshBasicMaterial({ color: HDR(.25, .35, .7) })); K.dyn.tv.position.set(.35, .84, -3.265); g.add(K.dyn.tv);
  // kitchen along the back wall on the right: counter, top, upper cabinets, kettle, pot; fridge in the corner
  const kc = flat('#e8dcc4'), top = flat('#4a7a8a');
  box(g, 2.4, .86, .62, 2.25, .43, -3.17, kc); box(g, 2.5, .06, .7, 2.25, .89, -3.15, top);
  for (let i = 0; i < 3; i++) { box(g, .74, .7, .02, 1.45 + i * .8, .43, -2.85, flat('#d6c8ae')); cyl(g, .02, .02, .12, 1.45 + i * .8 + .25, .62, -2.83, flat('#5e3a26'), 6).rotation.z = Math.PI / 2; }
  box(g, 2.4, .7, .36, 2.25, 2.05, -3.3, kc); for (let i = 0; i < 3; i++) box(g, .74, .62, .02, 1.45 + i * .8, 2.05, -3.11, flat('#d6c8ae'));
  const tile = new THREE.Mesh(new THREE.PlaneGeometry(2.4, .78), painted(tileTex({ a: '#e8a23a', b: '#f6efe0', ink: '#3a4a6a', rep: [6, 2] }))); tile.position.set(2.25, 1.31, -3.47); g.add(tile);
  cyl(g, .1, .12, .22, 1.55, 1.03, -3.15, flat('#c8323a')); cyl(g, .18, .16, .16, 2.55, 1.0, -3.15, flat('#7a8496'));
  K.dyn.fridge = box(g, .85, 1.95, .72, 3.95, .975, -3.1, flat('#eef2f8'));
  box(g, .04, .5, .05, 3.6, 1.25, -2.72, flat('#9aa4b4')); box(g, .04, .3, .05, 3.6, .55, -2.72, flat('#9aa4b4')); box(g, .85, .02, .02, 3.95, .8, -2.735, flat('#b8c0cc'));
  for (const [x, y, c] of [[4.1, 1.55, '#f2c64a'], [3.85, 1.4, '#86d45a'], [4.15, 1.15, '#f25a9a']]) box(g, .14, .14, .01, x, y, -2.735, flat(c));
  // dining table (round) with two chairs, a fruit bowl
  cyl(g, .55, .55, .05, 2.05, .74, -1.1, painted(woodTex({ base: '#a8744a' })), 32); cyl(g, .06, .1, .72, 2.05, .36, -1.1, flat('#5e3a26'));
  for (const s of [-1, 1]) { box(g, .42, .05, .42, 2.05 + s * .85, .45, -1.1, flat('#c9963e')); box(g, .42, .5, .05, 2.05 + s * .85, .72, -1.1 - .2, flat('#c9963e')); for (const [dx, dz] of [[-.18, -.18], [.18, -.18], [-.18, .18], [.18, .18]]) box(g, .04, .45, .04, 2.05 + s * .85 + dx, .225, -1.1 + dz, flat('#5e3a26')); }
  cyl(g, .18, .12, .1, 2.05, .82, -1.1, flat('#e8e0d0')); for (const [dx, dz, c] of [[-.07, 0, '#e04a3a'], [.07, .03, '#f2a03a'], [0, -.07, '#86d45a']]) ball(g, .07, 2.05 + dx, .9, -1.1 + dz, flat(c));
  // front door on the left wall, a coat rack, a picture on the right wall, a plant
  K.dyn.evKapi = new THREE.Group(); K.dyn.evKapi.position.set(-4.44, 0, .05); g.add(K.dyn.evKapi);   // hinge at the back edge: opens into the room, away from the camera
  const kd = box(K.dyn.evKapi, .06, 2.1, .95, 0, 1.05, .475, painted(woodTex({ base: '#7a4a2e', plank: 96, vertical: true })));
  ball(K.dyn.evKapi, .045, .06, 1.0, .85, flat('#e0b050'));
  // behind the door: a slice of the stairwell (teal wall, tiled floor, a warm lamp), seen only when the door opens (kapi(K, k))
  const hall = new THREE.Mesh(new THREE.PlaneGeometry(.95, 2.1), new THREE.MeshBasicMaterial({ map: canvasTex(190, 420, (c, w, h) => {
    const gr = c.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#6f9488'); gr.addColorStop(.7, '#8ab4a6'); gr.addColorStop(1, '#5a7a70'); c.fillStyle = gr; c.fillRect(0, 0, w, h);
    const lg = c.createRadialGradient(w * .5, h * .2, 4, w * .5, h * .2, w * .9); lg.addColorStop(0, 'rgba(255,214,150,.75)'); lg.addColorStop(1, 'rgba(255,214,150,0)'); c.fillStyle = lg; c.fillRect(0, 0, w, h);
    c.fillStyle = '#c86a4a'; c.fillRect(0, h * .82, w, h * .18); c.fillStyle = '#f2ead8'; for (let i = 0; i < 6; i++) c.fillRect(i * w / 5 - 4, h * .82, 6, h * .18);
    c.fillStyle = '#5e3a26'; c.fillRect(0, h * .55, w, 8); c.fillStyle = 'rgba(0,0,0,.25)'; c.fillRect(0, 0, 10, h); c.fillRect(w - 10, 0, 10, h);
  }), color: HDR(.85, .85, .85) }));
  hall.position.set(-4.488, 1.05, .525); hall.rotation.y = Math.PI / 2; g.add(hall);
  for (const [sy, sz, y, z] of [[.1, 1.15, 2.15, .48], [2.2, .1, 1.1, 1.05], [2.2, .1, 1.1, -.05]]) box(g, .1, sy, sz, -4.42, y, z + .02, flat('#f2ead8'));
  cyl(g, .03, .03, 1.7, -4.2, .85, 1.75, flat('#5e3a26')); ball(g, .14, -4.2, 1.6, 1.75, flat('#3a6aa8')); ball(g, .12, -4.15, 1.4, 1.85, flat('#c8505a'));
  const pic = new THREE.Mesh(new THREE.PlaneGeometry(1.0, .7), new THREE.MeshBasicMaterial({ map: canvasTex(256, 180, (c, w, h) => { c.fillStyle = '#f6efe0'; c.fillRect(0, 0, w, h); c.fillStyle = '#86b8e0'; c.fillRect(14, 14, w - 28, h * .55); c.fillStyle = '#5ab06a'; c.beginPath(); c.moveTo(14, h - 14); c.lineTo(w * .4, h * .35); c.lineTo(w * .7, h - 14); c.fill(); c.fillStyle = '#f2c64a'; c.beginPath(); c.arc(w * .75, h * .3, 18, 0, 6.29); c.fill(); c.strokeStyle = '#5e3a26'; c.lineWidth = 14; c.strokeRect(0, 0, w, h); }), color: HDR(.8, .78, .76) }));
  pic.position.set(4.46, 1.75, -.6); pic.rotation.y = -Math.PI / 2; g.add(pic);
  cyl(g, .22, .17, .42, -3.9, .21, -3.0, flat('#c8663a')); for (const [dx, dy, r] of [[0, .7, .32], [-.13, .98, .24], [.12, 1.1, .2]]) ball(g, r, -3.9 + dx, dy, -3.0, flat('#3f9a48'));
  // lights: cool fill, floor lamp by the sofa, pendant over the kitchen counter, moon through the window
  L.add(new THREE.HemisphereLight('#a9b4f0', '#6a5a7a', 1.7));
  cyl(g, .025, .025, 1.6, -3.1, .8, -2.7, flat('#2a2630'), 6); cyl(g, .22, .26, .06, -3.1, .03, -2.7, flat('#2a2630'));
  const fl1 = lamba(g, L, -3.1, 1.75, -2.7, { cord: .02, power: 3.0, shadeCol: '#f2c64a' });
  const fl2 = lamba(g, L, 2.2, 2.3, -2.5, { cord: .55, power: 3.2 });
  const moon = new THREE.DirectionalLight('#8aa0ff', 1.2); moon.position.set(-2, 4, -9); moon.target.position.set(-1, 0, 0); moon.castShadow = true; moon.shadow.mapSize.set(1024, 1024);
  Object.assign(moon.shadow.camera, { left: -6, right: 6, top: 5, bottom: -2, near: 1, far: 20 }); L.add(moon); L.add(moon.target);
  K.dyn.evAy = moon;
  // bozuk para yığını (Zip'in kirası): sehpanın üstünde, para(K, 0..1) ile büyür; 0 iken görünmez
  K.dyn.para = new THREE.Group(); K.dyn.para.position.set(...PARA); g.add(K.dyn.para); K.dyn.para.visible = false;
  { const R = rng(4), gold = [new THREE.MeshLambertMaterial({ color: '#f2c64a', emissive: '#5a4208' }), new THREE.MeshLambertMaterial({ color: '#e0a83a', emissive: '#4a3206' }), new THREE.MeshLambertMaterial({ color: '#d8d8e0', emissive: '#3a3a44' })];
    for (let i = 0; i < 70; i++) { const r = Math.sqrt(R()) * .27, an = R() * 6.29, y = (.27 - r) * .85 * R() + .01;
      const c = cyl(K.dyn.para, .036, .036, .012, Math.cos(an) * r, y, Math.sin(an) * r * .7, gold[i % 3], 12); c.rotation.set((R() - .5) * 1.2, R() * 3, (R() - .5) * 1.2); }
    for (const [x, z, n] of [[.3, .12, 9], [-.31, .1, 6], [.22, .2, 4]]) for (let i = 0; i < n; i++) cyl(K.dyn.para, .036, .036, .012, x, .006 + i * .013, z, gold[(i + n) % 2], 12); }
  K.dyn.evGunes = new THREE.DirectionalLight('#ffe2b0', 0); K.dyn.evGunes.position.set(-2, 5, -9); K.dyn.evGunes.target.position.set(-1, 0, 0); L.add(K.dyn.evGunes); L.add(K.dyn.evGunes.target);
  K.sets.ev = { g, L, keys: [fl1, fl2] };
  shadows(g);
}

// ---------------------------------------------------------------- MERDIVEN (x = 100)
export const MERDIVEN = { hugoKapi: [-1.35, 0, -1.75], sol: [-.7, 0, -1.2], orta: [0, 0, -1.2], sag: [.7, 0, -1.2], basamak: [1.75, .54, -1.75], on: [0, 0, .3] };
function buildMerdiven(scene, K) {
  const g = new THREE.Group(); g.position.x = 100; scene.add(g); const L = new THREE.Group(); L.position.x = 100; scene.add(L);
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(9, 7), painted(tileTex({ a: '#c86a4a', b: '#f2ead8', ink: '#5a3a3a', rep: [9, 7] }))); fl.rotation.x = -Math.PI / 2; fl.position.z = .5; g.add(fl);
  const wp = (rx, ry) => duvarKagidi('#a8c8bc', '#98bcae', { rep: [rx, ry] });
  const back = new THREE.Mesh(new THREE.PlaneGeometry(9, 4.2), wp(9 / 1.6, 4.2 / 1.6)); back.position.set(0, 2.1, -2.6); g.add(back);
  for (const s of [-1, 1]) { const w = new THREE.Mesh(new THREE.PlaneGeometry(7, 4.2), wp(7 / 1.6, 4.2 / 1.6)); w.position.set(s * 4.5, 2.1, .9); w.rotation.y = -s * Math.PI / 2; g.add(w); }
  const ws = painted(woodTex({ base: '#7a5a3e', plank: 64, vertical: true, rep: [6, 1] })); const p = new THREE.Mesh(new THREE.PlaneGeometry(9, .9), ws); p.position.set(0, .45, -2.58); g.add(p); box(g, 9, .05, .07, 0, .92, -2.57, flat('#4e3022'));
  // Hugo's door: dark wood, brass knob, peephole, name plate, a doormat
  K.dyn.hugoKapi = new THREE.Group(); K.dyn.hugoKapi.position.set(-1.35 - .5, 0, -2.55); g.add(K.dyn.hugoKapi);
  box(K.dyn.hugoKapi, 1.0, 2.15, .06, .5, 1.075, 0, painted(woodTex({ base: '#5e3a26', plank: 96, vertical: true })));
  ball(K.dyn.hugoKapi, .05, .85, 1.0, .06, flat('#e0b050')); cyl(K.dyn.hugoKapi, .03, .03, .02, .5, 1.6, .04, flat('#2a2630')).rotation.x = Math.PI / 2;
  const plate = new THREE.Mesh(new THREE.PlaneGeometry(.5, .16), new THREE.MeshBasicMaterial({ map: yaziTex('HUGO', { bg: '#e0b050', fg: '#3a2418', border: '#3a2418' }), color: HDR(.9, .88, .85) })); plate.position.set(.5, 1.82, .04); K.dyn.hugoKapi.add(plate);
  for (const [sx, sy, x, y] of [[1.2, .1, -1.35, 2.2], [.1, 2.2, -1.95, 1.1], [.1, 2.2, -.75, 1.1]]) box(g, sx, sy, .1, x, y, -2.55, flat('#f2ead8'));
  const mat = new THREE.Mesh(new THREE.PlaneGeometry(.9, .5), painted(carpetTex({ base: '#8a3a3a', band: '#f0b84a', rows: 1 }))); mat.rotation.x = -Math.PI / 2; mat.position.set(-1.35, .006, -2.15); g.add(mat);
  // stairs up along the back wall on the right, a banister
  const st = painted(woodTex({ base: '#a8744a' }));
  for (let i = 0; i < 9; i++) box(g, .32, .18 * (i + 1), 1.1, .9 + i * .32, .09 * (i + 1), -2.0, st);
  const rail = flat('#4e3022'); for (let i = 0; i < 9; i += 2) box(g, .04, .9, .04, .9 + i * .32, .18 * (i + 1) + .45, -1.47, rail);
  const r = box(g, 3.1, .07, .07, 2.15, 1.55, -1.47, rail); r.rotation.z = Math.atan2(.18, .32);
  // a high window at the top of the stairs (night), a wall lamp, a radiator, a plant
  const win = new THREE.Mesh(new THREE.PlaneGeometry(1.0, 1.0), vistaMat(nightCityTex({ seed: 5 }), { yaw: Math.PI, az: Math.PI / 2.4, el: [0, 40 * DEG], gain: 1.1 })); win.position.set(3.0, 2.9, -2.62); g.add(win);
  for (const [sx, sy, x, y] of [[1.16, .08, 3.0, 3.44], [1.16, .08, 3.0, 2.36], [.08, 1.16, 2.46, 2.9], [.08, 1.16, 3.54, 2.9], [.04, 1.0, 3.0, 2.9]]) box(g, sx, sy, .08, x, y, -2.58, flat('#f2ead8'));
  for (let i = 0; i < 6; i++) box(g, .08, .55, .1, -3.3 + i * .14, .55, -2.5, flat('#e8eef8'));
  cyl(g, .2, .16, .4, -3.9, .2, -2.2, flat('#c8663a')); for (const [dx, dy, r2] of [[0, .65, .3], [.12, .9, .22]]) ball(g, r2, -3.9 + dx, dy, -2.2, flat('#3f9a48'));
  L.add(new THREE.HemisphereLight('#a9c4e8', '#6a5a7a', 1.6));
  box(g, .3, .05, .2, 0, 2.15, -2.5, flat('#2a2630'));
  const sh = new THREE.Mesh(new THREE.SphereGeometry(.16, 18, 12, 0, 6.29, 0, Math.PI / 2), new THREE.MeshBasicMaterial({ color: HDR(2.0, 1.6, .9) })); sh.position.set(0, 2.15, -2.42); sh.rotation.x = Math.PI; sh.userData.noShadow = true; g.add(sh);
  const pl = new THREE.PointLight('#ffc884', 3.6, 7, 1.5); pl.position.set(0, 2.0, -2.2); pl.castShadow = true; pl.shadow.mapSize.set(1024, 1024); pl.shadow.bias = -.003; pl.shadow.radius = 4; L.add(pl);
  K.sets.merdiven = { g, L, keys: [V(100, 2.0, -2.2)] };
  shadows(g);
}

// ---------------------------------------------------------------- SOKAK (x = 200), gün batımı
export const SOKAK = { bakkalKapi: [0, 0, -1.55], sol: [-1.0, 0, -.5], orta: [0, 0, -.5], sag: [1.0, 0, -.5], kasa: [1.9, 0, -1.2], uzakSol: [-3.5, 0, -.3], uzakSag: [3.5, 0, -.3] };
function buildSokak(scene, K) {
  const g = new THREE.Group(); g.position.x = 200; scene.add(g); const L = new THREE.Group(); L.position.x = 200; scene.add(L);
  const sky = new THREE.Mesh(new THREE.PlaneGeometry(90, 34), new THREE.MeshBasicMaterial({ map: canvasTex(64, 256, (c, w, h) => {
    const gr = c.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#3a4a9a'); gr.addColorStop(.55, '#c87a9a'); gr.addColorStop(.8, '#ffb46a'); gr.addColorStop(1, '#ffd08a'); c.fillStyle = gr; c.fillRect(0, 0, w, h); }) }));
  sky.position.set(0, 11, -16); g.add(sky);
  const walk = new THREE.Mesh(new THREE.PlaneGeometry(60, 6), painted(stoneTex({ base: '#d8c8b0', seam: '#8a7a6a', bw: 128, bh: 128, rep: [30, 3] }))); walk.rotation.x = -Math.PI / 2; walk.position.set(0, 0, .5); g.add(walk);
  const road = new THREE.Mesh(new THREE.PlaneGeometry(60, 8), painted(stoneTex({ base: '#5a5a7a', seam: '#3a3a5a', bw: 256, bh: 64, rep: [15, 2] }))); road.rotation.x = -Math.PI / 2; road.position.set(0, -.01, 7.5); g.add(road);
  // the shop: facade, awning stripes, sign, window with shelves, door, fruit crates on the pavement
  const f = flat('#e9d2a8'); box(g, 6.4, 3.6, .3, 0, 1.8, -2.4, f);
  const sign = new THREE.Mesh(new THREE.PlaneGeometry(3.2, .7), new THREE.MeshBasicMaterial({ map: yaziTex('BAKKAL', { w: 1024, h: 224, size: 150, bg: '#2f6a8a', fg: '#ffe9b0' }), color: HDR(1.0, .98, .95) })); sign.position.set(0, 3.15, -2.23); g.add(sign);
  const awT = canvasTex(256, 64, (c, w, h) => { for (let x = 0; x < w; x += 32) { c.fillStyle = (x / 32) % 2 ? '#f6efe0' : '#c8323a'; c.fillRect(x, 0, 32, h); } });
  awT.wrapS = THREE.RepeatWrapping; awT.repeat.set(3, 1);
  const aw = new THREE.Mesh(new THREE.PlaneGeometry(5.6, 1.0), new THREE.MeshLambertMaterial({ map: awT, side: THREE.DoubleSide })); aw.position.set(0, 2.55, -1.85); aw.rotation.x = -.85; g.add(aw);
  const glass = new THREE.MeshBasicMaterial({ color: HDR(1.25, 1.05, .7) });
  const win = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 1.4), glass); win.position.set(-1.6, 1.45, -2.24); g.add(win);
  for (let r = 0; r < 3; r++) { box(g, 2.1, .04, .1, -1.6, .9 + r * .45, -2.22, flat('#7a4a2e')); for (let k = 0; k < 7; k++) box(g, .16, .22, .08, -2.5 + k * .3, 1.03 + r * .45, -2.2, flat(['#e04a3a', '#f2c64a', '#3a8ad8', '#86d45a', '#f25a9a'][(k + r) % 5])); }
  for (const [sx, sy, x, y] of [[2.4, .1, -1.6, 2.18], [2.4, .1, -1.6, .72], [.1, 1.5, -2.75, 1.45], [.1, 1.5, -.45, 1.45]]) box(g, sx, sy, .1, x, y, -2.2, flat('#2f6a8a'));
  K.dyn.bakkalKapi = box(g, 1.1, 2.1, .06, .9, 1.05, -2.22, flat('#2f6a8a'));
  const dg = new THREE.Mesh(new THREE.PlaneGeometry(.8, 1.2), glass); dg.position.set(.9, 1.35, -2.18); g.add(dg);
  const crate = painted(woodTex({ base: '#c9963e' }));
  for (const [x, y, c] of [[1.95, .2, '#e04a3a'], [2.6, .2, '#f2a03a'], [2.28, .58, '#86d45a']]) {
    box(g, .6, .36, .45, x, y, -1.7, crate); for (let k = 0; k < 6; k++) ball(g, .09, x - .2 + (k % 3) * .2, y + .2, -1.78 + Math.floor(k / 3) * .16, flat(c));
  }
  // neighbouring houses left and right, behind: a row of facades
  const R = rng(9), cols = ['#e9b07a', '#9ab8d8', '#e8d8a0', '#d88a7a', '#a8c8a0', '#c8a8d8'];
  for (let i = 0; i < 10; i++) {
    const x = (i < 5 ? -1 : 1) * (5.6 + (i % 5) * 4.6), w = 4.2, h = 4.5 + R() * 3;
    const b = new THREE.Mesh(new THREE.BoxGeometry(w, h, 3), painted(wallTex({ base: cols[i % 6], frame: '#4a4458', cols: 2, rows: [1, 2], night: false }))); b.position.set(x, h / 2, -3.9); g.add(b);
    const roof = new THREE.Mesh(new THREE.ConeGeometry(w * .75, 1.2, 4), flat('#8a3a3a')); roof.rotation.y = Math.PI / 4; roof.position.set(x, h + .6, -3.9); g.add(roof);
  }
  for (const x of [-9, 9, -18, 18]) { const b = new THREE.Mesh(new THREE.BoxGeometry(5, 9, 3), painted(wallTex({ base: '#b8a8c8', frame: '#4a4458', cols: 3, rows: [1, 3] }))); b.position.set(x * 1.3, 4.5, -12); g.add(b); }
  for (const x of [-3.6, 3.6, -11, 11]) {
    cyl(g, .05, .06, 3.2, x, 1.6, -.9, flat('#2a2630'), 8);
    const lp = ball(g, .14, x, 3.25, -.9, new THREE.MeshBasicMaterial({ color: HDR(2.6, 2.0, 1.0) })); lp.userData.noShadow = true;
  }
  for (const x of [-7, 7]) { cyl(g, .08, .1, 1.6, x, .8, -1.2, flat('#6a4a3a'), 8); ball(g, .85, x, 2.2, -1.2, flat('#4a9a4a')); }
  box(g, 1.4, .08, .45, -2.2, .45, -1.5, painted(woodTex({ base: '#8f5a34' }))); for (const s of [-1, 1]) box(g, .06, .45, .4, -2.2 + s * .6, .225, -1.5, flat('#3a3040'));
  L.add(new THREE.HemisphereLight('#a6b4ff', '#7a6a8a', 1.8));
  const sun = new THREE.DirectionalLight('#ffb460', 3.2); sun.position.set(12, 6, 4); sun.target.position.set(0, 0, -1); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -10, right: 10, top: 7, bottom: -3, near: 1, far: 40 }); sun.shadow.bias = -.0006; sun.shadow.radius = 3; L.add(sun); L.add(sun.target);
  K.sets.sokak = { g, L, keys: [V(-12, -6, -4).normalize()], dir: true };
  shadows(g);
}

// ---------------------------------------------------------------- ELDE TUTULANLAR (propR / propL: 'cips', 'kilavuz', 'kek')
// 2B çizilir (karakter kartının içinde), elin etrafında; yeni bir eşya gerekiyorsa buraya ekle.
TOON_PROPS.cips = (g, x, y, s) => { g.save(); g.translate(x, y - 40); g.rotate(-.15 * s); g.fillStyle = '#e04a3a'; g.strokeStyle = PLUM; g.lineWidth = 5;
  g.beginPath(); g.moveTo(-34, -46); g.lineTo(34, -46); g.lineTo(28, 46); g.lineTo(-28, 46); g.closePath(); g.fill(); g.stroke();
  g.fillStyle = '#f2c64a'; g.beginPath(); g.ellipse(0, 0, 20, 14, 0, 0, 6.29); g.fill(); g.stroke();
  for (const [dx, dy] of [[-14, -52], [4, -58], [18, -50]]) { g.fillStyle = '#f6d36a'; g.beginPath(); g.ellipse(dx, dy, 11, 7, dx * .05, 0, 6.29); g.fill(); g.stroke(); } g.restore(); };
TOON_PROPS.kilavuz = (g, x, y, s) => { g.save(); g.translate(x, y - 50); g.rotate(-.12 * s); g.fillStyle = '#5a7ae0'; g.strokeStyle = PLUM; g.lineWidth = 5;
  g.beginPath(); g.roundRect(-44, -58, 88, 116, 8); g.fill(); g.stroke(); g.fillStyle = '#fbf6ea'; g.fillRect(-32, -42, 64, 20);
  g.fillStyle = '#f25a9a'; g.beginPath(); g.arc(0, 18, 16, 0, 6.29); g.fill(); g.stroke(); g.strokeStyle = '#fbf6ea'; g.lineWidth = 3; g.beginPath(); g.ellipse(0, 18, 28, 8, -.3, 0, 6.29); g.stroke(); g.restore(); };
TOON_PROPS.kek = (g, x, y, s) => { g.save(); g.translate(x, y - 30); g.fillStyle = '#c9963e'; g.strokeStyle = PLUM; g.lineWidth = 5;
  g.beginPath(); g.moveTo(-34, 0); g.lineTo(34, 0); g.lineTo(26, 40); g.lineTo(-26, 40); g.closePath(); g.fill(); g.stroke();
  g.fillStyle = '#f6efe0'; g.beginPath(); g.ellipse(0, -4, 38, 22, 0, Math.PI, 0); g.fill(); g.stroke(); g.fillStyle = '#e04a3a'; g.beginPath(); g.arc(0, -28, 9, 0, 6.29); g.fill(); g.stroke(); g.restore(); };

// el ilanı: "KİRALIK ODA" (yazı ters dönmesin diye ilanı tutan karaktere flip verme)
TOON_PROPS.ilan = (g, x, y, s) => { g.save(); g.translate(x, y - 70); g.rotate(-.06 * s); g.fillStyle = '#fbf6ea'; g.strokeStyle = PLUM; g.lineWidth = 5;
  g.beginPath(); g.roundRect(-92, -64, 184, 128, 8); g.fill(); g.stroke(); g.fillStyle = '#c8323a'; g.fillRect(-92, -64, 184, 16);
  g.fillStyle = '#2a2a4a'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.font = '700 40px Poppins, "Arial Black", sans-serif'; g.fillText('KİRALIK', 0, -10); g.fillText('ODA', 0, 32); g.restore(); };

// ---------------------------------------------------------------- KUR (story.setup içinde)
// Sahneyi, oyuncuları ve yazı tiplerini kurar. K = { cast, sets, dyn, where }
export async function kur(ctx) {
  await UK.hazirla();
  const { scene } = ctx; scene.background = new THREE.Color('#1a1f3a');
  const K = { cast: {}, sets: {}, dyn: {}, ctx, where: 'ev' };
  buildEv(scene, K); buildMerdiven(scene, K); buildSokak(scene, K);
  for (const [k, l] of Object.entries(LOOK)) K.cast[k] = new OrguToon(l, scene);
  return K;
}
// Bölüm süresi: zaman çizelgesinin sonu + kısa kuyruk (kare sayısına yuvarlanır)
export const sure = (ctx, tail = .4) => Math.ceil((ctx.timeline.total + tail) * 30) / 30;

// ---------------------------------------------------------------- ZAMAN (ses.py zaman çizelgesi, kopru.py ile gelir)
// S('t3') replik başı, E('t3') replik sonu, B('kapi') sessiz vuruş [baş, son], SC(4) 4. sahnenin başı,
// on('t3', t) replik sürüyor mu, kim(t) o an konuşan kod, agiz('T', t) Tobi'nin ağız açıklığı, W('pasta', 2) kelime saati.
export function zaman(ctx) {
  const T = ctx.timeline; if (!T) throw new Error('voice/timeline.json yok: önce tools/kopru.py çalıştır');
  const L = {}; for (const l of T.lines) L[l.id] = l;
  const need = id => { if (!L[id]) throw new Error('replik yok: ' + id); return L[id]; };
  const norm = s => s.toLocaleLowerCase('tr-TR').replace(/[^\p{L}\p{N}]/gu, '');
  return {
    T, L, total: T.total,
    S: id => need(id).start, E: id => need(id).end,
    B: n => { if (!T.beats[n]) throw new Error('vuruş yok: ' + n); return T.beats[n]; },
    SC: n => { if (T.scenes[n] == null) throw new Error('sahne yok: ' + n); return T.scenes[n]; },
    on: (id, t) => t >= need(id).start && t < need(id).end,
    kim: t => (T.lines.find(l => t >= l.start && t < l.end) || {}).spk || null,
    agiz: (spk, t) => flap((ctx.env && ctx.env[spk]) || [], t, ctx.fps),
    W: (w, n = 1) => { let k = 0; for (const x of ctx.words) if (norm(x.word) === norm(w) && ++k === n) return x.start; throw new Error('kelime yok: ' + w); },
  };
}

// ---------------------------------------------------------------- MEKÂN, OYUNCU, CANLILIK
export function mekan(K, where) {
  K.where = where;
  for (const [k, s] of Object.entries(K.sets)) { s.g.visible = k === where; s.L.visible = k === where; }
  for (const c of Object.values(K.cast)) c.hide();
}
// ev kapısı: k 0 kapalı .. 1 açık (içeri doğru döner, arkasında merdiven koridoru görünür)
export function kapi(K, k) { K.dyn.evKapi.rotation.y = 1.45 * Math.max(0, Math.min(1, k)); }
// ev: gündüz (k = 1) ya da gece (k = 0). Pencerenin manzarası, güneş ve ay ışığı değişir.
export function gunduz(K, k) {
  K.dyn.evVista.material = k > .5 ? K.dyn.evVistaGun : K.dyn.evVistaGece;
  K.dyn.evGunes.intensity = 2.3 * k; K.dyn.evAy.intensity = 1.2 * (1 - k);
  K.tint = k > .5 ? [1.06, 1.03, .98] : null;
}
// bozuk para yığını: k 0 yok .. 1 tam (dökülürken backOut ile büyüt)
export function para(K, k) { K.dyn.para.visible = k > .01; K.dyn.para.scale.set(Math.max(.01, k), Math.max(.01, k), Math.max(.01, k)); }
export const mekanOf = cam => cam.position.x < 50 ? 'ev' : cam.position.x < 150 ? 'merdiven' : 'sokak';
const KOD = Object.fromEntries(Object.entries(SPK).map(([s, k]) => [k, s]));
const SEED = { luna: 3, tobi: 7, zip: 11, hugo: 17 };
// Konuşma ve nefes: göz kırpma, ağız (yalnızca kendi repliğinde), konuşurken hafif baş sallama ve kol hareketi,
// Zip'in antenleri, Hugo'nun burnu, Tobi'nin göbeği. Sahnedeki ifade ve pozu bunun üstüne yaz: { ...canli(...), expr: 'laugh' }
export function canli(Z, k, t, { swaps = [] } = {}) {
  const spk = KOD[k], sd = SEED[k] || 1, m = spk ? Z.agiz(spk, t) : 0, talking = spk && Z.kim(t) === spk;
  return {
    blink: blinkAt(t, sd, swaps, 30), mouth: m,
    tilt: talking ? Math.sin(t * 2.6 + sd) * 3.5 : Math.sin(t * .9 + sd) * 1.2,
    bob: -Math.abs(Math.sin(t * (talking ? 5.5 : 1.7) + sd)) * (talking ? 6 : 3),
    armR: talking ? [26 + Math.sin(t * 3.1 + sd) * 14, 30 + Math.sin(t * 4.3) * 18] : [16, 8], armL: [16, 8],
    antT: t, sniffT: t, jiggleT: t, jiggle: k === 'tobi' ? .6 : 0,
  };
}
// bir oyuncuyu göster, yerleştir, gölgesini ışığa çevir ve çiz.
//   pos [x, y, z] mekânın içindeki yer (mekânın x'i kendiliğinden eklenir); p çizim parametreleri; scale 1 = boyu
export function oyna(K, k, pos, cam, p = {}, { scale = 1, pitch = 0 } = {}) {
  const c = K.cast[k], s = K.sets[K.where], ox = SET_X[K.where];
  c.show(); c.place(pos[0] + ox, pos[1], pos[2], cam, K.tint || [1, 1, 1], scale, pitch);
  if (s.dir) c.castFrom(s.keys[0], true);
  else { let best = s.keys[0], d = 1e9; for (const q of s.keys) { const e = Math.hypot(q.x - pos[0] - ox, q.z - pos[2]); if (e < d) { d = e; best = q; } } c.castFrom(best); }
  c.draw({ ...ISIK[K.where], ...p });
  return c;
}
// ışık parametreleri: anahtar ışığın tarafı, lambanın sıcak kenar ışığı
const ISIK = {
  ev: { lit: -1, rim: { color: '#ffb45a', a: .35 } },
  merdiven: { lit: 1, rim: { color: '#ffb45a', a: .3 } },
  sokak: { lit: 1, rim: { color: '#ffb46a', a: .45 } },
};
// yürüme: t0..t1 arasında a'dan b'ye; { pos, walk, flip, lean } döner. walk adım döngüsüdür (bacaklar gerçekten adım atar).
export function yuru(t, t0, t1, a, b, { adim = 2.2 } = {}) {
  const u = Math.max(0, Math.min(1, (t - t0) / (t1 - t0))), e = smoother(u);
  const pos = a.map((v, i) => v + (b[i] - v) * e), moving = u > 0 && u < 1;
  const dist = Math.hypot(b[0] - a[0], b[2] - a[2]);
  return { pos, walk: moving ? e * dist * adim * Math.PI : null, flip: b[0] < a[0], lean: moving ? 3 : 0, moving };
}

// ---------------------------------------------------------------- KAMERA PLANLARI
// plan('ev.kanepe', ctx) -> { pos, look, fov } CamPath anahtarına yayılır: { t: S('t2'), move: 'whip', dur: .3, ...plan('ev.kanepe', ctx) }
// Yatayda aynı plan biraz daha dar açıyla çekilir (karakterler yatay kadrajda da aynı boyda kalır, yanlar dekorla dolar).
const PLAN = {
  'ev.genis': [[0, 1.95, 4.4], [0, 1.15, -2.0], 58], 'ev.kanepe': [[-1.5, 1.45, 1.4], [-1.6, 1.05, -2.4], 46], 'ev.mutfak': [[2.7, 1.5, .9], [2.8, 1.15, -2.8], 46],
  'ev.masa': [[2.0, 1.45, 1.5], [2.05, 1.05, -1.1], 46], 'ev.kapi': [[-1.4, 1.5, 1.9], [-3.9, 1.15, .45], 46], 'ev.pencere': [[-1.0, 1.5, .6], [-1.6, 1.5, -3.5], 44],
  'merdiven.genis': [[0, 1.8, 3.8], [.2, 1.25, -2.0], 56], 'merdiven.kapi': [[-.4, 1.5, 1.3], [-1.35, 1.2, -2.4], 44], 'merdiven.basamak': [[.9, 1.65, 1.3], [2.0, 1.5, -2.0], 46],
  'sokak.genis': [[0, 1.85, 5.2], [0, 1.45, -2.0], 56], 'sokak.bakkal': [[.2, 1.5, 2.4], [0, 1.3, -2.2], 46], 'sokak.kasa': [[1.2, 1.4, 1.6], [2.2, .9, -1.6], 44],
};
export function plan(ad, ctx, { dx = 0, dz = 0, fov = null } = {}) {
  const P = PLAN[ad]; if (!P) throw new Error('plan yok: ' + ad);
  const ox = SET_X[ad.split('.')[0]], f = fov || P[2];
  return { pos: [P[0][0] + ox + dx, P[0][1], P[0][2] + dz], look: [P[1][0] + ox + dx, P[1][1], P[1][2] + dz], fov: ctx.LAND ? f * .78 : f };
}
// bir karakterin yakın planı: x, z karakterin yeri, h kameranın yüksekliği, yan -1 / 1 kameranın kaydığı taraf
// (uzak 3.0: baş ve gövdenin üstü; uzak 2.3: yalnızca yüz, tepki anları; uzak 3.8: boydan)
export function yakin(where, pos, ctx, { h = 1.3, uzak = 3.0, yan = .35, fov = 40 } = {}) {
  const ox = SET_X[where];
  return { pos: [pos[0] + ox + yan, h, pos[2] + uzak], look: [pos[0] + ox, h - .18, pos[2]], fov: ctx.LAND ? fov * .8 : fov };
}
// iki kişilik plan: a ve b arasına bakar
export function ikili(where, a, b, ctx, { h = 1.4, uzak = 3.6, fov = 44 } = {}) {
  const ox = SET_X[where], mx = (a[0] + b[0]) / 2, mz = (a[2] + b[2]) / 2;
  return { pos: [mx + ox, h, mz + uzak], look: [mx + ox, h - .2, mz], fov: ctx.LAND ? fov * .8 : fov };
}

// ---------------------------------------------------------------- GÖRÜNTÜ AYARI (frame() dönüşü)
const GRADE = { ev: [1.02, 1.0, .98], merdiven: [1.0, 1.0, .99], sokak: [1.04, .99, .96] };
export function bak(K, cam, cp, { odak = 2.6, blur = true } = {}) {
  const p = cam.position.clone().add(V(0, 0, -1).applyQuaternion(cam.quaternion).multiplyScalar(odak));
  const look = { focus: cam.position.distanceTo(p), coc: 4.5, range: 2.2, sat: 1.28, lift: [.105, .095, .16], bloom: K.where === 'sokak' ? .8 : .85, vignette: .22 };
  look.tint = GRADE[K.where]; look.blur = blur && cp.moving > .15 ? 12 : 0;
  return look;
}

// ---------------------------------------------------------------- ÜST KATMAN (story.overlay)
// o = { kanca: 'EN FAZLA BEŞ KELİME?', bolum: 1, abone: [t0, ...], aboneSon: [t0, [x, y]] | null, kartlar: [{ t0, t1, lines, cy }] }
export function ustKatman(g, t, ctx, o) {
  const { W, H } = ctx;
  if (o.kanca) UK.kancaYazisi(g, t, W, H, o.kanca);
  if (t > 2.2 && o.bolum) UK.etiket(g, W, H, `${DIZI} · ${o.bolum}. BÖLÜM`, Math.min(1, (t - 2.2) / .3));
  for (const k of o.kartlar || []) UK.kartAc(g, t, k.t0, k.t1, W, H, k.lines, { cy: k.cy });
  for (const a of o.abone || []) UK.abone(g, t, a, W, H);
  if (o.aboneSon) UK.abone(g, t, o.aboneSon[0], W, H, o.aboneSon[1] ? o.aboneSon[1](W, H) : null);
}
export const KART = { baslik: '#ffb0a4', alt: '#faf6ea', soru: '#ffd23f', not: '#b0bee8' };
