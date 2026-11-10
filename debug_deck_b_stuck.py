import os

with open(os.path.join("naux_analysis", "PlayerEngine_raw.js"), "r", encoding="utf-8") as f:
    code = f.read()

# Let's inspect timeout and handoff handling in NAUX
for word in ["timeout", "pendingHandoff", "awaitingStart", "failIncoming", "holding", "timer"]:
    idx = code.find(word)
    if idx != -1:
        print(f"\n--- Context for '{word}' ---")
        print(code[max(0, idx - 100):min(len(code), idx + 400)])

