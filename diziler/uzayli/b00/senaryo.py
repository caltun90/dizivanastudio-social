"""Kiraci Uzayli, 0. Bolum: DENEME (yayinlanmaz). KOMEDI.md kurallarinin sinamasi: "Karnim zil caliyor" blogu.
Ucluk kurali: zil 1 (Zip kapiya kosar, kimse yok) -> zil 2 (Zip gobege konusur) -> zil 3 (gercek zil: Hugo).
Geri cagirma ve dugme: Hugo gidince karin bir kez daha calar, Zip: "Ben bakmiyorum."
Konusanlar: T Tobi, Z Zip, H Hugo.
"""
import sys
import numpy as np

TITLE = 'KİRACI UZAYLI'
EP = '0. BÖLÜM'
EP_NAME = 'Deneme: Karnım Zil Çalıyor'

SEQ = [
    ('scene', 1),
    ('line', 't1', 'T', 'Karnım zil çalıyor.', ['zil', 'çalıyor.'], 0.1),
    ('beat', 'zil1', 1.15),        # karından kapı zili; göbek sallanır; Zip'in antenleri fırlar, çifte bakış
    ('line', 'z1', 'Z', 'Misafir!', ['Misafir!'], 0.05),
    ('scene', 2),
    ('beat', 'kos1', 1.35),        # Zip kapıya koşar, kapıyı açar
    ('beat', 'bos1', 0.8),         # boş koridor, donma
    ('line', 'z2', 'Z', 'Kimse yok.', ['yok.'], 0.3),
    ('scene', 3),
    ('line', 't2', 'T', 'Zip, o bir deyim. Yani çok acıktım.', ['deyim.', 'acıktım.'], 0.25),
    ('line', 'z3', 'Z', 'Anladım. Zil çalarsa kapıya bakılmaz.', ['bakılmaz.'], 0.35),
    ('beat', 'zil2', 1.3),         # karın yine çalar; Zip kapıya doğru çekilir, direnir, göbeğe döner
    ('line', 'z4', 'Z', 'Evde yokuz! Sonra gelin!', ['yokuz!', 'gelin!'], 0.15),
    ('beat', 'bakis', 0.8),        # Tobi yavaşça Zip'e bakar
    ('line', 't3', 'T', 'Boşuna. Ben yıllardır deniyorum.', ['yıllardır'], 0.35),
    ('beat', 'zil3', 0.95),        # bu kez gerçek kapı zili
    ('line', 'z5', 'Z', 'Yokuz dedik!', ['dedik!'], 0.3),
    ('line', 't4', 'T', 'Zip... o ben değilim.', ['değilim.'], 0.1),
    ('beat', 'donma', 1.3),        # ikisi donar, yavaşça kapıya döner
    ('scene', 4),
    ('beat', 'burun', 1.4),        # kapı açılır; kadrajı önce Hugo'nun burnu doldurur, koklar
    ('line', 'h1', 'H', 'Hımm. Bu kapı bugün üç kez açıldı.', ['üç', 'kez'], 0.2),
    ('beat', 'sakla', 0.8),        # Zip ışık hızıyla Tobi'nin arkasına
    ('line', 'h2', 'H', 'Çilek... ve yıldız tozu.', ['yıldız', 'tozu.'], 0.3),
    ('line', 't5', 'T', 'Cips. Çilekli.', ['Çilekli.'], 0.25),
    ('line', 'h3', 'H', 'Çilekli cips mi olur?', ['olur?'], 0.4),
    ('line', 't6', 'T', 'Olur. Ben yerim.', ['yerim.'], 0.2),
    ('beat', 'anten', 1.6),        # Zip'in anteni Tobi'nin başının üstünden yükselir; Tobi bakmadan, yüzünde hiçbir ifade olmadan boyunu uzatıp antenleri kafasıyla ezer
    ('line', 'h4', 'H', 'Bu burun yanılmaz, Tobi. Yanılmaz.', ['yanılmaz,', 'Yanılmaz.'], 0.2),
    ('beat', 'kapat', 1.1),        # Hugo geri geri çıkar, kapı kapanır, sessizlik
    ('beat', 'zil4', 1.0),         # karın son kez çalar
    ('line', 'z6', 'Z', 'Ben bakmıyorum.', ['bakmıyorum.'], 0.2),
    ('beat', 'end', 1.8),
]
VOICES = {'H': 'Orus', 'T': 'Puck', 'L': 'Aoede', 'Z': 'Fenrir', 'N': 'Achird'}
NAMES = {'H': 'Hugo', 'T': 'Tobi', 'L': 'Luna', 'Z': 'Zip', 'N': 'Anlatici'}
_DIZI = 'Türkçe bir komedi çizgi dizisinden replikler seslendir; olay bir öğrenci evinde geçiyor. Komedi ciddiyetten gelir: kimse bağırmaz, kimse abartmaz, herkes durumu çok ciddiye alır. '
_SON = 'Her replikten sonra bir saniye dur.'
GROUPS = {
    'tz': dict(ids=['t1', 'z1', 'z2', 't2', 'z3', 'z4', 't3', 'z5', 't4', 'z6'],
               style=_DIZI + 'Tobi genç, tombul, iyi kalpli bir aşçılık öğrencisi: ağır, kısa, düz ve uykulu bir sesle, hiç heyecanlanmadan konuşuyor; '
                     '"Boşuna. Ben yıllardır deniyorum." cümlesini kabullenmiş bir iç çekişle söylüyor. Zip küçük, çok kibar bir uzaylı: hevesli, '
                     'tane tane, kendinden emin; "Evde yokuz! Sonra gelin!" ve "Yokuz dedik!" cümlelerini kapıya seslenir gibi ama kibarca, '
                     'son repliği "Ben bakmıyorum." fısıldayarak. ' + _SON),
    'ht': dict(ids=['h1', 'h2', 't5', 'h3', 't6', 'h4'],
               style=_DIZI + 'Hugo yaşlıca, resmi, kuşkucu bir ev sahibi: yavaş, alçak sesle, koklayarak ve şüpheyle konuşuyor; "üç kez" sözünü '
                     'tek tek vurgular. Tobi ağzı doluymuş gibi, ağır, kısa ve tamamen ciddi; "Olur. Ben yerim." cümlesini omuz silker gibi düz söyler. ' + _SON),
}
GAP_SCALE = 1.0
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {}
VOICE_FX = {'Z': dict(rate=1.12)}
TEMPO = {'*': 1.0}
ABONE = []

def mix_plan(T):
    L = {l['id']: l for l in T['lines']}; S = T['scenes']; B = T['beats']; tot = T['total']
    fx = [
        ('ding', B['zil1'][0] + 0.05, 0.9, {}),                         # karından kapı zili
        ('boing', B['zil1'][0] + 0.55, 0.55, dict(d=0.6)),              # Zip'in antenleri
        ('whoosh', B['kos1'][0] + 0.05, 0.6, dict(d=0.5)),              # koşu
        ('slide', B['kos1'][0] + 0.85, 0.35, dict(d=0.5)),              # kapı açılır
        ('ding', B['zil2'][0] + 0.05, 0.9, {}),                         # karın yine
        ('ding', B['zil3'][0] + 0.05, 1.25, {}),                        # gerçek zil (daha yüksek)
        ('whistle_down', B['donma'][0] + 0.15, 0.45, dict(d=0.8)),      # donma
        ('slide', S[4] + 0.05, 0.35, dict(d=0.6)),                      # kapı açılır
        ('sniff', B['burun'][0] + 0.35, 0.7, dict(n=3)),                # Hugo koklar
        ('whoosh', B['sakla'][0] + 0.05, 0.7, dict(d=0.35)),            # Zip saklanır
        ('sniff', L['h2']['start'] - 0.45, 0.6, dict(n=4)),
        ('munch', L['t6']['start'] + 0.05, 0.5, dict(n=4)),
        ('zip', B['anten'][0] + 0.1, 0.5, dict(d=0.6)),                 # anten yükselir
        ('whistle_up', B['anten'][0] + 0.7, 0.45, dict(d=0.35)), ('boing', B['anten'][0] + 1.0, 0.45, dict(d=0.5)),   # Tobi uzar, başı antenleri ezer
        ('steps', B['kapat'][0], 0.4, dict(d=0.8, rate=3.0)),
        ('slide', B['kapat'][0] + 0.45, 0.35, dict(d=0.5)),             # kapı kapanır
        ('ding', B['zil4'][0] + 0.05, 0.8, {}),                         # düğme
    ]
    music = [(0.0, B['zil3'][0], 'komik', 0.85), (B['zil3'][1] + 0.4, B['donma'][0], 'sinsi', 0.6),
             (S[4] + 0.2, B['kapat'][0] + 0.2, 'sinsi', 0.85), (B['end'][0], tot, 'komik', 0.85)]
    return dict(pads=[], fx=fx, music=music)
