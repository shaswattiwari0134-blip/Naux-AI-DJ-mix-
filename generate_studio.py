cue_studio_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NAUX Cue Studio · Custom Hook & Track Editor</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
  <style>
    body { background-color: #080808; color: #f5f5f5; font-family: 'Inter', sans-serif; }
    .font-anton { font-family: 'Anton', sans-serif; letter-spacing: 0.05em; }
    .text-lime { color: #d4ff00; }
    .bg-lime { background-color: #d4ff00; }
    .border-lime { border-color: #d4ff00; }
    input[type=range] { accent-color: #d4ff00; }
  </style>
</head>
<body class="min-h-screen p-6 max-w-4xl mx-auto flex flex-col justify-between">

  <!-- Header -->
  <header class="flex justify-between items-center border-b border-white/10 pb-4 mb-6">
    <div>
      <h1 class="text-3xl font-anton text-lime tracking-wide">CUE STUDIO</h1>
      <p class="text-xs text-white/50 uppercase tracking-widest">Find hooks, trim intros, and export tracks to NAUX</p>
    </div>
    <a href="naux_party_clone.html" class="border border-white/20 hover:border-lime text-xs uppercase px-4 py-2 rounded-xl text-white/70 hover:text-lime transition font-bold">
      Back to Party Player ↗
    </a>
  </header>

  <!-- Studio Workspace -->
  <main class="space-y-6 flex-1">

    <!-- Step 1: Input URL -->
    <div class="bg-white/5 border border-white/10 rounded-3xl p-6 space-y-4">
      <h2 class="text-xs uppercase font-bold text-white/40 tracking-wider">1. Load Any YouTube Song</h2>
      <div class="flex gap-3">
        <input id="videoInput" type="text" placeholder="Paste YouTube Video URL or ID (e.g. uTuchIYZdbM)" 
               value="uTuchIYZdbM" 
               class="flex-1 bg-black/60 border border-white/20 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:border-lime font-mono text-white">
        <button id="loadBtn" class="bg-lime text-black font-anton px-6 py-3 rounded-2xl text-lg hover:brightness-110 transition uppercase">
          Load Video
        </button>
      </div>
    </div>

    <!-- Step 2: Player & Trimmer -->
    <div class="bg-white/5 border border-white/10 rounded-3xl p-6 space-y-6">
      <div class="flex justify-between items-center">
        <h2 class="text-xs uppercase font-bold text-white/40 tracking-wider">2. Interactive Hook Trimmer</h2>
        <span id="playerStatePill" class="text-xs font-mono text-white/50">Player Ready</span>
      </div>

      <!-- YouTube Embed Frame -->
      <div class="aspect-video w-full max-w-xl mx-auto rounded-2xl overflow-hidden bg-black border border-white/10 shadow-2xl">
        <div id="studio-player" class="w-full h-full"></div>
      </div>

      <!-- Live Timestamp Readout -->
      <div class="grid grid-cols-3 gap-4 text-center font-mono">
        <div class="bg-white/5 p-3 rounded-2xl border border-white/5">
          <p class="text-xs text-white/40 mb-1 uppercase">Hook In (Entry)</p>
          <p id="entryDisplay" class="text-xl font-bold text-lime">0:13</p>
        </div>
        <div class="bg-white/5 p-3 rounded-2xl border border-white/5">
          <p class="text-xs text-white/40 mb-1 uppercase">Current Position</p>
          <p id="posDisplay" class="text-xl font-bold text-white">0:00</p>
        </div>
        <div class="bg-white/5 p-3 rounded-2xl border border-white/5">
          <p class="text-xs text-white/40 mb-1 uppercase">Mix Out (Exit)</p>
          <p id="exitDisplay" class="text-xl font-bold text-amber-400">1:27</p>
        </div>
      </div>

      <!-- Sliders -->
      <div class="space-y-4">
        <div>
          <div class="flex justify-between text-xs text-white/50 mb-1">
            <span>Hook Drop (Entry Seconds): <strong id="entryValLabel" class="text-lime">13s</strong></span>
            <button id="setEntryToCurrent" class="text-lime hover:underline font-bold text-xs uppercase">Set to Current Time</button>
          </div>
          <input id="entryRange" type="range" min="0" max="300" value="13" class="w-full">
        </div>

        <div>
          <div class="flex justify-between text-xs text-white/50 mb-1">
            <span>Mix Out (Exit Seconds): <strong id="exitValLabel" class="text-amber-400">87s</strong></span>
            <button id="setExitToCurrent" class="text-amber-400 hover:underline font-bold text-xs uppercase">Set to Current Time</button>
          </div>
          <input id="exitRange" type="range" min="0" max="300" value="87" class="w-full">
        </div>
      </div>

      <!-- Preview Buttons -->
      <div class="flex flex-wrap gap-3 pt-2">
        <button id="previewHookBtn" class="bg-white/10 hover:bg-white/20 border border-white/20 px-5 py-2.5 rounded-xl text-xs font-bold uppercase tracking-wider transition">
          ▶ Test Hook Drop (-2s lead-in)
        </button>
        <button id="previewExitBtn" class="bg-white/10 hover:bg-white/20 border border-white/20 px-5 py-2.5 rounded-xl text-xs font-bold uppercase tracking-wider transition">
          ▶ Test Outro Cut (-3s before mix)
        </button>
      </div>
    </div>

    <!-- Step 3: Track Metadata & Export -->
    <div class="bg-white/5 border border-white/10 rounded-3xl p-6 space-y-4">
      <h2 class="text-xs uppercase font-bold text-white/40 tracking-wider">3. Metadata & Library Export</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
        <input id="metaTitle" type="text" placeholder="Song Title (e.g. Tauba Tauba)" value="Tauba Tauba" 
               class="bg-black/60 border border-white/20 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-lime">
        <input id="metaArtist" type="text" placeholder="Artist (e.g. Karan Aujla)" value="Karan Aujla" 
               class="bg-black/60 border border-white/20 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-lime">
        <select id="metaLang" class="bg-black/60 border border-white/20 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-lime text-white">
          <option value="punjabi">Punjabi</option>
          <option value="hindi">Hindi</option>
          <option value="english">English</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div class="flex gap-3 pt-2">
        <button id="exportJsonBtn" class="flex-1 bg-lime text-black font-anton py-3.5 rounded-xl text-lg hover:brightness-110 transition uppercase">
          Copy Song JSON
        </button>
        <button id="saveLocalBtn" class="bg-white/10 border border-white/20 hover:border-lime text-white font-bold px-6 py-3.5 rounded-xl text-xs uppercase tracking-wider transition">
          Save to Browser Storage
        </button>
      </div>
      <p id="exportMsg" class="text-xs text-lime font-mono text-center hidden"></p>
    </div>

  </main>

  <footer class="text-center text-xs text-white/30 pt-6">
    NAUX Cue Studio · Calibrate exact hook entry and exit cut points for seamless party transitions.
  </footer>

  <!-- Scripts -->
  <script src="https://www.youtube.com/iframe_api"></script>
  <script>
    let player = null;
    let videoId = 'uTuchIYZdbM';
    let duration = 208;
    let pollInterval = null;

    function formatTime(sec) {
      sec = Math.max(0, Math.floor(sec));
      const m = Math.floor(sec / 60);
      const s = sec % 60;
      return `${m}:${s < 10 ? '0' : ''}${s}`;
    }

    function parseYouTubeId(input) {
      input = input.trim();
      const match = input.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([\w-]{11})/);
      return match ? match[1] : (input.length === 11 ? input : null);
    }

    window.onYouTubeIframeAPIReady = function() {
      player = new YT.Player('studio-player', {
        videoId: videoId,
        playerVars: { autoplay: 0, controls: 1, modestbranding: 1, rel: 0 },
        events: {
          onReady: () => {
            document.getElementById('playerStatePill').textContent = 'Video Loaded';
            duration = Math.floor(player.getDuration()) || 208;
            updateSliderRanges();
            startTracking();
          }
        }
      });
    };

    function startTracking() {
      if (pollInterval) clearInterval(pollInterval);
      pollInterval = setInterval(() => {
        if (player && typeof player.getCurrentTime === 'function') {
          const cur = player.getCurrentTime();
          document.getElementById('posDisplay').textContent = formatTime(cur);
        }
      }, 250);
    }

    function updateSliderRanges() {
      const entrySlider = document.getElementById('entryRange');
      const exitSlider = document.getElementById('exitRange');
      entrySlider.max = duration;
      exitSlider.max = duration;
    }

    // Sliders event
    const entryRange = document.getElementById('entryRange');
    const exitRange = document.getElementById('exitRange');

    entryRange.addEventListener('input', () => {
      const val = Number(entryRange.value);
      document.getElementById('entryValLabel').textContent = `${val}s`;
      document.getElementById('entryDisplay').textContent = formatTime(val);
    });

    exitRange.addEventListener('input', () => {
      const val = Number(exitRange.value);
      document.getElementById('exitValLabel').textContent = `${val}s`;
      document.getElementById('exitDisplay').textContent = formatTime(val);
    });

    // Set buttons
    document.getElementById('setEntryToCurrent').addEventListener('click', () => {
      if (!player) return;
      const cur = Math.floor(player.getCurrentTime());
      entryRange.value = cur;
      entryRange.dispatchEvent(new Event('input'));
    });

    document.getElementById('setExitToCurrent').addEventListener('click', () => {
      if (!player) return;
      const cur = Math.floor(player.getCurrentTime());
      exitRange.value = cur;
      exitRange.dispatchEvent(new Event('input'));
    });

    // Preview
    document.getElementById('previewHookBtn').addEventListener('click', () => {
      if (!player) return;
      const target = Math.max(0, Number(entryRange.value) - 2);
      player.seekTo(target, true);
      player.playVideo();
    });

    document.getElementById('previewExitBtn').addEventListener('click', () => {
      if (!player) return;
      const target = Math.max(0, Number(exitRange.value) - 3);
      player.seekTo(target, true);
      player.playVideo();
    });

    // Load video
    document.getElementById('loadBtn').addEventListener('click', () => {
      const raw = document.getElementById('videoInput').value;
      const parsed = parseYouTubeId(raw);
      if (!parsed) {
        alert('Could not parse YouTube Video ID. Please check URL.');
        return;
      }
      videoId = parsed;
      if (player && player.loadVideoById) {
        player.loadVideoById(videoId);
        setTimeout(() => {
          duration = Math.floor(player.getDuration()) || 208;
          updateSliderRanges();
        }, 1500);
      }
    });

    // Export JSON
    document.getElementById('exportJsonBtn').addEventListener('click', () => {
      const songData = {
        song_id: document.getElementById('metaTitle').value.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '-' + Math.floor(Math.random() * 1000),
        title: document.getElementById('metaTitle').value,
        artist: document.getElementById('metaArtist').value,
        youtube_ids: [videoId],
        duration_sec: duration,
        entry_sec: Number(entryRange.value),
        exit_sec: Number(exitRange.value),
        language: document.getElementById('metaLang').value,
        energy: 8,
        banger: true
      };

      const jsonStr = JSON.stringify(songData, null, 2);
      navigator.clipboard.writeText(jsonStr);
      const msg = document.getElementById('exportMsg');
      msg.textContent = '✓ Copied song JSON to clipboard! Paste into your library.';
      msg.classList.remove('hidden');
      setTimeout(() => msg.classList.add('hidden'), 4000);
    });

    // Save to LocalStorage
    document.getElementById('saveLocalBtn').addEventListener('click', () => {
      const songData = {
        song_id: document.getElementById('metaTitle').value.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
        title: document.getElementById('metaTitle').value,
        artist: document.getElementById('metaArtist').value,
        youtube_ids: [videoId],
        duration_sec: duration,
        entry_sec: Number(entryRange.value),
        exit_sec: Number(exitRange.value),
        language: document.getElementById('metaLang').value,
        energy: 8,
        banger: true
      };

      let customList = [];
      try {
        customList = JSON.parse(localStorage.getItem('naux_custom_tracks') || '[]');
      } catch(e) {}
      customList.push(songData);
      localStorage.setItem('naux_custom_tracks', JSON.stringify(customList));

      const msg = document.getElementById('exportMsg');
      msg.textContent = `✓ Saved "${songData.title}" to browser storage!`;
      msg.classList.remove('hidden');
      setTimeout(() => msg.classList.add('hidden'), 4000);
    });
  </script>
</body>
</html>
'''

with open("naux_cue_studio.html", "w", encoding="utf-8") as out:
    out.write(cue_studio_html)

print("Generated naux_cue_studio.html successfully!")

