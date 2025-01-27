Proxy to call yggnode without giving your key to a remote server.

YggNode project : https://github.com/YggNode/yggnode

How to use :
===

```bash
// To get the rss feed from a category
curl <url>/ygg/<category id>

// To download a .torrent
curl <url>/ygg-dl/<torrent id>
```

How to build :
===

From scratch :
---

No .exe sorry

```bash
git clone https://github.com/PurplePlane897/ygg-rss
cd ygg-rss
mkdir -p torrents/tmp
python3 -m pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8192

# You can run it in the background with pm2 :
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8192" -name RssYgg 
```

With docker :
---

Just build and run it
