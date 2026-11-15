"""13. Kat, 2. Bolum: Sessizlik. Senaryo, ses gruplari, efekt plani.

Yapi: NEREDEYSE DIYALOGSUZ bolum. Asansorde kisa konusma; kural basladiktan sonra katta kimse konusmaz:
jest, bakis, avuca yazi, parmakla sayma, ses efektleri ve yalnizca anlatici. Tek istisna Sam'in bagirisi.
Luna bu bolumde hic konusmaz (parmaklariyla sayar).
Konusanlar: N anlatici, V asansorun sesi, L Leo, Z Zoe, S Sam
"""
TITLE = '13. KAT'
EP = '2. BÖLÜM'
EP_NAME = 'Sessizlik'

SEQ = [
    # ---- 1: kanca (ileriden bir an: arsivde paket tikirdar) ----
    ('scene', 1),
    ('beat', 'open', 0.5),
    ('line', 'n1', 'N', 'On dördüncü katın tek bir kuralı vardı: ses çıkarmayın.', ['ses', 'çıkarmayın.'], 0.2),
    ('beat', 'tik0', 1.5),                                    # paket tikirdar, herkes donar
    ('line', 'n2', 'N', "Ve Leo'nun paketi, tam o sırada tıkırdamaya başladı.", ['tıkırdamaya'], 0.4),
    ('beat', 'title', 2.5),

    # ---- 2: asansor (kisa konusma, kural) ----
    ('scene', 2),
    ('beat', 'dark', 0.6),
    ('line', 'n3', 'N', 'Önceki bölümde Kai on üçüncü katta kaldı, ama asansörde hâlâ dört kişi vardı.', ['dört', 'kişi'], 0.2),
    ('beat', 'lights', 1.0),                                  # isiklar geri gelir
    ('line', 'z1', 'Z', 'Dört kişi bindiysek, fazla olan kim?', ['fazla'], 0.3),
    ('line', 's1', 'S', 'Kimse fazla değil kızım. Çocuk yanlış saymıştır.', [], 0.1),
    ('beat', 'fingers', 1.5),                                 # Luna dort parmagini kaldirir
    ('line', 'l1', 'L', 'Şimdi sırası değil. Bakın, duruyoruz.', [], 0.1),
    ('beat', 'ding', 2.0),                                    # kapi acilir: karanlik arsiv
    ('line', 'v1', 'V', 'On dördüncü kata hoş geldiniz. Bu katın tek bir kuralı var: ses çıkarmayın.', ['ses', 'çıkarmayın.'], 0.3),
    ('line', 's2', 'S', 'Ses mi? Fısıldasak da mı?', [], 0.3),
    ('line', 'v2', 'V', 'Kuralı bozan, katta kalır.', ['katta', 'kalır.'], 0.3),
    ('line', 'z2', 'Z', 'Peki çıkış nerede?', [], 0.3),
    ('line', 'l2', 'L', 'Orada. En dipteki kırmızı kapı.', ['kırmızı'], 0.3),
    ('line', 's3', 'S', 'Luna, yanımdan ayrılma kızım.', [], 0.3),
    ('line', 'v3', 'V', 'Kural, şimdi başlıyor.', ['şimdi'], 0.1),
    ('beat', 'hush', 1.5),                                    # herkes agzini kapatir

    # ---- 3: arsiv: citirti, gozler, avuca yazi ----
    ('scene', 3),
    ('beat', 'out', 1.2),                                     # asansorden parmak ucunda cikarlar
    ('line', 'n4', 'N', 'Raflarla dolu, karanlık bir arşiv. Yerler kâğıt doluydu.', ['kâğıt'], 0.1),
    ('beat', 'tiptoe', 0.8),
    ('beat', 'crack', 1.7),                                   # Zoe bir kagida basar: CIT
    ('line', 'n5', 'N', 'Tek bir çıtırtı yetti. Rafların arasında bir şey uyandı.', ['uyandı.'], 0.1),
    ('beat', 'wait', 1.6),                                    # gozler bakinir, sonra kapanir
    ('beat', 'write', 2.4),                                   # Zoe avucuna yazar ve gosterir
    ('line', 'n7', 'N', 'Zoe avucuna yazdı: kâğıda basmayın.', ['kâğıda', 'basmayın.'], 0.1),
    ('beat', 'nod', 0.9),

    # ---- 4: sayim ve paket ----
    ('scene', 4),
    ('beat', 'walk2', 1.0),
    ('line', 'n8', 'N', 'Luna yürürken parmaklarıyla saydı.', ['saydı.'], 0.1),
    ('beat', 'count', 2.4),                                   # 1, 2, 3, 4
    ('line', 'n9', 'N', 'Yine dört. Olması gereken üçtü.', ['dört.', 'üçtü.'], 0.1),
    ('beat', 'tik', 2.0),                                     # paket: tik tik tik
    ('line', 'n10', 'N', 'Sonra paket tıkırdadı. İçinde bir şey kıpırdıyordu.', ['tıkırdadı.'], 0.1),
    ('beat', 'hug', 1.8),                                     # Leo paketi gogsune bastirir, gozler acilir
    ('line', 'n11', 'N', 'Leo paketi göğsüne bastırdı. Ses kesildi.', ['kesildi.'], 0.1),
    ('beat', 'ask', 2.4),                                     # Zoe avucuna yazar: ICINDE NE VAR?
    ('line', 'n12', 'N', 'İçinde ne vardı? Leo da bilmiyordu.', ['bilmiyordu.'], 0.4),

    # ---- 5: kule devrilir, Sam bagirir ----
    ('scene', 5),
    ('beat', 'lean', 1.8),
    ('line', 'n13', 'N', 'Luna geride kalmıştı. Tam üstünde, dev bir kâğıt kulesi eğiliyordu.', ['kâğıt', 'kulesi'], 0.1),
    ('beat', 'wave', 1.9),                                    # Sam el sallar, Luna gormez
    ('line', 'n14', 'N', 'Sam el salladı. Luna görmedi.', ['görmedi.'], 0.1),
    ('beat', 'think', 1.4),                                   # Sam kuleye, Luna'ya bakar; nefes alir
    ('line', 'n15', 'N', 'Sam bir an durdu. Sonra kararını verdi.', ['kararını'], 0.25),
    ('line', 's4', 'S', 'Luna! Kaç oradan!', ['Kaç'], 0.0),
    ('beat', 'crash', 2.4),                                   # Luna kacar, kule devrilir
    ('beat', 'taken', 3.4),                                   # isiklar soner, karalti Sam'i alir
    ('beat', 'hush2', 1.7),                                   # Luna ciglik atacakken Zoe agzini kapatir
    ('line', 'v4', 'V', 'Üç kişi kaldınız.', ['Üç'], 0.1),
    ('beat', 'beret', 1.5),                                   # bere Luna'nin ayagina yuvarlanir
    ('line', 'n16', 'N', 'Geriye yalnızca yeşil beresi kaldı.', ['beresi'], 0.5),

    # ---- 6: asansore donus, panel ----
    ('scene', 6),
    ('beat', 'door', 2.3),                                    # kirmizi kapi acilir: yine asansor
    ('beat', 'inside', 1.0),                                  # kabinde: kapi kapanir
    ('line', 'v5', 'V', 'Kurala uydunuz. Sıradaki kat: on beş.', ['on', 'beş.'], 0.1),
    ('beat', 'rise', 1.2),
    ('line', 'z3', 'Z', 'Sam kuralı biliyordu. Yine de bağırdı.', ['Yine', 'de'], 0.3),
    ('line', 'l3', 'L', "Luna'yı kurtardı.", [], 0.1),
    ('beat', 'panel', 2.1),                                   # Zoe panele bakar: yakin plan
    ('line', 'z4', 'Z', 'Leo, bak. Panelde lobi düğmesi yok.', ['lobi', 'düğmesi', 'yok.'], 0.3),
    ('line', 'l4', 'L', 'Hiç fark etmemiştim.', [], 0.3),
    ('line', 'z5', 'Z', 'Bu asansör aşağı hiç inmiyor mu?', ['hiç'], 0.1),
    ('beat', 'stare', 0.8),
    ('line', 'n17', 'N', 'Dört kişi binmişti. İki kişi gitti.', ['İki', 'kişi'], 0.3),
    ('line', 'n17b', 'N', 'Ama asansörde hâlâ üç kişi var.', ['üç', 'kişi'], 0.7),

    # ---- 7: bitis ----
    ('scene', 7),
    ('beat', 'endin', 0.5),
    ('line', 'n18', 'N', 'Sence Sam bilerek mi bağırdı? Devamı, bir sonraki bölümde.', ['bir', 'sonraki', 'bölümde.'], 0.3),
    ('beat', 'end', 3.0),
]

# ---- seslendirme: her grup TEK istek, en fazla 2 ses; grup icinde konusanlar sirayla degisir ----
VOICES = {'N': 'Achird', 'V': 'Kore', 'L': 'Puck', 'Z': 'Aoede', 'S': 'Algenib'}
NAMES = {'V': 'Asansor', 'L': 'Leo', 'Z': 'Zoe', 'S': 'Sam'}
_NARR = ('Gerilim dizisi anlatıcısı gibi, alçak, sakin ve tekinsiz bir tonla, akıcı bir Türkçe ile oku. '
         'Çok yavaşlama. Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:')
GROUPS = {
    'na': dict(ids=['n1', 'n2', 'n3', 'n4', 'n5', 'n7'], style=_NARR),
    'nb': dict(ids=['n8', 'n9', 'n10', 'n11', 'n12', 'n13'], style=_NARR),
    'nc': dict(ids=['n14', 'n15', 'n16', 'n17', 'n17b', 'n18'], style=_NARR),
    'vs': dict(ids=['v1', 's1', 'v2', 's2', 'v3', 's3', 'v4', 's4', 'v5'],
               style='Türkçe bir gerilim çizgi dizisinden replikler seslendir. '
                     'Asansor bir asansörün anons sesi: kadın, çok sakin, duygusuz, tane tane ve soğuk. '
                     'Sam yaşlı bir bina görevlisi: kalın, yorgun, babacan ve sakin bir ses; ikinci repliğinde alçak sesle ama net, tane tane soruyor; '
                     'son repliğinde bir çocuğu uyarmak için var gücüyle, telaşla bağırıyor. '
                     'Her replikten sonra bir saniye dur.'),
    'zl': dict(ids=['z1', 'l1', 'z2', 'l2', 'z3', 'l3', 'z4', 'l4', 'z5'],
               style='Türkçe bir gerilim çizgi dizisinden replikler seslendir. '
                     'Zoe genç bir kadın, doktor: zeki, net, şüpheci; son repliklerinde alçak sesle ve düşünceli konuşuyor. '
                     'Leo genç bir kurye: samimi, tedirgin, kısa konuşuyor; son repliklerinde üzgün ve şaşkın. '
                     'Her replikten sonra bir saniye dur.'),
}

GAP_SCALE = 0.75                                            # replik arasi bosluklar
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {}
VOICE_FX = {'Z': dict(rate=0.95), 'V': dict(intercom=True)}
TEMPO = {'*': 1.0, 'N': 1.04}

# abone ol bandi: (replik_id, saniye). Bitis sahnesindeki ikinci band bolum.py icinde.
ABONE = [('s1', 0.0)]
ABONE_END = 1.0                                             # son sahne basladiktan kac sn sonra

# ---- cizim ve sesin ortak kullandigi zamanlar (vurus basina gore saniye) ----
TIK = (0.25, 0.55, 0.85, 1.25, 1.5)                         # paketin tikirtilari
CRACK = 0.45                                                # Zoe'nin kagida bastigi an
EYES_OPEN = 1.0                                             # 'crack' icinde gozlerin acildigi an
CRASH = 0.75                                                # 'crash' icinde kulenin yere vurdugu an

# ---- efekt ve fon plani ----
DM = [73.42, 110.0, 146.83, 174.61]
AM = [110.0, 164.81, 220.0, 261.63]
CM = [130.81, 196.0, 261.63, 329.63]
LOW = [69.30, 103.83, 138.59, 164.81]
LOW2 = [61.74, 92.50, 123.47, 146.83]


def mix_plan(T):
    B, S, L, tot = T['beats'], T['scenes'], {l['id']: l for l in T['lines']}, T['total']
    fr = lambda i, f: L[i]['start'] + (L[i]['end'] - L[i]['start']) * f
    pads = [(S[1], S[2], LOW, 1.0), (S[2], B['ding'][0], CM, 0.55), (B['ding'][0], S[3], DM, 0.9),
            (S[3], S[4], LOW2, 0.8), (S[4], S[5], LOW, 0.9), (S[5], B['taken'][0], LOW2, 1.0), (B['taken'][0], S[6], LOW, 1.35),
            (S[6], S[7], AM, 0.85), (S[7], tot, DM, 1.0)]
    fx = []
    tk = lambda t0, g=0.6: [fx.append(('tick', t0 + o, g, dict(f=2300 if i % 2 else 1900))) for i, o in enumerate(TIK)]
    steps = lambda a, b, g=0.22, rate=1.7: fx.append(('steps', a, g, dict(d=max(0.3, b - a), rate=rate)))
    # 1: kanca
    steps(B['open'][0] + 0.1, B['tik0'][0], 0.2)
    tk(B['tik0'][0])
    fx.append(('hum', B['tik0'][0] + 1.0, 0.3, dict(d=L['n2']['end'] - B['tik0'][0] - 0.6)))
    for i in range(4): fx.append(('tick', fr('n2', 0.15 + 0.2 * i), 0.4, dict(f=2100)))
    fx.append(('chime', B['title'][0] + 0.1, 0.6, dict(freqs=[277.18, 415.3, 554.37])))
    # 2: asansor
    lg = B['lights'][0]
    for o in (0.15, 0.45, 0.7): fx.append(('buzz', lg + o, 0.4, dict(d=0.16)))
    fg = B['fingers'][0]
    for i in range(4): fx.append(('tick', fg + 0.35 + i * 0.22, 0.35, dict(f=900 + 90 * i)))
    dg = B['ding'][0]
    fx.append(('rumble', L['l1']['start'] + 0.2, 0.25, dict(d=1.4)))
    fx.append(('ding', dg + 0.15, 0.7, {}))
    fx.append(('slide', dg + 0.6, 0.5, dict(d=1.6)))
    hs = B['hush'][0]
    fx.append(('hum', L['v3']['start'] - 0.2, 0.3, dict(d=L['v3']['end'] - L['v3']['start'] + 0.5)))
    fx.append(('whoosh', hs + 0.1, 0.35, dict(d=0.7, up=False)))
    for o in (0.35, 0.5, 0.62): fx.append(('tick', hs + o, 0.3, dict(f=420)))                       # eller agizlara
    # 3: arsiv
    steps(B['out'][0] + 0.3, B['crack'][0] + CRACK - 0.1)
    ck = B['crack'][0] + CRACK
    fx.append(('snap', ck, 0.9, {}))
    fx.append(('hum', B['crack'][0] + EYES_OPEN, 0.45, dict(d=B['wait'][1] - B['crack'][0] - EYES_OPEN)))
    fx.append(('buzz', B['crack'][0] + EYES_OPEN + 0.05, 0.3, dict(d=0.25)))
    wr = B['write'][0]
    for i in range(9): fx.append(('tick', wr + 0.45 + i * 0.13, 0.2, dict(f=2600 + 200 * (i % 3))))  # kalem
    fx.append(('chime', wr + 1.85, 0.25, dict(freqs=[880.0, 1318.5], d=0.8)))
    # 4: sayim ve paket
    steps(B['walk2'][0] + 0.1, B['tik'][0] - 0.1)
    c0, c1 = B['count']
    for i in range(4): fx.append(('tick', c0 + 0.25 + i * (c1 - c0 - 0.5) / 4, 0.4, dict(f=900 + 90 * i)))
    fx.append(('buzz', fr('n9', 0.5), 0.4, dict(d=0.3)))
    tk(B['tik'][0])
    for i in range(3): fx.append(('tick', fr('n10', 0.1 + 0.16 * i), 0.5, dict(f=2100)))
    hg = B['hug'][0]
    for i, o in enumerate((0.2, 0.5, 0.8)): fx.append(('tick', hg + o, 0.4 - 0.1 * i, dict(f=1500)))  # bogulan tikirti
    fx.append(('hum', hg + 0.6, 0.45, dict(d=L['n11']['end'] - hg - 0.4)))
    ak = B['ask'][0]
    for i in range(8): fx.append(('tick', ak + 0.4 + i * 0.13, 0.2, dict(f=2600 + 200 * (i % 3))))
    fx.append(('chime', ak + 1.7, 0.25, dict(freqs=[880.0, 1318.5], d=0.8)))
    # 5: kule
    steps(B['lean'][0] + 0.1, fr('n13', 0.4))
    for o in (0.9, 1.7): fx.append(('slide', B['lean'][0] + o, 0.3, dict(d=0.5)))                    # kule gicirdar
    fx.append(('slide', fr('n13', 0.55), 0.4, dict(d=0.9)))
    wv = B['wave'][0]
    for i in range(4): fx.append(('whoosh', wv + 0.2 + i * 0.45, 0.22, dict(d=0.35, up=i % 2 == 0)))  # kollar havayi doverken
    fx.append(('slide', B['think'][0] + 0.3, 0.45, dict(d=1.0)))
    cr = B['crash'][0]
    fx.append(('steps', cr - 0.3, 0.8, dict(d=0.9, rate=7.0)))                                     # Luna kosar
    fx.append(('rumble', cr + CRASH - 0.15, 1.0, dict(d=2.0)))
    fx.append(('snap', cr + CRASH, 0.8, {}))
    tkn = B['taken'][0]
    for i, o in enumerate((0.2, 0.6, 1.0)): fx.append(('buzz', tkn + o, 0.45, dict(d=0.2)))          # lambalar sirayla soner
    fx.append(('hum', tkn + 0.9, 0.6, dict(d=2.6)))
    fx.append(('whoosh', tkn + 1.9, 0.7, dict(d=1.5, up=True)))
    fx.append(('snap', tkn + 3.3, 0.5, {}))
    fx.append(('tick', B['hush2'][0] + 0.75, 0.5, dict(f=420)))                                     # Zoe'nin eli
    fx.append(('hum', L['v4']['start'] - 0.2, 0.4, dict(d=L['v4']['end'] - L['v4']['start'] + 1.0)))
    br = B['beret'][0]
    fx.append(('tick', br + 0.15, 0.4, dict(f=300)))
    fx.append(('slide', br + 0.3, 0.2, dict(d=0.9)))
    # 6: asansor
    od = B['door'][0]
    steps(od, od + 0.9, 0.3, 2.4)
    fx.append(('tick', od + 1.0, 0.5, dict(f=700)))
    fx.append(('slide', od + 1.2, 0.5, dict(d=1.1)))
    fx.append(('ding', od + 2.0, 0.6, {}))
    fx.append(('slide', B['inside'][0] + 0.15, 0.5, dict(d=1.0)))
    fx.append(('hum', L['v5']['start'] - 0.2, 0.35, dict(d=L['v5']['end'] - L['v5']['start'] + 0.6)))
    fx.append(('rumble', B['rise'][0], 0.2, dict(d=1.2)))
    fx.append(('ding', B['rise'][0] + 0.7, 0.55, {}))
    pn = B['panel'][0]
    fx.append(('whoosh', pn + 0.5, 0.3, dict(d=0.6, up=True)))
    fx.append(('buzz', pn + 1.5, 0.45, dict(d=0.4)))                                                # bos yuva
    fx.append(('tick', fr('n17', 0.75), 0.4, dict(f=600))); fx.append(('tick', fr('n17', 0.85), 0.4, dict(f=500)))
    fx.append(('buzz', fr('n17b', 0.5), 0.5, dict(d=0.5)))
    fx.append(('chime', B['end'][0], 0.55, dict(freqs=[277.18, 415.3], d=2.4)))
    for t0 in [L[i]['start'] + o for i, o in ABONE] + [S[7] + ABONE_END]:                           # abone ol: tik + kisa zil
        fx.append(('tick', t0 + 2.3, 0.5, dict(f=1200))); fx.append(('chime', t0 + 2.45, 0.32, dict(freqs=[1318.5, 1760.0], d=1.0)))
    return dict(pads=pads, fx=fx)
