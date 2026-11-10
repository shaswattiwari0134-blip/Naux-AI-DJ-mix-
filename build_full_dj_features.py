import json
import shutil
import re

print("1. Loading naux_full_library.json...")
with open("naux_full_library.json", "r", encoding="utf-8") as f:
    library = json.load(f)

# Ensure Jalebi Bai has rock-solid fallback IDs
for s in library:
    if s.get("song_id") == "jalebi-bai-ritu-pathak":
        s["youtube_ids"] = ["rpw4l39z_9A", "jURo-_lj9yk", "QYh6mYIJG2Y", "8B_N7-1v0s0"]

with open("naux_full_library.json", "w", encoding="utf-8") as f:
    json.dump(library, f, indent=2)

# Extract top artists with song counts for quick-select pills
artist_counts = {}
for s in library:
    art = s.get("artist", "")
    # Clean and split
    parts = re.split(r'[,&]|\bfeat\.?\b', art, flags=re.IGNORECASE)
    for p in parts:
        name = p.strip()
        if len(name) >= 3 and not name.lower().startswith("dj ") and not name.lower() in ["various", "ft", "the", "and"]:
            artist_counts[name] = artist_counts.get(name, 0) + 1

# Top 20 popular artists for the quick-pick UI
popular_artists = sorted(artist_counts.items(), key=lambda x: x[1], reverse=True)[:24]
top_artists_json = json.dumps([{"name": name, "count": count} for name, count in popular_artists])

# Minify library for embedding
min_lib = []
for s in library:
    min_lib.append({
        "song_id": s.get("song_id"),
        "title": s.get("title", ""),
        "artist": s.get("artist", ""),
        "youtube_ids": s.get("youtube_ids", []),
        "entry_sec": s.get("entry_sec", 0),
        "exit_sec": s.get("exit_sec", s.get("duration_sec", 180)),
        "duration_sec": s.get("duration_sec", 180),
        "energy": s.get("energy", 7),
        "language": s.get("language", "hindi"),
        "subtype": s.get("subtype", "party"),
        "banger": s.get("banger", False)
    })

library_json = json.dumps(min_lib)

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NAUX · Universal Party DJ (DJ Song Maker & Multi-Artist Spotlight)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
  <style>
    body {{
      background-color: #080808;
      color: #f5f5f5;
      font-family: 'Inter', sans-serif;
    }}
    .font-anton {{
      font-family: 'Anton', sans-serif;
      letter-spacing: 0.05em;
    }}
    .text-lime {{ color: #d4ff00; }}
    .bg-lime {{ background-color: #d4ff00; }}
    .border-lime {{ border-color: #d4ff00; }}
    .pulse-glow {{
      box-shadow: 0 0 35px rgba(212, 255, 0, 0.45);
    }}
    #naux-players-host {{
      position: fixed;
      left: 0;
      bottom: 0;
      width: 320px;
      height: 180px;
      opacity: 0.01;
      pointer-events: none;
      z-index: -1;
      overflow: hidden;
    }}
    .eq-bar {{
      animation: eqBounce 0.8s ease-in-out infinite alternate;
    }}
    @keyframes eqBounce {{
      0% {{ height: 20%; }}
      100% {{ height: 100%; }}
    }}
    .queue-item.dragging {{
      opacity: 0.4;
      border: 2px dashed #d4ff00;
    }}
    .queue-item.drag-over {{
      border-top: 2px solid #d4ff00;
      background: rgba(212, 255, 0, 0.08);
    }}
    input[type=range] {{
      accent-color: #d4ff00;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-lime selection:text-black">

  <!-- PERSISTENT YOUTUBE IFRAME HOST -->
  <div id="naux-players-host">
    <div id="deck-A-player"></div>
    <div id="deck-B-player"></div>
  </div>

  <!-- Top Bar -->
  <header class="border-b border-white/10 px-4 sm:px-6 py-4 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <h1 class="text-3xl font-anton text-lime tracking-wider">NAUX</h1>
      <span class="text-xs bg-white/10 px-2 py-0.5 rounded text-white/70 font-mono">PRO DJ EDITION</span>
    </div>
    <div class="flex items-center gap-2 sm:gap-3">
      <!-- DJ Song Maker Header Button -->
      <button id="headerOpenDjMakerBtn" class="bg-lime/10 border border-lime/40 hover:bg-lime hover:text-black text-lime font-anton px-3.5 py-1.5 rounded-xl text-xs uppercase tracking-wider transition flex items-center gap-1.5 shadow-lg">
        <span>🎛️</span> Make Song DJ
      </button>

      <div id="ytStatusBadge" class="hidden sm:flex items-center gap-2 text-xs font-mono text-white/50">
        <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span> Connecting YouTube...
      </div>

      <a href="room.html" target="_blank" class="hidden md:inline-flex items-center gap-1.5 text-xs bg-white/10 hover:bg-white/20 border border-white/20 px-3 py-1.5 rounded-xl transition">
        <span>📱</span> Guest Mobile Mode
      </a>
    </div>
  </header>

  <!-- Localhost Warning Notice -->
  <div id="fileNotice" class="hidden bg-amber-500/20 border border-amber-500/50 p-4 mx-4 mt-4 rounded-2xl text-xs text-amber-200 flex items-center justify-between">
    <div>
      <strong>⚠️ Running via file://:</strong> YouTube IFrame API blocks audio on local files. Launch via <strong>run_naux.bat</strong> (or run <code>python -m http.server 3000</code>) and open <a href="http://localhost:3000" class="underline font-bold">http://localhost:3000</a>.
    </div>
  </div>

  <!-- Browser Audio Autoplay Prompt Banner -->
  <div id="unmutePrompt" class="hidden bg-lime/20 border border-lime/60 p-4 mx-4 mt-4 rounded-2xl text-sm text-lime flex items-center justify-between animate-pulse">
    <div class="flex items-center gap-3">
      <span class="text-2xl">🔊</span>
      <div>
        <p class="font-bold">Browser Blocked Background Audio Autoplay</p>
        <p class="text-xs text-white/80">Click Unmute Audio to let the dual-deck auto-mix flow without interruptions.</p>
      </div>
    </div>
    <button id="unmuteBtn" class="bg-lime text-black font-anton px-5 py-2.5 rounded-xl text-sm uppercase hover:brightness-110 shadow-lg">
      Unmute Audio Now
    </button>
  </div>

  <!-- MAIN APP CONTAINER -->
  <main class="flex-1 max-w-4xl w-full mx-auto p-4 sm:p-6 space-y-6">

    <!-- 1. SETUP / MOOD TUNER VIEW -->
    <div id="setupView" class="space-y-6">
      
      <div class="text-center space-y-2 py-6">
        <h2 class="text-4xl sm:text-6xl font-anton tracking-tight uppercase">Party Without Breaks</h2>
        <p class="text-white/60 text-sm sm:text-base max-w-xl mx-auto">
          Dual-deck YouTube audio engine. Pick your favorite singers, make your own DJ drops, and enjoy seamless equal-power hook crossfades.
        </p>
      </div>

      <!-- FEATURE 2: MULTI-ARTIST SPOTLIGHT DJ MODE -->
      <div class="border-2 border-lime/40 bg-lime/[0.02] rounded-3xl p-6 space-y-4 shadow-xl">
        <div class="flex flex-wrap justify-between items-center gap-2">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-lg">🎤</span>
              <h3 class="font-anton text-lg uppercase tracking-wide text-white">Artist Spotlight DJ Mode</h3>
            </div>
            <p class="text-[11px] text-white/50">Pick 1 singer to play only their tracks, or add multiple singers so only their songs play!</p>
          </div>
          <div class="flex items-center gap-2">
            <button id="clearArtistsBtn" class="hidden text-xs text-red-400 hover:text-red-300 font-mono px-3 py-1 rounded-xl border border-red-500/30 transition">
              ✕ Clear Singers
            </button>
            <span id="artistMatchCountBadge" class="text-xs font-mono text-lime bg-lime/10 px-3 py-1 rounded-xl border border-lime/30 font-bold">
              All Artists Active
            </span>
          </div>
        </div>

        <!-- Singer Search & Autocomplete Input -->
        <div class="relative">
          <input id="artistSearchInput" type="text" placeholder="Search singer to add (e.g. Diljit, Arijit, Karan Aujla, Moose Wala, Honey Singh, Drake...)" 
                 class="w-full bg-black/60 border border-white/20 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:border-lime text-white">
          <div id="artistSearchDropdown" class="hidden absolute left-0 right-0 top-full mt-2 bg-neutral-900 border border-white/20 rounded-2xl p-2 max-h-52 overflow-y-auto z-50 divide-y divide-white/5 shadow-2xl space-y-1">
          </div>
        </div>

        <!-- Active Selected Singers Badges -->
        <div id="selectedArtistsContainer" class="hidden flex flex-wrap gap-2 pt-1">
        </div>

        <!-- Quick Pick Top Artists Pills -->
        <div class="space-y-2 pt-2 border-t border-white/10">
          <span class="text-[10px] font-mono uppercase text-white/40 tracking-wider">Quick Pick Top Artists (Tap to Toggle):</span>
          <div class="flex flex-wrap gap-2" id="topArtistPills">
          </div>
        </div>
      </div>

      <!-- Language Selector -->
      <div class="border border-white/10 rounded-3xl p-6 bg-white/[0.02] space-y-4">
        <h3 class="text-xs font-mono uppercase tracking-widest text-white/40">Select Languages (Applies when no artist selected)</h3>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3" id="langSelector">
          <button data-lang="punjabi" class="lang-btn border border-lime bg-lime/10 text-lime px-4 py-3 rounded-2xl font-bold text-sm transition">
            Punjabi 🔥
          </button>
          <button data-lang="hindi" class="lang-btn border border-lime bg-lime/10 text-lime px-4 py-3 rounded-2xl font-bold text-sm transition">
            Hindi ⚡
          </button>
          <button data-lang="english" class="lang-btn border border-lime bg-lime/10 text-lime px-4 py-3 rounded-2xl font-bold text-sm transition">
            English / EDM 🌐
          </button>
          <button data-lang="all" class="lang-btn border border-white/10 text-white/60 hover:border-white/30 px-4 py-3 rounded-2xl font-bold text-sm transition">
            All Languages ({len(min_lib)})
          </button>
        </div>
      </div>

      <!-- Energy / Time Mood -->
      <div class="border border-white/10 rounded-3xl p-6 bg-white/[0.02] space-y-4">
        <h3 class="text-xs font-mono uppercase tracking-widest text-white/40">Party Energy Mood</h3>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3" id="moodSelector">
          <button data-mood="warmup" class="mood-btn border border-white/10 text-white/60 hover:border-white/30 px-4 py-3 rounded-2xl font-bold text-sm transition">
            Warm Up 🍸
          </button>
          <button data-mood="peak" class="mood-btn border border-lime bg-lime/10 text-lime px-4 py-3 rounded-2xl font-bold text-sm transition">
            Peak Party 🚀
          </button>
          <button data-mood="bangers" class="mood-btn border border-white/10 text-white/60 hover:border-white/30 px-4 py-3 rounded-2xl font-bold text-sm transition">
            Only Bangers 💣
          </button>
          <button data-mood="winddown" class="mood-btn border border-white/10 text-white/60 hover:border-white/30 px-4 py-3 rounded-2xl font-bold text-sm transition">
            Late Night 🌙
          </button>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
        <button id="approvePlayBtn" class="w-full sm:w-auto bg-lime text-black font-anton text-2xl px-12 py-5 rounded-3xl hover:brightness-110 active:scale-95 transition shadow-2xl pulse-glow uppercase tracking-wider">
          Approve &amp; Start DJ Set
        </button>
        <button id="setupMakeDjBtn" class="w-full sm:w-auto border border-lime/40 hover:bg-lime/10 text-lime font-anton text-lg px-8 py-5 rounded-3xl transition uppercase tracking-wider flex items-center justify-center gap-2">
          <span>🎛️</span> Make Custom DJ Song
        </button>
      </div>

    </div>

    <!-- 2. LIVE DJ PLAYER VIEW -->
    <div id="playerView" class="hidden space-y-6">

      <!-- NOW PLAYING HERO DECK -->
      <div class="relative overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03] p-6 sm:p-8 space-y-6">
        
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-bold bg-lime/20 text-lime border border-lime/40">
              <span class="w-2 h-2 rounded-full bg-lime animate-ping"></span>
              LIVE ON AUX
            </span>
            <span id="activeDeckPill" class="text-xs font-mono text-white/40 uppercase">Deck A Live</span>
          </div>
          
          <div id="crossfadeIndicator" class="hidden text-xs font-mono font-bold text-lime animate-pulse">
            ⚡ CROSSFADING...
          </div>
        </div>

        <div class="space-y-1">
          <h2 id="nowPlayingTitle" class="text-4xl sm:text-6xl font-anton text-white tracking-wide uppercase truncate">
            Loading...
          </h2>
          <p id="nowPlayingArtist" class="text-white/60 text-lg sm:text-xl font-medium truncate">
            -
          </p>
        </div>

        <div class="space-y-2">
          <div class="flex justify-between text-xs text-white/40 font-mono">
            <span id="currentTimeLabel">0:00</span>
            <span id="cutPointLabel" class="text-lime">Hook Cut @ 1:27</span>
          </div>
          <div class="relative w-full h-3 bg-white/10 rounded-full overflow-hidden">
            <div id="progressBar" class="h-full bg-lime transition-all duration-100" style="width: 0%"></div>
          </div>
        </div>

        <!-- Controls -->
        <div class="mt-8 flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <button id="togglePlayBtn" class="bg-white text-black font-anton px-8 py-3 rounded-2xl hover:bg-white/90 active:scale-95 transition text-lg uppercase">
              Pause
            </button>
            <button id="skipBtn" class="bg-white/10 border border-white/20 hover:border-lime hover:text-lime px-6 py-3 rounded-2xl font-bold text-sm transition flex items-center gap-2">
              <span>Skip Track ⏭</span>
            </button>
          </div>

          <div class="flex flex-wrap items-center gap-3">
            <!-- Custom DJ this playing song button -->
            <button id="djCurrentSongBtn" class="border border-lime/40 bg-lime/10 hover:bg-lime hover:text-black text-lime px-3.5 py-2 rounded-xl text-xs font-anton uppercase tracking-wider transition flex items-center gap-1.5" title="Customize hook drop and cut for this song">
              <span>🎛️</span> DJ This Song
            </button>

            <!-- Fade duration selector -->
            <div class="flex items-center gap-1.5 bg-black/40 border border-white/10 px-3 py-1.5 rounded-xl text-xs">
              <span class="text-white/40 uppercase text-[10px] font-bold">Fade:</span>
              <select id="fadeDurationSelect" class="bg-transparent text-lime font-mono font-bold focus:outline-none cursor-pointer">
                <option value="500" class="bg-neutral-900 text-white">0.5s (Quick Drop)</option>
                <option value="1500" selected class="bg-neutral-900 text-white">1.5s (Standard Mix)</option>
                <option value="3000" class="bg-neutral-900 text-white">3.0s (Long Blend)</option>
              </select>
            </div>

            <!-- Master Volume -->
            <div class="flex items-center gap-2 bg-black/40 border border-white/10 px-3 py-1.5 rounded-xl text-xs">
              <span class="text-white/40">🔊</span>
              <input id="masterVolumeSlider" type="range" min="0" max="100" value="100" class="w-16 sm:w-20 cursor-pointer" title="Master Speaker Volume">
              <span id="masterVolLabel" class="font-mono text-lime text-[11px] w-7 text-right">100%</span>
            </div>

            <button id="playFullBtn" class="border border-white/20 hover:border-white/50 text-white/70 px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition">
              Ride Full Song (Don't Cut)
            </button>
          </div>
        </div>

        <!-- Keyboard Shortcuts Hint Badge -->
        <div class="mt-4 pt-3 border-t border-white/5 flex flex-wrap items-center gap-2 text-[11px] text-white/40 font-mono">
          <span class="text-white/60 font-semibold uppercase text-[10px] tracking-wider">Keyboard:</span>
          <span class="bg-white/10 px-2 py-0.5 rounded border border-white/10 text-white/80 font-bold">Space</span> <span class="text-white/60">Play / Pause</span>
          <span class="bg-white/10 px-2 py-0.5 rounded border border-white/10 text-white/80 font-bold ml-2">→</span> <span class="text-white/60">Skip Hook</span>
          <span class="bg-white/10 px-2 py-0.5 rounded border border-white/10 text-white/80 font-bold ml-2">S</span> <span class="text-white/60">Shuffle</span>
          <span class="bg-white/10 px-2 py-0.5 rounded border border-white/10 text-white/80 font-bold ml-2">F</span> <span class="text-white/60">Ride Full</span>
        </div>
      </div>

      <!-- LIVE SINGER SPOTLIGHT BAR (Change on-the-fly) -->
      <div class="bg-lime/[0.04] border border-lime/30 rounded-2xl p-4 flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <span class="text-2xl">🎤</span>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-mono uppercase text-white/50 font-bold">Artist Spotlight:</span>
              <span id="liveActiveSingersText" class="text-xs font-mono font-bold text-lime">All Artists (Full Catalog)</span>
            </div>
            <p class="text-[11px] text-white/40">Change singers anytime to re-mix only their tracks into the queue.</p>
          </div>
        </div>
        <button id="openLiveArtistFilterBtn" class="bg-lime text-black font-anton text-xs uppercase px-4 py-2 rounded-xl hover:brightness-110 transition shadow">
          ⚙️ Change Singers
        </button>
      </div>

      <!-- UNIVERSAL SEARCH & QUEUE -->
      <div class="bg-white/5 border border-white/10 rounded-3xl p-5 space-y-3">
        <div class="flex justify-between items-center">
          <h3 class="font-anton text-lg uppercase tracking-wide text-white/90">Find Any Artist / Add Any YouTube Track</h3>
          <span class="text-[10px] text-white/40 uppercase tracking-widest">{len(min_lib)}+ Songs Ready</span>
        </div>
        
        <div class="flex gap-2">
          <input id="quickSearchInput" type="text" placeholder="Search artist (Arijit, Drake, Diljit, Weeknd...) or paste YouTube URL" 
                 class="flex-1 bg-black/60 border border-white/20 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:border-lime text-white">
          <button id="addCustomYtBtn" class="bg-lime text-black font-anton px-5 py-3 rounded-2xl text-sm uppercase hover:brightness-110 transition whitespace-nowrap">
            + Queue Track
          </button>
          <button id="openDjMakerSearchBtn" class="border border-lime/40 bg-lime/10 hover:bg-lime hover:text-black text-lime font-anton px-4 py-3 rounded-2xl text-sm uppercase transition whitespace-nowrap">
            🎛️ DJ Maker
          </button>
        </div>

        <div id="searchResultsDropdown" class="hidden bg-neutral-900 border border-white/20 rounded-2xl p-2 max-h-60 overflow-y-auto divide-y divide-white/5 space-y-1">
        </div>
      </div>

      <!-- DUAL-DECK DJ MONITORS -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        <!-- DECK A -->
        <div id="deckAMonitor" class="p-5 rounded-3xl border-2 border-lime bg-white/[0.04] space-y-3 transition">
          <div class="flex justify-between items-center text-xs font-mono">
            <span class="text-white/60 font-bold">DECK A (YOUTUBE)</span>
            <span id="deckAStatus" class="text-lime font-bold">LIVE (100% VOL)</span>
          </div>

          <div class="flex items-center gap-4 bg-black/40 p-4 rounded-2xl border border-white/5">
            <div id="deckAEq" class="flex items-end gap-1 h-8 w-8">
              <span class="w-1.5 bg-lime rounded-full eq-bar" style="animation-delay: 0.1s;"></span>
              <span class="w-1.5 bg-lime rounded-full eq-bar" style="animation-delay: 0.3s;"></span>
              <span class="w-1.5 bg-lime rounded-full eq-bar" style="animation-delay: 0.2s;"></span>
              <span class="w-1.5 bg-lime rounded-full eq-bar" style="animation-delay: 0.4s;"></span>
            </div>
            <div class="truncate">
              <p id="deckASong" class="font-bold text-white text-sm truncate">Loading...</p>
              <p id="deckAArtist" class="text-xs text-white/50 truncate">Artist</p>
            </div>
          </div>

          <div class="space-y-1">
            <div class="flex justify-between text-[10px] font-mono text-white/40">
              <span>Fader Volume</span>
              <span id="deckAVolLabel">100%</span>
            </div>
            <div class="h-2 w-full bg-white/10 rounded-full overflow-hidden">
              <div id="deckAVolume" class="h-full bg-lime transition-all duration-75" style="width: 100%"></div>
            </div>
          </div>
        </div>

        <!-- DECK B -->
        <div id="deckBMonitor" class="p-5 rounded-3xl border border-white/10 bg-white/[0.02] space-y-3 transition">
          <div class="flex justify-between items-center text-xs font-mono">
            <span class="text-white/60 font-bold">DECK B (YOUTUBE)</span>
            <span id="deckBStatus" class="text-white/40">PRELOADING...</span>
          </div>

          <div class="flex items-center gap-4 bg-black/40 p-4 rounded-2xl border border-white/5">
            <div id="deckBEq" class="flex items-end gap-1 h-8 w-8 opacity-40">
              <span class="w-1.5 bg-white/50 rounded-full h-2"></span>
              <span class="w-1.5 bg-white/50 rounded-full h-4"></span>
              <span class="w-1.5 bg-white/50 rounded-full h-2"></span>
              <span class="w-1.5 bg-white/50 rounded-full h-3"></span>
            </div>
            <div class="truncate">
              <p id="deckBSong" class="font-bold text-white text-sm truncate">Upcoming Track</p>
              <p id="deckBArtist" class="text-xs text-white/50 truncate">Ready to mix</p>
            </div>
          </div>

          <div class="space-y-1">
            <div class="flex justify-between text-[10px] font-mono text-white/40">
              <span>Fader Volume</span>
              <span id="deckBVolLabel">0%</span>
            </div>
            <div class="h-2 w-full bg-white/10 rounded-full overflow-hidden">
              <div id="deckBVolume" class="h-full bg-lime transition-all duration-75" style="width: 0%"></div>
            </div>
          </div>
        </div>

      </div>

      <!-- LIVE GUEST REQUESTS (from room.html) -->
      <div id="guestRequestsCard" class="hidden border border-lime/30 bg-lime/[0.03] rounded-3xl p-5 space-y-3 transition">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-lime animate-ping"></span>
            <h3 class="font-anton text-lg uppercase tracking-wide text-lime">Live Guest Requests</h3>
            <span id="guestReqCountBadge" class="bg-lime text-black font-mono font-bold text-xs px-2 py-0.5 rounded-full">0</span>
          </div>
          <span class="text-[11px] text-white/50 font-mono">Guests can request at <strong class="text-lime">/room.html</strong></span>
        </div>
        <div id="guestRequestsList" class="space-y-2 max-h-40 overflow-y-auto divide-y divide-white/5">
        </div>
      </div>

      <!-- UPCOMING QUEUE WITH FULL DRAG & DROP, SHUFFLE, AND REORDERING -->
      <div class="border border-white/10 rounded-3xl p-6 bg-white/[0.02] space-y-4">
        <div class="flex flex-wrap justify-between items-center gap-3">
          <div>
            <h3 class="font-anton text-2xl uppercase tracking-wide text-white/90">Party Queue</h3>
            <p class="text-[11px] text-white/40">Drag handles <strong class="text-white/70">⠿</strong> to reorder freely, or tap buttons to play now</p>
          </div>
          <div class="flex flex-wrap items-center gap-2">
            <button id="shuffleQueueBtn" class="bg-lime/10 border border-lime/30 hover:bg-lime hover:text-black text-lime font-anton px-4 py-2 rounded-xl text-xs uppercase tracking-wider transition flex items-center gap-1.5">
              <span>🔀</span> Shuffle Queue
            </button>
            <button id="exportSetlistBtn" class="border border-white/20 hover:border-lime hover:text-lime text-white/70 font-anton px-3 py-2 rounded-xl text-xs uppercase tracking-wider transition" title="Save current queue to JSON">
              💾 Export Set
            </button>
            <button id="retuneBtn" class="border border-white/10 hover:border-white/30 text-white/50 hover:text-white px-3 py-2 rounded-xl text-xs uppercase tracking-wider transition">
              Retune
            </button>
          </div>
        </div>

        <ol id="queueList" class="space-y-2 text-sm">
        </ol>
      </div>

      <!-- Live Event Engine Logs -->
      <div class="border border-white/10 rounded-2xl p-4 bg-black/40 text-xs font-mono text-white/50 space-y-1">
        <p class="text-white/30 uppercase text-[10px] font-bold">DJ Engine Log:</p>
        <div id="engineLog" class="h-24 overflow-y-auto space-y-1 text-white/70">
          <div>[NAUX] Ready to play {len(min_lib)} tracks. Tap APPROVE & PLAY to drop the hook.</div>
        </div>
      </div>

    </div>

  </main>

  <!-- ======================================================== -->
  <!-- FEATURE 1 MODAL: INTERACTIVE CUSTOM DJ SONG MAKER STUDIO -->
  <!-- ======================================================== -->
  <div id="djMakerModal" class="hidden fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
    <div class="bg-neutral-950 border-2 border-lime/50 rounded-3xl p-5 sm:p-7 max-w-2xl w-full space-y-5 shadow-2xl relative my-auto">
      
      <!-- Modal Header -->
      <div class="flex justify-between items-center border-b border-white/10 pb-4">
        <div class="flex items-center gap-2.5">
          <span class="text-2xl">🎛️</span>
          <div>
            <h3 class="font-anton text-2xl uppercase tracking-wider text-lime">Custom DJ Song Maker</h3>
            <p class="text-xs text-white/50">Make any track a DJ banger with custom drop-in and hook-cut points</p>
          </div>
        </div>
        <button id="closeDjMakerBtn" class="text-white/40 hover:text-white text-2xl font-mono p-1 transition">
          ✕
        </button>
      </div>

      <!-- Step 1: Song Source & Metadata -->
      <div class="space-y-3 bg-white/[0.02] border border-white/10 p-4 rounded-2xl">
        <label class="text-xs font-mono uppercase tracking-wider text-white/50 font-bold">1. Song Source (Paste YouTube URL or Search)</label>
        <div class="flex gap-2">
          <input id="djSongInput" type="text" placeholder="Paste YouTube URL/ID or search catalog..." 
                 class="flex-1 bg-black/60 border border-white/20 rounded-xl px-3.5 py-2.5 text-sm focus:outline-none focus:border-lime text-white">
          <button id="djLoadSongBtn" class="bg-lime text-black font-anton px-4 py-2.5 rounded-xl text-xs uppercase hover:brightness-110 transition whitespace-nowrap">
            Load Song
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
          <div>
            <label class="text-[10px] font-mono text-white/40 uppercase">Track Title</label>
            <input id="djTitleInput" type="text" placeholder="Title" class="w-full bg-black/40 border border-white/15 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-lime">
          </div>
          <div>
            <label class="text-[10px] font-mono text-white/40 uppercase">Artist / Singer</label>
            <input id="djArtistInput" type="text" placeholder="Artist" class="w-full bg-black/40 border border-white/15 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-lime">
          </div>
        </div>
      </div>

      <!-- Step 2: Interactive Video Preview & Live Playhead -->
      <div class="space-y-3 bg-white/[0.02] border border-white/10 p-4 rounded-2xl">
        <div class="flex justify-between items-center text-xs font-mono">
          <span class="text-white/50 uppercase font-bold">2. Audition &amp; Scrub Timeline</span>
          <span id="djPreviewTimeLabel" class="text-lime font-bold">0:00 / 0:00</span>
        </div>

        <!-- Embedded Preview Player Frame -->
        <div class="aspect-video max-h-48 w-full mx-auto rounded-xl overflow-hidden bg-black border border-white/10 shadow-lg relative">
          <div id="dj-preview-player" class="w-full h-full"></div>
        </div>

        <!-- Scrub Range -->
        <div class="space-y-1">
          <input id="djScrubSlider" type="range" min="0" max="180" value="0" class="w-full cursor-pointer h-2 bg-white/10 rounded-lg">
          <div class="flex justify-between text-[10px] font-mono text-white/40">
            <span>0:00</span>
            <span id="djTotalDurationLabel">3:00</span>
          </div>
        </div>
      </div>

      <!-- Step 3: Interactive DJ Cuer (Drop-in & Hook-cut) -->
      <div class="space-y-4 bg-white/[0.02] border border-white/10 p-4 rounded-2xl">
        <div class="flex justify-between items-center">
          <span class="text-xs font-mono uppercase tracking-wider text-white/50 font-bold">3. Set DJ Cue Points</span>
          <span class="text-[10px] font-mono text-lime bg-lime/10 px-2 py-0.5 rounded border border-lime/30">Equal-Power Drop</span>
        </div>

        <!-- DROP-IN START HOOK -->
        <div class="space-y-1.5 p-3 rounded-xl bg-black/40 border border-white/5">
          <div class="flex justify-between items-center text-xs font-mono">
            <span class="text-white font-bold flex items-center gap-1.5"><span class="text-lime">▶</span> Drop-in Beat (Hook Start):</span>
            <span id="djEntryLabel" class="text-lime font-bold text-sm">0:15</span>
          </div>
          <div class="flex items-center gap-3">
            <input id="djEntrySlider" type="range" min="0" max="180" value="15" class="flex-1 cursor-pointer">
            <input id="djEntryNum" type="number" min="0" max="600" value="15" class="w-16 bg-neutral-900 border border-white/20 rounded-lg px-2 py-1 text-xs font-mono text-lime text-center">
            <span class="text-[10px] text-white/40 font-mono">sec</span>
          </div>
          <div class="flex items-center gap-2 pt-1">
            <button id="setEntryToCurrentBtn" class="text-[11px] bg-white/10 hover:bg-white/20 text-white font-mono px-2.5 py-1 rounded-lg border border-white/20 transition">
              📍 Set Drop-in at Current Time
            </button>
            <button id="testEntryBtn" class="text-[11px] bg-lime/10 hover:bg-lime hover:text-black text-lime font-mono font-bold px-2.5 py-1 rounded-lg border border-lime/30 transition">
              ▶ Test Drop (6s)
            </button>
          </div>
        </div>

        <!-- HOOK CUT EXIT MIX -->
        <div class="space-y-1.5 p-3 rounded-xl bg-black/40 border border-white/5">
          <div class="flex justify-between items-center text-xs font-mono">
            <span class="text-white font-bold flex items-center gap-1.5"><span class="text-amber-400">⏹</span> Hook Cut / Mix Out:</span>
            <span id="djExitLabel" class="text-amber-400 font-bold text-sm">1:15</span>
          </div>
          <div class="flex items-center gap-3">
            <input id="djExitSlider" type="range" min="0" max="180" value="75" class="flex-1 cursor-pointer">
            <input id="djExitNum" type="number" min="0" max="600" value="75" class="w-16 bg-neutral-900 border border-white/20 rounded-lg px-2 py-1 text-xs font-mono text-amber-400 text-center">
            <span class="text-[10px] text-white/40 font-mono">sec</span>
          </div>
          <div class="flex items-center gap-2 pt-1">
            <button id="setExitToCurrentBtn" class="text-[11px] bg-white/10 hover:bg-white/20 text-white font-mono px-2.5 py-1 rounded-lg border border-white/20 transition">
              📍 Set Cut at Current Time
            </button>
            <button id="testExitBtn" class="text-[11px] bg-amber-400/10 hover:bg-amber-400 hover:text-black text-amber-300 font-mono font-bold px-2.5 py-1 rounded-lg border border-amber-400/30 transition">
              ▶ Test Hook Cut (4s)
            </button>
          </div>
        </div>

        <!-- Energy Vibe Selector -->
        <div class="flex items-center justify-between text-xs font-mono pt-1">
          <span class="text-white/40 uppercase">Vibe:</span>
          <div class="flex gap-2" id="djEnergyPicker">
            <button data-energy="5" class="dj-energy-btn px-3 py-1 rounded-lg border border-white/20 text-white/60 text-xs">Warmup</button>
            <button data-energy="8" class="dj-energy-btn px-3 py-1 rounded-lg border border-lime bg-lime/10 text-lime font-bold text-xs">Peak Party</button>
            <button data-energy="10" class="dj-energy-btn px-3 py-1 rounded-lg border border-white/20 text-white/60 text-xs">Banger 🔥</button>
          </div>
        </div>
      </div>

      <!-- Action Buttons Footer -->
      <div class="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-white/10">
        <button id="djTestFullSnippetBtn" class="border border-white/20 hover:border-lime hover:text-lime text-white/70 font-mono text-xs px-3 py-2.5 rounded-xl transition">
          ▶ Audition Full Hook
        </button>

        <div class="flex items-center gap-2">
          <button id="djSaveToLibBtn" class="border border-white/20 hover:border-white/50 text-white font-anton text-xs uppercase px-4 py-3 rounded-2xl transition">
            💾 Save to Library
          </button>
          <button id="djQueueTrackBtn" class="bg-white/10 hover:bg-white/20 text-white font-anton text-xs uppercase px-4 py-3 rounded-2xl transition">
            + Queue Track
          </button>
          <button id="djPlayNowBtn" class="bg-lime text-black font-anton text-xs uppercase px-5 py-3 rounded-2xl hover:brightness-110 active:scale-95 transition shadow-xl pulse-glow">
            ⚡ Play DJ Cut Now
          </button>
        </div>
      </div>

    </div>
  </div>

  <footer class="border-t border-white/10 p-4 text-center text-xs text-white/40 flex justify-between items-center max-w-4xl mx-auto w-full">
    <span>Reverse Engineered NAUX Dual-Deck Player ({len(min_lib)} Tracks)</span>
    <button id="footerOpenDjMakerBtn" class="text-lime hover:underline font-bold">Open DJ Maker Studio →</button>
  </footer>

  <script>
    if (window.location.protocol === 'file:') {{
      const notice = document.getElementById('fileNotice');
      if (notice) notice.classList.remove('hidden');
    }}

    const LIBRARY = {library_json};
    const TOP_ARTISTS = {top_artists_json};
    let selectedLangs = ['punjabi', 'hindi', 'english'];
    let selectedTime = 'peak';
    let selectedArtists = []; // Active artist filter list (empty = all artists)

    // Extract all unique artists sorted for search
    const ALL_ARTISTS = Array.from(new Set(
      LIBRARY.flatMap(s => {{
        return (s.artist || '').replace(/&/g, ',').replace(/feat\.?/gi, ',').split(',')
          .map(a => a.trim())
          .filter(a => a.length >= 2);
      }})
    )).sort((a, b) => a.localeCompare(b));

    function formatTime(sec) {{
      sec = Math.max(0, Math.floor(sec || 0));
      const m = Math.floor(sec / 60);
      const s = sec % 60;
      return `${{m}}:${{s < 10 ? '0' : ''}}${{s}}`;
    }}

    function logToScreen(msg) {{
      const el = document.getElementById('engineLog');
      if (!el) return;
      const d = document.createElement('div');
      d.textContent = `[${{new Date().toLocaleTimeString()}}] ${{msg}}`;
      el.appendChild(d);
      el.scrollTop = el.scrollHeight;
      console.log("[NAUX]", msg);
    }}

    // COUNT MATCHED SONGS FOR SELECTED ARTISTS
    function countMatchedSongs(artists) {{
      if (!artists || artists.length === 0) return LIBRARY.length;
      const lowers = artists.map(a => a.toLowerCase().trim());
      return LIBRARY.filter(s => {{
        const art = (s.artist || '').toLowerCase();
        return lowers.some(singer => art.includes(singer));
      }}).length;
    }}

    // UPDATE SELECTED ARTISTS UI TAGS
    function updateSelectedArtistsUI() {{
      const container = document.getElementById('selectedArtistsContainer');
      const badge = document.getElementById('artistMatchCountBadge');
      const clearBtn = document.getElementById('clearArtistsBtn');
      const liveText = document.getElementById('liveActiveSingersText');

      container.innerHTML = '';
      if (selectedArtists.length === 0) {{
        container.classList.add('hidden');
        badge.textContent = 'All Artists Active';
        clearBtn.classList.add('hidden');
        if (liveText) liveText.textContent = 'All Artists (Full Catalog)';
      }} else {{
        container.classList.remove('hidden');
        clearBtn.classList.remove('hidden');
        const count = countMatchedSongs(selectedArtists);
        badge.textContent = `${{count}} Songs Matched (${{selectedArtists.length}} Singers)`;
        if (liveText) liveText.textContent = selectedArtists.join(' + ') + ` (${{count}} tracks)`;

        selectedArtists.forEach(singer => {{
          const tag = document.createElement('span');
          tag.className = 'inline-flex items-center gap-1.5 bg-lime/10 border border-lime text-lime px-3 py-1 rounded-full text-xs font-bold font-mono';
          tag.innerHTML = `
            <span>${{singer}}</span>
            <button class="hover:text-white font-bold text-sm remove-singer-btn" data-name="${{singer}}">✕</button>
          `;
          tag.querySelector('.remove-singer-btn').addEventListener('click', (e) => {{
            e.stopPropagation();
            removeArtist(singer);
          }});
          container.appendChild(tag);
        }});
      }}

      // Refresh top artist pills active state
      document.querySelectorAll('.top-artist-pill').forEach(pill => {{
        const name = pill.dataset.name;
        if (selectedArtists.includes(name)) {{
          pill.className = 'top-artist-pill bg-lime text-black border border-lime px-3 py-1 rounded-xl text-xs font-bold transition flex items-center gap-1.5';
        }} else {{
          pill.className = 'top-artist-pill bg-white/5 hover:bg-white/10 text-white/70 border border-white/15 px-3 py-1 rounded-xl text-xs font-medium transition flex items-center gap-1.5';
        }}
      }});
    }}

    function addArtist(name) {{
      if (!name) return;
      if (!selectedArtists.includes(name)) {{
        selectedArtists.push(name);
        updateSelectedArtistsUI();
        logToScreen(`🎤 Added artist filter: "${{name}}"`);
      }}
    }}

    function removeArtist(name) {{
      selectedArtists = selectedArtists.filter(a => a !== name);
      updateSelectedArtistsUI();
      logToScreen(`Removed artist filter: "${{name}}"`);
    }}

    // POPULATE TOP ARTISTS PILLS
    const topArtistsContainer = document.getElementById('topArtistPills');
    TOP_ARTISTS.forEach(a => {{
      const btn = document.createElement('button');
      btn.className = 'top-artist-pill bg-white/5 hover:bg-white/10 text-white/70 border border-white/15 px-3 py-1 rounded-xl text-xs font-medium transition flex items-center gap-1.5';
      btn.dataset.name = a.name;
      btn.innerHTML = `<span>${{a.name}}</span><span class="opacity-50 text-[10px] font-mono">(${{a.count}})</span>`;
      btn.addEventListener('click', () => {{
        if (selectedArtists.includes(a.name)) {{
          removeArtist(a.name);
        }} else {{
          addArtist(a.name);
        }}
      }});
      topArtistsContainer.appendChild(btn);
    }});

    // ARTIST SEARCH AUTOCOMPLETE
    const artistSearchInput = document.getElementById('artistSearchInput');
    const artistSearchDropdown = document.getElementById('artistSearchDropdown');

    artistSearchInput.addEventListener('input', (e) => {{
      const q = e.target.value.toLowerCase().trim();
      if (q.length < 2) {{
        artistSearchDropdown.classList.add('hidden');
        return;
      }}

      const matches = ALL_ARTISTS.filter(a => a.toLowerCase().includes(q)).slice(0, 10);
      artistSearchDropdown.innerHTML = '';
      if (matches.length === 0) {{
        artistSearchDropdown.innerHTML = '<div class="p-2.5 text-xs text-white/40">No matching singer found in catalog.</div>';
      }} else {{
        matches.forEach(name => {{
          const row = document.createElement('div');
          row.className = 'p-2 hover:bg-white/10 rounded-xl flex items-center justify-between cursor-pointer transition text-xs';
          const matchCount = countMatchedSongs([name]);
          row.innerHTML = `
            <span class="font-bold text-white">${{name}}</span>
            <span class="text-lime font-mono text-[10px] bg-lime/10 px-2 py-0.5 rounded">${{matchCount}} tracks</span>
          `;
          row.addEventListener('click', () => {{
            addArtist(name);
            artistSearchInput.value = '';
            artistSearchDropdown.classList.add('hidden');
          }});
          artistSearchDropdown.appendChild(row);
        }});
      }}
      artistSearchDropdown.classList.remove('hidden');
    }});

    document.getElementById('clearArtistsBtn').addEventListener('click', () => {{
      selectedArtists = [];
      updateSelectedArtistsUI();
      logToScreen("Cleared all artist filters.");
    }});

    // SMART SETLIST BUILDER WITH MULTI-ARTIST SPOTLIGHT
    function buildSetlist(lib, languages, timeMood, singers = []) {{
      const energyTargets = {{
        warmup: 5.0,
        peak: 7.5,
        bangers: 8.8,
        winddown: 4.0
      }};
      const targetEnergy = energyTargets[timeMood] || 7.0;

      let pool = lib;

      // 1. FILTER BY SELECTED ARTISTS / SINGERS
      if (singers && singers.length > 0) {{
        const lowers = singers.map(s => s.toLowerCase().trim());
        pool = lib.filter(s => {{
          const art = (s.artist || '').toLowerCase();
          return lowers.some(singer => art.includes(singer));
        }});
        if (pool.length === 0) {{
          logToScreen("⚠️ No tracks found for selected singers, falling back to full library.");
          pool = lib;
        }}
      }} else {{
        // Standard language filter when no specific singers selected
        if (!languages.includes('all')) {{
          pool = lib.filter(s => languages.includes(s.language));
        }}
      }}
      if (pool.length < 5) pool = lib;

      // 2. SCORE BY ENERGY
      let scored = pool.map(s => {{
        let dist = Math.abs(s.energy - targetEnergy);
        let score = 10 - (dist * 2) + (s.banger ? 3 : 0) + (Math.random() * 2.0);
        return {{ song: s, score }};
      }}).sort((a, b) => b.score - a.score);

      let list = scored.map(item => ({{ ...item.song, play_full: false }}));

      // 3. SMART MULTI-ARTIST INTERLEAVING:
      // If multiple singers selected, alternate them!
      for (let i = 1; i < list.length; i++) {{
        const primary = s => (s.artist || '').split(/,|&|feat/i)[0].trim().toLowerCase();
        if (primary(list[i]) === primary(list[i - 1])) {{
          for (let j = i + 1; j < list.length; j++) {{
            if (primary(list[j]) !== primary(list[i - 1])) {{
              const temp = list[i];
              list[i] = list[j];
              list[j] = temp;
              break;
            }}
          }}
        }}
      }}
      return list.slice(0, 50);
    }}

    // BULLETPROOF STALL-PROOF DUAL-DECK ENGINE
    class NauxDualDeckEngine {{
      constructor() {{
        this.decks = {{
          A: {{ id: 'A', player: null, status: 'empty', role: null, cue: null, volume: 100, idIndex: 0, playFull: false, timer: null }},
          B: {{ id: 'B', player: null, status: 'empty', role: null, cue: null, volume: 0, idIndex: 0, playFull: false, timer: null }}
        }};
        this.liveId = 'A';
        this.crossfading = false;
        this.paused = false;
        this.queue = [];
        this.ready = false;
        this.awaitingStart = null;
        this.pendingHandoff = null;
        this.tickTimer = null;
        this.fadeTimer = null;
        this.masterVolume = 100;
        this.crossfadeDuration = 1500;
      }}

      async init() {{
        logToScreen("Connecting YouTube Players...");
        await this.loadYT();
        await Promise.all([
          this.createPlayer('A', 'deck-A-player'),
          this.createPlayer('B', 'deck-B-player')
        ]);
        this.ready = true;
        logToScreen("Both Deck A & Deck B ready.");

        this.tickTimer = setInterval(() => this.tick(), 250);
        document.getElementById('ytStatusBadge').innerHTML = '<span class="w-2 h-2 rounded-full bg-lime"></span> Decks Ready';
      }}

      loadYT() {{
        return new Promise((resolve) => {{
          if (window.YT && window.YT.Player) return resolve(window.YT);
          window.onYouTubeIframeAPIReady = () => resolve(window.YT);
          const tag = document.createElement('script');
          tag.src = "https://www.youtube.com/iframe_api";
          document.head.appendChild(tag);
        }});
      }}

      createPlayer(deckId, domId) {{
        return new Promise((resolve) => {{
          const vars = {{
            autoplay: 0,
            controls: 0,
            disablekb: 1,
            fs: 0,
            playsinline: 1,
            rel: 0,
            enablejsapi: 1
          }};
          if (window.location.protocol.startsWith('http')) {{
            vars.origin = window.location.origin;
          }}

          this.decks[deckId].player = new YT.Player(domId, {{
            width: '320',
            height: '180',
            playerVars: vars,
            events: {{
              onReady: () => {{
                logToScreen(`Deck ${{deckId}} initialized.`);
                resolve();
              }},
              onStateChange: (e) => this.onStateChange(this.decks[deckId], e.data),
              onError: (e) => this.onError(this.decks[deckId], e.data)
            }}
          }});
        }});
      }}

      start(setlist) {{
        if (!this.ready || setlist.length === 0) return;
        this.queue = setlist.slice();
        
        const first = this.queue.shift();
        this.liveId = 'A';
        this.assign(this.decks.A, first);
        this.load(this.decks.A, 'live');

        this.preloadNextOn(this.decks.B);
        this.updateUI();
        renderQueue(this.queue);
      }}

      assign(deck, cue) {{
        deck.cue = cue;
        deck.idIndex = 0;
        deck.playFull = false;
      }}

      clearTimer(deck) {{
        if (deck.timer) {{
          clearTimeout(deck.timer);
          deck.timer = null;
        }}
      }}

      load(deck, role) {{
        const cue = deck.cue;
        if (!cue) return;
        const vid = cue.youtube_ids[deck.idIndex] || cue.youtube_ids[0];
        
        this.clearTimer(deck);
        deck.status = 'loading';
        deck.role = role;

        const startSec = deck.playFull ? 0 : (cue.entry_sec || 0);
        logToScreen(`Deck ${{deck.id}} cueing "${{cue.title}}" at ${{startSec}}s (${{role}}) [ID: ${{vid}}]`);

        if (role === 'preload') {{
          deck.player.mute();
          deck.player.setVolume(0);
          deck.volume = 0;
        }} else {{
          deck.player.unMute();
          const targetVol = Math.round((100 * this.masterVolume) / 100);
          deck.player.setVolume(targetVol);
          deck.volume = 100;
        }}

        deck.player.loadVideoById({{
          videoId: vid,
          startSeconds: startSec
        }});

        // 5-SECOND BUFFER SAFETY TIMEOUT:
        deck.timer = setTimeout(() => {{
          logToScreen(`⚠️ Deck ${{deck.id}} buffering timeout (5s) on "${{cue.title}}". Advancing to fallback...`);
          this.nextSource(deck);
        }}, 5000);

        if (role === 'live') {{
          deck.player.playVideo();
          setTimeout(() => {{
            try {{
              if (deck.player.getPlayerState() !== 1) {{
                document.getElementById('unmutePrompt').classList.remove('hidden');
              }}
            }} catch(e) {{}}
          }}, 1200);
        }}
        this.updateUI();
      }}

      nextSource(deck) {{
        this.clearTimer(deck);
        const cue = deck.cue;
        if (!cue) return;

        deck.idIndex += 1;
        if (deck.idIndex < cue.youtube_ids.length) {{
          logToScreen(`Deck ${{deck.id}} trying fallback source ${{deck.idIndex + 1}}/${{cue.youtube_ids.length}} for "${{cue.title}}"...`);
          this.load(deck, deck.role);
          return;
        }}

        // ALL SOURCES FOR THIS TRACK FAILED: PURGE IT PERMANENTLY FROM QUEUE!
        logToScreen(`⚠️ Dropping "${{cue.title}}" (embed blocked or stream failed). Advancing queue...`);
        this.queue = this.queue.filter(s => s.song_id !== cue.song_id);
        renderQueue(this.queue);

        if (deck.role === 'live') {{
          deck.status = 'empty';
          deck.cue = null;
          this.updateUI();
          this.requestHandoff('error');
        }} else {{
          this.preloadNextOn(deck);
        }}
      }}

      preloadNextOn(deck) {{
        if (this.queue.length === 0) {{
          deck.status = 'empty';
          deck.cue = null;
          this.updateUI();
          return;
        }}
        const nextCue = this.queue[0];
        this.assign(deck, nextCue);
        this.load(deck, 'preload');
      }}

      forceSkipStuckDeck(deck) {{
        this.clearTimer(deck);
        const stuck = deck.cue;
        if (stuck) {{
          logToScreen(`⚡ Auto-purging stuck track "${{stuck.title}}" from queue.`);
          this.queue = this.queue.filter(s => s.song_id !== stuck.song_id);
          renderQueue(this.queue);
        }}

        if (this.queue.length === 0) {{
          logToScreen("Queue is empty. No more tracks to load.");
          deck.status = 'empty';
          deck.cue = null;
          this.updateUI();
          return;
        }}

        const nextSong = this.queue[0];
        this.assign(deck, nextSong);
        this.load(deck, 'preload');
        this.startIncoming(deck, 'recovery_auto_drop');
      }}

      onStateChange(deck, state) {{
        // State 1: PLAYING
        if (state === 1) {{
          if (this.awaitingStart === deck.id) {{
            this.startFade(deck);
          }} else if (deck.status === 'loading' && deck.role === 'preload') {{
            this.clearTimer(deck);
            deck.player.pauseVideo();
            deck.player.seekTo(deck.cue.entry_sec || 0, true);
            deck.status = 'ready';
            logToScreen(`✓ Deck ${{deck.id}} primed at hook (${{deck.cue.entry_sec}}s). Ready for mix!`);
            this.updateUI();
            
            if (this.pendingHandoff) {{
              const reason = this.pendingHandoff;
              this.pendingHandoff = null;
              this.requestHandoff(reason);
            }}
          }} else if (deck.status === 'loading' && deck.role === 'live') {{
            this.clearTimer(deck);
            deck.status = 'live';
            document.getElementById('unmutePrompt').classList.add('hidden');
            logToScreen(`Deck ${{deck.id}} is LIVE & PLAYING.`);
            this.updateLiveTrackMetadata(deck.cue);
            this.updateUI();
          }}
        }} 
        // State 5: CUED or State 2: PAUSED
        else if (state === 5 || state === 2) {{
          if (deck.status === 'loading' && deck.role === 'preload') {{
            this.clearTimer(deck);
            deck.status = 'ready';
            logToScreen(`✓ Deck ${{deck.id}} ready (state ${{state}}): "${{deck.cue.title}}"`);
            this.updateUI();
            if (this.pendingHandoff) {{
              const reason = this.pendingHandoff;
              this.pendingHandoff = null;
              this.requestHandoff(reason);
            }}
          }}
        }} 
        // State 0: ENDED
        else if (state === 0) {{
          if (deck.id === this.liveId && !this.crossfading) {{
            this.requestHandoff('ended');
          }}
        }}
      }}

      onError(deck, err) {{
        logToScreen(`Deck ${{deck.id}} YouTube error code ${{err}} on "${{deck.cue?.title}}"`);
        if (this.awaitingStart === deck.id) {{
          this.failIncoming(deck);
        }} else if (deck.status === 'loading' || deck.status === 'ready') {{
          this.nextSource(deck);
        }} else if (deck.id === this.liveId && deck.status === 'live') {{
          this.requestHandoff('error');
        }}
      }}

      tick() {{
        if (this.paused || this.crossfading || this.awaitingStart) return;
        const live = this.decks[this.liveId];
        if (!live || !live.player || live.status !== 'live') return;

        let curTime = 0;
        try {{ curTime = live.player.getCurrentTime() || 0; }} catch(e) {{ return; }}

        const duration = live.cue.duration_sec || live.player.getDuration() || 180;
        const cutAt = live.playFull ? (duration - 1.5) : (live.cue.exit_sec || duration - 1.5);

        const pct = Math.min(100, Math.max(0, (curTime / cutAt) * 100));
        document.getElementById('progressBar').style.width = `${{pct}}%`;
        document.getElementById('currentTimeLabel').textContent = formatTime(curTime);

        // Check if cut point reached!
        if (curTime >= cutAt) {{
          const otherId = this.liveId === 'A' ? 'B' : 'A';
          const other = this.decks[otherId];

          if (other.status === 'loading') {{
            const holdSec = (curTime - cutAt).toFixed(1);
            document.getElementById('cutPointLabel').innerHTML = `<span class="text-amber-400 font-bold">⏳ Buffering next (${{holdSec}}s / 3.0s)...</span>`;
          }} else {{
            document.getElementById('cutPointLabel').textContent = live.playFull 
              ? `Playing Full (${{formatTime(duration)}})` 
              : `Hook Cut @ ${{formatTime(cutAt)}}`;
          }}

          // SAFETY VALVE: Max 3 seconds holding grace period
          if (curTime >= cutAt + 3.0 && other.status === 'loading') {{
            logToScreen(`⚠️ Live track reached +3s grace period while Deck ${{other.id}} was buffering. Auto-dropping stuck track!`);
            this.forceSkipStuckDeck(other);
            return;
          }}

          this.requestHandoff('hook_cut');
        }} else {{
          document.getElementById('cutPointLabel').textContent = live.playFull 
            ? `Playing Full (${{formatTime(duration)}})` 
            : `Hook Cut @ ${{formatTime(cutAt)}}`;
        }}
      }}

      requestHandoff(reason) {{
        if (this.crossfading || this.awaitingStart) return;
        const nextId = this.liveId === 'A' ? 'B' : 'A';
        const nextDeck = this.decks[nextId];

        if (nextDeck.status === 'ready') {{
          this.startIncoming(nextDeck, reason);
        }} else if (nextDeck.status === 'loading') {{
          if (!this.pendingHandoff) {{
            logToScreen(`Next track still buffering. Holding live Deck ${{this.liveId}}...`);
          }}
          this.pendingHandoff = reason;
        }} else if (nextDeck.status === 'empty') {{
          logToScreen("End of party set reached.");
        }}
      }}

      startIncoming(deck, reason) {{
        this.pendingHandoff = reason;
        this.awaitingStart = deck.id;
        const player = deck.player;

        player.setVolume(0);
        player.unMute();
        player.playVideo();

        logToScreen(`Triggering incoming Deck ${{deck.id}} ("${{deck.cue.title}}"). Awaiting playback...`);

        deck.timer = setTimeout(() => {{
          logToScreen(`Deck ${{deck.id}} did not start in time (4s timeout). Failing incoming...`);
          this.failIncoming(deck);
        }}, 4000);
      }}

      failIncoming(deck) {{
        this.clearTimer(deck);
        this.awaitingStart = null;
        try {{ deck.player.mute(); }} catch(e) {{}}
        this.nextSource(deck);
      }}

      startFade(incoming) {{
        this.clearTimer(incoming);
        this.awaitingStart = null;
        this.pendingHandoff = null;

        const outgoing = this.decks[this.liveId];
        incoming.status = 'live';
        incoming.role = 'live';
        this.liveId = incoming.id;
        this.crossfading = true;

        if (this.queue.length > 0 && this.queue[0].song_id === incoming.cue.song_id) {{
          this.queue.shift();
        }}

        document.getElementById('crossfadeIndicator').classList.remove('hidden');
        logToScreen(`⚡ Mixing into "${{incoming.cue.title}}" on Deck ${{incoming.id}} (${{this.crossfadeDuration / 1000}}s curve)`);

        const start = performance.now();
        const FADE_MS = this.crossfadeDuration || 1500;

        if (this.fadeTimer) clearInterval(this.fadeTimer);
        this.fadeTimer = setInterval(() => {{
          const elapsed = performance.now() - start;
          const s = Math.min(1, elapsed / FADE_MS);

          const rawIn = Math.round(100 * Math.sin(s * Math.PI / 2));
          const rawOut = Math.round(100 * Math.cos(s * Math.PI / 2));

          incoming.volume = rawIn;
          outgoing.volume = rawOut;

          const inVol = Math.round((rawIn * this.masterVolume) / 100);
          const outVol = Math.round((rawOut * this.masterVolume) / 100);

          try {{
            incoming.player.setVolume(inVol);
            outgoing.player.setVolume(outVol);
          }} catch(e) {{}}

          this.updateUI();

          if (s >= 1) {{
            clearInterval(this.fadeTimer);
            this.fadeTimer = null;
            this.crossfading = false;
            document.getElementById('crossfadeIndicator').classList.add('hidden');

            try {{
              outgoing.player.pauseVideo();
              outgoing.player.mute();
            }} catch(e) {{}}

            outgoing.status = 'empty';
            outgoing.cue = null;
            this.updateLiveTrackMetadata(incoming.cue);
            this.updateUI();

            this.preloadNextOn(outgoing);
            renderQueue(this.queue);
          }}
        }}, 40);
      }}

      skip() {{
        logToScreen("Skip pressed.");
        const nextId = this.liveId === 'A' ? 'B' : 'A';
        const nextDeck = this.decks[nextId];

        if (nextDeck.status === 'loading') {{
          logToScreen(`Next deck is currently buffering. Force-advancing to next song...`);
          this.forceSkipStuckDeck(nextDeck);
        }} else if (nextDeck.status === 'ready') {{
          this.startIncoming(nextDeck, 'skip');
        }} else {{
          if (this.queue.length > 0) {{
            this.forceSkipStuckDeck(nextDeck);
          }}
        }}
      }}

      playNow(song) {{
        logToScreen(`⚡ Immediate Play Now: "${{song.title}}"`);
        const nextId = this.liveId === 'A' ? 'B' : 'A';
        const nextDeck = this.decks[nextId];

        this.queue = this.queue.filter(s => s.song_id !== song.song_id);
        this.queue.unshift(song);

        this.assign(nextDeck, song);
        this.load(nextDeck, 'preload');
        this.startIncoming(nextDeck, 'user_play_now');
        renderQueue(this.queue);
      }}

      queueNext(song) {{
        this.queue = this.queue.filter(s => s.song_id !== song.song_id);
        this.queue.unshift(song);
        logToScreen(`Placed "${{song.title}}" next in queue!`);

        const otherId = this.liveId === 'A' ? 'B' : 'A';
        const otherDeck = this.decks[otherId];
        this.assign(otherDeck, song);
        this.load(otherDeck, 'preload');

        renderQueue(this.queue);
      }}

      queueTrack(song) {{
        this.queue.push(song);
        logToScreen(`Added "${{song.title}}" to party queue.`);
        
        const otherId = this.liveId === 'A' ? 'B' : 'A';
        const otherDeck = this.decks[otherId];
        if (otherDeck.status === 'empty') {{
          this.preloadNextOn(otherDeck);
        }}
        renderQueue(this.queue);
      }}

      shuffleQueue() {{
        if (this.queue.length <= 1) return;
        for (let i = this.queue.length - 1; i > 0; i--) {{
          const j = Math.floor(Math.random() * (i + 1));
          [this.queue[i], this.queue[j]] = [this.queue[j], this.queue[i]];
        }}
        logToScreen("🔀 Queue shuffled!");
        const otherId = this.liveId === 'A' ? 'B' : 'A';
        const otherDeck = this.decks[otherId];
        this.preloadNextOn(otherDeck);
        renderQueue(this.queue);
      }}

      reorderQueue(fromIdx, toIdx) {{
        if (fromIdx === toIdx || fromIdx < 0 || toIdx < 0 || fromIdx >= this.queue.length || toIdx >= this.queue.length) return;
        const [moved] = this.queue.splice(fromIdx, 1);
        this.queue.splice(toIdx, 0, moved);
        logToScreen(`Moved "${{moved.title}}" to position ${{toIdx + 1}} in queue.`);

        const otherId = this.liveId === 'A' ? 'B' : 'A';
        const otherDeck = this.decks[otherId];
        this.preloadNextOn(otherDeck);
        renderQueue(this.queue);
      }}

      removeItem(idx) {{
        if (idx < 0 || idx >= this.queue.length) return;
        const [removed] = this.queue.splice(idx, 1);
        logToScreen(`Removed "${{removed.title}}" from queue.`);

        if (idx === 0) {{
          const otherId = this.liveId === 'A' ? 'B' : 'A';
          const otherDeck = this.decks[otherId];
          this.preloadNextOn(otherDeck);
        }}
        renderQueue(this.queue);
      }}

      togglePlay() {{
        const live = this.decks[this.liveId];
        if (!live || !live.player) return false;
        if (this.paused) {{
          live.player.playVideo();
          this.paused = false;
        }} else {{
          live.player.pauseVideo();
          this.paused = true;
        }}
        return this.paused;
      }}

      togglePlayFull() {{
        const live = this.decks[this.liveId];
        if (!live) return false;
        live.playFull = !live.playFull;
        logToScreen(live.playFull ? "Full song mode on." : "Hook cut mode on.");
        return live.playFull;
      }}

      updateLiveTrackMetadata(cue) {{
        if (!cue) return;
        document.getElementById('nowPlayingTitle').textContent = cue.title;
        document.getElementById('nowPlayingArtist').textContent = cue.artist;
        renderQueue(this.queue);

        if ('mediaSession' in navigator) {{
          try {{
            navigator.mediaSession.metadata = new MediaMetadata({{
              title: cue.title,
              artist: cue.artist,
              album: 'NAUX Party Set',
              artwork: [
                {{ src: `https://img.youtube.com/vi/${{cue.youtube_ids[0]}}/hqdefault.jpg`, sizes: '480x360', type: 'image/jpeg' }}
              ]
            }});
            navigator.mediaSession.playbackState = 'playing';
          }} catch(e) {{}}
        }}

        // Sync with mobile room (/api/room/update)
        if (window.location.protocol.startsWith('http')) {{
          fetch('/api/room/update', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
              room_code: 'AUX1',
              now_playing: {{ title: cue.title, artist: cue.artist }},
              queue: this.queue.map(s => ({{ title: s.title, artist: s.artist }}))
            }})
          }}).catch(() => {{}});
        }}
      }}

      updateUI() {{
        const dA = this.decks.A;
        const dB = this.decks.B;

        document.getElementById('deckAStatus').textContent = `${{dA.status.toUpperCase()}} (${{dA.volume}}%)`;
        document.getElementById('deckAVolume').style.width = `${{dA.volume}}%`;
        document.getElementById('deckAVolLabel').textContent = `${{dA.volume}}%`;
        document.getElementById('deckASong').textContent = dA.cue ? dA.cue.title : 'Empty';
        document.getElementById('deckAArtist').textContent = dA.cue ? dA.cue.artist : '-';

        document.getElementById('deckBStatus').textContent = `${{dB.status.toUpperCase()}} (${{dB.volume}}%)`;
        document.getElementById('deckBVolume').style.width = `${{dB.volume}}%`;
        document.getElementById('deckBVolLabel').textContent = `${{dB.volume}}%`;
        document.getElementById('deckBSong').textContent = dB.cue ? dB.cue.title : 'Empty';
        document.getElementById('deckBArtist').textContent = dB.cue ? dB.cue.artist : '-';

        const eqA = document.getElementById('deckAEq');
        const eqB = document.getElementById('deckBEq');
        if (this.liveId === 'A') {{
          eqA.className = 'flex items-end gap-1 h-8 w-8 opacity-100';
          eqB.className = 'flex items-end gap-1 h-8 w-8 opacity-30';
        }} else {{
          eqA.className = 'flex items-end gap-1 h-8 w-8 opacity-30';
          eqB.className = 'flex items-end gap-1 h-8 w-8 opacity-100';
        }}

        document.getElementById('deckAMonitor').className = this.liveId === 'A'
          ? 'p-5 rounded-3xl border-2 border-lime bg-white/[0.04] space-y-3 transition shadow-lg pulse-glow'
          : 'p-5 rounded-3xl border border-white/10 bg-white/[0.02] space-y-3 transition opacity-60';

        document.getElementById('deckBMonitor').className = this.liveId === 'B'
          ? 'p-5 rounded-3xl border-2 border-lime bg-white/[0.04] space-y-3 transition shadow-lg pulse-glow'
          : 'p-5 rounded-3xl border border-white/10 bg-white/[0.02] space-y-3 transition opacity-60';

        document.getElementById('activeDeckPill').textContent = `Deck ${{this.liveId}} Live`;
      }}
    }}

    const engine = new NauxDualDeckEngine();
    engine.init();

    // INTERACTIVE QUEUE RENDERER
    let draggedIndex = null;

    function renderQueue(list) {{
      const queueListEl = document.getElementById('queueList');
      queueListEl.innerHTML = '';

      if (!list || list.length === 0) {{
        queueListEl.innerHTML = '<li class="text-xs text-white/40 text-center py-6">Queue is empty. Search any artist above or click Shuffle!</li>';
        return;
      }}

      list.forEach((s, idx) => {{
        const li = document.createElement('li');
        li.className = 'queue-item bg-white/[0.02] hover:bg-white/[0.05] border border-white/10 rounded-2xl p-3 flex items-center justify-between gap-3 transition cursor-grab active:cursor-grabbing';
        li.draggable = true;
        li.dataset.index = idx;

        li.innerHTML = `
          <div class="flex items-center gap-3 min-w-0">
            <span class="text-white/30 font-mono text-xs select-none">⠿</span>
            <span class="text-xs font-mono text-lime font-bold w-5">${{idx + 1}}</span>
            <div class="truncate">
              <p class="font-bold text-white text-sm truncate">${{s.title}}</p>
              <p class="text-xs text-white/40 truncate">${{s.artist}} · ${{formatTime(s.entry_sec)}} ➔ ${{formatTime(s.exit_sec)}}</p>
            </div>
          </div>
          <div class="flex items-center gap-1.5 shrink-0">
            <button class="dj-edit-item-btn border border-lime/30 bg-lime/5 hover:bg-lime hover:text-black text-lime font-anton text-xs px-2.5 py-1.5 rounded-xl transition" data-id="${{s.song_id}}" title="Customize DJ Drop & Cut for this track">
              🎛️ DJ
            </button>
            <button class="play-now-btn bg-lime/10 hover:bg-lime hover:text-black text-lime font-anton text-xs px-2.5 py-1.5 rounded-xl transition" data-id="${{s.song_id}}" title="Play this song right now">
              ⚡ Play
            </button>
            <button class="remove-btn text-white/30 hover:text-red-400 p-1.5 transition text-xs" data-index="${{idx}}" title="Remove from queue">
              ✕
            </button>
          </div>
        `;

        li.addEventListener('dragstart', (e) => {{
          draggedIndex = idx;
          li.classList.add('dragging');
          e.dataTransfer.effectAllowed = 'move';
        }});

        li.addEventListener('dragend', () => {{
          li.classList.remove('dragging');
          document.querySelectorAll('.queue-item').forEach(el => el.classList.remove('drag-over'));
        }});

        li.addEventListener('dragover', (e) => {{
          e.preventDefault();
          e.dataTransfer.dropEffect = 'move';
          li.classList.add('drag-over');
        }});

        li.addEventListener('dragleave', () => {{
          li.classList.remove('drag-over');
        }});

        li.addEventListener('drop', (e) => {{
          e.preventDefault();
          li.classList.remove('drag-over');
          if (draggedIndex !== null && draggedIndex !== idx) {{
            engine.reorderQueue(draggedIndex, idx);
          }}
          draggedIndex = null;
        }});

        queueListEl.appendChild(li);
      }});

      // Attach button events
      document.querySelectorAll('.play-now-btn').forEach(btn => {{
        btn.addEventListener('click', (e) => {{
          e.stopPropagation();
          const songId = btn.dataset.id;
          const found = LIBRARY.find(s => s.song_id === songId) || engine.queue.find(s => s.song_id === songId);
          if (found) engine.playNow(found);
        }});
      }});

      document.querySelectorAll('.dj-edit-item-btn').forEach(btn => {{
        btn.addEventListener('click', (e) => {{
          e.stopPropagation();
          const songId = btn.dataset.id;
          const found = LIBRARY.find(s => s.song_id === songId) || engine.queue.find(s => s.song_id === songId);
          if (found) openDjMakerWithSong(found);
        }});
      }});

      document.querySelectorAll('.remove-btn').forEach(btn => {{
        btn.addEventListener('click', (e) => {{
          e.stopPropagation();
          const idx = parseInt(btn.dataset.index, 10);
          engine.removeItem(idx);
        }});
      }});
    }}

    // ========================================================
    // FEATURE 1: INTERACTIVE DJ MAKER ENGINE & CONTROLS
    // ========================================================
    let djPreviewPlayer = null;
    let djPreviewTimer = null;
    let djAuditionTimeout = null;
    let currentDjVid = 'uTuchIYZdbM';
    let currentDjDuration = 180;
    let selectedDjEnergy = 8;

    function openDjMakerModal() {{
      document.getElementById('djMakerModal').classList.remove('hidden');
      initDjPreviewPlayer();
    }}

    function closeDjMakerModal() {{
      if (djPreviewPlayer) {{
        try {{ djPreviewPlayer.pauseVideo(); }} catch(e) {{}}
      }}
      if (djAuditionTimeout) clearTimeout(djAuditionTimeout);
      document.getElementById('djMakerModal').classList.add('hidden');
    }}

    function openDjMakerWithSong(song) {{
      if (!song) return;
      openDjMakerModal();
      document.getElementById('djSongInput').value = song.youtube_ids ? song.youtube_ids[0] : '';
      document.getElementById('djTitleInput').value = song.title || '';
      document.getElementById('djArtistInput').value = song.artist || '';

      const entry = song.entry_sec || 0;
      const exit = song.exit_sec || song.duration_sec || 180;
      const dur = song.duration_sec || exit || 180;

      currentDjDuration = dur;
      updateDjSlidersMax(dur);

      setDjEntry(entry);
      setDjExit(exit);

      const vid = (song.youtube_ids && song.youtube_ids[0]) ? song.youtube_ids[0] : 'uTuchIYZdbM';
      loadVideoInDjPreview(vid);
    }}

    function initDjPreviewPlayer() {{
      if (djPreviewPlayer) return;
      if (!window.YT || !window.YT.Player) return;

      djPreviewPlayer = new YT.Player('dj-preview-player', {{
        width: '100%',
        height: '100%',
        videoId: currentDjVid,
        playerVars: {{
          autoplay: 0,
          controls: 1,
          playsinline: 1,
          rel: 0,
          enablejsapi: 1
        }},
        events: {{
          onReady: () => {{
            startDjPreviewScrubber();
          }},
          onStateChange: (e) => {{
            if (e.data === 1) {{
              const d = djPreviewPlayer.getDuration();
              if (d && d > 10) {{
                currentDjDuration = Math.floor(d);
                updateDjSlidersMax(currentDjDuration);
              }}
            }}
          }}
        }}
      }});
    }}

    function loadVideoInDjPreview(vid) {{
      currentDjVid = vid;
      if (djPreviewPlayer && djPreviewPlayer.loadVideoById) {{
        djPreviewPlayer.loadVideoById(vid);
      }}
    }}

    function updateDjSlidersMax(maxSec) {{
      document.getElementById('djScrubSlider').max = maxSec;
      document.getElementById('djEntrySlider').max = maxSec;
      document.getElementById('djExitSlider').max = maxSec;
      document.getElementById('djTotalDurationLabel').textContent = formatTime(maxSec);
    }}

    function setDjEntry(sec) {{
      sec = Math.max(0, Math.floor(sec));
      document.getElementById('djEntrySlider').value = sec;
      document.getElementById('djEntryNum').value = sec;
      document.getElementById('djEntryLabel').textContent = formatTime(sec);
    }}

    function setDjExit(sec) {{
      sec = Math.max(0, Math.floor(sec));
      document.getElementById('djExitSlider').value = sec;
      document.getElementById('djExitNum').value = sec;
      document.getElementById('djExitLabel').textContent = formatTime(sec);
    }}

    function startDjPreviewScrubber() {{
      if (djPreviewTimer) clearInterval(djPreviewTimer);
      djPreviewTimer = setInterval(() => {{
        if (!djPreviewPlayer || typeof djPreviewPlayer.getCurrentTime !== 'function') return;
        try {{
          const cur = djPreviewPlayer.getCurrentTime() || 0;
          const dur = djPreviewPlayer.getDuration() || currentDjDuration;
          document.getElementById('djPreviewTimeLabel').textContent = `${{formatTime(cur)}} / ${{formatTime(dur)}}`;
          document.getElementById('djScrubSlider').value = Math.floor(cur);
        }} catch(e) {{}}
      }}, 300);
    }}

    // Audition Helpers
    function auditionSnippet(fromSec, durationSec) {{
      if (!djPreviewPlayer) return;
      if (djAuditionTimeout) clearTimeout(djAuditionTimeout);
      djPreviewPlayer.seekTo(fromSec, true);
      djPreviewPlayer.unMute();
      djPreviewPlayer.playVideo();

      djAuditionTimeout = setTimeout(() => {{
        try {{ djPreviewPlayer.pauseVideo(); }} catch(e) {{}}
      }}, durationSec * 1000);
    }}

    // DJ Maker Modal Listeners
    document.getElementById('closeDjMakerBtn').addEventListener('click', closeDjMakerModal);
    document.getElementById('headerOpenDjMakerBtn').addEventListener('click', openDjMakerModal);
    document.getElementById('setupMakeDjBtn').addEventListener('click', openDjMakerModal);
    document.getElementById('openDjMakerSearchBtn').addEventListener('click', openDjMakerModal);
    document.getElementById('footerOpenDjMakerBtn').addEventListener('click', openDjMakerModal);

    document.getElementById('djCurrentSongBtn').addEventListener('click', () => {{
      const live = engine.decks[engine.liveId];
      if (live && live.cue) {{
        openDjMakerWithSong(live.cue);
      }} else {{
        openDjMakerModal();
      }}
    }});

    // Load song in DJ maker
    document.getElementById('djLoadSongBtn').addEventListener('click', () => {{
      const val = document.getElementById('djSongInput').value.trim();
      if (!val) return;

      const ytMatch = val.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([a-zA-Z0-9_-]{{11}})/);
      if (ytMatch) {{
        const vid = ytMatch[1];
        loadVideoInDjPreview(vid);
        if (!document.getElementById('djTitleInput').value) {{
          document.getElementById('djTitleInput').value = `Custom DJ Track (${{vid}})`;
          document.getElementById('djArtistInput').value = 'Custom Artist';
        }}
        return;
      }}

      // Search in library
      const found = LIBRARY.find(s => s.title.toLowerCase().includes(val.toLowerCase()) || s.artist.toLowerCase().includes(val.toLowerCase()));
      if (found) {{
        openDjMakerWithSong(found);
      }} else if (val.length === 11) {{
        loadVideoInDjPreview(val);
      }} else {{
        alert("Enter a YouTube URL (or video ID) or search a song title from the library.");
      }}
    }});

    // Scrub slider
    document.getElementById('djScrubSlider').addEventListener('input', (e) => {{
      const sec = parseInt(e.target.value, 10);
      if (djPreviewPlayer) djPreviewPlayer.seekTo(sec, true);
    }});

    // Drop-in slider & num
    document.getElementById('djEntrySlider').addEventListener('input', (e) => {{
      setDjEntry(e.target.value);
    }});
    document.getElementById('djEntryNum').addEventListener('input', (e) => {{
      setDjEntry(e.target.value);
    }});

    // Exit slider & num
    document.getElementById('djExitSlider').addEventListener('input', (e) => {{
      setDjExit(e.target.value);
    }});
    document.getElementById('djExitNum').addEventListener('input', (e) => {{
      setDjExit(e.target.value);
    }});

    // Snap to current playing position buttons
    document.getElementById('setEntryToCurrentBtn').addEventListener('click', () => {{
      if (djPreviewPlayer && djPreviewPlayer.getCurrentTime) {{
        const cur = Math.floor(djPreviewPlayer.getCurrentTime());
        setDjEntry(cur);
      }}
    }});
    document.getElementById('setExitToCurrentBtn').addEventListener('click', () => {{
      if (djPreviewPlayer && djPreviewPlayer.getCurrentTime) {{
        const cur = Math.floor(djPreviewPlayer.getCurrentTime());
        setDjExit(cur);
      }}
    }});

    // Test buttons
    document.getElementById('testEntryBtn').addEventListener('click', () => {{
      const entry = parseInt(document.getElementById('djEntrySlider').value, 10) || 0;
      auditionSnippet(entry, 6);
    }});
    document.getElementById('testExitBtn').addEventListener('click', () => {{
      const exit = parseInt(document.getElementById('djExitSlider').value, 10) || 60;
      const start = Math.max(0, exit - 4);
      auditionSnippet(start, 4.5);
    }});
    document.getElementById('djTestFullSnippetBtn').addEventListener('click', () => {{
      const entry = parseInt(document.getElementById('djEntrySlider').value, 10) || 0;
      const exit = parseInt(document.getElementById('djExitSlider').value, 10) || 60;
      const duration = Math.max(1, exit - entry);
      auditionSnippet(entry, Math.min(duration, 40));
    }});

    // Energy picker
    document.querySelectorAll('.dj-energy-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        selectedDjEnergy = parseInt(btn.dataset.energy, 10);
        document.querySelectorAll('.dj-energy-btn').forEach(b => {{
          b.className = b.dataset.energy == selectedDjEnergy
            ? 'dj-energy-btn px-3 py-1 rounded-lg border border-lime bg-lime/10 text-lime font-bold text-xs'
            : 'dj-energy-btn px-3 py-1 rounded-lg border border-white/20 text-white/60 text-xs';
        }});
      }});
    }});

    function getCustomDjTrackObject() {{
      const title = document.getElementById('djTitleInput').value.trim() || 'My Custom DJ Track';
      const artist = document.getElementById('djArtistInput').value.trim() || 'Custom Artist';
      const entry = parseInt(document.getElementById('djEntrySlider').value, 10) || 0;
      const exit = parseInt(document.getElementById('djExitSlider').value, 10) || 120;
      const dur = currentDjDuration || 180;

      return {{
        song_id: `custom-dj-${{currentDjVid}}-${{Date.now()}}`,
        title: title,
        artist: artist,
        youtube_ids: [currentDjVid],
        entry_sec: entry,
        exit_sec: exit,
        duration_sec: dur,
        energy: selectedDjEnergy,
        language: 'custom',
        subtype: 'dj_custom',
        banger: true
      }};
    }}

    // Play Now from DJ maker
    document.getElementById('djPlayNowBtn').addEventListener('click', () => {{
      const customTrack = getCustomDjTrackObject();
      closeDjMakerModal();
      document.getElementById('setupView').classList.add('hidden');
      document.getElementById('playerView').classList.remove('hidden');
      engine.playNow(customTrack);
      logToScreen(`🎉 Mixing live into your custom DJ track: "${{customTrack.title}}"!`);
    }});

    // Queue Track from DJ maker
    document.getElementById('djQueueTrackBtn').addEventListener('click', () => {{
      const customTrack = getCustomDjTrackObject();
      closeDjMakerModal();
      engine.queueNext(customTrack);
      logToScreen(`✓ Queued your custom DJ cut: "${{customTrack.title}}" as next up.`);
    }});

    // Save to Library from DJ maker
    document.getElementById('djSaveToLibBtn').addEventListener('click', () => {{
      const customTrack = getCustomDjTrackObject();
      LIBRARY.unshift(customTrack);
      closeDjMakerModal();
      logToScreen(`💾 Saved custom DJ track "${{customTrack.title}}" to party catalog!`);
    }});

    // ========================================================
    // UI BUTTONS & MULTI-ARTIST LIVE RETUNING
    // ========================================================
    document.getElementById('approvePlayBtn').addEventListener('click', () => {{
      document.getElementById('setupView').classList.add('hidden');
      document.getElementById('playerView').classList.remove('hidden');

      const setlist = buildSetlist(LIBRARY, selectedLangs, selectedTime, selectedArtists);
      logToScreen(`Generated setlist with ${{setlist.length}} tracks. Singer filter: ${{selectedArtists.length ? selectedArtists.join(", ") : "All Artists"}}`);
      engine.start(setlist);
      updateSelectedArtistsUI();
    }});

    // Change singers mid-party button
    document.getElementById('openLiveArtistFilterBtn').addEventListener('click', () => {{
      document.getElementById('playerView').classList.add('hidden');
      document.getElementById('setupView').classList.remove('hidden');
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }});

    document.getElementById('togglePlayBtn').addEventListener('click', () => {{
      const paused = engine.togglePlay();
      document.getElementById('togglePlayBtn').textContent = paused ? 'Resume' : 'Pause';
      if ('mediaSession' in navigator) {{
        navigator.mediaSession.playbackState = paused ? 'paused' : 'playing';
      }}
    }});

    document.getElementById('skipBtn').addEventListener('click', () => {{
      engine.skip();
    }});

    document.getElementById('shuffleQueueBtn').addEventListener('click', () => {{
      engine.shuffleQueue();
    }});

    document.getElementById('exportSetlistBtn').addEventListener('click', () => {{
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(engine.queue, null, 2));
      const dlAnchor = document.createElement('a');
      dlAnchor.setAttribute("href", dataStr);
      dlAnchor.setAttribute("download", `naux_party_setlist_${{Date.now()}}.json`);
      document.body.appendChild(dlAnchor);
      dlAnchor.click();
      dlAnchor.remove();
      logToScreen("💾 Setlist exported to JSON.");
    }});

    // Fade speed selector
    document.getElementById('fadeDurationSelect').addEventListener('change', (e) => {{
      const ms = parseInt(e.target.value, 10);
      engine.crossfadeDuration = ms;
      logToScreen(`Crossfade duration set to ${{ms / 1000}}s`);
    }});

    // Master volume slider
    document.getElementById('masterVolumeSlider').addEventListener('input', (e) => {{
      const val = parseInt(e.target.value, 10);
      engine.masterVolume = val;
      document.getElementById('masterVolLabel').textContent = `${{val}}%`;
      
      const live = engine.decks[engine.liveId];
      if (live && live.player && !engine.crossfading) {{
        const effectiveVol = Math.round((live.volume * val) / 100);
        try {{ live.player.setVolume(effectiveVol); }} catch(err) {{}}
      }}
    }});

    // Quick Search & YouTube Custom Track
    const searchInput = document.getElementById('quickSearchInput');
    const searchDropdown = document.getElementById('searchResultsDropdown');

    searchInput.addEventListener('input', (e) => {{
      const q = e.target.value.toLowerCase().trim();
      if (q.length < 2) {{
        searchDropdown.classList.add('hidden');
        return;
      }}

      const matches = LIBRARY.filter(s => 
        s.title.toLowerCase().includes(q) || 
        s.artist.toLowerCase().includes(q)
      ).slice(0, 10);

      searchDropdown.innerHTML = '';
      if (matches.length === 0) {{
        searchDropdown.innerHTML = '<div class="p-3 text-xs text-white/40">No library match found. You can paste a YouTube URL and click + Queue Track.</div>';
      }} else {{
        matches.forEach(s => {{
          const row = document.createElement('div');
          row.className = 'p-2.5 hover:bg-white/10 rounded-xl flex items-center justify-between cursor-pointer transition';
          row.innerHTML = `
            <div class="truncate">
              <p class="font-bold text-white text-sm">${{s.title}}</p>
              <p class="text-xs text-white/50">${{s.artist}}</p>
            </div>
            <div class="flex gap-2">
              <button class="text-xs bg-lime/10 border border-lime/30 text-lime font-anton px-2.5 py-1.5 rounded-lg hover:bg-lime hover:text-black quick-dj-edit">
                🎛️ DJ
              </button>
              <button class="text-xs bg-lime text-black font-anton px-3 py-1.5 rounded-lg hover:brightness-110 quick-add-next">
                ⚡ Next
              </button>
              <button class="text-xs bg-white/10 hover:bg-white/20 text-white font-anton px-3 py-1.5 rounded-lg quick-add-end">
                + End
              </button>
            </div>
          `;

          row.querySelector('.quick-dj-edit').addEventListener('click', (ev) => {{
            ev.stopPropagation();
            openDjMakerWithSong(s);
            searchInput.value = '';
            searchDropdown.classList.add('hidden');
          }});

          row.querySelector('.quick-add-next').addEventListener('click', (ev) => {{
            ev.stopPropagation();
            engine.queueNext(s);
            searchInput.value = '';
            searchDropdown.classList.add('hidden');
          }});

          row.querySelector('.quick-add-end').addEventListener('click', (ev) => {{
            ev.stopPropagation();
            engine.queueTrack(s);
            searchInput.value = '';
            searchDropdown.classList.add('hidden');
          }});

          searchDropdown.appendChild(row);
        }});
      }}
      searchDropdown.classList.remove('hidden');
    }});

    document.getElementById('addCustomYtBtn').addEventListener('click', () => {{
      const val = searchInput.value.trim();
      if (!val) return;

      const ytMatch = val.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([a-zA-Z0-9_-]{{11}})/);
      if (ytMatch) {{
        const vid = ytMatch[1];
        const customTrack = {{
          song_id: `custom-${{vid}}-${{Date.now()}}`,
          title: `Custom Track (${{vid}})`,
          artist: 'User Added YouTube Track',
          youtube_ids: [vid],
          entry_sec: 0,
          exit_sec: 180,
          duration_sec: 180,
          energy: 7.5,
          language: 'custom',
          banger: true
        }};
        engine.queueTrack(customTrack);
        searchInput.value = '';
        searchDropdown.classList.add('hidden');
      }} else {{
        const match = LIBRARY.find(s => s.title.toLowerCase().includes(val.toLowerCase()) || s.artist.toLowerCase().includes(val.toLowerCase()));
        if (match) {{
          engine.queueTrack(match);
          searchInput.value = '';
          searchDropdown.classList.add('hidden');
        }} else {{
          alert("Please paste a valid YouTube URL or search an artist in our catalog.");
        }}
      }}
    }});

    // Language Selector Toggles
    document.querySelectorAll('.lang-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const lang = btn.dataset.lang;
        if (lang === 'all') {{
          selectedLangs = ['all'];
          document.querySelectorAll('.lang-btn').forEach(b => {{
            b.className = b.dataset.lang === 'all' 
              ? 'lang-btn border border-lime bg-lime/10 text-lime px-4 py-3 rounded-2xl font-bold text-sm transition'
              : 'lang-btn border border-white/10 text-white/60 hover:border-white/30 px-4 py-3 rounded-2xl font-bold text-sm transition';
          }});
          return;
        }}

        if (selectedLangs.includes('all')) selectedLangs = [];
        if (selectedLangs.includes(lang)) {{
          selectedLangs = selectedLangs.filter(l => l !== lang);
          btn.className = 'lang-btn border border-white/10 text-white/60 hover:border-white/30 px-4 py-3 rounded-2xl font-bold text-sm transition';
        }} else {{
          selectedLangs.push(lang);
          btn.className = 'lang-btn border border-lime bg-lime/10 text-lime px-4 py-3 rounded-2xl font-bold text-sm transition';
        }}
        if (selectedLangs.length === 0) selectedLangs = ['hindi', 'punjabi'];
      }});
    }});

    // Mood Selector Toggles
    document.querySelectorAll('.mood-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        selectedTime = btn.dataset.mood;
        document.querySelectorAll('.mood-btn').forEach(b => {{
          b.className = b.dataset.mood === selectedTime
            ? 'mood-btn border border-lime bg-lime/10 text-lime px-4 py-3 rounded-2xl font-bold text-sm transition'
            : 'mood-btn border border-white/10 text-white/60 hover:border-white/30 px-4 py-3 rounded-2xl font-bold text-sm transition';
        }});
      }});
    }});

    document.getElementById('playFullBtn').addEventListener('click', () => {{
      const isFull = engine.togglePlayFull();
      document.getElementById('playFullBtn').className = isFull 
        ? 'border border-lime text-lime px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition bg-lime/10'
        : 'border border-white/20 hover:border-white/50 text-white/70 px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition';
    }});

    document.getElementById('unmuteBtn').addEventListener('click', () => {{
      const live = engine.decks[engine.liveId];
      if (live && live.player) {{
        live.player.unMute();
        live.player.setVolume(100);
        live.player.playVideo();
        document.getElementById('unmutePrompt').classList.add('hidden');
        logToScreen("Audio unmuted by user tap.");
      }}
    }});

    document.getElementById('retuneBtn').addEventListener('click', () => {{
      document.getElementById('playerView').classList.add('hidden');
      document.getElementById('setupView').classList.remove('hidden');
    }});

    // HARDWARE MEDIA KEYS
    if ('mediaSession' in navigator) {{
      try {{
        navigator.mediaSession.setActionHandler('play', () => {{
          engine.togglePlay();
          document.getElementById('togglePlayBtn').textContent = 'Pause';
          navigator.mediaSession.playbackState = 'playing';
        }});
        navigator.mediaSession.setActionHandler('pause', () => {{
          engine.togglePlay();
          document.getElementById('togglePlayBtn').textContent = 'Resume';
          navigator.mediaSession.playbackState = 'paused';
        }});
        navigator.mediaSession.setActionHandler('nexttrack', () => {{
          engine.skip();
        }});
      }} catch(e) {{}}
    }}

    // KEYBOARD SHORTCUTS
    window.addEventListener('keydown', (e) => {{
      const activeTag = document.activeElement ? document.activeElement.tagName : '';
      if (activeTag === 'INPUT' || activeTag === 'TEXTAREA') {{
        return;
      }}

      if (e.code === 'Space' || e.key === ' ' || e.key.toLowerCase() === 'k') {{
        e.preventDefault();
        const paused = engine.togglePlay();
        document.getElementById('togglePlayBtn').textContent = paused ? 'Resume' : 'Pause';
        if ('mediaSession' in navigator) {{
          navigator.mediaSession.playbackState = paused ? 'paused' : 'playing';
        }}
      }} else if (e.code === 'ArrowRight' || e.key.toLowerCase() === 'n') {{
        e.preventDefault();
        engine.skip();
      }} else if (e.key.toLowerCase() === 's') {{
        engine.shuffleQueue();
      }} else if (e.key.toLowerCase() === 'f') {{
        const isFull = engine.togglePlayFull();
        document.getElementById('playFullBtn').className = isFull 
          ? 'border border-lime text-lime px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition bg-lime/10'
          : 'border border-white/20 hover:border-white/50 text-white/70 px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition';
      }}
    }});

    // GUEST MOBILE ROOM REQUESTS SYNC
    async function syncGuestRequests() {{
      if (!window.location.protocol.startsWith('http')) return;
      try {{
        const res = await fetch('/api/room?code=AUX1');
        if (!res.ok) return;
        const data = await res.json();
        const requests = data.requests || [];
        const card = document.getElementById('guestRequestsCard');
        const countBadge = document.getElementById('guestReqCountBadge');
        const listEl = document.getElementById('guestRequestsList');

        if (requests.length === 0) {{
          card.classList.add('hidden');
          return;
        }}

        card.classList.remove('hidden');
        countBadge.textContent = requests.length;
        listEl.innerHTML = '';

        requests.forEach((req, idx) => {{
          const item = document.createElement('div');
          item.className = 'flex items-center justify-between py-2 gap-3';
          item.innerHTML = `
            <div class="truncate">
              <p class="font-bold text-white text-sm truncate">${{req.song.title}}</p>
              <p class="text-xs text-white/50 truncate">${{req.song.artist}} · <span class="text-lime">Requested by ${{req.guest || 'Guest'}}</span></p>
            </div>
            <div class="flex items-center gap-2 shrink-0">
              <button class="bg-lime text-black font-anton text-xs px-3 py-1.5 rounded-xl hover:brightness-110 guest-play-now" data-idx="${{idx}}">
                ⚡ Play Now
              </button>
              <button class="bg-white/10 hover:bg-white/20 text-white font-anton text-xs px-3 py-1.5 rounded-xl guest-queue-next" data-idx="${{idx}}">
                + Queue Next
              </button>
            </div>
          `;

          item.querySelector('.guest-play-now').addEventListener('click', () => {{
            engine.playNow(req.song);
            logToScreen(`Approved guest request: "${{req.song.title}}" playing now!`);
          }});

          item.querySelector('.guest-queue-next').addEventListener('click', () => {{
            engine.queueNext(req.song);
            logToScreen(`Approved guest request: "${{req.song.title}}" queued next!`);
          }});

          listEl.appendChild(item);
        }});
      }} catch(e) {{}}
    }}
    setInterval(syncGuestRequests, 4000);

  </script>
</body>
</html>
'''

with open("naux_party_clone.html", "w", encoding="utf-8") as out:
    out.write(html_content)

shutil.copy("naux_party_clone.html", "index.html")
print("SUCCESS: Both naux_party_clone.html and index.html compiled with DJ Song Maker & Multi-Artist Spotlight Mode!")

