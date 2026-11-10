# Let's find alternative working YouTube IDs for Jalebi Bai
# and test if there are other songs with single blocked IDs
import urllib.request
import json
import re

candidates = [
    "jURo-_lj9yk", # Double Dhamaal lyrical
    "QYh6mYIJG2Y", # Official video Double Dhamaal
    "gWp0J5vD79U",
    "8B_N7-1v0s0"
]

for c in candidates:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={c}&format=json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"[OK] {c}: {data.get('title')}")
    except Exception as e:
        print(f"[FAIL] {c}: {e}")

