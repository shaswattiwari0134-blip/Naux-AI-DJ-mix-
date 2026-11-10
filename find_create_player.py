import os

with open(os.path.join("naux_analysis", "PlayerEngine_raw.js"), "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("createPlayer(e,t){")
if idx == -1:
    idx = code.find("createPlayer(")
print(code[idx:idx+1200])

