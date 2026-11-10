import os
import re

chunk_dir = "naux_analysis"
js_files = [f for f in os.listdir(chunk_dir) if f.endswith(".js")]

for jf in js_files:
    path = os.path.join(chunk_dir, jf)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    idx = text.find('"buildSetlist"')
    if idx != -1:
        print(f"Found \"buildSetlist\" export in {jf} at {idx}!")
        print(text[max(0, idx - 1500):min(len(text), idx + 500)])

