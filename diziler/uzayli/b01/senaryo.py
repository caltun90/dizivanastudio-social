"""Kiraci Uzayli, 1. Bolum: Kiralik Oda. Yapi: duz anlatim.
Kucuk mesele: Zip'in ilk kirasi (bozuk parayla, tek tek sayilir).
Deyimler: "Karnim zil caliyor" (cekirdek blok), "ilk teklif reddedilir" (kilavuz kurali, cay israri).
Ucluk kurali: zil 1 (Zip kapiya kosar, kimse yok) -> zil 2 (Zip gobege konusur) -> zil 3 (gercek zil: Hugo).
Dugme: Hugo gidince karin bir kez daha calar, Zip: "Ben bakmiyorum."
Konusanlar: L Luna, T Tobi, Z Zip, H Hugo.
"""
import sys
import numpy as np

TITLE = 'KİRACI UZAYLI'
EP = '1. BÖLÜM'
EP_NAME = 'Kiralık Oda'

SEQ = [
    # 1 KANCA (gece, kanepe): Tobi'nin karnından kapı zili, Zip fırlar
    ('scene', 1),
    ('beat', 'kzil', 0.8),
    ('line', 'z0', 'Z', 'Misafir!', ['Misafir!'], 0.25),
    ('beat', 'title', 2.5),
    # 2 GÜNDÜZ, masa: kira yetmiyor
    ('scene', 2),
    ('line', 'l1', 'L', 'Tobi. Kira yine yetmiyor.', ['yetmiyor.'], 0.35),
    ('line', 't1', 'T', 'Yemekten kısarız.', ['Yemekten'], 0.1),
    ('beat', 'soguk', 1.5),        # ikisi donar; Tobi söylediğinden dehşete düşer, cipsi göğsüne bastırır
    ('line', 't2', 'T', 'Yok. Kiracı bulalım.', ['Kiracı'], 0.4),
    ('line', 'l9', 'L', 'Sessiz, normal, sıradan biri olsun.', ['sıradan'], 0.3),
    ('line', 't15', 'T', 'Az yiyen biri olsun.', ['Az', 'yiyen'], 0.4),
    # 3 kapı: Luna ilanı asmaya gider, daha asmadan kapı çalar
    ('scene', 3),
    ('beat', 'yuru', 1.6),         # Luna elinde KİRALIK ODA ilanıyla kapıya yürür
    ('beat', 'tak', 1.1),          # tak tak tak; Luna'nın eli havada kalır
    ('line', 'l2', 'L', 'Daha asmadım.', ['asmadım.'], 0.3),
    ('beat', 'ac', 1.4),           # kapı açılır: eşikte minik Zip, antenler yaylanır
    ('line', 'z1', 'Z', 'Merhaba Dünyalı! Kılavuz diyor ki: önce tanış.', ['Dünyalı!', 'tanış.'], 0.3),
    ('line', 'l3', 'L', 'Sen kimsin?', ['kimsin?'], 0.25),
    ('line', 'z2', 'Z', 'Ben Zip. Çok uzaktan geldim.', ['Zip.', 'uzaktan'], 0.3),
    ('line', 't3', 'T', 'Ankara mı?', ['Ankara'], 0.3),
    ('line', 'z3', 'Z', 'Biraz daha uzak.', ['daha'], 0.3),
    ('beat', 'antenbak', 1.3),     # Tobi'nin gözü yavaşça antenlere çıkar; antenler el sallar gibi sallanır
    ('line', 't4', 'T', 'Antenlerin var.', ['Antenlerin'], 0.3),
    ('line', 'z4', 'Z', 'Sağ olun. Sizin yok. Geçmiş olsun.', ['Geçmiş', 'olsun.'], 0.2),
    ('beat', 'gecmis', 1.2),       # Luna kameraya bakar
    # 4 içeride, kanepe: çay ısrarı
    ('scene', 4),
    ('line', 'l4', 'L', 'Çay içer misin?', ['Çay'], 0.3),
    ('line', 'z5', 'Z', 'Hayır. Kılavuz diyor ki: ilk teklif reddedilir.', ['Hayır.', 'reddedilir.'], 0.3),
    ('line', 'l5', 'L', 'Peki.', ['Peki.'], 0.1),
    ('beat', 'bekle', 2.8),        # Zip umutla bekler; antenleri yavaş yavaş düşer
    ('line', 'z6', 'Z', 'İkinci teklif gelmedi.', ['gelmedi.'], 0.4),
    ('line', 't5', 'T', 'Gelmez. Ben hep ilkinde alırım.', ['ilkinde'], 0.5),
    # 5 kira: bozuk para
    ('scene', 5),
    ('line', 'l6', 'L', 'Zip. Kira peşin.', ['peşin.'], 0.3),
    ('line', 'z7', 'Z', 'Hazır. Bozuk var.', ['Bozuk'], 0.1),
    ('beat', 'para', 1.9),         # Zip sehpaya bir dağ bozuk para döker
    ('line', 'z8', 'Z', 'Bir. İki. Üç.', ['Bir.', 'İki.', 'Üç.'], 0.35),
    ('line', 't6', 'T', 'Kaç tane var?', ['Kaç'], 0.3),
    ('line', 'z9', 'Z', 'On iki bin. Dört.', ['bin.', 'Dört.'], 0.2),
    ('beat', 'lunacam', 1.4),      # Luna yavaşça kameraya döner
    ('beat', 'saat', 2.6),         # kart: ÜÇ SAAT SONRA; pencere geceye döner
    # 6 GECE, kanepe: karnım zil çalıyor
    ('scene', 6),
    ('line', 'z10', 'Z', 'Dört yüz bir. Dört yüz iki.', ['bir.', 'iki.'], 0.4),
    ('line', 't7', 'T', 'Karnım zil çalıyor.', ['zil', 'çalıyor.'], 0.1),
    ('beat', 'zil1', 1.25),        # karından kapı zili; göbek sallanır; Zip'in antenleri fırlar, çifte bakış
    ('line', 'z11', 'Z', 'Misafir!', ['Misafir!'], 0.05),
    ('scene', 7),
    ('beat', 'kos1', 1.4),         # Zip kapıya koşar, kapıyı açar
    ('beat', 'bos1', 1.0),         # boş koridor, donma
    ('line', 'z12', 'Z', 'Kimse yok.', ['yok.'], 0.4),
    ('scene', 8),
    ('line', 't8', 'T', 'Zip, o bir deyim. Yani acıktım.', ['deyim.', 'acıktım.'], 0.3),
    ('line', 'z13', 'Z', 'Anladım. Yeni kural: zil çalarsa kapıya bakılmaz.', ['bakılmaz.'], 0.45),
    ('beat', 'zil2', 1.4),         # karın yine çalar; Zip kapıya doğru çekilir, direnir, göbeğe döner
    ('line', 'z14', 'Z', 'Evde yokuz! Sonra gelin!', ['yokuz!', 'gelin!'], 0.15),
    ('beat', 'bakis', 1.0),        # Tobi yavaşça Zip'e bakar
    ('line', 't9', 'T', 'Boşuna. Ben yıllardır deniyorum.', ['yıllardır'], 0.45),
    ('beat', 'zil3', 1.0),         # bu kez gerçek kapı zili
    ('line', 'z15', 'Z', 'Yokuz dedik!', ['dedik!'], 0.35),
    ('line', 't10', 'T', 'Zip... o ben değilim.', ['değilim.'], 0.1),
    ('beat', 'donma', 1.5),        # ikisi donar, yavaşça kapıya döner
    # 9 Hugo: önce burun
    ('scene', 9),
    ('beat', 'burun', 1.6),        # kapı açılır; kadrajı önce Hugo'nun burnu doldurur, koklar
    ('line', 'h1', 'H', 'Hımm. Bu kapı bugün üç kez açıldı.', ['üç', 'kez'], 0.2),
    ('beat', 'sakla', 0.9),        # Zip ışık hızıyla Tobi'nin arkasına; Luna odasından gelir
    ('line', 'l7', 'L', 'Hugo Bey! Kira yarın, söz.', ['yarın,'], 0.3),
    ('line', 'h8', 'H', 'Bu ay on bir kez yarın dediniz.', ['on', 'bir', 'kez'], 0.35),
    ('line', 'l10', 'L', 'On iki oldu.', ['iki'], 0.5),
    ('line', 'h2', 'H', 'Kira değil. Koku. Çilek ve yıldız tozu.', ['Koku.', 'yıldız', 'tozu.'], 0.35),
    ('line', 't11', 'T', 'Cips. Çilekli.', ['Çilekli.'], 0.3),
    ('line', 'h3', 'H', 'Çilekli cips mi olur?', ['olur?'], 0.45),
    ('line', 't12', 'T', 'Olur. Ben yerim.', ['yerim.'], 0.2),
    ('beat', 'anten', 1.8),        # Zip'in anteni Tobi'nin başının üstünden yükselir; Tobi bakmadan boyunu uzatıp antenleri kafasıyla ezer
    ('line', 'h9', 'H', 'Başınızın üstünde bir şey kıpırdadı.', ['kıpırdadı.'], 0.35),
    ('line', 't16', 'T', 'Saçım. Heyecanlandı.', ['Heyecanlandı.'], 0.5),
    ('line', 'h4', 'H', 'Sehpada dört yüz on bozuk para var.', ['dört', 'yüz', 'on'], 0.3),
    ('line', 'l8', 'L', 'Kumbara. Kiranız için.', ['Kumbara.'], 0.3),
    ('line', 'z16', 'Z', 'Dört yüz on bir.', ['bir.'], 0.1),
    ('beat', 'duy', 1.3),          # herkes donar; Hugo yavaşça döner
    ('line', 'h5', 'H', 'Beni kim düzeltti?', ['kim'], 0.4),
    ('line', 't13', 'T', 'Karnım. Bazen konuşur.', ['konuşur.'], 0.2),
    ('beat', 'egil', 1.6),         # Hugo eğilip göbeği koklar
    ('line', 'h10', 'H', 'Soğan. Sarımsak. Dünkü mantı.', ['mantı.'], 0.35),
    ('line', 't17', 'T', 'Evvelsi günkü.', ['Evvelsi'], 0.5),
    ('line', 'h6', 'H', 'Yedinci madde: tuhaf koku yasak.', ['Yedinci', 'yasak.'], 0.3),
    ('line', 't14', 'T', 'Biliyoruz.', ['Biliyoruz.'], 0.3),
    ('line', 'h7', 'H', 'Bu burun yanılmaz, Tobi. Yanılmaz.', ['yanılmaz,', 'Yanılmaz.'], 0.2),
    ('beat', 'kapat', 1.4),        # Hugo geri geri çıkar, kapı kapanır
    ('beat', 'sessiz', 1.6),       # üçü kıpırtısız
    ('beat', 'zil4', 1.1),         # karın son kez çalar
    ('line', 'z17', 'Z', 'Ben bakmıyorum.', ['bakmıyorum.'], 0.3),
    # 10 bitiş kartı
    ('scene', 10),
    ('beat', 'end', 7.0),
]
VOICES = {'H': 'Orus', 'T': 'Puck', 'L': 'Aoede', 'Z': 'Fenrir', 'N': 'Achird'}
NAMES = {'H': 'Hugo', 'T': 'Tobi', 'L': 'Luna', 'Z': 'Zip', 'N': 'Anlatici'}
_DIZI = ('Türkçe bir komedi çizgi dizisinden replikler seslendir; olay bir öğrenci evinde geçiyor. Komedi ciddiyetten gelir: '
         'kimse bağırmaz, kimse abartmaz, herkes durumu çok ciddiye alır; sakin, düz, net ve tane tane. ')
_L = 'Luna genç bir kadın, evin aklı: sabırlı, bilgiç, biraz yorgun; kısa ve düz konuşur. '
_T = 'Tobi genç, tombul, iyi kalpli bir aşçılık öğrencisi: ağır, kısa, düz ve uykulu bir sesle, hiç heyecanlanmadan konuşur. '
_Z = 'Zip küçük, çok kibar bir uzaylı: hevesli, tane tane, kendinden çok emin ama alçak sesli. '
_H = 'Hugo yaşlıca, resmi, kuşkucu bir ev sahibi: yavaş, alçak sesle, şüpheyle ve sayarak konuşur. '
_SON = 'Her replikten sonra bir saniye dur.'
GROUPS = {
    'lz': dict(ids=['z10', 'l2', 'z1', 'l3', 'z2', 'l4', 'z5', 'l5', 'z6', 'l6', 'z7', 'l9'],
               style=_DIZI + _L + _Z + 'Zip "Dört yüz bir. Dört yüz iki." cümlesini kendi kendine para sayar gibi mırıldanır; '
                     '"İkinci teklif gelmedi." cümlesini kırgın ve kibar söyler. ' + _SON),
    'tz1': dict(ids=['t3', 'z3', 't4', 'z4', 't5', 'z8', 't6', 'z9', 't1', 'z12', 't15'],
                style=_DIZI + _T + _Z + 'Zip "Bir. İki. Üç." ve "On iki bin. Dört." cümlelerinde bozuk parayı tek tek, yavaş yavaş sayar; '
                      '"Kimse yok." cümlesini şaşkın ve düz söyler. ' + _SON),
    'tz2': dict(ids=['t7', 'z11', 't8', 'z13', 't9', 'z14', 't10', 'z15', 't2', 'z16', 't14', 'z17'],
                style=_DIZI + _T + _Z + 'Tobi "Boşuna. Ben yıllardır deniyorum." cümlesini kabullenmiş bir iç çekişle söyler. '
                      'Zip "Misafir!" kelimesini sevinçle, "Evde yokuz! Sonra gelin!" ve "Yokuz dedik!" cümlelerini kapıya seslenir gibi ama kibarca söyler; '
                      'son iki repliğini, "Dört yüz on bir." ve "Ben bakmıyorum." cümlelerini fısıldayarak ama net söyler. ' + _SON),
    # 'ht' tek istekte bozuk geldi (651 sn, sessiz); KIT 5'e göre ikiye bölündü
    'ht1': dict(ids=['h2', 't11', 'h3', 't12', 'h9', 't16'],
                style=_DIZI + _H + 'Tobi ağır, kısa ve tamamen ciddi; "Olur. Ben yerim." cümlesini omuz silker gibi düz söyler. ' + _SON),
    'ht2': dict(ids=['h5', 't13', 'h10', 't17', 'h6'],
                style=_DIZI + _H + 'Tobi ağır, kısa ve tamamen ciddi. Hugo "Soğan. Sarımsak. Dünkü mantı." derken her kelimeden sonra kısa durur. ' + _SON),
    'hl': dict(ids=['l1', 'h1', 'l7', 'h8', 'l10', 'h4', 'l8', 'h7'],
               style=_DIZI + _H + _L + 'Hugo "üç kez" ve "dört yüz on" sözlerini tek tek vurgular; "Bu burun yanılmaz, Tobi. Yanılmaz." cümlesini '
                     'uyarır gibi, alçak sesle söyler. ' + _SON),
}
GAP_SCALE = 1.25
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {'z0': 'z11'}        # kancadaki "Misafir!" 6. sahnedeki kayıtla aynı
VOICE_FX = {'Z': dict(rate=1.12)}
TEMPO = {'*': 1.0}
ABONE = [('z2', 0.3)]            # yeni motorda story.js overlay çizer; tık ve zil mix_plan'da
ABONE_END = 1.6

def mix_plan(T):
    L = {l['id']: l for l in T['lines']}; S = T['scenes']; B = T['beats']; tot = T['total']
    st = lambda i: L[i]['start']; en = lambda i: L[i]['end']
    rng = np.random.default_rng(3)
    fx = [
        ('ding', B['kzil'][0] + 0.03, 0.95, {}),                        # KANCA: karından kapı zili
        ('boing', B['kzil'][0] + 0.4, 0.5, dict(d=0.5)),
        ('chime', B['title'][0] + 0.15, 0.5, dict(freqs=[523, 659, 784], d=1.8)),
        ('whistle_down', B['soguk'][0] + 0.25, 0.4, dict(d=0.9)),       # "yemekten kısarız": dehşet
        ('steps', B['yuru'][0] + 0.1, 0.4, dict(d=1.3, rate=2.4)),
        ('knock', B['tak'][0] + 0.1, 0.9, dict(n=3)),
        ('slide', B['ac'][0] + 0.05, 0.35, dict(d=0.6)),
        ('boing', B['ac'][0] + 0.65, 0.55, dict(d=0.7)),                # antenler yaylanır
        ('zip', B['antenbak'][0] + 0.45, 0.45, dict(d=0.6)),            # antenler el sallar
        ('pop', B['gecmis'][0] + 0.35, 0.5, {}),
        ('whistle_down', B['bekle'][0] + 0.7, 0.35, dict(d=1.4)),       # antenler düşer
        ('whoosh', B['para'][0] + 0.05, 0.5, dict(d=0.4)),
        ('tick', st('z8') + 0.05, 0.6, dict(f=2600)), ('tick', (st('z8') + en('z8')) / 2, 0.6, dict(f=2900)), ('tick', en('z8') - 0.15, 0.6, dict(f=3200)),
        ('tick', en('z9') - 0.1, 0.6, dict(f=3500)),
        ('pop', B['lunacam'][0] + 0.5, 0.45, {}),
        ('chime', B['saat'][0] + 0.2, 0.45, dict(freqs=[392, 494, 587], d=1.8)),
        ('tick', st('z10') + 0.2, 0.5, dict(f=2600)), ('tick', en('z10') - 0.2, 0.5, dict(f=2900)),
        ('ding', B['zil1'][0] + 0.05, 0.9, {}),                         # karından kapı zili
        ('boing', B['zil1'][0] + 0.55, 0.55, dict(d=0.6)),              # Zip'in antenleri
        ('whoosh', B['kos1'][0] + 0.05, 0.6, dict(d=0.5)),              # koşu
        ('slide', B['kos1'][0] + 0.85, 0.35, dict(d=0.5)),              # kapı açılır
        ('ding', B['zil2'][0] + 0.05, 0.9, {}),                         # karın yine
        ('ding', B['zil3'][0] + 0.05, 1.25, {}),                        # gerçek zil (daha yüksek)
        ('whistle_down', B['donma'][0] + 0.15, 0.45, dict(d=0.8)),      # donma
        ('slide', S[9] + 0.05, 0.35, dict(d=0.6)),                      # kapı açılır
        ('sniff', B['burun'][0] + 0.4, 0.7, dict(n=3)),                 # Hugo koklar
        ('whoosh', B['sakla'][0] + 0.05, 0.7, dict(d=0.35)),            # Zip saklanır
        ('sniff', st('h2') + 0.9, 0.5, dict(n=2)),
        ('munch', st('t12') + 0.05, 0.5, dict(n=4)),
        ('zip', B['anten'][0] + 0.1, 0.5, dict(d=0.6)),                 # anten yükselir
        ('whistle_up', B['anten'][0] + 0.8, 0.45, dict(d=0.35)), ('boing', B['anten'][0] + 1.1, 0.45, dict(d=0.5)),   # Tobi uzar, başı antenleri ezer
        ('whistle_down', B['duy'][0] + 0.2, 0.4, dict(d=0.8)),
        ('sniff', B['egil'][0] + 0.5, 0.7, dict(n=4)),                  # Hugo göbeği koklar
        ('steps', B['kapat'][0], 0.4, dict(d=0.8, rate=3.0)),
        ('slide', B['kapat'][0] + 0.6, 0.35, dict(d=0.5)),              # kapı kapanır
        ('ding', B['zil4'][0] + 0.05, 0.8, {}),                         # düğme
        ('chime', S[10] + 0.2, 0.5, dict(freqs=[523, 659, 784, 1047], d=2.4)),
    ]
    for k in range(14):                                                 # bozuk para yağmuru
        fx.append(('tick', B['para'][0] + 0.35 + k * 0.085 + float(rng.uniform(0, .03)), 0.5, dict(f=float(rng.uniform(2300, 4200)))))
    for t0 in (st(ABONE[0][0]) + ABONE[0][1], S[10] + ABONE_END):       # abone bandı: tık ve kısa zil
        fx += [('tick', t0 + 2.1, 0.5, {}), ('chime', t0 + 2.2, 0.3, dict(freqs=[880, 1319], d=0.9))]
    music = [(B['title'][0], B['soguk'][0] + 0.1, 'komik', 0.85),                 # vuruştan önce sessizlik
             (st('t2') - 0.1, B['tak'][0], 'komik', 0.8),
             (B['ac'][0] + 0.9, B['bekle'][0] + 0.3, 'komik', 0.75),
             (st('t5'), B['lunacam'][0] + 0.3, 'komik', 0.8),
             (B['saat'][0] + 0.2, B['zil1'][0], 'sinsi', 0.5),
             (S[7], B['zil3'][0], 'komik', 0.8),
             (B['zil3'][1] + 0.4, B['donma'][0], 'sinsi', 0.6),
             (S[9] + 0.2, B['duy'][0], 'sinsi', 0.85),
             (st('h5'), B['kapat'][0] + 0.3, 'sinsi', 0.8),
             (S[10], tot, 'komik', 0.85)]
    return dict(pads=[], fx=fx, music=music)
