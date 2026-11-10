import os

with open(os.path.join("naux_analysis", "0yeca2llo2xci.js"), "r", encoding="utf-8") as f:
    text = f.read()

# Let's find how `ea` (the approve and play handler) works
idx = text.find("APPROVE & PLAY")
if idx == -1:
    idx = text.find("approve")
print("Snippet around approve / play:")
print(text[max(0, idx - 150):min(len(text), idx + 500)])

