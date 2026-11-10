import os
import re
import json

with open(os.path.join("naux_analysis", "1vakelacxrphe.js"), "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

idx = content.find('{"song_id":"tauba-tauba-karan-aujla"')
if idx == -1:
    idx = content.find('"song_id":"tauba-tauba-karan-aujla"')

# Find object boundaries
start = content.rfind('{', 0, idx + 10)
depth = 0
end = start
for i in range(start, len(content)):
    if content[i] == '{':
        depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            end = i + 1
            break

raw_obj = content[start:end]
print("Song object:")
try:
    obj = json.loads(raw_obj)
    print(json.dumps(obj, indent=2))
except Exception as e:
    print(raw_obj)


