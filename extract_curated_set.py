import os
import re
import json

with open(os.path.join("naux_analysis", "1vakelacxrphe.js"), "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Find all occurrences of song_id
matches = re.finditer(r'\{"song_id":"(?P<id>[^"]+)"', content)

songs = []
for m in matches:
    start = m.start()
    depth = 0
    end = start
    for i in range(start, min(len(content), start + 3000)):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    try:
        obj = json.loads(content[start:end])
        if obj.get("youtube_ids") and len(obj["youtube_ids"]) > 0:
            songs.append(obj)
    except Exception:
        pass

print(f"Total songs parsed with valid YouTube IDs: {len(songs)}")

# Let's filter top bangers across languages
bangers = [s for s in songs if s.get("banger") or s.get("energy", 0) >= 7]
print(f"Total bangers/high energy: {len(bangers)}")

with open("naux_top_tracks.json", "w", encoding="utf-8") as out:
    json.dump(bangers[:40], out, indent=2)

print("Saved 40 top tracks to naux_top_tracks.json")

