import os
import re

chunk_dir = "naux_analysis"
js_files = [f for f in os.listdir(chunk_dir) if f.endswith(".js")]

for jf in js_files:
    path = os.path.join(chunk_dir, jf)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    matches = [m.start() for m in re.finditer(r'PlayerEngine', text)]
    if matches:
        print(f"\n{jf}: {len(matches)} occurrences of PlayerEngine")
        for m in matches:
            # Let's inspect context
            print("  --- snippet ---")
            print(text[max(0, m - 50):min(len(text), m + 300)])

