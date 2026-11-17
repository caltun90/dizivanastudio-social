"""13. Kat, 3. Bolum: Ayna. Senaryo, ses gruplari, efekt plani.

Yapi: TEK KARAKTERIN GOZUNDEN. Anlatici yok; bolumu Zoe'nin ic sesi anlatir (birinci tekil). Zoe yalnizca kendi
gordugunu ve dusundugunu soyler. Aynaya baktiktan sonra da ic ses surer: artik camin obur tarafindan izler.
Konusanlar: I Zoe'nin ic sesi, Z Zoe (yuksek sesle), L Leo, U Luna, V asansorun sesi
"""
TITLE = '13. KAT'
EP = '3. BÖLÜM'
EP_NAME = 'Ayna'

SEQ = [
    # ---- 1: kanca (ileriden bir an: su birikintisi) ----
    ('scene', 1),
    ('beat', 'open', 0.5),
    ('line', 'i1', 'I', 'Ben doktorum. Yalnızca gözümle gördüğüme inanırım.', ['gördüğüme'], 0.2),
    ('beat', 'pool0', 1.5),                                   # yakin plan: su, iki yansima
    ('line', 'i2', 'I', 'O gün suya baktım. Üç kişiydik. Suda iki kişi vardı.', ['iki', 'kişi'], 0.4),
    ('beat', 'title', 2.5),

    # ---- 2: asansor (hatirlatma, suphe, kural) ----
    ('scene', 2),
    ('beat', 'dark', 0.5),
    ('line', 'i3', 'I', 'Önceki bölümde Sam on dördüncü katta kaldı. Ondan önce de Kai.', ['Sam', 'Kai.'], 0.2),
    ('beat', 'lights', 0.9),                                  # isiklar geri gelir
    ('line', 'i4', 'I', 'Dört kişi binmiştik. İki kişi gitti. Ama hâlâ üç kişiyiz.', ['üç', 'kişiyiz.'], 0.3),
    ('line', 'i5', 'I', 'Biri fazla. Ya Leo, ya Luna.', ['fazla.'], 0.3),
    ('line', 'z1', 'Z', 'Luna, lobide doğru saydığına emin misin?', [], 0.3),
    ('line', 'u1', 'U', 'Eminim. Ben hiç yanlış saymam.', ['hiç'], 0.1),
    ('beat', 'ding', 2.0),                                    # kapi acilir: aynali salon
    ('line', 'v1', 'V', 'On beşinci kata hoş geldiniz. Bu katın tek bir kuralı var: aynaya bakmayın.', ['aynaya', 'bakmayın.'], 0.3),
    ('line', 'l1', 'L', 'Ama her yer ayna!', ['her', 'yer'], 0.3),
    ('line', 'v2', 'V', 'Kuralı bozan, katta kalır.', ['katta', 'kalır.'], 0.3),
    ('line', 'u2', 'U', 'Yere bakın. Yerde ayna yok.', ['Yere'], 0.3),
    ('line', 'i6', 'I', 'Bu çocuk her kuralı bizden önce çözüyor.', [], 0.3),
    ('line', 'l2', 'L', 'Çıkış orada. Yine kırmızı kapı.', ['kırmızı'], 0.3),
    ('line', 'v3', 'V', 'Kural, şimdi başlıyor.', ['şimdi'], 0.1),
    ('beat', 'down', 1.5),                                    # herkes basini egip yere bakar

    # ---- 3: aynali salon: yere bakarak yuruyus, camin icindeki ----
    ('scene', 3),
    ('beat', 'out', 1.0),
    ('line', 'i7', 'I', 'Yere bakarak yürüdük. Aynalar karanlıktı. İçlerinde biz yoktuk.', ['biz', 'yoktuk.'], 0.1),
    ('beat', 'follow', 2.4),                                  # arkalarindaki aynada karalti belirir, onlarla yurur
    ('line', 'i8', 'I', 'Ama camın içinden ayak sesi geliyordu. Bizimle yürüyordu.', ['ayak', 'sesi'], 0.1),
    ('beat', 'knock', 2.2),                                   # cama iceriden vurulur: TAK TAK. Leo basini kaldiracak olur
    ('line', 'z2', 'Z', 'Bakma Leo. Yere bak.', ['Bakma'], 0.3),
    ('line', 'i9', 'I', 'Yüzlerini göremiyordum. O yüzden sordum.', ['sordum.'], 0.4),

    # ---- 4: sorgu ----
    ('scene', 4),
    ('beat', 'ask', 0.6),
    ('line', 'z3', 'Z', 'Leo, sen asansöre ne zaman bindin?', ['ne', 'zaman'], 0.3),
    ('line', 'l3', 'L', 'Sizinle. Lobide... Sanırım.', [], 0.3),
    ('line', 'z4', 'Z', 'Lobide seni görmedim. Seni ilk kez asansörün içinde gördüm.', ['asansörün', 'içinde'], 0.1),
    ('beat', 'think', 1.8),                                   # Leo durur, hatirlamaya calisir
    ('line', 'l4', 'L', 'Ben... lobiyi hatırlamıyorum.', ['hatırlamıyorum.'], 0.3),
    ('line', 'i10', 'I', 'Hatırlamıyor. Ya da söylemiyor.', [], 0.2),
    ('beat', 'turnu', 0.8),                                   # Zoe Luna'ya doner; yeniden yururler
    ('line', 'z5', 'Z', 'Luna, annen hangi katta?', [], 0.3),
    ('line', 'u3', 'U', 'Bilmiyorum. Bir yıldır yukarıda bekliyor.', ['Bir', 'yıldır'], 0.3),
    ('line', 'i11', 'I', 'Bir yıl mı? Bu çocuk buraya ilk kez gelmiyor.', ['ilk', 'kez'], 0.1),
    ('beat', 'drip', 1.6),                                    # tavandan damla duser: SIP

    # ---- 5: su birikintisi, ayna ----
    ('scene', 5),
    ('beat', 'stop', 0.6),
    ('line', 'i12', 'I', 'Tavan damlatıyordu. Yerde bir su birikintisi vardı.', ['su', 'birikintisi'], 0.2),
    ('line', 'i13', 'I', 'Kural ayna demişti. Su dememişti.', ['Su'], 0.1),
    ('beat', 'lookw', 2.4),                                   # Zoe suya egilir; yakin plan
    ('line', 'i14', 'I', 'Suyun başında üç kişiydik. Suda iki yansıma vardı.', ['iki', 'yansıma'], 0.1),
    ('beat', 'ripple', 1.8),                                  # damla duser, su dalgalanir
    ('line', 'i15', 'I', 'Biri benimdi. Öbürü kimindi? Su dalgalıydı, seçemedim.', ['kimindi?'], 0.3),
    ('line', 'i16', 'I', 'Bir doktor, emin olmadan karar vermez. Başımı kaldırdım.', ['Başımı', 'kaldırdım.'], 0.0),
    ('beat', 'raise', 1.8),                                   # Zoe dogrulur, basini aynaya kaldirir
    ('line', 'l5', 'L', 'Zoe, hayır! Bakma!', ['Bakma!'], 0.0),
    ('beat', 'see', 3.0),                                     # ayna aydinlanir; Zoe'nin yuzu
    ('line', 'z6', 'Z', 'Leo... sen...', ['sen...'], 0.0),
    ('beat', 'taken', 3.6),                                   # isiklar titrer, karalti Zoe'yi camin icine ceker
    ('line', 'v4', 'V', 'İki kişi kaldınız.', ['İki'], 0.3),

    # ---- 6: camin obur tarafindan ----
    ('scene', 6),
    ('beat', 'glass', 1.8),                                   # Zoe'nin elleri camda; disarida Leo ve Luna
    ('line', 'i17', 'I', 'Camın öbür tarafındaydım. Bağırdım. Beni duymadılar.', ['duymadılar.'], 0.1),
    ('beat', 'pick', 2.0),                                    # Leo yerdeki gozlugu alir
    ('line', 'u4', 'U', 'Leo. Zoe aynada ne gördü?', ['ne', 'gördü?'], 0.3),
    ('line', 'l6', 'L', 'Bilmiyorum. Ama bana bakıyordu.', ['bana'], 0.1),
    ('beat', 'leave', 3.4),                                   # kirmizi kapiya yururler; kapi acilir: yine asansor
    ('line', 'v5', 'V', 'Kurala uydunuz. Sıradaki kat: on altı.', ['on', 'altı.'], 0.2),
    ('line', 'i18', 'I', 'Dört kişi binmiştik. Üç kişi gitti.', ['Üç', 'kişi'], 0.3),
    ('line', 'i19', 'I', 'Ama o kapıdan iki kişi geçti.', ['iki', 'kişi'], 0.7),

    # ---- 7: bitis ----
    ('scene', 7),
    ('beat', 'endin', 0.5),
    ('line', 'i20', 'I', 'Sence ben aynada ne gördüm? Devamı, bir sonraki bölümde.', ['bir', 'sonraki', 'bölümde.'], 0.3),
    ('beat', 'end', 3.4),
]

# ---- seslendirme: her grup TEK istek, en fazla 2 ses; grup icinde konusanlar sirayla degisir ----
VOICES = {'I': 'Aoede', 'Z': 'Aoede', 'V': 'Kore', 'L': 'Puck', 'U': 'Leda'}
NAMES = {'V': 'Asansor', 'L': 'Leo', 'Z': 'Zoe', 'U': 'Luna'}
_IC = ('Bir gerilim dizisinde genç bir kadın doktorun iç sesi gibi oku: alçak, düşünceli, kendi kendine konuşur gibi, '
       'sakin ama tedirgin; akıcı bir Türkçe ile. Çok yavaşlama. Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:')
GROUPS = {
    'ia': dict(ids=['i1', 'i2', 'i3', 'i4', 'i5', 'i6'], style=_IC),
    'ib': dict(ids=['i7', 'i8', 'i9', 'i10'], style=_IC),
    'id': dict(ids=['i11', 'i12', 'i13'], style=_IC),            # ib'nin sonu gurultulu cikti: bu uc replik ayri istekle yeniden uretildi
    'ic': dict(ids=['i14', 'i15', 'i16', 'i17', 'i18', 'i19', 'i20'], style=_IC),
    'zl': dict(ids=['z1', 'l1', 'z2', 'l2', 'z3', 'l3', 'z4', 'l4', 'z5', 'l5', 'z6', 'l6'],
               style='Türkçe bir gerilim çizgi dizisinden replikler seslendir. '
                     'Zoe genç bir kadın, doktor: zeki, net, şüpheci, sorgular gibi; son repliğinde şaşkın ve korkmuş, cümlesi yarıda kalıyor. '
                     'Leo genç bir kurye: samimi, tedirgin, kısa konuşuyor; kararsız ve şaşkın; beşinci repliğinde telaşla bağırıyor; son repliğinde üzgün ve alçak sesle ama net, tane tane. '
                     'Her replikten sonra bir saniye dur.'),
    'vu': dict(ids=['v1', 'u1', 'v2', 'u2', 'v3', 'u3', 'v4', 'u4', 'v5'],
               style='Türkçe bir gerilim çizgi dizisinden replikler seslendir. '
                     'Asansor bir asansörün anons sesi: kadın, çok sakin, duygusuz, tane tane ve soğuk. '
                     'Luna küçük bir kız çocuğu: ince sesli, tuhaf biçimde sakin ve kendinden emin. '
                     'Her replikten sonra bir saniye dur.'),
}

GAP_SCALE = 1.0                                            # replik arasi bosluklar
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {}
# Luna daha ince ve hizli (cocuk), Zoe'nin yuksek sesi biraz daha kalin (ic sesten ayrilsin), asansor anons hoparlorunden
VOICE_FX = {'U': dict(rate=1.14), 'Z': dict(rate=0.95), 'V': dict(intercom=True)}
TEMPO = {'*': 1.0}

# abone ol bandi: (replik_id, saniye). Bitis sahnesindeki ikinci band bolum.py icinde.
ABONE = [('z1', 0.0)]
ABONE_END = 1.0                                             # son sahne basladiktan kac sn sonra

# ---- cizim ve sesin ortak kullandigi zamanlar (vurus basina gore saniye) ----
KNOCK = (0.35, 0.62, 1.05)                                  # cama vurus anlari ('knock' icinde)
DRIP = 0.85                                                 # 'drip' icinde damlanin suya degdigi an
DROP2 = 0.45                                                # 'ripple' icinde ikinci damla
GLOW = 0.5                                                  # 'see' icinde aynanin aydinlandigi an
FALL = 2.6                                                 # 'taken' icinde gozlugun yere dustugu an

# ---- efekt ve fon plani ----
DM = [73.42, 110.0, 146.83, 174.61]
AM = [110.0, 164.81, 220.0, 261.63]
CM = [130.81, 196.0, 261.63, 329.63]
LOW = [69.30, 103.83, 138.59, 164.81]
LOW2 = [61.74, 92.50, 123.47, 146.83]
GLS = [311.13, 466.16, 622.25, 932.33]                      # cam gibi ince, soguk akor


def mix_plan(T):
    B, S, L, tot = T['beats'], T['scenes'], {l['id']: l for l in T['lines']}, T['total']
    fr = lambda i, f: L[i]['start'] + (L[i]['end'] - L[i]['start']) * f
    pads = [(S[1], S[2], LOW, 1.0), (S[2], B['ding'][0], CM, 0.55), (B['ding'][0], S[3], DM, 0.9),
            (S[3], S[4], LOW2, 0.85), (S[4], S[5], AM, 0.7), (S[5], B['raise'][0], LOW, 0.95), (B['raise'][0], S[6], LOW2, 1.35),
            (S[6], S[7], GLS, 0.5), (S[6], S[7], DM, 0.8), (S[7], tot, DM, 1.0)]
    fx = []
    steps = lambda a, b, g=0.22, rate=1.7: fx.append(('steps', a, g, dict(d=max(0.3, b - a), rate=rate)))
    drop = lambda t0, g=0.55: (fx.append(('tick', t0, g, dict(f=1250))), fx.append(('tick', t0 + 0.07, g * 0.7, dict(f=820))),
                               fx.append(('chime', t0 + 0.05, 0.16, dict(freqs=[1568.0, 2093.0], d=0.7))))
    # 1: kanca
    steps(B['open'][0] + 0.1, fr('i1', 0.55), 0.2)
    drop(fr('i1', 0.75), 0.4)
    drop(B['pool0'][0] + 0.25)
    fx.append(('hum', B['pool0'][0] + 0.5, 0.3, dict(d=L['i2']['end'] - B['pool0'][0])))
    fx.append(('buzz', fr('i2', 0.78), 0.4, dict(d=0.3)))
    fx.append(('chime', B['title'][0] + 0.1, 0.6, dict(freqs=[311.13, 466.16, 622.25])))
    # 2: asansor
    lg = B['lights'][0]
    for o in (0.1, 0.4, 0.62): fx.append(('buzz', lg + o, 0.4, dict(d=0.16)))
    fx.append(('tick', fr('i4', 0.38), 0.4, dict(f=600))); fx.append(('tick', fr('i4', 0.50), 0.4, dict(f=500)))
    fx.append(('buzz', fr('i4', 0.8), 0.4, dict(d=0.3)))
    for f_ in (0.45, 0.8): fx.append(('tick', fr('i5', f_), 0.35, dict(f=1000)))
    dg = B['ding'][0]
    fx.append(('rumble', L['u1']['start'] + 0.2, 0.25, dict(d=1.4)))
    fx.append(('ding', dg + 0.15, 0.7, {}))
    fx.append(('slide', dg + 0.6, 0.5, dict(d=1.5)))
    fx.append(('chime', dg + 1.2, 0.3, dict(freqs=GLS, d=1.6)))                                     # aynalar
    fx.append(('chime', L['l2']['start'] + 0.3, 0.2, dict(freqs=[880.0, 1318.5], d=0.8)))
    fx.append(('hum', L['v3']['start'] - 0.2, 0.3, dict(d=L['v3']['end'] - L['v3']['start'] + 0.5)))
    fx.append(('whoosh', B['down'][0] + 0.1, 0.3, dict(d=0.7, up=False)))
    # 3: salon
    steps(B['out'][0] + 0.3, B['knock'][0] + KNOCK[0] - 0.1)
    fo = B['follow'][0]
    fx.append(('hum', fo + 0.2, 0.4, dict(d=B['knock'][0] - fo)))
    fx.append(('steps', fo + 0.35, 0.5, dict(d=max(0.5, B['knock'][0] - fo - 0.2), rate=1.7)))        # camin icindeki adimlar (yanki gibi, yarim vurus geride)
    for i, o in enumerate(KNOCK):
        fx.append(('tick', B['knock'][0] + o, 0.85, dict(f=520))); fx.append(('snap', B['knock'][0] + o, 0.3, {}))
    fx.append(('hum', B['knock'][0] + 0.3, 0.4, dict(d=L['z2']['end'] - B['knock'][0])))
    # 4: sorgu
    fx.append(('tick', B['think'][0] + 0.2, 0.3, dict(f=420)))
    fx.append(('hum', B['think'][0] + 0.2, 0.3, dict(d=1.6)))
    fx.append(('chime', B['think'][0] + 0.75, 0.22, dict(freqs=[415.3, 554.37], d=1.2)))             # bos dusunce balonu
    steps(B['turnu'][0] + 0.2, B['drip'][0] + DRIP - 0.1)
    drop(B['drip'][0] + DRIP)
    # 5: su ve ayna
    drop(fr('i12', 0.3), 0.4)
    drop(fr('i13', 0.9), 0.35)
    lw = B['lookw'][0]
    fx.append(('whoosh', lw + 0.9, 0.3, dict(d=0.6, up=False)))
    drop(lw + 1.5, 0.45)
    fx.append(('hum', lw + 1.0, 0.35, dict(d=L['i15']['end'] - lw - 0.8)))
    fx.append(('buzz', fr('i14', 0.8), 0.35, dict(d=0.3)))
    drop(B['ripple'][0] + DROP2, 0.6)
    fx.append(('slide', B['ripple'][0] + DROP2 + 0.1, 0.2, dict(d=0.9)))
    rs = B['raise'][0]
    fx.append(('whoosh', rs + 0.2, 0.4, dict(d=1.1, up=True)))
    se = B['see'][0]
    fx.append(('chime', se + GLOW, 0.6, dict(freqs=GLS, d=2.6)))
    fx.append(('hum', se + GLOW, 0.5, dict(d=B['taken'][0] - se)))
    fx.append(('buzz', se + GLOW + 0.05, 0.3, dict(d=0.25)))
    tk = B['taken'][0]
    for o in (0.15, 0.5, 0.85): fx.append(('buzz', tk + o, 0.45, dict(d=0.2)))
    fx.append(('hum', tk + 0.6, 0.6, dict(d=2.4)))
    fx.append(('whoosh', tk + 1.2, 0.7, dict(d=1.1, up=True)))
    fx.append(('tick', tk + FALL, 0.7, dict(f=2400))); fx.append(('tick', tk + FALL + 0.16, 0.4, dict(f=2100)))   # gozluk yere duser
    fx.append(('snap', tk + 2.25, 0.4, {}))
    fx.append(('hum', L['v4']['start'] - 0.2, 0.4, dict(d=L['v4']['end'] - L['v4']['start'] + 1.0)))
    # 6: camin ardindan
    gl = B['glass'][0]
    for o in (0.35, 0.6, 0.95, 1.2): fx.append(('tick', gl + o, 0.45, dict(f=300)))                  # Zoe cama vurur (boguk)
    fx.append(('hum', gl + 0.2, 0.3, dict(d=L['i17']['end'] - gl)))
    pk = B['pick'][0]
    fx.append(('tick', pk + 1.0, 0.35, dict(f=2200)))
    lv = B['leave'][0]
    steps(L['l6']['end'] - 0.3, lv + 2.0, 0.28, 2.2)
    fx.append(('tick', lv + 2.05, 0.5, dict(f=700)))
    fx.append(('slide', lv + 2.15, 0.5, dict(d=1.0)))
    fx.append(('ding', lv + 2.9, 0.5, {}))
    fx.append(('hum', L['v5']['start'] - 0.2, 0.3, dict(d=L['v5']['end'] - L['v5']['start'] + 0.6)))
    fx.append(('slide', L['v5']['end'] + 0.1, 0.4, dict(d=0.9)))
    fx.append(('tick', fr('i18', 0.8), 0.4, dict(f=500)))
    fx.append(('buzz', fr('i19', 0.6), 0.5, dict(d=0.5)))
    fx.append(('chime', B['end'][0], 0.55, dict(freqs=[311.13, 466.16], d=2.4)))
    for t0 in [L[i]['start'] + o for i, o in ABONE] + [S[7] + ABONE_END]:                           # abone ol: tik + kisa zil
        fx.append(('tick', t0 + 2.3, 0.5, dict(f=1200))); fx.append(('chime', t0 + 2.45, 0.32, dict(freqs=[1318.5, 1760.0], d=1.0)))
    return dict(pads=pads, fx=fx)
