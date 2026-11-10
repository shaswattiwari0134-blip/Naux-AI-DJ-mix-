import urllib.request
import json
import re

# Let's search YouTube HTML or oEmbed for alternative Jalebi Bai videos
queries = [
    "jalebi bai audio",
    "jalebi bai song double dhamaal",
    "jalebi bai mallika sherawat"
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

req = urllib.request.Request("https://www.youtube.com/results?search_query=jalebi+bai+song", headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        vids = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', html)
        unique_vids = []
        for v in vids:
            if v not in unique_vids:
                unique_vids.append(v)
        print("Found YouTube IDs for Jalebi Bai:", unique_vids[:8])
        
        # Test them with oEmbed
        for v in unique_vids[:6]:
            try:
                oe_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={v}&format=json"
                req_oe = urllib.request.Request(oe_url, headers=headers)
                with urllib.request.urlopen(req_oe) as oe_resp:
                    data = json.loads(oe_resp.read().decode())
                    print(f"  [OK] {v}: {data.get('title')}")
            except Exception as e:
                print(f"  [FAIL] {v}: {e}")
except Exception as e:
    print(f"Search failed: {e}")

