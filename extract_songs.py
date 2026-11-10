import os
import re
import json

with open(os.path.join("naux_analysis", "1vakelacxrphe.js"), "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Let's extract complete JSON song objects
# Look for pattern {"song_id": ...}
matches = re.findall(r'(\{"song_id"[^}]+?\})', content)
print(f"Direct match found: {len(matches)}")

if not matches:
    # Try finding where songs are defined
    idx = content.find('"song_id"')
    if idx != -1:
        # Find closing brace
        print("Snippet around first song_id:")
        print(content[idx:idx+1000])

# Let's see how many song_ids exist in the file
all_song_ids = re.findall(r'"song_id"\s*:\s*"([^"]+)"', content)
print(f"Total songs found: {len(all_song_ids)}")
print("Sample song IDs:", all_song_ids[:15])


