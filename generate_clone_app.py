import json

with open("naux_top_tracks.json", "r", encoding="utf-8") as f:
    top_tracks = json.load(f)[:30]

# Keep minimal essential fields to keep HTML clean
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
  <title>NAUX Party Engine · Reverse Engineered Prototype</title>
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
    .text-lime {{
      color: #d4ff00;
    }}
    .bg-lime {{
      background-color: #d4ff00;
    }}
    .border-lime {{
      border-color: #d4ff00;
    }}
    .pulse-glow {{
      box-shadow: 0 0 25px rgba(212, 255, 0, 0.35);
    }}
    /* Hidden YouTube iframe container */
    #player-container {{
      position: fixed;
      left: -9999px;
      bottom: -9999px;
      width: 320px;
      height: 180px;
      opacity: 0;
      pointer-events: none;
      z-index: -100;
    }}
    /* Custom range input */
    input[type=range] {{
      accent-color: #d4ff00;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-lime selection:text-black">

  <!-- Hidden YouTube host for Dual Deck A & B -->
  <div id="player-container">
    <div id="deck-A"></div>
    <div id="deck-B"></div>
  </div>

  <!-- Top Bar -->
  <header class="border-b border-white/10 px-6 py-4 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <h1 class="text-3xl font-anton text-lime tracking-wider">NAUX</h1>
      <span class="text-xs uppercase tracking-widest text-white/40 border border-white/20 px-2 py-0.5 rounded">Clone Engine</span>
    </div>
    <div class="flex items-center gap-4 text-xs">
      <div id="wakeLockBadge" class="flex items-center gap-1.5 text-white/50">
        <span class="w-2 h-2 rounded-full bg-white/30"></span> Screen Awake
      </div>
      <div id="ytStatusBadge" class="flex items-center gap-1.5 text-white/50">
        <span class="w-2 h-2 rounded-full bg-amber-400"></span> Loading YT API
      </div>
    </div>
  </header>

  <!-- Main View Area -->
  <main class="max-w-4xl w-full mx-auto p-6 flex-1 flex flex-col justify-center">

    <!-- SETUP / FUNNEL VIEW -->
    <div id="setupView" class="space-y-8">
      <div class="text-center space-y-2">
        <h2 class="text-5xl md:text-7xl font-anton text-white tracking-tight uppercase">
          The Aux, <span class="text-lime">Handled.</span>
        </h2>
        <p class="text-white/60 text-sm md:text-base max-w-lg mx-auto">
          Party sets that start right at the hook, cut before the boring outro, and crossfade seamlessly between tracks.
        </p>
      </div>

      <!-- Controls Card -->
      <div class="bg-white/5 border border-white/10 rounded-3xl p-6 md:p-8 space-y-6">
        <!-- Language selector -->
        <div>
          <label class="block text-xs uppercase tracking-wider text-white/50 mb-3 font-semibold">1. Select Languages</label>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5">
            <button data-lang="punjabi" class="lang-btn border border-lime bg-lime/10 text-lime py-3 px-4 rounded-2xl font-bold text-sm transition">Punjabi</button>
            <button data-lang="hindi" class="lang-btn border border-lime bg-lime/10 text-lime py-3 px-4 rounded-2xl font-bold text-sm transition">Hindi / Bollywood</button>
            <button data-lang="english" class="lang-btn border border-white/10 text-white/70 hover:border-white/30 py-3 px-4 rounded-2xl font-bold text-sm transition">English</button>
            <button data-lang="all" class="lang-btn border border-white/10 text-white/70 hover:border-white/30 py-3 px-4 rounded-2xl font-bold text-sm transition">All Combined</button>
          </div>
        </div>

        <!-- Party Vibe / Mood -->
        <div>
          <label class="block text-xs uppercase tracking-wider text-white/50 mb-3 font-semibold">2. Party Energy / Time of Night</label>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5">
            <button data-time="warmup" class="time-btn border border-white/10 text-white/70 hover:border-white/30 py-3 px-4 rounded-2xl font-bold text-sm transition">Warmup (Chill)</button>
            <button data-time="peak" class="time-btn border border-lime bg-lime/10 text-lime py-3 px-4 rounded-2xl font-bold text-sm transition">Peak (Party)</button>
            <button data-time="bangers" class="time-btn border border-white/10 text-white/70 hover:border-white/30 py-3 px-4 rounded-2xl font-bold text-sm transition">Bangers Only 🔥</button>
            <button data-time="winddown" class="time-btn border border-white/10 text-white/70 hover:border-white/30 py-3 px-4 rounded-2xl font-bold text-sm transition">Wind-down</button>
          </div>
        </div>

        <button id="startPartyBtn" class="w-full bg-lime text-black font-anton text-2xl py-5 rounded-2xl hover:brightness-110 active:scale-[0.99] transition shadow-lg pulse-glow uppercase tracking-wider">
          Generate Set & Drop the Hook
        </button>
      </div>

      <!-- Quick Track Inventory Preview -->
      <div class="text-center">
        <p class="text-xs text-white/30 uppercase tracking-widest">
          Loaded <span id="libCount">0</span> Verified Hook Tracks with YouTube Fallbacks
        </p>
      </div>
    </div>

    <!-- LIVE PLAYER VIEW (Hidden by default) -->
    <div id="playerView" class="hidden space-y-6">
      
      <!-- Current Playing Deck Hero -->
      <div class="bg-white/5 border border-white/10 rounded-3xl p-6 md:p-8 relative overflow-hidden">
        
        <!-- Live Pill -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-lime/20 text-lime border border-lime/30">
              <span class="w-2 h-2 rounded-full bg-lime animate-ping"></span> LIVE ON AUX
            </span>
            <span id="activeDeckPill" class="text-xs uppercase text-white/40 tracking-wider font-mono">Deck A</span>
          </div>
          <div id="crossfadeIndicator" class="hidden text-xs font-bold text-lime uppercase tracking-wider animate-pulse">
            ⚡ Mixing Into Next Track (1.5s Equal-Power)
          </div>
        </div>

        <!-- Song Metadata -->
        <div class="space-y-1 mb-6">
          <h2 id="nowPlayingTitle" class="text-3xl md:text-5xl font-anton text-white tracking-wide uppercase truncate">
            Loading Track...
          </h2>
          <p id="nowPlayingArtist" class="text-white/60 text-lg font-medium truncate">
            Artist
          </p>
        </div>

        <!-- Waveform / Progress Slider -->
        <div class="space-y-2">
          <div class="flex justify-between text-xs text-white/40 font-mono">
            <span id="currentTimeLabel">0:00</span>
            <span id="cutPointLabel" class="text-lime">Hook Cut @ 1:20</span>
          </div>
          <div class="relative w-full h-3 bg-white/10 rounded-full overflow-hidden">
            <div id="progressBar" class="h-full bg-lime transition-all duration-100" style="width: 0%"></div>
          </div>
        </div>

        <!-- DJ Controls -->
        <div class="mt-8 flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <button id="togglePlayBtn" class="bg-white text-black font-anton px-6 py-3 rounded-2xl hover:bg-white/90 active:scale-95 transition text-lg uppercase">
              Pause
            </button>
            <button id="skipBtn" class="bg-white/10 border border-white/20 hover:border-lime hover:text-lime px-6 py-3 rounded-2xl font-bold text-sm transition">
              Skip to Next Hook ⏭
            </button>
          </div>

          <!-- Play Full Toggle -->
          <div class="flex items-center gap-2">
            <button id="playFullBtn" class="border border-white/20 hover:border-white/50 text-white/70 px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition">
              Ride Full Song (Don't Cut)
            </button>
          </div>
        </div>
      </div>

      <!-- Dual Deck Visualizer & Handoff Monitor -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Deck A Monitor -->
        <div id="deckAMonitor" class="p-4 rounded-2xl border border-white/10 bg-white/[0.02] space-y-2">
          <div class="flex justify-between items-center text-xs font-mono">
            <span class="text-white/50">DECK A (YouTube IFrame)</span>
            <span id="deckAStatus" class="text-lime font-bold">READY</span>
          </div>
          <div class="h-2 w-full bg-white/10 rounded-full overflow-hidden">
            <div id="deckAVolume" class="h-full bg-lime transition-all duration-75" style="width: 100%"></div>
          </div>
          <p id="deckASong" class="text-xs text-white/60 truncate">-</p>
        </div>

        <!-- Deck B Monitor -->
        <div id="deckBMonitor" class="p-4 rounded-2xl border border-white/10 bg-white/[0.02] space-y-2">
          <div class="flex justify-between items-center text-xs font-mono">
            <span class="text-white/50">DECK B (YouTube IFrame)</span>
            <span id="deckBStatus" class="text-white/40">PRELOADING...</span>
          </div>
          <div class="h-2 w-full bg-white/10 rounded-full overflow-hidden">
            <div id="deckBVolume" class="h-full bg-lime transition-all duration-75" style="width: 0%"></div>
          </div>
          <p id="deckBSong" class="text-xs text-white/60 truncate">Upcoming Track</p>
        </div>
      </div>

      <!-- Upcoming Queue -->
      <div class="border border-white/10 rounded-3xl p-6 bg-white/[0.02]">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-anton text-xl uppercase tracking-wide text-white/80">Upcoming in Set</h3>
          <button id="retuneBtn" class="text-xs text-lime uppercase tracking-wider hover:underline">
            Change Mood / Retune
          </button>
        </div>
        <ol id="queueList" class="space-y-3 text-sm divide-y divide-white/5">
          <!-- Injected dynamically -->
        </ol>
      </div>

    </div>

  </main>

  <footer class="border-t border-white/10 p-4 text-center text-xs text-white/40">
    Reverse engineered dual-deck YouTube crossfade engine · Inspired by NAUX.PARTY
  </footer>

  <!-- SCRIPT -->
  <script>
    // 1. EMBEDDED SONG DATABASE EXTRACTED FROM NAUX
    const LIBRARY = {tracks_json};
    document.getElementById('libCount').textContent = LIBRARY.length;

    // 2. STATE
    let selectedLangs = ['punjabi', 'hindi'];
    let selectedTime = 'peak';
    let setlist = [];
    let currentCueIndex = 0;

    // 3. SELECTION HANDLERS
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

    // 4. SETLIST GENERATOR (NAUX Algorithm)
    function buildSetlist(lib, languages, timeMood) {{
      const energyTargets = {{
        warmup: 5.0,
        peak: 7.5,
        bangers: 8.8,
        winddown: 4.0
      }};
      const targetEnergy = energyTargets[timeMood] || 7.0;

      // Filter by language
      let pool = lib.filter(s => languages.includes(s.language));
      if (pool.length < 5) pool = lib; // fallback if pool is too small

      // Score songs
      let scored = pool.map(s => {{
        let dist = Math.abs(s.energy - targetEnergy);
        let score = 10 - (dist * 2) + (s.banger ? 3 : 0) + (Math.random() * 1.5);
        return {{ song: s, score }};
      }}).sort((a, b) => b.score - a.score);

      let list = scored.map(item => ({{ ...item.song, play_full: false }}));

      // Artist deduplication: avoid back to back songs by the same primary artist
      for (let i = 1; i < list.length; i++) {{
        const primaryArtist = s => s.artist.split(/,|&|feat/i)[0].trim().toLowerCase();
        if (primaryArtist(list[i]) === primaryArtist(list[i - 1])) {{
          for (let j = i + 1; j < list.length; j++) {{
            if (primaryArtist(list[j]) !== primaryArtist(list[i - 1])) {{
              const temp = list[i];
              list[i] = list[j];
              list[j] = temp;
              break;
            }}
          }}
        }}
      }}
      return list.slice(0, 20);
    }}

    // 5. DUAL-DECK YOUTUBE PLAYER ENGINE (Reconstruction)
    class DualDeckPlayerEngine {{
      constructor(onDeckUpdate, onTrackChange) {{
        this.onDeckUpdate = onDeckUpdate;
        this.onTrackChange = onTrackChange;
        this.decks = {{
          A: {{ id: 'A', player: null, status: 'empty', cue: null, volume: 100, idIndex: 0, playFull: false }},
          B: {{ id: 'B', player: null, status: 'empty', cue: null, volume: 0, idIndex: 0, playFull: false }}
        }};
        this.liveId = 'A';
        this.crossfading = false;
        this.paused = false;
        this.queue = [];
        this.nextQueueIdx = 0;
        this.tickInterval = null;
        this.fadeInterval = null;
      }}

      async init() {{
        await this.loadYT();
        await Promise.all([
          this.initPlayer('A', 'deck-A'),
          this.initPlayer('B', 'deck-B')
        ]);
        this.tickInterval = setInterval(() => this.tick(), 250);
      }}

      loadYT() {{
        return new Promise((resolve) => {{
          if (window.YT && window.YT.Player) return resolve(window.YT);
          window.onYouTubeIframeAPIReady = () => {{
            document.getElementById('ytStatusBadge').innerHTML = '<span class="w-2 h-2 rounded-full bg-lime"></span> YT Ready';
            resolve(window.YT);
          }};
          const tag = document.createElement('script');
          tag.src = "https://www.youtube.com/iframe_api";
          document.head.appendChild(tag);
        }});
      }}

      initPlayer(id, elementId) {{
        return new Promise((resolve) => {{
          this.decks[id].player = new YT.Player(elementId, {{
            width: '320',
            height: '180',
            playerVars: {{
              autoplay: 0,
              controls: 0,
              disablekb: 1,
              playsinline: 1,
              rel: 0,
              origin: window.location.origin
            }},
            events: {{
              onReady: () => resolve(),
              onStateChange: (e) => this.onStateChange(this.decks[id], e.data),
              onError: (e) => this.onError(this.decks[id], e.data)
            }}
          }});
        }});
      }}

      start(queue) {{
        this.queue = queue.slice();
        this.nextQueueIdx = 0;
        const first = this.queue[this.nextQueueIdx++];
        if (!first) return;

        this.liveId = 'A';
        this.assign(this.decks.A, first);
        this.loadDeck(this.decks.A, 'live');

        this.preloadNext(this.decks.B);
        this.notify();
      }}

      assign(deck, cue) {{
        deck.cue = cue;
        deck.idIndex = 0;
        deck.playFull = false;
      }}

      loadDeck(deck, mode) {{
        const cue = deck.cue;
        const vid = cue.youtube_ids[deck.idIndex] || cue.youtube_ids[0];
        deck.status = 'loading';
        deck.role = mode;

        if (mode === 'preload') {{
          deck.player.mute();
          deck.player.setVolume(0);
          deck.volume = 0;
        }} else {{
          deck.player.unMute();
          deck.player.setVolume(100);
          deck.volume = 100;
        }}

        const startSec = deck.playFull ? 0 : cue.entry_sec;
        deck.player.loadVideoById({{ videoId: vid, startSeconds: startSec }});
        this.notify();
      }}

      preloadNext(deck) {{
        if (this.nextQueueIdx >= this.queue.length) {{
          deck.status = 'empty';
          deck.cue = null;
          this.notify();
          return;
        }}
        const nextCue = this.queue[this.nextQueueIdx++];
        this.assign(deck, nextCue);
        this.loadDeck(deck, 'preload');
      }}

      onStateChange(deck, state) {{
        // YT.PlayerState.PLAYING === 1
        if (state === 1) {{
          if (deck.role === 'preload' && deck.status === 'loading') {{
            // Immediately pause and cue to the hook
            deck.player.pauseVideo();
            deck.player.seekTo(deck.cue.entry_sec, true);
            deck.status = 'ready';
            this.notify();
          }} else if (deck.role === 'live') {{
            deck.status = 'live';
            if (this.onTrackChange) this.onTrackChange(deck.cue);
            this.notify();
          }}
        }} else if (state === 0) {{ // ENDED
          if (deck.id === this.liveId && !this.crossfading) {{
            this.handoff('ended');
          }}
        }}
      }}

      onError(deck, err) {{
        console.warn(`Deck ${{deck.id}} error ${{err}} on ${{deck.cue?.title}}`);
        if (deck.cue && deck.idIndex + 1 < deck.cue.youtube_ids.length) {{
          deck.idIndex++;
          this.loadDeck(deck, deck.role);
        }} else {{
          this.handoff('error');
        }}
      }}

      tick() {{
        if (this.paused || this.crossfading) return;
        const live = this.decks[this.liveId];
        if (!live || !live.player || live.status !== 'live') return;

        const curTime = live.player.getCurrentTime() || 0;
        const duration = live.player.getDuration() || live.cue.duration_sec;
        const cutAt = live.playFull ? duration - 1.5 : (live.cue.exit_sec || duration - 1.5);

        // Update UI progress
        if (this.onDeckUpdate) {{
          this.onDeckUpdate({{
            curTime,
            cutAt,
            duration,
            cue: live.cue,
            playFull: live.playFull
          }});
        }}

        // Check if we hit the cut point!
        if (curTime >= cutAt) {{
          this.handoff('hook_cut');
        }}
      }}

      handoff(reason) {{
        if (this.crossfading) return;
        const nextId = this.liveId === 'A' ? 'B' : 'A';
        const nextDeck = this.decks[nextId];

        if (nextDeck.status === 'ready') {{
          this.startCrossfade(nextDeck);
        }} else if (nextDeck.status === 'loading') {{
          console.log("Holding live track while next track finishes buffering...");
        }} else {{
          console.log("End of queue reached.");
        }}
      }}

      startCrossfade(incoming) {{
        this.crossfading = true;
        document.getElementById('crossfadeIndicator').classList.remove('hidden');
        const outgoing = this.decks[this.liveId];

        incoming.status = 'live';
        incoming.role = 'live';
        this.liveId = incoming.id;

        incoming.player.unMute();
        incoming.player.setVolume(0);
        incoming.player.playVideo();

        const startTime = performance.now();
        const DURATION = 1500; // 1.5s NAUX equal-power transition

        if (this.fadeInterval) clearInterval(this.fadeInterval);
        this.fadeInterval = setInterval(() => {{
          const elapsed = performance.now() - startTime;
          const s = Math.min(1, elapsed / DURATION);

          // Equal-power sinusoidal curve
          const inVol = Math.round(100 * Math.sin(s * Math.PI / 2));
          const outVol = Math.round(100 * Math.cos(s * Math.PI / 2));

          incoming.volume = inVol;
          outgoing.volume = outVol;
          incoming.player.setVolume(inVol);
          outgoing.player.setVolume(outVol);
          this.notify();

          if (s >= 1) {{
            clearInterval(this.fadeInterval);
            this.fadeInterval = null;
            this.crossfading = false;
            document.getElementById('crossfadeIndicator').classList.add('hidden');

            outgoing.player.pauseVideo();
            outgoing.player.mute();
            outgoing.status = 'empty';
            outgoing.cue = null;
            this.notify();

            // Preload the track after next on the outgoing deck!
            this.preloadNext(outgoing);
          }}
        }}, 40);
      }}

      skip() {{
        this.handoff('user_skip');
      }}

      togglePlay() {{
        const live = this.decks[this.liveId];
        if (!live || !live.player) return;
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
        if (!live) return;
        live.playFull = !live.playFull;
        return live.playFull;
      }}

      notify() {{
        // Update deck monitor widgets
        const dA = this.decks.A;
        const dB = this.decks.B;
        document.getElementById('deckAStatus').textContent = dA.status.toUpperCase();
        document.getElementById('deckAVolume').style.width = `${{dA.volume}}%`;
        document.getElementById('deckASong').textContent = dA.cue ? `${{dA.cue.title}} (${{dA.volume}}%)` : '-';

        document.getElementById('deckBStatus').textContent = dB.status.toUpperCase();
        document.getElementById('deckBVolume').style.width = `${{dB.volume}}%`;
        document.getElementById('deckBSong').textContent = dB.cue ? `${{dB.cue.title}} (${{dB.volume}}%)` : '-';

        document.getElementById('activeDeckPill').textContent = `Deck ${{this.liveId}} Live`;
      }}
    }}

    // 6. INITIALIZATION & UI BINDING
    let engine = null;

    function formatTime(sec) {{
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return `${{m}}:${{s < 10 ? '0' : ''}}${{s}}`;
    }}

    document.getElementById('startPartyBtn').addEventListener('click', async () => {{
      document.getElementById('setupView').classList.add('hidden');
      document.getElementById('playerView').classList.remove('hidden');

      // Request wake lock so party audio doesn't cut out when screen sleeps
      if ('wakeLock' in navigator) {{
        try {{
          await navigator.wakeLock.request('screen');
          document.getElementById('wakeLockBadge').innerHTML = '<span class="w-2 h-2 rounded-full bg-lime"></span> Awake Locked';
        }} catch(e) {{}}
      }}

      setlist = buildSetlist(LIBRARY, selectedLangs, selectedTime);
      renderQueue(setlist);

      if (!engine) {{
        engine = new DualDeckPlayerEngine(
          (tickData) => {{
            const pct = Math.min(100, (tickData.curTime / tickData.cutAt) * 100);
            document.getElementById('progressBar').style.width = `${{pct}}%`;
            document.getElementById('currentTimeLabel').textContent = formatTime(tickData.curTime);
            document.getElementById('cutPointLabel').textContent = tickData.playFull ? 'Playing Full' : `Hook Cut @ ${{formatTime(tickData.cutAt)}}`;
          }},
          (cue) => {{
            document.getElementById('nowPlayingTitle').textContent = cue.title;
            document.getElementById('nowPlayingArtist').textContent = cue.artist;
            renderQueue(setlist);
          }}
        );
        await engine.init();
      }}

      engine.start(setlist);
    }});

    function renderQueue(list) {{
      const queueListEl = document.getElementById('queueList');
      queueListEl.innerHTML = '';
      const currentLiveCue = engine ? engine.decks[engine.liveId]?.cue : null;
      const upcoming = list.filter(s => !currentLiveCue || s.song_id !== currentLiveCue.song_id);

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

    document.getElementById('skipBtn').addEventListener('click', () => {{
      if (engine) engine.skip();
    }});

    document.getElementById('togglePlayBtn').addEventListener('click', () => {{
      if (engine) {{
        const paused = engine.togglePlay();
        document.getElementById('togglePlayBtn').textContent = paused ? 'Resume' : 'Pause';
      }}
    }});

    document.getElementById('playFullBtn').addEventListener('click', () => {{
      if (engine) {{
        const isFull = engine.togglePlayFull();
        document.getElementById('playFullBtn').className = isFull 
          ? 'border border-lime text-lime px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition bg-lime/10'
          : 'border border-white/20 hover:border-white/50 text-white/70 px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition';
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

print("Generated standalone naux_party_clone.html successfully!")

