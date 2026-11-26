# dizivanastudio görüntü motoru (örgü karakterler + 3B dünya)

Cem 25 Kasım 2026'da istedi: dizinin örgü karakterleri Demek O Yüzden'deki gibi hareketli, ifadeli ve komik olsun. Kiracı Uzaylı dizisinden itibaren bölümlerin GÖRÜNTÜSÜ bu klasördeki motorla üretilir. Senaryo (`diziler/<dizi>/bNN/senaryo.py`) ve ses (`motor/ses.py`) eskisi gibidir; `bolum.py`, `uret.py`, `sinema.py`, `motor/orgu.py` yalnızca eski diziler için arşivdir.

Motor: [kodlaciz/yumurta-stili](https://github.com/kodlaciz/yumurta-stili) (MIT, `LICENSE`). Üç.js ile 3B setler, karakterler 2B kart (`engine/src/orgu.js`: örgü ilmekli top kafa, örgü kollar ve bacaklar, işlemeli yüz). Kanala özel: dikey ve yatay aynı hikâyeden, konuşanın adı ve vurgu kelimeli altyazı, kişi başına ağız senkronu, kanca yazısı, dizi etiketi, abone bandı, kartlar, GitHub Actions'ta paralel render.

Cem'e yazılan her şey Türkçe, kısa ve sade; uzun tire (em dash) asla kullanılmaz.

## Klasörler
```
yumurta/
  engine/                 motor (render.mjs, faces.mjs, src/orgu.js karakterler, src/captions.js altyazı)
  lib/dizi.js             üst katman: kanca yazısı, etiket, abone bandı, kartlar (+ logo, Poppins)
  tools/kopru.py          ses.py çıktısını motora taşır (zaman çizelgesi, kelimeler, ağız zarfları, miks)
  diziler/<dizi>/         dizinin kadrosu (kadro.js) ve ortak dosyası (ortak.js: setler, planlar, yardımcılar)
  stories/<dizi>-bNN/     bölümün hikâyesi: story.js + voice/ (kopru.py yazar) + audio/mix.m4a
  stories/uzayli-b00/     ÇALIŞAN ÖRNEK (deneme sahnesi, yayınlanmaz): yeni bölüm bu iskeletle yazılır
  stories/_kadro/         kadro sayfası: node faces.mjs _kadro  ->  stories/_kadro/out/faces.png
.github/workflows/yumurta-render.yml   paralel render (dikey ve yatay)
```

## Akış (bir bölüm)
1. **Senaryo:** `diziler/<dizi>/bNN/senaryo.py`, KIT.md bölüm 4 ile aynı biçim (SEQ, GROUPS, VOICES, NAMES, mix_plan...). Konuşmacı kodları `kadro.js` içindeki `SPK` ile aynıdır (Kiracı Uzaylı: L Luna, T Tobi, Z Zip, H Hugo, N anlatıcı). Sahne numaraları (`('scene', n)`) story.js'te kamera ve mekân değişimine bağlanır.
2. **Ses:** bölüm klasöründe KIT.md bölüm 5 (tts, gaps, check, build). Önce `ses.py dry` ile taslak süre.
3. **Köprü:** depo kökünden `python3 yumurta/tools/kopru.py diziler/<dizi>/bNN yumurta/stories/<dizi>-bNN`. Her `build`'den sonra tekrar çalıştır. (Taslak sesle de çalışır: görüntüyü sesten önce kurabilirsin; gerçek ses gelince yeniden çalıştır, saatler kendiliğinden kayar.)
3b. **Kelime hizalama (WhisperX, Cem 27 Kasım 2026, son `build` + `kopru`'dan sonra):** `kopru.py` kelimeleri satır içinde hecelerle TAHMİN eder; WhisperX her kelimenin sesteki gerçek yerini ölçer (altyazı ve kelimeye bağlı olaylar tam oturur). Bulut oturumu HuggingFace'e ulaşamadığı için GitHub Actions'ta çalışır. `kopru.py` artık `voice/voice.ogg` ve `words.json` içine satır aralıklarını yazar; hikâye klasörünü commit edip main'e push et, sonra:
   ```bash
   gh api -X POST repos/caltun90/dizivanastudio-social/actions/workflows/hizala.yml/dispatches -f ref=main -f 'inputs[klasor]=yumurta/stories/<dizi>-bNN'
   # 2-4 dakika; bitince:
   git fetch -q --depth 1 origin hizalama/<dizi>-bNN && git show FETCH_HEAD:words.json > yumurta/stories/<dizi>-bNN/voice/words.json && git show FETCH_HEAD:hizalama.txt | head -3
   ```
   `kopru.py`'yi bundan sonra yeniden çalıştırırsan ölçüm silinir, hizalamayı tekrarla. İş başarısız olursa ya da 8 dakikada bitmezse tahmini words.json ile devam et ve raporda yaz.
4. **Hikâye:** `yumurta/stories/<dizi>-bNN/story.js`. `stories/uzayli-b00/story.js` dosyasını kopyala, `NAME` değiştir, sahneleri bu bölüme göre yeniden kur. Kurallar aşağıda.
5. **Kare kontrolü** (yarım çözünürlük, hızlı; motor klasöründen):
   ```bash
   cd yumurta/engine && npm ci --ignore-scripts --no-audit --no-fund
   node render.mjs <dizi>-bNN --stills=0,0.5,1,1.9,<her plandan bir saniye> --scale=0.5 --cols=8
   node render.mjs <dizi>-bNN --aspect=16:9 --stills=<aynı saniyeler> --scale=0.5 --cols=4 --name=stills_h.jpg
   ```
   `stories/<dizi>-bNN/out/stills.jpg` ve `stills_h.jpg` dosyalarını Read ile aç, aşağıdaki kontrol listesine göre bak, düzelt, tekrar bak. Bir çalıştırma 10-60 sn sürer.
6. **Render (GitHub Actions):** hikâye klasörünü commit edip main'e push et (`out/` git'e girmez), sonra ikisini birden başlat:
   ```bash
   R=repos/caltun90/dizivanastudio-social
   gh api -X POST $R/actions/workflows/yumurta-render.yml/dispatches -f ref=main -f 'inputs[story]=<dizi>-bNN' -f 'inputs[parts]=20' -f 'inputs[crf]=23' -f 'inputs[aspect]=9:16' -f 'inputs[dal]=render/dikey'
   gh api -X POST $R/actions/workflows/yumurta-render.yml/dispatches -f ref=main -f 'inputs[story]=<dizi>-bNN' -f 'inputs[parts]=20' -f 'inputs[crf]=23' -f 'inputs[aspect]=16:9' -f 'inputs[dal]=render/yatay'
   gh api "$R/actions/runs?per_page=4" --jq '.workflow_runs[] | [.id,.status,.conclusion,.display_title] | @tsv'
   ```
   (`gh workflow run` çalışmaz; yukarıdaki REST çağrısı.) 3 dakikalık bir bölüm yaklaşık 20-35 dakikada biter; 2 dakikada bir bak. Başarısız parça olursa `gh api -X POST $R/actions/runs/<id>/rerun-failed-jobs`; yine olmazsa `gh api $R/actions/jobs/<job_id>/logs` ile hatayı oku.
7. **Teslim al:** artifact indirme bulut oturumunda engelli; video teslim dalındadır:
   ```bash
   git fetch -q --depth 1 origin render/dikey && git show FETCH_HEAD:<dizi>-bNN.mp4 > /tmp/dikey.mp4
   git fetch -q --depth 1 origin render/yatay && git show FETCH_HEAD:<dizi>-bNN.mp4 > /tmp/yatay.mp4
   ```
   100 MB üstü video dalda `<ad>.mp4.part00, part01...` olarak durur: `git ls-tree --name-only FETCH_HEAD`, sırayla `git show` ve `cat`. Depoya konacak dosya 95 MB'ı geçmemeli (GitHub sınırı): geçerse `ffmpeg -i in.mp4 -c:v libx264 -crf 26 -preset medium -c:a copy out.mp4` ile küçült. Dal her render'da üzerine yazılır; dosya adının bu bölüm olduğunu kontrol et.
8. **Son kontrol ve yayın:** KIT.md bölüm 7 (son kontrol) ve 8 (videos/, log.json, Buffer, YouTube).

Render yapılamazsa (Actions iki kez başarısız): aynı hikâyeyi yerelde render et (`node render.mjs <ad> --crf=23` ve `--aspect=16:9 --name=<ad>-yatay`), arka planda çalıştır ve bekle; 2 çekirdekli makinede bölüm başına 2-3 saat sürebilir.

## story.js kuralları

- **Parçacık efektleri (three.quarks, Cem 27 Kasım 2026):** `engine/src/parcacik.js` hazır efektler verir: `konfeti`, `kivilcim`, `parilti`, `toz`, `duman`. Setup'ta `PF = new Parcaciklar(scene); PF.ekle('toz', { t: <replik ya da kelime saati>, pos: [x, 0, z] })`, `frame(t)` içinde kamera uygulandıktan sonra `PF.guncelle(t)`. Komedide en iyi işleyenler: düşme ve çarpışmada `toz`, sinirde kafadan `duman`, fikirde `kivilcim`, sevinçte `konfeti`. Bölümde en fazla 3-4 efekt; konfeti kameradan en az 1,5 m uzakta; efekt yüzü ve altyazıyı kapatmasın. Kare kare kesindir, paralel render'da aynı kare çıkar. Ayrıntı: demekoyuzden-social `yumurta/README.md` 2. bölüm.
- **Hareket zamanlaması:** süre ve yumuşatma seçerken `docs/motion-design/SKILL.md` (LottieFiles, MIT; Disney'in 12 prensibi, süre/easing tabloları). "Creator MCP" önerileri geçersiz.
- **Zaman elle yazılmaz.** `Z = O.zaman(ctx)`: `Z.S('t3')` replik başı, `Z.E('t3')` sonu, `Z.B('pop')` sessiz vuruş `[baş, son]`, `Z.SC(4)` 4. sahnenin başı, `Z.on('t3', t)`, `Z.kim(t)` o an konuşan, `Z.W('pasta', 2)` kelime saati. Olmayan bir ad hata verir (iyi: senaryoyla story.js uyuşmuyor demektir).
- **Kamera:** `new CamPath([...anahtarlar])`. Her anahtar bir sahne ya da repliğe bağlı: `{ t: Z.SC(3), move: 'whip', dur: .3, ...O.plan('ev.mutfak', ctx) }`. Ev kapısı `O.kapi(K, 0..1)` ile açılır (arkasında koridor görünür). Hazır planlar `O.plan('ev.genis' | 'ev.kanepe' | 'ev.mutfak' | 'ev.masa' | 'ev.kapi' | 'ev.pencere' | 'merdiven.genis' | 'merdiven.kapi' | 'merdiven.basamak' | 'sokak.genis' | 'sokak.bakkal' | 'sokak.kasa')`, bir karaktere `O.yakin(mekan, yer, ctx, { uzak })` (3.0 baş ve gövde, 2.3 tepki yüzü, 3.8 boydan), iki kişiye `O.ikili(mekan, a, b, ctx)`. Yatayda aynı plan kendiliğinden biraz daralır (`ctx.LAND`).
  - **Kamera kuralı (Cem, 19 Kasım):** plan içinde kamera yalnızca yavaş iter ve kayar (`creep`, `drift`); yeni açı = yeni anahtar (`whip` 0,25-0,35 sn ya da `cut`). Kamera bir karakteri kare kare izlemez, sallanmaz. Sarsıntı (`cp.kick(t, güç)`) yalnızca kısa olaylarda (kapı vuruşu, zıplama, düşme).
  - Ortalama 3-5 saniyede yeni plan, hiçbir plan 8 saniyeden uzun değil (KIT kural 17). Mekânlar arası geçiş `cut` ya da `whip`.
- **Mekân:** her karede `O.mekan(K, O.mekanOf(cam))`: kameranın bulunduğu set görünür, ötekiler ve bütün oyuncular gizlenir; sonra o karede görünecek oyuncular `O.oyna(...)` ile çizilir.
- **Oyuncu:** `O.oyna(K, 'tobi', EV.kanepe1, cam, { ...O.canli(Z, 'tobi', t), expr: 'laugh', laughMarks: .8, armR: [150, 20] }, { scale })`. `O.canli` göz kırpma, kendi repliğinde ağız, konuşurken baş sallama ve el hareketi, nefes, Zip'in antenleri, Hugo'nun burnu, Tobi'nin göbeği verir; ifade ve poz üstüne yazılır. Yerler mekânın içindeki koordinattır (`O.EV`, `O.MERDIVEN`, `O.SOKAK` hazır yerler; mekânın x'i kendiliğinden eklenir).
  - İfadeler: `neutral smile happy smug focused angry proud surprised worried laugh grin` (Türkçe adlar da çalışır: `sakin mutlu kahkaha endişeli kızgın şaşkın kurnaz gururlu odaklı sırıtma gülümseme`). Bir sahne boyunca tek ifadede kalma; ifade repliğe ve tepkiye göre değişsin, değişimde göz kırpsın (`O.canli(Z, k, t, { swaps: [t1, t2] })`).
  - Poz: `armL / armR: [üst kol açısı (aşağıdan, + dışarı), dirsek]` ör. `[150, 20]` el havada, `[60, 50]` öne uzanmış, `[16, 8]` aşağıda. `lean` (derece), `bob`, `tilt`, `look` (-1 sol .. 1 sağ; yüz ve burun o yöne döner), `lookY`, `flip`, `squash` (-.2 uzar, +.2 basılır), `sweat`, `laughMarks`, `blush`, `sniff` (Hugo'nun burun delikleri açılır), `antUp` (-.4..1, Zip'in antenleri iner ya da fırlar), `antWob` (0..1, antenler yay gibi sallanır), `propL / propR` (`cips`, `kilavuz`, `kek`, `spoon`, `scroll`, `pen`, `lantern`...; yeni eşya `ortak.js` ELDE TUTULANLAR bölümüne).
  - Yürüme: `const y = O.yuru(t, t0, t1, a, b)` sonra `O.oyna(K, k, y.pos, cam, { ...canli, walk: y.walk, flip: y.flip, lean: y.lean })`: bacaklar gerçek adım atar, karakter kaymaz (KIT kural 3).
  - Önce eylem, sonra replik (KIT kural 6): replikte anlatılan şey ekranda görünür.
- **Görüntü ayarı:** `frame()` sonunda `return O.bak(K, cam, cp.apply(...))` (odak, renk, hareket bulanıklığı).
- **Üst katman:** `export function overlay(g, t, ctx) { O.ustKatman(g, t, ctx, { kanca: 'EN FAZLA BEŞ KELİME?', bolum: n, abone: [Z.S('<replik>') + .3], aboneSon: [t0, (W, H) => [W / 2, H * .78]], kartlar: [{ t0, t1, lines: [[metin, punto, renk]] }] }); }`. Başlık kartı `Z.B('title')` içinde, bitiş kartı son sahnede, kılavuz kuralı kartı kuralın okunduğu replikte. Renkler `O.KART`.
- **Altyazı:** `export const CAPTION = { colors: O.COLORS, names: O.NAMES, font: O.FONT };` konuşanın adını renkli etikette, vurgu kelimelerini (senaryodaki `hl`) sarı yamada gösterir. Altyazı dikeyde ekran yüksekliğinin %70'inde, yatayda %86'sında.
- Yeni set parçası, eşya, plan ya da yardımcı başka bölümde de işe yarayacaksa `ortak.js` içine ekle, bölüme özel olanı story.js içinde tut.

## Kontrol listesi (kare kontrolü)
- **İlk 2 saniye:** 0,0 / 0,5 / 1,0 / 1,9 sn karelerinde kanca yazısı okunuyor, karakter görünüyor, hareket var (KIT kural 16).
- **Kadraj:** yüzler ekran yüksekliğinin %30-60'ında; altyazı yüzün üstüne binmiyor; kanca yazısı (üstte) ve abone bandı yüzü kapatmıyor; kafa ve antenler kadrajın kenarında kesilmiyor. Yatayda yanlar dekorla dolu.
- **Oyunculuk:** konuşan karakterin ağzı oynuyor, dinleyen tepki veriyor (ifade, bakış, küçük hareket); kimse uzun süre donuk kalmıyor. Gülme sahnesinde kahkaha çizgileri ve zıplama var.
- **Mekân:** karakter mobilyanın içine girmiyor (kanepenin, masanın önünde duruyor), ayakları zeminde, gölgesi var.
- Her plan değişimi bir sahne ya da repliğe denk geliyor; aynı açı art arda iki kez gelmiyor.
- Türkçe karakterler doğru (ı, İ, ş, ğ, ü, ö, ç).

## Bilinen tuzaklar
- `O.oyna` çağrılmayan oyuncu o karede görünmez (`O.mekan` her karede hepsini gizler); bir sahnede arkadaki karakteri unutma.
- `O.yakin` ile çok yakın (uzak < 2) planda büyük kafa kadrajı doldurur; tepki yüzü için 2.3 yeterli.
- Hugo'nun burnu iri ve yuvarlaktır, yüzün ortasında durur; `look` ile biraz kayar. `sniff` 0..1 burun deliklerini açar; koklama anlarında `sniff: 1` ve `sniff` efekti birlikte.
- Kart (`kartlar`) ve abone bandı aynı anda üst üste gelmesin.
- `kopru.py` her `build`'den sonra çalışmazsa story.js eski saatlerle çalışır ve ses ile görüntü kayar.
- Yerel render arka planda bırakılırsa oturum biterken kesilebilir; tam render her zaman Actions'ta.
