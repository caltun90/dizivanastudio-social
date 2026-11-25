// Kiracı Uzaylı: oyuncu kadrosu (dizi boyunca aynı kalır). Konuşmacı kodları senaryo.py ile aynıdır.
export const LOOK = {
  // Luna: evin asıl kiracısı, üniversite öğrencisi, akıllı ve sabırlı; planları o yapar
  luna: { yarn: '#f08a7a', hair: { style: 'uzun', color: '#4a2a3a' }, lashes: true, scarf: '#f2c64a', height: 1.62 },
  // Tobi: oda arkadaşı; şişko, obur, tembel ama iyi kalpli. Göbeği kocaman, elinde hep yiyecek
  tobi: { yarn: '#f2b43c', fat: true, cloth: '#2f9a8e', hair: { style: 'kisa', color: '#6a3a24' }, headR: 158, height: 1.6 },
  // Zip: kiracı uzaylı; minik, yeşil, iki antenli. "Dünyalı Kılavuzu"ndaki her kuralı harfi harfine uygular
  zip: { yarn: '#86d45a', antenna: '#f25a9a', tie: '#5a7ae0', bigEyes: true, headR: 164, height: 1.38 },
  // Hugo: ev sahibi, alt katta oturur; iri, kalın, yuvarlak burnuyla her kokuyu alır (kokladıkça burun delikleri açılır), kuşkucu, bıyıklı
  hugo: { yarn: '#a88ad8', nose: { size: 1.25, color: '#d48ab4' }, mustache: '#3a2a3a', glasses: true, hair: { style: 'kisa', color: '#8a8aa0' }, headR: 150, height: 1.8 },
};
export const SPK = { L: 'luna', T: 'tobi', Z: 'zip', H: 'hugo' };            // N anlatıcının kartı yok
export const NAMES = { L: 'Luna', T: 'Tobi', Z: 'Zip', H: 'Hugo', N: 'Anlatıcı' };
export const COLORS = { L: '#ffb0a4', T: '#ffd36a', Z: '#b6f08a', H: '#d4bcff', N: '#e8e2d4' };
