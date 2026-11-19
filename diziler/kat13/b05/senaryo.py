"""13. Kat, 5. Bolum: Paket (dizi finali). Senaryo, ses gruplari, efekt plani.

Yapi: TEK MEKAN, GERCEK ZAMANLI. Kat 17'nin kurali "biri kalir". Asansorun sesi "Kapi doksan saniye sonra kapanir"
dedigi anda ekranda 01:30'dan geri sayan bir sayac baslar ve kapi tam 00:00'da kapanir: aradaki 90 saniye kesintisiz,
gercek zamanli akar (yalnizca aci degisir: kabin, 17. kattan kabine bakis, kutunun ustu, kart, raflar, panel).
Kanca: sayacin son saniyelerinden bir an (Luna: "Leo! Kim kalacak?"); ayni replik 90 saniyenin icinde yerinde yeniden gecer.
Kapanis: asansor ilk kez asagi iner (asansor boslugu kesiti), lobide bes kisi iner, 13. katta hardal sapkali biri.
Konusanlar: N anlatici, V asansorun sesi, L Leo, U Luna, M Luna'nin annesi
"""
TITLE = '13. KAT'
EP = '5. BÖLÜM'
EP_NAME = 'Paket'

SEQ = [
    # ---- 1: kanca (sayacin sonundan bir an) + hatirlatma + baslik ----
    ('scene', 1),
    ('line', 'h1', 'U', 'Leo! Kim kalacak?', ['Kim'], 0.25),                # ses: u7 ile ayni kayit (SEG_ALIAS)
    ('line', 'n1', 'N', 'Son katın kuralı iki kelimeydi: biri kalır.', ['biri', 'kalır.'], 0.3),
    ('line', 'n2', 'N', 'Önceki bölümde öğrendik: Leo bu asansöre hiç binmedi. Hep içerideydi.', ['hiç', 'binmedi.'], 0.3),
    ('beat', 'title', 2.5),

    # ---- 2: kabin: 16'dan 17'ye ----
    ('scene', 2),
    ('beat', 'ride', 0.8),
    ('line', 'l1', 'L', 'Luna. Bu paketi açmaya korkuyorum.', ['korkuyorum.'], 0.3),
    ('line', 'u1', 'U', 'Korkma Leo. İçinde ne varsa, zaten senin.', ['zaten', 'senin.'], 0.3),
    ('line', 'l2', 'L', 'Ya içinden kötü bir şey çıkarsa?', ['kötü'], 0.3),
    ('line', 'u2', 'U', 'O zaman en azından kim olduğunu bilirsin.', ['kim'], 0.1),
    ('beat', 'ding', 2.0),                                    # kapi acilir: 17. kat, karanlikta tek bir sandalye

    # ---- 3: kural ve sayac ----
    ('scene', 3),
    ('line', 'v1', 'V', 'On yedinci kat. Son kat. Bu katın tek bir kuralı var: biri kalır.', ['biri', 'kalır.'], 0.3),
    ('line', 'v2', 'V', 'Kapı doksan saniye sonra kapanır.', ['doksan', 'saniye'], 0.0),   # BITTIGI AN sayac baslar (T0)
    ('beat', 'start', 0.4),
    ('line', 'v3', 'V', 'Kimse kalmazsa, asansör bir daha hareket etmez.', ['Kimse'], 0.1),
    ('beat', 'look', 1.2),                                    # ikisi de kapidan disari bakar: bos sandalye

    # ---- 4: 17. kattan kabine bakis ----
    ('scene', 4),
    ('line', 'u3', 'U', 'Ben kalırım. Annem yukarıda. Hep yukarıda bekler.', ['Ben'], 0.2),
    ('line', 'l3', 'L', 'Dur! Önce paketi açalım. Belki cevap içindedir.', ['Dur!'], 0.1),

    # ---- 5: kutu (ustten) ----
    ('scene', 5),
    ('beat', 'open', 2.8),                                    # bant yirtilir, kapaklar acilir
    ('line', 'l4', 'L', 'Bir düğme. Üstünde tek bir harf var.', ['düğme.'], 0.3),
    ('line', 'u4', 'U', 'Lobi düğmesi bu. Panelde tam onun yeri boş.', ['Lobi', 'boş.'], 0.3),
    ('line', 'l5', 'L', 'Asansör bu yüzden aşağı inmiyormuş. Düğme hep bendeymiş.', ['bendeymiş.'], 0.3),
    ('line', 'u5', 'U', 'Kutuda bir şey daha var. Bir yaka kartı.', ['yaka', 'kartı.'], 0.1),

    # ---- 6: kart ----
    ('scene', 6),
    ('beat', 'card', 2.0),                                    # kart doner: GOREVLI
    ('line', 'l6', 'L', 'Bu benim kartım. Paketin göndereni bu yüzden yokmuş.', ['benim'], 0.3),
    ('line', 'n3', 'N', 'Leo kurye değildi. Bu asansörün görevlisiydi: yolcuları yukarı taşıyan kişi.', ['görevlisiydi:'], 0.3),

    # ---- 7: kabin: 17. katin isiklari yanar ----
    ('scene', 7),
    ('line', 'v4', 'V', 'Görevli tanındı. Görevli kalırsa, katlarda kalan bütün yolcular lobiye iner.', ['bütün', 'yolcular'], 0.3),
    ('line', 'u6', 'U', 'Bütün yolcular mı? Annem de mi?', ['Annem'], 0.3),
    ('line', 'l7', 'L', 'Annen de. Kai de, Zoe de, Sam de.', ['Kai', 'Zoe', 'Sam'], 0.1),

    # ---- 8: raflar ----
    ('scene', 8),
    ('beat', 'fear', 2.24),                                    # raflar dolusu ayni paket
    ('line', 'l8', 'L', 'Raflara bak, hepsi aynı paket. Ben bunu kaç kere yaptım?', ['kaç', 'kere'], 0.2),
    ('line', 'v6', 'V', 'Görevli, her yolcuyu yukarı taşıdı. Hiçbirini aşağı indirmedi.', ['Hiçbirini'], 0.3),

    # ---- 9: karar ----
    ('scene', 9),
    ('line', 'u7', 'U', 'Leo! Kim kalacak?', ['Kim'], 0.0),
    ('beat', 'decide', 2.5),                                  # Leo karta, sonra Luna'ya bakar
    ('line', 'l9', 'L', 'Görevli kalır. Bu sefer herkes iniyor.', ['Görevli', 'herkes'], 0.1),

    # ---- 10: panel ----
    ('scene', 10),
    ('beat', 'btn', 2.8),                                     # Leo dugmeyi yuvasina takar
    ('line', 'v5', 'V', 'Lobi düğmesi takıldı.', ['takıldı.'], 0.1),

    # ---- 11: veda ----
    ('scene', 11),
    ('beat', 'out', 2.4),                                     # Leo kapidan cikar
    ('line', 'u8', 'U', 'Leo, bekle! Sen de bin. Bir yolunu buluruz.', ['bekle!'], 0.1),
    ('line', 'l10', 'L', 'Ben bu asansöre hiç binmedim ki Luna. İnecek bir katım yok.', ['hiç', 'binmedim'], 0.1),
    ('beat', 'push', 1.8),                                    # Leo, Luna'yi iceri iter
    ('line', 'l11', 'L', 'Hadi. Annen seni bir yıldır bekliyor.', ['Annen'], 0.0),
    ('beat', 'close', 5.2),                                   # kapi kapanir: BITTIGI AN sayac 00:00 (T1)

    # ---- 12: Luna tek basina ----
    ('scene', 12),
    ('beat', 'shut', 1.5),
    ('line', 'u9', 'U', 'Teşekkür ederim Leo.', [], 0.1),
    ('beat', 'down', 1.2),                                    # asansor asagi hareket eder

    # ---- 13: asansor boslugu (kesit) ----
    ('scene', 13),
    ('line', 'n4', 'N', 'Asansör ilk kez aşağı indi. Her katta, kalanlardan biri geri döndü.', ['aşağı', 'geri', 'döndü.'], 0.1),
    ('beat', 'fall', 2.2),

    # ---- 14: lobi ----
    ('scene', 14),
    ('beat', 'lobby', 2.4),                                   # 3, 2, 1, L; kapi acilir
    ('line', 'u10', 'U', 'Anne!', [], 0.2),
    ('line', 'm1', 'M', 'Luna! Benim sabırlı kızım.', ['sabırlı'], 0.3),
    ('line', 'u11', 'U', 'Artık saymama gerek yok anne. Herkes burada.', ['Herkes'], 0.4),
    ('line', 'n5', 'N', 'O akşam asansöre dört kişi binmişti. Asansörden beş kişi indi.', ['dört', 'beş', 'kişi'], 0.5),

    # ---- 15: 13. kat ----
    ('scene', 15),
    ('beat', 'corr', 1.2),
    ('line', 'n6', 'N', 'Peki ya Leo? On üçüncü katta, hardal şapkalı biri hâlâ paket taşıyor.', ['Leo?', 'hâlâ'], 0.6),

    # ---- 16: kapanis ----
    ('scene', 16),
    ('beat', 'endin', 0.5),
    ('line', 'n7', 'N', 'On üçüncü Kat burada bitti. Yeni dizi çok yakında.', ['bitti.', 'çok', 'yakında.'], 0.3),
    ('beat', 'end', 3.4),
]

# ---- seslendirme: her grup TEK istek, en fazla 2 ses; grup icinde konusanlar sirayla degisir ----
VOICES = {'N': 'Achird', 'V': 'Kore', 'L': 'Puck', 'U': 'Leda', 'M': 'Aoede'}
NAMES = {'V': 'Asansor', 'L': 'Leo', 'U': 'Luna', 'M': 'Anne'}
_DIZI = 'Türkçe bir gerilim çizgi dizisinin final bölümünden replikler seslendir. '
_L = 'Leo genç bir kurye: samimi, tedirgin, kısa konuşuyor. '
_U = 'Luna küçük bir kız çocuğu: ince sesli, tuhaf biçimde sakin ve kendinden emin. '
GROUPS = {
    'na': dict(ids=['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7'],
               style='Gerilim dizisi anlatıcısı gibi, alçak, sakin ve tekinsiz bir tonla, akıcı bir Türkçe ile oku; son iki paragrafta '
                     'biraz daha sıcak. Çok yavaşlama. Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:'),
    'va': dict(ids=['v1', 'v2', 'v3', 'v4', 'v6', 'v5'],
               style='Bir asansörün anons sesi gibi oku: kadın, çok sakin, duygusuz, tane tane ve soğuk; akıcı bir Türkçe ile. '
                     'Çok yavaşlama. Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:'),
    'lu1': dict(ids=['l1', 'u1', 'l2', 'u2', 'l3', 'u3', 'l4', 'u4', 'l5', 'u5'],
                style=_DIZI + _L +
                      'İlk iki repliğinde korkuyor, alçak sesle ama net, tane tane; üçüncüsünde telaşla "Dur!" diye bağırıp hızlı konuşuyor; '
                      'dördüncüsünde şaşkın; beşincisinde yavaş yavaş anlıyor. ' + _U +
                      'Üçüncü repliğinde kararlı; dördüncü ve beşincisinde merakla bir şey gösteriyor. '
                      'Her replikten sonra bir saniye dur.'),
    'lu2': dict(ids=['l6', 'u6', 'l7', 'u7', 'l8', 'u8', 'l9', 'u9', 'l10', 'u10', 'l11', 'u11'],
                style=_DIZI + _L +
                      'İlk repliğinde şaşkın, kendi kendine konuşur gibi ama net; ikincisinde yumuşak ve güven verici; üçüncüsünde korkuyla; '
                      'dördüncüsünde çok kararlı, kısa ve net; beşincisinde hüzünlü ama sakin; son repliğinde şefkatle, veda eder gibi. ' + _U +
                      'İlk repliğinde umutla soruyor; ikincisinde telaşla bağırıyor; üçüncüsünde telaşla yalvarıyor; '
                      'dördüncüsünde alçak sesle ama net, hüzünlü; beşincisinde sevinçle bağırıyor; son repliğinde mutlu ve huzurlu. '
                      'Her replikten sonra bir saniye dur.'),
    'ma': dict(ids=['m1'],
               style='Bir yıldır görmediği küçük kızına kavuşan genç bir anne gibi, sıcak, sevinçli ve duygulu bir sesle, akıcı bir Türkçe ile söyle:'),
}

GAP_SCALE = 1.0                                            # replik arasi bosluklar
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {'h1': 'u7'}                                    # kanca, 90 saniyenin icindeki replikle ayni kayit
# Luna daha ince ve hizli (cocuk), anne biraz daha kalin, asansor anons hoparlorunden
VOICE_FX = {'U': dict(rate=1.14), 'M': dict(rate=0.96), 'V': dict(intercom=True)}
TEMPO = {'*': 1.0}

# abone ol bandi: (replik_id, saniye). Bitis sahnesindeki ikinci band bolum.py icinde.
ABONE = [('l2', 0.0)]
ABONE_END = 1.0                                             # son sahne basladiktan kac sn sonra

# ---- cizim ve sesin ortak kullandigi zamanlar (vurus basina gore saniye) ----
COUNT = 90.0                                                # sayac: v2 bittigi an baslar, 'close' vurusu bittigi an 00:00
DOOR_OPEN = 0.6                                             # 'ding' icinde kapinin acilmaya basladigi an
RIP = 0.6                                                   # 'open' icinde bandin yirtildigi an
FLAPS = 1.3                                                 # 'open' icinde kapaklarin acildigi an
FLIP = 0.5                                                  # 'card' icinde kartin donmeye basladigi an
LIGHTS = 0.3                                                # v4 repliginin bu oraninda 17. katin isiklari yanar
CLICK = 1.9                                                 # 'btn' icinde dugmenin yuvaya oturdugu an
PUSH = 0.7                                                  # 'push' icinde Leo'nun Luna'yi ittigi an
CLOSE_START = 1.1                                           # 'close' icinde kapinin kapanmaya basladigi an (vurus sonunda tam kapanir)
MOVE = 0.3                                                  # 'down' icinde asansorun hareket ettigi an
FALL_N, FALL_EASE = 5.6, 1.25                               # bosluk sahnesi: kac kat inilir, hizlanma
def fall_u(n):
    """bosluk sahnesinin hangi oraninda n kat asagida olunur (17'den n kat asagi)"""
    return (n / FALL_N) ** (1 / FALL_EASE)
RETURNS = (('Z', 2), ('S', 3), ('K', 4), ('M', 4))          # kim, 17'den kac kat asagida (15: Zoe, 14: Sam, 13: Kai ve anne)
LOBBY_DING = 1.1                                            # 'lobby' icinde asansorun lobiye vardigi an (kapi sonra acilir)
TALLY = (0.30, 0.36, 0.42, 0.48, 0.84)                      # n5 icinde sayac isaretleri: dort kisi bindi; besinci

# ---- efekt ve fon plani ----
DM = [73.42, 110.0, 146.83, 174.61]
AM = [110.0, 164.81, 220.0, 261.63]
CM = [130.81, 196.0, 261.63, 329.63]
LOW = [69.30, 103.83, 138.59, 164.81]
LOW2 = [61.74, 92.50, 123.47, 146.83]
FMAJ = [174.61, 220.0, 261.63, 349.23]                      # sicak: kavusma
CMAJ = [130.81, 164.81, 196.0, 261.63]


def mix_plan(T):
    B, S, L, tot = T['beats'], T['scenes'], {l['id']: l for l in T['lines']}, T['total']
    fr = lambda i, f: L[i]['start'] + (L[i]['end'] - L[i]['start']) * f
    T0 = L['v2']['end']; T1 = B['close'][1]
    pads = [(0.0, B['title'][0], LOW, 1.0), (B['title'][0], S[2], DM, 0.9), (S[2], B['ding'][0], CM, 0.55), (B['ding'][0], S[4], LOW2, 0.9),
            (S[4], S[6], AM, 0.7), (S[6], S[7], DM, 0.85), (S[7], S[9], LOW2, 0.9), (S[9], S[11], LOW, 1.0), (S[11], T1, DM, 1.0),
            (S[12] + 0.6, S[13], AM, 0.5), (S[13], S[14], CM, 0.8), (S[14], S[15], FMAJ, 1.0), (S[15], S[16], LOW2, 0.8), (S[16], tot, CMAJ, 0.9)]
    fx = []
    steps = lambda a, b, g=0.22, rate=1.7: fx.append(('steps', a, g, dict(d=max(0.3, b - a), rate=rate)))
    voice = lambda i, g=0.28: fx.append(('hum', L[i]['start'] - 0.2, g, dict(d=L[i]['end'] - L[i]['start'] + 0.5)))

    # sayac: saniyede bir tik (son 10 saniyede yuksek ve cift)
    n = int(round(T1 - T0))
    for i in range(n):
        left = n - i; t0 = T0 + i
        fx.append(('tick', t0, 0.5 if left <= 10 else (0.22 if left <= 30 else 0.13), dict(f=1250 if left <= 10 else 900)))
        if left <= 10: fx.append(('tick', t0 + 0.5, 0.3, dict(f=1000)))
    # 1: kanca (sayacin son saniyeleri: hizli tik + vizilti)
    fx.append(('buzz', 0.0, 0.5, dict(d=0.25)))
    for o in (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5): fx.append(('tick', 0.05 + o, 0.5 if o < 2 else 0.3, dict(f=1250)))
    fx.append(('hum', 0.0, 0.5, dict(d=L['n1']['end'])))
    fx.append(('whoosh', L['n2']['start'] - 0.35, 0.45, dict(d=0.8, up=True)))                       # geri donus: lobi
    fx.append(('ding', fr('n2', 0.5), 0.35, {}))
    fx.append(('buzz', fr('n2', 0.82), 0.35, dict(d=0.3)))
    fx.append(('chime', B['title'][0] + 0.1, 0.6, dict(freqs=[311.13, 466.16, 622.25])))
    # 2: kabin
    fx.append(('rumble', B['ride'][0], 0.22, dict(d=1.6)))
    fx.append(('rumble', L['u2']['start'], 0.22, dict(d=1.4)))
    dg = B['ding'][0]
    fx.append(('ding', dg + 0.15, 0.7, {}))
    fx.append(('slide', dg + DOOR_OPEN, 0.5, dict(d=1.3)))
    fx.append(('hum', dg + DOOR_OPEN + 0.4, 0.4, dict(d=1.4)))
    # 3: kural, sayac baslar
    for i in ('v1', 'v2', 'v3'): voice(i, 0.25)
    fx.append(('chime', T0, 0.5, dict(freqs=[440.0, 660.0], d=1.2)))
    fx.append(('buzz', T0 + 0.05, 0.4, dict(d=0.25)))
    fx.append(('hum', B['look'][0], 0.35, dict(d=1.4)))
    # 4: 17. kattan bakis
    steps(fr('u3', 0.05), fr('u3', 0.5), 0.2, 2.2)
    fx.append(('snap', L['l3']['start'] + 0.05, 0.4, {}))                                            # Leo kolunu uzatir
    # 5: kutu
    op = B['open'][0]
    fx.append(('tick', op + 0.15, 0.4, dict(f=300)))                                                 # paket yere konur
    fx.append(('whoosh', op + RIP - 0.1, 0.45, dict(d=0.5, up=True))); fx.append(('snap', op + RIP + 0.3, 0.45, {}))
    fx.append(('slide', op + FLAPS, 0.3, dict(d=0.7)))
    fx.append(('chime', op + FLAPS + 0.5, 0.5, dict(freqs=[523.25, 783.99, 1046.5], d=2.0)))
    fx.append(('tick', fr('l4', 0.1), 0.45, dict(f=1500)))
    fx.append(('whoosh', fr('u4', 0.42), 0.3, dict(d=0.5, up=True)))                                 # panel yakin plani
    for f_ in (0.6, 0.78): fx.append(('buzz', fr('u4', f_), 0.3, dict(d=0.14)))                       # bos yuva yanip soner
    fx.append(('chime', fr('l5', 0.55), 0.3, dict(freqs=[659.25, 987.77], d=1.2)))
    fx.append(('tick', fr('u5', 0.5), 0.4, dict(f=700)))
    # 6: kart
    cd = B['card'][0]
    fx.append(('whoosh', cd + FLIP, 0.4, dict(d=0.7, up=True)))
    fx.append(('chime', cd + FLIP + 0.7, 0.55, dict(freqs=[311.13, 466.16, 622.25], d=2.2)))
    for f_ in (0.62, 0.72, 0.82, 0.92): fx.append(('tick', fr('n3', f_), 0.25, dict(f=1000)))         # yolcular yukari
    # 7: isiklar yanar
    voice('v4'); voice('v6', 0.3)
    lt = fr('v4', LIGHTS)
    for o in (0.0, 0.18, 0.36): fx.append(('buzz', lt + o, 0.4, dict(d=0.14)))
    fx.append(('chime', lt + 0.5, 0.3, dict(freqs=[392.0, 587.33], d=1.6)))
    fx.append(('chime', fr('u6', 0.6), 0.22, dict(freqs=[880.0, 1318.5], d=1.0)))
    for f_ in (0.34, 0.6, 0.86): fx.append(('tick', fr('l7', f_), 0.3, dict(f=1000)))
    # 8: raflar
    fx.append(('hum', B['fear'][0], 0.55, dict(d=B['fear'][1] - B['fear'][0] + 1.5)))
    fx.append(('whoosh', B['fear'][0], 0.3, dict(d=1.2, up=False)))
    # 9: karar
    fx.append(('buzz', L['u7']['start'], 0.5, dict(d=0.25)))
    dc = B['decide'][0]
    for o in (0.2, 0.55, 1.1, 1.45): fx.append(('tick', dc + o, 0.5, dict(f=220)))                    # kalp atisi
    fx.append(('chime', L['l9']['start'], 0.4, dict(freqs=[146.83, 220.0, 293.66], d=2.0)))
    # 10: panel
    bt = B['btn'][0]
    steps(bt + 0.1, bt + 1.0, 0.22, 2.2)
    fx.append(('snap', bt + CLICK, 0.6, {})); fx.append(('tick', bt + CLICK, 0.6, dict(f=1500)))
    fx.append(('chime', bt + CLICK + 0.12, 0.55, dict(freqs=[880.0, 1318.5], d=1.4)))
    voice('v5')
    # 11: veda
    ot = B['out'][0]
    steps(ot + 0.25, ot + 2.1, 0.26, 1.8)
    steps(fr('u8', 0.0), fr('u8', 0.4), 0.2, 3.0)                                                     # Luna kosar
    ps = B['push'][0]
    fx.append(('whoosh', ps + PUSH - 0.15, 0.4, dict(d=0.6, up=False)))
    steps(ps + PUSH, ps + PUSH + 0.7, 0.2, 3.0)
    cl = B['close'][0]
    fx.append(('slide', cl + CLOSE_START, 0.55, dict(d=T1 - cl - CLOSE_START)))
    fx.append(('hum', cl + CLOSE_START, 0.5, dict(d=T1 - cl - CLOSE_START)))
    fx.append(('snap', T1 - 0.02, 0.8, {})); fx.append(('rumble', T1, 0.3, dict(d=1.2)))             # kapi kapandi
    fx.append(('buzz', T1, 0.5, dict(d=0.5)))
    # 12: Luna tek basina
    dn = B['down'][0]
    fx.append(('ding', dn + MOVE - 0.2, 0.5, {}))
    fx.append(('rumble', dn + MOVE, 0.3, dict(d=1.8)))
    # 13: bosluk
    a13, b13 = S[13], S[14]
    fx.append(('whoosh', a13, 0.4, dict(d=1.6, up=False)))
    fx.append(('hum', a13, 0.4, dict(d=b13 - a13)))
    fx.append(('rumble', a13 + 0.2, 0.2, dict(d=2.0))); fx.append(('rumble', a13 + (b13 - a13) * 0.5, 0.2, dict(d=2.0)))
    for (w, n_), fq in zip(RETURNS, ([659.25, 987.77], [587.33, 880.0], [523.25, 783.99], [783.99, 1174.66])):
        t0 = a13 + (b13 - a13) * fall_u(n_) + (0.25 if w == 'M' else 0.0)
        fx.append(('chime', t0, 0.5, dict(freqs=fq, d=1.6))); fx.append(('tick', t0, 0.4, dict(f=1500)))
    # 14: lobi
    lb = B['lobby'][0]
    for j, o in enumerate((0.15, 0.45, 0.75)): fx.append(('tick', lb + o, 0.3, dict(f=900 - 60 * j)))
    fx.append(('ding', lb + LOBBY_DING, 0.7, {}))
    fx.append(('slide', lb + LOBBY_DING + 0.3, 0.5, dict(d=1.0)))
    fx.append(('chime', lb + LOBBY_DING + 0.8, 0.5, dict(freqs=[523.25, 659.25, 783.99, 1046.5], d=2.6)))
    steps(L['m1']['start'], L['m1']['end'], 0.18, 2.4)
    for f_ in TALLY[:4]: fx.append(('tick', fr('n5', f_), 0.35, dict(f=1000)))
    fx.append(('chime', fr('n5', TALLY[4]), 0.5, dict(freqs=[783.99, 1174.66, 1567.98], d=2.0)))
    # 15: 13. kat
    cr = B['corr'][0]
    fx.append(('buzz', cr + 0.2, 0.3, dict(d=0.2)))
    steps(cr + 0.3, S[16] - 0.3, 0.26, 1.6)
    fx.append(('hum', cr, 0.35, dict(d=S[16] - cr)))
    fx.append(('chime', fr('n6', 0.55), 0.3, dict(freqs=[311.13, 466.16], d=2.0)))
    # 16: kapanis
    fx.append(('chime', B['end'][0], 0.55, dict(freqs=[261.63, 329.63, 392.0, 523.25], d=2.8)))
    for t0 in [L[i]['start'] + o for i, o in ABONE] + [S[16] + ABONE_END]:                           # abone ol: tik + kisa zil
        fx.append(('tick', t0 + 2.3, 0.5, dict(f=1200))); fx.append(('chime', t0 + 2.45, 0.32, dict(freqs=[1318.5, 1760.0], d=1.0)))
    return dict(pads=pads, fx=fx)
