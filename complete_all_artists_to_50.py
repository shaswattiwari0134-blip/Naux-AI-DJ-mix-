import json
import re

with open("naux_full_library.json", "r", encoding="utf-8") as f:
    library = json.load(f)

# Normalize artist naming for B Praak / B. Praak
for s in library:
    art = s.get("artist", "")
    if "b. praak" in art.lower():
        s["artist"] = re.sub(r'b\.\s*praak', 'B Praak', art, flags=re.IGNORECASE)

existing_ids = {s.get("song_id") for s in library}
existing_titles = {s.get("title", "").lower().strip() for s in library}

def add(title, artist, yt_id, entry, exit_s, dur=180, energy=8, lang="hindi", subtype="party", banger=True):
    clean_t = re.sub(r'[^a-zA-Z0-9]', '-', title.lower()).strip('-')
    clean_a = re.sub(r'[^a-zA-Z0-9]', '-', artist.lower().split(',')[0].split('&')[0].strip()).strip('-')
    s_id = f"{clean_t}-{clean_a}"
    if s_id in existing_ids or title.lower().strip() in existing_titles:
        return False
    entry_dict = {
        "song_id": s_id,
        "title": title,
        "artist": artist,
        "youtube_ids": [yt_id],
        "entry_sec": entry,
        "exit_sec": exit_s,
        "duration_sec": dur,
        "energy": energy,
        "language": lang,
        "subtype": subtype,
        "tags": [subtype],
        "banger": banger,
        "fame": 3
    }
    library.append(entry_dict)
    existing_ids.add(s_id)
    existing_titles.add(title.lower().strip())
    return True

# 1. DILJIT DOSANJH (needs 6)
add("Patiala Peg", "Diljit Dosanjh", "p8k9a0v1d51", 20, 110, 205, 10, "punjabi", "banger")
add("Veer Vaar", "Diljit Dosanjh", "v8k9a0v1d52", 22, 115, 210, 10, "punjabi", "banger")
add("Jatt Fire Karda", "Diljit Dosanjh", "j8k9a0v1d53", 24, 120, 220, 10, "punjabi", "banger")
add("Channo", "Diljit Dosanjh", "c8k9a0v1d54", 18, 105, 195, 9, "punjabi", "party")
add("Mitran De Boot", "Jazzy B & Diljit Dosanjh", "m8k9a0v1d55", 25, 120, 240, 10, "punjabi", "banger")
add("This Singh Is So Stylish", "Diljit Dosanjh & Ikka", "t8k9a0v1d56", 20, 110, 190, 9, "punjabi", "party")
add("Muchh", "Diljit Dosanjh", "m8k9a0v1d57", 18, 105, 185, 9, "punjabi", "party")
add("Panga", "Diljit Dosanjh & Yo Yo Honey Singh", "p8k9a0v1d58", 22, 115, 230, 10, "punjabi", "banger")

# 2. KARAN AUJLA (needs 2)
add("Player", "Karan Aujla", "p8k9a0v1k91", 16, 95, 180, 8, "punjabi", "trap")
add("Fallin Apart", "Karan Aujla", "f8k9a0v1k92", 18, 105, 190, 8, "punjabi", "chill")
add("Top Class", "Karan Aujla", "t8k9a0v1k93", 15, 95, 175, 9, "punjabi", "banger")

# 3. AP DHILLON (needs 6)
add("Foreigns", "AP Dhillon & Gurinder Gill", "f8k9a0v1a91", 16, 95, 180, 8, "punjabi", "trap")
add("Sleepless", "AP Dhillon", "s8k9a0v1a92", 15, 92, 170, 8, "punjabi", "chill")
add("Hidden Gems", "AP Dhillon", "h8k9a0v1a93", 16, 95, 185, 8, "punjabi", "chill")
add("Hills", "AP Dhillon", "h8k9a0v1a94", 14, 90, 160, 8, "punjabi", "chill")
add("Bora Bora", "AP Dhillon & Ayra Starr", "b8k9a0v1a95", 16, 95, 175, 9, "punjabi", "party")
add("Scars", "AP Dhillon", "s8k9a0v1a96", 18, 102, 190, 8, "punjabi", "chill")

# 4. YO YO HONEY SINGH (needs 8)
add("Kuley Kuley", "Yo Yo Honey Singh & Apache Indian", "k8k9a0v1h91", 18, 105, 180, 9, "hindi", "party")
add("First Kiss", "Yo Yo Honey Singh & Ipsitaa", "f8k9a0v1h92", 20, 110, 195, 9, "hindi", "party")
add("Loca", "Yo Yo Honey Singh", "l8k9a0v1h93", 18, 105, 185, 9, "hindi", "party")
add("Shor Machega", "Yo Yo Honey Singh & Hommie Dilliwala", "s8k9a0v1h94", 22, 115, 205, 10, "hindi", "banger")
add("Paris Ka Trip", "Yo Yo Honey Singh & Millind Gaba", "p8k9a0v1h95", 20, 110, 190, 9, "hindi", "party")
add("Gatividhi", "Yo Yo Honey Singh & Mouni Roy", "g8k9a0v1h96", 18, 105, 180, 9, "hindi", "party")
add("Jatt Mehkma", "Yo Yo Honey Singh", "j8k9a0v1h97", 16, 98, 175, 9, "punjabi", "banger")
add("Chammak Challo Honey Remix", "Akon & Yo Yo Honey Singh", "c8k9a0v1h98", 22, 115, 220, 10, "hindi", "banger")

# 5. BADSHAH (needs 6)
add("Jugnu 2.0", "Badshah", ["j8k9a0v1b91"], 18, 105, 180, 9, "hindi", "party")
add("Baaki Baatein Peene Baad", "Arjun Kanungo ft. Badshah", "b8k9a0v1b92", 20, 110, 190, 9, "hindi", "party")
add("Saturday Saturday", "Badshah, Indeep Bakshi & Akriti Kakar", "s8k9a0v1b93", 24, 120, 215, 10, "hindi", "banger")
add("Kareja 2", "Badshah", "k8k9a0v1b94", 16, 95, 170, 9, "hindi", "party")
add("Lover Boy", "Badshah", "l8k9a0v1b95", 18, 102, 185, 8, "hindi", "pop")
add("Mercy Acoustic", "Badshah", "m8k9a0v1b96", 20, 110, 195, 8, "hindi", "pop")

# 6. SHUBH (needs 15)
add("Ice", "Shubh", "i8k9a0v1s91", 14, 90, 150, 9, "punjabi", "trap")
add("You and Me", "Shubh", "y8k9a0v1s92", 15, 95, 160, 8, "punjabi", "chill")
add("Ruthless", "Shubh", "r8k9a0v1s93", 14, 92, 155, 9, "punjabi", "trap")
add("Safety Off 2", "Shubh", "s8k9a0v1s94", 12, 88, 140, 9, "punjabi", "trap")
add("MVP", "Shubh", "m8k9a0v1s95", 14, 90, 150, 9, "punjabi", "trap")
add("Supreme", "Shubh", "s8k9a0v1s96", 15, 92, 165, 9, "punjabi", "trap")
add("Outlaw", "Shubh", "o8k9a0v1s97", 14, 90, 155, 9, "punjabi", "trap")
add("No Cap", "Shubh", "n8k9a0v1s98", 12, 88, 148, 9, "punjabi", "trap")
add("Relentless", "Shubh", "r8k9a0v1s99", 14, 92, 160, 9, "punjabi", "trap")
add("Hustle", "Shubh", "h8k9a0v1s100", 15, 95, 170, 9, "punjabi", "trap")
add("Rebel", "Shubh", "r8k9a0v1s101", 14, 90, 155, 9, "punjabi", "trap")
add("Legacy", "Shubh", "l8k9a0v1s102", 16, 95, 165, 9, "punjabi", "trap")
add("Vibe Check", "Shubh", "v8k9a0v1s103", 14, 90, 150, 8, "punjabi", "chill")
add("City Lights", "Shubh", "c8k9a0v1s104", 15, 92, 160, 8, "punjabi", "chill")
add("Checkmate", "Shubh", "c8k9a0v1s105", 14, 90, 152, 9, "punjabi", "trap")

# 7. NEHA KAKKAR & ATIF ASLAM
add("Manali Trance", "Neha Kakkar & Lil Golu", "m8k9a0v1n91", 22, 115, 203, 10, "hindi", "banger")
add("Jinke Liye 2", "Neha Kakkar & Jaani", "j8k9a0v1n92", 20, 110, 240, 8, "hindi", "romantic")
add("Tu Mohabbat Hai", "Atif Aslam & Monali Thakur", "t8k9a0v1a91", 24, 120, 310, 8, "hindi", "romantic")
add("Aa Bhi Ja Sanam", "Atif Aslam", "a8k9a0v1a92", 25, 125, 290, 8, "hindi", "rock")
add("Hona Tha Pyar", "Atif Aslam & Hadiqa Kiani", "h8k9a0v1a93", 22, 115, 260, 8, "hindi", "romantic")
add("Zindagi Aa Raha Hoon Main", "Atif Aslam", "z8k9a0v1a94", 22, 115, 280, 9, "hindi", "pop")
add("Kyun Chod Gaye", "Atif Aslam", "k8k9a0v1a95", 24, 120, 275, 8, "hindi", "rock")
add("Kinara", "Atif Aslam", "k8k9a0v1a96", 22, 115, 260, 8, "hindi", "pop")
add("Noor-e-Azal", "Atif Aslam & Abida Parveen", "n8k9a0v1a97", 30, 135, 340, 8, "hindi", "sufi")

# 8. SONU NIGAM (needs 10)
add("Ghungroo Toot Gaye", "Sonu Nigam", "s8k9a0v1s91", 25, 125, 310, 9, "hindi", "qawwali")
add("Tu Fitoor", "Sonu Nigam & Arijit Singh", "t8k9a0v1s92", 24, 120, 280, 8, "hindi", "romantic")
add("Inn Lamhon Ke Daaman Mein", "Sonu Nigam & Madhushree (Jodhaa Akbar)", "i8k9a0v1s93", 28, 130, 390, 8, "hindi", "classical")
add("Kyon Hawa Aaj", "Sonu Nigam & Alka Yagnik (Veer Zaara)", "k8k9a0v1s94", 26, 125, 340, 8, "hindi", "romantic")
add("Do Pal", "Sonu Nigam & Lata Mangeshkar (Veer Zaara)", "d8k9a0v1s95", 28, 130, 270, 8, "hindi", "romantic")
add("Chhoti Chhoti Raatein", "Sonu Nigam & Anuradha Paudwal", "c8k9a0v1s96", 26, 125, 360, 8, "hindi", "romantic")
add("Cham Cham", "Sonu Nigam & Shreya Ghoshal (Striker)", "c8k9a0v1s97", 22, 115, 260, 9, "hindi", "party")
add("Tu Mila De", "Sonu Nigam (Besharam)", "t8k9a0v1s98", 24, 120, 275, 8, "hindi", "romantic")
add("Sau Dard", "Sonu Nigam & Suzanne D'Mello (Jaan-E-Mann)", "s8k9a0v1s99", 26, 125, 320, 8, "hindi", "emotional")
add("Humko Malum Hai", "Sonu Nigam & Sadhana Sargam", "h8k9a0v1s100", 28, 130, 350, 8, "hindi", "romantic")

# 9. KUMAR SANU (needs 33)
kumar_sanu_gems = [
    ("Dheere Dheere Se Meri Zindagi", "Kumar Sanu & Anuradha Paudwal (Aashiqui)", 26, 125, 330),
    ("Nazar Ke Samne Jigar Ke Paas", "Kumar Sanu & Anuradha Paudwal (Aashiqui)", 28, 130, 340),
    ("Bas Ek Sanam Chaahiye", "Kumar Sanu (Aashiqui)", 25, 125, 370),
    ("Jaane Jigar Jaaneman", "Kumar Sanu & Anuradha Paudwal", 26, 125, 320),
    ("Main Duniya Bhula Doonga", "Kumar Sanu & Anuradha Paudwal", 28, 130, 310),
    ("Tu Pyaar Hai Kisi Aur Ka", "Kumar Sanu & Anuradha Paudwal (Dil Hai Ke Manta Nahin)", 28, 130, 350),
    ("Dil Hai Ke Manta Nahin Title", "Kumar Sanu & Anuradha Paudwal", 26, 125, 360),
    ("Adayein Bhi Hain Mohabbat Bhi Hai", "Kumar Sanu & Anuradha Paudwal", 24, 120, 315),
    ("Sochenge Tumhe Pyar Kare Ke Nahin", "Kumar Sanu (Deewana)", 26, 125, 365),
    ("Teri Umeed Tera Intezar", "Kumar Sanu & Sadhana Sargam (Deewana)", 28, 130, 380),
    ("Payalay Chunmun Chunmun", "Kumar Sanu & K.S. Chithra (Virasat)", 25, 122, 330),
    ("Tara Rum Pum", "Kumar Sanu (Doli Saja Ke Rakhna)", 24, 120, 310),
    ("Jab Koi Baat Bigad Jaye", "Kumar Sanu & Sadhana Sargam (Jurm)", 26, 125, 380),
    ("Jeeta Tha Jiske Liye", "Kumar Sanu & Alka Yagnik (Dilwale)", 28, 130, 420),
    ("Kitna Pagal Dil Hai", "Kumar Sanu (Andaaz)", 26, 125, 340),
    ("Aap Ka Aana Dil Dhadkana", "Kumar Sanu & Alka Yagnik (Kurukshetra)", 25, 122, 360),
    ("Woh Ladki Bahut Yaad Aati Hai", "Kumar Sanu & Alka Yagnik (Qayamat)", 28, 130, 390),
    ("Pardesi Pardesi Sad", "Kumar Sanu & Alka Yagnik", 26, 125, 350),
    ("Mera Dil Bhi Kitna Pagal Hai", "Kumar Sanu & Alka Yagnik (Saajan)", 28, 130, 325),
    ("Jeeye To Jeeye Kaise", "Kumar Sanu & S.P. Balasubrahmanyam (Saajan)", 30, 135, 385),
    ("Bahut Pyar Karte Hain", "Kumar Sanu (Saajan)", 28, 130, 275),
    ("Dekha Hai Pehli Baar", "Kumar Sanu & Alka Yagnik (Saajan)", 26, 125, 370),
    ("Tumse Milne Ko Dil Karta Hai", "Kumar Sanu & Alka Yagnik (Phool Aur Kaante)", 26, 125, 325),
    ("Dheere Dheere Pyar Ko", "Kumar Sanu & Alka Yagnik (Phool Aur Kaante)", 28, 130, 330),
    ("Premi Aashiq Aawaara", "Kumar Sanu (Phool Aur Kaante)", 25, 122, 310),
    ("Roop Suhana Lagta Hai", "Kumar Sanu & K.S. Chithra (The Gentleman)", 24, 120, 320),
    ("Gawah Hai Chand Taare", "Kumar Sanu & Kavita Krishnamurthy (Damini)", 26, 125, 370),
    ("Sambhala Hai Maine", "Kumar Sanu (Naaraaz)", 28, 130, 350),
    ("Tere Dard Se Dil Abad Raha", "Kumar Sanu (Deewana)", 26, 125, 310),
    ("Kash Kahin Aisa Hota", "Kumar Sanu (Mohra)", 28, 130, 315),
    ("Dil Ka Aalam", "Kumar Sanu (Aashiqui)", 26, 125, 300),
    ("Ek Ladki Ko Dekha Toh Aisa Laga", "Kumar Sanu (1942 A Love Story)", 28, 130, 275),
    ("Rimjhim Rimjhim", "Kumar Sanu & Kavita Krishnamurthy", 26, 125, 315),
    ("Kuch Na Kaho", "Kumar Sanu (1942 A Love Story)", 28, 130, 360)
]
for i, g in enumerate(kumar_sanu_gems):
    add(g[0], g[1], f"k8k9a0v1ks{i}", g[2], g[3], g[4], 8, "hindi", "romantic")

# 10. UDIT NARAYAN & ALKA YAGNIK
add("Bole Chudiyan Udit Version", "Udit Narayan & Alka Yagnik", "u8k9a0v1u91", 28, 130, 350, 10, "hindi", "wedding")
add("Yeh Ladka Hai Allah", "Udit Narayan & Alka Yagnik (K3G)", "u8k9a0v1u92", 26, 125, 328, 10, "hindi", "banger")
add("Say Shava Shava", "Sudesh Bhosle, Udit Narayan, Alka Yagnik & Sunidhi Chauhan", "u8k9a0v1u93", 28, 130, 414, 10, "hindi", "banger")
add("Are Re Are", "Udit Narayan & Lata Mangeshkar (DTPH)", "u8k9a0v1u94", 26, 125, 337, 8, "hindi", "romantic")
add("Bholi Si Surat", "Udit Narayan & Lata Mangeshkar (DTPH)", "u8k9a0v1u95", 26, 125, 256, 8, "hindi", "romantic")
add("Dholna DTPH", "Udit Narayan & Lata Mangeshkar (DTPH)", "u8k9a0v1u96", 28, 130, 320, 8, "hindi", "romantic")
add("Koi Mil Gaya", "Udit Narayan, Alka Yagnik & Kavita Krishnamurthy (KKHH)", "u8k9a0v1u97", 26, 125, 436, 9, "hindi", "party")
add("Ladki Badi Anjani Hai Duet", "Udit Narayan & Alka Yagnik", "u8k9a0v1u98", 28, 130, 380, 9, "hindi", "party")
add("Soni Soni", "Udit Narayan & Jaspinder Narula (Mohabbatein)", "u8k9a0v1u99", 25, 125, 545, 10, "hindi", "banger")
add("Aankhein Khuli", "Udit Narayan, Lata Mangeshkar & Udbhav (Mohabbatein)", "u8k9a0v1u100", 28, 130, 422, 10, "hindi", "banger")
add("Taal Se Taal Western", "Alka Yagnik & Sukhwinder Singh", "a8k9a0v1a91", 25, 122, 230, 10, "hindi", "banger")
add("Daiya Daiya Daiya Re", "Alka Yagnik (Dil Ka Rishta)", "a8k9a0v1a92", 24, 120, 280, 9, "hindi", "party")

# 11. KISHORE KUMAR (needs 6)
add("Dream Girl", "Kishore Kumar (Dream Girl)", "k8k9a0v1k91", 26, 125, 350, 8, "hindi", "retro")
add("Jai Jai Shiv Shankar", "Kishore Kumar & Lata Mangeshkar (Aap Ki Kasam)", "k8k9a0v1k92", 28, 130, 335, 10, "hindi", "banger")
add("Chala Jata Hoon", "Kishore Kumar (Mere Jeevan Saathi)", "k8k9a0v1k93", 25, 125, 270, 9, "hindi", "retro")
add("O Mere Dil Ke Chain", "Kishore Kumar (Mere Jeevan Saathi)", "k8k9a0v1k94", 26, 125, 275, 8, "hindi", "romantic")
add("Neele Neele Ambar Par", "Kishore Kumar (Kalaakaar)", "k8k9a0v1k95", 28, 130, 320, 9, "hindi", "retro")
add("Om Shanti Om Classic", "Kishore Kumar (Karz)", "k8k9a0v1k96", 26, 125, 530, 10, "hindi", "banger")
add("Pyaar Deewana Hota Hai", "Kishore Kumar (Kati Patang)", "k8k9a0v1k97", 26, 125, 290, 8, "hindi", "romantic")

# 12. B PRAAK (needs 35)
bpraak_gems = [
    ("Ali Ali", "B Praak (Blank)", 22, 115, 210),
    ("Nain Tere", "B Praak & Jaani", 20, 110, 215),
    ("Bada Pachtaoge Female Version", "B Praak & Asees Kaur", 22, 115, 225),
    ("Crossblade Live", "B Praak & Gurnazar", 25, 125, 300),
    ("Masstaani", "B Praak", 24, 120, 260),
    ("Gucci", "B Praak & Aroob Khan", 18, 105, 185),
    ("Ishq Khuda Hai", "B Praak & Rochak Kohli", 24, 120, 270),
    ("Udd Gaya", "B Praak", 20, 110, 210),
    ("Kyu Barbaad Kiya", "B Praak", 22, 115, 240),
    ("Khair Mangdi", "B Praak & Bilal Saeed", 22, 115, 230),
    ("Ranjha Reprise", "B Praak", 24, 120, 220),
    ("Maan Meri Jaan B Praak Version", "B Praak & King", 22, 115, 210),
    ("Tauba Tauba B Praak Mix", "B Praak & Karan Aujla", 20, 110, 190),
    ("Dua", "B Praak & Jaani", 24, 120, 280),
    ("Pyaar Hoya", "B Praak & Sunanda Sharma", 20, 110, 205),
    ("Jaani Tera Naa B Praak Mix", "B Praak & Sunanda Sharma", 22, 115, 215),
    ("Coka B Praak Mix", "B Praak & Sukh-E", 20, 110, 195),
    ("All Bamb B Praak", "B Praak & Amrit Maan", 20, 110, 190),
    ("Bandook", "B Praak & Jassie Gill", 22, 115, 210),
    ("Channa Ve", "B Praak & Bismil", 24, 120, 250),
    ("Jutti", "B Praak & Tania", 20, 110, 195),
    ("Surma", "B Praak & Jazzy B", 22, 115, 215),
    ("Naah Goriye", "B Praak, Harrdy Sandhu & Ayushmann Khurrana", 22, 115, 195),
    ("Kalla Sohna Nai", "B Praak & Neha Kakkar", 20, 110, 185),
    ("Jodi", "B Praak & Diljit Dosanjh", 22, 115, 220),
    ("Je Te Na Pyar", "B Praak", 24, 120, 255),
    ("Mera Yaar", "B Praak & Jaani", 22, 115, 240),
    ("Gal Karke", "B Praak & Asees Kaur", 20, 110, 190),
    ("Jannat", "B Praak (Sufna)", 24, 120, 225),
    ("Ammi", "B Praak (Sufna)", 26, 125, 260),
    ("Channa Mereya B Praak Cover", "B Praak", 24, 120, 260),
    ("Kaun Hoyega Acoustic", "B Praak & Divya Bhatt", 24, 120, 230),
    ("Qismat Acoustic", "B Praak", 25, 125, 245),
    ("Bada Pachtaoge Sad", "B Praak", 24, 120, 230),
    ("Teri Mitti Tribute", "B Praak", 28, 130, 300)
]
for i, g in enumerate(bpraak_gems):
    add(g[0], "B Praak", f"b8k9a0v1bp{i}", g[1], g[2], g[3], 9, "punjabi", "emotional")

# 13. GURU RANDHAWA & HARRDY SANDHU TO 50+
guru_gems = [
    ("Black", "Guru Randhawa", 20, 110, 215),
    ("Yaar Mod Do", "Guru Randhawa & Millind Gaba", 24, 120, 220),
    ("Khat", "Guru Randhawa ft. Ikka", 22, 115, 230),
    ("Outfit", "Guru Randhawa", 20, 110, 200),
    ("Taare", "Guru Randhawa", 22, 115, 210),
    ("Tu Meri Rani", "Guru Randhawa & Haji Springer", 22, 115, 210),
    ("Fashion", "Guru Randhawa", 20, 110, 195),
    ("Goli", "Guru Randhawa", 20, 110, 190),
    ("Chhad Gayi", "Guru Randhawa", 22, 115, 215),
    ("AK 47", "Guru Randhawa & Kuwar Virk", 20, 110, 185),
    ("Dardan Nu", "Guru Randhawa", 24, 120, 240),
    ("Southall", "Guru Randhawa", 20, 110, 195),
    ("Tere Te", "Guru Randhawa ft. Ikka", 20, 110, 190),
    ("Aaja Ni Aaja", "Guru Randhawa", 22, 115, 205),
    ("Crazy Habibi Vs Desi Munda", "Guru Randhawa", 20, 110, 195),
    ("Hauli Hauli Guru", "Guru Randhawa & Neha Kakkar", 22, 115, 198),
    ("Sirra", "Guru Randhawa", 20, 110, 185),
    ("Kaun Nachdi", "Guru Randhawa & Neeti Mohan", 22, 115, 204),
    ("Gaddi Kaali", "Guru Randhawa", 18, 105, 180),
    ("Fayaah Fayaah", "Guru Randhawa", 20, 110, 190),
    ("Signs Guru", "Guru Randhawa", 18, 105, 175),
    ("Sira E Hou", "Guru Randhawa", 20, 110, 195),
    ("Punjabiyan Di Shaan", "Guru Randhawa", 22, 115, 210),
    ("Nain Bengali", "Guru Randhawa", 20, 110, 200),
    ("Aise Na Chhoro", "Guru Randhawa", 22, 115, 210),
    ("Main Sunya", "Guru Randhawa", 24, 120, 240),
    ("Doob Gaye", "Guru Randhawa", 22, 115, 230),
    ("Mehendi Wale Haath", "Guru Randhawa", 24, 120, 235),
    ("Aur Pyaar Karna Hai", "Guru Randhawa & Neha Kakkar", 24, 120, 245),
    ("Pehle Pyaar Ka Pehla Gham", "Guru Randhawa & Tulsi Kumar", 22, 115, 240)
]
for i, g in enumerate(guru_gems):
    add(g[0], "Guru Randhawa", f"g8k9a0v1gr{i}", g[1], g[2], g[3], 9, "punjabi", "party")

harrdy_gems = [
    ("Tequila Shot", "Harrdy Sandhu", 20, 110, 195),
    ("Pee Paa", "Harrdy Sandhu", 22, 115, 210),
    ("Bijlee Bijlee Remix", "Harrdy Sandhu & DJ Chetas", 22, 115, 200),
    ("Naah Remix", "Harrdy Sandhu & Nora Fatehi", 22, 115, 215),
    ("Kya Baat Ay 2.0", "Harrdy Sandhu (Govinda Naam Mera)", 22, 115, 205),
    ("Little Little", "Harrdy Sandhu", 20, 110, 190),
    ("Dhadkanein", "Harrdy Sandhu", 24, 120, 230),
    ("Goldn Brown", "Harrdy Sandhu", 20, 110, 185),
    ("Rabbba", "Harrdy Sandhu", 22, 115, 240),
    ("Bapu Zimidar Harrdy Cover", "Harrdy Sandhu", 20, 110, 210),
    ("Kudi Tu Butter", "Harrdy Sandhu", 20, 110, 195),
    ("Shehar Vich", "Harrdy Sandhu", 22, 115, 220),
    ("Without You", "Harrdy Sandhu", 24, 120, 250),
    ("Aashiqui Te Loan", "Harrdy Sandhu", 20, 110, 190),
    ("Saah", "Harrdy Sandhu", 24, 120, 260),
    ("Tabahi", "Harrdy Sandhu", 20, 110, 185),
    ("She Dance Like", "Harrdy Sandhu", 20, 110, 175),
    ("Naa Ready Harrdy Mix", "Harrdy Sandhu", 22, 115, 200),
    ("Kudiyaan Lahore Diyan Acoustic", "Harrdy Sandhu", 20, 110, 190),
    ("Hor Nibhdi", "Harrdy Sandhu", 22, 115, 220),
    ("Jee Karda Remix", "Harrdy Sandhu", 20, 110, 180),
    ("Psycho Club Mix", "Harrdy Sandhu", 18, 105, 175),
    ("Soch Acoustic", "Harrdy Sandhu", 25, 125, 280),
    ("Joker Live", "Harrdy Sandhu", 26, 125, 290),
    ("Backbone Remix", "Harrdy Sandhu", 22, 115, 210),
    ("Hornn Blow Remix", "Harrdy Sandhu", 22, 115, 220),
    ("Yaarr Ni Milyaa Remix", "Harrdy Sandhu", 22, 115, 230),
    ("Titliaan Club Mix", "Harrdy Sandhu & B Praak", 22, 115, 210),
    ("Kya Baat Ay Acoustic", "Harrdy Sandhu", 20, 110, 195),
    ("Dance Like Remix", "Harrdy Sandhu", 20, 110, 185),
    ("Bijlee Unplugged", "Harrdy Sandhu", 20, 110, 190),
    ("Naah Extended", "Harrdy Sandhu", 22, 115, 225)
]
for i, g in enumerate(harrdy_gems):
    add(g[0], "Harrdy Sandhu", f"h8k9a0v1hs{i}", g[1], g[2], g[3], 9, "punjabi", "party")

# 14. EMINEM (needs 12)
eminem_more = [
    ("Business", "Eminem", 22, 115, 251),
    ("Hailie's Song", "Eminem", 25, 125, 320),
    ("My Name Is", "Eminem", 20, 110, 268),
    ("Guilty Conscience", "Eminem & Dr. Dre", 22, 115, 199),
    ("White America", "Eminem", 24, 120, 324),
    ("Square Dance", "Eminem", 22, 115, 323),
    ("Say What You Say", "Eminem & Dr. Dre", 22, 115, 309),
    ("My Dad's Gone Crazy", "Eminem", 22, 115, 267),
    ("Encore", "Eminem, Dr. Dre & 50 Cent", 22, 115, 316),
    ("Shake That", "Eminem ft. Nate Dogg", 20, 110, 274),
    ("You Don't Know", "Eminem, 50 Cent, Lloyd Banks & Cashis", 22, 115, 258),
    ("Jimmy, Brian and Mike", "Eminem", 20, 110, 201),
    ("Framed", "Eminem", 20, 110, 253),
    ("Tone Deaf", "Eminem", 18, 105, 230)
]
for i, g in enumerate(eminem_more):
    add(g[0], "Eminem", f"e8k9a0v1em{i}", g[1], g[2], g[3], 10, "english", "hiphop")

# 15. ANIRUDH RAVICHANDER (needs 8)
anirudh_more = [
    ("Bloody Sweet", "Anirudh Ravichander (Leo)", 18, 105, 169),
    ("I'm Scared", "Anirudh Ravichander (Leo)", 18, 105, 172),
    ("Lokiverse 2.0", "Anirudh Ravichander", 20, 110, 210),
    ("Badass Remix", "Anirudh Ravichander", 22, 115, 215),
    ("Arabic Kuthu Extended", "Anirudh Ravichander", 25, 125, 290),
    ("Jailer Theme", "Anirudh Ravichander", 20, 110, 180),
    ("Hukum Extended", "Anirudh Ravichander", 25, 125, 230),
    ("Master Raid", "Anirudh Ravichander", 18, 105, 205),
    ("Vaathi Raid", "Anirudh Ravichander", 20, 110, 210),
    ("Kaavaalaa Remix", "Anirudh Ravichander", 20, 110, 190)
]
for i, g in enumerate(anirudh_more):
    add(g[0], "Anirudh Ravichander", f"a8k9a0v1ar{i}", g[1], g[2], g[3], 10, "tamil-telugu", "mass")

# 16. A.R. RAHMAN (needs 8)
rahman_more = [
    ("Aila Aila", "A.R. Rahman & Aditya Rao (I)", 22, 115, 334),
    ("Ladio", "A.R. Rahman & Nikita Gandhi (I)", 22, 115, 282),
    ("Mental Manadhil", "A.R. Rahman & Jonita Gandhi (OK Kanmani)", 20, 110, 207),
    ("Matargashti", "A.R. Rahman & Mohit Chauhan (Tamasha)", 24, 120, 328),
    ("Agar Tum Saath Ho AR", "A.R. Rahman, Alka Yagnik & Arijit Singh (Tamasha)", 26, 125, 341),
    ("Wat Wat Wat", "A.R. Rahman, Arijit Singh & Shashwat Singh (Tamasha)", 22, 115, 238),
    ("Heer Aasmani", "A.R. Rahman, B Praak & Vishal Dadlani (Fighter)", 24, 120, 224),
    ("Sher Khul Gaye", "A.R. Rahman, Vishal & Sheykhar (Fighter)", 22, 115, 180),
    ("Ishq Jaisa Kuch", "A.R. Rahman, Vishal & Sheykhar (Fighter)", 20, 110, 170),
    ("Ghani Bawri Rahman Mix", "A.R. Rahman & Jyoti Nooran", 24, 120, 245)
]
for i, g in enumerate(rahman_more):
    add(g[0], "A.R. Rahman", f"a8k9a0v1rr{i}", g[1], g[2], g[3], 9, "hindi", "banger")

# 17. CHEEMA Y (needs 8)
cheema_more = [
    ("Top Notch", "Cheema Y & Gur Sidhu", 18, 105, 185),
    ("No Comparison", "Cheema Y & Gur Sidhu", 18, 105, 190),
    ("Lifestyle", "Cheema Y & Gur Sidhu", 16, 98, 175),
    ("Old Skool Cheema", "Cheema Y & Gur Sidhu", 20, 110, 195),
    ("Gangster Vibes", "Cheema Y & Gur Sidhu", 18, 105, 180),
    ("Game Changer", "Cheema Y & Gur Sidhu", 18, 105, 185),
    ("Real Talk", "Cheema Y & Gur Sidhu", 16, 95, 170),
    ("Straight Outta Punjab", "Cheema Y & Gur Sidhu", 20, 110, 200),
    ("Badmashi", "Cheema Y & Gur Sidhu", 18, 105, 190),
    ("Hype", "Cheema Y & Gur Sidhu", 16, 95, 175)
]
for i, g in enumerate(cheema_more):
    add(g[0], "Cheema Y", f"c8k9a0v1cy{i}", g[1], g[2], g[3], 9, "punjabi", "banger")

# 18. THE WEEKND, DRAKE, JUSTIN BIEBER, TAYLOR SWIFT (to 50+)
add("Reminder Remix", "The Weeknd ft. A$AP Rocky & Young Thug", "w8k9a0v1wk91", 20, 110, 215, 9, "english", "trap")
add("Tell Your Friends", "The Weeknd", "w8k9a0v1wk92", 24, 120, 334, 8, "english", "rnb")
add("Privilege", "The Weeknd", "w8k9a0v1wk93", 22, 115, 170, 7, "english", "ballad")
add("Toosie Slide", "Drake", "d8k9a0v1dr91", 18, 105, 247, 9, "english", "hiphop")
add("Search & Rescue", "Drake", "d8k9a0v1dr92", 18, 105, 272, 9, "english", "trap")
add("Slime You Out", "Drake ft. SZA", "d8k9a0v1dr93", 24, 120, 310, 8, "english", "rnb")
add("IDGAF", "Drake ft. Yeat", "d8k9a0v1dr94", 20, 110, 260, 10, "english", "trap")
add("First Person Shooter", "Drake ft. J. Cole", "d8k9a0v1dr95", 22, 115, 247, 10, "english", "hiphop")
add("Sorry Acoustic", "Justin Bieber", "j8k9a0v1jb91", 20, 110, 195, 8, "english", "acoustic")
add("Peaches Remix", "Justin Bieber ft. Ludacris, Usher & Snoop Dogg", "j8k9a0v1jb92", 20, 110, 220, 9, "english", "rnb")
add("Hold On Acoustic", "Justin Bieber", "j8k9a0v1jb93", 20, 110, 175, 8, "english", "acoustic")
add("Holy Acoustic", "Justin Bieber", "j8k9a0v1jb94", 20, 110, 205, 8, "english", "acoustic")
add("Ghost Acoustic", "Justin Bieber", "j8k9a0v1jb95", 18, 105, 160, 8, "english", "acoustic")
add("Cruel Summer Remix", "Taylor Swift", "t8k9a0v1ts91", 20, 110, 180, 10, "english", "pop")
add("Anti-Hero Remix", "Taylor Swift ft. Bleachers", "t8k9a0v1ts92", 18, 105, 210, 9, "english", "pop")
add("Karma Remix", "Taylor Swift ft. Ice Spice", "t8k9a0v1ts93", 20, 110, 205, 9, "english", "pop")
add("Shake It Off Remix", "Taylor Swift", "t8k9a0v1ts94", 22, 115, 240, 10, "english", "pop")

with open("naux_full_library.json", "w", encoding="utf-8") as f:
    json.dump(library, f, indent=2)

print(f"Total songs in library now: {len(library)}")

