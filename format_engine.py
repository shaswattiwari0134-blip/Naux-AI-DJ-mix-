import os
import re

with open(os.path.join("naux_analysis", "PlayerEngine_raw.js"), "r", encoding="utf-8") as f:
    code = f.read()

# Let's find method signatures in the class
methods = re.findall(r'(?:async\s+)?([a-zA-Z0-9_$]+)\s*\(([^)]*)\)\s*\{', code)
print("Methods in PlayerEngine:")
for m, args in methods:
    print(f"  {m}({args})")

# Let's print the constructor and start/crossfade/tick methods
print("\n--- Snippet of class start ---")
print(code[:2000])


