# dizivanastudio: üretim kiti

Kanal: **dizivanastudio** (YouTube). Örgü (tığ işi) görünümlü çizgi karakterlerle kısa animasyon diziler. Her gün 1 yeni bölüm. Her dizinin bölüm sayısı kendi `DIZI.md` dosyasında yazar (13. Kat ve Son Vagon 5, Kiracı Uzaylı 8; Cem 25 Kasım 2026), her bölüm yaklaşık 3 dakika. Bir dizi biter, yenisi başlar. Önce gerilim ve bilimkurgu, sonra komedi.

Bu dosya, bölümü üreten kişinin (çoğu zaman otomatik görev) tek kaynağıdır. Baştan sona oku, sonra işe başla. Cem'e yazılan her şey Türkçe, kısa ve sade olur; uzun tire (em dash) asla kullanılmaz.

> HAFTALIK ANALİZ (Cem, 25 Kasım 2026): İşe başlamadan bu dosyadan sonra `ANALIZ.md` dosyasının "Bu haftanın kararları" bölümünü oku ve uygula. ANALIZ.md yalnızca konu seçimi, kanca, başlık, kapak ve süre tercihlerinde yön verir, bu dosyadaki sınırlar içinde kalır. Bu dosyadaki kurallar, güvenlik, yapay zeka etiketi, video sayısı ve yayın saatleri her zaman önce gelir; çelişirse bu dosya geçerlidir.

> **YENİ GÖRÜNTÜ MOTORU (Cem, 25 Kasım 2026).** Kiracı Uzaylı dizisinden itibaren bölümlerin görüntüsü `yumurta/` motoruyla üretilir: örgü karakterler 3B setlerde, Demek O Yüzden'deki gibi ifadeli, hareketli ve komik (Cem örnek videoyu beğendi: "Bu şekilde yapalım"). **Senaryo (bölüm 4) ve ses (bölüm 5) aynen geçerlidir.** Bölüm 6 (`bolum.py`, sinema katmanı), `uret.py` ve bölüm 7'deki `FMT=v/h ... still` komutları YALNIZCA eski diziler (13. Kat, Son Vagon) içindir. Yeni bölümde görüntü için baştan sona `yumurta/README.md` uygulanır: `tools/kopru.py` (ses -> motor), `stories/<dizi>-bNN/story.js` (örnek: `stories/uzayli-b00`), iki formatta kare kontrolü, GitHub Actions'ta dikey ve yatay paralel render, teslim dalından alma. Bölüm 7'deki kontrol listesi ve bölüm 8 (depo ve yayın) aynen geçerlidir; videolar Actions'tan gelir. Kamera kuralı (19 Kasım) yeni motorda şöyle uygulanır: plan içinde yalnızca yavaş itme ve kayma; yeni açı yeni plan (`whip` ya da `cut`); kamera bir karakteri kare kare izlemez.

## 1. Değişmez kurallar
1. **Tekrar eden kalıp yok.** Bir dizinin bölümleri aynı yapıyı tekrar etmez (YouTube "tekrar eden içerik" kuralı). Her bölümün yapısı dizinin `DIZI.md` dosyasında yazar; ona uy. Yeni dizi yazarken beş bölüme beş farklı yapı ver (düz anlatım, neredeyse diyalogsuz, tek karakterin gözünden, geri dönüşlü, tek mekân gerçek zamanlı, mektup ya da kayıt biçiminde, tersten anlatım gibi).
2. **Yüz ifadesi her zaman var.** Gerilim sahnesinde kimse gülmez; `mutlu` yalnızca gündelik sohbet anında kullanılır, sakin duran karakter için `sakin`.
3. **Yürüme gerçek adım döngüsüdür** (`walk`), zıplama değil. Ayak kaymaz, kollar ters salınır.
4. **Yön her zaman okunur.** Nereden nereye gidildiği belli olur; hedef (kapı, çıkış) sahnenin başında gösterilir.
5. **Karakterler bükülür:** `crouch`, `lean`, `belly` birlikte kullanılır (yeni motorda `lean`, `tilt`, `squash`, `bob`, kol açıları). Düz çubuk gibi durmak varsayılan değildir.
6. **Önce eylem, sonra replik.** "Düğmeler çalışmıyor" denecekse önce biri düğmeye basar ve çalışmadığı görülür.
7. **Geçişler animasyonla gösterilir** (kapı açılır, ışık söner). Önce karakterin tepkisi (1,5 ile 2 sn sessiz), sonra anlatıcı.
8. **Dekorda yanıltıcı ya da anlamsız öğe olmaz.** Ekrandaki her yazı ve kapı hikâyeye hizmet eder.
9. **Mantık açıkça söylenir.** İzleyicinin "neden?" diye soracağı her şey (neden bir üst kata çıkıldı, sayı neden tutmuyor) bir replikle ya da görselle cevaplanır. Sayılar ekranda gösterilir (`tally`, `badge`).
10. **Sesler net ayrılır.** Çocuk, kadın, erkek ve anons sesleri karışmaz (`VOICE_FX`).
11. **Kadın karakter kadın gibi görünür** (saç, kirpik, etek gibi). Karakterler özgündür: gerçek kişi, telifli karakter, başka kanalın karakteri çizilmez.
12. **İsimler uluslararasıdır** (her dilde aynı okunur: Leo, Zoe, Kai, Luna, Sam, Mia, Noa, Max, Eli, Ada, Ren, Nil gibi).
13. **Süre 2:40 ile 2:55 arası.** 3:00'ı geçen video Shorts olamaz; geçerse yayınlama, kısalt.
14. Şiddet, kan, korkutucu ayrıntı yok: gerilim ima ile kurulur (karaltı, sönen ışık, kaybolan kişi). Küfür, siyaset, din, tıbbi tavsiye yok.
15. Kapanışta "yarın" denmez; "bir sonraki bölümde" denir.
16. **İlk 2 saniye kancası (Cem, 19 Kasım 2026; istisnasız her video: dikey, yatay ve film).** İlk 2 saniye izleyiciyi ekrana kilitler. Logo, kanal adı, dizi adı, jenerik, başlık kartı, "Önceki bölümde" hatırlatması, selamlama, boş, siyah ya da hareketsiz kareyle açılmaz; bunlar 2. saniyeden sonra gelir. Abone ol bandı ilk 2 saniyede görünmez.
    - 0:00'daki ilk kare doludur; ses (replik ya da efekt) en geç 0,5. saniyede başlar.
    - Kanca, bölümün en gerilimli anından 1-2 saniyelik bir soğuk açılış ya da bölümün sorusunu cevabı vermeden soran tek bir repliktir (en fazla 8 kelime, 2. saniye dolmadan biter). Cevap bölümün ilerisinde gelir; kancanın verdiği söz mutlaka karşılanır, yanıltıcı tıklama tuzağı yok.
    - İlk karede büyük, okunaklı, en fazla 5 kelimelik bir kanca yazısı ve bölümün en çarpıcı görseli olur; ilk 2 saniyede belirgin bir hareket (hızlı yakınlaşma, giriş animasyonu ya da ani kesme) olur. Kanca yazısı altyazıyla üst üste binmez.
    - Bu kural bu dosyadaki ve `DIZI.md` dosyalarındaki diğer açılış kurallarından önce gelir; çelişirse buna uy. Kural 7'deki 1,5-2 sn sessiz tepki ilk 2 saniyeye uygulanmaz.

17. **Görsel kalite (Cem, 19 Kasım 2026; hedef: film ışığı almış 2.5D çizgi film).** Her bölümde en az 6 farklı mekân ya da açı olur; ortalama 3-5 saniyede bir yeni plan gelir (aynı mekânda farklı açı da sayılır: geniş, yakın, üstten, alttan, kesit). Hiçbir plan 8 saniyeden uzun sabit kalmaz. Aynı koridoru ya da kapıyı bölümün yarısından fazlasında kullanma; her bölüm en az bir yeni mekân ekler (bina dışı gece, asansör boşluğu kesiti, uzun perspektif koridor gibi). Sinema katmanı (bölüm 6) her sahnede açıktır.
- WHISPERX VE EFEKTLER (Cem, 27 Kasım 2026): yumurta düzeninde üretilen bölümlerde son `kopru.py`'den sonra kelime hizalama (`yumurta/README.md` 3b) yapılır; parçacık efektleri (`konfeti`, `kivilcim`, `parilti`, `toz`, `duman`) `yumurta/README.md` "story.js kuralları"ndaki gibi komik anlarda kullanılabilir. Müzik dizinin kendi `music` modlarıyla kalır (sahneye göre değişen besteler).

## 2. Depo düzeni
```
KIT.md                      bu dosya
log.json                    üretilen ve yayınlanan bölümlerin kaydı
motor/                      diziden bağımsız araçlar
  stil.py                   tığ işi çizim temelleri (yarn_limb, yarn_ball), renkler, yazı tipleri
  orgu.py                   karakter motoru (figure, face, poz), sahne dönüşümü, Timeline, altyazı, kart
  ses.py                    Gemini TTS, satırlara bölme, yazıya dökerek kontrol, miks
  uret.py                   iki formatı üretir
  yayin.py                  dikey için Buffer API, yatay için YouTube API
  sheet.py                  kontrol karelerini tek görselde birleştirir
  fonts/                    Poppins
diziler/<dizi>/
  DIZI.md                   dizinin tamamı: dünya, karakterler, sır, 5 bölümün özeti ve yapısı
  ortak.py                  dizinin karakterleri, aksesuarları, pozları, dekorları, yardımcıları
  b01/ b02/ ...             her bölüm: senaryo.py, bolum.py, voice/cuts.json (gerekirse)
videos/                     yayınlanan mp4 dosyaları (<tarih>-<dizi>-b<no>-<slug>-dikey.mp4 ve -yatay.mp4)
yumurta/                    YENİ görüntü motoru (Kiracı Uzaylı'dan itibaren): README.md, engine/, lib/, tools/kopru.py,
  diziler/<dizi>/             kadro.js (karakterler), ortak.js (setler, planlar, yardımcılar)
  stories/<dizi>-bNN/         bölümün story.js dosyası + voice/ + audio/mix.m4a
.github/workflows/yumurta-render.yml   paralel render (dikey ve yatay)
```
Depo herkese açıktır. **Hiçbir anahtar, belirteç ya da parola depoya yazılmaz.**

## 3. Günlük akış
Her çalışmada tek bölüm üretilir ve yayına planlanır.

1. **Hazırlık.** `pip install --break-system-packages skia-python soundfile numpy imageio-ffmpeg`; yeni motor için `cd yumurta/engine && npm ci --ignore-scripts --no-audit --no-fund` (Chrome: `/usr/bin/google-chrome`, kendiliğinden bulunur). `git push --dry-run origin HEAD:main` ile yazma yetkisini sına; reddedilirse dur ve Cem'e bildir. GitHub Actions erişimini sına: `gh api repos/caltun90/dizivanastudio-social/actions/workflows --jq '.workflows[].name'` içinde `yumurta-render` görünmeli.
2. **Sıradaki bölümü bul.** `log.json` içindeki son kayda bak.
   - Son dizinin son bölümü (o dizinin `DIZI.md` dosyasındaki bölüm sayısı) yayınlandıysa: önce o dizinin filmini derle (bölüm 9), sonra **yeni dizi** başlat (bölüm 10). Son Vagon'dan sonraki dizi **Kiracı Uzaylı**dır (Cem, 25 Kasım 2026: komedi, 8 bölüm); `diziler/uzayli/DIZI.md`, `yumurta/diziler/uzayli/kadro.js` ve `ortak.js` hazırdır, yeni dizi yazma, doğrudan b01'den başla.
   - Değilse aynı dizinin sıradaki bölümü. `diziler/<dizi>/DIZI.md` dosyasını ve önceki bölümlerin `senaryo.py` dosyalarını oku (süreklilik: kim gitti, kim ne biliyor, hangi ipucu verildi).
   - Bugünün tarihli kayıt varsa ikinci bölüm üretme, dur.
3. **Senaryo:** `diziler/<dizi>/bNN/senaryo.py` (bölüm 4).
4. **Ses:** bölüm klasöründe `python ../../../motor/ses.py tts`, `gaps`, `check`, `build` (bölüm 5).
5. **Sahneler:** yeni motorda `yumurta/README.md` akış 3-4 (`kopru.py`, sonra `yumurta/stories/<dizi>-bNN/story.js`). Önce `python ../../../motor/ses.py dry` ile taslak zaman çizelgesi çıkarıp sahneleri onunla da kurabilirsin; gerçek ses gelince `build` ve `kopru.py` yeniden. (Eski diziler: `bolum.py`, bölüm 6.)
6. **Kare kontrolü:** README akış 5 (dikey ve yatay `--stills`), kontrol listesi bölüm 7 ve README. Sorun varsa düzelt. Düzelmiyorsa yayınlama, Cem'e bildir.
7. **Üretim:** README akış 6-7: hikâye klasörünü push et, Actions'ta dikey ve yatay render, teslim dallarından al, `videos/<tarih>-<dizi>-b<no>-<slug>-dikey.mp4` ve `-yatay.mp4` olarak koy (her biri 95 MB altında). Sonra son kontrol: süre, ses var mı (`ebur128`, yaklaşık -14 LUFS), iki dosyadan 12'şer kare. (Eski diziler: `uret.py`.)
8. **Depo ve yayın** (bölüm 8).
9. **Rapor:** Cem'e tek kısa mesaj.

## 4. Senaryo (`senaryo.py`)
Örnek: `diziler/kat13/b01/senaryo.py`. Aynı adlar korunur: `TITLE`, `EP`, `EP_NAME`, `SEQ`, `VOICES`, `NAMES`, `GROUPS`, `LINES`, `SEG_ALIAS`, `VOICE_FX`, `TEMPO`, `GAP_SCALE`, `mix_plan(T)`.

- `SEQ` öğeleri: `('scene', no)`, `('beat', ad, süre_sn)` (sessiz aksiyon), `('line', id, konuşan, metin, vurgu_kelimeleri, sonraki_boşluk_sn)`.
- Yaklaşık 40 ile 48 replik, 300 ile 340 kelime, 30 ile 38 sn sessiz aksiyon. İlk tahmin için `ses.py dry` toplamına bak; gerçek ses genelde taslaktan uzun çıkar.
- **İlk 2 saniye kancadır** (kural 16): `SEQ` ilk sahneyle ve kanca repliğiyle başlar, öncesinde sessiz vuruş ya da kart olmaz. Kancanın açtığı merak ilk 15 saniyede büyütülür. Sonra başlık kartı (`('beat', 'title', 2.5)`). Dizinin ilk bölümü değilse kancadan hemen önce ya da sonra tek cümleyle "Önceki bölümde" hatırlatması.
- Bitiş: izleyiciye tek soru + sonraki bölümün adı (kart). Dizinin son bölümünde soru yerine kapanış.
- Replikler kısa, konuşma dilinde. Bir replik en fazla iki cümle. Her karakterin kendine ait bir konuşma biçimi olsun.
- **Ses grupları (`GROUPS`):** Gemini tek istekte en fazla 2 konuşmacı üretir. Replikleri çiftlere böl; grup içinde konuşanlar **sırayla değişmeli** (aynı kişi art arda iki replik söylemesin, yoksa bölme karışır). Grup, sahne sırasını izlemek zorunda değil. Tek konuşmacılı gruplar olabilir (anlatıcı; çifti olmayan artık replikler). Hedef: bölüm başına **en fazla 5 istek**. Grubu 25 saniyeden uzun tutma (uzun isteklerde 502 gelebilir); gerekirse ikiye böl ama toplam 6'yı geçme.
- Stil talimatının sonuna "Her replikten sonra bir saniye dur." yaz; tek konuşmacılı grupta "Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:". Alçak sesle söylenecek replik için "net, tane tane" ekle.
- `VOICE_FX`: `rate>1` daha ince ve hızlı (çocuk), `rate<1` daha kalın, `intercom=True` anons hoparlörü. `TEMPO`: perdeyi bozmadan hızlandırma (`'*'` herkes). `GAP_SCALE`: replik arası boşlukların çarpanı.
- **Abone ol bandı (her bölümde zorunlu):** `ABONE = [('<replik_id>', 0.0)]` bandın gireceği anı verir (o replik başlarken). Bölümün 20. ile 35. saniyesi arasında, gerilimin düşük olduğu bir replik seç; bant 4,6 saniye sürer, kanal logosunu ve tıklanan "ABONE OL" butonunu gösterir. İkinci bant bitiş sahnesinde: `ABONE_END` (son sahne başladıktan kaç saniye sonra) ve `bolum.py` içinde `abone(cv, t, a0 + ABONE_END, pos=...)`. Her bant için `mix_plan` içine tık ve kısa zil ekle (örnek b01).
- **Müzik (`music`, 20 Kasım 2026):** `mix_plan` dönüşüne `music=[(baş, bit, mod, kazanç)]` ekle. Modlar: `gerilim` (D minör: alçak uğultu, seyrek piyano notaları, uzaktan müzik kutusu), `sicak` (F majör: müzik kutusu melodisi ve yumuşak piyano akorları), `gizem` (minör müzik kutusu, bitiş kartı için). Konuşma varken müzik kendiliğinden kısılır. Müzik kullanan bölümde `pads` boş kalsın (ton çatışır). Bölümün duygusu döndüğünde (gerilimden rahatlamaya, sırrın sıcak tarafı açılınca) mod değişsin; dönüş anı bir repliğe ya da görsele denk gelsin. Gündelik sohbet sahneleri `sicak`, kural ve kaybolma sahneleri `gerilim`.
- `mix_plan(T)`: fon akorları (`pads`) ve efektler (`fx`). Efektler: `hum, rumble, snap, tick, whoosh, chime, buzz, ding, slide, steps, ring`. Her görsel olayın (kapı, düğme, adım, ışık) bir sesi olsun; efekt zamanını çizimle aynı vuruştan hesapla.

## 5. Ses (`motor/ses.py`)
Bölüm klasörünün içinden çalıştırılır. `GEMINI_API_KEY` yalnızca komutta ortam değişkeni olarak verilir.

- `TTS_MODEL=gemini-2.5-flash-preview-tts` kullan. Ücretsiz kota **günde 10 istek** (İstanbul saatiyle 11:00 civarı sıfırlanır). Bir bölüm 5 istek harcar; yeniden deneme hakkın azdır, grubu göndermeden önce metni iki kez oku.
- `gemini-3.1-flash-tts-preview` kotası **"Demek O Yüzden" kanalıyla ortaktır**; yalnızca 2.5 kotası dolduysa ve en fazla 1 istek için kullan. `gemini-3.8-flash-tts` stil talimatını sesli okur; ona yalnızca düz metin gönder.
- 429 (kota) gelirse: kalan grupları başka modelle dene; o da olmuyorsa bölümü yayınlama, Cem'e bildir. Para harcatacak hiçbir şey yapma (ücretli katman yok).
- **Bozuk kayıt kontrolü (20 Kasım 2026):** `tts` her kaydı kontrol eder. 3 saniyeden uzun sessizlikleri 1 saniyeye indirir. Kayıt beklenen sürenin 1,35 katını geçerse (metin tekrar okunmuş ya da replik atlanmış) `raw_<grup>.wav` yazılmaz, `voice/bozuk_<grup>.wav` yazılır ve uyarı basılır: o grubu ikiye böl ve yalnızca onu yeniden üret. Anlatıcı grubunda en fazla 4 paragraf olsun (6-7 paragraflık grup iki kez bozuk geldi). Yanlış alarmdan eminsen `TTS_KABUL=1`.
- `python ../../../motor/ses.py tts` (var olan `voice/raw_<grup>.wav` yeniden üretilmez), `gaps`, sonra `CHECK_MODEL=gemini-3.1-flash-lite python ../../../motor/ses.py check`: her satırı yazıya döküp senaryoyla karşılaştırır.
  - Sayıların rakamla yazılması ("on üç" yerine "13"), isimlerin farklı yazılması (Kai yerine Kay) ve çok kısa parçalar `XX` çıkabilir; sorun değildir.
  - Bir replik komşusuna kaymışsa `gaps` çıktısına bakıp doğru kesimleri `voice/cuts.json` içine yaz: `{"<grup>": [kesim zamanları]}` (ilk ve son dahil, replik sayısı + 1 değer), sonra `check <grup>` ile doğrula.
- `python ../../../motor/ses.py build`: `voice/voice.wav`, `voice/mix.wav`, `voice/final.json`. Toplam süre **175 saniyeyi geçmesin**. Geçerse sırayla: sessiz vuruşları kısalt, `GAP_SCALE` düşür (0,6'ya kadar), `TEMPO` artır (en fazla 1,08), en son replik çıkar. Yeni TTS isteği harcamadan çöz.

## 6. Sahneler (`bolum.py`)
Örnek: `diziler/kat13/b01/bolum.py`. Bölüm dosyası yalnızca sahne fonksiyonlarını yazar; ortak her şey dizinin `ortak.py` dosyasındadır. Yeni dekor ya da yardımcı başka bölümde de işe yarayacaksa `ortak.py` içine ekle.

**Koordinatlar.** Sahneler dikey sahne koordinatlarında yazılır: x 0..1080, zemin `GY=1330`. `with stage(cv): ...` içinde çiz.
- Dikey (1080x1920): sahne = ekran. Altyazı y≈1560, üst etiket y≈150, sayaç y≈305.
- Yatay (1920x1080, `STAGE_H=1.0,960,880`): görünen sahne aralığı **x -420..1500, y 450..1530**. Önemli her şey y≥470 olmalı; x<0 ve x>1080 bölgesi yalnızca yatayda görünür (oraları da dekorla doldur, boş duvar bırakma).
- Ekran koordinatında çizilenler (`tally`, `card`, `tag`, `captions`) `FMT`'ye göre kendileri yerleşir.

**Zaman.** `TL` zaman çizelgesi: `S(id)`, `E(id)` replik başı ve sonu; `B(ad)` vuruş `(baş, son)`; `frac(id, f)` replik içinde oran; `on(ts, id)` replik sürüyor mu; `TL.span(sahne)`; `TL.talk(konuşan, t)` ağız açıklığı. Her sahne `def sceneN(cv, t): ts, k = step(t), kk(t)` ile başlar (12 fps adım; `k` kare sayacı, `alt(k, a, b, hold)` iki değer arasında gidip gelir).

**Karakter.** `actor(cv, ts, kim, ifade, poz, bakış, ...)` ya da toplu `cast(cv, ts, {kim: (ifade, poz, bakış[, ek])})`.
- İfadeler: `mutlu, sakin, heyecan, panik, bagir, endise, uzgun, aglama, merak, saskin, yorgun, kararli`.
- Poz sözlüğü: `aL/aR` (dirsek_x, dirsek_y, el_x, el_y; omuza göre), `kL/kR` diz, `fL/fR` ayak (zemine göre), `bob, lean, crouch, belly`. Hazır pozlar `ortak.py` başında (HOLD, COWER, LOOKUP, LEAN_IN, SLUMP, PRESS_A, RANT, HIP...). `mixpose(p, q, u)` iki poz arasında geçiş.
- `walk(mesafe, ölçek, yön, scared, hold, run, off)` yürüme pozu; `place=(x, gy, s)` ile karakteri kabin dışında bir yere koy. `back=True` arkası dönük. `look` bakış yönü (-2 sol .. 2 sağ).
- Konuşan karakter kendiliğinden ağzını oynatır ve hafifçe salınır.
- Çok karakterli sahnede iki sıra kullan (arkada küçük ölçek, önde büyük). Arka sıranın arkasında kalan nesne görünmez; önemli nesneyi başların üstüne ya da kenara koy.

**Dekor (13. Kat için hazır):** `cabin(cv, sh, u, lamp)` asansör kabini (u: kapı açıklığı), `display(...)` kat göstergesi (asansörün sesi konuşurken ses çubukları), `lobby(cv, u)`, `side_corridor(cv, cam, door_x, lamp, k, open_u)` yandan koridor (kamera kayar), `corridor(...)` kapıdan görünen derinlik, `shadow(...)` karaltı, `dark_eyes(...)`, `tally(...)` kişi sayacı, `badge(...)` baş üstü sayı rozeti, `panel_flash(...)`, `phone(...)`, `dim(cv, a)` karartma, `card(...)` kart, `jit(k, amp)` sarsıntı.
Yeni dekor yazarken: düz renkli yüzeyler + kesik çizgili dikiş (`dashed`) + hafif gürültü dokusu. Keçe ve örgü havası korunur, palet kısık (koyu petrol, bordo, krem, tek vurgu rengi).

**Abone ol bandı.** `abone(cv, t, t0, pos=None)` (motor/orgu.py). `senaryo.ABONE` içindekileri `run` kendisi çizer (dikeyde üst orta, yatayda sol üst); o anda o bölgede önemli bir şey (sayaç, yazı) olmasın. Bitiş sahnesinde `pos` ile kartın ve gözlerin arasına, altyazının üstüne yerleştir. Logo `motor/logo.webp`.

**Sinema katmanı (`motor/sinema.py`, 19 Kasım 2026).** `run()` her karede kendiliğinden uygular; `SINEMA=0` eski görünümü verir.
- Kamera **sakindir** (Cem, 19 Kasım 2026): yalnızca yavaş yakınlaşma, yavaş uzaklaşma ve hafif yana kayma yapar. Konuşanı izlemez, sahne içinde sıçramaz, sallanmaz; yaklaşık 3,8 sn'lik hareketler birbirine kesintisiz bağlanır. Yeni açı gerekiyorsa kamerayı oynatma, yeni sahne (`('scene', no)`) yaz. Bölümün ilk saniyesinde kanca için tek bir hızlı hareket vardır. Son sahne (bitiş kartı) da aynı sakin harekettedir. `jit` sarsıntısını yalnızca kısa olaylarda (asansörün durması, kapının çarpması) kullan, sürekli sarsıntı yok.
- Sahne bazında ayar: `SINE = {sahne_no: dict(cam='oto'|'sabit', mood=None|'sicak'|'soguk'|'gece'|'kirmizi'|'sepya', rays=True, zmax=1.32)}` ve `run(DRAW, sine=SINE)`. Kamera dikeyde en fazla 1,17, yatayda 1,10 yakınlaşır; kenara yakın önemli bir şey kırpılıyorsa o sahneye `cam='sabit'` ver ya da göstergeyi `run(..., hud=...)` ile kameradan sonra çiz. Geri dönüş sahnelerine `mood='sepya'`.
- Işık: sahnenin en parlak noktası (lamba) kendiliğinden bulunur; oradan ışık hüzmesi ve zemine ışık havuzu düşer. Parlama, vinyet, renk ayarı, film greni, ayak altında temas gölgesi. Lambası olmayan sahnede hüzme çıkmaz: her sahneye en az bir ışık kaynağı (lamba, pencere, ekran, kapı aralığı) koy.
- Altyazı: ekranın ortasında (dikey y≈1250, yatay y≈985, ayakların altı), büyük beyaz harf + siyah kontur, 1-3 kelimelik parçalar; vurgu kelimeleri sarı; konuşanın rengi kelimelerin altındaki çizgide. Karakterin yüzü bu yükseklikte kalıyorsa karakteri biraz yukarı ya da yana yerleştir.
- Plaka (üretilmiş arka plan): `with stage(cv): sinema.plate(cv, 'arkaplan/lobi')` dosyayı `diziler/<dizi>/arkaplan/lobi-v.jpg` (dikey) ya da `-h.jpg` (yatay) olarak arar, görünen alanı doldurur; dosya yoksa `False` döner, sahne kodla çizilen dekora düşer. Karakterler, temas gölgesi, ön plan ve ışık üstüne gelir. `shift=(dx, dy)` ile plakayı karakterden yavaş kaydırarak parallax ver.
- Plaka üretimi **şimdilik kapalı**: 19 Kasım 2026'da bu anahtarın ücretsiz katmanında görsel modellerinin kotası 0 çıktı (gemini-2.5-flash-image ve gemini-3.1-flash-lite-image, `limit: 0`). Cem ücretli katman ya da başka bir kaynak açmadıkça görsel isteği gönderme; plakaları kodla çizilen dekor ve sinema katmanı karşılar. Açılırsa yöntem: anahtarın gördüğü modelleri listele (`GET https://generativelanguage.googleapis.com/v1beta/models`), adı `image` içeren ücretsiz bir Gemini modeliyle tek istekle dene. İstem: stilize 3D animasyon filmi arka planı, keçe ve yün örgü dokuları, sinematik yumuşak ışık (lamba, pencere huzmesi, sis), insan yok, karakter yok, yazı yok, logo yok, alt üçte birde boş düz zemin; dikey 9:16 ve yatay 16:9 ayrı. Bir çalışmada en fazla 4 görsel isteği, TTS isteklerinden ayrı. 429, `limit: 0`, faturalandırma ya da ücretli plan uyarısı gelirse dur, kodla çizime devam et ve bunu "Öğrenilenler"e yaz. Her görseli Read ile aç: yazı, insan, logo, bozuk perspektif varsa kullanma; zemin çizgisi GY=1330'a otursun. Geçenleri en fazla 600 KB jpg olarak `diziler/<dizi>/arkaplan/` altına koy ve commit et; plakalar dizi boyunca yeniden kullanılır.
- **Sıcak/soğuk zıtlık (`mood='kontrast'`, 20 Kasım 2026):** lambanın çevresi sıcak sarı, kenarlara doğru gece mavisi. Son Vagon'da bütün sahnelerin varsayılanı (`ortak.DEFAULT_MOOD`); sahne bazında `SINE` ile değiştirilebilir. Yeni dizide de varsayılan yap.
- **Büyük kafa (20 Kasım 2026):** `figure(..., head=1.2)` kafayı büyütür (sevimli, ifadesi okunan karakter). Dizinin `CAST` kayıtlarına `head` yaz ve `actor` içinde `figure`'a geçir; dizi boyunca aynı kalsın. Yüze göre konumlanan aksesuarlar (kirpik, gözlük, bıyık) `s` ile değil kafanın gerçek yarıçapı `f['HR']` ile hesaplansın.
- Hız: yeni katmanla bir kare yaklaşık 0,4 sn sürer (eskisinin 2 katı kadar); sahneler paralel işlendiği için bölüm yine sığar.

**Performans.** Karakterler sprite olarak önbelleğe alınır; her karede değişen poz (yürüyüş) pahalıdır. Uzun yürüyüş sahnelerini 10 ile 15 saniyede tut.

## 7. Kare kontrolü (zorunlu)
Her sahneden en az 3 kare, **iki formatta da**:
`FMT=v python bolum.py still chk 3.0 21.5 ...` ve `FMT=h ...`; sonra `python ../../../motor/sheet.py chk/sayfa.jpg 4 640 chk/h_*.png` ve görseli **aç, bak**.

Kontrol listesi:
- **İlk 2 saniye (kural 16):** her iki formatta 0,0 / 0,5 / 1,0 / 1,9. saniye karelerini ayrıca aç. İlk kare boş, siyah ya da yalnızca logo/başlık kartıysa, kanca yazısı okunmuyorsa ya da kanca repliği 2 saniyeyi aşıyorsa düzelt; düzelmiyorsa yayınlama, Cem'e bildir.
- **Görsel kalite (kural 17):** kamera hareket ediyor mu, ardışık iki plan aynı açı mı, ışık hüzmesi ve temas gölgesi var mı, ortadaki altyazı okunuyor mu ve yüz kapatıyor mu, yakın planda önemli bir nesne (sayaç, gösterge, kart) kırpılmış mı.
- Taşma, üst üste binme, kadraj dışında kalan önemli nesne ya da karakter (özellikle yatayda y<470 ve dikeyde x<0, x>1080).
- Altyazı doğru kişinin adıyla ve doğru anda mı; altyazı karakterin yüzünü kapatıyor mu.
- Gerilim sahnesinde gülen var mı. İfade repliğe uyuyor mu.
- Replikte anlatılan eylem ekranda görünüyor mu (bölüm 1, kural 6).
- Yatayda yanlar boş mu kalmış; dikeyde alt üçte bir boş mu.
- Yazılarda Türkçe karakterler doğru mu (ı, İ, ş, ğ, ü, ö, ç).

Üretimden sonra her dosyadan 12 kare çıkarıp bir kez daha bak; süreyi ve ses akışını (`ffmpeg -i`) doğrula.

## 8. Depo ve yayın
1. Videolar `videos/` altında: `<YYYY-MM-DD>-<dizi>-b<no>-<slug>-dikey.mp4` ve `-yatay.mp4`.
2. `log.json` içine kayıt ekle: `{"tarih", "dizi", "bolum", "ad", "slug", "baslik", "dikey", "yatay", "sure_sn", "playlist", "yatay_youtube", "durum"}`. `durum`: `planlandi` ya da hata açıklaması.
3. Yalnızca şunları commit et: yeni bölüm klasörü (senaryo.py, bolum.py, varsa voice/cuts.json), `ortak.py` ve `DIZI.md` değiştiyse onlar, `videos/` içindeki iki yeni dosya, `log.json`, gerekiyorsa `KIT.md` (yalnızca "Öğrenilenler" bölümü). Ses dosyaları ve sahne parçaları commit edilmez (`.gitignore`). Sonra `git push origin HEAD:main`.
   - main reddedilir ama `claude/` ile başlayan dala yazılabiliyorsa o dala gönder, adreslerde o dal adını kullan ve Cem'e bildir.
4. Açık adres: `https://raw.githubusercontent.com/caltun90/dizivanastudio-social/main/videos/<dosya>`. `curl -sI` ile 200 döndüğünü doğrula (gerekirse 1 dakika bekle).
5. **Yayın (`motor/yayin.py`).** İki video iki ayrı yoldan gider:
   - **Dikey: Buffer API** (YouTube Short olur). Buffer YouTube'da yalnızca Shorts destekler; **yatay videoyu Buffer'a verme, yayınlayamaz.**
   - **Yatay: YouTube Data API** (normal video). Özel yüklenir, verilen saatte kendiliğinden herkese açılır.
   - Anahtarlar ortam değişkeni olarak verilir: `BUFFER_API_KEY`, `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`. Claude'a bağlı Buffer bağlayıcısı (mcp Buffer araçları) başka bir hesaba aittir (Engrow ve Pofu Kids); **o araçları hiç kullanma.**
   - Önce `python motor/yayin.py liste 2`: bugüne ait planlı ya da gönderilmiş gönderi varsa yenisini ekleme.
   - Dikey: `python motor/yayin.py planla <dikey_adres> <bugün>T18:00:00+03:00 "<dikey başlık>" <bölüm>/aciklama.txt`. Adres reddedilirse bir kez `https://cdn.jsdelivr.net/gh/caltun90/dizivanastudio-social@main/videos/<dosya>` ile dene. Sonra `liste` ile `scheduled` olduğunu doğrula.
   - Yatay: `python motor/yayin.py yt-yukle videos/<yatay_dosya> "<yatay başlık>" <bölüm>/aciklama.txt <bugün>T18:05:00+03:00 "<etiketler, virgülle>" <oynatma_listesi_id>`. Çıktıdaki `video_id` değerini `log.json` kaydına `yatay_youtube` olarak yaz. Sonra `python motor/yayin.py yt-durum <video_id>` ile yüklemenin bittiğini ve yayın saatinin doğru olduğunu gör.
   - Şu an 17:30'dan sonraysa iki komutta da saat yerine `simdi` yaz.
   - **Oynatma listesi:** her dizinin bir listesi olur. Dizinin ilk bölümünde `yt-liste-olustur "<Dizi adı>" "<tek cümle>"` ile oluştur ve kimliği o dizinin `log.json` kayıtlarına `playlist` olarak yaz; sonraki bölümlerde aynı kimliği kullan.
   - YouTube API günlük kotası sınırlıdır (bir yükleme yaklaşık 1600 birim, günlük 10.000); aynı videoyu iki kez yükleme. Yükleme hata verirse bir kez daha dene, yine olmazsa Cem'e hata metnini bildir.
6. **Başlık ve açıklama.**
   - Yatay başlık: `<Dizi adı> | <no>. Bölüm: <bölüm adı>` (örnek: `13. Kat | 1. Bölüm: Asansör`).
   - Dikey başlık: merak uyandıran tek cümle + dizi ve bölüm (en fazla 90 karakter; örnek: `Asansöre 4 kişi bindi, içeride 5 kişi vardı | 13. Kat 1. Bölüm`).
   - Açıklama metnini bölüm klasörüne `aciklama.txt` olarak yaz (yayin.py bu dosyayı okur).
   - Açıklama: 2 cümlelik kanca (sürpriz bozmadan), izleyiciye bölümün sorusu, "Yeni bölüm her gün.", en fazla 6 etiket (her zaman `#dizivanastudio` ve dizinin etiketi, örnek `#13kat`).

## 9. Dizi bitince: film
Dizinin son bölümü yayınlandıktan sonraki çalışmada, yeni diziye başlamadan önce:
- Bütün yatay bölümleri tek dosyada birleştir (başta 2 sn dizi adı kartı, aralarda 1 sn kararma; `ffmpeg concat`, gerekirse yeniden kodla). Dosya 95 MB'ı geçmesin (geçerse `-crf` yükselt; 8 bölümlük filmde 1280x720 ve iki geçişli yaklaşık 480k video, 64k ses).
- `videos/<tarih>-<dizi>-film-yatay.mp4` olarak depoya koy, `yt-yukle` ile `<Dizi adı>: Tüm Bölümler (Film)` başlığıyla 20:00'a planla (aynı oynatma listesine ekle), `log.json` içine `"bolum": "film"` kaydı ekle. Film yataydır; Buffer'a verilmez.

## 10. Yeni dizi başlatmak
1. Aşağıdaki havuzdan sıradaki fikri al (havuz biterse aynı ruhta yenisini bul): tek cümlelik güçlü bir fikir, tek bir kural ya da sır, 4 ile 5 karakter, en fazla 3 mekân.
2. `diziler/<kısa-ad>/DIZI.md` yaz (`diziler/uzayli/DIZI.md` örnek): dünya ve kural, karakterler (renk, tek bir ayırt edici aksesuar, konuşma biçimi, ses), sır ve ipuçları, **bütün bölümlerin özeti ve her birinin farklı yapısı**, dizi bitişi. Bölüm sayısını yaz (varsayılan 5; Cem başka sayı istediyse o). Sonu baştan belli olsun; her bölüm bir soruyla biter, son bölüm bütün soruları kapatır.
3. Yeni motorda: `yumurta/diziler/<kısa-ad>/kadro.js` (karakterler: `OrguToon` görünüşleri, `SPK`, `NAMES`, `COLORS`) ve `ortak.js` (en fazla 3 mekân, planlar, yardımcılar) yaz; `yumurta/diziler/uzayli/` örnektir, mekân dışındaki yardımcıları oradan kopyala. Kadro sayfasına bak: `node faces.mjs <kadro hikâyesi>`. (Eski motor: `ortak.py`, `kat13/ortak.py` örnek.)
4. Karakter renkleri birbirinden net ayrılsın (turkuaz, mercan, lacivert, lila, hardal, açık kahve, yeşil, pembe). Bir önceki dizinin karakterlerini aynen kullanma.
5. Sesler: Gemini hazır seslerinden seç (Achird anlatıcı için iyi; Kore, Aoede, Leda kadın; Puck, Fenrir, Algenib, Charon, Orus erkek). Her karaktere ayrı ses; benzer çıkanları `VOICE_FX` ile ayır.
6. İlk bölüm dünyayı ve kuralı ilk 30 saniyede kurar.

**Dizi havuzu (sırayla)**
1. **13. Kat** (gerilim): asansör olmayan katlara çıkar, her katın bir kuralı vardır. (YAYINDA)
2. **Son Vagon** (gerilim): gece treninde her istasyonda bir vagon kayboluyor; yolcular en öndeki vagona doğru ilerlemek zorunda. Biletlerde herkesin ineceği istasyon yazıyor, biri hariç. (BİTTİ, 25 Kasım 2026)
3. **Yedek** (bilimkurgu): bir adam sabah uyanır, evde ondan önce uyanmış bir "o" daha vardır. Hangisi yedek?
4. **Saat 03:03** (gerilim): bir apartmanda herkes her gece 03:03'te uyanıyor ve her gece binadan bir şey eksiliyor: önce bir kapı numarası, sonra bir merdiven, sonra bir komşu.
5. **Kayıp Eşya Bürosu** (komedi, gizem): kaybolan her şeyin geldiği bir büro. Bir gün rafa bir "pazartesi günü" gelir ve şehirde kimse pazartesiyi hatırlamaz.
6. **Kiracı Uzaylı** (komedi): öğrenci evine kiracı olarak bir uzaylı taşınır; dünyalı gibi davranmayı öğrenmeye çalışır, Türkçe deyimleri ve kılavuz kurallarını harfi harfine anlar. (SIRADAKİ: Cem 25 Kasım 2026'da Son Vagon'dan sonra bir komedi istedi, komik şişko ve biraz büyük, kalın burunlu karakterlerle, 8 bölüm; `diziler/uzayli/` hazır. Bölüm yazmadan önce `diziler/uzayli/KOMEDI.md` okunur. Havuzda 3, 4 ve 5 bunun ardından sırayla gelir.)

## 11. Rapor ve hata
- Başarıyla bitince Cem'e tek kısa mesaj: dizi ve bölüm adı, iki başlık, planlanan saatler, iki videonun depo bağlantısı. Dikey videoyu dosya olarak da gönder ki yayından önce izleyebilsin; beğenmezse Buffer'dan silebileceğini bir cümleyle hatırlat.
- Herhangi bir adım başarısız ya da yarım kalırsa (anahtar, kota, ses, render, push, Buffer, ağ) sessiz kalma: neyin başarısız olduğunu, hata metnini ve Cem'in bir şey yapması gerekip gerekmediğini tek kısa mesajla bildir. Yarım ya da hatalı bölümü yayınlama.

## 12. Öğrenilenler
- Gerçek ses, taslak tahminden yaklaşık yüzde 10 ile 15 uzun çıkar. Anlatıcı yavaş okur; anlatıcı cümlelerini kısa tut.
- TTS cümle içinde 1 saniyelik nefesler bırakır; `ses.py` bunları kendisi sıkıştırır (`squeeze`).
- Kontrol modeli kısa parçaları ("Kai!") komşusuyla birleştirip numaraları kaydırabilir; süreler doğruysa sorun yoktur.
- Sayım gösteren sahnede rozet sırası ekrandaki soldan sağa sırayla aynı olmalı.
- Karanlık sahnede "fazla olan" gibi bir sırrı görselle ele verme (gözler sırayla kırmızı yanar).
- Buffer YouTube'da yalnızca Shorts yayınlar (dikey ya da kare). Yatay video her zaman YouTube API ile yüklenir.
- Windows'ta ffmpeg `imageio-ffmpeg` paketinden gelir; yazı tipi `motor/fonts` içindedir.
- Bulut ortamında skia için `apt-get update && apt-get install -y libegl1` ve `python -m pip install ...` gerekir; TTS bazen bozuk, çok uzun ve sessiz kayıt döndürür (655 sn gibi): süreyi kontrol et, yalnızca o grubu silip yeniden üret.
- TTS bazen grubun bir kısmını dip gürültülü üretir (`gaps` sessizlik bulamaz, `check` replikleri kaydırır): yalnızca o replikleri yeni bir grupta yeniden üret, kalanları `voice/cuts.json` ile kes.
- 2.5 TTS kotası gün içinde başka işlerce de harcanabiliyor: 429 gelirse kalan tek grubu `TTS_MODEL=gemini-3.1-flash-tts-preview python ../../../motor/ses.py tts <grup>` ile üret (b04'te çalıştı). TTS konuşmacı değişiminde her zaman 1 saniye durmaz; `check` kayma gösterirse `gaps` çıktısından `voice/cuts.json` yaz.
- Gemini görsel modelleri (adında `image` olanlar) ücretsiz katmanda kullanılamıyor (19 Kasım 2026, `limit: 0`); deneme isteği harcama.
- Sinema kamerası sahneyi yakınlaştırıp kırpar: sayaç gibi hiç kırpılmaması gereken göstergeyi `run(..., hud=fonk)` ile kameradan sonra çiz. Dikeyde ortadaki altyazı ekranda y 1160-1300 arasını kaplar; yüzleri ve önemli nesneyi (kart yazısı, düğme) bunun üstünde tut, kare kontrolünde özellikle buna bak.
- Kameranın konuşanın kafasını kare kare izlemesi görüntüyü sallıyordu (b05'in ilk üretimi, Cem beğenmedi): kamera artık yalnızca yavaş zoom ve hafif kayma yapar. Kamerayı bir karaktere ya da hareket eden bir şeye bağlama.
- 20 Kasım 2026: Film de kancayla açılır (kural 16): başa son bölümün ilk 2 saniyesi, sonra 2 sn dizi kartı konur; iki geçişli x264 (790k video, 64k ses) 14 dakikayı yaklaşık 87 MB yapar. Yapay zeka etiketi: `videos.update` ile `containsSyntheticMedia=true` çalışıyor (Cem 20 Kasım'da Studio'da 12 videoda Evet gördü), ama `videos.list` bu alanı hiç döndürmez. Bu yüzden "true olmayan" kontrolü API ile yapılamaz: etiketlenen video kimliklerini `log.json` kayıtlarındaki `yz_etiketli` listesinde tut, yalnızca listede olmayan videolara gönder. Buffer Short'u planlanan saatte yükler; o saatten önce kanalda görünmez, etiketi ertesi çalışmada eklenir. Anlatıcı TTS grubu son paragrafı atlayıp uzun sessizlik ekleyebilir: eksik repliği tek satırlık ayrı grupta üret.
- 21 Kasım 2026: İki konuşmacılı TTS grubu replik arasını 0,2 sn'ye kadar kısaltabiliyor; `check` kayma gösterirse 0,05 sn'lik sessizliklere de bakıp `voice/cuts.json` yaz. Ses kısa çıkarsa (155 sn) yeni istek harcamadan `GAP_SCALE` (1,4), sessiz vuruşlar ve `TEMPO` (0,97) ile 2:40'ın üstüne çıkar. Büyük kafada `SHOW` pozu elindekini yüzün üstüne getirir; eli yüzün yanında tutan bir poz kullan (b02 `SHOWB`). Özçekim planı: öndeki karakter ölçek 1,7 ve zemin 1900 ile çizilir, arkası `door_view`.
- 23 Kasım 2026: Yavaş okunan anons grubu "bozuk kayıt" yanlış alarmı verebilir (16,5 sn, sonu 3 sn sessiz): yeni istek harcamadan `voice/bozuk_<grup>.wav` dosyasını `raw_<grup>.wav` adıyla kopyala ve `check` ile doğrula. Karakterler vagon koltuğuna oturtulamaz (koltuk boylarından yüksek): duvara katlanır koltuk çiz (b03 `jump_seat`, `SEATP`). Küçük ölçekli karakteri `zoom` içinde büyütme (bulanır); zoom dışında, hesaplanmış yer ve ölçekte çiz (b03 `door_shot`). Bulut ortamında `pip` başka Python'a kurabiliyor: `python -m pip` kullan.
- 24 Kasım 2026: Mektup ya da dış ses biçimi: sesi okuyan karakteri köşede konuşan bir portreyle göster (b04 `portrait`, nakış kasnağı) ve replikleri iki konuşmacılı gruba koy (8 replik, 35 sn sorunsuz geldi). İki konuşmacılı grupta konuşmacı değişimindeki boşluk (0,3 sn) cümle içi duraklamadan (0,5-1 sn) kısa çıkabiliyor: `check` kayma gösterirse kesimleri `gaps` çıktısından cümle sayarak yaz. Kamera sahneyi kırptığı için kenara yapışık çerçeve ve etiketleri (`memory_frame`, köşe portresi) sahnede değil `hud` içinde çiz. `CRF=23` ile bölüm 45 MB civarı çıkar (21 ile 75 MB).
- 25 Kasım 2026: Sinema kamerası dikeyde kenarlardan yaklaşık 80 piksel kırpar: tabela, saat ve kenardaki karakteri x 90-990 arasında tut (b05'te gişe tabelası ve kapıdaki Kondüktör kesildi, kaydırıldı). Hazır `SIT` pozu karakteri yere yakın oturtur: alçak bank çiz, zemini oturma tahtasının 62 piksel altına ver (b05 `bench`). "Boş" bir şeyi (boş koltuk) kancada göstermek için kesik çizgili siluet ve soru işareti koy; yalnız boş dekor okunmuyor. Tek heceli replik başı ("Ev.") iki konuşmacılı grupta bir önceki repliğe yapışabiliyor: kesimi `gaps` çıktısından elle yaz.
- 25 Kasım 2026: Yeni motorla (yumurta + örgü) 16,8 sn'lik deneme Actions'ta 4 parçayla dikey ve yatay birlikte yaklaşık 5 dakikada çıktı (kare başına yaklaşık 1,8 sn, kurulum 2 dk). 3 dakikalık bölümde `parts=20` ile iki format birlikte 20-35 dakika bekle. Ses `ses.py` ile aynı yoldan gelir; `kopru.py` her `build`'den sonra çalışmalı. Konuşanın adı ve vurgu kelimeleri altyazıda kendiliğinden çıkar (`senaryo` `hl` listesi).
- 26 Kasım 2026: Kiracı Uzaylı b01 (yeni motor): 55 kısa replik + 45 sn sessiz vuruş + `GAP_SCALE` 1,25 = 2:46; gerçek ses taslaktan yaklaşık yüzde 15 uzun çıktı. Dört kişili dizide 5 TTS grubu için replikleri sayarak eşle (her grupta iki konuşmacı sırayla); 11 replikli grup bozuk gelirse ikiye böl. Dikeyde kadraj dardır (4 m uzaklıkta yaklaşık 1,8 m): ikili planda iki oyuncu en fazla 1 m arayla durur, şişman Tobi için `uzak` 4; kapıya yürüyüşte `ev.kapi` yerine b01'deki `KAPI_L` planı. Uzun planda `creep` yakınlaşmayı büyütüp kafayı keser: b01'deki sınır satırını kopyala (`.43 / plan süresi`). Zip'in yakın planında `h` 1,25 (antenler kesilmesin); kart ya da abone bandı olan planda `h` 1,35 ve `uzak` 2,9. Oyuncuyu sehpanın içine koyma (sehpa x -2,1..-1,1, z -1,6..-1,0); bitiş ve başlık kartı için b01 `SON` planı. Film: tek `filter_complex` ile iki geçiş, 770k video 13:58'i 88 MB yaptı.
