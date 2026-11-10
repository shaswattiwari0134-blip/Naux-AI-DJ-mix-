import os

with open(os.path.join("naux_analysis", "0yeca2llo2xci.js"), "r", encoding="utf-8") as f:
    text_0y = f.read()

with open(os.path.join("naux_analysis", "1c5oexlmb71x4.js"), "r", encoding="utf-8") as f:
    text_1c = f.read()

# Search for naux-players in css or js
idx = text_0y.find("styleHost")
print("styleHost snippet in 0yeca2llo2xci.js:")
print(text_0y[idx-50:idx+350])

idx2 = text_1c.find(".naux-players")
print("\n.naux-players in 1c5oexlmb71x4.js:")
print(text_1c[idx2-50:idx2+600])

# Also check CSS file: 0g8wdnf_9cbsd.css if exists
css_path = None
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".css"):
            print("Found CSS:", f)

