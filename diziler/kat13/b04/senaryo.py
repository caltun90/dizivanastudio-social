"""13. Kat, 4. Bolum: Lobi. Senaryo, ses gruplari, efekt plani.

Yapi: GERI DONUSLU. Kat 16'da uc kapi var; her kapi bir soru sorar ve yalnizca dogruya acilir. Her cevap bir geri
donus sahnesi acar: (1) bir yil once Luna'nin annesi asansore biner (soluk, sepya); (2) 1. bolumun lobisi, bu kez
renkli ve net: binen dort kisi Kai, Zoe, Sam ve Luna; kapi acildiginda Leo zaten iceridedir.
Geri donusleri anlatici degil Luna anlatir. Yalan soyleyince isik kizarir ve karalti yaklasir.
Konusanlar: N anlatici, V asansorun sesi, L Leo, U Luna
"""
TITLE = '13. KAT'
EP = '4. BÖLÜM'
EP_NAME = 'Lobi'

SEQ = [
    # ---- 1: kanca (ileriden bir an: son kapi) ----
    ('scene', 1),
    ('beat', 'open', 0.6),
    ('line', 'n1', 'N', 'On altıncı katın kuralı basitti: yalan söyleme.', ['yalan', 'söyleme.'], 0.3),
    ('line', 'n2', 'N', "Ama son kapı Leo'ya öyle bir soru sordu ki, Leo cevabı bilmiyordu.", ['bilmiyordu.'], 0.4),
    ('beat', 'title', 2.5),

    # ---- 2: asansor (hatirlatma, sayim, kural) ----
    ('scene', 2),
    ('beat', 'dark', 0.5),
    ('line', 'n3', 'N', 'Önceki bölümde Zoe aynaya baktı ve camın içinde kaldı.', ['Zoe'], 0.3),
    ('line', 'n4', 'N', 'Dört kişi binmişti. Üç kişi gitti. Ama asansörde hâlâ iki kişi var.', ['iki', 'kişi'], 0.4),
    ('line', 'l1', 'L', 'Luna. Bir tek ikimiz kaldık.', [], 0.3),
    ('line', 'u1', 'U', 'Evet. Ve ikimizden biri fazla.', ['fazla.'], 0.3),
    ('line', 'l2', 'L', 'Fazla olan ben değilim. Bundan eminim.', ['eminim.'], 0.1),
    ('beat', 'ding', 2.0),                                    # kapi acilir: sorgu salonu, karsida 1 numarali kapi
    ('line', 'v1', 'V', 'On altıncı kata hoş geldiniz. Bu katın tek bir kuralı var: yalan söylemeyin.', ['yalan', 'söylemeyin.'], 0.3),
    ('line', 'v2', 'V', 'Kuralı bozan, katta kalır.', ['katta', 'kalır.'], 0.3),
    ('line', 'v3', 'V', 'Önünüzde üç kapı var. Her kapı bir soru sorar ve yalnızca doğruya açılır.', ['üç', 'kapı', 'doğruya'], 0.5),

    # ---- 3: birinci oda: kucuk bir yalan, sonra birinci soru ----
    ('scene', 3),
    ('beat', 'out', 1.3),                                     # asansorden cikarlar
    ('line', 'u2', 'U', 'Leo. Sen korkuyor musun?', [], 0.3),
    ('line', 'l3', 'L', 'Ben mi? Hayır. Hiç korkmuyorum.', ['Hiç'], 0.0),
    ('beat', 'lie', 2.4),                                     # isik kizarir: YALAN. Karalti Leo'nun arkasinda belirir
    ('line', 'u3', 'U', 'Yalan söyleme Leo! Hemen doğruyu söyle!', ['doğruyu'], 0.2),
    ('line', 'l4', 'L', 'Korkuyorum! Tamam, çok korkuyorum!', ['çok'], 0.0),
    ('beat', 'truth', 1.6),                                   # isik duzelir, karalti geri cekilir
    ('line', 'v4', 'V', 'Birinci kapı. Luna, bu binaya neden geldin?', ['neden'], 0.4),
    ('line', 'u4', 'U', 'Annemi bulmaya geldim.', ['Annemi'], 0.5),

    # ---- 4: geri donus 1: bir yil once (sepya) ----
    ('scene', 4),
    ('beat', 'fb1', 1.2),
    ('line', 'u5', 'U', 'Bir yıl önce annemle bu lobideydik. Annem asansöre bindi.', ['Bir', 'yıl', 'önce'], 0.3),
    ('line', 'u6', 'U', 'Bana, sen burada bekle, hemen geleceğim dedi.', ['bekle,'], 0.1),
    ('beat', 'up', 2.6),                                      # kapi kapanir, gosterge sayar: 12... 13
    ('line', 'u7', 'U', 'Asansör on ikiyi geçti ve on üçte durdu. Annem bir daha inmedi.', ['on', 'üçte'], 0.3),
    ('line', 'u7b', 'U', 'Herkes bana, bu binada on üçüncü kat yok dedi.', ['yok'], 0.5),

    # ---- 5: birinci kapi acilir ----
    ('scene', 5),
    ('beat', 'open1', 1.8),                                   # DOGRU: kapi acilir
    ('line', 'l5', 'L', 'Bir yıldır onu mu bekliyorsun?', ['Bir', 'yıldır'], 0.3),
    ('line', 'u8', 'U', 'Evet. O günden beri asansöre binen herkesi sayıyorum.', ['sayıyorum.'], 0.1),
    ('beat', 'thru1', 1.5),                                   # kapidan gecerler

    # ---- 6: ikinci oda: ikinci soru ----
    ('scene', 6),
    ('beat', 'in2', 0.8),
    ('line', 'v5', 'V', 'İkinci kapı. Luna, o akşam asansöre kaç kişi bindi?', ['kaç', 'kişi'], 0.4),
    ('line', 'u9', 'U', 'Dört kişi. Tek tek saydım.', ['Dört'], 0.5),

    # ---- 7: geri donus 2: o aksam, lobi (renkli ve net) ----
    ('scene', 7),
    ('beat', 'fb2', 1.0),
    ('line', 'u10', 'U', 'Önce Kai bindi. Sonra Zoe. Sonra Sam. En son da ben.', ['Kai', 'Zoe.', 'Sam.', 'ben.'], 0.3),
    ('line', 'l6', 'L', 'Peki ben? Ben ne zaman bindim?', ['ne', 'zaman'], 0.1),
    ('beat', 'doorfb', 2.8),                                  # geri sar: kapi acilir, Leo zaten iceride
    ('line', 'u11', 'U', 'Sen binmedin Leo. Kapı açıldığında, sen zaten içerideydin.', ['zaten', 'içerideydin.'], 0.5),

    # ---- 8: ikinci oda: itiraz (ikinci yalan), kapi acilir ----
    ('scene', 8),
    ('beat', 'back', 1.4),                                    # DOGRU: ikinci kapi acilmaya baslar
    ('line', 'l7', 'L', 'Hayır! Ben de sizinle bindim!', ['Hayır!'], 0.0),
    ('beat', 'lie2', 2.4),                                    # isik kizarir; karalti bu kez Leo'nun omzuna uzanir
    ('line', 'u12', 'U', 'Leo, dur! Emin olmadığın şeyi söyleme!', ['söyleme!'], 0.0),
    ('beat', 'hush', 1.8),                                    # Leo agzini kapatir; karalti cekilir
    ('line', 'l7b', 'L', 'Kapı açıldı... Demek doğru söylüyorsun.', ['doğru'], 0.1),
    ('beat', 'thru2', 1.5),

    # ---- 9: ucuncu oda: son soru ----
    ('scene', 9),
    ('beat', 'in3', 0.8),
    ('line', 'v6', 'V', 'Son kapı. Leo, sen bu asansöre nereden bindin?', ['nereden'], 0.1),
    ('beat', 'think', 2.0),                                   # Leo hatirlamaya calisir: bos balon
    ('line', 'l8', 'L', 'Bilmiyorum. Hiçbir şey hatırlamıyorum.', ['hatırlamıyorum.'], 0.0),
    ('beat', 'wait', 2.6),                                    # sessizlik... isik yesile doner
    ('line', 'n7', 'N', 'Kapı açıldı. Çünkü bu, doğruydu.', ['doğruydu.'], 0.4),
    ('line', 'l9', 'L', 'Luna... Ben kimim?', ['kimim?'], 0.3),
    ('line', 'u13', 'U', 'Bilmiyorum. Ama elindeki paket biliyor olabilir.', ['paket'], 0.1),
    ('beat', 'leave', 2.6),                                   # kapidan asansore girerler

    # ---- 10: yine asansor ----
    ('scene', 10),
    ('beat', 'ride', 0.6),
    ('line', 'v7', 'V', 'Kurala uydunuz. Sıradaki ve son kat: on yedi.', ['on', 'yedi.'], 0.3),
    ('line', 'n8', 'N', 'O akşam asansöre dört kişi binmişti. Beşinci kişi, hep içerideydi.', ['Beşinci', 'içerideydi.'], 0.7),

    # ---- 11: bitis ----
    ('scene', 11),
    ('beat', 'endin', 0.5),
    ('line', 'n9', 'N', 'Sence Leo kim? Devamı, bir sonraki bölümde.', ['bir', 'sonraki', 'bölümde.'], 0.3),
    ('beat', 'end', 3.4),
]

# ---- seslendirme: her grup TEK istek, en fazla 2 ses; grup icinde konusanlar sirayla degisir ----
VOICES = {'N': 'Achird', 'V': 'Kore', 'L': 'Puck', 'U': 'Leda'}
NAMES = {'V': 'Asansor', 'L': 'Leo', 'U': 'Luna'}
_DIZI = 'Türkçe bir gerilim çizgi dizisinden replikler seslendir. '
_V = 'Asansor bir asansörün anons sesi: kadın, çok sakin, duygusuz, tane tane ve soğuk. '
GROUPS = {
    'na': dict(ids=['n1', 'n2', 'n3', 'n4', 'n7', 'n8', 'n9'],
               style='Gerilim dizisi anlatıcısı gibi, alçak, sakin ve tekinsiz bir tonla, akıcı bir Türkçe ile oku. '
                     'Çok yavaşlama. Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:'),
    'uf': dict(ids=['u5', 'u6', 'u7', 'u7b', 'u10'],
               style='Küçük bir kız çocuğu, geçmişte yaşadığı bir anıyı anlatıyor: ince sesli, tuhaf biçimde sakin, biraz hüzünlü '
                     'ama ağlamıyor; net ve akıcı bir Türkçe ile. Çok yavaşlama. Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:'),
    # lu: 2.5 kotasi doldugu icin gemini-3.1-flash-tts-preview ile uretildi (tek istek)
    'vl': dict(ids=['v1', 'l1', 'v2', 'l2', 'v3', 'l7b', 'v6', 'l8'],
               style=_DIZI + _V +
                     'Leo genç bir kurye: samimi, tedirgin, kısa konuşuyor. İlk repliğinde üzgün; ikincisinde kendinden emin; '
                     'üçüncüsünde şaşkın ve yenilmiş; son repliğinde çaresiz, alçak sesle ama net, tane tane. '
                     'Her replikten sonra bir saniye dur.'),
    'vu': dict(ids=['u1', 'v4', 'u4', 'v5', 'u9', 'v7', 'u13'],
               style=_DIZI +
                     'Luna küçük bir kız çocuğu: ince sesli, tuhaf biçimde sakin ve kendinden emin. ' + _V +
                     'Her replikten sonra bir saniye dur.'),
    'lu': dict(ids=['l5', 'u8', 'l6', 'u11', 'l7', 'u12', 'l9', 'u2', 'l3', 'u3', 'l4'],
               style=_DIZI +
                     'Leo genç bir kurye: samimi ve tedirgin. İlk iki repliğinde şaşkın, merakla soruyor; üçüncüsünde itiraz edip bağırıyor; '
                     'dördüncüsünde kırgın, alçak sesle ama net, tane tane; beşincisinde yapmacık bir rahatlıkla; son repliğinde korkuyla bağırıyor. '
                     'Luna küçük bir kız çocuğu: ince sesli, tuhaf biçimde sakin ve kendinden emin; üçüncü ve beşinci repliklerinde telaşla bağırıyor. '
                     'Her replikten sonra bir saniye dur.'),
}

GAP_SCALE = 1.0                                            # replik arasi bosluklar
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {}
# Luna daha ince ve hizli (cocuk), asansor anons hoparlorunden
VOICE_FX = {'U': dict(rate=1.14), 'V': dict(intercom=True)}
TEMPO = {'*': 1.0}

# abone ol bandi: (replik_id, saniye). Bitis sahnesindeki ikinci band bolum.py icinde.
ABONE = [('l1', 0.0)]
ABONE_END = 1.0                                             # son sahne basladiktan kac sn sonra

# ---- cizim ve sesin ortak kullandigi zamanlar (vurus basina gore saniye) ----
RED_ON = 0.25                                               # 'lie' ve 'lie2' icinde isigin kizardigi an
SHADOW_IN = 0.8                                             # karaltinin belirdigi an
SHUT = 0.3                                                  # 'up' icinde lobi kapisinin kapanmaya basladigi an
STOP13 = 1.9                                                # 'up' icinde gostergenin 13'te durdugu an
FB_DING = 0.5                                               # 'doorfb' icinde lobi asansorunun geldigi an (kapi sonra acilir)
GREEN = 1.7                                                 # 'wait' icinde isigin yesile dondugu an

# ---- efekt ve fon plani ----
DM = [73.42, 110.0, 146.83, 174.61]
AM = [110.0, 164.81, 220.0, 261.63]
CM = [130.81, 196.0, 261.63, 329.63]
LOW = [69.30, 103.83, 138.59, 164.81]
LOW2 = [61.74, 92.50, 123.47, 146.83]
FMAJ = [174.61, 220.0, 261.63, 349.23]                      # ani: sicak, soluk
FB2C = [146.83, 220.0, 293.66, 369.99]                      # ikinci ani: acik ama tedirgin


def mix_plan(T):
    B, S, L, tot = T['beats'], T['scenes'], {l['id']: l for l in T['lines']}, T['total']
    fr = lambda i, f: L[i]['start'] + (L[i]['end'] - L[i]['start']) * f
    pads = [(S[1], S[2], LOW, 1.0), (S[2], B['ding'][0], CM, 0.55), (B['ding'][0], S[3], DM, 0.9),
            (S[3], S[4], LOW2, 0.8), (S[4], S[5], FMAJ, 0.9), (S[5], S[7], AM, 0.7), (S[7], S[8], FB2C, 0.85),
            (S[8], S[9], LOW2, 1.0), (S[9], B['wait'][0], LOW, 1.0), (B['wait'][0] + GREEN, S[10], DM, 0.9), (S[10], S[11], CM, 0.6), (S[11], tot, DM, 1.0)]
    fx = []
    steps = lambda a, b, g=0.22, rate=1.7: fx.append(('steps', a, g, dict(d=max(0.3, b - a), rate=rate)))
    voice = lambda i, g=0.3: fx.append(('hum', L[i]['start'] - 0.2, g, dict(d=L[i]['end'] - L[i]['start'] + 0.5)))

    def lie(t0, d):                                          # isik kizarir: vizilti + alcak ugultu; karalti: ters ruzgar
        for o in (0.0, 0.22, 0.44): fx.append(('buzz', t0 + RED_ON + o, 0.5, dict(d=0.18)))
        fx.append(('hum', t0 + RED_ON, 0.6, dict(d=d)))
        fx.append(('whoosh', t0 + SHADOW_IN, 0.5, dict(d=1.0, up=False)))

    def right(t0, g=0.5):                                    # DOGRU: iki notali zil + kapi kayar
        fx.append(('chime', t0, g, dict(freqs=[880.0, 1318.5], d=1.2))); fx.append(('tick', t0, 0.5, dict(f=1500)))

    # 1: kanca
    for o in (0.3, 1.1, 1.9, 2.7, 3.5): fx.append(('tick', B['open'][0] + o, 0.3, dict(f=700)))      # kirmizi isik: saat gibi
    fx.append(('hum', L['n2']['start'], 0.35, dict(d=L['n2']['end'] - L['n2']['start'])))
    fx.append(('buzz', fr('n2', 0.82), 0.4, dict(d=0.3)))
    fx.append(('chime', B['title'][0] + 0.1, 0.6, dict(freqs=[311.13, 466.16, 622.25])))
    # 2: asansor
    fx.append(('buzz', B['dark'][0] + 0.2, 0.35, dict(d=0.2)))
    fx.append(('tick', fr('n3', 0.75), 0.4, dict(f=500)))
    for f_ in (0.36, 0.52): fx.append(('tick', fr('n4', f_), 0.35, dict(f=560)))
    fx.append(('buzz', fr('n4', 0.82), 0.4, dict(d=0.3)))
    dg = B['ding'][0]
    fx.append(('rumble', L['l2']['start'] + 0.3, 0.25, dict(d=1.4)))
    fx.append(('ding', dg + 0.15, 0.7, {}))
    fx.append(('slide', dg + 0.6, 0.5, dict(d=1.3)))
    for i in ('v1', 'v2', 'v3'): voice(i, 0.25)
    fx.append(('chime', fr('v3', 0.2), 0.2, dict(freqs=[880.0, 1318.5], d=0.8)))
    # 3: birinci oda
    steps(B['out'][0] + 0.15, B['out'][1])
    lie(B['lie'][0], L['l4']['end'] - B['lie'][0] - 0.2)
    fx.append(('whoosh', B['truth'][0] + 0.2, 0.35, dict(d=0.9, up=True)))
    fx.append(('chime', B['truth'][0] + 0.5, 0.25, dict(freqs=[659.25, 987.77], d=1.0)))
    voice('v4')
    # 4: geri donus 1
    fx.append(('whoosh', B['fb1'][0] - 0.3, 0.5, dict(d=1.0, up=True)))
    fx.append(('chime', B['fb1'][0] + 0.35, 0.5, dict(freqs=[523.25, 783.99, 1046.5], d=2.2)))
    steps(fr('u5', 0.55), fr('u5', 0.98), 0.2, 2.0)
    up = B['up'][0]
    fx.append(('slide', up + SHUT, 0.45, dict(d=1.0)))
    fx.append(('rumble', up + SHUT + 0.9, 0.2, dict(d=1.0)))
    for j in range(5): fx.append(('tick', up + 1.25 + j * 0.13, 0.25, dict(f=900 + 60 * j)))
    fx.append(('buzz', up + STOP13, 0.5, dict(d=0.4)))
    fx.append(('hum', up + STOP13, 0.4, dict(d=L['u7']['end'] - up - STOP13)))
    for f_ in (0.2, 0.55): fx.append(('tick', fr('u7b', f_), 0.3, dict(f=420)))
    # 5: birinci kapi
    fx.append(('whoosh', B['open1'][0] - 0.3, 0.4, dict(d=0.8, up=False)))
    right(B['open1'][0] + 0.5); fx.append(('slide', B['open1'][0] + 0.8, 0.5, dict(d=1.0)))
    for f_ in (0.45, 0.6, 0.75, 0.9): fx.append(('tick', fr('u8', f_), 0.25, dict(f=1100)))
    steps(B['thru1'][0] + 0.1, B['thru1'][1], 0.25, 2.0)
    # 6: ikinci oda
    steps(B['in2'][0], B['in2'][1], 0.22, 2.0)
    voice('v5')
    for f_ in (0.5, 0.72, 0.84, 0.96): fx.append(('tick', fr('u9', f_), 0.25, dict(f=1100)))
    # 7: geri donus 2
    fx.append(('whoosh', B['fb2'][0] - 0.3, 0.5, dict(d=1.0, up=True)))
    fx.append(('chime', B['fb2'][0] + 0.3, 0.5, dict(freqs=[587.33, 880.0, 1174.66], d=2.2)))
    for f_ in (0.08, 0.36, 0.62, 0.88): fx.append(('tick', fr('u10', f_), 0.4, dict(f=1000)))
    steps(fr('u10', 0.05), L['u10']['end'], 0.18, 2.2)
    fx.append(('whoosh', L['l6']['start'] + 0.1, 0.4, dict(d=L['l6']['end'] - L['l6']['start'], up=False)))   # geri sarma
    df = B['doorfb'][0]
    fx.append(('ding', df + FB_DING, 0.7, {}))
    fx.append(('slide', df + FB_DING + 0.5, 0.5, dict(d=1.2)))
    fx.append(('hum', df + FB_DING + 1.0, 0.45, dict(d=L['u11']['end'] - df - FB_DING - 0.6)))
    fx.append(('buzz', fr('u11', 0.75), 0.4, dict(d=0.35)))
    # 8: ikinci oda: itiraz
    fx.append(('whoosh', B['back'][0] - 0.3, 0.4, dict(d=0.8, up=False)))
    right(B['back'][0] + 0.4); fx.append(('slide', B['back'][0] + 0.7, 0.45, dict(d=0.9)))
    lie(B['lie2'][0], L['u12']['end'] - B['lie2'][0] + 0.6)
    fx.append(('snap', B['lie2'][0] + 1.7, 0.4, {}))                                               # el omuza konar
    fx.append(('whoosh', B['hush'][0] + 0.7, 0.35, dict(d=0.9, up=True)))
    steps(B['thru2'][0] + 0.1, B['thru2'][1], 0.25, 2.0)
    # 9: ucuncu oda
    steps(B['in3'][0], B['in3'][1], 0.22, 2.0)
    voice('v6', 0.35)
    th = B['think'][0]
    for o in (0.2, 0.8, 1.4): fx.append(('tick', th + o, 0.35, dict(f=700)))
    fx.append(('chime', th + 0.75, 0.22, dict(freqs=[415.3, 554.37], d=1.2)))                       # bos dusunce balonu
    wt = B['wait'][0]
    for o in (0.2, 0.7, 1.2): fx.append(('tick', wt + o, 0.4, dict(f=700)))
    fx.append(('hum', wt + 0.1, 0.45, dict(d=GREEN)))
    right(wt + GREEN, 0.6); fx.append(('slide', wt + GREEN + 0.25, 0.5, dict(d=1.1)))
    fx.append(('chime', fr('u13', 0.5), 0.25, dict(freqs=[311.13, 466.16], d=1.6)))                  # paket
    lv = B['leave'][0]
    steps(lv + 0.2, lv + 2.0, 0.26, 2.0)
    # 10: yine asansor
    rd = B['ride'][0]
    fx.append(('slide', rd - 0.3, 0.45, dict(d=0.9)))
    fx.append(('ding', rd + 0.1, 0.4, {}))
    voice('v7')
    fx.append(('rumble', L['v7']['end'] + 0.1, 0.22, dict(d=1.6)))
    for f_ in (0.26, 0.32, 0.38, 0.44): fx.append(('tick', fr('n8', f_), 0.3, dict(f=600)))
    fx.append(('buzz', fr('n8', 0.64), 0.5, dict(d=0.5)))
    fx.append(('chime', B['end'][0], 0.55, dict(freqs=[311.13, 466.16], d=2.4)))
    for t0 in [L[i]['start'] + o for i, o in ABONE] + [S[11] + ABONE_END]:                          # abone ol: tik + kisa zil
        fx.append(('tick', t0 + 2.3, 0.5, dict(f=1200))); fx.append(('chime', t0 + 2.45, 0.32, dict(freqs=[1318.5, 1760.0], d=1.0)))
    return dict(pads=pads, fx=fx)
