import urllib.request
import json

vid = "jURo-_lj9yk"
url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        print(f"oEmbed response: {data}")
except Exception as e:
    print(f"oEmbed failed for {vid}: {e}")

