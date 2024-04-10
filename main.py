import re
import json
import requests
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse

from torrentool.api import Torrent

app = FastAPI()

fake_passkey='Ttw5xQcCbmjHUwC9jCs8fdbrGEnF8yEt'
passkey='<your ygg key>'
my_server='localhost:8192' # change this accordingly to the container name if you use docker

@app.get("/ygg/{cat}")
async def ygg(cat):
    url='https://rss.dathomir.fr/rss?id={cat}&passkey={passkey}'.format(cat=cat, passkey=fake_passkey)
    r=requests.get(url)
    rss=r.text.replace('https://rss.dathomir.fr:443/download?id=', 'http://{server}/ygg-dl/'.format(server=my_server))\
              .replace('&amp;passkey={}'.format(fake_passkey), '')
    return Response(content=rss, headers={'content-type': 'text/xml; charset=utf-8'})

@app.get("/ygg-dl/{id}", response_class=FileResponse)
async def yggdl(id):
    url='https://rss.dathomir.fr:443/download?id={id}&passkey=Ttw5xQcCbmjHUwC9jCs8fdbrGEnF8yEt'.format(id=id)
    r=requests.get(url, stream=True)
    with open(f"torrents/{id}.torrent", "wb") as torrentFile:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                torrentFile.write(chunk)
    
    my_torrent = Torrent.from_file('torrents/{id}.torrent'.format(id=id))
    my_torrent.announce_urls = re.sub(
        "[a-zA-Z0-9]{32}", passkey, ((my_torrent.announce_urls[0])[0]))
    my_torrent.to_file('torrents/tmp/{id}.{passkey}.torrent'.format(id=id, passkey=passkey))

    return 'torrents/tmp/{id}.{passkey}.torrent'.format(id=id, passkey=passkey)
    return send_file('torrents/tmp/{id}{passkey}.torrent'.format(id=id, passkey=passkey),
                     as_attachment=True,
                     attachment_filename=(my_torrent.name + ".torrent"),
                     mimetype='application/x-bittorrent')
