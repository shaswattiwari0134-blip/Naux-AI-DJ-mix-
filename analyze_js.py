import os
import re
import xml.etree.ElementTree as ET

# Read sitemap
sitemap_path = os.path.join("naux_analysis", "sitemap.xml")
if os.path.exists(sitemap_path):
    print("=== SITEMAP URLS ===")
    root = ET.parse(sitemap_path).getroot()
    for elem in root.iter():
        if elem.tag.endswith("loc"):
            print(elem.text)

# Inspect songs.html
print("\n=== SONGS.HTML TITLE & HEADINGS ===")
with open(os.path.join("naux_analysis", "songs.html"), "r", encoding="utf-8", errors="ignore") as f:
    songs_html = f.read()
    # find links or titles
    links = re.findall(r'href="([^"]+)"', songs_html)
    unique_links = sorted(set(links))
    print("Links in songs.html:")
    for l in unique_links:
        if not l.startswith(("/_next", "#")) and len(l) > 1:
            print("  ", l)


