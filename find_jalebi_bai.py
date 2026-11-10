import json

with open("naux_full_library.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

for s in songs:
    if "jalebi" in s.get("title", "").lower() or "jalebi" in s.get("song_id", "").lower():
        print("Found song:")
        print(json.dumps(s, indent=2))

