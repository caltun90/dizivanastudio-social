"""dizivanastudio yayin araci.

  DIKEY video  -> Buffer API (YouTube Short olarak yayinlanir). Buffer YouTube'da YALNIZCA Shorts destekler
                  (dikey 9:16 ya da kare); yatay videoyu Buffer'a verme.
  YATAY video  -> YouTube Data API (normal video; ozel yuklenir, verilen saatte herkese acilir).

Anahtarlar YALNIZCA ortam degiskeninden okunur; yoksa (Cem'in bilgisayarinda) Windows Kimlik Bilgisi Yoneticisi'nden:
  BUFFER_API_KEY, YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
Hicbir anahtar ekrana, dosyaya ya da depoya yazilmaz.

  python yayin.py kanal                                   -> Buffer org ve YouTube kanal kimligi
  python yayin.py liste [gun]                             -> Buffer'da son gunlerin planli/gonderilmis gonderileri
  python yayin.py planla <dikey_video_url> <saat_iso> <baslik> <metin_dosyasi>
        -> DIKEY videoyu o saate planlar (saat 'simdi' ise 5 dk sonraya)
  python yayin.py sil <post_id>
  python yayin.py yt-kanal                                -> YouTube API ile kanal ve video sayisi
  python yayin.py yt-yukle <yatay_dosya> <baslik> <metin_dosyasi> <yayin_saati_iso | simdi> [etiketler] [oynatma_listesi_id]
        -> YATAY videoyu yukler. Saat verilirse ozel yuklenir ve o saatte yayinlanir; 'simdi' ise hemen herkese acik.
  python yayin.py yt-durum <video_id>                     -> gizlilik, yayin saati, yukleme durumu
  python yayin.py yt-liste-olustur <ad> <aciklama>        -> oynatma listesi kimligi
  python yayin.py yt-listeye-ekle <oynatma_listesi_id> <video_id>
  python yayin.py yt-bul <baslik_parcasi>                 -> kanaldaki son videolarda basligi arar (video_id)
"""
import os, sys, json, io, urllib.request, urllib.error, urllib.parse, datetime

UA = 'dizivanastudio-otomasyon/1.0'


def secret(name):
    v = os.environ.get(name)
    if v: return v
    try:
        import keyring
        v = keyring.get_password('dizivanastudio', name)
    except Exception:
        v = None
    if not v: raise SystemExit(f'Anahtar yok: {name} (ortam degiskeni olarak ver)')
    return v


# ---------------- Buffer ----------------
def buf(q, v=None):
    req = urllib.request.Request('https://api.buffer.com', data=json.dumps({'query': q, 'variables': v or {}}).encode(),
                                 headers={'Authorization': 'Bearer ' + secret('BUFFER_API_KEY'), 'Content-Type': 'application/json', 'User-Agent': UA})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=90))
    except urllib.error.HTTPError as e:
        raise SystemExit(f'Buffer HTTP {e.code}: {e.read().decode()[:500]}')
    if r.get('errors'): raise SystemExit('Buffer hata: ' + json.dumps(r['errors'], ensure_ascii=False)[:800])
    return r['data']


def buf_channel():
    org = buf('{ account { organizations { id name } } }')['account']['organizations'][0]
    chs = buf('query($o: OrganizationId!) { channels(input: {organizationId: $o}) { id name service } }', {'o': org['id']})['channels']
    yt = [c for c in chs if c['service'] == 'youtube']
    if not yt: raise SystemExit('Buffer hesabinda YouTube kanali yok: ' + json.dumps(chs))
    return org['id'], yt[0]


POST_F = 'id status dueAt sentAt text externalLink error { message }'


def buf_list(days=3):
    org, ch = buf_channel()
    q = ('query($o: OrganizationId!, $c: [ChannelId!]!) { posts(first: 40, input: {organizationId: $o, sort: [], '
         'filter: {channelIds: $c, status: [scheduled, sending, sent, error]}}) { edges { node { %s } } } }' % POST_F)
    nodes = [e['node'] for e in buf(q, {'o': org, 'c': [ch['id']]})['posts']['edges']]
    lim = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).isoformat()
    return [n for n in nodes if (n.get('dueAt') or n.get('sentAt') or '9') >= lim]


def buf_schedule(url, when, title, text):
    org, ch = buf_channel()
    if when == 'simdi': when = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%SZ')
    q = ('mutation($i: CreatePostInput!) { createPost(input: $i) { __typename ... on PostActionSuccess { post { %s } } '
         '... on InvalidInputError { message } ... on LimitReachedError { message } ... on UnexpectedError { message } '
         '... on UnauthorizedError { message } ... on NotFoundError { message } ... on RestProxyError { message } } }' % POST_F)
    inp = dict(channelId=ch['id'], mode='customScheduled', schedulingType='automatic', dueAt=when, text=text, needsApproval=False, tagIds=[],
               assets=[{'video': {'url': url}}],
               metadata={'youtube': dict(title=title[:100], privacy='public', madeForKids=False, categoryId='1', notifySubscribers=True, embeddable=True)})
    r = buf(q, {'i': inp})['createPost']
    if r['__typename'] != 'PostActionSuccess': raise SystemExit('Buffer planlama basarisiz: ' + json.dumps(r, ensure_ascii=False))
    return r['post']


# ---------------- YouTube Data API ----------------
_TOK = {}
def yt_token():
    if 't' not in _TOK:
        body = urllib.parse.urlencode(dict(client_id=secret('YT_CLIENT_ID'), client_secret=secret('YT_CLIENT_SECRET'),
                                           refresh_token=secret('YT_REFRESH_TOKEN'), grant_type='refresh_token')).encode()
        try:
            _TOK['t'] = json.load(urllib.request.urlopen(urllib.request.Request('https://oauth2.googleapis.com/token', data=body)))['access_token']
        except urllib.error.HTTPError as e:
            raise SystemExit(f'YouTube yetki hatasi {e.code}: {e.read().decode()[:300]}')
    return _TOK['t']


def yt(method, path, body=None, params=None):
    url = 'https://www.googleapis.com/youtube/v3/' + path + ('?' + urllib.parse.urlencode(params) if params else '')
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, method=method,
                                 headers={'Authorization': 'Bearer ' + yt_token(), 'Content-Type': 'application/json'})
    try:
        raw = urllib.request.urlopen(req, timeout=120).read()
        return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise SystemExit(f'YouTube API {e.code}: {e.read().decode()[:600]}')


def yt_upload(path, title, text, publish_at=None, playlist=None, tags=None):
    """parcali (resumable) yukleme. publish_at verilirse video ozel yuklenir ve o saatte yayinlanir."""
    status = {'selfDeclaredMadeForKids': False, 'privacyStatus': 'private' if publish_at else 'public'}
    meta = {'snippet': {'title': title[:100], 'description': text, 'categoryId': '1', 'defaultLanguage': 'tr', 'defaultAudioLanguage': 'tr'}, 'status': status}
    if tags: meta['snippet']['tags'] = [t.strip() for t in tags.split(',') if t.strip()]
    if publish_at:                                           # YouTube publishAt'i UTC ister
        dt = datetime.datetime.fromisoformat(publish_at).astimezone(datetime.timezone.utc)
        status['publishAt'] = dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    size = os.path.getsize(path)
    req = urllib.request.Request('https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status', data=json.dumps(meta).encode(), method='POST',
                                 headers={'Authorization': 'Bearer ' + yt_token(), 'Content-Type': 'application/json; charset=UTF-8',
                                          'X-Upload-Content-Type': 'video/mp4', 'X-Upload-Content-Length': str(size)})
    try:
        loc = urllib.request.urlopen(req, timeout=120).headers['Location']
        r = json.load(urllib.request.urlopen(urllib.request.Request(loc, data=open(path, 'rb').read(), method='PUT',
                                                                    headers={'Content-Type': 'video/mp4', 'Content-Length': str(size)}), timeout=1800))
    except urllib.error.HTTPError as e:
        raise SystemExit(f'YouTube yukleme {e.code}: {e.read().decode()[:600]}')
    if playlist: yt('POST', 'playlistItems', {'snippet': {'playlistId': playlist, 'resourceId': {'kind': 'youtube#video', 'videoId': r['id']}}}, {'part': 'snippet'})
    return r


if __name__ == '__main__':
    a = sys.argv[1:]; cmd = a[0] if a else ''
    rd = lambda p: io.open(p, encoding='utf-8').read().strip()
    out = lambda o: print(json.dumps(o, ensure_ascii=False, indent=1))
    if cmd == 'kanal': out(dict(zip(('org', 'kanal'), buf_channel())))
    elif cmd == 'liste': out(buf_list(int(a[1]) if len(a) > 1 else 3))
    elif cmd == 'planla': out(buf_schedule(a[1], a[2], a[3], rd(a[4])))
    elif cmd == 'sil':
        out(buf('mutation($i: DeletePostInput!) { deletePost(input: $i) { __typename } }', {'i': {'id': a[1]}}))
    elif cmd == 'yt-kanal':
        c = yt('GET', 'channels', params={'part': 'snippet,statistics', 'mine': 'true'})['items'][0]
        out({'id': c['id'], 'ad': c['snippet']['title'], 'video': c['statistics'].get('videoCount'), 'abone': c['statistics'].get('subscriberCount')})
    elif cmd == 'yt-yukle':
        r = yt_upload(a[1], a[2], rd(a[3]), None if a[4] in ('simdi', '-') else a[4], a[6] if len(a) > 6 else None, a[5] if len(a) > 5 and a[5] != '-' else None)
        out({'video_id': r['id'], 'adres': 'https://youtu.be/' + r['id'], 'durum': r['status']})
    elif cmd == 'yt-durum':
        v = yt('GET', 'videos', params={'part': 'status,snippet,contentDetails', 'id': a[1]})['items']
        out({'baslik': v[0]['snippet']['title'], 'durum': v[0]['status'], 'sure': v[0]['contentDetails'].get('duration')} if v else {'hata': 'video yok'})
    elif cmd == 'yt-liste-olustur':
        r = yt('POST', 'playlists', {'snippet': {'title': a[1], 'description': a[2], 'defaultLanguage': 'tr'}, 'status': {'privacyStatus': 'public'}}, {'part': 'snippet,status'})
        out({'playlist_id': r['id']})
    elif cmd == 'yt-listeye-ekle':
        yt('POST', 'playlistItems', {'snippet': {'playlistId': a[1], 'resourceId': {'kind': 'youtube#video', 'videoId': a[2]}}}, {'part': 'snippet'}); print('ok')
    elif cmd == 'yt-bul':
        c = yt('GET', 'channels', params={'part': 'contentDetails', 'mine': 'true'})['items'][0]
        up = c['contentDetails']['relatedPlaylists']['uploads']
        its = yt('GET', 'playlistItems', params={'part': 'snippet,status', 'playlistId': up, 'maxResults': 25}).get('items', [])
        out([{'video_id': i['snippet']['resourceId']['videoId'], 'baslik': i['snippet']['title'], 'gizlilik': i['status']['privacyStatus']}
             for i in its if a[1].lower() in i['snippet']['title'].lower()])
    else:
        print(__doc__)
