import shutil
import json

# 1. Copy naux_party_clone.html to index.html for zero-config static hosting
shutil.copy("naux_party_clone.html", "index.html")
print("Created index.html (identical to naux_party_clone.html) for web deployment!")

# 2. vercel.json
vercel_config = {
    "version": 2,
    "routes": [
        {"src": "/room", "dest": "/room.html"},
        {"src": "/studio", "dest": "/naux_cue_studio.html"},
        {"src": "/(.*)", "dest": "/$1"}
    ]
}
with open("vercel.json", "w", encoding="utf-8") as f:
    json.dump(vercel_config, f, indent=2)
print("Created vercel.json")

# 3. netlify.toml
netlify_toml = """[build]
  publish = "."

[[redirects]]
  from = "/room"
  to = "/room.html"
  status = 200

[[redirects]]
  from = "/studio"
  to = "/naux_cue_studio.html"
  status = 200
"""
with open("netlify.toml", "w", encoding="utf-8") as f:
    f.write(netlify_toml)
print("Created netlify.toml")

