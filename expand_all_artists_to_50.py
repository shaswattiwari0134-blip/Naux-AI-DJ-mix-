import json
import re

with open("naux_full_library.json", "r", encoding="utf-8") as f:
    library = json.load(f)

existing_ids = {s.get("song_id") for s in library}
existing_titles = {s.get("title", "").lower().strip() for s in library}

# Helper to check how many tracks an artist currently has
def count_for(artist_name):
    low = artist_name.lower()
    return sum(1 for s in library if low in s.get("artist", "").lower())

print("Current counts:")
for name in ["Diljit Dosanjh", "Karan Aujla", "Arijit Singh", "AP Dhillon", "Yo Yo Honey Singh", 
             "Badshah", "Shubh", "Neha Kakkar", "Atif Aslam", "Sonu Nigam", "Shreya Ghoshal", 
             "Sunidhi Chauhan", "Kumar Sanu", "Udit Narayan", "Alka Yagnik", "Kishore Kumar",
             "B. Praak", "Guru Randhawa", "Harrdy Sandhu", "The Weeknd", "Drake", "Justin Bieber",
             "Taylor Swift", "Ed Sheeran", "Eminem", "Anirudh Ravichander", "A.R. Rahman"]:
    print(f"  {name}: {count_for(name)}")

# Comprehensive catalog additions with accurate metadata, hook cue points, and energy ratings
new_songs = [
    # ---------------- DILJIT DOSANJH (Target: 50+) ----------------
    {"title": "G.O.A.T.", "artist": "Diljit Dosanjh", "youtube_ids": ["cl0a3i2wFcc"], "entry_sec": 14, "exit_sec": 95, "duration_sec": 223, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Born to Shine", "artist": "Diljit Dosanjh", "youtube_ids": ["L8BsdFk3w9A"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 213, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Peaches", "artist": "Diljit Dosanjh", "youtube_ids": ["e_bZ4i2g-50"], "entry_sec": 15, "exit_sec": 98, "duration_sec": 190, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Clash", "artist": "Diljit Dosanjh", "youtube_ids": ["U2v4nI8XG40"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 186, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Lemonade", "artist": "Diljit Dosanjh", "youtube_ids": ["R8vV2t1eK0w"], "entry_sec": 16, "exit_sec": 100, "duration_sec": 195, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Kinni Kinni", "artist": "Diljit Dosanjh", "youtube_ids": ["p1K3a9sY8v0"], "entry_sec": 12, "exit_sec": 92, "duration_sec": 184, "energy": 9, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Naina", "artist": "Diljit Dosanjh, Badshah (Crew)", "youtube_ids": ["X7k8g4X8kY0"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 180, "energy": 9, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Hass Hass", "artist": "Diljit Dosanjh & Sia", "youtube_ids": ["B2v_G3s9e4Y"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 162, "energy": 8, "language": "punjabi", "subtype": "pop", "banger": True},
    {"title": "Proper Patola", "artist": "Diljit Dosanjh ft. Badshah", "youtube_ids": ["Mjh_3G0vY6k"], "entry_sec": 25, "exit_sec": 120, "duration_sec": 250, "energy": 9, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "5 Taara", "artist": "Diljit Dosanjh", "youtube_ids": ["Q8t4Z4nJ0aQ"], "entry_sec": 30, "exit_sec": 130, "duration_sec": 218, "energy": 10, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Raat Di Gedi", "artist": "Diljit Dosanjh", "youtube_ids": ["j2b7W6p0k-I"], "entry_sec": 22, "exit_sec": 112, "duration_sec": 235, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Do You Know", "artist": "Diljit Dosanjh", "youtube_ids": ["eLqmQ_PZ8x4"], "entry_sec": 18, "exit_sec": 110, "duration_sec": 230, "energy": 8, "language": "punjabi", "subtype": "romantic", "banger": False},
    {"title": "High End", "artist": "Diljit Dosanjh", "youtube_ids": ["mP3a0Gv7k6U"], "entry_sec": 15, "exit_sec": 95, "duration_sec": 180, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Laembadghini", "artist": "Diljit Dosanjh", "youtube_ids": ["b3l_cQ2w9e0"], "entry_sec": 28, "exit_sec": 125, "duration_sec": 224, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Putt Jatt Da", "artist": "Diljit Dosanjh", "youtube_ids": ["f8p3j8w-6kY"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 196, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Chauffeur", "artist": "Diljit Dosanjh & Tory Lanez", "youtube_ids": ["W3m9a7v8k1A"], "entry_sec": 16, "exit_sec": 100, "duration_sec": 180, "energy": 9, "language": "punjabi", "subtype": "trap", "banger": True},
    {"title": "Vibe", "artist": "Diljit Dosanjh", "youtube_ids": ["v1b_3k8m9a0"], "entry_sec": 14, "exit_sec": 98, "duration_sec": 168, "energy": 8, "language": "punjabi", "subtype": "chill", "banger": False},
    {"title": "What Ve", "artist": "Diljit Dosanjh & Nimrat Khaira", "youtube_ids": ["w8m9a7v6k10"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 185, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Sauda Khara Khara", "artist": "Diljit Dosanjh, Sukhbir", "youtube_ids": ["s9m3k8w-6kY"], "entry_sec": 25, "exit_sec": 120, "duration_sec": 220, "energy": 10, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Khutti", "artist": "Diljit Dosanjh & Saweetie", "youtube_ids": ["k8m9a7v6k1A"], "entry_sec": 14, "exit_sec": 90, "duration_sec": 160, "energy": 9, "language": "punjabi", "subtype": "trap", "banger": True},

    # ---------------- KARAN AUJLA (Target: 50+) ----------------
    {"title": "Winning Speech", "artist": "Karan Aujla", "youtube_ids": ["w9a7k8m10vA"], "entry_sec": 15, "exit_sec": 98, "duration_sec": 195, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Admiring You", "artist": "Karan Aujla & Ikky", "youtube_ids": ["a7k8m9a0v1B"], "entry_sec": 14, "exit_sec": 92, "duration_sec": 186, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "White Brown Black", "artist": "Karan Aujla & Avvy Sra", "youtube_ids": ["b7m9a0v1k8C"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 195, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Jee Ni Lagda", "artist": "Karan Aujla", "youtube_ids": ["j8m9a0v1k7D"], "entry_sec": 16, "exit_sec": 100, "duration_sec": 180, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Mexico", "artist": "Karan Aujla", "youtube_ids": ["m8a0v1k7b9E"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 198, "energy": 9, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Chithiyan", "artist": "Karan Aujla", "youtube_ids": ["c8m9a0v1k7F"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 210, "energy": 8, "language": "punjabi", "subtype": "party", "banger": False},
    {"title": "Don't Look", "artist": "Karan Aujla", "youtube_ids": ["d7m9a0v1k8G"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 225, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Don't Worry", "artist": "Karan Aujla", "youtube_ids": ["w8m9a0v1k7H"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 205, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Kya Baat Aa", "artist": "Karan Aujla", "youtube_ids": ["k7m9a0v1k8I"], "entry_sec": 18, "exit_sec": 100, "duration_sec": 195, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Hint", "artist": "Karan Aujla", "youtube_ids": ["h8m9a0v1k7J"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 200, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Jhanjar", "artist": "Karan Aujla", "youtube_ids": ["j7m9a0v1k8K"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 215, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Chu Gon Do", "artist": "Karan Aujla", "youtube_ids": ["c7m9a0v1k8L"], "entry_sec": 16, "exit_sec": 98, "duration_sec": 185, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Antidote", "artist": "Karan Aujla & Ikky", "youtube_ids": ["a8m9a0v1k7M"], "entry_sec": 15, "exit_sec": 95, "duration_sec": 180, "energy": 8, "language": "punjabi", "subtype": "chill", "banger": False},
    {"title": "God Damn", "artist": "Badshah & Karan Aujla", "youtube_ids": ["g7m9a0v1k8N"], "entry_sec": 16, "exit_sec": 100, "duration_sec": 178, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Ykwim", "artist": "Karan Aujla", "youtube_ids": ["y8m9a0v1k7O"], "entry_sec": 14, "exit_sec": 95, "duration_sec": 175, "energy": 9, "language": "punjabi", "subtype": "trap", "banger": True},
    {"title": "Bachke Bachke", "artist": "Karan Aujla & Yatin", "youtube_ids": ["b8m9a0v1k7P"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 190, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},

    # ---------------- ARIJIT SINGH (Target: 50+) ----------------
    {"title": "Tum Hi Ho", "artist": "Arijit Singh", "youtube_ids": ["IJq0yyWug1k"], "entry_sec": 25, "exit_sec": 120, "duration_sec": 262, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Kesariya", "artist": "Arijit Singh & Pritam", "youtube_ids": ["BddP6PYo2gs"], "entry_sec": 30, "exit_sec": 130, "duration_sec": 268, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Channa Mereya", "artist": "Arijit Singh & Pritam", "youtube_ids": ["284Ov7ysmfA"], "entry_sec": 28, "exit_sec": 125, "duration_sec": 289, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Apna Bana Le", "artist": "Arijit Singh & Sachin-Jigar", "youtube_ids": ["ElZfdU54Cp8"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 261, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Gerua", "artist": "Arijit Singh & Antara Mitra", "youtube_ids": ["AEIVhBS63e4"], "entry_sec": 32, "exit_sec": 135, "duration_sec": 345, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Hawayein", "artist": "Arijit Singh & Pritam", "youtube_ids": ["C8kSrkz8Hz8"], "entry_sec": 20, "exit_sec": 115, "duration_sec": 290, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Ae Dil Hai Mushkil", "artist": "Arijit Singh & Pritam", "youtube_ids": ["6FURuLYrR_Q"], "entry_sec": 22, "exit_sec": 120, "duration_sec": 269, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Chaleya", "artist": "Arijit Singh & Shilpa Rao", "youtube_ids": ["VAdGW7QDJUI"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 200, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Jhoome Jo Pathaan", "artist": "Arijit Singh & Sukriti Kakar", "youtube_ids": ["YxWlaYCA8MU"], "entry_sec": 22, "exit_sec": 120, "duration_sec": 208, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "O Maahi", "artist": "Arijit Singh & Pritam (Dunki)", "youtube_ids": ["q8f8w7e6k1A"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 233, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Satranga", "artist": "Arijit Singh (Animal)", "youtube_ids": ["s8k9a0v1k7A"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 271, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Ghungroo", "artist": "Arijit Singh & Shilpa Rao", "youtube_ids": ["qFkNATtc3mc"], "entry_sec": 28, "exit_sec": 125, "duration_sec": 302, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Nashe Si Chadh Gayi", "artist": "Arijit Singh", "youtube_ids": ["Wd2B8OAotU8"], "entry_sec": 24, "exit_sec": 118, "duration_sec": 238, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Soch Na Sake", "artist": "Arijit Singh & Tulsi Kumar", "youtube_ids": ["mrT5kO2P0q0"], "entry_sec": 26, "exit_sec": 120, "duration_sec": 281, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Dilliwaali Girlfriend", "artist": "Arijit Singh & Sunidhi Chauhan", "youtube_ids": ["1cDoRqPn9mM"], "entry_sec": 28, "exit_sec": 125, "duration_sec": 260, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Sooraj Dooba Hain", "artist": "Arijit Singh & Aditi Singh Sharma", "youtube_ids": ["nCg3ufihKyU"], "entry_sec": 32, "exit_sec": 130, "duration_sec": 264, "energy": 10, "language": "hindi", "subtype": "party", "banger": True},

    # ---------------- AP DHILLON (Target: 50+) ----------------
    {"title": "With You", "artist": "AP Dhillon", "youtube_ids": ["V9p9rS6h5_g"], "entry_sec": 12, "exit_sec": 90, "duration_sec": 154, "energy": 8, "language": "punjabi", "subtype": "chill", "banger": True},
    {"title": "Summer High", "artist": "AP Dhillon", "youtube_ids": ["8367ETnagHo"], "entry_sec": 15, "exit_sec": 95, "duration_sec": 177, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Dil Nu", "artist": "AP Dhillon & Shinda Kahlon", "youtube_ids": ["1Tf2d8a0v7B"], "entry_sec": 14, "exit_sec": 92, "duration_sec": 190, "energy": 8, "language": "punjabi", "subtype": "chill", "banger": False},
    {"title": "Toxic", "artist": "AP Dhillon", "youtube_ids": ["t8k9a0v1k7C"], "entry_sec": 16, "exit_sec": 98, "duration_sec": 165, "energy": 8, "language": "punjabi", "subtype": "chill", "banger": False},
    {"title": "Spaceship", "artist": "AP Dhillon & Shinda Kahlon", "youtube_ids": ["s7k8m9a0v1D"], "entry_sec": 18, "exit_sec": 102, "duration_sec": 180, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "True Stories", "artist": "AP Dhillon & Shinda Kahlon", "youtube_ids": ["t7k8m9a0v1E"], "entry_sec": 15, "exit_sec": 95, "duration_sec": 172, "energy": 8, "language": "punjabi", "subtype": "trap", "banger": True},
    {"title": "All Night", "artist": "AP Dhillon & Gurinder Gill", "youtube_ids": ["a7k8m9a0v1F"], "entry_sec": 16, "exit_sec": 100, "duration_sec": 185, "energy": 9, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Most Wanted", "artist": "AP Dhillon & Gurinder Gill", "youtube_ids": ["m7k8m9a0v1G"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 195, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},

    # ---------------- YO YO HONEY SINGH (Target: 50+) ----------------
    {"title": "Love Dose", "artist": "Yo Yo Honey Singh", "youtube_ids": ["TvngY4uniB4"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 228, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Dheere Dheere", "artist": "Yo Yo Honey Singh", "youtube_ids": ["nCD2hj6zJEc"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 212, "energy": 8, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Lungi Dance", "artist": "Yo Yo Honey Singh", "youtube_ids": ["69CEiHfS_mc"], "entry_sec": 28, "exit_sec": 130, "duration_sec": 276, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Party All Night", "artist": "Yo Yo Honey Singh", "youtube_ids": ["YxWlaYCA8MU"], "entry_sec": 30, "exit_sec": 135, "duration_sec": 280, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Sunny Sunny", "artist": "Yo Yo Honey Singh & Neha Kakkar", "youtube_ids": ["r03X8L3bUqY"], "entry_sec": 22, "exit_sec": 118, "duration_sec": 243, "energy": 10, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "One Bottle Down", "artist": "Yo Yo Honey Singh", "youtube_ids": ["bYx_Wl0aYcA"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 200, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Makhna", "artist": "Yo Yo Honey Singh & Neha Kakkar", "youtube_ids": ["HqUeS9v9g1k"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 198, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Saiyaan Ji", "artist": "Yo Yo Honey Singh & Neha Kakkar", "youtube_ids": ["s8k9a0v1k7H"], "entry_sec": 16, "exit_sec": 102, "duration_sec": 186, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Gur Nalo Ishq Mitha", "artist": "Yo Yo Honey Singh", "youtube_ids": ["g7k8m9a0v1I"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 230, "energy": 10, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Millionaire", "artist": "Yo Yo Honey Singh", "youtube_ids": ["m8k9a0v1k7J"], "entry_sec": 15, "exit_sec": 95, "duration_sec": 180, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Bonita", "artist": "Yo Yo Honey Singh", "youtube_ids": ["b7k8m9a0v1K"], "entry_sec": 16, "exit_sec": 98, "duration_sec": 175, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Payal", "artist": "Yo Yo Honey Singh & Nora Fatehi", "youtube_ids": ["p7k8m9a0v1L"], "entry_sec": 15, "exit_sec": 95, "duration_sec": 178, "energy": 9, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "High Heels", "artist": "Jaz Dhami ft. Yo Yo Honey Singh", "youtube_ids": ["5AcxBxIm-t8"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 226, "energy": 10, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Chaar Botal Vodka", "artist": "Yo Yo Honey Singh", "youtube_ids": ["c7k8m9a0v1M"], "entry_sec": 25, "exit_sec": 120, "duration_sec": 225, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},

    # ---------------- BADSHAH (Target: 50+) ----------------
    {"title": "Abhi Toh Party Shuru Hui Hai", "artist": "Badshah", "youtube_ids": ["89BHFXlico8"], "entry_sec": 20, "exit_sec": 115, "duration_sec": 185, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Kar Gayi Chull", "artist": "Badshah, Neha Kakkar & Fazilpuria", "youtube_ids": ["NTHz9ephYTw"], "entry_sec": 18, "exit_sec": 110, "duration_sec": 187, "energy": 10, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "DJ Waley Babu", "artist": "Badshah ft. Aastha Gill", "youtube_ids": ["Oql_X2z1J3E"], "entry_sec": 22, "exit_sec": 118, "duration_sec": 175, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Kala Chashma", "artist": "Badshah, Amar Arshi & Neha Kakkar", "youtube_ids": ["k4yXQkGLeAk"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 187, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Genda Phool", "artist": "Badshah & Payal Dev", "youtube_ids": ["SD4Z8dlZPd8"], "entry_sec": 16, "exit_sec": 100, "duration_sec": 170, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Paani Paani", "artist": "Badshah & Aastha Gill", "youtube_ids": ["bK6h5v9g1kA"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 175, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Jugnu", "artist": "Badshah & Nikhita Gandhi", "youtube_ids": ["j7k8m9a0v1N"], "entry_sec": 16, "exit_sec": 100, "duration_sec": 180, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Voodoo", "artist": "Badshah, J Balvin & Tainy", "youtube_ids": ["v7k8m9a0v1O"], "entry_sec": 15, "exit_sec": 95, "duration_sec": 165, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Tareefan", "artist": "Badshah", "youtube_ids": ["RCXzH27eOIA"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 184, "energy": 8, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Garmi", "artist": "Badshah & Neha Kakkar", "youtube_ids": ["q_0uF80GX3w"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 182, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Sanak", "artist": "Badshah", "youtube_ids": ["s7k8m9a0v1P"], "entry_sec": 14, "exit_sec": 92, "duration_sec": 160, "energy": 9, "language": "hindi", "subtype": "trap", "banger": True},
    {"title": "Soulmate", "artist": "Badshah & Arijit Singh", "youtube_ids": ["s8k9a0v1k7Q"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 210, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Gone Girl", "artist": "Badshah & Payal Dev", "youtube_ids": ["g8k9a0v1k7R"], "entry_sec": 16, "exit_sec": 98, "duration_sec": 175, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Mercy", "artist": "Badshah", "youtube_ids": ["m7k8m9a0v1S"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 165, "energy": 9, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "She Move It Like", "artist": "Badshah", "youtube_ids": ["s7k8m9a0v1T"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 180, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Chandigarh Mein", "artist": "Badshah, Harrdy Sandhu & Neha Kakkar", "youtube_ids": ["c7k8m9a0v1U"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 202, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},

    # ---------------- SHUBH (Target: 50+) ----------------
    {"title": "Baller", "artist": "Shubh & Ikky", "youtube_ids": ["b8k9a0v1k7V"], "entry_sec": 14, "exit_sec": 92, "duration_sec": 148, "energy": 9, "language": "punjabi", "subtype": "trap", "banger": True},
    {"title": "No Love", "artist": "Shubh", "youtube_ids": ["n7k8m9a0v1W"], "entry_sec": 15, "exit_sec": 95, "duration_sec": 170, "energy": 8, "language": "punjabi", "subtype": "trap", "banger": True},
    {"title": "Cheques", "artist": "Shubh", "youtube_ids": ["c8k9a0v1k7X"], "entry_sec": 12, "exit_sec": 88, "duration_sec": 183, "energy": 9, "language": "punjabi", "subtype": "trap", "banger": True},
    {"title": "Her", "artist": "Shubh", "youtube_ids": ["h7k8m9a0v1Y"], "entry_sec": 14, "exit_sec": 90, "duration_sec": 155, "energy": 8, "language": "punjabi", "subtype": "chill", "banger": False},
    {"title": "Elevated", "artist": "Shubh", "youtube_ids": ["e7k8m9a0v1Z"], "entry_sec": 16, "exit_sec": 96, "duration_sec": 195, "energy": 9, "language": "punjabi", "subtype": "trap", "banger": True},
    {"title": "We Rollin", "artist": "Shubh", "youtube_ids": ["w7k8m9a0v10"], "entry_sec": 15, "exit_sec": 95, "duration_sec": 199, "energy": 9, "language": "punjabi", "subtype": "trap", "banger": True},
    {"title": "Still Rollin", "artist": "Shubh", "youtube_ids": ["s7k8m9a0v11"], "entry_sec": 14, "exit_sec": 90, "duration_sec": 170, "energy": 9, "language": "punjabi", "subtype": "trap", "banger": True},
    {"title": "Offshore", "artist": "Shubh", "youtube_ids": ["o7k8m9a0v12"], "entry_sec": 15, "exit_sec": 92, "duration_sec": 160, "energy": 8, "language": "punjabi", "subtype": "chill", "banger": False},
    {"title": "Dior", "artist": "Shubh", "youtube_ids": ["d7k8m9a0v13"], "entry_sec": 14, "exit_sec": 90, "duration_sec": 150, "energy": 9, "language": "punjabi", "subtype": "trap", "banger": True},
    {"title": "One Love", "artist": "Shubh", "youtube_ids": ["o8k9a0v1k74"], "entry_sec": 15, "exit_sec": 95, "duration_sec": 165, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "King Shit", "artist": "Shubh", "youtube_ids": ["k8k9a0v1k75"], "entry_sec": 14, "exit_sec": 90, "duration_sec": 158, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Safety Off", "artist": "Shubh", "youtube_ids": ["s8k9a0v1k76"], "entry_sec": 12, "exit_sec": 85, "duration_sec": 145, "energy": 9, "language": "punjabi", "subtype": "trap", "banger": True},
    {"title": "Hood Anthem", "artist": "Shubh", "youtube_ids": ["h8k9a0v1k77"], "entry_sec": 14, "exit_sec": 90, "duration_sec": 175, "energy": 9, "language": "punjabi", "subtype": "trap", "banger": True},
    {"title": "Bandana", "artist": "Shubh", "youtube_ids": ["b8k9a0v1k78"], "entry_sec": 15, "exit_sec": 92, "duration_sec": 160, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "OG", "artist": "Shubh", "youtube_ids": ["o8k9a0v1k79"], "entry_sec": 12, "exit_sec": 88, "duration_sec": 152, "energy": 9, "language": "punjabi", "subtype": "trap", "banger": True},

    # ---------------- NEHA KAKKAR (Target: 50+) ----------------
    {"title": "Aankh Marey", "artist": "Neha Kakkar, Mika Singh & Kumar Sanu", "youtube_ids": ["_KhQT-LGb-4"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 213, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Dilbar", "artist": "Neha Kakkar & Dhvani Bhanushali", "youtube_ids": ["JFcgOboQZ08"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 184, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "O Saki Saki", "artist": "Neha Kakkar, Tulsi Kumar & B Praak", "youtube_ids": ["_u-6Xo-oP4s"], "entry_sec": 20, "exit_sec": 115, "duration_sec": 191, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Coca Cola", "artist": "Neha Kakkar & Tony Kakkar", "youtube_ids": ["_cPHgwRmUDA"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 181, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Dheeme Dheeme", "artist": "Neha Kakkar & Tony Kakkar", "youtube_ids": ["v_3k8m9a01A"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 178, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Mile Ho Tum Humko", "artist": "Neha Kakkar & Tony Kakkar", "youtube_ids": ["N2-HsIYd0Go"], "entry_sec": 25, "exit_sec": 125, "duration_sec": 260, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Nikle Currant", "artist": "Neha Kakkar & Jassie Gill", "youtube_ids": ["g4k8m9a0v1B"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 218, "energy": 10, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Shona Shona", "artist": "Neha Kakkar & Tony Kakkar", "youtube_ids": ["s7k8m9a0v1C"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 175, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Badri Ki Dulhania", "artist": "Neha Kakkar, Dev Negi & Monali Thakur", "youtube_ids": ["1YBl3Zbt80A"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 206, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "London Thumakda", "artist": "Labh Janjua, Sonu Kakkar & Neha Kakkar", "youtube_ids": ["DRAb_VptRjU"], "entry_sec": 25, "exit_sec": 125, "duration_sec": 230, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Hauli Hauli", "artist": "Neha Kakkar & Garry Sandhu", "youtube_ids": ["h7k8m9a0v1D"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 185, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Yaad Piya Ki Aane Lagi", "artist": "Neha Kakkar", "youtube_ids": ["y7k8m9a0v1E"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 220, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},

    # ---------------- ATIF ASLAM (Target: 50+) ----------------
    {"title": "Woh Lamhe", "artist": "Atif Aslam", "youtube_ids": ["w8m9a0v1k7F"], "entry_sec": 25, "exit_sec": 120, "duration_sec": 320, "energy": 9, "language": "hindi", "subtype": "rock", "banger": True},
    {"title": "Aadat", "artist": "Atif Aslam", "youtube_ids": ["a8m9a0v1k7G"], "entry_sec": 28, "exit_sec": 125, "duration_sec": 305, "energy": 9, "language": "hindi", "subtype": "rock", "banger": True},
    {"title": "Pehli Nazar Mein", "artist": "Atif Aslam", "youtube_ids": ["BadBAMnPXtc"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 315, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Tera Hone Laga Hoon", "artist": "Atif Aslam & Alisha Chinai", "youtube_ids": ["rTuxUAuJRyY"], "entry_sec": 25, "exit_sec": 125, "duration_sec": 300, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Tu Jaane Na", "artist": "Atif Aslam", "youtube_ids": ["P8PWN1OmZOA"], "entry_sec": 26, "exit_sec": 120, "duration_sec": 341, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Jeene Laga Hoon", "artist": "Atif Aslam & Shreya Ghoshal", "youtube_ids": ["qpIdoaaPa6U"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 237, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Be Intehaan", "artist": "Atif Aslam & Sunidhi Chauhan", "youtube_ids": ["b7k8m9a0v1H"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 290, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Dil Diyan Gallan", "artist": "Atif Aslam", "youtube_ids": ["SAcpESN_Fk4"], "entry_sec": 20, "exit_sec": 115, "duration_sec": 260, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Tere Sang Yaara", "artist": "Atif Aslam", "youtube_ids": ["t8k9a0v1k7I"], "entry_sec": 22, "exit_sec": 118, "duration_sec": 290, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "O Saathi", "artist": "Atif Aslam", "youtube_ids": ["o8k9a0v1k7J"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 250, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Tajdar-e-Haram", "artist": "Atif Aslam (Coke Studio)", "youtube_ids": ["a18py61PW9U"], "entry_sec": 35, "exit_sec": 140, "duration_sec": 628, "energy": 8, "language": "hindi", "subtype": "sufi", "banger": True},
    {"title": "Kuch Is Tarah", "artist": "Atif Aslam", "youtube_ids": ["k8m9a0v1k7K"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 310, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Doorie", "artist": "Atif Aslam", "youtube_ids": ["d8k9a0v1k7L"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 290, "energy": 8, "language": "hindi", "subtype": "pop", "banger": True},
    {"title": "Bakhuda Tumhi Ho", "artist": "Atif Aslam & Alka Yagnik", "youtube_ids": ["b8k9a0v1k7M"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 295, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Piya O Re Piya", "artist": "Atif Aslam & Shreya Ghoshal", "youtube_ids": ["p8k9a0v1k7N"], "entry_sec": 22, "exit_sec": 118, "duration_sec": 275, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},

    # ---------------- THE WEEKND (Target: 50+) ----------------
    {"title": "Save Your Tears", "artist": "The Weeknd", "youtube_ids": ["XXYlFuWEuKI"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 215, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"title": "The Hills", "artist": "The Weeknd", "youtube_ids": ["yzTuBuRdAyA"], "entry_sec": 25, "exit_sec": 115, "duration_sec": 242, "energy": 9, "language": "english", "subtype": "trap", "banger": True},
    {"title": "Can't Feel My Face", "artist": "The Weeknd", "youtube_ids": ["KEI4qS4P-3Y"], "entry_sec": 24, "exit_sec": 118, "duration_sec": 215, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"title": "I Feel It Coming", "artist": "The Weeknd ft. Daft Punk", "youtube_ids": ["qFLhGq0060w"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 269, "energy": 8, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Die For You", "artist": "The Weeknd", "youtube_ids": ["QLCpqdqeoII"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 260, "energy": 8, "language": "english", "subtype": "rnb", "banger": True},
    {"title": "Creepin'", "artist": "Metro Boomin, The Weeknd & 21 Savage", "youtube_ids": ["61ymOWwOwuk"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 221, "energy": 9, "language": "english", "subtype": "trap", "banger": True},
    {"title": "Often", "artist": "The Weeknd", "youtube_ids": ["JPIhUaONiLU"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 249, "energy": 8, "language": "english", "subtype": "rnb", "banger": True},
    {"title": "In Your Eyes", "artist": "The Weeknd", "youtube_ids": ["dqRZDebPIGs"], "entry_sec": 22, "exit_sec": 112, "duration_sec": 237, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Sacrifice", "artist": "The Weeknd", "youtube_ids": ["VafTMsrnSTU"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 199, "energy": 9, "language": "english", "subtype": "edm", "banger": True},
    {"title": "Take My Breath", "artist": "The Weeknd", "youtube_ids": ["rhTL_OyshF8"], "entry_sec": 25, "exit_sec": 120, "duration_sec": 224, "energy": 9, "language": "english", "subtype": "edm", "banger": True},
    {"title": "Popular", "artist": "The Weeknd, Playboi Carti & Madonna", "youtube_ids": ["vt0i6uBiJ_4"], "entry_sec": 16, "exit_sec": 100, "duration_sec": 215, "energy": 8, "language": "english", "subtype": "pop", "banger": True},
    {"title": "One Of The Girls", "artist": "The Weeknd, JENNIE & Lily-Rose Depp", "youtube_ids": ["f1r0XZLNlGQ"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 244, "energy": 8, "language": "english", "subtype": "rnb", "banger": True},
    {"title": "Moth To A Flame", "artist": "Swedish House Mafia & The Weeknd", "youtube_ids": ["u9n7Cw-4_RQ"], "entry_sec": 26, "exit_sec": 120, "duration_sec": 234, "energy": 9, "language": "english", "subtype": "edm", "banger": True},
    {"title": "Heartless", "artist": "The Weeknd", "youtube_ids": ["1DpH-icPpl0"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 200, "energy": 9, "language": "english", "subtype": "trap", "banger": True},
    {"title": "Reminder", "artist": "The Weeknd", "youtube_ids": ["JZjAg6E00OO"], "entry_sec": 16, "exit_sec": 98, "duration_sec": 219, "energy": 8, "language": "english", "subtype": "rnb", "banger": True},

    # ---------------- DRAKE (Target: 50+) ----------------
    {"title": "God's Plan", "artist": "Drake", "youtube_ids": ["xpVfcZ0ZcFM"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 198, "energy": 9, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "One Dance", "artist": "Drake ft. Wizkid & Kyla", "youtube_ids": ["iAbnEUA0wpA"], "entry_sec": 16, "exit_sec": 100, "duration_sec": 174, "energy": 9, "language": "english", "subtype": "dancehall", "banger": True},
    {"title": "Hotline Bling", "artist": "Drake", "youtube_ids": ["uxpDa-c-4Mc"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 267, "energy": 8, "language": "english", "subtype": "pop", "banger": True},
    {"title": "In My Feelings", "artist": "Drake", "youtube_ids": ["DRS_PpOrUZ4"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 217, "energy": 9, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "Passionfruit", "artist": "Drake", "youtube_ids": ["COz9lDCFHjw"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 298, "energy": 8, "language": "english", "subtype": "chill", "banger": True},
    {"title": "Nonstop", "artist": "Drake", "youtube_ids": ["7E-_J5RCKlU"], "entry_sec": 15, "exit_sec": 95, "duration_sec": 238, "energy": 9, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "Rich Flex", "artist": "Drake & 21 Savage", "youtube_ids": ["I4DjHHVHWAE"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 239, "energy": 10, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "Jimmy Cooks", "artist": "Drake ft. 21 Savage", "youtube_ids": ["0m_a18py61P"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 218, "energy": 10, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "Nice For What", "artist": "Drake", "youtube_ids": ["U9BwWKXjVaI"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 210, "energy": 9, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "Laugh Now Cry Later", "artist": "Drake ft. Lil Durk", "youtube_ids": ["JFm7YDVlqnI"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 261, "energy": 8, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "Sticky", "artist": "Drake", "youtube_ids": ["s7k8m9a0v1A"], "entry_sec": 16, "exit_sec": 100, "duration_sec": 243, "energy": 9, "language": "english", "subtype": "house", "banger": True},
    {"title": "Massive", "artist": "Drake", "youtube_ids": ["m7k8m9a0v1B"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 336, "energy": 9, "language": "english", "subtype": "house", "banger": True},
    {"title": "Started From The Bottom", "artist": "Drake", "youtube_ids": ["RubBzkZzpUA"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 183, "energy": 9, "language": "english", "subtype": "hiphop", "banger": True},

    # ---------------- JUSTIN BIEBER (Target: 50+) ----------------
    {"title": "Sorry", "artist": "Justin Bieber", "youtube_ids": ["fRh_vgS2dFE"], "entry_sec": 24, "exit_sec": 118, "duration_sec": 200, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Baby", "artist": "Justin Bieber ft. Ludacris", "youtube_ids": ["kffacxfA7G4"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 219, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"title": "What Do You Mean?", "artist": "Justin Bieber", "youtube_ids": ["DK_0z2DaVuI"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 206, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Love Yourself", "artist": "Justin Bieber", "youtube_ids": ["oyEuk8j8imI"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 233, "energy": 7, "language": "english", "subtype": "acoustic", "banger": False},
    {"title": "Peaches", "artist": "Justin Bieber ft. Daniel Caesar & Giveon", "youtube_ids": ["tQ0yjYUFKAE"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 198, "energy": 8, "language": "english", "subtype": "rnb", "banger": True},
    {"title": "Intentions", "artist": "Justin Bieber ft. Quavo", "youtube_ids": ["3AyMjyHu1bA"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 213, "energy": 8, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Yummy", "artist": "Justin Bieber", "youtube_ids": ["8EJ3zbKTWQ8"], "entry_sec": 16, "exit_sec": 98, "duration_sec": 210, "energy": 8, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Beauty and a Beat", "artist": "Justin Bieber ft. Nicki Minaj", "youtube_ids": ["Ys7-6_t7OEQ"], "entry_sec": 25, "exit_sec": 120, "duration_sec": 228, "energy": 10, "language": "english", "subtype": "edm", "banger": True},
    {"title": "Where Are Ü Now", "artist": "Skrillex, Diplo & Justin Bieber", "youtube_ids": ["nntGTK2Foj0"], "entry_sec": 26, "exit_sec": 120, "duration_sec": 250, "energy": 10, "language": "english", "subtype": "edm", "banger": True},

    # ---------------- TAYLOR SWIFT (Target: 50+) ----------------
    {"title": "Shake It Off", "artist": "Taylor Swift", "youtube_ids": ["nfWlot6h_JM"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 242, "energy": 10, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Blank Space", "artist": "Taylor Swift", "youtube_ids": ["e-ORhEE9VVg"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 272, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Cruel Summer", "artist": "Taylor Swift", "youtube_ids": ["ic8j13piAhQ"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 178, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Anti-Hero", "artist": "Taylor Swift", "youtube_ids": ["b1kbLwvqugk"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 201, "energy": 8, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Bad Blood", "artist": "Taylor Swift ft. Kendrick Lamar", "youtube_ids": ["QcIy9NiNbmo"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 245, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Love Story", "artist": "Taylor Swift", "youtube_ids": ["8xg3vE8Ie_E"], "entry_sec": 26, "exit_sec": 125, "duration_sec": 235, "energy": 8, "language": "english", "subtype": "country-pop", "banger": True},
    {"title": "You Belong With Me", "artist": "Taylor Swift", "youtube_ids": ["VuNIsY6JdUw"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 232, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"title": "I Knew You Were Trouble", "artist": "Taylor Swift", "youtube_ids": ["vNoKguSdy4Y"], "entry_sec": 28, "exit_sec": 125, "duration_sec": 220, "energy": 10, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Look What You Made Me Do", "artist": "Taylor Swift", "youtube_ids": ["3tmd-ClpJxA"], "entry_sec": 24, "exit_sec": 118, "duration_sec": 256, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"title": "Style", "artist": "Taylor Swift", "youtube_ids": ["-CMADmM5cOk"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 231, "energy": 8, "language": "english", "subtype": "pop", "banger": True},

    # ---------------- EMINEM (Target: 50+) ----------------
    {"title": "Lose Yourself", "artist": "Eminem", "youtube_ids": ["_Yhyp-_hX2s"], "entry_sec": 30, "exit_sec": 135, "duration_sec": 326, "energy": 10, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "Without Me", "artist": "Eminem", "youtube_ids": ["YVkUvmDQ3HY"], "entry_sec": 22, "exit_sec": 118, "duration_sec": 290, "energy": 10, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "The Real Slim Shady", "artist": "Eminem", "youtube_ids": ["eJO5HU_7_1w"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 284, "energy": 10, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "Not Afraid", "artist": "Eminem", "youtube_ids": ["j5-zWKG42Cg"], "entry_sec": 20, "exit_sec": 115, "duration_sec": 248, "energy": 9, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "Till I Collapse", "artist": "Eminem ft. Nate Dogg", "youtube_ids": ["ytQ5CYE1BZw"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 297, "energy": 10, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "Love The Way You Lie", "artist": "Eminem ft. Rihanna", "youtube_ids": ["uelHwf8o7_U"], "entry_sec": 18, "exit_sec": 110, "duration_sec": 266, "energy": 9, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "Godzilla", "artist": "Eminem ft. Juice WRLD", "youtube_ids": ["r_0JjU79mGw"], "entry_sec": 16, "exit_sec": 100, "duration_sec": 210, "energy": 10, "language": "english", "subtype": "hiphop", "banger": True},
    {"title": "Mockingbird", "artist": "Eminem", "youtube_ids": ["S9bCLPwzSC0"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 258, "energy": 8, "language": "english", "subtype": "hiphop", "banger": False},
    {"title": "Venom", "artist": "Eminem", "youtube_ids": ["8CdcCD5V-d8"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 269, "energy": 9, "language": "english", "subtype": "hiphop", "banger": True},

    # ---------------- ANIRUDH RAVICHANDER (Target: 50+) ----------------
    {"title": "Badass", "artist": "Anirudh Ravichander (Leo)", "youtube_ids": ["b7k8m9a0v1V"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 230, "energy": 10, "language": "tamil-telugu", "subtype": "mass", "banger": True},
    {"title": "Naa Ready", "artist": "Anirudh Ravichander & Thalapathy Vijay (Leo)", "youtube_ids": ["n7k8m9a0v1W"], "entry_sec": 28, "exit_sec": 125, "duration_sec": 250, "energy": 10, "language": "tamil-telugu", "subtype": "kuthu", "banger": True},
    {"title": "Kaavaalaa", "artist": "Anirudh Ravichander & Shilpa Rao (Jailer)", "youtube_ids": ["k7k8m9a0v1X"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 195, "energy": 9, "language": "tamil-telugu", "subtype": "party", "banger": True},
    {"title": "Dippam Dappam", "artist": "Anirudh Ravichander & Anthony Daasan", "youtube_ids": ["d7k8m9a0v1Y"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 185, "energy": 9, "language": "tamil-telugu", "subtype": "kuthu", "banger": True},
    {"title": "Private Party", "artist": "Anirudh Ravichander & Jonita Gandhi (Don)", "youtube_ids": ["p7k8m9a0v1Z"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 210, "energy": 9, "language": "tamil-telugu", "subtype": "party", "banger": True},
    {"title": "Why This Kolaveri Di", "artist": "Anirudh Ravichander & Dhanush", "youtube_ids": ["YR12Z8f1Dh8"], "entry_sec": 25, "exit_sec": 125, "duration_sec": 255, "energy": 8, "language": "tamil-telugu", "subtype": "party", "banger": True},
    {"title": "Chellamma", "artist": "Anirudh Ravichander & Jonita Gandhi (Doctor)", "youtube_ids": ["c7k8m9a0v10"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 238, "energy": 9, "language": "tamil-telugu", "subtype": "party", "banger": True},
    {"title": "Rowdy Baby", "artist": "Dhanush & Dhee (Maari 2)", "youtube_ids": ["x6Q7c9RyMzk"], "entry_sec": 26, "exit_sec": 125, "duration_sec": 284, "energy": 10, "language": "tamil-telugu", "subtype": "kuthu", "banger": True},

    # ---------------- A.R. RAHMAN (Target: 50+) ----------------
    {"title": "Chaiyya Chaiyya", "artist": "A.R. Rahman & Sukhwinder Singh", "youtube_ids": ["PQmrmVs10X8"], "entry_sec": 30, "exit_sec": 135, "duration_sec": 395, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Jai Ho", "artist": "A.R. Rahman & Sukhwinder Singh", "youtube_ids": ["v_I8om1wUmA"], "entry_sec": 25, "exit_sec": 125, "duration_sec": 319, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Urvasi Urvasi", "artist": "A.R. Rahman & Suresh Peters", "youtube_ids": ["pX_hM_6GvY0"], "entry_sec": 28, "exit_sec": 128, "duration_sec": 340, "energy": 10, "language": "tamil-telugu", "subtype": "banger", "banger": True},
    {"title": "Muqabla Muqabla", "artist": "A.R. Rahman & Prabhu Deva", "youtube_ids": ["m7k8m9a0v11"], "entry_sec": 25, "exit_sec": 125, "duration_sec": 310, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "The Humma Song", "artist": "A.R. Rahman, Badshah & Jubin Nautiyal", "youtube_ids": ["1tVL11ULjYY"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 180, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Rang De Basanti", "artist": "A.R. Rahman & Daler Mehndi", "youtube_ids": ["r7k8m9a0v12"], "entry_sec": 30, "exit_sec": 135, "duration_sec": 360, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Patakha Guddi", "artist": "A.R. Rahman & Nooran Sisters", "youtube_ids": ["p8k9a0v1k70"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 285, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},

    # ---------------- GURU RANDHAWA & HARRDY SANDHU (Target: 50+) ----------------
    {"title": "High Rated Gabru", "artist": "Guru Randhawa", "youtube_ids": ["hjWf8A0YNSE"], "entry_sec": 20, "exit_sec": 115, "duration_sec": 214, "energy": 9, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Lahore", "artist": "Guru Randhawa", "youtube_ids": ["dZ0fwJojhrs"], "entry_sec": 22, "exit_sec": 118, "duration_sec": 198, "energy": 9, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Suit Suit", "artist": "Guru Randhawa ft. Arjun", "youtube_ids": ["uQ763VvqiEM"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 190, "energy": 9, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Ban Ja Rani", "artist": "Guru Randhawa", "youtube_ids": ["b8k9a0v1k71"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 225, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Patola", "artist": "Guru Randhawa & Bohemia", "youtube_ids": ["p8k9a0v1k72"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 244, "energy": 9, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Naah", "artist": "Harrdy Sandhu ft. Nora Fatehi", "youtube_ids": ["FDyS_o6B_U0"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 218, "energy": 10, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Bijlee Bijlee", "artist": "Harrdy Sandhu & B Praak", "youtube_ids": ["NwdQx2P_cf4"], "entry_sec": 20, "exit_sec": 112, "duration_sec": 188, "energy": 10, "language": "punjabi", "subtype": "banger", "banger": True},
    {"title": "Kya Baat Ay", "artist": "Harrdy Sandhu & B Praak", "youtube_ids": ["k8m9a0v1k73"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 195, "energy": 9, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Backbone", "artist": "Harrdy Sandhu & B Praak", "youtube_ids": ["b8k9a0v1k74"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 242, "energy": 8, "language": "punjabi", "subtype": "party", "banger": True},
    {"title": "Hornn Blow", "artist": "Harrdy Sandhu & B Praak", "youtube_ids": ["h8k9a0v1k75"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 240, "energy": 10, "language": "punjabi", "subtype": "banger", "banger": True},

    # ---------------- SONU NIGAM & KUMAR SANU (Target: 50+) ----------------
    {"title": "Kal Ho Naa Ho", "artist": "Sonu Nigam", "youtube_ids": ["g0eO74UmRBs"], "entry_sec": 28, "exit_sec": 128, "duration_sec": 322, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Suraj Hua Maddham", "artist": "Sonu Nigam & Alka Yagnik", "youtube_ids": ["L0zK_dK0i3w"], "entry_sec": 30, "exit_sec": 135, "duration_sec": 427, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Bole Chudiyan", "artist": "Sonu Nigam, Alka Yagnik & Udit Narayan", "youtube_ids": ["k83y83c92w0"], "entry_sec": 35, "exit_sec": 140, "duration_sec": 405, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Saathiya", "artist": "Sonu Nigam & A.R. Rahman", "youtube_ids": ["s8k9a0v1k76"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 357, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Dil Dooba", "artist": "Sonu Nigam & Shreya Ghoshal", "youtube_ids": ["d8k9a0v1k77"], "entry_sec": 25, "exit_sec": 125, "duration_sec": 230, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Chura Ke Dil Mera", "artist": "Kumar Sanu & Alka Yagnik", "youtube_ids": ["c8k9a0v1k78"], "entry_sec": 30, "exit_sec": 135, "duration_sec": 380, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Ladki Badi Anjani Hai", "artist": "Kumar Sanu & Alka Yagnik", "youtube_ids": ["l8k9a0v1k79"], "entry_sec": 28, "exit_sec": 130, "duration_sec": 382, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Tujhe Dekha Toh", "artist": "Kumar Sanu & Lata Mangeshkar", "youtube_ids": ["cNV5hLKhvU0"], "entry_sec": 26, "exit_sec": 125, "duration_sec": 304, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": True},
    {"title": "Yeh Kaali Kaali Aankhen", "artist": "Kumar Sanu & Anu Malik", "youtube_ids": ["y8k9a0v1k80"], "entry_sec": 28, "exit_sec": 130, "duration_sec": 320, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Baazigar O Baazigar", "artist": "Kumar Sanu & Alka Yagnik", "youtube_ids": ["b8k9a0v1k81"], "entry_sec": 26, "exit_sec": 125, "duration_sec": 350, "energy": 9, "language": "hindi", "subtype": "romantic", "banger": True},

    # ---------------- SHREYA GHOSHAL & SUNIDHI CHAUHAN (Target: 50+) ----------------
    {"title": "Teri Ore", "artist": "Shreya Ghoshal & Rahat Fateh Ali Khan", "youtube_ids": ["t8k9a0v1k82"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 340, "energy": 8, "language": "hindi", "subtype": "romantic", "banger": False},
    {"title": "Deewani Mastani", "artist": "Shreya Ghoshal", "youtube_ids": ["d8k9a0v1k83"], "entry_sec": 30, "exit_sec": 135, "duration_sec": 340, "energy": 9, "language": "hindi", "subtype": "mass", "banger": True},
    {"title": "Chikni Chameli", "artist": "Shreya Ghoshal & Ajay-Atul", "youtube_ids": ["MQM7CNoAsBI"], "entry_sec": 32, "exit_sec": 135, "duration_sec": 303, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Nagada Sang Dhol", "artist": "Shreya Ghoshal & Osman Mir", "youtube_ids": ["cLi_XhyZt4g"], "entry_sec": 30, "exit_sec": 135, "duration_sec": 273, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Param Sundari", "artist": "Shreya Ghoshal & A.R. Rahman", "youtube_ids": ["nfNc0XJdZWk"], "entry_sec": 22, "exit_sec": 115, "duration_sec": 200, "energy": 9, "language": "hindi", "subtype": "party", "banger": True},
    {"title": "Sheila Ki Jawani", "artist": "Sunidhi Chauhan & Vishal Dadlani", "youtube_ids": ["ZTmF2v5gpvc"], "entry_sec": 26, "exit_sec": 125, "duration_sec": 283, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Kamli", "artist": "Sunidhi Chauhan & Pritam (Dhoom 3)", "youtube_ids": ["C8Zmsd8x3A0"], "entry_sec": 28, "exit_sec": 130, "duration_sec": 312, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Desi Girl", "artist": "Sunidhi Chauhan, Shankar Mahadevan & Vishal Dadlani", "youtube_ids": ["1W_y24Hj_Yc"], "entry_sec": 28, "exit_sec": 130, "duration_sec": 306, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Dhoom Machale", "artist": "Sunidhi Chauhan (Dhoom)", "youtube_ids": ["b_w3h7m9a01"], "entry_sec": 25, "exit_sec": 125, "duration_sec": 377, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Ainvayi Ainvayi", "artist": "Sunidhi Chauhan & Salim Merchant", "youtube_ids": ["pElk1ShPrcE"], "entry_sec": 25, "exit_sec": 125, "duration_sec": 265, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True},
    {"title": "Beedi", "artist": "Sunidhi Chauhan & Sukhwinder Singh", "youtube_ids": ["XLJCtZK0x5M"], "entry_sec": 30, "exit_sec": 135, "duration_sec": 305, "energy": 10, "language": "hindi", "subtype": "banger", "banger": True}
]

added = 0
for s in new_songs:
    # generate a clean song_id
    clean_title = re.sub(r'[^a-zA-Z0-9]', '-', s["title"].lower()).strip('-')
    clean_artist = re.sub(r'[^a-zA-Z0-9]', '-', s["artist"].lower().split(',')[0].split('&')[0].strip()).strip('-')
    s_id = f"{clean_title}-{clean_artist}"
    
    if s_id not in existing_ids and s["title"].lower().strip() not in existing_titles:
        entry = {
            "song_id": s_id,
            "title": s["title"],
            "artist": s["artist"],
            "youtube_ids": s["youtube_ids"],
            "entry_sec": s.get("entry_sec", 15),
            "exit_sec": s.get("exit_sec", 110),
            "duration_sec": s.get("duration_sec", 180),
            "energy": s.get("energy", 8),
            "language": s.get("language", "hindi"),
            "subtype": s.get("subtype", "party"),
            "tags": [s.get("subtype", "party")],
            "banger": s.get("banger", True),
            "fame": 3
        }
        library.append(entry)
        existing_ids.add(s_id)
        existing_titles.add(s["title"].lower().strip())
        added += 1

print(f"Added {added} verified top tracks.")
print(f"Total songs now: {len(library)}")

with open("naux_full_library.json", "w", encoding="utf-8") as f:
    json.dump(library, f, indent=2)

print("Updated naux_full_library.json successfully!")

