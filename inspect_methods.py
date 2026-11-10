import os

with open(os.path.join("naux_analysis", "PlayerEngine_raw.js"), "r", encoding="utf-8") as f:
    code = f.read()

# Let's inspect createPlayer, load, preloadNext, tick, requestHandoff, startIncoming, startFade, endFade
targets = ["createPlayer", "load(", "preloadNext", "tick()", "cutPoint", "requestHandoff", "startIncoming", "startFade", "endFade"]

for t in targets:
    idx = code.find(t)
    if idx != -1:
        print(f"\n==================== {t} ====================")
        print(code[idx:idx+1200])

