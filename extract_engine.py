import os
import re

with open(os.path.join("naux_analysis", "0yeca2llo2xci.js"), "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# find where PlayerEngine class `a` is defined
idx = text.find('e.s(["PlayerEngine"')
if idx != -1:
    # search backwards for class or function
    start = text.rfind('class ', 0, idx)
    if start == -1:
        start = text.rfind('function ', 0, idx)
    
    snippet = text[start:idx+50]
    print(f"Extracted PlayerEngine code ({len(snippet)} chars):")
    with open(os.path.join("naux_analysis", "PlayerEngine_raw.js"), "w", encoding="utf-8") as out:
        out.write(snippet)
    print("Saved to naux_analysis/PlayerEngine_raw.js")


