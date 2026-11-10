import os
import re

chunk_dir = "naux_analysis"
js_files = [f for f in os.listdir(chunk_dir) if f.endswith(".js")]

keywords = [
    "AudioContext", "webkitAudioContext", "createGain", "crossfade",
    "youtube", "soundcloud", "spotify", "hook", "drop", "cue",
    "/api/", "fetch(", "player", "room", "prompt", "setlist", "curation"
]

print(f"Analyzing {len(js_files)} JS files...")

for jf in js_files:
    path = os.path.join(chunk_dir, jf)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    
    print(f"\n--- {jf} ({len(text)} bytes) ---")
    
    # Check for API routes
    apis = set(re.findall(r'["\'](/api/[^"\']+)["\']', text))
    if apis:
        print("  API routes found:", apis)

    # Check for YouTube player references
    if "youtube" in text.lower() or "youtu.be" in text.lower() or "ytplayer" in text.lower():
        yt_matches = set(re.findall(r'[a-zA-Z0-9_\-]{11}', text))
        print("  Mentions YouTube / video IDs")
    
    # Check for Audio / WebAudio
    webaudio = [kw for kw in ["AudioContext", "createGain", "linearRampToValueAtTime", "Audio(", "HTMLAudioElement"] if kw in text]
    if webaudio:
        print("  WebAudio / Audio elements:", webaudio)

    # Search for specific interesting strings or function patterns
    matches = re.findall(r'(\b[a-zA-Z0-9_$]+\b\s*:\s*\[[^\]]{20,200}\])', text)

