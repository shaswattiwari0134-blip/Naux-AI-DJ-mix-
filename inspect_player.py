import os
import re

chunk_dir = "naux_analysis"
js_files = [f for f in os.listdir(chunk_dir) if f.endswith(".js")]

for jf in js_files:
    path = os.path.join(chunk_dir, jf)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    if "naux-players" in text or "naux_players" in text or "YT.Player" in text or "onYouTubeIframeAPIReady" in text or "iframe_api" in text:
        print(f"Match in {jf}!")
        # Let's find snippets around these terms
        for term in ["naux-players", "YT.Player", "onYouTubeIframeAPIReady", "iframe_api", "crossfade"]:
            for m in re.finditer(re.escape(term), text):
                idx = m.start()
                snippet = text[max(0, idx - 150):min(len(text), idx + 250)]
                print(f"--- {term} snippet ---")
                print(snippet)
                print("\n")


