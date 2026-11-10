import os
import re

chunk_dir = "naux_analysis"
js_files = [f for f in os.listdir(chunk_dir) if f.endswith(".js")]

for jf in js_files:
    path = os.path.join(chunk_dir, jf)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    idx = text.find("buildSetlist")
    if idx != -1:
        print(f"Found buildSetlist in {jf} at {idx}!")
        # Let's inspect 3000 chars around it
        start = max(0, idx - 200)
        end = min(len(text), idx + 3500)
        print(text[start:end])


