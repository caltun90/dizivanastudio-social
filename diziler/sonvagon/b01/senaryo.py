"""Son Vagon, 1. Bolum: Bilet. Senaryo, ses gruplari, efekt plani.

Yapi: DUZ ANLATIM. Kanca (bolumun en gerilimli ani: arka kapinin ardinda vagon yok) -> trenin disaridan sayimi (5 vagon, sonra 4)
-> baslik -> son vagonda dort yolcu, biletler (Mia'nin bileti bos) -> anons: "her istasyonda bir vagon birakir" -> one yuruyus,
koruk -> Eli cantasi icin geri doner -> Karakopru: bos peron -> Eli karanlikta, "burasi benim istasyonum" -> vagon yok ->
yerde Eli'nin bileti (Inis: Karakopru) -> siradaki anons: Degirmen (Ren'in bileti) -> soru.
Konusanlar: N anlatici, A anons (kondüktorun sesi), M Mia, R Ren, D Ada, E Eli
"""
import sys
import numpy as np

TITLE = 'SON VAGON'
EP = '1. BÖLÜM'
EP_NAME = 'Bilet'

SEQ = [
    # ---- 1: kanca (arka kapi: vagon yok) + disaridan sayim + baslik ----
    ('scene', 1),
    ('line', 'h1', 'M', 'Son vagon yok!', ['yok!'], 0.3),                     # ses: m7 ile ayni kayit (SEG_ALIAS)
    ('line', 'n1', 'N', 'Gece treni yola beş vagonla çıktı.', ['beş'], 0.3),
    ('line', 'n2', 'N', 'İlk istasyondan sonra dört vagon kaldı. Bir yolcu da eksikti.', ['dört', 'eksikti.'], 0.3),
    ('beat', 'title', 2.5),

    # ---- 2: tren gecede (disaridan) ----
    ('scene', 2),
    ('line', 'n3', 'N', 'Gece Ekspresi saat on birde kalktı. Son vagonda dört yolcu vardı.', ['dört', 'yolcu'], 0.2),

    # ---- 3: son vagon (genis) ----
    ('scene', 3),
    ('beat', 'ride', 1.4),
    ('line', 'r1', 'R', 'Koca vagonda dört kişiyiz. Bu trene kimse binmiyor mu?', ['dört'], 0.3),
    ('line', 'd1', 'D', 'Gece treni böyledir evladım. Yolcusu az olur, yolu uzun.', ['az', 'uzun.'], 0.2),

    # ---- 4: Mia ve Ada (yakin) ----
    ('scene', 4),
    ('line', 'm1', 'M', 'Ben ilk kez tek başıma yolculuk yapıyorum.', ['ilk', 'kez'], 0.3),
    ('line', 'd2', 'D', 'Nereye gidiyorsun kızım?', ['Nereye'], 0.3),
    ('line', 'm2', 'M', 'Bilmiyorum. Gişede ilk kalkan trene bilet istedim.', ['Bilmiyorum.'], 0.2),

    # ---- 5: biletler ----
    ('scene', 5),
    ('beat', 'ticket', 1.4),                                   # Mia biletini cikarir: INIS satiri bos
    ('line', 'm3', 'M', 'Tuhaf. Biletimde ineceğim istasyon yazmıyor.', ['yazmıyor.'], 0.3),
    ('line', 'r2', 'R', 'Benimkinde yazıyor: Değirmen. Seninki baskı hatasıdır.', ['Değirmen.'], 0.3),
    ('line', 'e1', 'E', 'Benimki Karaköprü. Tam on iki dakika sonra iniyorum.', ['Karaköprü.'], 0.2),

    # ---- 6: anons (hoparlor) ----
    ('scene', 6),
    ('beat', 'chime', 1.2),
    ('line', 'a1', 'A', 'Sayın yolcular. Bu tren, her istasyonda bir vagon bırakır.', ['bir', 'vagon', 'bırakır.'], 0.3),
    ('line', 'a2', 'A', 'Sıradaki istasyon: Karaköprü. Bırakılacak vagon: beş numara.', ['beş', 'numara.'], 0.1),

    # ---- 7: levha: VAGON 5 ----
    ('scene', 7),
    ('beat', 'plate', 1.8),                                    # herkes kapinin ustundeki levhaya bakar
    ('line', 'r3', 'R', 'Bir saniye. Beş numara bizim vagon değil mi?', ['bizim'], 0.3),
    ('line', 'e2', 'E', 'Vagon bırakmak da ne demek? Tarifede böyle bir şey yok!', ['Tarifede'], 0.3),
    ('line', 'd3', 'D', 'Anons açık evladım. Bu vagon kalıyor. Biz öne geçelim.', ['öne'], 0.2),

    # ---- 8: one yuruyus ----
    ('scene', 8),
    ('line', 'm4', 'M', 'Tren yavaşlıyor! Çabuk, öndeki vagona!', ['Çabuk,'], 0.0),
    ('beat', 'walk', 3.6),

    # ---- 9: koruk ----
    ('scene', 9),
    ('beat', 'gang', 2.4),                                     # sarsilan korukten gecerler; Eli durur
    ('line', 'e3', 'E', 'Durun! Çantam koltukta kaldı. Bütün hesaplarım onun içinde.', ['Çantam'], 0.3),
    ('line', 'm5', 'M', 'Bırak çantayı Eli! Tren durmak üzere.', ['Bırak'], 0.3),
    ('line', 'e4', 'E', 'Otuz saniye sürer. Hesapladım.', ['Otuz', 'saniye'], 0.0),
    ('beat', 'back', 1.7),                                     # Eli geri doner; kapi arkasindan kapanir

    # ---- 10: Karakopru (peron) ----
    ('scene', 10),
    ('beat', 'stop', 2.8),                                     # fren; tren durur
    ('line', 'n4', 'N', 'Tren Karaköprü\'de durdu. Peron boştu, kapılar açılmadı.', ['boştu,'], 0.2),

    # ---- 11: dort numarali vagon (pencere) ----
    ('scene', 11),
    ('line', 'd4', 'D', 'Ne inen var ne binen. Bu istasyon kimi bekliyor?', ['kimi'], 0.3),
    ('line', 'r4', 'R', 'Eli nerede kaldı? Otuz saniye çoktan doldu.', ['Eli'], 0.1),

    # ---- 12: son vagon: Eli tek basina ----
    ('scene', 12),
    ('beat', 'dark', 2.2),                                     # lambalar arkadan one dogru soner
    ('line', 'e5', 'E', 'Çantayı buldum, geliyorum! Işıklar neden sönüyor?', ['Işıklar'], 0.0),
    ('beat', 'sign', 1.5),                                     # pencerede tabela
    ('line', 'e6', 'E', 'Karaköprü. Burası benim istasyonum.', ['benim'], 0.0),
    ('beat', 'out', 1.5),                                      # son lamba da soner

    # ---- 13: arka kapi ----
    ('scene', 13),
    ('beat', 'whistle', 1.5),                                  # duduk; tren kalkar, Mia kapiya kosar
    ('line', 'm6', 'M', 'Kapı açılmıyor! Eli, beni duyuyor musun?', ['açılmıyor!'], 0.0),
    ('beat', 'fog', 2.0),                                      # camdaki sis dagilir: ray bos
    ('line', 'm7', 'M', 'Son vagon yok!', ['yok!'], 0.3),
    ('line', 'r5', 'R', 'Arkamızda yalnızca ray var. Vagon kopmamış, yok olmuş.', ['yok', 'olmuş.'], 0.3),
    ('line', 'd6', 'D', 'Eli o vagondaydı evladım.', ['Eli'], 0.2),

    # ---- 14: disaridan: dort vagon ----
    ('scene', 14),
    ('line', 'n5', 'N', 'Beş numaralı vagon artık yoktu. İçindeki yolcu da.', ['yoktu.'], 0.2),

    # ---- 15: yerdeki bilet ----
    ('scene', 15),
    ('beat', 'find', 2.0),                                     # Ren egilir, yerden bileti alir
    ('line', 'r6', 'R', 'Yerde bir bilet var. Eli düşürmüş.', ['bilet'], 0.3),
    ('line', 'm8', 'M', 'İniş: Karaköprü. Eli tam biletinde yazan istasyonda kayboldu.', ['biletinde', 'yazan'], 0.3),
    ('line', 'r7', 'R', 'Harika. Benim biletimde de Değirmen yazıyor.', ['Değirmen'], 0.1),

    # ---- 16: anons ----
    ('scene', 16),
    ('beat', 'chime2', 1.0),
    ('line', 'a3', 'A', 'Sıradaki istasyon: Değirmen. Bırakılacak vagon: dört numara.', ['Değirmen.', 'dört'], 0.1),

    # ---- 17: levha: VAGON 4 ----
    ('scene', 17),
    ('beat', 'plate4', 1.4),
    ('line', 'd5', 'D', 'Kalk evladım. Öne yürüyoruz.', ['Öne'], 0.3),

    # ---- 18: tren geceye karisir ----
    ('scene', 18),
    ('line', 'n6', 'N', 'O gece yolcular tek bir kural öğrendi: tren durduğunda son vagonda olma.', ['son', 'vagonda', 'olma.'], 0.4),

    # ---- 19: kapanis ----
    ('scene', 19),
    ('beat', 'endin', 0.5),
    ('line', 'n7', 'N', 'Peki Mia\'nın biletinde neden hiçbir istasyon yazmıyordu?', ['neden'], 0.3),
    ('beat', 'end', 4.2),
]

# ---- seslendirme: her grup TEK istek, en fazla 2 ses; grup icinde konusanlar sirayla degisir ----
VOICES = {'N': 'Achird', 'A': 'Charon', 'M': 'Leda', 'R': 'Puck', 'D': 'Kore', 'E': 'Fenrir'}
NAMES = {'M': 'Mia', 'R': 'Ren', 'D': 'Ada', 'E': 'Eli'}
_DIZI = 'Türkçe bir gerilim çizgi dizisinden replikler seslendir; olay bir gece treninde geçiyor. '
_M = 'Mia on dokuz yaşında, meraklı ve cesur bir genç kadın: hızlı ve canlı konuşuyor. '
_R = 'Ren rahat, şakacı bir genç adam: korkunca espri yapıyor. '
GROUPS = {
    'na': dict(ids=['n1', 'n2', 'n3', 'n4', 'n5', 'n6'],
               style='Gerilim dizisi anlatıcısı gibi, alçak, sakin ve tekinsiz bir tonla, akıcı bir Türkçe ile oku. Çok yavaşlama. '
                     'Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:'),
    'nb': dict(ids=['n7'],
               style='Gerilim dizisi anlatıcısı gibi, alçak, sakin ve tekinsiz bir tonla, merak uyandıran bir soru sorar gibi, akıcı bir Türkçe ile oku. Çok yavaşlama:'),
    'an': dict(ids=['a1', 'a2', 'a3'],
               style='Eski bir trenin kondüktörü hoparlörden anons yapıyor: erkek, kibar, çok sakin, resmi ve tane tane; akıcı bir Türkçe ile. '
                     'Çok yavaşlama. Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:'),
    'mr1': dict(ids=['m1', 'r1', 'm2', 'r2', 'm3', 'r3', 'm4', 'r4'],
                style=_DIZI + _M + 'İlk üç repliğinde gündelik ve meraklı; dördüncü repliğinde telaşla bağırıyor. ' + _R +
                      'İlk iki repliğinde keyifli ve şakacı; üçüncüsünde şaşkın; dördüncüsünde endişeli. '
                      'Her replikten sonra bir saniye dur.'),
    'mr2': dict(ids=['m5', 'r5', 'm6', 'r6', 'm7', 'r7', 'm8'],
                style=_DIZI + _M + 'İlk iki repliğinde telaşla bağırıyor; üçüncü repliğinde dehşetle, kısa ve yüksek sesle bağırıyor; '
                      'son repliğinde alçak sesle ama net, tane tane, bir şeyi yeni anlamış gibi. ' + _R +
                      'İlk repliğinde korkmuş, inanamıyor; ikincisinde alçak sesle ama net; üçüncüsünde korkusunu espriyle gizliyor. '
                      'Her replikten sonra bir saniye dur.'),
    'de': dict(ids=['e1', 'd1', 'e2', 'd2', 'e3', 'd3', 'e4', 'd4', 'e5', 'd5', 'e6', 'd6'],
               style=_DIZI + 'Eli titiz, hesapçı ve tedirgin bir adam: hızlı konuşuyor. İlk repliğinde kendinden emin; ikincisinde öfkeli; '
                     'üçüncüsünde telaşla bağırıyor; dördüncüsünde inatçı; beşincisinde önce sevinçli sonra korkmuş; '
                     'son repliğinde çok sakin, şaşkın, neredeyse fısıltıyla ama net, tane tane. '
                     'Ada yaşlı, bilge ve çok sakin bir kadın: yavaş, sıcak ve kendinden emin konuşuyor; son repliğinde üzgün. '
                     'Her replikten sonra bir saniye dur.'),
}

GAP_SCALE = 1.0
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {'h1': 'm7'}                                    # kanca, bolumun icindeki replikle ayni kayit
VOICE_FX = {'A': dict(intercom=True), 'D': dict(rate=0.95)}
TEMPO = {'*': 1.0}

# abone ol bandi: (replik_id, saniye). Bitis sahnesindeki ikinci bant bolum.py icinde.
ABONE = [('d1', 0.0)]
ABONE_END = 1.0                                             # son sahne basladiktan kac sn sonra

# ---- cizim ve sesin ortak kullandigi zamanlar (vurus basina gore saniye) ----
HOOK_CUT = 0.25                                             # kanca repligi bittikten kac sn sonra disari plana kesilir
BRAKE = 0.2                                                 # 'stop' icinde frenin basladigi an
LAMP_OFF = (0.2, 0.75, 1.3)                                 # 'dark' icinde arka lambalarin sondugu anlar
WHISTLE = 0.15                                              # 'whistle' icinde dudugun caldigi an
PICK = 1.1                                                  # 'find' icinde Ren'in bileti yerden aldigi an


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


# ---- efekt ve fon plani ----
DM = [73.42, 110.0, 146.83, 174.61]
AM = [110.0, 164.81, 220.0, 261.63]
CM = [130.81, 196.0, 261.63, 311.13]
LOW = [69.30, 103.83, 138.59, 164.81]
LOW2 = [61.74, 92.50, 123.47, 146.83]
FM = [87.31, 130.81, 174.61, 207.65]


def mix_plan(T):
    _main().FX.update(whistle=whistle, brake=brake, clack=clack)
    B, S, L, tot = T['beats'], T['scenes'], {l['id']: l for l in T['lines']}, T['total']
    fr = lambda i, f: L[i]['start'] + (L[i]['end'] - L[i]['start']) * f
    hk = L['h1']['end'] + HOOK_CUT
    pads = [(0.0, B['title'][0], LOW, 1.0), (B['title'][0], S[3], DM, 0.9), (S[3], S[5], CM, 0.5), (S[5], S[6], AM, 0.6), (S[6], S[8], LOW2, 0.85),
            (S[8], S[10], DM, 0.95), (S[10], S[12], LOW, 0.8), (S[12], S[13], LOW2, 1.0), (S[13], S[14], DM, 1.0), (S[14], S[15], LOW, 0.9),
            (S[15], S[16], AM, 0.7), (S[16], S[18], LOW2, 0.9), (S[18], S[19], DM, 0.9), (S[19], tot, FM, 0.9)]
    fx = []
    steps = lambda a, b, g=0.22, rate=1.8: fx.append(('steps', a, g, dict(d=max(0.3, b - a), rate=rate)))
    rails = lambda a, b, g=0.2, rate=1.6: fx.append(('clack', a, g, dict(d=max(0.6, b - a), rate=rate)))
    voice = lambda i, g=0.22: fx.append(('hum', L[i]['start'] - 0.2, g, dict(d=L[i]['end'] - L[i]['start'] + 0.5)))

    # 1: kanca + sayim + baslik
    fx.append(('buzz', 0.0, 0.5, dict(d=0.22))); fx.append(('rumble', 0.0, 0.3, dict(d=1.4)))
    rails(0.0, hk, 0.3, 2.4)
    fx.append(('whoosh', hk - 0.15, 0.45, dict(d=0.7, up=True)))
    rails(hk, B['title'][0], 0.16, 1.8)
    for j in range(5): fx.append(('tick', fr('n1', 0.30 + 0.12 * j), 0.35, dict(f=900 + 60 * j)))      # vagonlar sayilir
    fx.append(('whoosh', fr('n2', 0.30), 0.4, dict(d=0.9, up=False)))                                 # son vagon sise karisir
    fx.append(('buzz', fr('n2', 0.48), 0.35, dict(d=0.25)))
    fx.append(('chime', B['title'][0] + 0.1, 0.6, dict(freqs=[311.13, 466.16, 622.25])))
    # 2-4: tren gecede, vagon
    fx.append(('whistle', S[2] + 0.2, 0.5, dict(d=1.5)))
    rails(S[2], S[5], 0.14, 1.7)
    fx.append(('tick', fr('d1', 0.2), 0.2, dict(f=1700))); fx.append(('tick', fr('d1', 0.6), 0.2, dict(f=1700)))   # orgu sisleri
    # 5: biletler
    tk = B['ticket'][0]
    fx.append(('whoosh', tk + 0.2, 0.3, dict(d=0.5, up=True))); fx.append(('tick', tk + 0.7, 0.4, dict(f=700)))
    fx.append(('buzz', fr('m3', 0.55), 0.3, dict(d=0.18)))                                           # bos satir yanip soner
    fx.append(('tick', L['r2']['start'], 0.4, dict(f=800))); fx.append(('tick', L['e1']['start'], 0.4, dict(f=800)))
    rails(S[5], S[6], 0.08, 1.7)
    # 6: anons
    ch = B['chime'][0]
    fx.append(('chime', ch + 0.1, 0.6, dict(freqs=[659.25, 523.25], d=1.4))); fx.append(('chime', ch + 0.55, 0.5, dict(freqs=[523.25, 392.0], d=1.4)))
    for i in ('a1', 'a2', 'a3'): voice(i)
    rails(S[6], S[8], 0.07, 1.7)
    # 7: levha
    pl = B['plate'][0]
    fx.append(('whoosh', pl + 0.1, 0.3, dict(d=0.6, up=True)))
    for o in (0.6, 0.85, 1.1): fx.append(('buzz', pl + o, 0.35, dict(d=0.14)))
    fx.append(('snap', L['e2']['start'] + 0.05, 0.3, {}))
    # 8: yuruyus, tren yavaslar
    fx.append(('brake', L['m4']['start'] - 0.3, 0.35, dict(d=1.4)))
    wk = B['walk'][0]
    steps(L['m4']['end'] - 0.3, wk + 3.6, 0.26, 2.6)
    rails(S[8], S[9], 0.16, 1.4)
    # 9: koruk
    gg = B['gang'][0]
    fx.append(('slide', gg, 0.4, dict(d=0.8)))
    fx.append(('rumble', gg + 0.2, 0.3, dict(d=1.8))); rails(gg, S[10], 0.3, 1.25)
    steps(gg + 0.3, gg + 2.3, 0.22, 2.6)
    fx.append(('snap', L['e3']['start'], 0.4, {}))
    bk = B['back'][0]
    steps(bk + 0.1, bk + 1.2, 0.24, 2.6)
    fx.append(('slide', bk + 1.0, 0.5, dict(d=0.6))); fx.append(('snap', bk + 1.55, 0.6, {}))          # kapi kapanir
    # 10: Karakopru
    st = B['stop'][0]
    fx.append(('brake', st + BRAKE, 0.6, dict(d=2.1)))
    rails(st, st + 2.0, 0.2, 1.0)
    fx.append(('rumble', st + 2.1, 0.3, dict(d=1.0))); fx.append(('whoosh', st + 2.2, 0.3, dict(d=1.0, up=False)))   # buhar
    fx.append(('hum', L['n4']['start'], 0.25, dict(d=S[12] - L['n4']['start'])))
    fx.append(('chime', fr('n4', 0.5), 0.25, dict(freqs=[207.65, 311.13], d=2.0)))
    # 12: Eli karanlikta
    dk = B['dark'][0]
    for j, o in enumerate(LAMP_OFF): fx.append(('buzz', dk + o, 0.45, dict(d=0.16))); fx.append(('tick', dk + o + 0.16, 0.4, dict(f=500 - 60 * j)))
    fx.append(('hum', dk, 0.4, dict(d=S[13] - dk)))
    steps(L['e5']['start'], fr('e5', 0.4), 0.2, 2.4)
    sg = B['sign'][0]
    fx.append(('chime', sg + 0.4, 0.4, dict(freqs=[311.13, 466.16], d=2.2)))
    ot = B['out'][0]
    fx.append(('buzz', ot + 0.3, 0.5, dict(d=0.2))); fx.append(('snap', ot + 0.5, 0.5, {}))
    # 13: arka kapi
    wh = B['whistle'][0]
    fx.append(('whistle', wh + WHISTLE, 0.7, dict(d=1.3)))
    fx.append(('rumble', wh + 0.5, 0.3, dict(d=1.6)))
    rails(wh + 0.7, S[14], 0.18, 1.3)
    steps(wh + 0.4, wh + 1.4, 0.26, 3.2)
    for f_ in (0.05, 0.22, 0.4): fx.append(('snap', fr('m6', f_), 0.35, {}))                           # kapi kolu
    fg = B['fog'][0]
    fx.append(('whoosh', fg + 0.3, 0.4, dict(d=1.5, up=False)))
    fx.append(('buzz', L['m7']['start'], 0.5, dict(d=0.22))); fx.append(('rumble', L['m7']['start'], 0.3, dict(d=1.4)))
    fx.append(('chime', L['d6']['start'], 0.3, dict(freqs=[146.83, 220.0], d=2.0)))
    # 14: dort vagon
    rails(S[14], S[15], 0.16, 1.8)
    fx.append(('whistle', S[14] + 0.3, 0.3, dict(d=1.2)))
    for j in range(4): fx.append(('tick', fr('n5', 0.1 + 0.1 * j), 0.3, dict(f=900 + 60 * j)))
    fx.append(('buzz', fr('n5', 0.52), 0.4, dict(d=0.25)))
    # 15: bilet
    fd = B['find'][0]
    fx.append(('tick', fd + PICK, 0.4, dict(f=700))); fx.append(('whoosh', fd + PICK + 0.1, 0.25, dict(d=0.5, up=True)))
    fx.append(('chime', fr('m8', 0.12), 0.4, dict(freqs=[311.13, 466.16, 622.25], d=2.2)))
    rails(S[15], S[18], 0.07, 1.7)
    # 16-17: anons, levha
    c2 = B['chime2'][0]
    fx.append(('chime', c2 + 0.05, 0.6, dict(freqs=[659.25, 523.25], d=1.4))); fx.append(('chime', c2 + 0.5, 0.5, dict(freqs=[523.25, 392.0], d=1.4)))
    p4 = B['plate4'][0]
    for o in (0.3, 0.55, 0.8): fx.append(('buzz', p4 + o, 0.35, dict(d=0.14)))
    steps(fr('d5', 0.5), S[18], 0.22, 2.4)
    # 18: tren geceye karisir
    rails(S[18], S[19] + 1.5, 0.2, 1.8)
    fx.append(('whistle', fr('n6', 0.6), 0.4, dict(d=1.6)))
    # 19: kapanis
    fx.append(('chime', B['end'][0], 0.55, dict(freqs=[207.65, 311.13, 415.3, 523.25], d=2.8)))
    for t0 in [L[i]['start'] + o for i, o in ABONE] + [S[19] + ABONE_END]:                           # abone ol: tik + kisa zil
        fx.append(('tick', t0 + 2.3, 0.5, dict(f=1200))); fx.append(('chime', t0 + 2.45, 0.32, dict(freqs=[1318.5, 1760.0], d=1.0)))
    return dict(pads=pads, fx=fx)
