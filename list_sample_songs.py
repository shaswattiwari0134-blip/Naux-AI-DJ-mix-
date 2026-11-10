import json

with open("naux_songs_sample.json", "r", encoding="utf-8") as f:
    songs = json.load(f)

valid = [s for s in songs if s.get("youtube_ids") and len(s["youtube_ids"]) > 0]
print(f"Total valid songs with YouTube IDs: {len(valid)}")
for i, s in enumerate(valid[:20]):
    print(f"{i+1}. {s['title']} - {s['artist']} | YT: {s['youtube_ids'][0]} | Entry: {s.get('entry_sec', 0)}s | Exit: {s.get('exit_sec', s.get('duration_sec', 120))}s | Energy: {s.get('energy', 7)}")
