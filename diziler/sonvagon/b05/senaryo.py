"""Son Vagon, 5. Bolum: Son Durak (dizinin son bolumu). Senaryo, ses gruplari, efekt ve muzik plani.

Yapi: GERI DONUSLU + KAPANIS MONTAJI. Bugun (bir numara ve lokomotif) ile bu aksam (sepya: ev, gise) arasinda gidip gelir;
son bolum sabah montajidir (Karakopru, Degirmen, Yedigol, ev) ve gisede yeni bir yolcuyla kapanir.
Kanca (lokomotif: makinist koltugu bos) -> onceki bolum (disaridan) -> Konduktor duvardaki mikrofondan anons yapar: Son Durak, bir numara ->
"Son Durak benim duragim" -> lokomotifin kilidi acilir -> makinist yok: "Bu tren yolunu biletlerden okur" -> yol tablosu: bos bilet = durmayan tren ->
"Nereden geldiginizi biliyor musunuz?" -> GERI DONUS 1: kapi carpilir -> GERI DONUS 2: gise, "Nereye?" "Ilk kalkan trene." ->
GERI DONUS 3: arkaya bakis, mutfagin isigi yaniyor -> Son Durak gorunur -> Mia biletine kendi eliyle EV yazar -> zimba deler ->
"Eve trenle varilmaz, yurunur": tren ilk kez kapisini acar -> Son Durak, trene bindigi istasyondur (ayni saat, ayni gise) ->
yarim orgu Ada'ya gider -> SABAH MONTAJI: Eli, Ren ve kardesi, Ada (biten orgu), Mia eve yurur ->
"O gece trenden kimse kaybolmadi" -> gisede yeni yolcu -> kapanis karti.
Konusanlar: N anlatici, A anons (Konduktor, hoparlorden), M Mia, C Konduktor, D Ada (tek replik).
"""
import sys
import numpy as np

TITLE = 'SON VAGON'
EP = '5. BÖLÜM'
EP_NAME = 'Son Durak'

SEQ = [
    # ---- 1: kanca: lokomotif; makinist koltugu bos ----
    ('scene', 1),
    ('line', 'm1', 'M', 'Bu treni kim sürüyor?', ['kim'], 0.25),

    # ---- 2: disaridan: lokomotif ve tek vagon ----
    ('scene', 2),
    ('line', 'n1', 'N', "Önceki bölümde Kondüktör sırrı açtı: kimse kaybolmadı, herkes indi. Ama Mia'nın bileti boş.", ['herkes', 'indi.', 'boş.'], 0.3),

    # ---- 3: bir numara: Konduktor duvardaki mikrofonu alir; anons ve levha ----
    ('scene', 3),
    ('beat', 'mic', 1.2),
    ('line', 'a1', 'A', 'Sıradaki istasyon: Son Durak. Bırakılacak vagon: bir numara.', ['Son', 'Durak.', 'bir', 'numara.'], 0.2),

    # ---- 4: Mia (yakin); baslik ----
    ('scene', 4),
    ('line', 'm2', 'M', 'Bir numara mı? Bu son vagon!', ['son', 'vagon!'], 0.1),
    ('beat', 'title', 2.5),

    # ---- 5: ikisi ----
    ('scene', 5),
    ('line', 'c1', 'C', 'Son Durak benim durağım küçük hanım. Bir numara benimle kalır.', ['benim', 'durağım'], 0.3),
    ('line', 'm3', 'M', 'Peki ben? Benim biletim boş!', ['boş!'], 0.3),

    # ---- 6: Konduktor (yakin): lokomotifi gosterir ----
    ('scene', 6),
    ('line', 'c2', 'C', 'Bileti boş olan inemez. Siz lokomotifle devam edersiniz.', ['inemez.', 'lokomotifle'], 0.3),

    # ---- 7: lokomotifin kapisi: kilit acilir ----
    ('scene', 7),
    ('line', 'm4', 'M', 'Lokomotif mi? O kapı kilitli!', ['kilitli!'], 0.1),
    ('beat', 'unlock', 2.2),

    # ---- 8: lokomotif (genis): makinist koltugu bos ----
    ('scene', 8),
    ('line', 'm5', 'M', 'Makinist koltuğu boş! Bu treni kim sürüyor?', ['boş!', 'kim'], 0.3),
    ('line', 'c3', 'C', 'Hiç kimse. Bu tren yolunu biletlerden okur.', ['Hiç', 'kimse.', 'biletlerden'], 0.3),

    # ---- 9: yol tablosu (yakin): bes durak, bir bos bilet ----
    ('scene', 9),
    ('line', 'c4', 'C', 'Boş bilet, durağı olmayan tren demektir. Hiç durmaz.', ['Hiç', 'durmaz.'], 0.2),

    # ---- 10: on cam: karanlik; Mia (yakin) ----
    ('scene', 10),
    ('beat', 'ahead', 1.4),
    ('line', 'm6', 'M', 'Hiç durmayan bir trende tek başıma mı kalacağım?', ['tek', 'başıma'], 0.3),

    # ---- 11: ikisi (lokomotif) ----
    ('scene', 11),
    ('line', 'c5', 'C', 'Nereye gittiğinizi bilmiyorsunuz. Peki nereden geldiğinizi biliyor musunuz?', ['nereden', 'geldiğinizi'], 0.3),

    # ---- 12: GERI DONUS 1 (sepya): ev; kapi carpilir ----
    ('scene', 12),
    ('beat', 'slam', 1.5),
    ('line', 'm7', 'M', 'Bu akşam annemle tartıştık. Kapıyı çarpıp çıktım.', ['çarpıp', 'çıktım.'], 0.3),

    # ---- 13: GERI DONUS 2 (sepya): gise ----
    ('scene', 13),
    ('line', 'm8', 'M', 'Gişedeki adam sordu: Nereye? İlk kalkan trene, dedim.', ['Nereye?', 'İlk', 'kalkan'], 0.0),
    ('beat', 'slip', 1.4),

    # ---- 14: bugun: ikisi ----
    ('scene', 14),
    ('line', 'c6', 'C', 'Kaçan yolcu yer söylemez. Satır o yüzden boş kaldı.', ['boş', 'kaldı.'], 0.3),

    # ---- 15: GERI DONUS 3 (sepya): Mia arkasina bakar; mutfagin isigi ----
    ('scene', 15),
    ('line', 'm9', 'M', 'Ama çıkarken arkama baktım. Mutfağın ışığı hâlâ yanıyordu.', ['ışığı', 'yanıyordu.'], 0.3),

    # ---- 16: Konduktor (yakin) ----
    ('scene', 16),
    ('line', 'c7', 'C', 'Işık yanıyorsa bekleyen var demektir küçük hanım.', ['bekleyen', 'var'], 0.3),

    # ---- 17: on cam: Son Durak'in isiklari; sonra Konduktor ----
    ('scene', 17),
    ('beat', 'near', 1.8),
    ('line', 'c8', 'C', 'Son Durak göründü. Kalem sizde.', ['Kalem', 'sizde.'], 0.3),

    # ---- 18: Mia, kalem bos satirin ustunde; Konduktor ----
    ('scene', 18),
    ('line', 'm10', 'M', 'Ya yanlış yazarsam?', ['yanlış'], 0.3),
    ('line', 'c9', 'C', 'Yanlış durak olmaz küçük hanım. Yalnızca gidilmemiş durak olur.', ['gidilmemiş'], 0.3),

    # ---- 19: Mia karar verir (kosede Ada'nin kasnagi) ----
    ('scene', 19),
    ('line', 'm11', 'M', 'Ada haklıydı. Ne yazacağıma ben karar veririm.', ['ben', 'karar'], 0.1),

    # ---- 20: bilet (cok yakin): kalem EV yazar ----
    ('scene', 20),
    ('beat', 'write', 2.4),
    ('line', 'm12', 'M', 'Ev. Biletime ev yazdım.', ['Ev.', 'ev'], 0.3),

    # ---- 21: Konduktor bileti okur ----
    ('scene', 21),
    ('line', 'c10', 'C', 'Ev. Otuz yıldır bu satırda gördüğüm en güzel durak.', ['en', 'güzel', 'durak.'], 0.1),

    # ---- 22: zimba (cok yakin): bu kez deler ----
    ('scene', 22),
    ('beat', 'punch', 1.5),
    ('line', 'm13', 'M', 'Zımba deldi! Ama ev istasyon değil ki.', ['deldi!', 'istasyon'], 0.3),

    # ---- 23: ikisi ----
    ('scene', 23),
    ('line', 'c11', 'C', 'Eve trenle varılmaz, yürünür. Onun için kapıyı açıyorum.', ['yürünür.', 'kapıyı', 'açıyorum.'], 0.2),

    # ---- 24: Son Durak peronu: tren durur ----
    ('scene', 24),
    ('beat', 'stop', 2.6),

    # ---- 25: vagonun kapisi ilk kez acilir ----
    ('scene', 25),
    ('beat', 'door', 2.2),
    ('line', 'n2', 'N', 'Gece Ekspresi, o gece ilk kez kapısını açtı.', ['ilk', 'kez'], 0.3),

    # ---- 26: istasyon: ayni saat, ayni gise ----
    ('scene', 26),
    ('line', 'm14', 'M', 'Bu saat, bu gişe... Burası trene bindiğim istasyon!', ['bindiğim', 'istasyon!'], 0.3),

    # ---- 27: peron: Konduktor kapida, Mia peronda ----
    ('scene', 27),
    ('line', 'c12', 'C', 'Raylar daire çizer küçük hanım. Son durak, ilk duraktır.', ['daire', 'ilk', 'duraktır.'], 0.3),
    ('line', 'm15', 'M', "Bunu Ada'ya verin. Yarım iş bırakılmaz.", ['Yarım', 'iş'], 0.3),
    ('line', 'c13', 'C', "Veririm. Yedigöl'e her gece uğrarım.", ['her', 'gece'], 0.3),

    # ---- 28: SABAH MONTAJI: Karakopru (Eli), sonra Degirmen (Ren ve kardesi) ----
    ('scene', 28),
    ('line', 'n3', 'N', "Sabah oldu. Karaköprü'de Eli evine yürüdü. Değirmen'de Ren'i kardeşi karşıladı.", ['Sabah', 'Eli', "Ren'i"], 0.0),
    ('beat', 'hug', 1.2),

    # ---- 29: Yedigol: Ada orgusunu bitirir ----
    ('scene', 29),
    ('beat', 'knit', 1.0),
    ('line', 'd1', 'D', 'Yarım iş bırakılmaz demiştim. Bak, bitti kızım.', ['bitti'], 0.3),

    # ---- 30: ev (sabah): Mia eve yurur; kapi acilir ----
    ('scene', 30),
    ('line', 'n4', 'N', 'Mia da eve yürüdü. Mutfağın ışığı hâlâ yanıyordu.', ['eve', 'ışığı'], 0.0),
    ('beat', 'home', 2.0),

    # ---- 31: gece: tren yeniden yolda ----
    ('scene', 31),
    ('line', 'n5', 'N', 'O gece trenden kimse kaybolmadı. Herkes, biletinde yazan yerde indi.', ['kimse', 'kaybolmadı.', 'indi.'], 0.3),

    # ---- 32: gise: yeni bir yolcu ----
    ('scene', 32),
    ('beat', 'new', 1.6),
    ('line', 'a2', 'A', 'Gece Ekspresi yirmi üçte kalkar. Biletinizi boş bırakmayın.', ['boş', 'bırakmayın.'], 0.2),

    # ---- 33: kapanis ----
    ('scene', 33),
    ('beat', 'end', 6.2),
]

# ---- seslendirme: her grup TEK istek, en fazla 2 ses; grup icinde konusanlar sirayla degisir ----
VOICES = {'N': 'Achird', 'A': 'Charon', 'M': 'Leda', 'D': 'Kore', 'C': 'Charon'}
NAMES = {'M': 'Mia', 'D': 'Ada', 'C': 'Max', 'N': 'Anlatici', 'A': 'Anons'}
_DIZI = 'Türkçe bir gerilim çizgi dizisinin son bölümünden replikler seslendir; olay bir gece treninde geçiyor. '
_M = 'Mia on dokuz yaşında, meraklı ve cesur bir genç kadın: hızlı ve canlı konuşuyor. '
_C = ('Max eski bir gece treninin kondüktörü: yaşlıca bir erkek, kibar, resmi, yorgun ama sıcak; "küçük hanım" diye hitap ediyor, '
      'sakin ve tane tane konuşuyor, hiç tehditkâr değil. ')
_SON = 'Her replikten sonra bir saniye dur.'
GROUPS = {
    'an': dict(ids=['n1', 'a1', 'n2', 'a2', 'n5'],
               style='Türkçe bir çizgi dizinin son bölümü için iki ses. Anlatici: dizi anlatıcısı; akıcı okuyor, çok yavaşlamıyor. İlk repliğinde alçak, '
                     'sakin ve tekinsiz bir tonla önceki bölümü hatırlatıyor; ikinci repliğinde sıcak ve hayranlıkla; son repliğinde huzurlu, '
                     'bir masalı bitirir gibi, tane tane. Anons: eski bir trenin kondüktörü hoparlörden anons yapıyor: erkek, kibar, çok sakin, resmi ve '
                     'tane tane, çok yavaşlamadan; ikinci repliğinde hafifçe gülümseyerek. ' + _SON),
    'nd': dict(ids=['n3', 'd1', 'n4'],
               style='Türkçe bir çizgi dizinin mutlu sonu için iki ses. Anlatici: dizi anlatıcısı; sıcak, huzurlu ve gülümseyen bir tonla, akıcı okuyor, '
                     'çok yavaşlamıyor. Ada yaşlı, bilge ve çok sakin bir kadın: gülümseyerek, sevinçle ve şefkatle, yavaş konuşuyor. ' + _SON),
    'cm1': dict(ids=['m1', 'c1', 'm2', 'c2', 'm3', 'c3', 'm4', 'c4', 'm5'],
                style=_DIZI + _M + 'İlk repliğinde korku ve şaşkınlıkla, kısa ve hızlı soruyor; ikincisinde şaşkın, telaşlı; üçüncüsünde endişeyle, '
                      'yüksek sesle; dördüncüsünde şaşkın, itiraz ederek; son repliğinde korkuyla bağırıyor. ' + _C +
                      'İlk repliğinde sakin, sıradan bir şeyi söyler gibi; ikincisinde ciddi ve üzgün; üçüncüsünde sakin, bir sırrı açıklar gibi; '
                      'son repliğinde alçak sesle ama net, ağır ağır, uyarır gibi. ' + _SON),
    'cm2': dict(ids=['m6', 'c5', 'm7', 'c6', 'm8', 'c7', 'm9', 'c8', 'm10'],
                style=_DIZI + _M + 'İlk repliğinde korkuyla, ağlamaklı soruyor; ikincisinde mahcup, üzgün, alçak sesle ama net; üçüncüsünde bir anıyı '
                      'anlatır gibi, sakin; dördüncüsünde özlemle, yumuşak, alçak sesle ama net; son repliğinde çekinerek, kısaca soruyor. ' + _C +
                      'İlk repliğinde şefkatle, düşündüren bir soru soruyor; ikincisinde anlayışla; üçüncüsünde sıcak, gülümseyerek; '
                      'son repliğinde sakin ama acele ettirerek. ' + _SON),
    'cm3': dict(ids=['c9', 'm11', 'c10', 'm12', 'c11', 'm13', 'c12', 'm14', 'c13', 'm15'],
                style=_DIZI + _C + 'İlk repliğinde şefkatle, cesaret vererek; ikincisinde duygulanmış, gülümseyerek, yavaş; üçüncüsünde sıcak, '
                      'bir müjde verir gibi; dördüncüsünde bilgece, gülümseyerek; son repliğinde söz verir gibi, sıcak. ' + _M +
                      'İlk repliğinde kararlı, kendinden emin; ikincisinde sakin ve mutlu, ilk kelimeden sonra kısa bir duraklamayla; üçüncüsünde önce '
                      'sevinçle bağırıyor, sonra şaşkın; dördüncüsünde şaşkınlıkla, fark ederek, heyecanla; son repliğinde sıcak, gülümseyerek. ' + _SON),
}

GAP_SCALE = 1.5
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {}
VOICE_FX = {'A': dict(intercom=True), 'D': dict(rate=0.95)}
TEMPO = {'*': 0.97}

# abone ol bandi: (replik_id, saniye). Bitis sahnesindeki ikinci bant bolum.py icinde.
ABONE = [('c1', 0.3)]
ABONE_END = 1.0                                             # son sahne basladiktan kac sn sonra

# ---- cizim ve sesin ortak kullandigi zamanlar (vurus basina gore saniye) ----
MIC = 0.4                                                   # 'mic' icinde mikrofonun duvardan alindigi an
UNLOCK = (0.45, 0.95, 1.25, 2.0)                            # 'unlock': anahtar girer, kilit acilir, kapi kaymaya baslar, biter
SLAM = 0.3                                                  # 'slam' icinde kapinin carpildigi an
SLIP = 0.25                                                 # 'slip' icinde biletin gise deliginden ciktigi an
WRITE = (0.25, 1.05, 1.25, 2.05)                            # 'write': E harfi (bas, son), V harfi (bas, son)
PUNCH = 0.6                                                 # 'punch' icinde zimbanin kapandigi an
BRAKE, HALT = 0.1, 2.0                                      # 'stop' icinde fren ve durus
DOOR = (0.35, 1.25)                                         # 'door' icinde kapinin acilmaya basladigi ve bittigi an
HUG = 0.45                                                  # 'hug' icinde kardesin Ren'e sarildigi an
HOME = (0.3, 1.1)                                           # 'home' icinde evin kapisinin acildigi anlar
NEW = 0.35                                                  # 'new' icinde gisedeki sorunun belirdigi an


# ---- bu dizinin efektleri (motor/ses.py FX sozlugune eklenir) ----
def _main(): return sys.modules['__main__']
def whistle(d=1.4):
    m = _main(); t = m.tt(d); vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t)
    x = sum(np.sin(2 * np.pi * f * vib * t) / (1 + i * 0.3) for i, f in enumerate((392.0, 466.16, 587.33)))
    n = m.highpass(m.lowpass(m.RNG.standard_normal(len(t)).astype(np.float32), 2600), 700) * 0.5
    return ((x * 0.3 + n * 0.25) * m.env(d, 0.08, d * 0.45)).astype(np.float32) * 0.6
def brake(d=2.0):
    m = _main(); t = m.tt(d); f = 2300 - 900 * (t / d) ** 0.6
    x = np.sin(2 * np.pi * np.cumsum(f) / m.SR) * 0.35 + m.highpass(m.RNG.standard_normal(len(t)).astype(np.float32), 2500) * 0.12
    return (x * m.env(d, 0.25, d * 0.5) * (0.75 + 0.25 * np.sin(2 * np.pi * 9 * t))).astype(np.float32) * 0.45
def clack(d=3.0, rate=1.6):
    """ray sesi: 'ta-tak' ciftleri"""
    m = _main(); y = np.zeros(int(d * m.SR) + 1, dtype=np.float32); th = m.tt(0.16); t0 = 0.0
    while t0 < d - 0.35:
        for o, g in ((0.0, 1.0), (0.13, 0.7)):
            hit = np.sin(2 * np.pi * 86 * th) * np.exp(-th * 34) + 0.3 * m.lowpass(m.RNG.standard_normal(len(th)).astype(np.float32), 700) * np.exp(-th * 55)
            m.put(y, hit.astype(np.float32), t0 + o, g)
        t0 += 1.0 / rate
    return (y[:int(d * m.SR)] * m.env(d, min(0.4, d / 4), min(0.5, d / 4))).astype(np.float32)
def rustle(d=0.5):
    """kagit hisirtisi / kalem sesi: kisa, titrek, tiz gurultu"""
    m = _main(); t = m.tt(d)
    n = m.highpass(m.RNG.standard_normal(len(t)).astype(np.float32), 3200)
    am = np.clip(np.sin(2 * np.pi * 17 * t) * np.sin(2 * np.pi * 5.3 * t + 1.0), 0, 1) ** 0.6
    return (n * am * m.env(d, 0.03, d * 0.4)).astype(np.float32) * 0.5
def punchfx(ok=True):
    """bilet zimbasi: metal 'cik' (+ delerse kisa 'tak')"""
    m = _main(); t = m.tt(0.22)
    x = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 70) + 0.6 * np.sin(2 * np.pi * 3650 * t) * np.exp(-t * 90)
    if ok: x = x + 0.9 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 40) * (t > 0.03)
    else: x = x * 0.5 + 0.5 * m.lowpass(m.RNG.standard_normal(len(t)).astype(np.float32), 500) * np.exp(-t * 30)
    return x.astype(np.float32) * 0.6
def birds(d=2.0, seed=1):
    """sabah: kisa kus civiltilari"""
    m = _main(); y = np.zeros(int(d * m.SR) + 1, dtype=np.float32); r = np.random.default_rng(seed); t0 = 0.05
    while t0 < d - 0.3:
        n = int(r.integers(2, 5)); f0 = float(r.uniform(2600, 4200))
        for j in range(n):
            th = m.tt(0.09); f = f0 * (1 + 0.25 * np.sin(np.pi * th / 0.09)) * (1 + 0.06 * j)
            chirp = np.sin(2 * np.pi * np.cumsum(f) / m.SR) * np.sin(np.pi * th / 0.09) ** 2
            m.put(y, chirp.astype(np.float32), t0 + j * 0.11, 0.5)
        t0 += n * 0.11 + float(r.uniform(0.25, 0.7))
    return (y[:int(d * m.SR)] * m.env(d, 0.1, 0.3)).astype(np.float32) * 0.5


# ---- efekt ve muzik plani ----
def mix_plan(T):
    _main().FX.update(whistle=whistle, brake=brake, clack=clack, rustle=rustle, punchfx=punchfx, birds=birds)
    B, S, L, tot = T['beats'], T['scenes'], {l['id']: l for l in T['lines']}, T['total']
    fr = lambda i, f: L[i]['start'] + (L[i]['end'] - L[i]['start']) * f
    fx = []
    steps = lambda a, b, g=0.22, rate=1.8: fx.append(('steps', a, g, dict(d=max(0.3, b - a), rate=rate)))
    rails = lambda a, b, g=0.2, rate=1.6: fx.append(('clack', a, g, dict(d=max(0.6, b - a), rate=rate)))
    jing = lambda t, g=0.3: [fx.append(('chime', t + o, g, dict(freqs=[f_], d=0.5))) for o, f_ in ((0.0, 1975.5), (0.07, 2349.3), (0.15, 1760.0))]

    # 1: kanca (lokomotif, bos koltuk)
    fx.append(('buzz', 0.0, 0.5, dict(d=0.22))); fx.append(('rumble', 0.0, 0.34, dict(d=1.6)))
    rails(0.0, S[2], 0.24, 2.1)
    # 2: disaridan
    fx.append(('whoosh', S[2] - 0.15, 0.4, dict(d=0.6, up=True))); rails(S[2], S[3], 0.16, 1.8)
    # 3: mikrofon ve anons
    rails(S[3], S[7], 0.09, 1.7)
    mc = B['mic'][0]
    fx.append(('tick', mc + MIC, 0.45, dict(f=900))); fx.append(('buzz', mc + MIC + 0.1, 0.3, dict(d=0.18)))
    fx.append(('chime', mc + 0.6, 0.55, dict(freqs=[659.25, 523.25], d=1.4)))
    fx.append(('hum', L['a1']['start'] - 0.2, 0.22, dict(d=L['a1']['end'] - L['a1']['start'] + 0.5)))
    for o in (0.0, 0.25, 0.5): fx.append(('buzz', fr('a1', 0.62) + o, 0.35, dict(d=0.14)))                 # levha kirmizi yanar
    fx.append(('chime', B['title'][0] + 0.1, 0.6, dict(freqs=[311.13, 466.16, 622.25])))
    # 5-6: Konduktor
    jing(L['c1']['start'] - 0.2, 0.22)
    fx.append(('chime', fr('c2', 0.3), 0.3, dict(freqs=[146.83, 207.65], d=2.4)))
    # 7: lokomotifin kapisi: kilit acilir
    rails(S[7], S[8], 0.12, 1.7)
    fx.append(('buzz', fr('m4', 0.75), 0.3, dict(d=0.18)))
    ul = B['unlock'][0]
    jing(ul + 0.1, 0.3)
    fx.append(('tick', ul + UNLOCK[0], 0.5, dict(f=1500))); fx.append(('tick', ul + UNLOCK[0] + 0.16, 0.4, dict(f=1100)))
    fx.append(('snap', ul + UNLOCK[1], 0.6, {})); fx.append(('tick', ul + UNLOCK[1] + 0.06, 0.45, dict(f=600)))
    fx.append(('slide', ul + UNLOCK[2], 0.55, dict(d=UNLOCK[3] - UNLOCK[2])))
    fx.append(('whoosh', ul + UNLOCK[2], 0.3, dict(d=0.9, up=False)))
    # 8-11: lokomotif: ocak ugultusu, ray
    fx.append(('rumble', S[8], 0.22, dict(d=min(6.0, S[12] - S[8])))); rails(S[8], S[12], 0.16, 2.0)
    fx.append(('hum', S[8], 0.14, dict(d=S[12] - S[8])))
    steps(S[8] + 0.05, S[8] + 0.9, 0.24, 2.6)
    fx.append(('chime', fr('c3', 0.1), 0.34, dict(freqs=[146.83, 220.0, 293.66], d=2.6)))
    for j, f_ in enumerate((0.02, 0.07, 0.12, 0.17, 0.22)): fx.append(('tick', fr('c4', f_), 0.3, dict(f=1200 + 120 * j)))   # tablodaki duraklar yanar
    fx.append(('buzz', fr('c4', 0.32), 0.35, dict(d=0.2))); fx.append(('buzz', fr('c4', 0.74), 0.4, dict(d=0.2))); fx.append(('buzz', fr('c4', 0.74) + 0.3, 0.35, dict(d=0.2)))
    ah = B['ahead'][0]
    fx.append(('whoosh', ah, 0.4, dict(d=1.2, up=False))); fx.append(('whistle', ah + 0.2, 0.4, dict(d=1.1)))
    fx.append(('chime', fr('c5', 0.55), 0.3, dict(freqs=[293.66, 440.0], d=2.2)))
    # 12: geri donus 1: kapi carpilir
    sl = B['slam'][0]
    fx.append(('whoosh', S[12] - 0.12, 0.45, dict(d=0.5, up=True)))
    fx.append(('snap', sl + SLAM, 0.8, {})); fx.append(('rumble', sl + SLAM, 0.3, dict(d=0.5)))
    steps(sl + SLAM + 0.25, L['m7']['start'] + 1.2, 0.26, 2.2)
    # 13: geri donus 2: gise
    fx.append(('whoosh', S[13] - 0.1, 0.3, dict(d=0.5, up=True)))
    fx.append(('ding', fr('m8', 0.02), 0.3, {}))
    sp = B['slip'][0]
    fx.append(('slide', sp + SLIP, 0.35, dict(d=0.4))); fx.append(('rustle', sp + SLIP + 0.1, 0.5, dict(d=0.4)))
    fx.append(('buzz', sp + 0.85, 0.3, dict(d=0.18)))
    # 14: bugun
    fx.append(('whoosh', S[14] - 0.1, 0.3, dict(d=0.5, up=False))); rails(S[14], S[15], 0.14, 2.0)
    # 15: geri donus 3
    fx.append(('whoosh', S[15] - 0.1, 0.3, dict(d=0.5, up=True)))
    fx.append(('chime', fr('m9', 0.5), 0.36, dict(freqs=[349.23, 440.0, 523.25], d=2.6)))
    # 16-19: bugun: Son Durak gorunur
    fx.append(('whoosh', S[16] - 0.1, 0.3, dict(d=0.5, up=False))); rails(S[16], S[20], 0.14, 1.8)
    nr = B['near'][0]
    fx.append(('whistle', nr + 0.2, 0.55, dict(d=1.4)))
    fx.append(('tick', fr('c8', 0.6), 0.35, dict(f=1500)))
    fx.append(('chime', fr('m11', 0.4), 0.34, dict(freqs=[587.33, 880.0], d=2.0)))
    # 20: kalem yazar
    rails(S[20], S[24], 0.07, 1.4)
    wr = B['write'][0]
    for a, b in ((WRITE[0], WRITE[1]), (WRITE[2], WRITE[3])):
        n = 4 if a == WRITE[0] else 2
        for j in range(n): fx.append(('rustle', wr + a + (b - a) * j / n, 0.7, dict(d=(b - a) / n * 0.9)))
    fx.append(('chime', wr + WRITE[3] + 0.05, 0.45, dict(freqs=[523.25, 659.25, 783.99], d=2.4)))
    # 21-22: zimba deler
    pn = B['punch'][0]
    fx.append(('punchfx', pn + PUNCH, 0.7, dict(ok=True))); fx.append(('chime', pn + PUNCH + 0.08, 0.4, dict(freqs=[783.99, 1046.5], d=1.6)))
    # 24: Son Durak: tren durur
    st = B['stop'][0]
    fx.append(('brake', st + BRAKE, 0.6, dict(d=1.9))); rails(st, st + 1.6, 0.2, 1.1)
    fx.append(('rumble', st + HALT - 0.2, 0.3, dict(d=1.0))); fx.append(('whoosh', st + HALT, 0.3, dict(d=0.9, up=False)))
    # 25: kapi acilir
    dr = B['door'][0]
    fx.append(('tick', dr + 0.1, 0.4, dict(f=600))); fx.append(('slide', dr + DOOR[0], 0.6, dict(d=DOOR[1] - DOOR[0])))
    fx.append(('snap', dr + DOOR[1], 0.5, {})); fx.append(('chime', dr + DOOR[1] + 0.05, 0.4, dict(freqs=[392.0, 523.25, 659.25], d=2.6)))
    steps(L['n2']['start'] + 0.3, L['n2']['end'], 0.22, 1.6)
    # 26-27: istasyon
    fx.append(('ding', fr('m14', 0.05), 0.3, {}))
    fx.append(('rustle', fr('m15', 0.15), 0.35, dict(d=0.4)))
    jing(L['c13']['start'] - 0.15, 0.22)
    # 28-30: sabah
    fx.append(('whoosh', S[28] - 0.12, 0.35, dict(d=0.7, up=True)))
    fx.append(('birds', S[28], 0.5, dict(d=S[31] - S[28], seed=3)))
    steps(fr('n3', 0.2), fr('n3', 0.5), 0.2, 1.7)
    hg = B['hug'][0]
    steps(fr('n3', 0.78), hg + HUG, 0.24, 3.4); fx.append(('chime', hg + HUG, 0.34, dict(freqs=[659.25, 783.99], d=1.4)))
    fx.append(('tick', B['knit'][0] + 0.2, 0.3, dict(f=1700))); fx.append(('tick', B['knit'][0] + 0.6, 0.3, dict(f=1900)))
    fx.append(('chime', fr('d1', 0.62), 0.36, dict(freqs=[523.25, 659.25, 783.99], d=2.2)))
    steps(fr('n4', 0.05), fr('n4', 0.5), 0.22, 1.7)
    hm = B['home'][0]
    fx.append(('slide', hm + HOME[0], 0.4, dict(d=HOME[1] - HOME[0]))); fx.append(('chime', hm + HOME[1], 0.45, dict(freqs=[349.23, 440.0, 523.25, 698.46], d=3.0)))
    # 31: gece: tren yeniden yolda
    fx.append(('whoosh', S[31] - 0.12, 0.35, dict(d=0.6, up=True))); rails(S[31], S[32], 0.2, 1.9); fx.append(('whistle', S[31] + 0.3, 0.45, dict(d=1.4)))
    # 32: gise: yeni yolcu
    nw = B['new'][0]
    fx.append(('ding', nw + 0.05, 0.35, {})); fx.append(('tick', nw + NEW, 0.4, dict(f=1500)))
    fx.append(('hum', L['a2']['start'] - 0.2, 0.2, dict(d=L['a2']['end'] - L['a2']['start'] + 0.5)))
    # 33: kapanis
    rails(S[33], S[33] + 3.0, 0.14, 1.7)
    fx.append(('chime', B['end'][0] + 0.15, 0.55, dict(freqs=[261.63, 329.63, 392.0, 523.25], d=3.0)))
    for t0 in [L[i]['start'] + o for i, o in ABONE] + [S[33] + ABONE_END]:                                 # abone ol: tik + kisa zil
        fx.append(('tick', t0 + 2.3, 0.5, dict(f=1200))); fx.append(('chime', t0 + 2.45, 0.32, dict(freqs=[1318.5, 1760.0], d=1.0)))
    # muzik: Mia karar verene kadar gerilim (geri donuslerde gizem); "Ne yazacagima ben karar veririm" ile sicak ve sonuna kadar sicak
    music = [(0.0, S[12], 'gerilim', 0.9), (S[12], S[14], 'gizem', 0.8), (S[14], S[15], 'gerilim', 0.8), (S[15], S[16], 'gizem', 0.8),
             (S[16], L['m11']['start'], 'gerilim', 0.9), (L['m11']['start'], S[28], 'sicak', 0.8), (S[28], S[31], 'sicak', 1.0),
             (S[31], tot, 'sicak', 0.9)]
    return dict(pads=[], fx=fx, music=music)
