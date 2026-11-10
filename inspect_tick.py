import os

with open(os.path.join("naux_analysis", "PlayerEngine_raw.js"), "r", encoding="utf-8") as f:
    code = f.read()

for target in ["tick(){", "createPlayer(", "cutPoint("]:
    idx = code.find(target)
    if idx != -1:
        print(f"\n--- {target} ---")
        print(code[idx:idx+800])

