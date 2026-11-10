import os

with open(os.path.join("naux_analysis", "PlayerEngine_raw.js"), "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("cutPoint(e){")
if idx != -1:
    print(code[idx:idx+500])
else:
    # search all cutPoint occurrences
    print("All cutPoint matches:")
    for m in [m.start() for m in [i for i in range(len(code)) if code.startswith("cutPoint", i)]]:
        print(code[m:m+200])


