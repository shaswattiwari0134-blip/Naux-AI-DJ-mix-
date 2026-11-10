import json

with open("naux_full_library.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

print(f"Total songs in naux_full_library.json: {len(songs)}")

# Artists count
artists = set()
languages = {}
for s in songs:
    artists.add(s.get("artist", "").split(",")[0].strip())
    l = s.get("language", "unknown")
    languages[l] = languages.get(l, 0) + 1

print(f"Total unique primary artists: {len(artists)}")
print("Language breakdown:", languages)
print("Sample artists:", list(artists)[:20])

