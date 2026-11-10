import urllib.request
import re
import os

os.makedirs("naux_analysis", exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

urls = [
    ("robots.txt", "https://www.naux.party/robots.txt"),
    ("sitemap.xml", "https://www.naux.party/sitemap.xml"),
    ("songs.html", "https://www.naux.party/songs"),
]

for name, u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            with open(os.path.join("naux_analysis", name), "wb") as f:
                f.write(content)
            print(f"Downloaded {u} -> {name} ({len(content)} bytes)")
    except Exception as e:
        print(f"Error {u}: {e}")

# Read naux_home.html to find all JS chunks
with open("naux_home.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

chunks = list(set(re.findall(r'/_next/static/chunks/[a-zA-Z0-9_\-\.]+\.js', html)))
print(f"Found {len(chunks)} JS chunks:")
for c in chunks:
    chunk_name = os.path.basename(c)
    chunk_url = f"https://www.naux.party{c}"
    try:
        req = urllib.request.Request(chunk_url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            with open(os.path.join("naux_analysis", chunk_name), "wb") as f:
                f.write(content)
            print(f"Downloaded {chunk_name} ({len(content)} bytes)")
    except Exception as e:
        print(f"Error {chunk_url}: {e}")

