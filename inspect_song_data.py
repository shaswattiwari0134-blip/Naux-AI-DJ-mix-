import os
import re

with open(os.path.join("naux_analysis", "1vakelacxrphe.js"), "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

print("File size:", len(content))

# Look for song data patterns
# Songs likely have titles, artists, youtube ids, hook timestamps, energy, etc.
# Let's search for typical song titles or properties
patterns = [
    r'\{[^{}]*?"title"[^{}]*?\}',
    r'\{[^{}]*?"youtube"[^{}]*?\}',
    r'\{[^{}]*?"hook"[^{}]*?\}',
    r'\{[^{}]*?"start"[^{}]*?\}',
    r'\{[^{}]*?"drop"[^{}]*?\}',
    r'\{[^{}]*?"bpm"[^{}]*?\}',
    r'\{[^{}]*?"cue"[^{}]*?\}',
]

for p in patterns:
    matches = re.findall(p, content[:200000])
    print(f"Pattern {p}: {len(matches)} matches in first 200KB")
    if matches:
        print("Sample match:", matches[0][:150])

# Let's search for some well-known songs in Hindi / Punjabi
test_songs = ["chattar", "tauba", "badshah", "apna bana le", "dilbar", "brown munde", "karan aujla", "shubh", "dhurva"]
for ts in test_songs:
    if ts in content.lower():
        idx = content.lower().find(ts)
        snippet = content[max(0, idx - 100):min(len(content), idx + 200)]
        print(f"\nFound song '{ts}' at {idx}:")
        print(snippet)
        break

