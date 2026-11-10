import os

with open(os.path.join("naux_analysis", "PlayerEngine_raw.js"), "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("nextSource(e){")
print("NAUX nextSource implementation:")
print(code[idx:idx+800])

