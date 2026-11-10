import os

with open(os.path.join("naux_analysis", "PlayerEngine_raw.js"), "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("onStateChange(e,t){")
print("NAUX onStateChange implementation:")
print(code[idx:idx+1200])

idx2 = code.find("requestHandoff(e){")
print("\nNAUX requestHandoff implementation:")
print(code[idx2:idx2+1200])

