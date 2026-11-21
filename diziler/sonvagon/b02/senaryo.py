"""Son Vagon, 2. Bolum: Degirmen. Senaryo, ses gruplari, efekt ve muzik plani.

Yapi: KAYIT BICIMINDE. Bolumun tamami Ren'in telefonuyla cektigi video (REC cercevesi, sayac, pil). Anlatici yok; onceki bolumu
Ren kameraya anlatir, soruyu kaydin sonunda Mia sorar.
Kanca (attigi bilet cebinden cikar) -> kayit baslar: Karakopru'de olan, Eli'nin bileti, Ren'in bileti (Degirmen) -> baslik ->
Mia ile Ada (pil yuzde 15) -> anons: birakilacak vagon dort -> koruk, uc numara -> plan: bileti yirt, camdan at -> bilet cebinde ->
en one kosu -> lokomotifin kilitli kapisi -> pencerede degirmen, yokus -> Ada'nin bos koltugu, ip dort numaraya gidiyor ->
dort numara: Ada yumaginin pesinde, lambalar soner -> Ren Ada'yi koruge iter, telefon yere duser, kapi kapanir ->
kapinin ardinda Ren sakinlesir ("burasi tanidik geliyor") -> bos ray -> Mia telefonu alir, soruyu sorar, kayit biter.
Konusanlar: A anons (kondüktorun sesi), M Mia, R Ren, D Ada
"""
import sys
import numpy as np

TITLE = 'SON VAGON'
EP = '2. BÖLÜM'
EP_NAME = 'Değirmen'

SEQ = [
    # ---- 1: kanca (ozcekim: bilet geri geldi) ----
    ('scene', 1),
    ('line', 'h1', 'R', 'Bilet geri geldi!', ['geri', 'geldi!'], 0.3),         # ses: r10 ile ayni kayit (SEG_ALIAS)

    # ---- 2: kayit baslar (ozcekim, dort numara; sonra arka kapinin cami: bos ray) ----
    ('scene', 2),
    ('line', 'r1', 'R', "Biri bunu bulursa bilsin. Karaköprü'de son vagon kayboldu, Eli de içindeydi.", ['kayboldu,'], 0.3),

    # ---- 3: biletler kameraya ----
    ('scene', 3),
    ('line', 'r2', 'R', 'Geriye bir tek bileti kaldı. İniş: Karaköprü.', ['Karaköprü.'], 0.3),
    ('line', 'r3', 'R', 'Benim biletimde Değirmen yazıyor. Sıradaki istasyon da orası.', ['Değirmen'], 0.3),
    ('beat', 'title', 2.8),

    # ---- 4: kamera Mia'da, sonra Ada'da (yakin) ----
    ('scene', 4),
    ('line', 'r4', 'R', 'Bu Mia, bileti boş. Bu da Ada, hâlâ örgü örüyor.', ['Mia,', 'Ada,'], 0.3),
    ('line', 'd1', 'D', 'Çek evladım, çek. Örgü, insanın aklını yerinde tutar.', ['aklını'], 0.3),

    # ---- 5: ikisi birden (genis): pil ----
    ('scene', 5),
    ('line', 'm1', 'M', 'Ren, pilin yüzde on beş. Boşa harcama.', ['yüzde', 'on', 'beş.'], 0.3),
    ('line', 'r5', 'R', 'Boşa değil. Bu video benim sigortam.', ['sigortam.'], 0.2),

    # ---- 6: anons (hoparlor ve levha) ----
    ('scene', 6),
    ('beat', 'chime', 1.2),
    ('line', 'a1', 'A', 'Sıradaki istasyon: Değirmen. Bırakılacak vagon: dört numara.', ['Değirmen.', 'dört', 'numara.'], 0.2),

    # ---- 7: ozcekim: dort numara bizim vagon ----
    ('scene', 7),
    ('line', 'r6', 'R', 'Dört numara. Yani tam şu an içinde durduğum vagon.', ['Dört', 'numara.'], 0.3),

    # ---- 8: kural; one yururler ----
    ('scene', 8),
    ('line', 'd2', 'D', 'Kural belli evladım. Tren durduğunda son vagonda olma.', ['son', 'vagonda', 'olma.'], 0.3),
    ('line', 'm2', 'M', 'Öyleyse üç numaraya geçiyoruz. Hemen!', ['üç', 'numaraya'], 0.0),

    # ---- 9: koruk ----
    ('scene', 9),
    ('beat', 'gang', 2.8),

    # ---- 10: uc numara (ozcekim): plan ----
    ('scene', 10),
    ('line', 'r7', 'R', 'Bir planım var. Bilet yoksa istasyon da yok.', ['Bilet', 'yoksa'], 0.1),
    ('beat', 'tear', 1.5),                                     # bileti ikiye yirtar
    ('line', 'm3', 'M', 'Yırtınca ne değişecek, Ren?', ['ne'], 0.3),
    ('line', 'r8', 'R', 'Yırtmakla kalmıyorum. Camdan da atıyorum.', ['Camdan'], 0.1),

    # ---- 11: pencere ----
    ('scene', 11),
    ('beat', 'throw', 2.6),                                    # parcalar camdan ucar
    ('line', 'r9', 'R', 'Güle güle Değirmen. Tanışamadık.', ['Güle', 'güle'], 0.3),

    # ---- 12: Mia kamerayi (Ren'in cebini) gosterir ----
    ('scene', 12),
    ('line', 'm4', 'M', 'Ren, cebine bak!', ['cebine'], 0.1),

    # ---- 13: ozcekim: bilet cebinde ----
    ('scene', 13),
    ('beat', 'pocket', 1.6),                                   # eli cebine gider; bilet saglam
    ('line', 'r10', 'R', 'Bilet geri geldi!', ['geri', 'geldi!'], 0.3),

    # ---- 14: Ada (yakin) ve saglam bilet ----
    ('scene', 14),
    ('line', 'd3', 'D', 'Kâğıdı yırtarsın evladım. Yazıyı yırtamazsın.', ['Yazıyı'], 0.2),

    # ---- 15: ozcekim: kacis karari ----
    ('scene', 15),
    ('line', 'r11', 'R', 'O zaman kaçarım. En öne, bir numaraya!', ['kaçarım.'], 0.2),

    # ---- 16: one kosu (kapilar: VAGON 2, VAGON 1) ----
    ('scene', 16),
    ('line', 'm5', 'M', 'Ren, dur! Ayrılmayalım!', ['dur!'], 0.0),
    ('beat', 'run', 3.6),

    # ---- 17: lokomotifin kapisi ----
    ('scene', 17),
    ('beat', 'lock', 1.8),                                     # kapi kolu: kilitli
    ('line', 'r12', 'R', 'Lokomotifin kapısı kilitli. Buradan öteye yol yok.', ['kilitli.'], 0.3),

    # ---- 18: bir numara (ozcekim) ----
    ('scene', 18),
    ('line', 'm6', 'M', 'Gerek de yok. Dört numara üç vagon arkamızda.', ['üç', 'vagon'], 0.3),
    ('line', 'r13', 'R', 'Doğru. Değirmen artık bana ulaşamaz.', ['ulaşamaz.'], 0.2),

    # ---- 19: pencerede degirmen, yokus ----
    ('scene', 19),
    ('beat', 'mill', 2.0),
    ('line', 'm7', 'M', 'Tren yokuş çıkıyor. Bak, tepede değirmen!', ['yokuş', 'değirmen!'], 0.3),
    ('line', 'r14', 'R', 'Fena yokuş. Her şey arkaya kayıyor.', ['arkaya'], 0.3),

    # ---- 20: ozcekim: Ada yok ----
    ('scene', 20),
    ('line', 'm8', 'M', 'Ren, Ada nerede? Arkamızdan geliyordu.', ['Ada'], 0.2),

    # ---- 21: uc numara: bos koltuk, ip ----
    ('scene', 21),
    ('beat', 'yarn', 2.6),                                     # kamera ipi izler: arka kapiya, dort numaraya
    ('line', 'r15', 'R', 'Koltuğu boş. Yumağı arkaya yuvarlanmış, ipi dört numaraya gidiyor!', ['dört', 'numaraya'], 0.3),
    ('line', 'm9', 'M', 'Peşinden gitmiş! Tren durmak üzere!', ['durmak', 'üzere!'], 0.1),

    # ---- 22: dort numara: Ada yumagin pesinde ----
    ('scene', 22),
    ('line', 'r16', 'R', 'Ada! Çık oradan, tren duruyor!', ['Çık'], 0.2),
    ('line', 'd4', 'D', 'Yumağım koltuğun altına kaçtı evladım. Yarım iş bırakılmaz.', ['Yarım', 'iş'], 0.2),
    ('line', 'r17', 'R', 'Örgüyü boş ver, yürü!', ['yürü!'], 0.0),
    ('beat', 'stop', 2.2),                                     # fren; arka lambalar sirayla soner

    # ---- 23: koruk (telefon yerde) ----
    ('scene', 23),
    ('beat', 'push', 2.4),                                     # Ren Ada'yi kapidan iter; telefon duser
    ('line', 'd5', 'D', 'Ren! Sen de gel evladım!', ['Sen', 'de', 'gel'], 0.1),
    ('beat', 'door', 1.2),                                     # kapi aralarinda kapanir
    ('line', 'm10', 'M', 'Kapı açılmıyor! Ren, kolu çevir!', ['açılmıyor!'], 0.2),

    # ---- 24: kapinin ardinda Ren ----
    ('scene', 24),
    ('line', 'r18', 'R', 'Mia, sakin ol. Burası tanıdık geliyor.', ['tanıdık'], 0.1),
    ('beat', 'out', 2.2),                                      # son lambalar da soner

    # ---- 25: bos ray ----
    ('scene', 25),
    ('beat', 'fog', 2.8),                                      # sis dagilir: kapinin ardinda vagon yok
    ('line', 'm11', 'M', 'Dört numara yok. Ren de yok.', ['yok.'], 0.4),

    # ---- 26: Ada ile Mia (yakin) ----
    ('scene', 26),
    ('line', 'd6', 'D', 'Beni dışarı itti kızım. Kendi içeride kaldı.', ['içeride'], 0.3),

    # ---- 27: Mia telefonu alir ----
    ('scene', 27),
    ('line', 'm12', 'M', 'Telefonu düşmüş. Hâlâ çekiyor.', ['çekiyor.'], 0.1),
    ('beat', 'pick', 2.0),
    ('line', 'm13', 'M', 'Biletini yırttı, attı, en öne kaçtı. Sence insan biletinden kaçabilir mi?', ['kaçabilir', 'mi?'], 0.4),

    # ---- 28: kapanis ----
    ('scene', 28),
    ('beat', 'end', 6.4),
]

# ---- seslendirme: her grup TEK istek, en fazla 2 ses; grup icinde konusanlar sirayla degisir ----
VOICES = {'A': 'Charon', 'M': 'Leda', 'R': 'Puck', 'D': 'Kore'}
NAMES = {'M': 'Mia', 'R': 'Ren', 'D': 'Ada'}
_DIZI = 'Türkçe bir gerilim çizgi dizisinden replikler seslendir; olay bir gece treninde geçiyor ve Ren her şeyi telefonuyla kaydediyor. '
_M = 'Mia on dokuz yaşında, meraklı ve cesur bir genç kadın: hızlı ve canlı konuşuyor. '
_R = 'Ren rahat, şakacı bir genç adam: korkunca espri yapıyor. '
_SON = 'Her replikten sonra bir saniye dur.'
GROUPS = {
    'an': dict(ids=['a1'],
               style='Eski bir trenin kondüktörü hoparlörden anons yapıyor: erkek, kibar, çok sakin, resmi ve tane tane; akıcı bir Türkçe ile. Çok yavaşlama:'),
    'rd': dict(ids=['r4', 'd1', 'r6', 'd2', 'r10', 'd3', 'r16', 'd4', 'r17', 'd5', 'r18', 'd6'],
               style=_DIZI + _R + 'İlk repliğinde keyifli, kameraya arkadaşlarını tanıtıyor; ikincisinde gergin, korkusunu espriyle gizliyor; '
                     'üçüncüsünde dehşetle, kısa ve yüksek sesle bağırıyor; dördüncüsünde telaşla bağırıyor; beşincisinde sabırsız, bağırıyor; '
                     'son repliğinde çok sakin, şaşkın, alçak sesle ama net, tane tane. '
                     'Ada yaşlı, bilge ve çok sakin bir kadın: yavaş, sıcak ve kendinden emin konuşuyor; dördüncü repliğinde sakin ve inatçı; '
                     'beşincisinde telaşla sesleniyor; son repliğinde üzgün, alçak sesle ama net. ' + _SON),
    'rm1': dict(ids=['m1', 'r5', 'm2', 'r7', 'm3', 'r8', 'm4'],
                style=_DIZI + _M + 'İlk repliğinde gündelik, uyarır gibi; ikincisinde kararlı ve aceleci; üçüncüsünde şüpheyle soruyor; '
                      'son repliğinde şaşkın, yüksek sesle uyarıyor. ' + _R + 'Üç repliğinde de keyifli, şakacı ve kendinden emin. ' + _SON),
    'rm2': dict(ids=['r1', 'm5', 'r2', 'm6', 'r3', 'm7', 'r9', 'm8'],
                style=_DIZI + _R + 'İlk iki repliğinde kameraya ciddi bir kayıt bırakıyor: alçak sesle ama net, tane tane; üçüncüsünde gergin; '
                      'son repliğinde alaycı bir keyifle veda ediyor. ' + _M + 'İlk repliğinde arkasından bağırıyor; ikincisinde sakin, rahatlatıcı; '
                      'üçüncüsünde şaşkın ve heyecanlı; son repliğinde endişeyle soruyor. ' + _SON),
    'rm3': dict(ids=['r11', 'm9', 'r12', 'm10', 'r13', 'm11', 'r14', 'm12', 'r15', 'm13'],
                style=_DIZI + _R + 'İlk repliğinde panikle ama kararlı, bağırıyor; ikincisinde nefes nefese, hayal kırıklığıyla; '
                      'üçüncüsünde rahatlamış, espriyle; dördüncüsünde tedirgin; son repliğinde telaşla, hızlı. ' + _M +
                      'İlk repliğinde telaşla bağırıyor; ikincisinde dehşetle bağırıyor; üçüncüsünde şaşkın, alçak sesle ama net; '
                      'dördüncüsünde yorgun, alçak sesle ama net; son repliğinde kameraya alçak sesle, yavaşça, merak uyandıran bir soru sorar gibi, '
                      'net ve tane tane. ' + _SON),
}

GAP_SCALE = 1.4
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {'h1': 'r10'}                                   # kanca, bolumun icindeki replikle ayni kayit
VOICE_FX = {'A': dict(intercom=True), 'D': dict(rate=0.95)}
TEMPO = {'*': 0.97, 'D': 0.94}

# abone ol bandi: (replik_id, saniye). Bitis sahnesindeki ikinci bant bolum.py icinde.
ABONE = [('d1', 0.0)]
ABONE_END = 1.0                                             # son sahne basladiktan kac sn sonra

# ---- cizim ve sesin ortak kullandigi zamanlar (vurus basina gore saniye) ----
TEAR = 0.55                                                 # 'tear' icinde biletin yirtildigi an
THROW = 0.9                                                 # 'throw' icinde parcalarin elden ciktigi an
POCK = 0.95                                                 # 'pocket' icinde biletin cepten ciktigi an
RUSH = ((0.5, 1.35), (1.9, 2.75))                          # 'run' icinde iki kapidan gecis (bas, son)
LOCKS = (0.45, 0.8, 1.15)                                   # 'lock' icinde kapi kolunun zorlandigi anlar
BRAKE = 0.1                                                 # 'stop' icinde frenin basladigi an
LAMP_OFF = (0.9, 1.35, 1.8)                                 # 'stop' icinde arka lambalarin sondugu anlar
PUSH, FALL = 0.1, 0.5                                       # 'push' icinde itis ve telefonun yere carptigi an
SHUT = 0.8                                                  # 'door' icinde kapinin kapandigi an
OUT_OFF = (0.35, 0.95)                                      # 'out' icinde son lambalarin sondugu anlar
GONE = 1.2                                                  # 'fog' icinde vagonun yok oldugu an (sis en yogunken)
PICK = 0.5                                                  # 'pick' icinde telefonun yerden kalktigi an


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
def beep(f=1320.0, d=0.12):
    """telefonun kayit sesi"""
    m = _main(); t = m.tt(d)
    return (np.sin(2 * np.pi * f * t) * m.env(d, 0.008, 0.03)).astype(np.float32) * 0.35
def rip(d=0.5):
    """kagit yirtilmasi"""
    m = _main(); t = m.tt(d); n = m.highpass(m.RNG.standard_normal(len(t)).astype(np.float32), 1800)
    return (n * (0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 46 * t))) * m.env(d, 0.02, d * 0.4)).astype(np.float32) * 0.5


# ---- efekt ve muzik plani ----
def mix_plan(T):
    _main().FX.update(whistle=whistle, brake=brake, clack=clack, beep=beep, rip=rip)
    B, S, L, tot = T['beats'], T['scenes'], {l['id']: l for l in T['lines']}, T['total']
    fr = lambda i, f: L[i]['start'] + (L[i]['end'] - L[i]['start']) * f
    hk = S[2]                                                   # kancadan kayda kesme ani
    fx = []
    steps = lambda a, b, g=0.22, rate=1.8: fx.append(('steps', a, g, dict(d=max(0.3, b - a), rate=rate)))
    rails = lambda a, b, g=0.2, rate=1.6: fx.append(('clack', a, g, dict(d=max(0.6, b - a), rate=rate)))
    dbl = lambda t, g=0.5, f=1320.0: (fx.append(('beep', t, g, dict(f=f))), fx.append(('beep', t + 0.16, g, dict(f=f * 1.26))))

    # 1: kanca; kayda kesme
    fx.append(('buzz', 0.0, 0.5, dict(d=0.22))); fx.append(('rumble', 0.0, 0.3, dict(d=1.4)))
    rails(0.0, hk, 0.26, 2.2)
    fx.append(('whoosh', hk - 0.15, 0.45, dict(d=0.6, up=True)))
    dbl(hk + 0.05)                                              # kayit basladi
    # 2-6: dort numara
    rails(hk, S[9], 0.10, 1.7)
    fx.append(('tick', L['r2']['start'] + 0.1, 0.4, dict(f=800))); fx.append(('tick', L['r3']['start'] + 0.1, 0.4, dict(f=800)))   # biletler
    fx.append(('chime', B['title'][0] + 0.1, 0.6, dict(freqs=[311.13, 466.16, 622.25])))
    for f_ in (0.2, 0.45, 0.7): fx.append(('tick', fr('d1', f_), 0.2, dict(f=1700)))                      # orgu sisleri
    fx.append(('beep', fr('m1', 0.3), 0.3, dict(f=880.0, d=0.2)))                                         # pil uyarisi
    ch = B['chime'][0]
    fx.append(('chime', ch + 0.1, 0.6, dict(freqs=[659.25, 523.25], d=1.4))); fx.append(('chime', ch + 0.55, 0.5, dict(freqs=[523.25, 392.0], d=1.4)))
    fx.append(('hum', L['a1']['start'] - 0.2, 0.22, dict(d=L['a1']['end'] - L['a1']['start'] + 0.5)))
    for o in (0.0, 0.25, 0.5): fx.append(('buzz', fr('a1', 0.62) + o, 0.35, dict(d=0.14)))                 # levha kirmizi yanar
    steps(fr('m2', 0.5), S[9], 0.2, 2.4)
    # 7: koruk
    gg = B['gang'][0]
    fx.append(('slide', gg, 0.4, dict(d=0.8))); fx.append(('rumble', gg + 0.2, 0.3, dict(d=1.8)))
    rails(gg, S[10], 0.3, 1.5); steps(gg + 0.2, gg + 2.6, 0.22, 2.6)
    # 8-10: uc numara
    rails(S[10], S[15], 0.09, 1.7)
    tr = B['tear'][0]
    fx.append(('rip', tr + TEAR, 0.6, dict(d=0.5)))
    th = B['throw'][0]
    fx.append(('slide', th + 0.05, 0.4, dict(d=0.6)))                                                     # cam acilir
    fx.append(('whoosh', th + 0.5, 0.35, dict(d=1.6, up=False))); rails(th + 0.4, S[12], 0.2, 1.7)         # ruzgar
    fx.append(('whoosh', th + THROW, 0.4, dict(d=0.5, up=True)))
    pk = B['pocket'][0]
    fx.append(('tick', pk + 0.3, 0.3, dict(f=500))); fx.append(('whoosh', pk + POCK - 0.1, 0.3, dict(d=0.4, up=True)))
    fx.append(('buzz', L['r10']['start'], 0.5, dict(d=0.22))); fx.append(('rumble', L['r10']['start'], 0.3, dict(d=1.4)))
    fx.append(('chime', fr('d3', 0.5), 0.35, dict(freqs=[146.83, 220.0], d=2.0)))
    # 11: kosu
    rn = B['run'][0]
    steps(fr('r11', 0.5), rn + 3.4, 0.28, 3.4); rails(S[15], S[17], 0.14, 1.9)
    fx.append(('slide', rn, 0.4, dict(d=0.45)))
    for a_, b_ in RUSH:
        fx.append(('whoosh', rn + a_, 0.5, dict(d=b_ - a_, up=True))); fx.append(('slide', rn + b_, 0.4, dict(d=0.4)))
    # 12: lokomotifin kapisi
    lk = B['lock'][0]
    for o in LOCKS: fx.append(('snap', lk + o, 0.5, {}))
    fx.append(('hum', lk, 0.3, dict(d=S[19] - lk))); rails(S[17], S[19], 0.12, 1.9)
    fx.append(('buzz', lk + LOCKS[-1] + 0.2, 0.35, dict(d=0.2)))
    # 13: degirmen, yokus
    ml = B['mill'][0]
    fx.append(('brake', ml + 0.2, 0.3, dict(d=1.6))); rails(S[19], S[21], 0.14, 1.25)
    fx.append(('chime', ml + 0.5, 0.3, dict(freqs=[207.65, 311.13], d=2.2)))
    fx.append(('slide', fr('r14', 0.25), 0.4, dict(d=1.2)))                                               # bavul kayar
    # 14: ip
    yn = B['yarn'][0]
    fx.append(('whoosh', yn + 0.3, 0.25, dict(d=1.5, up=False))); rails(S[21], S[22], 0.12, 1.2)
    fx.append(('chime', yn + 1.7, 0.35, dict(freqs=[146.83, 220.0], d=2.0)))
    steps(fr('m9', 0.4), S[22] + 0.6, 0.26, 3.2)
    # 15: dort numara
    st = B['stop'][0]
    rails(S[22], st + 1.6, 0.14, 1.0)
    steps(fr('r17', 0.3), st + 1.0, 0.24, 3.0)
    fx.append(('brake', st + BRAKE, 0.6, dict(d=2.0)))
    for j, o in enumerate(LAMP_OFF): fx.append(('buzz', st + o, 0.45, dict(d=0.16))); fx.append(('tick', st + o + 0.16, 0.4, dict(f=500 - 60 * j)))
    # 16: itis, telefon duser, kapi
    ps = B['push'][0]
    steps(ps, ps + 1.3, 0.28, 3.4)
    fx.append(('whoosh', ps + PUSH - 0.1, 0.45, dict(d=0.5, up=False)))
    fx.append(('snap', ps + FALL, 0.7, {})); fx.append(('rumble', ps + FALL, 0.3, dict(d=0.9))); fx.append(('buzz', ps + FALL + 0.05, 0.3, dict(d=0.12)))
    fx.append(('rumble', ps + 1.3, 0.25, dict(d=1.0))); fx.append(('whoosh', ps + 1.4, 0.25, dict(d=1.0, up=False)))   # tren durdu: buhar
    dr = B['door'][0]
    fx.append(('slide', dr + 0.1, 0.5, dict(d=0.7))); fx.append(('snap', dr + SHUT, 0.7, {}))
    for f_ in (0.05, 0.25, 0.45): fx.append(('snap', fr('m10', f_), 0.35, {}))                             # kapi kolu
    fx.append(('hum', dr, 0.3, dict(d=B['fog'][0] - dr)))
    # 17: Ren iceride
    fx.append(('chime', fr('r18', 0.45), 0.35, dict(freqs=[311.13, 466.16], d=2.2)))
    ot = B['out'][0]
    for j, o in enumerate(OUT_OFF): fx.append(('buzz', ot + o, 0.5, dict(d=0.18))); fx.append(('tick', ot + o + 0.18, 0.4, dict(f=380 - 60 * j)))
    fx.append(('snap', ot + OUT_OFF[-1] + 0.25, 0.4, {}))
    # 18: bos ray
    fg = B['fog'][0]
    fx.append(('whistle', fg + 0.1, 0.6, dict(d=1.3))); fx.append(('whoosh', fg + 0.4, 0.4, dict(d=1.6, up=False)))
    fx.append(('rumble', fg + 0.5, 0.3, dict(d=1.6))); rails(fg + 0.8, S[28] + 1.5, 0.14, 1.4)
    fx.append(('buzz', L['m11']['start'], 0.4, dict(d=0.22)))
    fx.append(('chime', L['d6']['start'], 0.3, dict(freqs=[146.83, 220.0], d=2.0)))
    # 19: Mia telefonu alir; kayit durur
    pc = B['pick'][0]
    fx.append(('whoosh', pc + PICK - 0.1, 0.35, dict(d=0.6, up=True))); fx.append(('tick', pc + PICK, 0.4, dict(f=700)))
    dbl(S[28] + 0.02, 0.5, 1660.0)
    # 20: kapanis
    fx.append(('chime', B['end'][0] + 0.15, 0.55, dict(freqs=[207.65, 311.13, 415.3, 523.25], d=2.8)))
    for t0 in [L[i]['start'] + o for i, o in ABONE] + [S[28] + ABONE_END]:                               # abone ol: tik + kisa zil
        fx.append(('tick', t0 + 2.3, 0.5, dict(f=1200))); fx.append(('chime', t0 + 2.45, 0.32, dict(freqs=[1318.5, 1760.0], d=1.0)))
    # muzik: kayit ve anons gerilim; tanisma ve "plan" sicak; "cebine bak" ile gerilime doner; kapanis gizem
    music = [(0.0, S[4], 'gerilim', 0.9), (S[4], ch, 'sicak', 0.8), (ch, S[10], 'gerilim', 0.9), (S[10], L['m4']['start'], 'sicak', 0.8),
             (L['m4']['start'], L['m13']['start'], 'gerilim', 1.0), (L['m13']['start'], tot, 'gizem', 1.0)]
    return dict(pads=[], fx=fx, music=music)
