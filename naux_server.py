import http.server
import socketserver
import json
import urllib.parse
import os
import random
import string

PORT = 3000

# Load songs library
LIBRARY = []
if os.path.exists("naux_full_library.json"):
    with open("naux_full_library.json", "r", encoding="utf-8") as f:
        LIBRARY = json.load(f)
elif os.path.exists("naux_top_tracks.json"):
    with open("naux_top_tracks.json", "r", encoding="utf-8") as f:
        LIBRARY = json.load(f)

# In-memory Party Rooms state: { room_code: { now_playing: {}, queue: [], requests: [] } }
ROOMS = {
    "AUX1": {
        "code": "AUX1",
        "now_playing": None,
        "queue": [],
        "requests": []
    }
}

class NauxRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Allow CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. API: Search Songs
        if path == "/api/songs":
            q = query.get("q", [""])[0].lower().strip()
            lang = query.get("lang", [""])[0].lower().strip()
            
            results = LIBRARY
            if lang and lang != "all":
                results = [s for s in results if s.get("language") == lang]
            if q:
                results = [s for s in results if q in s.get("title", "").lower() or q in s.get("artist", "").lower()]
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(results[:50]).encode())
            return

        # 2. API: Get Room State
        elif path == "/api/room":
            code = query.get("code", ["AUX1"])[0].upper()
            room = ROOMS.get(code)
            if not room:
                room = {"code": code, "now_playing": None, "queue": [], "requests": []}
                ROOMS[code] = room

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(room).encode())
            return

        # Default static file serving (e.g. index.html, naux_party_clone.html, room.html)
        if path == "/":
            self.path = "/naux_party_clone.html"
        elif path == "/room":
            self.path = "/room.html"

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}

        # 1. API: Guest Song Request
        if path == "/api/request":
            code = data.get("room_code", "AUX1").upper()
            song_id = data.get("song_id")
            guest_name = data.get("guest_name", "A Guest")

            room = ROOMS.get(code)
            if not room:
                room = {"code": code, "now_playing": None, "queue": [], "requests": []}
                ROOMS[code] = room

            # Find song in library
            song = next((s for s in LIBRARY if s.get("song_id") == song_id), None)
            if song:
                req_entry = {
                    "request_id": ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
                    "guest": guest_name,
                    "song": song,
                    "votes": 1
                }
                room["requests"].append(req_entry)
                print(f"[REQUEST] Guest {guest_name} requested '{song['title']}' in room {code}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "room": room}).encode())
            return

        # 2. API: Host Sync State
        elif path == "/api/room/update":
            code = data.get("room_code", "AUX1").upper()
            room = ROOMS.setdefault(code, {"code": code, "now_playing": None, "queue": [], "requests": []})
            if "now_playing" in data:
                room["now_playing"] = data["now_playing"]
            if "queue" in data:
                room["queue"] = data["queue"]

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
            return

        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    print(f"=========================================================")
    print(f"  NAUX Full-Stack Server Running on http://localhost:{PORT}")
    print(f"  - Host Player:   http://localhost:{PORT}/naux_party_clone.html")
    print(f"  - Guest Mobile:  http://localhost:{PORT}/room.html")
    print(f"  - Cue Studio:    http://localhost:{PORT}/naux_cue_studio.html")
    print(f"=========================================================")
    with socketserver.TCPServer(("", PORT), NauxRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

