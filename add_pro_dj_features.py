import shutil

with open("naux_party_clone.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Master Volume & Crossfade Speed controls to Player Controls
target_controls = """          <div class="flex items-center gap-2">
            <button id="playFullBtn" class="border border-white/20 hover:border-white/50 text-white/70 px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition">
              Ride Full Song (Don't Cut)
            </button>
          </div>
        </div>"""

replacement_controls = """          <div class="flex flex-wrap items-center gap-3">
            <!-- Crossfade Duration Selector -->
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

            <!-- Play Full Toggle -->
            <button id="playFullBtn" class="border border-white/20 hover:border-white/50 text-white/70 px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition">
              Ride Full Song (Don't Cut)
            </button>
          </div>
        </div>"""

if target_controls in content:
    content = content.replace(target_controls, replacement_controls, 1)
    print("Added Master Volume & Crossfade Duration controls!")
else:
    print("Target controls markup not matched, check formatting.")

# 2. Add Export & Save Setlist button to Queue header
target_queue_header = """          <div class="flex items-center gap-2">
            <button id="shuffleQueueBtn" class="bg-lime/10 border border-lime/30 hover:bg-lime hover:text-black text-lime font-anton px-4 py-2 rounded-xl text-xs uppercase tracking-wider transition flex items-center gap-1.5">
              <span>🔀</span> Shuffle Queue
            </button>
            <button id="retuneBtn" class="border border-white/10 hover:border-white/30 text-white/50 hover:text-white px-3 py-2 rounded-xl text-xs uppercase tracking-wider transition">
              Retune
            </button>
          </div>"""

replacement_queue_header = """          <div class="flex flex-wrap items-center gap-2">
            <button id="shuffleQueueBtn" class="bg-lime/10 border border-lime/30 hover:bg-lime hover:text-black text-lime font-anton px-4 py-2 rounded-xl text-xs uppercase tracking-wider transition flex items-center gap-1.5">
              <span>🔀</span> Shuffle Queue
            </button>
            <button id="exportSetlistBtn" class="border border-white/20 hover:border-lime hover:text-lime text-white/70 font-anton px-3 py-2 rounded-xl text-xs uppercase tracking-wider transition" title="Save current queue to JSON">
              💾 Export Set
            </button>
            <button id="retuneBtn" class="border border-white/10 hover:border-white/30 text-white/50 hover:text-white px-3 py-2 rounded-xl text-xs uppercase tracking-wider transition">
              Retune
            </button>
          </div>"""

if target_queue_header in content:
    content = content.replace(target_queue_header, replacement_queue_header, 1)
    print("Added Export Setlist button to Queue header!")
else:
    print("Target queue header markup not matched, check formatting.")

# 3. Add engine property & methods for masterVolume and crossfadeDuration
target_engine_init = """        this.ready = false;
        this.awaitingStart = null;
        this.pendingHandoff = null;
        this.tickTimer = null;
        this.fadeTimer = null;"""

replacement_engine_init = """        this.ready = false;
        this.awaitingStart = null;
        this.pendingHandoff = null;
        this.tickTimer = null;
        this.fadeTimer = null;
        this.masterVolume = 100;
        this.crossfadeDuration = 1500;"""

if target_engine_init in content:
    content = content.replace(target_engine_init, replacement_engine_init, 1)
    print("Added masterVolume & crossfadeDuration state to Engine!")

# 4. Update startFade to use this.crossfadeDuration and masterVolume scaling
target_fade_logic = """        const start = performance.now();
        const FADE_MS = 1500;

        if (this.fadeTimer) clearInterval(this.fadeTimer);
        this.fadeTimer = setInterval(() => {
          const elapsed = performance.now() - start;
          const s = Math.min(1, elapsed / FADE_MS);

          const inVol = Math.round(100 * Math.sin(s * Math.PI / 2));
          const outVol = Math.round(100 * Math.cos(s * Math.PI / 2));

          incoming.volume = inVol;
          outgoing.volume = outVol;
          try {
            incoming.player.setVolume(inVol);
            outgoing.player.setVolume(outVol);
          } catch(e) {}"""

replacement_fade_logic = """        const start = performance.now();
        const FADE_MS = this.crossfadeDuration || 1500;

        if (this.fadeTimer) clearInterval(this.fadeTimer);
        this.fadeTimer = setInterval(() => {
          const elapsed = performance.now() - start;
          const s = Math.min(1, elapsed / FADE_MS);

          const rawIn = Math.round(100 * Math.sin(s * Math.PI / 2));
          const rawOut = Math.round(100 * Math.cos(s * Math.PI / 2));

          incoming.volume = rawIn;
          outgoing.volume = rawOut;

          // Scale by masterVolume
          const inVol = Math.round((rawIn * this.masterVolume) / 100);
          const outVol = Math.round((rawOut * this.masterVolume) / 100);

          try {
            incoming.player.setVolume(inVol);
            outgoing.player.setVolume(outVol);
          } catch(e) {}"""

if target_fade_logic in content:
    content = content.replace(target_fade_logic, replacement_fade_logic, 1)
    print("Updated startFade with dynamic fade duration and master volume scaling!")

# 5. Add UI Event Listeners for Master Volume, Crossfade Speed, and Export Setlist
target_listeners = """    document.getElementById('skipBtn').addEventListener('click', () => engine.skip());"""

replacement_listeners = """    // Master Volume Slider
    document.getElementById('masterVolumeSlider').addEventListener('input', (e) => {
      const vol = Number(e.target.value);
      engine.masterVolume = vol;
      document.getElementById('masterVolLabel').textContent = `${vol}%`;
      const live = engine.decks[engine.liveId];
      if (live && live.player && live.status === 'live') {
        try { live.player.setVolume(Math.round((live.volume * vol) / 100)); } catch(err) {}
      }
    });

    // Crossfade Duration Selector
    document.getElementById('fadeDurationSelect').addEventListener('change', (e) => {
      const ms = Number(e.target.value);
      engine.crossfadeDuration = ms;
      logToScreen(`Set crossfade duration to ${ms / 1000}s`);
    });

    // Export Setlist to JSON
    document.getElementById('exportSetlistBtn').addEventListener('click', () => {
      if (!engine.queue || engine.queue.length === 0) {
        alert("The queue is currently empty.");
        return;
      }
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(engine.queue, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", `party_set_${Date.now()}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
      logToScreen("💾 Exported setlist to party_set.json!");
    });

    document.getElementById('skipBtn').addEventListener('click', () => engine.skip());"""

if target_listeners in content:
    content = content.replace(target_listeners, replacement_listeners, 1)
    print("Added Master Volume, Fade Duration, and Export Setlist event listeners!")

with open("naux_party_clone.html", "w", encoding="utf-8") as f:
    f.write(content)

# Update index.html
shutil.copy("naux_party_clone.html", "index.html")
print("Saved both naux_party_clone.html and index.html successfully!")

