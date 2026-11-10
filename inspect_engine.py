import os
import re

with open(os.path.join("naux_analysis", "0yeca2llo2xci.js"), "r", encoding="utf-8", errors="ignore") as f:
    text_0y = f.read()

with open(os.path.join("naux_analysis", "1c5oexlmb71x4.js"), "r", encoding="utf-8", errors="ignore") as f:
    text_1c = f.read()

# Search for PlayerEngine in 0yeca2llo2xci.js
idx = text_0y.find("PlayerEngine")
if idx != -1:
    print("PlayerEngine in 0yeca2llo2xci.js:")
    # print 3000 chars around it
    print(text_0y[max(0, idx - 200):min(len(text_0y), idx + 3500)])

# Search for crossfade or deck logic in 1c5oexlmb71x4.js
idx2 = text_1c.find("crossfading")
if idx2 != -1:
    print("\n\ncrossfading in 1c5oexlmb71x4.js:")
    print(text_1c[max(0, idx2 - 200):min(len(text_1c), idx2 + 2500)])

