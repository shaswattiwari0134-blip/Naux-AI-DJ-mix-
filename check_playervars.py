import os

with open(os.path.join("naux_analysis", "PlayerEngine_raw.js"), "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("playerVars")
print("playerVars in NAUX PlayerEngine:")
print(code[idx-50:idx+350])

