import os
import re
import json

with open(os.path.join("naux_analysis", "1vakelacxrphe.js"), "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Find all occurrences of {"song_id":...}
pattern = r'(\{"song_id":"[^"]+?".*?"versions_checked":true\})'
matches = re.findall(pattern, content)
print(f"Extracted {len(matches)} complete song records")

songs = []
for m in matches:
    try:
        s = json.loads(m)
        songs.append(s)
    except Exception:
        pass

print(f"Successfully parsed {len(songs)} song JSON objects!")
if songs:
    with open("naux_songs_sample.json", "w", encoding="utf-8") as out:
        json.dump(songs[:50], out, indent=2)
    print("Saved 50 sample songs to naux_songs_sample.json")

    # Group by language
    langs = {}
    for s in songs:
        l = s.get("language", "unknown")
        langs[l] = langs.get(l, 0) + 1
    print("Songs by language:", langs)

