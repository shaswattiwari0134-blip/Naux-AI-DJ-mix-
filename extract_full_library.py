import os
import re
import json

with open(os.path.join("naux_analysis", "1vakelacxrphe.js"), "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

matches = re.finditer(r'\{"song_id":"(?P<id>[^"]+)"', content)

full_library = []
seen_ids = set()

for m in matches:
    start = m.start()
    depth = 0
    end = start
    for i in range(start, min(len(content), start + 4000)):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    try:
        obj = json.loads(content[start:end])
        song_id = obj.get("song_id")
        yids = obj.get("youtube_ids", [])
        if song_id and yids and song_id not in seen_ids:
            seen_ids.add(song_id)
            full_library.append({
                "song_id": song_id,
                "title": obj.get("title", ""),
                "artist": obj.get("artist", ""),
                "youtube_ids": yids,
                "entry_sec": obj.get("entry_sec", 0),
                "exit_sec": obj.get("exit_sec", obj.get("duration_sec", 180)),
                "duration_sec": obj.get("duration_sec", 180),
                "energy": obj.get("energy", 7),
                "language": obj.get("language", "hindi"),
                "subtype": obj.get("subtype", "party"),
                "tags": obj.get("tags", []),
                "banger": obj.get("banger", False),
                "fame": obj.get("fame", 2)
            })
    except Exception:
        pass

print(f"Extracted {len(full_library)} unique verified songs!")
with open("naux_full_library.json", "w", encoding="utf-8") as out:
    json.dump(full_library, out, indent=2)

print("Saved to naux_full_library.json")

# Stats
by_lang = {}
for s in full_library:
    l = s["language"]
    by_lang[l] = by_lang.get(l, 0) + 1
print("Breakdown by language:", by_lang)

