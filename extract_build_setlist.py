import os

with open(os.path.join("naux_analysis", "0yeca2llo2xci.js"), "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('"buildSetlist"')
# search backwards for start of the export or function
start = text.rfind('{id:"hindi",label:"Hindi"', 0, idx)
end = text.find('}],', idx)
if end == -1:
    end = idx + 2500

snippet = text[start:idx + 3500]
print(snippet)
with open(os.path.join("naux_analysis", "buildSetlist_raw.js"), "w", encoding="utf-8") as out:
    out.write(snippet)


