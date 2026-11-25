"""Kiraci Uzayli, 0. Bolum: DENEME (yayinlanmaz). Yeni hattin (ses.py -> kopru.py -> yumurta motoru) sinamasi.
Kanca: Hugo kapida koklar -> evde Tobi cips yer, Luna susturur -> buzdolabindan Zip firlar -> merdivende Hugo koklar.
Konusanlar: H Hugo, T Tobi, L Luna, Z Zip.
"""
import sys
import numpy as np

TITLE = 'KİRACI UZAYLI'
EP = '0. BÖLÜM'
EP_NAME = 'Deneme'

SEQ = [
    ('scene', 1),
    ('line', 'h1', 'H', 'Burada bir uzay kokusu var!', ['uzay', 'kokusu'], 0.3),
    ('scene', 2),
    ('line', 't1', 'T', 'Koku benim cipsimden geliyor, Bay Hugo!', ['cipsimden'], 0.25),
    ('line', 'l1', 'L', 'Tobi, sessiz ol! Zip buzdolabının içinde.', ['buzdolabının'], 0.2),
    ('scene', 3),
    ('beat', 'pop', 0.9),
    ('line', 'z1', 'Z', 'Kılavuz diyor ki: misafire gülümse!', ['gülümse!'], 0.3),
    ('scene', 4),
    ('line', 'h2', 'H', 'Hmm. Çilek ve yıldız tozu...', ['yıldız', 'tozu...'], 0.6),
    ('beat', 'end', 1.2),
]
VOICES = {'H': 'Orus', 'T': 'Puck', 'L': 'Aoede', 'Z': 'Fenrir', 'N': 'Achird'}
NAMES = {'H': 'Hugo', 'T': 'Tobi', 'L': 'Luna', 'Z': 'Zip', 'N': 'Anlatici'}
_DIZI = 'Türkçe komik bir çizgi diziden replikler seslendir; olay bir öğrenci evinde geçiyor. '
_SON = 'Her replikten sonra bir saniye dur.'
GROUPS = {
    'ht': dict(ids=['h1', 't1', 'h2'],
               style=_DIZI + 'Hugo yaşlıca, kuşkucu bir ev sahibi: burnunu çeke çeke, abartılı ve komik bir ciddiyetle konuşuyor; ilk repliğinde '
                     'şüpheyle ve heyecanla bağırıyor, son repliğinde koklayarak, düşünceli ve yavaş. Tobi genç, tombul, keyifli bir oda arkadaşı: '
                     'ağzı doluymuş gibi, telaşla ama neşeyle, hızlı konuşuyor. ' + _SON),
    'lz': dict(ids=['l1', 'z1'],
               style=_DIZI + 'Luna genç bir üniversiteli kadın: telaşlı, fısıldar gibi ama net ve hızlı. Zip küçük, tatlı bir uzaylı: '
                     'neşeli, robot gibi tane tane ve çok hevesli, bir kuralı ezberden okur gibi. ' + _SON),
}
GAP_SCALE = 1.2
LINES = {it[1]: dict(id=it[1], spk=it[2], text=it[3], hl=it[4], gap=round(it[5] * GAP_SCALE, 2)) for it in SEQ if it[0] == 'line'}
SEG_ALIAS = {}
VOICE_FX = {'Z': dict(rate=1.12)}
TEMPO = {'*': 1.0}
ABONE = []

def mix_plan(T):
    L = {l['id']: l for l in T['lines']}; S = T['scenes']; B = T['beats']; tot = T['total']
    fx = [('knock', 0.0, 0.5, dict(n=3)), ('sniff', L['h1']['end'] + 0.05, 0.4, dict(n=3)),
          ('munch', L['t1']['start'] + 0.1, 0.35, dict(n=4)), ('pop', B['pop'][0] + 0.25, 0.6, {}), ('boing', B['pop'][0] + 0.3, 0.5, dict(d=0.7)),
          ('zip', L['z1']['start'] - 0.2, 0.4, dict(d=0.5)), ('sniff', L['h2']['start'] - 0.5, 0.45, dict(n=4))]
    music = [(0.0, S[3], 'sinsi', 0.9), (S[3], S[4], 'komik', 0.9), (S[4], tot, 'sinsi', 0.8)]
    return dict(pads=[], fx=fx, music=music)
