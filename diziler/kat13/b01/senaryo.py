"""13. Kat, 1. Bolum: Asansor. Senaryo, ses gruplari, efekt plani.

SEQ ogeleri:
  ('scene', no)
  ('beat', ad, sure_sn)                              -> sessiz aksiyon suresi
  ('line', id, konusan, metin, vurgu_kelimeleri, sonraki_bosluk_sn)
Konusanlar: N anlatici, V asansorun sesi, L Leo, Z Zoe, K Kai, U Luna, S Sam
"""
TITLE = '13. KAT'
EP = '1. BÖLÜM'
EP_NAME = 'Asansör'

SEQ = [
    ('scene', 1),
    ('beat', 'open', 0.5),
    ('beat', 'feet', 0.9),
    ('line', 'n1', 'N', 'O akşam asansöre dört kişi bindi.', ['dört', 'kişi'], 0.3),
    ('beat', 'shut', 1.3),
    ('line', 'n2', 'N', 'Ama kapı kapandığında, içeride beş kişi vardı.', ['beş', 'kişi'], 0.4),
    ('line', 'n3', 'N', 'Ve asansör, bu binada olmayan bir katta durdu.', ['olmayan'], 0.5),
    ('beat', 'title', 2.5),

    ('scene', 2),
    ('beat', 'lobby', 1.0),
    ('line', 'n4', 'N', 'Bir dakika önce.', ['Bir', 'dakika', 'önce.'], 0.4),
    ('line', 'k1', 'K', 'Hadi, hadi! Toplantıya geç kalıyorum!', [], 0.3),
    ('line', 's1', 'S', 'Düğmeye on kere basınca daha hızlı gitmiyor evlat.', [], 0.3),
    ('line', 'u1', 'U', 'Ben yedi kere bastım.', [], 0.3),
    ('line', 'z1', 'Z', 'Sen tek başına mısın küçük? Annen nerede?', [], 0.3),
    ('line', 'u1b', 'U', 'Yukarıda. Hep yukarıda bekler.', ['yukarıda'], 0.1),
    ('beat', 'odd', 1.2),
    ('line', 'z1c', 'Z', 'O paket kime?', [], 0.3),
    ('line', 'l1', 'L', 'On üçüncü kata. Ama gönderen yazmıyor.', ['On', 'üçüncü'], 0.3),
    ('line', 'z2', 'Z', 'Bu binada on üçüncü kat yok ki.', ['yok'], 0.3),
    ('line', 'l1b', 'L', 'Biliyorum. Ben de onu soracaktım.', [], 0.1),
    ('beat', 'flick1', 1.5),
    ('line', 's5', 'S', 'Sakin olun. Eski asansör.', [], 0.1),
    ('beat', 'flick2', 2.5),
    ('line', 'l2', 'L', 'O zaman... şu an neredeyiz?', ['neredeyiz?'], 0.6),

    ('scene', 3),
    ('beat', 'doors', 2.6),
    ('line', 'v1', 'V', 'On üçüncü kata hoş geldiniz.', [], 0.4),
    ('line', 'v2', 'V', 'Bu katın tek bir kuralı var. Arkanıza bakmayın.', ['Arkanıza', 'bakmayın.'], 0.4),
    ('line', 'v3', 'V', 'Kuralı bozan, katta kalır.', ['katta', 'kalır.'], 0.35),
    ('line', 'v3b', 'V', 'Kurala uyan, bir üst kata çıkar.', ['üst', 'kata'], 0.5),
    ('line', 'k2', 'K', 'Saçmalık! Bu bir şaka. Ben aşağı iniyorum.', [], 0.1),
    ('beat', 'press', 2.8),                                   # Kai dugmelere basar, hicbiri calismaz
    ('line', 'l3', 'L', 'Düğmeler çalışmıyor. Hiçbiri.', ['Hiçbiri.'], 0.3),
    ('line', 's2', 'S', 'Kırk yıldır bu binada çalışıyorum. Böyle bir kat hiç olmadı.', ['hiç', 'olmadı.'], 0.3),
    ('line', 'z3', 'Z', 'Merdiven de yok. Sadece koridor var.', [], 0.3),
    ('line', 'u2', 'U', 'Kapılar da kapanmıyor. Yürümek zorundayız.', ['Yürümek'], 0.6),

    ('scene', 4),
    ('beat', 'walkin', 1.4),
    ('line', 'n5', 'N', 'Koridorun sonunda kırmızı bir kapı vardı. Yürümeye başladılar.', ['kırmızı'], 0.2),
    ('beat', 'steps', 2.3),
    ('line', 'z4', 'Z', 'Duyuyor musunuz? Arkamızda biri yürüyor.', ['Arkamızda'], 0.3),
    ('line', 'l4', 'L', 'Bakma. Sakın bakma.', ['Sakın', 'bakma.'], 0.3),
    ('line', 's3', 'S', 'Önüne bak kızım.', [], 0.2),
    ('beat', 'ring', 2.3),
    ('line', 'k3', 'K', 'Bu benim telefonum! Arkamda çalıyor!', ['Arkamda'], 0.3),
    ('line', 's4', 'S', 'Dönme evlat. Telefonun cebinde.', ['Dönme'], 0.3),
    ('line', 'k4', 'K', 'Ama toplantı... Bir saniye bakıp...', [], 0.0),
    ('beat', 'turn', 4.1),
    ('line', 'u3', 'U', 'Kai!', ['Kai!'], 0.3),
    ('line', 'z5', 'Z', 'Nereye gitti? Az önce buradaydı!', [], 0.3),
    ('line', 'l5', 'L', 'Bakma Zoe! Yürü!', ['Yürü!'], 0.5),
    ('line', 'v4', 'V', 'Dört kişi kaldınız.', ['Dört'], 0.2),
    ('beat', 'after', 1.2),
    ('beat', 'opendoor', 2.6),                                # Leo kolu tutar, kirmizi kapi acilir
    ('beat', 'shock', 1.6),                                   # once yuzlerdeki sok

    ('scene', 5),
    ('beat', 'back', 0.9),
    ('line', 'n6', 'N', "Kırmızı kapı, yine asansöre açıldı. Kai'den geriye yalnızca kravatı kalmıştı.", ['asansöre', 'kravatı'], 0.2),
    ('beat', 'close', 1.8),
    ('line', 'v5', 'V', 'Kurala uydunuz. Sıradaki kat: on dört.', ['on', 'dört.'], 0.2),
    ('beat', 'rise', 1.6),
    ('line', 'u4', 'U', 'Leo. Sana bir şey söyleyeceğim.', [], 0.3),
    ('line', 'l6', 'L', 'Söyle Luna.', [], 0.3),
    ('line', 'u5', 'U', 'Ben lobide saymıştım. Asansöre dört kişi bindik.', ['dört', 'kişi'], 0.4),
    ('line', 'l7', 'L', 'Evet. Dört kişiyiz zaten.', [], 0.4),
    ('line', 'u6', 'U', 'Ama Kai de bizimle binmişti. Şimdi üç kişi olmamız lazım.', ['üç', 'kişi'], 0.2),
    ('beat', 'count', 3.3),
    ('line', 'n7', 'N', 'Dört kişi bindi. Biri gitti. Geriye üç kişi kalmalıydı.', ['üç', 'kişi'], 0.4),
    ('line', 'n7b', 'N', 'Ama asansörde hâlâ dört kişi var. İçlerinden biri, o asansöre hiç binmedi.', ['dört', 'hiç', 'binmedi.'], 0.7),

    ('scene', 6),
    ('beat', 'endin', 0.5),
    ('line', 'n8', 'N', 'Sence hiç binmeyen kim? Devamı, bir sonraki bölümde.', ['bir', 'sonraki', 'bölümde.'], 0.3),
    ('beat', 'end', 3.0),
]

# ---- seslendirme: her grup TEK istek, en fazla 2 ses; grup icinde konusanlar sirayla degisir ----
# Replikler zaman cizelgesine tek tek yerlestigi icin grup, sahne sirasini izlemek zorunda degil.
VOICES = {'N': 'Achird', 'V': 'Kore', 'L': 'Puck', 'U': 'Leda', 'K': 'Fenrir', 'Z': 'Aoede', 'S': 'Algenib'}
NAMES = {'V': 'Asansor', 'L': 'Leo', 'U': 'Luna', 'K': 'Kai', 'Z': 'Zoe', 'S': 'Sam'}
GROUPS = {
    'narr': dict(ids=['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n7b', 'n8'],
                 style='Gerilim dizisi anlatıcısı gibi, alçak, sakin ve tekinsiz bir tonla, akıcı bir Türkçe ile oku. '
                       'Çok yavaşlama. Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:'),
    'kv': dict(ids=['k1', 'v1', 'k2', 'v2', 'k3', 'v3', 'k4', 'v4'],
               style='Türkçe bir gerilim çizgi dizisinden replikler seslendir. '
                     'Kai sabırsız, kibirli bir iş adamı: hızlı, yüksek sesle, sinirli konuşuyor; son repliklerinde paniğe kapılıyor, son cümlesi yarıda kalıyor. '
                     'Asansor bir asansörün anons sesi: kadın, çok sakin, duygusuz, tane tane ve soğuk. '
                     'Her replikten sonra bir saniye dur.'),
    'vx': dict(ids=['v3b', 'v5'],
               style='Bir asansörün anons sesi gibi oku: kadın, çok sakin, duygusuz, tane tane ve soğuk, akıcı bir Türkçe ile. '
                     'Her paragraftan sonra belirgin biçimde, yaklaşık bir saniye dur:'),
    'sz': dict(ids=['z1', 's1', 'z1c', 's5', 'z2', 's2', 'z3', 's3', 'z4', 's4', 'z5'],
               style='Türkçe bir gerilim çizgi dizisinden replikler seslendir. '
                     'Zoe genç bir kadın, doktor: zeki, net, şüpheci; son repliklerinde korkuyor. '
                     'Sam yaşlı bir bina görevlisi: kalın, yorgun, babacan ve sakin bir ses. '
                     'Her replikten sonra bir saniye dur.'),
    'lu': dict(ids=['l1', 'u1', 'l1b', 'u1b', 'l2', 'u2', 'l3', 'u3', 'l4', 'u4', 'l5', 'u5', 'l6', 'u6', 'l7'],
               style='Türkçe bir gerilim çizgi dizisinden replikler seslendir. '
                     'Leo genç bir kurye: samimi, biraz tedirgin; tehlike anında kısa ve sert konuşuyor. '
                     'Luna küçük bir kız çocuğu: ince sesli, tuhaf biçimde sakin; tek kelimelik çığlığında korku dolu, son repliklerinde fısıltıya yakın. '
                     'Her replikten sonra bir saniye dur.'),
}

GAP_SCALE = 0.75                                            # replik arasi bosluklar (sure 3:00'i gecmesin)
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {}
# sesleri ayristir: Luna daha ince ve hizli (cocuk), Zoe biraz daha kalin (yetiskin), asansor anons hoparlorunden
VOICE_FX = {'U': dict(rate=1.14), 'Z': dict(rate=0.95), 'V': dict(intercom=True)}
# perdeyi bozmadan hizlandirma (ffmpeg atempo): '*' herkes, harf o konusmaci
TEMPO = {'*': 1.0, 'N': 1.04}

# ---- efekt ve fon plani ----
DM = [73.42, 110.0, 146.83, 174.61]
AM = [110.0, 164.81, 220.0, 261.63]
CM = [130.81, 196.0, 261.63, 329.63]
LOW = [69.30, 103.83, 138.59, 164.81]

# abone ol bandi: (replik_id, saniye) -> o replik basladiktan su kadar sonra girer. Bitis sahnesindeki ikinci band bolum.py icinde.
ABONE = [('s1', 0.0)]
ABONE_END = 1.0                                             # son sahne basladiktan kac sn sonra


def feet_plan(feet0, n1_end):
    """lobide asansore giren 4 golge: (baslangic, hiz, [kapiya varis zamanlari]). Cizim ve ses ayni plani kullanir."""
    f0 = feet0 + 0.25; v = (240 + 170 * 3) / max(1.6, n1_end - 0.1 - f0)
    return f0, v, [f0 + (240 + 170 * i) / v for i in range(4)]


def mix_plan(T):
    B, S, L, tot = T['beats'], T['scenes'], {l['id']: l for l in T['lines']}, T['total']
    fr = lambda i, f: L[i]['start'] + (L[i]['end'] - L[i]['start']) * f
    pads = [(S[1], S[2], DM, 1.0), (S[2], B['flick1'][0], CM, 0.6), (B['flick1'][0], S[4], DM, 1.0),
            (S[4], S[5], LOW, 1.25), (S[5], S[6], AM, 0.9), (S[6], tot, DM, 1.0)]
    fx = []
    for t in feet_plan(B['feet'][0], L['n1']['end'])[2]: fx.append(('tick', t, 0.45, dict(f=900)))   # dort kisi biner
    fx.append(('slide', B['shut'][0] + 0.1, 0.5, dict(d=1.1)))
    fx.append(('buzz', fr('n2', 0.62), 0.5, dict(d=0.35)))                                         # besinci
    for i in range(3): fx.append(('tick', fr('n3', 0.1 + 0.2 * i), 0.35, {}))
    fx.append(('ding', fr('n3', 0.7), 0.5, {}))
    fx.append(('buzz', L['n3']['end'] + 0.1, 0.5, dict(d=0.5)))
    fx.append(('chime', B['title'][0] + 0.1, 0.6, dict(freqs=[293.66, 440.0, 587.33])))
    f1, f2 = B['flick1'], B['flick2']
    for t in (f1[0] + 0.2, f1[0] + 0.7, f1[0] + 1.1, f2[0] + 0.2, f2[0] + 0.8, f2[0] + 1.2): fx.append(('buzz', t, 0.45, dict(d=0.18)))
    fx.append(('tick', f1[0] + 1.0, 0.4, {})); fx.append(('rumble', f2[0] + 0.3, 0.35, dict(d=1.6)))
    fx.append(('ding', f2[0] + 2.0, 0.8, {}))
    fx.append(('slide', B['doors'][0] + 0.4, 0.5, dict(d=1.8)))
    pr = B['press'][0]
    for i in range(4):                                                                             # dugmeye basar: tik + olumsuz vizilti
        fx.append(('tick', pr + 0.45 + i * 0.5, 0.5, dict(f=1400))); fx.append(('buzz', pr + 0.55 + i * 0.5, 0.4, dict(d=0.14)))
    st = B['steps']
    fx.append(('steps', st[0] + 0.4, 0.55, dict(d=L['s3']['end'] - st[0], rate=1.5)))
    rg = B['ring']
    fx.append(('ring', rg[0] + 0.3, 0.4, dict(d=rg[1] - rg[0] - 0.4)))
    fx.append(('ring', L['k3']['end'] + 0.1, 0.22, dict(d=L['k4']['start'] - L['k3']['end'] - 0.2)))
    tn = B['turn']
    fx.append(('steps', tn[0] + 0.2, 0.9, dict(d=1.0, rate=6.0)))
    fx.append(('whoosh', tn[0] + 1.4, 0.7, dict(d=1.6, up=True)))
    fx.append(('snap', tn[0] + 3.0, 0.6, {}))
    fx.append(('hum', L['v4']['start'] - 0.2, 0.4, dict(d=L['v4']['end'] - L['v4']['start'] + 1.2)))
    od = B['opendoor'][0]
    fx.append(('tick', od + 0.6, 0.5, dict(f=700)))                                                 # kapi kolu
    fx.append(('slide', od + 0.8, 0.5, dict(d=1.2)))                                                # kapi acilir
    fx.append(('ding', od + 1.9, 0.7, {}))                                                          # icerisi yine asansor
    fx.append(('slide', B['close'][0] + 0.2, 0.5, dict(d=1.3)))
    fx.append(('hum', L['v5']['start'] - 0.2, 0.35, dict(d=L['v5']['end'] - L['v5']['start'] + 0.6)))
    fx.append(('rumble', B['rise'][0], 0.2, dict(d=1.2)))
    fx.append(('ding', B['rise'][0] + 0.6, 0.6, {}))
    c0, c1 = B['count']
    for i in range(4): fx.append(('tick', c0 + 0.3 + i * (c1 - c0 - 0.4) / 4, 0.4, dict(f=900)))
    fx.append(('buzz', fr('n7b', 0.5), 0.5, dict(d=0.5)))
    fx.append(('chime', B['end'][0], 0.55, dict(freqs=[293.66, 440.0], d=2.4)))
    for t0 in [L[i]['start'] + o for i, o in ABONE] + [S[6] + ABONE_END]:                           # abone ol: tik + kisa zil
        fx.append(('tick', t0 + 2.3, 0.5, dict(f=1200))); fx.append(('chime', t0 + 2.45, 0.32, dict(freqs=[1318.5, 1760.0], d=1.0)))
    return dict(pads=pads, fx=fx)
