"""Son Vagon, 3. Bolum: Yedigol. Senaryo, ses gruplari, efekt ve muzik plani.

Yapi: TERSTEN ANLATIM. Bolum sondan baslar ve geriye dogru acilir; her geri sarista ekranda saat ve "N DAKIKA ONCE" etiketi cikar.
SIMDI 00:00 (kanca: Mia iki numarada tek basina, elinde Ada'nin yarim orgusu) -> onceki bolum (disaridan: iki vagon) -> baslik ->
geri sarma -> 2 DK ONCE 23:58 (Yedigol peronu; Ada orguyu Mia'ya verir; kapi kapanir; camin ardinda bir sey soyler, DUYULMAZ;
lambalar soner, bos ray) -> 5 DK ONCE 23:55 (Mia yalvarir; Ada katlanir koltukta; biletler; pencerede yedi gol) ->
10 DK ONCE 23:50 (orgude istasyon adlari; ip Yedigol'e kadar yetiyor) -> 15 DK ONCE 23:45 (anons: uc numara; Ada oturur) ->
GECENIN BASI 23:05 (bes numara, ilk anons: herkes korkar, Ada gulumser) -> 23:58 kapinin ardi, bu kez SESLI:
"Birakir dedi kizim. Kaybolur demedi." -> SIMDI -> soru.
Konusanlar: N anlatici, A anons (kondüktorun sesi), M Mia, D Ada. Ren ve Eli yalnizca gecenin basinda gorunur (sessiz).
"""
import sys
import numpy as np

TITLE = 'SON VAGON'
EP = '3. BÖLÜM'
EP_NAME = 'Yedigöl'

SEQ = [
    # ---- 1: kanca (SIMDI: iki numara, Mia tek basina, elinde yarim orgu) ----
    ('scene', 1),
    ('line', 'm1', 'M', 'Ada bilerek kaldı!', ['bilerek'], 0.3),

    # ---- 2: disaridan: iki vagon; uc numaranin yeri bos ----
    ('scene', 2),
    ('line', 'n1', 'N', 'Önceki bölümde Ren kayboldu. Şimdi üç numara da yok, Ada da.', ['Ren', 'üç', 'numara'], 0.3),

    # ---- 3: SIMDI: iki numara (genis, sonra orgu) ; baslik ----
    ('scene', 3),
    ('line', 'm2', 'M', 'Trende iki vagon kaldı. Bir de ben.', ['iki', 'vagon'], 0.3),
    ('line', 'm3', 'M', 'Yarım örgüsünü bana verdi. Kendi son vagonda kaldı.', ['Yarım', 'örgüsünü'], 0.2),
    ('beat', 'title', 2.6),

    # ---- 4: geri sarma (tren geri geri gider, uc numara sisten geri gelir) ----
    ('scene', 4),
    ('line', 'n2', 'N', 'Buraya nasıl gelindi? Geriye saralım.', ['Geriye'], 0.0),
    ('beat', 'rw1', 1.3),

    # ---- 5: 2 DK ONCE 23:58: Yedigol peronu, tren durur ----
    ('scene', 5),
    ('beat', 'stop', 2.8),

    # ---- 6: uc numaranin on kapisi (genis) ----
    ('scene', 6),
    ('line', 'm4', 'M', 'Tren durdu Ada! Son şansın, yürü!', ['durdu'], 0.3),
    ('line', 'd1', 'D', 'Bunu al kızım. Yarım iş bırakılmaz.', ['Yarım', 'iş'], 0.3),

    # ---- 7: ikisi (yakin); kapi aralarinda kapanir ----
    ('scene', 7),
    ('line', 'm5', 'M', 'Almam! Kendin bitireceksin, benimle gel!', ['Almam!'], 0.3),
    ('line', 'd2', 'D', 'Korkma kızım. Bak, ben korkmuyorum.', ['korkmuyorum.'], 0.1),
    ('beat', 'shut', 1.8),

    # ---- 8: iki numaradan arka kapiya bakis: Mia kapida, Ada camin ardinda ----
    ('scene', 8),
    ('line', 'm6', 'M', 'Ada! Kapıyı aç, ne olur!', ['aç,'], 0.0),
    ('beat', 'say', 2.2),                                      # Ada camin ardinda bir sey soyler: ses yok

    # ---- 9: cam (yakin): lambalar soner, sis, bos ray ----
    ('scene', 9),
    ('line', 'm7', 'M', 'Duyamıyorum! Ne dedin?', ['Ne', 'dedin?'], 0.0),
    ('beat', 'out', 3.3),

    # ---- 10: 5 DK ONCE 23:55: Ada katlanir koltukta, Mia yalvarir ----
    ('scene', 10),
    ('beat', 'rw2', 1.0),
    ('line', 'm8', 'M', 'Kalk Ada, lütfen! Hemen iki numaraya geçelim.', ['Kalk'], 0.3),
    ('line', 'd3', 'D', 'Sen geç kızım. Ben yerimi buldum.', ['yerimi'], 0.3),

    # ---- 11: biletler ----
    ('scene', 11),
    ('line', 'm9', 'M', 'Burası son vagon! Tren durunca yok olacak.', ['yok', 'olacak.'], 0.3),
    ('line', 'd4', 'D', 'Benim biletimde Yedigöl yazıyor. Seninki boş.', ['Yedigöl', 'boş.'], 0.3),

    # ---- 12: Mia (yakin), sonra Ada (yakin) ----
    ('scene', 12),
    ('line', 'm10', 'M', 'Bilet umurumda değil! Seni bırakmam.', ['bırakmam.'], 0.3),
    ('line', 'd5', 'D', 'Bırakacaksın kızım. Herkesin durağı ayrı.', ['durağı', 'ayrı.'], 0.1),

    # ---- 13: pencerede yedi gol ----
    ('scene', 13),
    ('beat', 'lakes', 2.8),
    ('line', 'd6', 'D', 'Bak, yedi göl. Yedisinde de ay var.', ['yedi', 'göl.'], 0.3),

    # ---- 14: genis: istasyonun lambalari yaklasir ----
    ('scene', 14),
    ('line', 'm11', 'M', 'Peronda kimse yok Ada. Lambalar boşuna yanıyor.', ['kimse', 'yok'], 0.3),
    ('line', 'd7', 'D', 'Boşuna yanan lamba olmaz kızım.', ['olmaz'], 0.2),

    # ---- 15: 10 DK ONCE 23:50: Mia orgudeki yaziyi fark eder ----
    ('scene', 15),
    ('beat', 'rw3', 1.0),
    ('line', 'm12', 'M', 'Dur. Örgünde yazı mı var?', ['yazı'], 0.3),
    ('line', 'd8', 'D', 'Var kızım. Yaklaş da oku.', ['oku.'], 0.0),

    # ---- 16: orgu (cok yakin): istasyon adlari ----
    ('scene', 16),
    ('beat', 'knit', 2.6),
    ('line', 'm13', 'M', 'Karaköprü. Değirmen. Yedigöl. Bütün gece bunu mu ördün?', ['Karaköprü.', 'Değirmen.', 'Yedigöl.'], 0.3),

    # ---- 17: Ada (yakin) ----
    ('scene', 17),
    ('line', 'd9', 'D', 'Her istasyona bir sıra kızım. Unutulmasınlar diye.', ['bir', 'sıra'], 0.3),

    # ---- 18: orgunun ustu bos; yumak bitmek uzere ----
    ('scene', 18),
    ('line', 'm14', 'M', 'Sarnıç yok. Son Durak yok. Neden?', ['Neden?'], 0.3),
    ('line', 'd10', 'D', "İpim Yedigöl'e kadar yetiyor.", ["Yedigöl'e"], 0.3),

    # ---- 19: 15 DK ONCE 23:45: anons (hoparlor ve levha) ----
    ('scene', 19),
    ('beat', 'rw4', 1.0),
    ('beat', 'chime', 1.2),
    ('line', 'a1', 'A', 'Sıradaki istasyon: Yedigöl. Bırakılacak vagon: üç numara.', ['Yedigöl.', 'üç', 'numara.'], 0.2),

    # ---- 20: uc numara (genis): Ada biletine bakar, sonra oturur ----
    ('scene', 20),
    ('line', 'd11', 'D', 'Yedigöl. Demek sıra bende.', ['sıra', 'bende.'], 0.3),
    ('line', 'm15', 'M', 'Üç numara, bizim vagon! Yürü Ada, öne!', ['Üç', 'numara,'], 0.3),
    ('line', 'd12', 'D', 'Acelem yok kızım. Şu sırayı bitireyim.', ['Acelem', 'yok'], 0.0),
    ('beat', 'sit', 1.6),                                      # katlanir koltugu indirir, oturur

    # ---- 21: ikisi (yakin) ----
    ('scene', 21),
    ('line', 'm16', 'M', 'Senin biletin Yedigöl! Hiç korkmuyor musun?', ['korkmuyor'], 0.3),
    ('line', 'd13', 'D', 'Korku, yolcuyu yorar kızım. Yolu kısaltmaz.', ['Korku,', 'kısaltmaz.'], 0.3),
    ('line', 'm18', 'M', 'Ren de korkmuyordu. Şimdi yok!', ['yok!'], 0.3),
    ('line', 'd15', 'D', 'Yok demek kolay kızım. Bilmiyoruz demek zor.', ['Bilmiyoruz'], 0.3),

    # ---- 22: GECENIN BASI 23:05: bes numara, ilk anons ----
    ('scene', 22),
    ('beat', 'rw5', 1.4),
    ('line', 'a2', 'A', 'Sayın yolcular. Bu tren, her istasyonda bir vagon bırakır.', ['bir', 'vagon', 'bırakır.'], 0.1),

    # ---- 23: herkes korkar; Ada gulumser ----
    ('scene', 23),
    ('beat', 'smile', 2.2),
    ('line', 'n3', 'N', 'O gece herkes korktu. Ada gülümsedi.', ['gülümsedi.'], 0.2),

    # ---- 24: 23:58 kapinin ardi: bu kez sesli ----
    ('scene', 24),
    ('beat', 'ff', 1.2),
    ('line', 'd14', 'D', 'Bırakır dedi kızım. Kaybolur demedi.', ['Bırakır', 'Kaybolur'], 0.1),
    ('beat', 'gone', 1.8),

    # ---- 25: SIMDI: Mia ve orgu ----
    ('scene', 25),
    ('line', 'm17', 'M', 'Ne dediğini duyamadım. Ama hiç korkmuyordu.', ['korkmuyordu.'], 0.4),

    # ---- 26: kapanis ----
    ('scene', 26),
    ('line', 'n4', 'N', 'Ada neden kalmayı seçti?', ['neden'], 0.3),
    ('beat', 'end', 6.6),
]

# ---- seslendirme: her grup TEK istek, en fazla 2 ses; grup icinde konusanlar sirayla degisir ----
VOICES = {'N': 'Achird', 'A': 'Charon', 'M': 'Leda', 'D': 'Kore'}
NAMES = {'M': 'Mia', 'D': 'Ada'}
_DIZI = 'Türkçe bir gerilim çizgi dizisinden replikler seslendir; olay bir gece treninde geçiyor. '
_M = 'Mia on dokuz yaşında, meraklı ve cesur bir genç kadın: hızlı ve canlı konuşuyor. '
_D = 'Ada yaşlı, bilge ve çok sakin bir kadın: yavaş, sıcak ve kendinden emin konuşuyor, hiç telaşlanmıyor. '
_SON = 'Her replikten sonra bir saniye dur.'
GROUPS = {
    'an': dict(ids=['a1', 'a2'],
               style='Eski bir trenin kondüktörü hoparlörden anons yapıyor: erkek, kibar, çok sakin, resmi ve tane tane; akıcı bir Türkçe ile. '
                     'Çok yavaşlama. Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:'),
    'na': dict(ids=['n1', 'n2', 'n3', 'n4'],
               style='Gerilim dizisi anlatıcısı gibi, alçak, sakin ve tekinsiz bir tonla, akıcı bir Türkçe ile oku. Çok yavaşlama. '
                     'Son paragrafı merak uyandıran bir soru sorar gibi oku. Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:'),
    'md1': dict(ids=['m1', 'd1', 'm4', 'd2', 'm5', 'd3', 'm6', 'd4', 'm7', 'd5', 'm8'],
                style=_DIZI + _M + 'İlk repliğinde şaşkın ve üzgün, kısa ve yüksek sesle; ikincisinde telaşla bağırıyor; üçüncüsünde inatla, ağlamaklı bağırıyor; '
                      'dördüncüsünde kapalı bir kapıya vurarak yalvarıyor; beşincisinde çaresizce bağırıyor; son repliğinde telaşla yalvarıyor. ' + _D +
                      'Bütün repliklerinde huzurlu ve şefkatli; ikinci repliğinde gülümseyerek teselli ediyor. ' + _SON),
    'md2': dict(ids=['m9', 'd6', 'm10', 'd7', 'm11', 'd8', 'm12', 'd9', 'm13', 'd10', 'm14'],
                style=_DIZI + _M + 'İlk repliğinde korkuyla bağırıyor; ikincisinde kararlı ve ağlamaklı; üçüncüsünde tedirgin, alçak sesle ama net; '
                      'dördüncüsünde şaşkın, merakla soruyor; beşincisinde üç istasyon adını tek tek, yavaşça okuyor, sonra şaşkınlıkla soruyor; '
                      'son repliğinde şüpheyle soruyor. ' + _D +
                      'İlk repliğinde pencereden manzaraya hayranlıkla bakıyor; diğerlerinde huzurlu, atasözü söyler gibi; '
                      'son repliğinde alçak sesle ama net, tane tane. ' + _SON),
    'md3': dict(ids=['m15', 'd11', 'm16', 'd12', 'm18', 'd13', 'm2', 'd15', 'm3', 'd14', 'm17'],
                style=_DIZI + _M + 'İlk repliğinde telaşla bağırıyor; ikincisinde endişeyle soruyor; üçüncüsünde öfkeyle, yüksek sesle; '
                      'dördüncüsünde yorgun, alçak sesle ama net; beşincisinde üzgün, alçak sesle ama net; '
                      'son repliğinde düşünceli, alçak sesle ama net, tane tane. ' + _D +
                      'İlk repliğinde biletine bakıp kendi kendine, sakin; ikincisinde rahat; üçüncü ve dördüncüsünde atasözü söyler gibi; '
                      'son repliğinde gülümseyerek, sıcak, yavaş ve tane tane, bir sır verir gibi. ' + _SON),
}

GAP_SCALE = 1.35
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {}
VOICE_FX = {'A': dict(intercom=True), 'D': dict(rate=0.95)}
TEMPO = {'*': 1.0}

# abone ol bandi: (replik_id, saniye). Bitis sahnesindeki ikinci bant bolum.py icinde.
ABONE = [('d1', 0.0)]
ABONE_END = 1.0                                             # son sahne basladiktan kac sn sonra

# ---- cizim ve sesin ortak kullandigi zamanlar (vurus basina gore saniye) ----
BRAKE = 0.1                                                 # 'stop' icinde frenin basladigi an
HALT = 2.2                                                  # 'stop' icinde trenin durdugu an
SHUT = 1.0                                                  # 'shut' icinde kapinin kapandigi an
OUT_OFF = (0.45, 0.95, 1.45)                                # 'out' icinde uc numaranin lambalarinin sondugu anlar
GONE = 2.2                                                  # 'out' icinde vagonun yok oldugu an (sis en yogunken)
SIT = 0.9                                                   # 'sit' icinde koltugun indigi an
NAMES_AT = (0.3, 0.9, 1.5)                                  # 'knit' icinde adlarin tek tek parladigi anlar
G_OFF = (0.5, 1.0)                                          # 'gone' icinde lambalarin sondugu anlar


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
def rewind(d=1.0, up=False):
    """bant geri sarma: hizli titreyen, kayan ton + hisirti (up: ileri sarma)"""
    m = _main(); t = m.tt(d); u = t / d
    f = 500 * (3.2 ** (u if up else 1 - u))
    x = np.sin(2 * np.pi * np.cumsum(f) / m.SR) * (0.55 + 0.45 * np.sign(np.sin(2 * np.pi * 26 * t)))
    n = m.highpass(m.RNG.standard_normal(len(t)).astype(np.float32), 2200) * 0.25
    return ((x * 0.4 + n) * m.env(d, 0.05, min(0.25, d / 3))).astype(np.float32) * 0.5


# ---- efekt ve muzik plani ----
def mix_plan(T):
    _main().FX.update(whistle=whistle, brake=brake, clack=clack, rewind=rewind)
    B, S, L, tot = T['beats'], T['scenes'], {l['id']: l for l in T['lines']}, T['total']
    fr = lambda i, f: L[i]['start'] + (L[i]['end'] - L[i]['start']) * f
    fx = []
    steps = lambda a, b, g=0.22, rate=1.8: fx.append(('steps', a, g, dict(d=max(0.3, b - a), rate=rate)))
    rails = lambda a, b, g=0.2, rate=1.6: fx.append(('clack', a, g, dict(d=max(0.6, b - a), rate=rate)))
    def stamp(t):                                               # saat etiketi oturur
        fx.append(('tick', t, 0.5, dict(f=900))); fx.append(('chime', t + 0.02, 0.3, dict(freqs=[293.66, 440.0], d=1.6)))
    def jump(name, up=False):                                   # geri sarma vurusu
        a, b = B[name]; fx.append(('rewind', a, 0.55, dict(d=b - a, up=up))); stamp(b - 0.05)

    # 1: kanca (SIMDI, iki numara)
    fx.append(('buzz', 0.0, 0.5, dict(d=0.22))); fx.append(('rumble', 0.0, 0.3, dict(d=1.4)))
    rails(0.0, S[2], 0.24, 1.9)
    # 2: disaridan
    fx.append(('whoosh', S[2] - 0.15, 0.4, dict(d=0.6, up=True))); rails(S[2], S[3], 0.16, 1.7)
    fx.append(('buzz', fr('n1', 0.62), 0.4, dict(d=0.2)))                                                  # uc numaranin ustunde carpi
    # 3: iki numara
    rails(S[3], S[4], 0.10, 1.7)
    for f_ in (0.3, 0.6): fx.append(('tick', fr('m3', f_), 0.2, dict(f=1700)))                             # sisler
    fx.append(('chime', B['title'][0] + 0.1, 0.6, dict(freqs=[311.13, 466.16, 622.25])))
    # 4: geri sarma
    fx.append(('rewind', L['n2']['start'], 0.22, dict(d=L['n2']['end'] - L['n2']['start'])))
    jump('rw1')
    # 5: Yedigol peronu, tren durur
    st = B['stop'][0]
    fx.append(('brake', st + BRAKE, 0.6, dict(d=2.0))); rails(st, st + 1.7, 0.2, 1.1)
    fx.append(('rumble', st + HALT - 0.2, 0.3, dict(d=1.0))); fx.append(('whoosh', st + HALT, 0.3, dict(d=1.0, up=False)))   # durdu: buhar
    # 6-7: on kapi
    fx.append(('hum', S[6], 0.22, dict(d=S[10] - S[6])))
    steps(S[6], fr('m4', 0.6), 0.24, 3.0)
    fx.append(('tick', fr('d1', 0.2), 0.3, dict(f=1500)))                                                  # orguyu uzatir
    sh = B['shut'][0]
    fx.append(('whoosh', sh + 0.15, 0.3, dict(d=0.4, up=True)))                                            # orgu el degistirir
    steps(sh + 0.3, sh + 0.9, 0.22, 2.6)
    fx.append(('slide', sh + SHUT - 0.5, 0.5, dict(d=0.6))); fx.append(('snap', sh + SHUT, 0.7, {}))
    # 8: kapi (iki numaradan)
    for f_ in (0.1, 0.4, 0.7): fx.append(('snap', fr('m6', f_), 0.35, {}))                                 # kapiya vurur
    sy = B['say'][0]
    fx.append(('whoosh', sy + 0.2, 0.35, dict(d=1.8, up=False)))                                           # buhar: ses duyulmaz
    for o in (0.5, 0.9, 1.3): fx.append(('tick', sy + o, 0.16, dict(f=420)))                               # camin ardindan bogu sesler
    # 9: lambalar, sis, bos ray
    ot = B['out'][0]
    for j, o in enumerate(OUT_OFF): fx.append(('buzz', ot + o, 0.45, dict(d=0.16))); fx.append(('tick', ot + o + 0.16, 0.4, dict(f=500 - 60 * j)))
    fx.append(('whistle', ot + 1.7, 0.55, dict(d=1.3))); fx.append(('whoosh', ot + 1.9, 0.4, dict(d=1.2, up=False)))
    fx.append(('rumble', ot + 2.0, 0.3, dict(d=1.0)))
    # 10-14: 5 dk once
    jump('rw2'); rails(S[10], S[15], 0.09, 1.3)
    for f_ in (0.3, 0.6): fx.append(('tick', fr('d3', f_), 0.2, dict(f=1700)))
    fx.append(('tick', L['d4']['start'] + 0.1, 0.4, dict(f=800))); fx.append(('buzz', fr('d4', 0.75), 0.3, dict(d=0.18)))   # biletler; bos satir
    lk = B['lakes'][0]
    fx.append(('chime', lk + 0.2, 0.4, dict(freqs=[349.23, 523.25, 698.46], d=2.6)))
    fx.append(('brake', fr('m11', 0.1), 0.2, dict(d=1.4)))
    # 15-18: 10 dk once
    jump('rw3'); rails(S[15], S[19], 0.09, 1.7)
    for f_ in (0.2, 0.6): fx.append(('tick', fr('m12', f_), 0.2, dict(f=1700)))
    kn = B['knit'][0]
    for j, o in enumerate(NAMES_AT): fx.append(('chime', kn + o, 0.3, dict(freqs=[(523.25, 587.33, 698.46)[j]], d=1.2)))
    fx.append(('chime', fr('d10', 0.4), 0.3, dict(freqs=[146.83, 220.0], d=2.0)))
    # 19-21: 15 dk once: anons
    jump('rw4'); rails(S[19], S[22], 0.10, 1.7)
    ch = B['chime'][0]
    fx.append(('chime', ch + 0.1, 0.6, dict(freqs=[659.25, 523.25], d=1.4))); fx.append(('chime', ch + 0.55, 0.5, dict(freqs=[523.25, 392.0], d=1.4)))
    fx.append(('hum', L['a1']['start'] - 0.2, 0.22, dict(d=L['a1']['end'] - L['a1']['start'] + 0.5)))
    for o in (0.0, 0.25, 0.5): fx.append(('buzz', fr('a1', 0.62) + o, 0.35, dict(d=0.14)))                 # levha kirmizi yanar
    fx.append(('tick', L['d11']['start'] + 0.05, 0.4, dict(f=800)))                                        # bilet
    si = B['sit'][0]
    fx.append(('slide', si + SIT - 0.4, 0.4, dict(d=0.45))); fx.append(('snap', si + SIT, 0.45, {}))       # katlanir koltuk iner
    # 22-23: gecenin basi
    jump('rw5'); rails(S[22], S[24], 0.10, 1.7)
    fx.append(('hum', L['a2']['start'] - 0.2, 0.22, dict(d=L['a2']['end'] - L['a2']['start'] + 0.5)))
    for o in (0.0, 0.25, 0.5): fx.append(('buzz', fr('a2', 0.8) + o, 0.3, dict(d=0.14)))
    fx.append(('chime', B['smile'][0] + 0.9, 0.4, dict(freqs=[349.23, 440.0, 523.25], d=2.4)))
    # 24: kapinin ardi (sesli)
    jump('ff', up=True)
    fx.append(('hum', S[24], 0.2, dict(d=S[25] - S[24])))
    gn = B['gone'][0]
    for j, o in enumerate(G_OFF): fx.append(('buzz', gn + o, 0.4, dict(d=0.16))); fx.append(('tick', gn + o + 0.16, 0.35, dict(f=440 - 60 * j)))
    # 25-26: SIMDI; kapanis
    fx.append(('whoosh', S[25] - 0.1, 0.3, dict(d=0.6, up=True))); rails(S[25], S[26] + 1.5, 0.12, 1.7)
    fx.append(('chime', B['end'][0] + 0.15, 0.55, dict(freqs=[207.65, 311.13, 415.3, 523.25], d=2.8)))
    for t0 in [L[i]['start'] + o for i, o in ABONE] + [S[26] + ABONE_END]:                                 # abone ol: tik + kisa zil
        fx.append(('tick', t0 + 2.3, 0.5, dict(f=1200))); fx.append(('chime', t0 + 2.45, 0.32, dict(freqs=[1318.5, 1760.0], d=1.0)))
    # muzik: SIMDI ve kapi gerilim; goller gorununce sicak (orgu sahnesi dahil); anonsla gerilim; gecenin basi ve Ada'nin sozu sicak; kapanis gizem
    music = [(0.0, lk, 'gerilim', 0.9), (lk, B['rw4'][0], 'sicak', 0.8), (B['rw4'][0], B['rw5'][0], 'gerilim', 0.9),
             (B['rw5'][0], S[25], 'sicak', 0.8), (S[25], tot, 'gizem', 1.0)]
    return dict(pads=[], fx=fx, music=music)
