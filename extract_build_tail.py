import os

with open(os.path.join("naux_analysis", "0yeca2llo2xci.js"), "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('if("winddown"===t)return[...r].reverse().flat()')
print(text[idx:idx+1500])

