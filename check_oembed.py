import urllib.request
import json

test_ids = [
    ("Tauba Tauba", "uTuchIYZdbM"),
    ("Excuses", "vX2cDW8LUWk"),
    ("Brown Munde", "YBTVJ_jWIGk"),
    ("Lover", "aoIhamvZKdQ"),
    ("High Rated Gabru", "hjWf8A0YNSE")
]

for title, vid in test_ids:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"[OK] {title} ({vid}): {data.get('title')}")
    except Exception as e:
        print(f"[ERR] {title} ({vid}): {e}")

