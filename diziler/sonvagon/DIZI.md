# Son Vagon: dizi dosyası (5 bölüm)

Bu dosya dizinin tamamını anlatır. Yeni bölüm yazan herkes (insan ya da otomasyon) önce bunu okur. Sürprizleri erken açma: aşağıdaki "Sır" bölümü 4. bölüme kadar izleyiciye belli edilmez.

## Dünya ve kural
- Gece Ekspresi: bir lokomotif ve beş vagon. Saat 23:00'te kalkar. Vagonlar numaralıdır: 1 en önde (lokomotifin arkası), 5 en arkada.
- Ekranda tren hep **sağa** gider: arka (son vagon) solda, ön sağda. "Öne geçmek" sağa yürümektir.
- Tren her istasyonda durur ama kapılar açılmaz, perona kimse inmez, kimse binmez. Tren kalktığında en arkadaki vagon artık yoktur: kopmamıştır, ray boştur. İçinde kim kaldıysa o da yoktur.
- Kondüktörün sesi (hoparlörden anons, erkek, kibar, resmi) her istasyondan önce aynı kalıbı söyler: "Sıradaki istasyon: ... Bırakılacak vagon: ... numara." İlk anonsta: "Bu tren, her istasyonda bir vagon bırakır."
- Yolcuların çıkardığı kural: **tren durduğunda son vagonda olma.** Her istasyondan önce bir öndeki vagona geçerler.
- Herkesin biletinde ineceği istasyon yazar. Mia'nın biletinde İNİŞ satırı boştur.
- İstasyonlar sırayla: Karaköprü, Değirmen, Yedigöl, Sarnıç, Son Durak.

## Karakterler
- **Mia:** hardal sarısı; lacivert küt saç, kırmızı atkı. 19 yaşında, ilk kez tek başına yolculuk ediyor. Meraklı, cesur, hızlı konuşur, soru sorar. Gişede "ilk kalkan trene" bilet istedi; nereye gittiğini bilmiyor. Ana karakter. Ses: Leda.
- **Ren:** yeşil; başında mercan rengi kulaklık. Rahat, şakacı; korkunca espri yapar. Bileti: Değirmen. Ses: Puck.
- **Ada:** gül kurusu; gri topuz, lila şal, elinde örgüsü. Yaşlı, bilge, çok sakin; "evladım", "kızım" der, atasözü gibi konuşur. Bileti: Yedigöl. Ses: Kore (rate 0,95).
- **Eli:** gök mavisi; melon şapka, bıyık, cep saati, evrak çantası. Titiz, hesapçı, tedirgin; sayılarla konuşur ("tam on iki dakika", "hesapladım"). Bileti: Karaköprü. 1. bölümde gitti; geriye bileti kaldı (Ren'de).
- **Kondüktör:** ilk üç bölümde yalnızca ses (ANONS, Charon, hoparlör efekti). 4. bölümde görünür: lacivert üniforma, kırmızı kasket, elinde bilet zımbası ve fener. Tehdit değildir; kibar ve yorgundur. `ortak.py` içine 4. bölümde eklenecek ('C').

Anlatıcı: Achird.

## Sır (izleyiciye 4. bölümde açılır, 5. bölümde gösterilir)
Vagonlar kaybolmuyor. Tren, her yolcuyu **biletinde yazan istasyona vagonuyla birlikte bırakıyor.** Kaybolan kimse yok; inen yolcu var. Kapılar bu yüzden açılmıyor: inecek olan zaten vagonuyla kalıyor. Geride kalanlar korkuyla öne kaçtıkça yalnızca kendi istasyonlarını geciktiriyor; herkes sonunda biletinde yazan yerde, o an son vagonda oluyor.
Asıl tehlike en öne varmak: lokomotifte makinist yok. Bileti boş olan inemez; tren Son Durak'tan sonra hiç durmaz. Mia'nın bileti boş, çünkü nereye gideceğine karar vermeden trene bindi (evden kaçtı). Kurtuluşu: biletine istasyonu kendi eliyle yazmak.

İpuçları (bölümlere serpiştir, altını çizme):
- Anons hiç "kaybolur" demez; hep "bırakır" der.
- Eli karanlıkta korkmadı; tabelayı görünce sakinleşti: "Burası benim istasyonum." (1. bölüm)
- Herkes tam biletinde yazan istasyonda "kayboluyor" (1. bölümde fark edildi; yolcular bunu lanet sanıyor).
- İstasyonlar boş ama bakımlı: lambalar yanıyor, saat doğru, bank temiz. Değirmen'de peronda bir çift ayak izi, Yedigöl'de bankta Eli'nin şapkası gibi küçük sıcak ayrıntılar (uzaktan, altı çizilmeden).
- Mia: "Gişede ilk kalkan trene bilet istedim."

## Bölümler (her birinin YAPISI farklı; aynı kalıp tekrar edilmez)
1. **Bilet** (ÜRETİLDİ). Karaköprü, bırakılan vagon 5. Yapı: **düz anlatım**, soğuk açılış (arka kapının ardında vagon yok) + trenin dışarıdan sayımı. Dört yolcu son vagonda tanışır; Mia'nın bileti boş. Anons, yürüyüş, körük. Eli çantası için geri döner ("Otuz saniye sürer. Hesapladım."), Karaköprü'de karanlıkta kalır: "Burası benim istasyonum." Tren kalkınca arka kapının ardında yalnızca ray vardır. Ren yerde Eli'nin biletini bulur: İniş Karaköprü. Sıradaki anons: Değirmen (Ren'in bileti). Soru: Mia'nın bileti neden boş? Üretimde: Mia, Ren ve Ada 4 numaralı vagonda kaldı; Eli'nin bileti Ren'de; Ren korkudan yere çöktü, Ada "Kalk evladım. Öne yürüyoruz." dedi.
2. **Değirmen.** Bırakılan vagon 4. Yapı: **kayıt biçiminde.** Bölümün tamamı Ren'in telefonuyla çektiği video: ekranda REC çerçevesi, pil ve saat; Ren kameraya konuşur ("Biri bunu bulursa..."). Ren biletinden kurtulmaya çalışır: bileti yırtar, camdan atar; bilet cebinde yine çıkar. En öne, 1 numaraya kadar koşar. Tren Değirmen'e yaklaşırken Ada'nın örgü yumağı arkaya, 4 numaraya yuvarlanır; Ada peşinden gider, Ren onu çıkarmak için döner, Ada'yı körüğe iter, kendisi içeride kalır. Telefon körükte yere düşer ve çekmeye devam eder: kararan vagon, sonra boş ray. Son kare: Mia telefonu yerden alır, kayıt biter. Soru: Biletinden kaçabilir misin?
3. **Yedigöl.** Bırakılan vagon 3. Yapı: **tersten anlatım.** Bölüm sondan başlar: 2 numaralı vagonda Mia tek başına, elinde Ada'nın yarım örgüsü. Sahneler geriye doğru açılır ("on dakika önce", "yirmi dakika önce"): Ada'nın 3 numarada koltuğa oturup örgüsüne devam etmesi, Mia'nın yalvarması, Ada'nın bütün gece istasyon adlarını örgüsüne işlediğinin anlaşılması. En baştaki (en eski) sahne en sonda gelir: Ada anonsu dinlerken gülümser, çünkü ilk anonsta anlamıştır: "Bırakır dedi kızım. Kaybolur demedi." Soru: Ada neden kalmayı seçti?
4. **Kondüktör.** Bırakılan vagon 2 (boş bırakılır; içinde kimse yoktur). Yapı: **mektup biçiminde.** Ada'nın örgüsünün içinden Mia'ya yazdığı not çıkar; bölümü Ada'nın sesi anlatır (mektup), görüntüde Mia 2'den 1'e yürür. 1 numarada Kondüktör ilk kez görünür ve biletleri zımbalar: Eli'nin, Ren'in, Ada'nın biletleri zımbalı; Mia'nınki zımbalanamaz, çünkü boş. Sır burada söylenir: "Kimse kaybolmadı küçük hanım. Herkes indi." Kondüktör son kuralı da söyler: bileti boş olan inemez; tren Son Durak'tan sonra durmaz. Soru: Mia biletine ne yazacak?
5. **Son Durak.** Bırakılan vagon 1. Yapı: **geri dönüşlü + kapanış montajı.** Lokomotif: makinist koltuğu boş, önde yalnızca karanlık. Geri dönüşler (sepya): Mia'nın evden çıkışı, gişe ("Nereye?" "İlk kalkan trene."). Mia biletine istasyon adını kendi eliyle yazar: geri döneceği yerin adını. Kondüktör bileti zımbalar. Tren ilk kez kapılarını açar. Kapanış montajı: sabah; Karaköprü'de Eli çantasıyla evine yürür, Değirmen'de Ren'i kulaklıklı bir kardeş karşılar, Yedigöl'de Ada bankta örgüsünü bitirir. Anlatıcı: "O gece trenden kimse kaybolmadı. Herkes, biletinde yazan yerde indi." Son kare: boş tren geceye doğru gider, gişede yeni bir yolcu bilet alır. Soru yok; kapanış kartı: "Son Vagon bitti. Yeni dizi yakında."

## Dizi bitince
Beş yatay bölüm tek dosyada birleştirilir ve "Son Vagon: Tüm Bölümler (Film)" adıyla yüklenir (KIT bölüm 9). Film de kancayla açılır: önce son bölümün ilk 2 saniyesi, sonra dizi adı kartı.

## Bölüm yazım kuralları (bu diziye özel)
- Süre 2:40 ile 2:55 arası. Yaklaşık 38 ile 45 replik, en fazla 6 ses isteği. Kanca ilk 2 saniyede (KIT kural 16).
- Her bölümde anons kalıbı bir kez geçer ve levha (VAGON n) kırmızı yanar: izleyici hangi vagonun bırakılacağını ekranda görür.
- Kimse şiddet görmez; "kaybolma" hep ışıkların sönmesi, sis ve boş rayla anlatılır. Kalan kişi son anda korkmaz, sakinleşir (sırrın ipucu).
- Gerilim sahnesinde kimse gülmez. Ren'in esprileri korkusunu gizler; yüzü `endise` ya da `yorgun` kalır.
- Her bölümde en az bir yeni mekân ve bir yeni görsel fikir (1: bilet kartları, tren dışarıdan, peron, körük; 2: REC çerçevesi ve lokomotifin arkası; 3: geri sayan zaman etiketi ve örgüdeki yazılar; 4: kondüktör ve zımba; 5: lokomotif, sabah ışığı).
- Dizinin ilk bölümü değilse ilk 10 saniyede tek cümleyle "Önceki bölümde" hatırlatması.
- Bu dizinin efektleri (`whistle`, `brake`, `clack`) `b01/senaryo.py` içinde tanımlı ve `mix_plan` başında `FX` sözlüğüne ekleniyor; sonraki bölümlerde aynı yöntemi kopyala.
- Oynatma listesi kimliği `log.json` içindeki Son Vagon kayıtlarında (`playlist`).
