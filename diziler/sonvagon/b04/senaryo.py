"""Son Vagon, 4. Bolum: Konduktor. Senaryo, ses gruplari, efekt ve muzik plani.

Yapi: MEKTUP BICIMINDE. Ada'nin yarim orgusunun icinden Mia'ya yazdigi not (ve bir kursun kalem) cikar; bolumu Ada'nin sesi
anlatir (D replikleri: mektup; ekranda nakis kasnagi icinde Ada ve kagit). Goruntude Mia iki numaradan bir numaraya gecer.
Kanca (bir numaranin arka kapisi: ardinda vagon yok ama camda bir fener) -> onceki bolum (disaridan) -> orgunun icinden not ->
baslik -> mektup -> anons: Sarnic, iki numara -> koruk -> bir numara, lokomotifin kapisi kilitli -> Sarnic peronu ->
arka kapi: iki numara (bos) soner, bos ray -> rayda bir fener yaklasir, kapi acilir: KONDUKTOR ->
"Kimse kaybolmadi kucuk hanim. Herkes indi." -> zimbali biletler (halka) -> Mia'nin bileti zimbalanamaz: bos ->
"Bileti bos olan inemez." "Bu tren, Son Durak'tan sonra hic durmaz." -> mektubun sonu: kalem -> soru.
Konusanlar: N anlatici, A anons, M Mia, D Ada (mektup), C Konduktor (anonstaki ses, bu kez hoparlorsuz).
"""
import sys
import numpy as np

TITLE = 'SON VAGON'
EP = '4. BÖLÜM'
EP_NAME = 'Kondüktör'

SEQ = [
    # ---- 1: kanca: bir numaranin arka kapisi; ardinda vagon yok, camda bir fener ----
    ('scene', 1),
    ('line', 'm1', 'M', 'Kapıda biri var!', ['biri'], 0.25),

    # ---- 2: disaridan: iki vagon ----
    ('scene', 2),
    ('line', 'n1', 'N', "Önceki bölümde Ada, Yedigöl'de kaldı. Trende tek yolcu var: Mia.", ['Ada,', 'tek', 'yolcu'], 0.3),

    # ---- 3: iki numara: Mia orguyu sikar, icinden bir sey cikar ----
    ('scene', 3),
    ('beat', 'feel', 0.9),
    ('line', 'm2', 'M', "Ada'nın örgüsü hışırdıyor. İçinde bir şey var!", ['hışırdıyor.'], 0.0),
    ('beat', 'find', 2.0),

    # ---- 4: eller (cok yakin): rulo not ve kursun kalem; baslik ----
    ('scene', 4),
    ('line', 'm3', 'M', 'Bir not. İçine kurşun kalem sarılmış.', ['not.', 'kurşun', 'kalem'], 0.2),
    ('beat', 'title', 2.5),

    # ---- 5: mektup (kagit ve kasnakta Ada) ----
    ('scene', 5),
    ('line', 'd1', 'D', 'Mia, kızım. Bu notu bulduysan ben yerime vardım.', ['yerime', 'vardım.'], 0.3),

    # ---- 6: Mia okur; arka kapiya bakar: bos ray ----
    ('scene', 6),
    ('line', 'd2', 'D', 'Arkana bakıp üzülme. Giden vagona ağlanmaz, öndekine yürünür.', ['öndekine', 'yürünür.'], 0.2),

    # ---- 7: anons (hoparlor ve levha) ----
    ('scene', 7),
    ('beat', 'chime', 1.2),
    ('line', 'a1', 'A', 'Sıradaki istasyon: Sarnıç. Bırakılacak vagon: iki numara.', ['Sarnıç.', 'iki', 'numara.'], 0.2),

    # ---- 8: iki numara (genis): Mia one kosar ----
    ('scene', 8),
    ('line', 'm4', 'M', 'İki numara mı? Burası iki numara!', ['Burası'], 0.2),

    # ---- 9: koruk: ikiden bire ----
    ('scene', 9),
    ('line', 'd3', 'D', 'Korkarsan durakları say kızım: Karaköprü, Değirmen, Yedigöl. Hepsi durak, hiçbiri uçurum değil.', ['Karaköprü,', 'Değirmen,', 'Yedigöl.', 'uçurum'], 0.2),

    # ---- 10: bir numara (genis): Mia girer ----
    ('scene', 10),
    ('beat', 'enter', 1.9),

    # ---- 11: lokomotifin kapisi: asma kilit ----
    ('scene', 11),
    ('beat', 'lock', 1.0),
    ('line', 'm5', 'M', 'Bir numara. Önümde yalnızca lokomotif var, o da kilitli.', ['kilitli.'], 0.3),

    # ---- 12: Mia notu okur (yakin) ----
    ('scene', 12),
    ('line', 'd4', 'D', 'O anonsu yapan bir ses var kızım. Her sesin bir sahibi olur.', ['sahibi'], 0.2),

    # ---- 13: Sarnic peronu: tren durur ----
    ('scene', 13),
    ('beat', 'stop', 3.0),

    # ---- 14: bir numaranin arka kapisi: iki numara soner, sis, bos ray ----
    ('scene', 14),
    ('beat', 'out', 3.0),
    ('line', 'm6', 'M', 'İki numara gitti. İçinde kimse yoktu.', ['kimse', 'yoktu.'], 0.1),

    # ---- 15: cam (yakin): rayda bir fener yaklasir; kapi acilir ----
    ('scene', 15),
    ('beat', 'lamp', 2.8),
    ('line', 'm7', 'M', 'Arkada vagon yok. Ama kapıda biri var!', ['vagon', 'yok.', 'biri'], 0.0),
    ('beat', 'open', 2.0),

    # ---- 16: bir numara (genis): Konduktor kapida ----
    ('scene', 16),
    ('line', 'c1', 'C', 'İyi geceler küçük hanım. Biletiniz lütfen.', ['Biletiniz'], 0.3),
    ('line', 'm8', 'M', 'Bu ses... Anonstaki ses sizsiniz!', ['Anonstaki'], 0.3),

    # ---- 17: Konduktor (yakin) ----
    ('scene', 17),
    ('line', 'c2', 'C', 'Benim. Otuz yıldır bu trenin kondüktörüyüm.', ['kondüktörüyüm.'], 0.3),

    # ---- 18: ikisi ----
    ('scene', 18),
    ('line', 'm9', 'M', 'O kapının ardında vagon yok! Nereden geldiniz?', ['Nereden'], 0.3),
    ('line', 'c3', 'C', "Sarnıç'tan. Her istasyonda iner, vagonu yerine bırakırım.", ["Sarnıç'tan.", 'bırakırım.'], 0.3),

    # ---- 19: Mia (yakin) ----
    ('scene', 19),
    ('line', 'm10', 'M', 'Eli, Ren, Ada... Hepsi sizin yüzünüzden kayboldu!', ['kayboldu!'], 0.2),

    # ---- 20: Konduktor (yakin): bilet halkasini kaldirir ----
    ('scene', 20),
    ('beat', 'jingle', 0.9),
    ('line', 'c4', 'C', 'Kimse kaybolmadı küçük hanım. Herkes indi.', ['kaybolmadı', 'indi.'], 0.4),

    # ---- 21: ikisi ----
    ('scene', 21),
    ('line', 'm11', 'M', 'İndi mi? Kapılar hiç açılmadı!', ['açılmadı!'], 0.3),
    ('line', 'c5', 'C', 'Açılmaz. Bu trende yolcu, vagonuyla birlikte iner.', ['vagonuyla'], 0.2),

    # ---- 22: halka (cok yakin): uc zimbali bilet ----
    ('scene', 22),
    ('beat', 'ring', 2.7),
    ('line', 'm12', 'M', 'Karaköprü, Değirmen, Yedigöl. Üçü de zımbalı.', ['zımbalı.'], 0.3),
    ('line', 'c6', 'C', 'Zımbalı bilet, yerine varmış yolcu demektir.', ['yerine', 'varmış'], 0.2),

    # ---- 23: mektup: uc istasyon, uc yolcu (sepya) ----
    ('scene', 23),
    ('line', 'd5', 'D', 'Eli korkmadı, Ren korkmadı, ben de korkmadım. Çünkü yolcu durağını tanır kızım.', ['korkmadım.', 'durağını', 'tanır'], 0.3),

    # ---- 24: sira Mia'da: biletini uzatir ----
    ('scene', 24),
    ('line', 'c7', 'C', 'Şimdi sıra sizde. Biletiniz?', ['sıra', 'sizde.'], 0.3),
    ('line', 'm13', 'M', 'Buyurun. Ama benimki biraz tuhaf.', ['tuhaf.'], 0.0),

    # ---- 25: zimba ve bos bilet (cok yakin) ----
    ('scene', 25),
    ('beat', 'punch', 2.8),
    ('line', 'c8', 'C', 'Zımba tutmuyor. İniş satırınız boş.', ['boş.'], 0.3),

    # ---- 26: Mia (yakin) ----
    ('scene', 26),
    ('line', 'm14', 'M', 'Gişede ilk kalkan trene bilet istedim. Yer söylemedim.', ['ilk', 'kalkan'], 0.3),

    # ---- 27: Konduktor (yakin), sonra ikisi ----
    ('scene', 27),
    ('line', 'c9', 'C', 'Bileti boş olan inemez küçük hanım.', ['inemez'], 0.3),
    ('line', 'm15', 'M', "Ya Son Durak'ta?", ['Son', "Durak'ta?"], 0.3),
    ('line', 'c10', 'C', "Bu tren, Son Durak'tan sonra hiç durmaz.", ['hiç', 'durmaz.'], 0.2),

    # ---- 28: disaridan: lokomotif ve tek vagon karanliga gider ----
    ('scene', 28),
    ('beat', 'dark', 2.8),

    # ---- 29: Mia, not ve bos bilet ----
    ('scene', 29),
    ('line', 'd6', 'D', 'Benim biletimde bir yer yazıyordu kızım. Seninki boş.', ['boş.'], 0.3),
    ('line', 'd7', 'D', 'Boş bilet kötü bilet değildir. Henüz yazılmamış bilettir.', ['yazılmamış'], 0.3),

    # ---- 30: kalem ve bos satir (cok yakin) ----
    ('scene', 30),
    ('line', 'd8', 'D', 'Kalemi onun için koydum. Ne yazacağına sen karar ver.', ['Kalemi', 'sen'], 0.4),

    # ---- 31: kapanis ----
    ('scene', 31),
    ('line', 'n2', 'N', 'Mia biletine ne yazacak?', ['ne', 'yazacak?'], 0.3),
    ('beat', 'end', 6.6),
]

# ---- seslendirme: her grup TEK istek, en fazla 2 ses; grup icinde konusanlar sirayla degisir ----
VOICES = {'N': 'Achird', 'A': 'Charon', 'M': 'Leda', 'D': 'Kore', 'C': 'Charon'}
NAMES = {'M': 'Mia', 'D': 'Ada', 'C': 'Max', 'N': 'Anlatici', 'A': 'Anons'}
_DIZI = 'Türkçe bir gerilim çizgi dizisinden replikler seslendir; olay bir gece treninde geçiyor. '
_M = 'Mia on dokuz yaşında, meraklı ve cesur bir genç kadın: hızlı ve canlı konuşuyor. '
_D = ('Ada yaşlı, bilge ve çok sakin bir kadın. Mia\'ya yazdığı bir mektubu kendi sesiyle okuyor: yavaş, sıcak, şefkatli ve kendinden emin, '
      'atasözü söyler gibi, hiç telaşlanmadan. ')
_C = ('Max eski bir gece treninin kondüktörü: yaşlıca bir erkek, kibar, resmi, yorgun ama sıcak; "küçük hanım" diye hitap ediyor, '
      'sakin ve tane tane konuşuyor, hiç tehditkâr değil. ')
_SON = 'Her replikten sonra bir saniye dur.'
GROUPS = {
    'an': dict(ids=['n1', 'a1', 'n2'],
               style='Türkçe bir gerilim çizgi dizisi için iki ses. Anlatici: gerilim dizisi anlatıcısı; alçak, sakin ve tekinsiz bir tonla, akıcı okuyor, '
                     'çok yavaşlamıyor; son repliğini merak uyandıran bir soru olarak soruyor. Anons: eski bir trenin kondüktörü hoparlörden anons yapıyor: '
                     'erkek, kibar, çok sakin, resmi ve tane tane, çok yavaşlamadan. ' + _SON),
    'dm1': dict(ids=['d1', 'm1', 'd2', 'm2', 'd3', 'm3', 'd4', 'm4'],
                style=_DIZI + _D + 'Üçüncü repliğinde üç istasyon adını tek tek, sayar gibi okuyor. ' + _M +
                      'İlk repliğinde korkuyla, kısa ve yüksek sesle bağırıyor; ikincisinde şaşkın ve meraklı; üçüncüsünde şaşkın, alçak sesle ama net; '
                      'son repliğinde önce şaşkınlıkla soruyor, sonra telaşla bağırıyor. ' + _SON),
    'dm2': dict(ids=['d5', 'm5', 'd6', 'm6', 'd7', 'm7', 'd8'],
                style=_DIZI + _D + 'Son repliğinde gülümseyerek, bir sır emanet eder gibi, alçak sesle ama net, tane tane. ' + _M +
                      'İlk repliğinde nefes nefese, hayal kırıklığıyla; ikincisinde tedirgin, alçak sesle ama net; '
                      'son repliğinde önce fısıltıya yakın ama net, sonra korkuyla bağırıyor. ' + _SON),
    'cm1': dict(ids=['c1', 'm8', 'c2', 'm9', 'c3', 'm10', 'c4', 'm11', 'c5'],
                style=_DIZI + _C + 'İlk repliğinde nazikçe selam veriyor; ikincisinde yorgun bir gururla; üçüncüsünde sıradan bir işi anlatır gibi; '
                      'dördüncüsünde şefkatle, yavaş ve tane tane, bir sırrı açıklıyor; son repliğinde sabırla açıklıyor. ' + _M +
                      'İlk repliğinde şaşkınlıkla, sesi tanıyarak; ikincisinde korkuyla, yüksek sesle; üçüncüsünde öfkeyle, ağlamaklı bağırıyor; '
                      'son repliğinde şaşkın, inanamayarak soruyor. ' + _SON),
    'cm2': dict(ids=['c6', 'm12', 'c7', 'm13', 'c8', 'm14', 'c9', 'm15', 'c10'],
                style=_DIZI + _C + 'İlk repliğinde atasözü söyler gibi; ikincisinde nazikçe, elini uzatarak; üçüncüsünde şaşkın, üzgün; '
                      'dördüncüsünde ciddi ve üzgün, yavaş; son repliğinde alçak sesle ama net, ağır ağır, uyarır gibi. ' + _M +
                      'İlk repliğinde üç istasyon adını tek tek, şaşkınlıkla okuyor; ikincisinde çekinerek; üçüncüsünde mahcup, alçak sesle ama net; '
                      'son repliğinde korkuyla, kısaca soruyor. ' + _SON),
}

GAP_SCALE = 1.5
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {}
VOICE_FX = {'A': dict(intercom=True), 'D': dict(rate=0.95)}
TEMPO = {'*': 0.97}

# abone ol bandi: (replik_id, saniye). Bitis sahnesindeki ikinci bant bolum.py icinde.
ABONE = [('d1', 1.2)]
ABONE_END = 1.0                                             # son sahne basladiktan kac sn sonra

# ---- cizim ve sesin ortak kullandigi zamanlar (vurus basina gore saniye) ----
FEEL = (0.2, 0.55)                                          # 'feel' icinde orgunun sikildigi anlar
FIND = 0.7                                                  # 'find' icinde notun orguden ciktigi an
LOCKS = (0.2, 0.55)                                         # 'lock' icinde kilidin sarsildigi anlar
BRAKE, HALT = 0.1, 2.0                                      # 'stop' icinde fren ve durus
OUT_OFF = (0.4, 0.85, 1.3)                                  # 'out' icinde iki numaranin lambalarinin sondugu anlar
GONE = 2.0                                                  # 'out' icinde vagonun yok oldugu an
OPEN = (0.35, 0.9)                                          # 'open' icinde kapinin acilmaya basladigi ve bittigi an
RING_AT = (0.3, 0.9, 1.5)                                   # 'ring' icinde biletlerin tek tek one geldigi anlar
PUNCH = (0.55, 1.35)                                        # 'punch' icinde zimbanin kapandigi anlar


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
    """kagit hisirtisi: kisa, titrek, tiz gurultu"""
    m = _main(); t = m.tt(d)
    n = m.highpass(m.RNG.standard_normal(len(t)).astype(np.float32), 3200)
    am = np.clip(np.sin(2 * np.pi * 17 * t) * np.sin(2 * np.pi * 5.3 * t + 1.0), 0, 1) ** 0.6
    return (n * am * m.env(d, 0.03, d * 0.4)).astype(np.float32) * 0.5
def punchfx(ok=True):
    """bilet zimbasi: metal 'cik' (+ delerse kisa 'tak'); delemezse bogu bir tik"""
    m = _main(); t = m.tt(0.22)
    x = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 70) + 0.6 * np.sin(2 * np.pi * 3650 * t) * np.exp(-t * 90)
    if ok: x = x + 0.9 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 40) * (t > 0.03)
    else: x = x * 0.5 + 0.5 * m.lowpass(m.RNG.standard_normal(len(t)).astype(np.float32), 500) * np.exp(-t * 30)
    return x.astype(np.float32) * 0.6


# ---- efekt ve muzik plani ----
def mix_plan(T):
    _main().FX.update(whistle=whistle, brake=brake, clack=clack, rustle=rustle, punchfx=punchfx)
    B, S, L, tot = T['beats'], T['scenes'], {l['id']: l for l in T['lines']}, T['total']
    fr = lambda i, f: L[i]['start'] + (L[i]['end'] - L[i]['start']) * f
    fx = []
    steps = lambda a, b, g=0.22, rate=1.8: fx.append(('steps', a, g, dict(d=max(0.3, b - a), rate=rate)))
    rails = lambda a, b, g=0.2, rate=1.6: fx.append(('clack', a, g, dict(d=max(0.6, b - a), rate=rate)))
    jing = lambda t, g=0.3: [fx.append(('chime', t + o, g, dict(freqs=[f_], d=0.5))) for o, f_ in ((0.0, 1975.5), (0.07, 2349.3), (0.15, 1760.0))]

    # 1: kanca (bir numaranin arka kapisi, camda fener)
    fx.append(('buzz', 0.0, 0.5, dict(d=0.22))); fx.append(('rumble', 0.0, 0.3, dict(d=1.4)))
    rails(0.0, S[2], 0.22, 1.9)
    # 2: disaridan
    fx.append(('whoosh', S[2] - 0.15, 0.4, dict(d=0.6, up=True))); rails(S[2], S[3], 0.16, 1.7)
    # 3-4: iki numara: orgu hisirdar, not cikar
    rails(S[3], S[7], 0.09, 1.7)
    fl = B['feel'][0]
    for o in FEEL: fx.append(('rustle', fl + o, 0.6, dict(d=0.32)))
    fd = B['find'][0]
    fx.append(('rustle', fd + FIND - 0.35, 0.6, dict(d=0.6))); fx.append(('chime', fd + FIND, 0.4, dict(freqs=[587.33, 880.0], d=1.6)))
    fx.append(('rustle', fr('m3', 0.05), 0.5, dict(d=0.5))); fx.append(('tick', fr('m3', 0.5), 0.35, dict(f=1500)))          # not acilir; kalem
    fx.append(('chime', B['title'][0] + 0.1, 0.6, dict(freqs=[311.13, 466.16, 622.25])))
    # 5-6: mektup
    fx.append(('rustle', S[5] + 0.05, 0.4, dict(d=0.5)))
    fx.append(('whoosh', fr('d2', 0.12), 0.2, dict(d=0.5, up=False)))                                      # arkaya bakar
    # 7-8: anons
    ch = B['chime'][0]
    rails(S[7], S[10], 0.12, 1.8)
    fx.append(('chime', ch + 0.1, 0.6, dict(freqs=[659.25, 523.25], d=1.4))); fx.append(('chime', ch + 0.55, 0.5, dict(freqs=[523.25, 392.0], d=1.4)))
    fx.append(('hum', L['a1']['start'] - 0.2, 0.22, dict(d=L['a1']['end'] - L['a1']['start'] + 0.5)))
    for o in (0.0, 0.25, 0.5): fx.append(('buzz', fr('a1', 0.62) + o, 0.35, dict(d=0.14)))                 # levha kirmizi yanar
    steps(fr('m4', 0.55), S[9], 0.26, 3.2)
    # 9: koruk
    fx.append(('rumble', S[9], 0.26, dict(d=min(4.0, S[10] - S[9])))); steps(S[9] + 0.1, S[9] + 2.4, 0.24, 2.6)
    for j, f_ in enumerate((0.34, 0.47, 0.60)): fx.append(('chime', fr('d3', f_), 0.26, dict(freqs=[(523.25, 587.33, 698.46)[j]], d=1.0)))
    # 10-12: bir numara; kilit
    rails(S[10], S[13], 0.10, 1.5)
    en = B['enter'][0]
    fx.append(('slide', en + 0.05, 0.4, dict(d=0.5))); steps(en + 0.3, en + 1.4, 0.24, 2.4)
    lk = B['lock'][0]
    for o in LOCKS: fx.append(('snap', lk + o, 0.5, {})); fx.append(('tick', lk + o + 0.05, 0.4, dict(f=700)))
    fx.append(('buzz', fr('m5', 0.8), 0.3, dict(d=0.18)))
    fx.append(('rustle', S[12] + 0.1, 0.35, dict(d=0.4)))
    # 13: Sarnic: tren durur
    st = B['stop'][0]
    fx.append(('brake', st + BRAKE, 0.6, dict(d=1.9))); rails(st, st + 1.6, 0.2, 1.1)
    fx.append(('rumble', st + HALT - 0.2, 0.3, dict(d=1.0))); fx.append(('whoosh', st + HALT, 0.3, dict(d=0.9, up=False)))
    # 14: iki numara soner, sis, bos ray
    ot = B['out'][0]
    fx.append(('hum', S[14], 0.2, dict(d=S[16] - S[14])))
    for j, o in enumerate(OUT_OFF): fx.append(('buzz', ot + o, 0.45, dict(d=0.16))); fx.append(('tick', ot + o + 0.16, 0.4, dict(f=500 - 60 * j)))
    fx.append(('whistle', ot + 1.5, 0.55, dict(d=1.3))); fx.append(('whoosh', ot + 1.7, 0.4, dict(d=1.2, up=False)))
    fx.append(('rumble', ot + GONE - 0.2, 0.3, dict(d=1.0)))
    # 15: fener yaklasir; kapi acilir
    lp = B['lamp'][0]
    steps(lp + 0.5, lp + 2.4, 0.16, 1.5)                                                                   # dışarıdan ayak sesleri
    fx.append(('chime', lp + 0.3, 0.3, dict(freqs=[146.83, 220.0, 293.66], d=2.6)))
    op = B['open'][0]
    fx.append(('tick', op + 0.1, 0.4, dict(f=600))); fx.append(('slide', op + OPEN[0], 0.55, dict(d=OPEN[1] - OPEN[0])))
    fx.append(('snap', op + OPEN[1], 0.6, {})); fx.append(('whoosh', op + OPEN[0], 0.35, dict(d=0.9, up=False)))
    steps(op + 0.95, op + 1.6, 0.26, 1.6)
    # 16-21: Konduktor
    rails(S[16], S[28], 0.07, 1.5)
    jing(L['c1']['start'] - 0.25)
    jb = B['jingle'][0]
    jing(jb + 0.15, 0.4); jing(jb + 0.5, 0.3)
    fx.append(('chime', fr('c4', 0.62), 0.4, dict(freqs=[349.23, 440.0, 523.25], d=2.6)))                  # "Herkes indi"
    # 22: halka: uc zimbali bilet
    rg = B['ring'][0]
    for j, o in enumerate(RING_AT):
        fx.append(('rustle', rg + o - 0.1, 0.3, dict(d=0.25))); fx.append(('punchfx', rg + o + 0.12, 0.5, dict(ok=True)))
        fx.append(('chime', rg + o + 0.14, 0.26, dict(freqs=[(523.25, 587.33, 698.46)[j]], d=1.0)))
    # 23: mektup (sepya)
    fx.append(('whoosh', S[23] - 0.1, 0.3, dict(d=0.6, up=True)))
    # 24-25: Mia'nin bileti: zimba tutmaz
    fx.append(('rustle', fr('m13', 0.2), 0.3, dict(d=0.3)))
    pb = B['punch'][0]
    for o in PUNCH: fx.append(('punchfx', pb + o, 0.6, dict(ok=False))); fx.append(('buzz', pb + o + 0.12, 0.3, dict(d=0.16)))
    fx.append(('buzz', fr('c8', 0.6), 0.3, dict(d=0.2)))
    # 27: son kural
    fx.append(('chime', fr('c9', 0.5), 0.3, dict(freqs=[146.83, 207.65], d=2.4)))
    fx.append(('chime', fr('c10', 0.6), 0.35, dict(freqs=[110.0, 155.56], d=3.0)))
    # 28: disaridan: karanliga
    dk = B['dark'][0]
    fx.append(('whoosh', dk - 0.1, 0.35, dict(d=0.6, up=True))); rails(dk, S[29], 0.2, 1.9); fx.append(('whistle', dk + 0.4, 0.5, dict(d=1.5)))
    # 29-30: mektubun sonu; kalem
    rails(S[29], S[31] + 1.5, 0.07, 1.5)
    fx.append(('rustle', S[29] + 0.1, 0.35, dict(d=0.4)))
    fx.append(('tick', fr('d8', 0.1), 0.35, dict(f=1500))); fx.append(('chime', fr('d8', 0.7), 0.35, dict(freqs=[587.33, 880.0], d=2.0)))
    # 31: kapanis
    fx.append(('chime', B['end'][0] + 0.15, 0.55, dict(freqs=[207.65, 311.13, 415.3, 523.25], d=2.8)))
    for t0 in [L[i]['start'] + o for i, o in ABONE] + [S[31] + ABONE_END]:                                 # abone ol: tik + kisa zil
        fx.append(('tick', t0 + 2.3, 0.5, dict(f=1200))); fx.append(('chime', t0 + 2.45, 0.32, dict(freqs=[1318.5, 1760.0], d=1.0)))
    # muzik: kanca ve bulus gerilim; mektup sicak; anonsla gerilim; "Herkes indi" ile sicak; "inemez" ile gerilim; mektubun sonu sicak; kapanis gizem
    music = [(0.0, S[5], 'gerilim', 0.9), (S[5], S[7], 'sicak', 0.8), (S[7], L['c4']['start'], 'gerilim', 0.9),
             (L['c4']['start'], L['c9']['start'], 'sicak', 0.8), (L['c9']['start'], S[29], 'gerilim', 0.9),
             (S[29], S[31], 'sicak', 0.8), (S[31], tot, 'gizem', 1.0)]
    return dict(pads=[], fx=fx, music=music)
