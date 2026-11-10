# NAUX Party DJ Engine · Reverse-Engineered Architecture & Implementation

An automated party DJ web application inspired by [NAUX.party](https://www.naux.party/) (*"The aux, handled"*). It automates party music curation across all languages and artists, skipping slow intros and awkward pauses by **dropping straight into the song's hook, cutting before the outro, and crossfading seamlessly into the next track**.

---

## 🎧 Key Features

* **Dual-Deck YouTube Player**: Operates two hidden YouTube players (Deck A & Deck B) with zero audio hosting costs or Spotify Premium requirements.
* **1.5s Equal-Power Sinusoidal Crossfade**: Smooth, club-grade volume transitions between incoming and outgoing tracks.
* **2,081+ Curated Tracks (50+ Songs Per Artist)**: Every major artist (Diljit Dosanjh, Karan Aujla, Arijit Singh, Sidhu Moose Wala, AP Dhillon, Yo Yo Honey Singh, Badshah, Shubh, Neha Kakkar, Atif Aslam, Sonu Nigam, Shreya Ghoshal, Sunidhi Chauhan, Kumar Sanu, Udit Narayan, Alka Yagnik, Kishore Kumar, B Praak, Guru Randhawa, Harrdy Sandhu, The Weeknd, Drake, Justin Bieber, Taylor Swift, Ed Sheeran, Eminem, Anirudh Ravichander, A.R. Rahman, etc.) has at least 50+ verified tracks ready for non-stop mixing.
* **Universal Artist Search & Play Now**: Search any artist in real time with 1-click *Play Now ▶*, *Play Next ⏭*, or *Add to End ➕*.
* **Play ANY YouTube Video**: Paste any YouTube watch URL or video ID to cue unreleased tracks, indie songs, or any language in the world.
* **Full Queue Control**:
  * ⠿ **Drag-and-Drop** reordering to place songs anywhere.
  * 🔀 **Shuffle Queue** without interrupting the currently playing song.
  * ▲ / ▼ Nudge up and down buttons + ✕ Remove.
* **Screen Wake Lock**: Prevents phones and laptops from going to sleep and cutting off party audio.
* **Guest Mobile Room (`room.html`)**: Guests scan a QR code on their phone to search and request songs without touching the host's laptop.
* **Automated Hook Detector (`auto_cue.py`)**: Uses YouTube's "Most Replayed" heat map to detect chorus/drop timestamps automatically.
* **Visual Cue Studio (`naux_cue_studio.html`)**: Test and calibrate custom hook entry and mix-out cut points.

---

## 📁 Project Structure

```
├── index.html                 # Main party player (identical to naux_party_clone.html)
├── naux_party_clone.html      # Standalone dual-deck player with drag-and-drop & search
├── naux_full_library.json     # Complete database of 1,293+ songs with verified hook cue points
├── naux_cue_studio.html       # Visual hook editor & track calibration tool
├── room.html                  # Mobile-first guest room for crowd song requests
├── auto_cue.py                # Automated YouTube heatmap hook detection script
├── naux_server.py             # Full Python server with REST endpoints & room state sync
├── run_naux.bat               # 1-click Windows batch launcher
├── vercel.json                # Vercel deployment configuration
└── netlify.toml               # Netlify deployment configuration
```

---

## 🚀 How to Run Locally

### Method 1: 1-Click Launcher (Windows)
Double-click **`run_naux.bat`** in your file explorer. It starts a local server on port 3000 and automatically opens:
👉 **`http://localhost:3000/`**

### Method 2: Python Command
Run in your terminal:
```bash
python -m http.server 3000
```
Then visit:
👉 **`http://localhost:3000/`**

### Method 3: Full-Stack Party Room Server
To enable mobile guest song requests from other devices on your Wi-Fi:
```bash
python naux_server.py
```
* **Host Player**: `http://localhost:3000/`
* **Guest Request Room**: `http://localhost:3000/room.html?code=AUX1`

---

## 🌐 Free Cloud Deployment (Vercel / Netlify / GitHub Pages)

This project has zero build step requirements and can be deployed for free:

### Deploy to Vercel:
1. Push this folder to a GitHub repository.
2. Go to [vercel.com](https://vercel.com) and click **"Add New Project"**.
3. Select your repository and click **Deploy**. Vercel will automatically use `vercel.json` and `index.html`.

### Deploy to Netlify:
1. Drag and drop this folder directly into [app.netlify.com/drop](https://app.netlify.com/drop).
2. Netlify will publish your site in under 10 seconds.

---

## 🔬 How the Technology Works (Reverse-Engineered Architecture)

### 1. Dual-Deck Preloading Architecture
```
┌──────────────────────────────────────────────────────────┐
│                   DUAL-DECK ENGINE                       │
│                                                          │
│   ┌───────────────────────────┐  ┌─────────────────────┐ │
│   │   DECK A (YouTube Player) │  │ DECK B (YouTube)    │ │
│   │   Role: LIVE (100% Vol)   │  │ Role: PRELOAD (0%)  │ │
│   │   Playing at: entry_sec   │  │ Cued at: entry_sec  │ │
│   │   Cuts at: exit_sec       │  │ Status: READY       │ │
│   └─────────────┬─────────────┘  └──────────┬──────────┘ │
│                 │                           │            │
│                 ▼                           ▼            │
│       1.5s Equal-Power Crossfade: sin(s*π/2) & cos(s*π/2)│
└──────────────────────────────────────────────────────────┘
```

1. **Deck A** plays the live track.
2. While Deck A is audible, **Deck B** is initialized with volume 0 (`mute()`, `setVolume(0)`).
3. Deck B calls `loadVideoById({ videoId, startSeconds: entry_sec })`.
4. When Deck B fires `onStateChange === 1` (playing) or `state === 5` (cued), it immediately pauses and seeks to `entry_sec`. It is now buffered in memory in the `ready` state.
5. When Deck A reaches `cutPoint` (`min(cue.exit_sec, duration - 1.5)`), the engine un-mutes Deck B and executes a sinusoidal equal-power crossfade over 1,500ms:
   $$\text{Volume}_{\text{incoming}} = 100 \times \sin\left(\frac{s \cdot \pi}{2}\right)$$
   $$\text{Volume}_{\text{outgoing}} = 100 \times \cos\left(\frac{s \cdot \pi}{2}\right)$$
   *(where $s = \frac{\Delta t}{1500}$)*.
6. Once the crossfade reaches $s = 1$, the outgoing deck is paused, muted, reset to `empty`, and immediately loads the track *after next* in `preload` mode.

### 2. Automated Hook Detection via YouTube Replay Heatmaps
In `auto_cue.py`, YouTube's watch page data (`ytInitialData`) is scraped for the `frameworkUpdates` entity batch containing `intensityScoreNormalized` markers (the "Most Replayed" graph). The timestamp with the highest intensity score after the intro (between 8s and 60s) is automatically detected as the song's **drop/hook**.

### 3. Custom DJ Song Maker
Clicking **`🎛️ Make Song DJ`** opens the interactive studio modal:
- Load any YouTube video URL or search from the 1,293+ library.
- Scrub the visual timeline and audition drops live.
- Tap `📍 Set Drop-in at Current Time` to capture the exact beat drop.
- Tap `📍 Set Cut at Current Time` to capture the hook cutoff point.
- Audition drops with `▶ Test Drop (6s)` or `▶ Test Hook Cut (4s)`.
- Instantly drop your custom DJ edit live on the aux with `⚡ Play DJ Cut Now`, or queue it into the party set.

### 4. Multi-Artist Spotlight DJ Mode
Filter the party setlist by single or multiple singers:
- **Single Singer**: Select one artist (e.g., *Diljit Dosanjh*), and only their tracks will play back-to-back.
- **Multiple Singers**: Select multiple artists (e.g., *Diljit Dosanjh + Karan Aujla + Sidhu Moose Wala*). Only tracks featuring those artists will play, with automatic anti-repetition interleaving.
- **Quick-Pills**: 24 top artists ready to tap with song counts.
- **Search Catalog**: Search and filter across 847 unique artists in the database.
- **Live Mid-Party Retuning**: Tap `⚙️ Change Singers` to update the singer roster while music is playing.

### 5. Keyboard Shortcuts & Pro DJ Controls
- **Space** or **K**: Play / Pause
- **→ (Right Arrow)** or **N**: Skip to next hook drop
- **S**: Shuffle upcoming queue
- **F**: Toggle Ride Full Song mode
- **Fade Speed Selector**: 0.5s (Quick Drop), 1.5s (Standard Mix), 3.0s (Long Blend)
- **Master Volume Slider**: 0% to 100% speaker output control
- **Export Set**: Save your curated party queue to JSON


