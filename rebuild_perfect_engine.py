import json

with open("naux_top_tracks.json", "r", encoding="utf-8") as f:
    top_tracks = json.load(f)[:50]

clean_tracks = []
for t in top_tracks:
    clean_tracks.append({
        "song_id": t.get("song_id"),
        "title": t.get("title"),
        "artist": t.get("artist"),
        "youtube_ids": t.get("youtube_ids", []),
        "entry_sec": t.get("entry_sec", 0),
        "exit_sec": t.get("exit_sec", 90),
        "duration_sec": t.get("duration_sec", 180),
        "energy": t.get("energy", 7),
        "language": t.get("language", "hindi"),
        "subtype": t.get("subtype", "party"),
        "banger": t.get("banger", True)
    })

tracks_json = json.dumps(clean_tracks, indent=2)

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NAUX · The aux, handled</title>
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
    /* The exact NAUX Host Container: 320x180, fixed at 0,0, opacity 0.01, z-index -1 */
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
  </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-lime selection:text-black">

  <!-- PERSISTENT YOUTUBE IFRAME HOST (320x180 in active DOM) -->
  <div id="naux-players-host">
    <div id="deck-A-player"></div>
    <div id="deck-B-player"></div>
  </div>

  <!-- Top Bar -->
  <header class="border-b border-white/10 px-6 py-4 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <h1 class="text-3xl font-anton text-lime tracking-wider">NAUX</h1>
      <span class="text-xs uppercase tracking-widest text-white/40 border border-white/20 px-2 py-0.5 rounded">The aux, handled</span>
    </div>
    <div class="flex items-center gap-4 text-xs">
      <div id="wakeBadge" class="hidden sm:flex items-center gap-1.5 text-white/50">
        <span class="w-2 h-2 rounded-full bg-white/30"></span> Screen Awake
      </div>
      <div id="ytStatusBadge" class="flex items-center gap-1.5 text-lime font-mono">
        <span class="w-2 h-2 rounded-full bg-lime animate-pulse"></span> Connecting YouTube...
      </div>
    </div>
  </header>

  <!-- Notice if opened via file:// instead of http:// -->
  <div id="fileNotice" class="hidden bg-amber-500/10 border-b border-amber-500/30 text-amber-300 px-6 py-2.5 text-xs flex items-center justify-between">
    <div class="flex items-center gap-2">
      <span>💡 Running on <code class="bg-black/50 px-1 py-0.5 rounded text-white font-mono">file://</code>. Run <code class="bg-black/50 px-1 py-0.5 rounded text-white font-mono">run_naux.bat</code> to open via <strong class="text-white">http://localhost:3000</strong>!</span>
    </div>
    <button onclick="document.getElementById('fileNotice').remove()" class="text-white/60 hover:text-white font-bold ml-4">✕</button>
  </div>

  <!-- MAIN AREA -->
  <main class="max-w-4xl w-full mx-auto p-4 sm:p-6 flex-1 flex flex-col justify-center">

    <!-- VIEW 1: FUNNEL / SET SETUP -->
    <div id="setupView" class="space-y-8">
      <div class="text-center space-y-3">
        <h1 class="text-6xl sm:text-8xl font-anton text-white tracking-tight uppercase">
          The Aux, <span class="text-lime">Handled.</span>
        </h1>
        <p class="text-white/60 text-sm sm:text-base max-w-lg mx-auto">
          Party songs that drop straight into the hook, cut before the boring outro, and mix seamlessly into the next track.
        </p>
      </div>

      <!-- Controls Card -->
      <div class="bg-white/5 border border-white/10 rounded-3xl p-6 sm:p-8 space-y-6">
        <!-- Language selector -->
        <div>
          <label class="block text-xs uppercase tracking-wider text-white/50 mb-3 font-semibold">1. Select Languages</label>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
            <button data-lang="punjabi" class="lang-btn border border-lime bg-lime/10 text-lime py-3 px-4 rounded-2xl font-bold text-sm transition">Punjabi</button>
            <button data-lang="hindi" class="lang-btn border border-lime bg-lime/10 text-lime py-3 px-4 rounded-2xl font-bold text-sm transition">Hindi / Bollywood</button>
            <button data-lang="english" class="lang-btn border border-white/10 text-white/70 hover:border-white/30 py-3 px-4 rounded-2xl font-bold text-sm transition">English</button>
            <button data-lang="all" class="lang-btn border border-white/10 text-white/70 hover:border-white/30 py-3 px-4 rounded-2xl font-bold text-sm transition">All Combined</button>
          </div>
        </div>

        <!-- Party Vibe / Mood -->
        <div>
          <label class="block text-xs uppercase tracking-wider text-white/50 mb-3 font-semibold">2. Party Energy / Time of Night</label>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
            <button data-time="warmup" class="time-btn border border-white/10 text-white/70 hover:border-white/30 py-3 px-4 rounded-2xl font-bold text-sm transition">Warmup</button>
            <button data-time="peak" class="time-btn border border-lime bg-lime/10 text-lime py-3 px-4 rounded-2xl font-bold text-sm transition">Peak (Party)</button>
            <button data-time="bangers" class="time-btn border border-white/10 text-white/70 hover:border-white/30 py-3 px-4 rounded-2xl font-bold text-sm transition">Bangers Only 🔥</button>
            <button data-time="winddown" class="time-btn border border-white/10 text-white/70 hover:border-white/30 py-3 px-4 rounded-2xl font-bold text-sm transition">Wind-down</button>
          </div>
        </div>

        <!-- Start Button -->
        <button id="startPartyBtn" class="w-full bg-lime text-black font-anton text-2xl sm:text-3xl py-5 rounded-2xl hover:brightness-110 active:scale-[0.99] transition shadow-lg pulse-glow uppercase tracking-wider cursor-pointer">
          APPROVE & PLAY (DROP THE HOOK) 🔥
        </button>
      </div>

      <div class="flex justify-between items-center text-xs text-white/30 uppercase tracking-widest px-2">
        <span>Verified Library: <strong class="text-lime">{len(clean_tracks)} Tracks</strong></span>
        <a href="naux_cue_studio.html" class="text-lime hover:underline font-bold">Open Cue Studio →</a>
      </div>
    </div>

    <!-- VIEW 2: LIVE DJ PLAYER -->
    <div id="playerView" class="hidden space-y-6">

      <!-- Tap to Play prompt if audio blocked by browser -->
      <div id="unmutePrompt" class="hidden bg-lime text-black p-4 rounded-2xl flex items-center justify-between font-bold shadow-2xl">
        <div class="flex items-center gap-2">
          <span>🔊 Browser requires a tap to start party audio:</span>
        </div>
        <button id="unmuteBtn" class="bg-black text-lime px-5 py-2.5 rounded-xl text-xs uppercase tracking-wider font-anton hover:bg-neutral-900 active:scale-95 transition">
          Tap To Play Audio
        </button>
      </div>

      <!-- Live Track Card -->
      <div class="bg-white/5 border border-white/10 rounded-3xl p-6 sm:p-8 relative overflow-hidden">
        
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-lime/20 text-lime border border-lime/30">
              <span class="w-2 h-2 rounded-full bg-lime animate-ping"></span> LIVE ON AUX
            </span>
            <span id="activeDeckPill" class="text-xs uppercase text-white/40 tracking-wider font-mono">Deck A</span>
          </div>
          <div id="crossfadeIndicator" class="hidden text-xs font-bold text-lime uppercase tracking-wider animate-pulse">
            ⚡ Mixing Into Next Hook (1.5s Equal-Power)
          </div>
        </div>

        <!-- Song Metadata -->
        <div class="space-y-1 mb-6">
          <h2 id="nowPlayingTitle" class="text-4xl sm:text-6xl font-anton text-white tracking-wide uppercase truncate">
            Loading...
          </h2>
          <p id="nowPlayingArtist" class="text-white/60 text-lg sm:text-xl font-medium truncate">
            -
          </p>
        </div>

        <!-- Progress Bar & Timestamps -->
        <div class="space-y-2">
          <div class="flex justify-between text-xs text-white/40 font-mono">
            <span id="currentTimeLabel">0:00</span>
            <span id="cutPointLabel" class="text-lime">Hook Cut @ 1:27</span>
          </div>
          <div class="relative w-full h-3 bg-white/10 rounded-full overflow-hidden">
            <div id="progressBar" class="h-full bg-lime transition-all duration-100" style="width: 0%"></div>
          </div>
        </div>

        <!-- Player Controls -->
        <div class="mt-8 flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <button id="togglePlayBtn" class="bg-white text-black font-anton px-8 py-3 rounded-2xl hover:bg-white/90 active:scale-95 transition text-lg uppercase">
              Pause
            </button>
            <button id="skipBtn" class="bg-white/10 border border-white/20 hover:border-lime hover:text-lime px-6 py-3 rounded-2xl font-bold text-sm transition">
              Skip Track ⏭
            </button>
          </div>

          <div class="flex items-center gap-2">
            <button id="playFullBtn" class="border border-white/20 hover:border-white/50 text-white/70 px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition">
              Ride Full Song (Don't Cut)
            </button>
          </div>
        </div>
      </div>

      <!-- DUAL-DECK DJ MONITOR CARDS -->
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

      <!-- Upcoming Setlist -->
      <div class="border border-white/10 rounded-3xl p-6 bg-white/[0.02]">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-anton text-xl uppercase tracking-wide text-white/80">Upcoming in Set</h3>
          <button id="retuneBtn" class="text-xs text-lime uppercase tracking-wider hover:underline">
            Change Mood / Retune
          </button>
        </div>
        <ol id="queueList" class="space-y-3 text-sm divide-y divide-white/5">
        </ol>
      </div>

      <!-- Live Event Engine Logs -->
      <div class="border border-white/10 rounded-2xl p-4 bg-black/40 text-xs font-mono text-white/50 space-y-1">
        <p class="text-white/30 uppercase text-[10px] font-bold">DJ Engine Log:</p>
        <div id="engineLog" class="h-20 overflow-y-auto space-y-1 text-white/70">
          <div>[NAUX] Ready to play. Tap APPROVE & PLAY to drop the hook.</div>
        </div>
      </div>

    </div>

  </main>

  <footer class="border-t border-white/10 p-4 text-center text-xs text-white/40 flex justify-between items-center max-w-4xl mx-auto w-full">
    <span>Reverse Engineered NAUX Dual-Deck Player</span>
    <a href="naux_cue_studio.html" class="text-lime hover:underline font-bold">Open Cue Studio →</a>
  </footer>

  <!-- SCRIPT -->
  <script>
    if (window.location.protocol === 'file:') {{
      const notice = document.getElementById('fileNotice');
      if (notice) notice.classList.remove('hidden');
    }}

    const LIBRARY = {tracks_json};
    let selectedLangs = ['punjabi', 'hindi'];
    let selectedTime = 'peak';
    let currentSetlist = [];

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

    // Setlist Generator
    function buildSetlist(lib, languages, timeMood) {{
      const energyTargets = {{
        warmup: 5.0,
        peak: 7.5,
        bangers: 8.8,
        winddown: 4.0
      }};
      const targetEnergy = energyTargets[timeMood] || 7.0;

      let pool = lib.filter(s => languages.includes(s.language));
      if (pool.length < 5) pool = lib;

      let scored = pool.map(s => {{
        let dist = Math.abs(s.energy - targetEnergy);
        let score = 10 - (dist * 2) + (s.banger ? 3 : 0) + (Math.random() * 1.5);
        return {{ song: s, score }};
      }}).sort((a, b) => b.score - a.score);

      let list = scored.map(item => ({{ ...item.song, play_full: false }}));

      // Artist deduplication
      for (let i = 1; i < list.length; i++) {{
        const primary = s => s.artist.split(/,|&|feat/i)[0].trim().toLowerCase();
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
      return list.slice(0, 30);
    }}

    // COMPLETE RESILIENT NAUX DUAL-DECK ENGINE
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
        this.nextIndex = 0;
        this.ready = false;
        this.awaitingStart = null;
        this.pendingHandoff = null;
        this.tickTimer = null;
        this.fadeTimer = null;
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

      start(queue) {{
        if (!this.ready) return;
        this.queue = queue.slice();
        this.nextIndex = 0;
        const first = this.takeNext();
        if (!first) return;

        this.liveId = 'A';
        this.assign(this.decks.A, first);
        this.load(this.decks.A, 'live');

        this.preloadNext(this.decks.B);
        this.updateUI();
      }}

      takeNext() {{
        return this.nextIndex < this.queue.length ? this.queue[this.nextIndex++] : null;
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
        logToScreen(`Deck ${{deck.id}} cueing "${{cue.title}}" at ${{startSec}}s (${{role}})`);

        if (role === 'preload') {{
          deck.player.mute();
          deck.player.setVolume(0);
          deck.volume = 0;
        }} else {{
          deck.player.unMute();
          deck.player.setVolume(100);
          deck.volume = 100;
        }}

        deck.player.loadVideoById({{
          videoId: vid,
          startSeconds: startSec
        }});

        // If Deck B takes > 10 seconds to load, fail it and try fallback/next track!
        deck.timer = setTimeout(() => {{
          logToScreen(`⚠️ Deck ${{deck.id}} timed out buffering "${{cue.title}}". Moving to fallback source...`);
          this.nextSource(deck);
        }}, 10000);

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
        if (cue) {{
          deck.idIndex += 1;
          if (deck.idIndex < cue.youtube_ids.length) {{
            logToScreen(`Deck ${{deck.id}} trying alternate source ${{deck.idIndex + 1}}/${{cue.youtube_ids.length}} for "${{cue.title}}"...`);
            this.load(deck, deck.role);
            return;
          }}
          logToScreen(`No working YouTube stream for "${{cue.title}}". Discarding and preloading next in queue.`);
          if (deck.role === 'live') {{
            deck.status = 'empty';
            deck.cue = null;
            this.updateUI();
            this.requestHandoff('error');
          }} else {{
            // Preload next track for Deck B!
            this.preloadNext(deck);
          }}
        }}
      }}

      preloadNext(deck) {{
        const nextCue = this.takeNext();
        if (!nextCue) {{
          deck.status = 'empty';
          deck.cue = null;
          this.updateUI();
          return;
        }}
        this.assign(deck, nextCue);
        this.load(deck, 'preload');
      }}

      onStateChange(deck, state) {{
        // YT.PlayerState.PLAYING === 1
        if (state === 1) {{
          if (this.awaitingStart === deck.id) {{
            // Incoming deck confirmed playing! Start volume fade!
            this.startFade(deck);
          }} else if (deck.status === 'loading' && deck.role === 'preload') {{
            this.clearTimer(deck);
            deck.player.pauseVideo();
            deck.player.seekTo(deck.cue.entry_sec || 0, true);
            deck.status = 'ready';
            logToScreen(`✓ Deck ${{deck.id}} primed & cued at hook (${{deck.cue.entry_sec}}s). Ready for mix!`);
            this.updateUI();
            
            // If live deck was waiting for this deck to become ready, trigger handoff immediately!
            if (this.pendingHandoff) {{
              logToScreen(`Deck ${{deck.id}} ready now. Executing pending handoff (${{this.pendingHandoff}})...`);
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
        // YT.PlayerState.CUED === 5
        else if (state === 5) {{
          if (deck.status === 'loading' && deck.role === 'preload') {{
            this.clearTimer(deck);
            deck.status = 'ready';
            logToScreen(`✓ Deck ${{deck.id}} cued (state 5): "${{deck.cue.title}}" ready!`);
            this.updateUI();
            if (this.pendingHandoff) {{
              const reason = this.pendingHandoff;
              this.pendingHandoff = null;
              this.requestHandoff(reason);
            }}
          }}
        }}
        // YT.PlayerState.ENDED === 0
        else if (state === 0) {{
          if (deck.id === this.liveId && !this.crossfading) {{
            logToScreen(`Live track ended on Deck ${{deck.id}}. Handoff requested.`);
            this.requestHandoff('ended');
          }}
        }}
      }}

      onError(deck, err) {{
        logToScreen(`Deck ${{deck.id}} error code ${{err}} on "${{deck.cue?.title}}"`);
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
        try {{
          curTime = live.player.getCurrentTime() || 0;
        }} catch(e) {{ return; }}

        const duration = live.cue.duration_sec || live.player.getDuration() || 180;
        const cutAt = live.playFull ? (duration - 1.5) : (live.cue.exit_sec || duration - 1.5);

        const pct = Math.min(100, Math.max(0, (curTime / cutAt) * 100));
        document.getElementById('progressBar').style.width = `${{pct}}%`;
        document.getElementById('currentTimeLabel').textContent = formatTime(curTime);
        document.getElementById('cutPointLabel').textContent = live.playFull 
          ? `Playing Full (${{formatTime(duration)}})` 
          : `Hook Cut @ ${{formatTime(cutAt)}}`;

        // Check if cut point reached!
        if (curTime >= cutAt) {{
          this.requestHandoff('hook_cut');
        }}
      }}

      requestHandoff(reason) {{
        if (this.crossfading || this.awaitingStart) return;
        const nextId = this.liveId === 'A' ? 'B' : 'A';
        const nextDeck = this.decks[nextId];

        if (nextDeck.status === 'ready') {{
          this.startIncoming(nextDeck, reason);
        }} else if (nextDeck.status === 'loading') {{
          this.pendingHandoff = reason;
          logToScreen(`Next track still buffering. Holding live Deck ${{this.liveId}}...`);
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

        logToScreen(`Triggering incoming Deck ${{deck.id}} ("${{deck.cue.title}}"). Awaiting playback confirmation...`);

        // Safety timeout: If incoming deck does not start playing within 4 seconds, fail it and try next!
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

        document.getElementById('crossfadeIndicator').classList.remove('hidden');
        logToScreen(`⚡ Crossfading into "${{incoming.cue.title}}" on Deck ${{incoming.id}} (1.5s curve)`);

        const start = performance.now();
        const FADE_MS = 1500;

        if (this.fadeTimer) clearInterval(this.fadeTimer);
        this.fadeTimer = setInterval(() => {{
          const elapsed = performance.now() - start;
          const s = Math.min(1, elapsed / FADE_MS);

          // Equal-power sinusoidal curve
          const inVol = Math.round(100 * Math.sin(s * Math.PI / 2));
          const outVol = Math.round(100 * Math.cos(s * Math.PI / 2));

          incoming.volume = inVol;
          outgoing.volume = outVol;
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

            // Immediately preload next track on outgoing deck!
            this.preloadNext(outgoing);
          }}
        }}, 40);
      }}

      skip() {{
        logToScreen("Skip pressed.");
        const nextId = this.liveId === 'A' ? 'B' : 'A';
        const nextDeck = this.decks[nextId];

        // If next deck is not ready or stuck loading, abort it and force preload next immediately!
        if (nextDeck.status === 'loading') {{
          logToScreen("Next deck was still buffering. Skipping directly to next available song...");
          this.nextSource(nextDeck);
        }} else {{
          this.requestHandoff('skip');
        }}
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
        renderQueue(this.queue, cue);
      }}

      updateUI() {{
        const dA = this.decks.A;
        const dB = this.decks.B;

        // Deck A
        document.getElementById('deckAStatus').textContent = `${{dA.status.toUpperCase()}} (${{dA.volume}}%)`;
        document.getElementById('deckAVolume').style.width = `${{dA.volume}}%`;
        document.getElementById('deckAVolLabel').textContent = `${{dA.volume}}%`;
        document.getElementById('deckASong').textContent = dA.cue ? dA.cue.title : 'Empty';
        document.getElementById('deckAArtist').textContent = dA.cue ? dA.cue.artist : '-';

        // Deck B
        document.getElementById('deckBStatus').textContent = `${{dB.status.toUpperCase()}} (${{dB.volume}}%)`;
        document.getElementById('deckBVolume').style.width = `${{dB.volume}}%`;
        document.getElementById('deckBVolLabel').textContent = `${{dB.volume}}%`;
        document.getElementById('deckBSong').textContent = dB.cue ? dB.cue.title : 'Empty';
        document.getElementById('deckBArtist').textContent = dB.cue ? dB.cue.artist : '-';

        // Visualizer bar animations
        const eqA = document.getElementById('deckAEq');
        const eqB = document.getElementById('deckBEq');
        if (this.liveId === 'A') {{
          eqA.className = 'flex items-end gap-1 h-8 w-8 opacity-100';
          eqB.className = 'flex items-end gap-1 h-8 w-8 opacity-30';
        }} else {{
          eqA.className = 'flex items-end gap-1 h-8 w-8 opacity-30';
          eqB.className = 'flex items-end gap-1 h-8 w-8 opacity-100';
        }}

        // Deck container glows
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

    // INTERFACE CONTROLS
    document.querySelectorAll('.lang-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const lang = btn.dataset.lang;
        if (lang === 'all') {{
          selectedLangs = ['punjabi', 'hindi', 'english'];
          document.querySelectorAll('.lang-btn').forEach(b => {{
            b.classList.remove('border-lime', 'bg-lime/10', 'text-lime');
            b.classList.add('border-white/10', 'text-white/70');
          }});
          btn.classList.add('border-lime', 'bg-lime/10', 'text-lime');
          btn.classList.remove('border-white/10', 'text-white/70');
          return;
        }}
        if (selectedLangs.includes(lang)) {{
          if (selectedLangs.length > 1) {{
            selectedLangs = selectedLangs.filter(l => l !== lang);
            btn.classList.remove('border-lime', 'bg-lime/10', 'text-lime');
            btn.classList.add('border-white/10', 'text-white/70');
          }}
        }} else {{
          selectedLangs.push(lang);
          btn.classList.add('border-lime', 'bg-lime/10', 'text-lime');
          btn.classList.remove('border-white/10', 'text-white/70');
        }}
      }});
    }});

    document.querySelectorAll('.time-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('.time-btn').forEach(b => {{
          b.classList.remove('border-lime', 'bg-lime/10', 'text-lime');
          b.classList.add('border-white/10', 'text-white/70');
        }});
        btn.classList.add('border-lime', 'bg-lime/10', 'text-lime');
        btn.classList.remove('border-white/10', 'text-white/70');
        selectedTime = btn.dataset.time;
      }});
    }});

    document.getElementById('startPartyBtn').addEventListener('click', async () => {{
      document.getElementById('setupView').classList.add('hidden');
      document.getElementById('playerView').classList.remove('hidden');

      if ('wakeLock' in navigator) {{
        try {{
          await navigator.wakeLock.request('screen');
          document.getElementById('wakeBadge').classList.remove('hidden');
        }} catch(e) {{}}
      }}

      currentSetlist = buildSetlist(LIBRARY, selectedLangs, selectedTime);
      renderQueue(currentSetlist, currentSetlist[0]);
      engine.start(currentSetlist);
    }});

    function renderQueue(list, currentSong) {{
      const queueListEl = document.getElementById('queueList');
      queueListEl.innerHTML = '';
      const upcoming = list.filter(s => !currentSong || s.song_id !== currentSong.song_id);

      upcoming.slice(0, 6).forEach((s, idx) => {{
        const li = document.createElement('li');
        li.className = 'pt-2 flex justify-between items-center';
        li.innerHTML = `
          <div>
            <p class="font-bold text-white/90">${{idx + 1}}. ${{s.title}}</p>
            <p class="text-xs text-white/50">${{s.artist}}</p>
          </div>
          <div class="text-right">
            <span class="text-xs font-mono text-lime border border-lime/20 px-2 py-0.5 rounded-full">
              Hook @ ${{formatTime(s.entry_sec)}}
            </span>
          </div>
        `;
        queueListEl.appendChild(li);
      }});
    }}

    document.getElementById('skipBtn').addEventListener('click', () => engine.skip());

    document.getElementById('togglePlayBtn').addEventListener('click', () => {{
      const paused = engine.togglePlay();
      document.getElementById('togglePlayBtn').textContent = paused ? 'Resume' : 'Pause';
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

  </script>
</body>
</html>
'''

with open("naux_party_clone.html", "w", encoding="utf-8") as out:
    out.write(html_content)

print("naux_party_clone.html updated with complete resilient dual-deck engine!")

