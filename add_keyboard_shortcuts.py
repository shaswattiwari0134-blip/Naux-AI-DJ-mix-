import shutil

with open("naux_party_clone.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add keyboard shortcut badge below player controls
target_markup = """          <div class="flex items-center gap-2">
            <button id="playFullBtn" class="border border-white/20 hover:border-white/50 text-white/70 px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition">
              Ride Full Song (Don't Cut)
            </button>
          </div>
        </div>
      </div>"""

replacement_markup = """          <div class="flex items-center gap-2">
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
      </div>"""

if target_markup in content:
    content = content.replace(target_markup, replacement_markup, 1)
    print("Added keyboard shortcuts badge to markup!")
else:
    print("Could not find exact target markup, check lines.")

# 2. Add MediaSession metadata update inside updateLiveTrackMetadata
target_meta = """      updateLiveTrackMetadata(cue) {
        if (!cue) return;
        document.getElementById('nowPlayingTitle').textContent = cue.title;
        document.getElementById('nowPlayingArtist').textContent = cue.artist;
        renderQueue(this.queue);
      }"""

replacement_meta = """      updateLiveTrackMetadata(cue) {
        if (!cue) return;
        document.getElementById('nowPlayingTitle').textContent = cue.title;
        document.getElementById('nowPlayingArtist').textContent = cue.artist;
        renderQueue(this.queue);

        // Hardware MediaSession metadata (for keyboard media keys, Bluetooth headphones & lockscreen)
        if ('mediaSession' in navigator) {
          try {
            navigator.mediaSession.metadata = new MediaMetadata({
              title: cue.title,
              artist: cue.artist,
              album: 'NAUX Party Set',
              artwork: [
                { src: `https://img.youtube.com/vi/${cue.youtube_ids[0]}/hqdefault.jpg`, sizes: '480x360', type: 'image/jpeg' }
              ]
            });
            navigator.mediaSession.playbackState = 'playing';
          } catch(e) {}
        }
      }"""

if target_meta in content:
    content = content.replace(target_meta, replacement_meta, 1)
    print("Added MediaSession metadata updates!")
else:
    print("Could not find target_meta, check formatting.")

# 3. Add Keyboard and MediaSession Event Handlers
target_end = """    document.getElementById('retuneBtn').addEventListener('click', () => {
      document.getElementById('playerView').classList.add('hidden');
      document.getElementById('setupView').classList.remove('hidden');
    });

  </script>"""

replacement_end = """    document.getElementById('retuneBtn').addEventListener('click', () => {
      document.getElementById('playerView').classList.add('hidden');
      document.getElementById('setupView').classList.remove('hidden');
    });

    // 1. HARDWARE MEDIA KEYS & BLUETOOTH HEADPHONES (MediaSession API)
    if ('mediaSession' in navigator) {
      try {
        navigator.mediaSession.setActionHandler('play', () => {
          engine.togglePlay();
          document.getElementById('togglePlayBtn').textContent = 'Pause';
          navigator.mediaSession.playbackState = 'playing';
        });
        navigator.mediaSession.setActionHandler('pause', () => {
          engine.togglePlay();
          document.getElementById('togglePlayBtn').textContent = 'Resume';
          navigator.mediaSession.playbackState = 'paused';
        });
        navigator.mediaSession.setActionHandler('nexttrack', () => {
          engine.skip();
        });
      } catch(e) {}
    }

    // 2. KEYBOARD SHORTCUTS (Space = Play/Pause, Right Arrow = Skip, S = Shuffle, F = Full)
    window.addEventListener('keydown', (e) => {
      // Ignore key shortcuts if typing in any text input
      const activeTag = document.activeElement ? document.activeElement.tagName : '';
      if (activeTag === 'INPUT' || activeTag === 'TEXTAREA') {
        return;
      }

      // SPACEBAR or 'K' -> Play/Pause
      if (e.code === 'Space' || e.key === ' ' || e.key.toLowerCase() === 'k') {
        e.preventDefault(); // Prevent page scroll down on Space!
        const paused = engine.togglePlay();
        document.getElementById('togglePlayBtn').textContent = paused ? 'Resume' : 'Pause';
        if ('mediaSession' in navigator) {
          navigator.mediaSession.playbackState = paused ? 'paused' : 'playing';
        }
      }
      // RIGHT ARROW (→) or 'N' -> Skip Hook
      else if (e.code === 'ArrowRight' || e.key.toLowerCase() === 'n') {
        e.preventDefault();
        engine.skip();
      }
      // 'S' -> Shuffle Upcoming Queue
      else if (e.key.toLowerCase() === 's') {
        engine.shuffleQueue();
      }
      // 'F' -> Toggle Play Full Song
      else if (e.key.toLowerCase() === 'f') {
        const isFull = engine.togglePlayFull();
        document.getElementById('playFullBtn').className = isFull 
          ? 'border border-lime text-lime px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition bg-lime/10'
          : 'border border-white/20 hover:border-white/50 text-white/70 px-4 py-2.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition';
      }
    });

  </script>"""

if target_end in content:
    content = content.replace(target_end, replacement_end, 1)
    print("Added keyboard shortcuts & media session event handlers!")
else:
    print("Could not find target_end, check formatting.")

with open("naux_party_clone.html", "w", encoding="utf-8") as f:
    f.write(content)

# Also update index.html
shutil.copy("naux_party_clone.html", "index.html")
print("Updated naux_party_clone.html and index.html successfully!")

