import json
import os

with open("naux_full_library.json", "r", encoding="utf-8") as f:
    library = json.load(f)

print(f"Current library size: {len(library)}")

# Additional global hits across all languages and artists
global_hits = [
    # English / Global Bangers
    {"song_id": "blinding-lights-weeknd", "title": "Blinding Lights", "artist": "The Weeknd", "youtube_ids": ["4NRXx6U8ABQ"], "entry_sec": 24, "exit_sec": 120, "duration_sec": 200, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"song_id": "uptown-funk-bruno-mars", "title": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "youtube_ids": ["OPf0YbXqDm0"], "entry_sec": 48, "exit_sec": 150, "duration_sec": 270, "energy": 10, "language": "english", "subtype": "pop", "banger": True},
    {"song_id": "levitating-dua-lipa", "title": "Levitating", "artist": "Dua Lipa", "youtube_ids": ["TUVcZfQe-Kw"], "entry_sec": 19, "exit_sec": 110, "duration_sec": 203, "energy": 9, "language": "english", "subtype": "pop", "banger": True},
    {"song_id": "give-me-everything-pitbull", "title": "Give Me Everything", "artist": "Pitbull ft. Ne-Yo, Afrojack", "youtube_ids": ["EPo5wWmKEaI"], "entry_sec": 38, "exit_sec": 140, "duration_sec": 266, "energy": 9, "language": "english", "subtype": "edm", "banger": True},
    {"song_id": "wake-me-up-avicii", "title": "Wake Me Up", "artist": "Avicii", "youtube_ids": ["IcrbM1l_BoI"], "entry_sec": 32, "exit_sec": 130, "duration_sec": 253, "energy": 9, "language": "english", "subtype": "edm", "banger": True},
    {"song_id": "titanium-david-guetta", "title": "Titanium", "artist": "David Guetta ft. Sia", "youtube_ids": ["JRfuAukYTKg"], "entry_sec": 39, "exit_sec": 125, "duration_sec": 245, "energy": 9, "language": "english", "subtype": "edm", "banger": True},
    {"song_id": "party-rock-anthem-lmfao", "title": "Party Rock Anthem", "artist": "LMFAO", "youtube_ids": ["KQ6zr6kCPj8"], "entry_sec": 57, "exit_sec": 145, "duration_sec": 278, "energy": 10, "language": "english", "subtype": "edm", "banger": True},
    {"song_id": "cant-hold-us-macklemore", "title": "Can't Hold Us", "artist": "Macklemore & Ryan Lewis", "youtube_ids": ["2zNSgSzhBf8"], "entry_sec": 18, "exit_sec": 115, "duration_sec": 258, "energy": 10, "language": "english", "subtype": "hiphop", "banger": True},
    {"song_id": "starboy-the-weeknd", "title": "Starboy", "artist": "The Weeknd ft. Daft Punk", "youtube_ids": ["34Na4j8AVgA"], "entry_sec": 28, "exit_sec": 110, "duration_sec": 230, "energy": 8, "language": "english", "subtype": "pop", "banger": True},
    {"song_id": "summer-calvin-harris", "title": "Summer", "artist": "Calvin Harris", "youtube_ids": ["ebXbLfLACGM"], "entry_sec": 32, "exit_sec": 118, "duration_sec": 214, "energy": 9, "language": "english", "subtype": "edm", "banger": True},
    {"song_id": "shape-of-you-ed-sheeran", "title": "Shape of You", "artist": "Ed Sheeran", "youtube_ids": ["JGwWNGJdvx8"], "entry_sec": 21, "exit_sec": 112, "duration_sec": 233, "energy": 8, "language": "english", "subtype": "pop", "banger": True},
    {"song_id": "stay-kid-laroi", "title": "Stay", "artist": "The Kid LAROI & Justin Bieber", "youtube_ids": ["kTJczUoc26U"], "entry_sec": 13, "exit_sec": 95, "duration_sec": 138, "energy": 9, "language": "english", "subtype": "pop", "banger": True},

    # Latin / Spanish Bangers
    {"song_id": "danza-kuduro-don-omar", "title": "Danza Kuduro", "artist": "Don Omar ft. Lucenzo", "youtube_ids": ["7zp1TbLFPp8"], "entry_sec": 23, "exit_sec": 125, "duration_sec": 199, "energy": 10, "language": "latin", "subtype": "party", "banger": True},
    {"song_id": "gasolina-daddy-yankee", "title": "Gasolina", "artist": "Daddy Yankee", "youtube_ids": ["CCF1_jI8Prk"], "entry_sec": 22, "exit_sec": 110, "duration_sec": 193, "energy": 10, "language": "latin", "subtype": "party", "banger": True},
    {"song_id": "despacito-luis-fonsi", "title": "Despacito", "artist": "Luis Fonsi ft. Daddy Yankee", "youtube_ids": ["kJQP7kiw5Fk"], "entry_sec": 33, "exit_sec": 130, "duration_sec": 242, "energy": 9, "language": "latin", "subtype": "party", "banger": True},
    {"song_id": "mi-gente-j-balvin", "title": "Mi Gente", "artist": "J Balvin, Willy William", "youtube_ids": ["wnJ6LuUFpMo"], "entry_sec": 15, "exit_sec": 105, "duration_sec": 185, "energy": 9, "language": "latin", "subtype": "party", "banger": True},

    # South Indian / Tamil / Telugu / Malayalam
    {"song_id": "illuminati-sushin-shyam", "title": "Illuminati", "artist": "Sushin Shyam & Dabzee (Aavesham)", "youtube_ids": ["tOM-nWPcR4U"], "entry_sec": 26, "exit_sec": 118, "duration_sec": 193, "energy": 10, "language": "tamil-telugu", "subtype": "mass", "banger": True},
    {"song_id": "naatu-naatu-rrr", "title": "Naatu Naatu", "artist": "Rahul Sipligunj, Kaala Bhairava (RRR)", "youtube_ids": ["OsU0CGZoV8E"], "entry_sec": 38, "exit_sec": 135, "duration_sec": 275, "energy": 10, "language": "tamil-telugu", "subtype": "mass", "banger": True},
    {"song_id": "hukum-anirudh", "title": "Hukum - Thalaivar Alappara", "artist": "Anirudh Ravichander (Jailer)", "youtube_ids": ["1F3hm6MfR1k"], "entry_sec": 42, "exit_sec": 130, "duration_sec": 207, "energy": 10, "language": "tamil-telugu", "subtype": "mass", "banger": True},
    {"song_id": "vaathi-coming-anirudh", "title": "Vaathi Coming", "artist": "Anirudh Ravichander (Master)", "youtube_ids": ["fRD_3vJagxk"], "entry_sec": 32, "exit_sec": 120, "duration_sec": 230, "energy": 10, "language": "tamil-telugu", "subtype": "kuthu", "banger": True},
    {"song_id": "oo-antava-dsp", "title": "Oo Antava Mava", "artist": "Devi Sri Prasad & Indravathi Chauhan (Pushpa)", "youtube_ids": ["VswF464q3Zk"], "entry_sec": 18, "exit_sec": 105, "duration_sec": 224, "energy": 9, "language": "tamil-telugu", "subtype": "mass", "banger": True},
    {"song_id": "arabic-kuthu-anirudh", "title": "Arabic Kuthu - Halamithi Habibo", "artist": "Anirudh Ravichander & Jonita Gandhi (Beast)", "youtube_ids": ["KUN5Uf9mObQ"], "entry_sec": 28, "exit_sec": 125, "duration_sec": 279, "energy": 9, "language": "tamil-telugu", "subtype": "kuthu", "banger": True},
    {"song_id": "butta-bomma-arman-malik", "title": "Butta Bomma", "artist": "Armaan Malik & Thaman S (Ala Vaikunthapurramuloo)", "youtube_ids": ["2mDCVzruYzQ"], "entry_sec": 16, "exit_sec": 98, "duration_sec": 198, "energy": 8, "language": "tamil-telugu", "subtype": "melody", "banger": True},

    # Desi / Haryanvi / Bhojpuri
    {"song_id": "52-gaj-ka-daman-renuka", "title": "52 GAJ KA DAMAN", "artist": "Renuka Panwar & Aman Jaji", "youtube_ids": ["CZt-rVn2BJs"], "entry_sec": 23, "exit_sec": 115, "duration_sec": 184, "energy": 9, "language": "haryanvi-bhojpuri", "subtype": "party", "banger": True},
    {"song_id": "teri-aakhya-ka-yo-kajal", "title": "Teri Aakhya Ka Yo Kajal", "artist": "DC Madana", "youtube_ids": ["1f7XwU79i8c"], "entry_sec": 20, "exit_sec": 110, "duration_sec": 190, "energy": 9, "language": "haryanvi-bhojpuri", "subtype": "party", "banger": True},
    {"song_id": "lollipop-lagelu-pawan-singh", "title": "Lollipop Lagelu", "artist": "Pawan Singh", "youtube_ids": ["1uUq_WqP9kM"], "entry_sec": 30, "exit_sec": 130, "duration_sec": 240, "energy": 10, "language": "haryanvi-bhojpuri", "subtype": "party", "banger": True}
]

existing_ids = {s["song_id"] for s in library}
added = 0
for g in global_hits:
    if g["song_id"] not in existing_ids:
        library.append(g)
        added += 1

print(f"Added {added} global bangers. Total library now: {len(library)} tracks!")

with open("naux_full_library.json", "w", encoding="utf-8") as out:
    json.dump(library, out, indent=2)

print("Saved updated naux_full_library.json!")

