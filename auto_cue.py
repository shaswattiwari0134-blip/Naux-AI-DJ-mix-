import urllib.request
import re
import json

def fetch_youtube_replay_heatmap(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    })
    
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Network error fetching video: {e}")
        return None

    # Search for ytInitialData
    match = re.search(r'var ytInitialData\s*=\s*({.+?});</script>', html)
    if not match:
        match = re.search(r'ytInitialData\s*=\s*({.+?});', html)
    
    if not match:
        print("ytInitialData not found in HTML")
        return None

    try:
        data = json.loads(match.group(1))
    except Exception as e:
        print(f"JSON parse error: {e}")
        return None

    # Search for markers in frameworkUpdates
    heat_markers = []
    
    def search_dict(d):
        if isinstance(d, dict):
            if "intensityScoreNormalized" in d and "startMillis" in d:
                heat_markers.append({
                    "start_sec": int(d["startMillis"]) / 1000.0,
                    "intensity": float(d["intensityScoreNormalized"])
                })
            for v in d.values():
                search_dict(v)
        elif isinstance(d, list):
            for item in d:
                search_dict(item)

    search_dict(data)
    print(f"Found {len(heat_markers)} heat map points for video {video_id}!")
    
    if heat_markers:
        # Sort by intensity descending
        sorted_by_intensity = sorted(heat_markers, key=lambda x: x["intensity"], reverse=True)
        # Hook is the highest peak that occurs after the first 10 seconds
        hook_candidates = [m for m in sorted_by_intensity if m["start_sec"] >= 8]
        best_hook = hook_candidates[0] if hook_candidates else sorted_by_intensity[0]
        return {
            "markers": heat_markers,
            "detected_hook_sec": round(best_hook["start_sec"]),
            "intensity": best_hook["intensity"]
        }
    return None

if __name__ == "__main__":
    test_id = "uTuchIYZdbM" # Tauba Tauba
    res = fetch_youtube_replay_heatmap(test_id)
    if res:
        print(f"Auto-detected Hook for {test_id}: {res['detected_hook_sec']}s (intensity: {res['intensity']})")
    else:
        print("No heatmap available for this video.")

