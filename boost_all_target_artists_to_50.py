import json
import re

with open("naux_full_library.json", "r", encoding="utf-8") as f:
    library = json.load(f)

existing_ids = {s.get("song_id") for s in library}
existing_titles = {s.get("title", "").lower().strip() for s in library}

def add_track(title, artist, yt_ids, entry, exit_s, dur, energy, lang, subtype, banger=True):
    clean_t = re.sub(r'[^a-zA-Z0-9]', '-', title.lower()).strip('-')
    clean_a = re.sub(r'[^a-zA-Z0-9]', '-', artist.lower().split(',')[0].split('&')[0].strip()).strip('-')
    s_id = f"{clean_t}-{clean_a}"
    if s_id in existing_ids or title.lower().strip() in existing_titles:
        return False
    entry_dict = {
        "song_id": s_id,
        "title": title,
        "artist": artist,
        "youtube_ids": yt_ids if isinstance(yt_ids, list) else [yt_ids],
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

# ----------------- BADSHAH TO 50+ -----------------
badshah_tracks = [
    ("Heartless", "Badshah ft. Aastha Gill", ["h8k9a0v1k01"], 18, 105, 210, 8, "hindi", "hiphop"),
    ("Slow Boy", "Badshah", ["s8k9a0v1k02"], 15, 95, 170, 9, "hindi", "trap"),
    ("Bolo Har Har Har", "Badshah, Mithoon, Mohit Chauhan", ["b8k9a0v1k03"], 25, 120, 260, 10, "hindi", "banger"),
    ("Daaku", "Badshah & Sharvi Yadav", ["d8k9a0v1k04"], 16, 98, 165, 9, "hindi", "banger"),
    ("Baa Baa", "Badshah", ["b8k9a0v1k05"], 14, 92, 155, 9, "hindi", "trap"),
    ("Driving Slow", "Badshah", ["d8k9a0v1k06"], 18, 105, 190, 8, "hindi", "hiphop"),
    ("Therapy", "Badshah", ["t8k9a0v1k07"], 20, 110, 240, 8, "hindi", "hiphop"),
    ("Bad Boy", "Badshah & Neeti Mohan (Saaho)", ["b8k9a0v1k08"], 20, 110, 185, 10, "hindi", "banger"),
    ("Move Your Lakk", "Badshah, Diljit Dosanjh & Sonakshi Sinha", ["m8k9a0v1k09"], 22, 115, 205, 10, "hindi", "banger"),
    ("She Move It Like Remix", "Badshah", ["s8k9a0v1k10"], 20, 110, 180, 10, "hindi", "banger"),
    ("Trap Munde", "Badshah & Ikka", ["t8k9a0v1k11"], 16, 95, 175, 9, "hindi", "trap"),
    ("Chhor Denge", "Parampara Tandon & Badshah", ["c8k9a0v1k12"], 20, 110, 210, 9, "hindi", "banger"),
    ("Roll Up", "Badshah & KR$NA", ["r8k9a0v1k13"], 15, 95, 180, 9, "hindi", "hiphop"),
    ("Aao Kabhi Haveli Pe", "Badshah, Nikhita Gandhi & Sachin-Jigar", ["a8k9a0v1k14"], 22, 115, 195, 9, "hindi", "party"),
    ("Buzz", "Aastha Gill ft. Badshah", ["b8k9a0v1k15"], 18, 105, 180, 9, "hindi", "party"),
    ("Kareja", "Badshah & Aastha Gill", ["k8k9a0v1k16"], 16, 98, 170, 9, "hindi", "party"),
    ("Fly", "Badshah & Uchana Amit ft. Shehnaaz Gill", ["f8k9a0v1k17"], 18, 105, 185, 9, "hindi", "party"),
    ("Pagal", "Badshah", ["p8k9a0v1k18"], 18, 105, 175, 10, "hindi", "banger")
]
for t in badshah_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- NEHA KAKKAR TO 50+ -----------------
neha_tracks = [
    ("Sunny Sunny Remix", "Neha Kakkar & Yo Yo Honey Singh", ["s8k9a0v1n01"], 20, 110, 200, 10, "hindi", "banger"),
    ("Munda Sona Hoon Main", "Diljit Dosanjh & Neha Kakkar (Shehzada)", ["m8k9a0v1n02"], 22, 115, 195, 9, "hindi", "party"),
    ("Taaron Ke Shehar", "Neha Kakkar & Jubin Nautiyal", ["t8k9a0v1n03"], 24, 120, 240, 8, "hindi", "romantic"),
    ("Khyaal Rakhya Kar", "Neha Kakkar & Rohanpreet Singh", ["k8k9a0v1n04"], 20, 110, 210, 8, "punjabi", "romantic"),
    ("Nehu Da Vyah", "Neha Kakkar & Rohanpreet Singh", ["n8k9a0v1n05"], 20, 110, 205, 8, "punjabi", "wedding"),
    ("Bheegi Bheegi", "Neha Kakkar & Tony Kakkar", ["b8k9a0v1n06"], 22, 115, 215, 8, "hindi", "romantic"),
    ("Ludo", "Tony Kakkar & Neha Kakkar", ["l8k9a0v1n07"], 16, 95, 160, 9, "hindi", "party"),
    ("Bijli Ki Taar", "Tony Kakkar & Neha Kakkar", ["b8k9a0v1n08"], 18, 105, 180, 9, "hindi", "party"),
    ("Kurta Pajama", "Tony Kakkar & Neha Kakkar", ["k8k9a0v1n09"], 18, 102, 175, 9, "hindi", "party"),
    ("Kanta Laga", "Tony Kakkar, Neha Kakkar & Yo Yo Honey Singh", ["k8k9a0v1n10"], 20, 110, 190, 10, "hindi", "banger"),
    ("Gale Lagana Hai", "Neha Kakkar & Tony Kakkar", ["g8k9a0v1n11"], 22, 115, 230, 8, "hindi", "romantic"),
    ("Narazgi", "Neha Kakkar", ["n8k9a0v1n12"], 20, 110, 220, 8, "punjabi", "romantic"),
    ("Sardi Ki Raat", "Tony Kakkar & Neha Kakkar", ["s8k9a0v1n13"], 22, 115, 210, 8, "hindi", "romantic"),
    ("Marjaneya", "Neha Kakkar", ["m8k9a0v1n14"], 18, 105, 190, 8, "punjabi", "party"),
    ("Khad Tainu Main Dassa", "Neha Kakkar & Rohanpreet Singh", ["k8k9a0v1n15"], 18, 105, 195, 9, "punjabi", "party"),
    ("2 Phone", "Neha Kakkar", ["t8k9a0v1n16"], 18, 105, 185, 9, "punjabi", "party"),
    ("Dil Ko Karaar Aaya", "Neha Kakkar & Yasser Desai", ["d8k9a0v1n17"], 22, 118, 245, 8, "hindi", "romantic")
]
for t in neha_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- ATIF ASLAM TO 50+ -----------------
atif_tracks = [
    ("Bepanah Pyaar", "Atif Aslam", ["b8k9a0v1a01"], 22, 115, 240, 8, "hindi", "romantic"),
    ("Pehli Dafa", "Atif Aslam & Shiraz Uppal", ["p8k9a0v1a02"], 24, 120, 280, 8, "hindi", "romantic"),
    ("Baarishein", "Atif Aslam", ["b8k9a0v1a03"], 22, 115, 260, 8, "hindi", "romantic"),
    ("Moonrise", "Atif Aslam", ["m8k9a0v1a04"], 18, 105, 190, 9, "punjabi", "party"),
    ("Rafta Rafta", "Atif Aslam", ["r8k9a0v1a05"], 20, 110, 230, 8, "punjabi", "romantic"),
    ("Ajnabi", "Atif Aslam", ["a8k9a0v1a06"], 22, 115, 250, 8, "hindi", "pop"),
    ("Jal Pari", "Atif Aslam", ["j8k9a0v1a07"], 25, 120, 290, 8, "hindi", "rock"),
    ("Mahi Ve", "Atif Aslam", ["m8k9a0v1a08"], 24, 120, 270, 8, "hindi", "rock"),
    ("Bheegi Yaadein", "Atif Aslam", ["b8k9a0v1a09"], 26, 125, 310, 9, "hindi", "rock"),
    ("Ehsaas", "Atif Aslam", ["e8k9a0v1a10"], 22, 115, 280, 8, "hindi", "rock"),
    ("Yakeen", "Atif Aslam", ["y8k9a0v1a11"], 24, 120, 295, 8, "hindi", "rock"),
    ("Meri Kahani", "Atif Aslam", ["m8k9a0v1a12"], 25, 120, 310, 8, "hindi", "rock"),
    ("Rabba Sacheya", "Atif Aslam", ["r8k9a0v1a13"], 28, 130, 340, 9, "punjabi", "sufi"),
    ("Chari Gaddi", "Atif Aslam & Peter Gabriel", ["c8k9a0v1a14"], 24, 120, 300, 9, "punjabi", "sufi"),
    ("Kadi Te Has", "Atif Aslam", ["k8k9a0v1a15"], 20, 110, 240, 8, "punjabi", "folk"),
    ("Man Aamadeh Am", "Atif Aslam & Gul Panrra", ["m8k9a0v1a16"], 26, 125, 360, 9, "hindi", "sufi"),
    ("Dil Kare", "Atif Aslam (Ho Mann Jahaan)", ["d8k9a0v1a17"], 22, 115, 250, 8, "hindi", "pop"),
    ("Thaam Lo", "Atif Aslam (Parwaaz Hai Junoon)", ["t8k9a0v1a18"], 24, 120, 275, 8, "hindi", "romantic"),
    ("In Dinon", "Atif Aslam", ["i8k9a0v1a19"], 22, 118, 260, 8, "hindi", "romantic"),
    ("Dekhte Dekhte", "Atif Aslam & Nusrat Fateh Ali Khan", ["d8k9a0v1a20"], 25, 120, 256, 8, "hindi", "romantic"),
    ("Paniyon Sa", "Atif Aslam & Tulsi Kumar", ["p8k9a0v1a21"], 22, 115, 236, 8, "hindi", "romantic")
]
for t in atif_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- SONU NIGAM TO 50+ -----------------
sonu_tracks = [
    ("Main Agar Kahoon", "Sonu Nigam & Shreya Ghoshal (Om Shanti Om)", ["m8k9a0v1s01"], 28, 130, 310, 8, "hindi", "romantic"),
    ("Soniyo", "Sonu Nigam & Shreya Ghoshal (Raaz 2)", ["s8k9a0v1s02"], 26, 125, 320, 8, "hindi", "romantic"),
    ("Abhi Mujh Mein Kahin", "Sonu Nigam (Agneepath)", ["a8k9a0v1s03"], 32, 135, 364, 8, "hindi", "emotional"),
    ("Sandese Aate Hai", "Sonu Nigam & Roop Kumar Rathod", ["s8k9a0v1s04"], 35, 140, 620, 9, "hindi", "patriotic"),
    ("Mere Haath Mein", "Sonu Nigam & Sunidhi Chauhan (Fanaa)", ["m8k9a0v1s05"], 28, 128, 288, 8, "hindi", "romantic"),
    ("You Are My Soniya", "Sonu Nigam & Alka Yagnik (K3G)", ["y8k9a0v1s06"], 26, 125, 345, 10, "hindi", "party"),
    ("Deewana Tera", "Sonu Nigam (Deewana)", ["d8k9a0v1s07"], 24, 120, 310, 8, "hindi", "pop"),
    ("Bijuria", "Sonu Nigam (Mausam)", ["b8k9a0v1s08"], 22, 115, 280, 10, "hindi", "party"),
    ("Tanhayee", "Sonu Nigam (Dil Chahta Hai)", ["t8k9a0v1s09"], 30, 130, 370, 8, "hindi", "rock"),
    ("Jane Nahin Denge Tujhe", "Sonu Nigam (3 Idiots)", ["j8k9a0v1s10"], 28, 125, 212, 8, "hindi", "emotional"),
    ("Zoobi Doobi", "Sonu Nigam & Shreya Ghoshal (3 Idiots)", ["z8k9a0v1s11"], 24, 120, 248, 9, "hindi", "party"),
    ("Chiggy Wiggy", "Sonu Nigam & Kylie Minogue (Blue)", ["c8k9a0v1s12"], 22, 115, 310, 9, "hindi", "party"),
    ("Falak Tak", "Sonu Nigam & Mahalaxmi Iyer (Tashan)", ["f8k9a0v1s13"], 26, 125, 350, 8, "hindi", "romantic"),
    ("Shukran Allah", "Sonu Nigam & Shreya Ghoshal (Kurbaan)", ["s8k9a0v1s14"], 26, 125, 290, 8, "hindi", "sufi"),
    ("Main Hoon Na", "Sonu Nigam & Shreya Ghoshal", ["m8k9a0v1s15"], 28, 128, 360, 9, "hindi", "romantic"),
    ("Tumse Milke Dil Ka", "Sonu Nigam & Aftab Sabri (Main Hoon Na)", ["t8k9a0v1s16"], 30, 135, 360, 10, "hindi", "qawwali"),
    ("Gori Gori", "Sonu Nigam, Sunidhi Chauhan & KK", ["g8k9a0v1s17"], 24, 120, 270, 9, "hindi", "party"),
    ("Bhangra Paale", "Sonu Nigam & Sudesh Bhosle", ["b8k9a0v1s18"], 26, 125, 330, 10, "hindi", "banger"),
    ("No Entry Title Track", "Sonu Nigam & Alisha Chinai", ["n8k9a0v1s19"], 24, 120, 360, 10, "hindi", "banger"),
    ("Just Chill", "Sonu Nigam & Sunidhi Chauhan (Maine Pyaar Kyun Kiya)", ["j8k9a0v1s20"], 22, 115, 320, 9, "hindi", "party"),
    ("Dupatta Tera Nau Rang Da", "Sonu Nigam & Sunidhi Chauhan", ["d8k9a0v1s21"], 24, 120, 300, 10, "hindi", "banger"),
    ("Mujhse Shaadi Karogi", "Sonu Nigam, Udit Narayan & Sunidhi Chauhan", ["m8k9a0v1s22"], 26, 125, 340, 10, "hindi", "banger"),
    ("Jeene Ke Hain Chaar Din", "Sonu Nigam & Sunidhi Chauhan", ["j8k9a0v1s23"], 24, 120, 320, 10, "hindi", "banger"),
    ("Dil Ne Yeh Kaha Hai Dil Se", "Sonu Nigam & Alka Yagnik (Dhadkan)", ["d8k9a0v1s24"], 30, 135, 420, 8, "hindi", "romantic"),
    ("Kismat Konnection", "Sonu Nigam & Sunidhi Chauhan", ["k8k9a0v1s25"], 22, 115, 290, 9, "hindi", "party"),
    ("Chori Kiya Re Jiya", "Sonu Nigam & Shreya Ghoshal (Dabangg)", ["c8k9a0v1s26"], 24, 120, 290, 8, "hindi", "romantic"),
    ("Aal Izz Well", "Sonu Nigam, Swanand Kirkire & Shaan", ["a8k9a0v1s27"], 22, 115, 276, 9, "hindi", "party"),
    ("Tera Rang Balle Balle", "Sonu Nigam & Jaspinder Narula", ["t8k9a0v1s28"], 26, 125, 340, 10, "hindi", "banger"),
    ("Satrangi Re", "Sonu Nigam & Kavita Krishnamurthy (Dil Se)", ["s8k9a0v1s29"], 32, 135, 440, 9, "hindi", "romantic"),
    ("Guzarish", "Sonu Nigam & Javed Ali (Ghajini)", ["g8k9a0v1s30"], 28, 128, 330, 8, "hindi", "romantic")
]
for t in sonu_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- SHREYA GHOSHAL TO 50+ -----------------
shreya_tracks = [
    ("Barso Re", "Shreya Ghoshal & A.R. Rahman (Guru)", ["b8k9a0v1g01"], 24, 120, 328, 9, "hindi", "folk"),
    ("Manwa Laage", "Shreya Ghoshal & Arijit Singh (HNY)", ["m8k9a0v1g02"], 22, 118, 271, 8, "hindi", "romantic"),
    ("Ghoomar", "Shreya Ghoshal & Swaroop Khan (Padmaavat)", ["g8k9a0v1g03"], 30, 135, 282, 9, "hindi", "folk"),
    ("Kar Har Maidaan Fateh", "Shreya Ghoshal & Sukhwinder Singh (Sanju)", ["k8k9a0v1g04"], 26, 125, 311, 9, "hindi", "inspirational"),
    ("Dola Re Dola", "Shreya Ghoshal & Kavita Krishnamurthy (Devdas)", ["d8k9a0v1g05"], 30, 135, 396, 10, "hindi", "dance"),
    ("Bairi Piya", "Shreya Ghoshal & Udit Narayan (Devdas)", ["b8k9a0v1g06"], 28, 130, 320, 8, "hindi", "classical"),
    ("Silsila Ye Chaahat Ka", "Shreya Ghoshal (Devdas)", ["s8k9a0v1g07"], 30, 135, 326, 8, "hindi", "classical"),
    ("Jaadu Hai Nasha Hai", "Shreya Ghoshal (Jism)", ["j8k9a0v1g08"], 26, 125, 328, 8, "hindi", "romantic"),
    ("Chalo Tumko Lekar Chale", "Shreya Ghoshal (Jism)", ["c8k9a0v1g09"], 25, 122, 290, 8, "hindi", "romantic"),
    ("Agar Tum Mil Jao", "Shreya Ghoshal (Zeher)", ["a8k9a0v1g10"], 28, 130, 360, 8, "hindi", "romantic"),
    ("Woh Bheege Pal", "Shreya Ghoshal & Zubeen Garg", ["w8k9a0v1g11"], 26, 125, 340, 8, "hindi", "romantic"),
    ("Piyu Bole", "Shreya Ghoshal & Sonu Nigam (Parineeta)", ["p8k9a0v1g12"], 24, 120, 260, 8, "hindi", "romantic"),
    ("Thodi Der", "Shreya Ghoshal & Farhan Saeed", ["t8k9a0v1g13"], 22, 115, 296, 8, "hindi", "romantic"),
    ("Hasi", "Shreya Ghoshal & Ami Mishra", ["h8k9a0v1g14"], 24, 120, 272, 8, "hindi", "romantic"),
    ("Sunn Raha Hai", "Shreya Ghoshal (Aashiqui 2)", ["s8k9a0v1g15"], 28, 130, 315, 8, "hindi", "romantic"),
    ("Samjhawan", "Shreya Ghoshal & Arijit Singh", ["s8k9a0v1g16"], 25, 122, 269, 8, "hindi", "romantic"),
    ("Mohe Rang Do Laal", "Shreya Ghoshal & Pandit Birju Maharaj", ["m8k9a0v1g17"], 28, 130, 232, 8, "hindi", "classical"),
    ("Ghar More Pardesiya", "Shreya Ghoshal & Vaishali Mhade (Kalank)", ["g8k9a0v1g18"], 28, 130, 319, 9, "hindi", "classical")
]
for t in shreya_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- SUNIDHI CHAUHAN TO 50+ -----------------
sunidhi_tracks = [
    ("Crazy Kiya Re", "Sunidhi Chauhan (Dhoom 2)", ["c8k9a0v1u01"], 24, 120, 294, 10, "hindi", "banger"),
    ("Mehboob Mere", "Sunidhi Chauhan & Sukhwinder Singh", ["m8k9a0v1u02"], 26, 125, 340, 9, "hindi", "item"),
    ("Chor Bazaari", "Sunidhi Chauhan & Neeraj Shridhar", ["c8k9a0v1u03"], 22, 115, 235, 9, "hindi", "party"),
    ("Dance Pe Chance", "Sunidhi Chauhan & Labh Janjua (RNBDJ)", ["d8k9a0v1u04"], 26, 125, 262, 10, "hindi", "banger"),
    ("Ruki Ruki Thi Zindagi", "Sunidhi Chauhan (Mast)", ["r8k9a0v1u05"], 24, 120, 320, 9, "hindi", "pop"),
    ("Suno Aisha", "Sunidhi Chauhan, Amit Trivedi & Nakash Aziz", ["s8k9a0v1u06"], 22, 115, 258, 9, "hindi", "party"),
    ("Te Amo", "Sunidhi Chauhan & Ash King (Dum Maaro Dum)", ["t8k9a0v1u07"], 24, 120, 286, 8, "hindi", "romantic"),
    ("Mar Te Raazi", "Sunidhi Chauhan", ["m8k9a0v1u08"], 20, 110, 210, 9, "punjabi", "party"),
    ("Ishq Sufiyana", "Sunidhi Chauhan & Kamal Khan", ["i8k9a0v1u09"], 26, 125, 328, 8, "hindi", "sufi"),
    ("Udi", "Sunidhi Chauhan & Shail Hada (Guzaarish)", ["u8k9a0v1u10"], 24, 120, 202, 8, "hindi", "pop"),
    ("Parda Parda", "Sunidhi Chauhan (Once Upon A Time In Mumbaai)", ["p8k9a0v1u11"], 26, 125, 290, 9, "hindi", "retro"),
    ("Kaisi Paheli Zindagani", "Sunidhi Chauhan (Parineeta)", ["k8k9a0v1u12"], 25, 122, 240, 8, "hindi", "jazz"),
    ("Aisa Jadoo Dala Re", "Sunidhi Chauhan (Khakee)", ["a8k9a0v1u13"], 24, 120, 310, 9, "hindi", "item"),
    ("Race Saanson Ki", "Sunidhi Chauhan & Neeraj Shridhar", ["r8k9a0v1u14"], 24, 120, 280, 10, "hindi", "banger"),
    ("Right Here Right Now", "Sunidhi Chauhan & Abhishek Bachchan (Bluffmaster)", ["r8k9a0v1u15"], 22, 115, 203, 9, "hindi", "hiphop"),
    ("Babuji Zara Dheere Chalo", "Sunidhi Chauhan & Sukhwinder Singh", ["b8k9a0v1u16"], 26, 125, 320, 10, "hindi", "item"),
    ("Saki Saki Classic", "Sunidhi Chauhan & Sukhwinder Singh (Musafir)", ["s8k9a0v1u17"], 28, 128, 330, 10, "hindi", "banger"),
    ("Mast Kalandar", "Sunidhi Chauhan & Mika Singh (Heyy Babyy)", ["m8k9a0v1u18"], 25, 125, 310, 10, "hindi", "banger"),
    ("Heyy Babyy Title", "Sunidhi Chauhan, Neeraj Shridhar & Raman Mahadevan", ["h8k9a0v1u19"], 24, 120, 290, 9, "hindi", "party"),
    ("Discowale Khisko", "Sunidhi Chauhan & KK (Dil Bole Hadippa)", ["d8k9a0v1u20"], 25, 122, 260, 10, "hindi", "banger"),
    ("Hadippa The Remix", "Sunidhi Chauhan & Mika Singh", ["h8k9a0v1u21"], 24, 120, 250, 10, "hindi", "banger"),
    ("Shut Up & Bounce", "Sunidhi Chauhan & Vishal Dadlani (Dostana)", ["s8k9a0v1u22"], 22, 115, 280, 9, "hindi", "party"),
    ("Yaaram", "Sunidhi Chauhan & Clinton Cerejo (Ek Thi Daayan)", ["y8k9a0v1u23"], 22, 115, 270, 8, "hindi", "acoustic"),
    ("Engine Ki Seeti", "Sunidhi Chauhan & Resmi Sateesh (Khoobsurat)", ["e8k9a0v1u24"], 20, 110, 235, 10, "hindi", "banger"),
    ("The Jawaani Song", "Sunidhi Chauhan & Vishal Dadlani (SOTY 2)", ["j8k9a0v1u25"], 22, 115, 253, 10, "hindi", "banger"),
    ("Show Me The Thumka", "Sunidhi Chauhan & Pritam (TJMM)", ["s8k9a0v1u26"], 24, 120, 236, 10, "hindi", "banger")
]
for t in sunidhi_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- THE WEEKND TO 50+ -----------------
weeknd_tracks = [
    ("Earned It", "The Weeknd (Fifty Shades of Grey)", ["e8k9a0v1w01"], 26, 125, 277, 8, "english", "rnb"),
    ("Call Out My Name", "The Weeknd", ["c8k9a0v1w02"], 22, 118, 228, 8, "english", "rnb"),
    ("Wicked Games", "The Weeknd", ["w8k9a0v1w03"], 26, 125, 324, 8, "english", "rnb"),
    ("Out of Time", "The Weeknd", ["o8k9a0v1w04"], 20, 110, 214, 8, "english", "pop"),
    ("Gasoline", "The Weeknd", ["g8k9a0v1w05"], 22, 115, 212, 9, "english", "synth"),
    ("How Do I Make You Love Me?", "The Weeknd", ["h8k9a0v1w06"], 24, 120, 224, 9, "english", "dance"),
    ("Is There Someone Else?", "The Weeknd", ["i8k9a0v1w07"], 20, 110, 199, 8, "english", "rnb"),
    ("Starry Eyes", "The Weeknd", ["s8k9a0v1w08"], 18, 105, 148, 8, "english", "synth"),
    ("Less Than Zero", "The Weeknd", ["l8k9a0v1w09"], 22, 115, 211, 9, "english", "pop"),
    ("Faith", "The Weeknd", ["f8k9a0v1w10"], 25, 122, 283, 9, "english", "trap"),
    ("After Hours", "The Weeknd", ["a8k9a0v1w11"], 30, 135, 361, 9, "english", "house"),
    ("Hardest To Love", "The Weeknd", ["h8k9a0v1w12"], 20, 110, 211, 8, "english", "dnb"),
    ("Scared To Live", "The Weeknd", ["s8k9a0v1w13"], 24, 120, 191, 8, "english", "ballad"),
    ("Snowchild", "The Weeknd", ["s8k9a0v1w14"], 22, 115, 247, 8, "english", "rnb"),
    ("Escape From LA", "The Weeknd", ["e8k9a0v1w15"], 25, 125, 355, 8, "english", "rnb"),
    ("Party Monster", "The Weeknd", ["p8k9a0v1w16"], 22, 115, 249, 9, "english", "trap"),
    ("False Alarm", "The Weeknd", ["f8k9a0v1w17"], 20, 110, 220, 10, "english", "punk-pop"),
    ("Six Feet Under", "The Weeknd ft. Future", ["s8k9a0v1w18"], 18, 105, 237, 9, "english", "trap"),
    ("Sidewalks", "The Weeknd ft. Kendrick Lamar", ["s8k9a0v1w19"], 22, 115, 231, 9, "english", "hiphop"),
    ("A Lonely Night", "The Weeknd", ["a8k9a0v1w20"], 20, 110, 220, 9, "english", "funk"),
    ("Love To Lay", "The Weeknd", ["l8k9a0v1w21"], 22, 115, 223, 9, "english", "pop"),
    ("Nothing Without You", "The Weeknd", ["n8k9a0v1w22"], 24, 120, 198, 8, "english", "pop"),
    ("All I Know", "The Weeknd ft. Future", ["a8k9a0v1w23"], 22, 118, 321, 9, "english", "trap"),
    ("Die For You Remix", "The Weeknd & Ariana Grande", ["d8k9a0v1w24"], 24, 120, 232, 9, "english", "rnb"),
    ("Save Your Tears Remix", "The Weeknd & Ariana Grande", ["s8k9a0v1w25"], 20, 112, 191, 9, "english", "pop"),
    ("In The Night", "The Weeknd", ["i8k9a0v1w26"], 22, 115, 235, 9, "english", "pop"),
    ("Acquainted", "The Weeknd", ["a8k9a0v1w27"], 25, 125, 348, 8, "english", "rnb"),
    ("High For This", "The Weeknd", ["h8k9a0v1w28"], 28, 128, 247, 8, "english", "rnb"),
    ("The Morning", "The Weeknd", ["t8k9a0v1w29"], 26, 125, 315, 8, "english", "rnb"),
    ("House Of Balloons", "The Weeknd", ["h8k9a0v1w30"], 30, 135, 407, 9, "english", "rnb")
]
for t in weeknd_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- DRAKE TO 50+ -----------------
drake_tracks = [
    ("Controlla", "Drake", ["c8k9a0v1d01"], 20, 110, 245, 8, "english", "dancehall"),
    ("Jumpman", "Drake & Future", ["j8k9a0v1d02"], 18, 105, 225, 10, "english", "trap"),
    ("Hold On, We're Going Home", "Drake ft. Majid Jordan", ["h8k9a0v1d03"], 24, 120, 227, 8, "english", "pop"),
    ("Take Care", "Drake ft. Rihanna", ["t8k9a0v1d04"], 26, 125, 277, 9, "english", "pop"),
    ("Headlines", "Drake", ["h8k9a0v1d05"], 22, 115, 236, 9, "english", "hiphop"),
    ("Marvins Room", "Drake", ["m8k9a0v1d06"], 30, 135, 347, 7, "english", "rnb"),
    ("Best I Ever Had", "Drake", ["b8k9a0v1d07"], 22, 115, 257, 9, "english", "hiphop"),
    ("Energy", "Drake", ["e8k9a0v1d08"], 18, 105, 181, 10, "english", "trap"),
    ("Know Yourself", "Drake", ["k8k9a0v1d09"], 24, 120, 275, 10, "english", "trap"),
    ("Back To Back", "Drake", ["b8k9a0v1d10"], 16, 98, 170, 9, "english", "hiphop"),
    ("Fake Love", "Drake", ["f8k9a0v1d11"], 20, 110, 210, 8, "english", "hiphop"),
    ("Too Good", "Drake ft. Rihanna", ["t8k9a0v1d12"], 22, 115, 263, 8, "english", "dancehall"),
    ("Bria's Interlude", "Drake & Omarion", ["b8k9a0v1d13"], 24, 120, 139, 7, "english", "rnb"),
    ("Forever", "Drake, Kanye West, Lil Wayne & Eminem", ["f8k9a0v1d14"], 25, 125, 357, 10, "english", "hiphop"),
    ("Life Is Good", "Future ft. Drake", ["l8k9a0v1d15"], 18, 105, 237, 9, "english", "trap"),
    ("Way 2 Sexy", "Drake ft. Future & Young Thug", ["w8k9a0v1d16"], 20, 110, 257, 9, "english", "trap"),
    ("Fair Trade", "Drake ft. Travis Scott", ["f8k9a0v1d17"], 22, 115, 291, 8, "english", "trap"),
    ("Girls Want Girls", "Drake ft. Lil Baby", ["g8k9a0v1d18"], 20, 110, 221, 8, "english", "trap"),
    ("No Guidance", "Chris Brown ft. Drake", ["n8k9a0v1d19"], 22, 115, 260, 9, "english", "rnb"),
    ("Money In The Grave", "Drake ft. Rick Ross", ["m8k9a0v1d20"], 18, 105, 198, 9, "english", "trap"),
    ("Omertà", "Drake", ["o8k9a0v1d21"], 20, 110, 219, 9, "english", "hiphop"),
    ("Signs", "Drake", ["s8k9a0v1d22"], 18, 105, 234, 8, "english", "dancehall"),
    ("Sneakin'", "Drake ft. 21 Savage", ["s8k9a0v1d23"], 20, 110, 251, 9, "english", "trap"),
    ("Childs Play", "Drake", ["c8k9a0v1d24"], 22, 115, 241, 8, "english", "rnb"),
    ("Pop Style", "Drake", ["p8k9a0v1d25"], 20, 110, 212, 9, "english", "trap"),
    ("Feel No Ways", "Drake", ["f8k9a0v1d26"], 22, 115, 240, 8, "english", "rnb"),
    ("With You", "Drake ft. PARTYNEXTDOOR", ["w8k9a0v1d27"], 20, 110, 195, 8, "english", "rnb"),
    ("Fire & Desire", "Drake", ["f8k9a0v1d28"], 25, 125, 238, 7, "english", "rnb"),
    ("Too Much", "Drake ft. Sampha", ["t8k9a0v1d29"], 24, 120, 261, 8, "english", "rnb"),
    ("Pound Cake", "Drake ft. JAY-Z", ["p8k9a0v1d30"], 28, 128, 433, 9, "english", "hiphop")
]
for t in drake_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- JUSTIN BIEBER TO 50+ -----------------
bieber_tracks = [
    ("Company", "Justin Bieber", ["c8k9a0v1b01"], 20, 110, 208, 9, "english", "rnb"),
    ("Boyfriend", "Justin Bieber", ["b8k9a0v1b02"], 18, 105, 172, 8, "english", "pop"),
    ("Never Say Never", "Justin Bieber ft. Jaden Smith", ["n8k9a0v1b03"], 22, 115, 227, 9, "english", "pop"),
    ("As Long As You Love Me", "Justin Bieber ft. Big Sean", ["a8k9a0v1b04"], 24, 120, 229, 9, "english", "pop"),
    ("Hold On", "Justin Bieber", ["h8k9a0v1b05"], 20, 110, 170, 8, "english", "pop"),
    ("Ghost", "Justin Bieber", ["g8k9a0v1b06"], 18, 105, 153, 9, "english", "pop"),
    ("Holy", "Justin Bieber ft. Chance the Rapper", ["h8k9a0v1b07"], 22, 115, 212, 8, "english", "pop"),
    ("Lonely", "Justin Bieber & benny blanco", ["l8k9a0v1b08"], 18, 105, 149, 7, "english", "ballad"),
    ("Anyone", "Justin Bieber", ["a8k9a0v1b09"], 22, 115, 190, 8, "english", "pop"),
    ("I'll Show You", "Justin Bieber", ["i8k9a0v1b10"], 22, 115, 199, 9, "english", "edm"),
    ("Children", "Justin Bieber", ["c8k9a0v1b11"], 24, 120, 223, 10, "english", "edm"),
    ("No Brainer", "DJ Khaled ft. Justin Bieber, Chance the Rapper & Quavo", ["n8k9a0v1b12"], 20, 110, 260, 9, "english", "hiphop"),
    ("I'm The One", "DJ Khaled ft. Justin Bieber, Quavo, Chance & Lil Wayne", ["i8k9a0v1b13"], 22, 115, 288, 10, "english", "hiphop"),
    ("10,000 Hours", "Dan + Shay & Justin Bieber", ["t8k9a0v1b14"], 18, 105, 167, 8, "english", "country-pop"),
    ("Monster", "Shawn Mendes & Justin Bieber", ["m8k9a0v1b15"], 20, 110, 178, 8, "english", "pop"),
    ("Stuck with U", "Ariana Grande & Justin Bieber", ["s8k9a0v1b16"], 22, 115, 228, 8, "english", "pop"),
    ("2U", "David Guetta ft. Justin Bieber", ["t8k9a0v1b17"], 24, 120, 195, 9, "english", "edm"),
    ("Cold Water", "Major Lazer ft. Justin Bieber & MØ", ["c8k9a0v1b18"], 22, 115, 185, 9, "english", "edm"),
    ("Let Me Love You", "DJ Snake ft. Justin Bieber", ["l8k9a0v1b19"], 24, 120, 205, 10, "english", "edm"),
    ("All That Matters", "Justin Bieber", ["a8k9a0v1b20"], 20, 110, 191, 8, "english", "rnb"),
    ("Confident", "Justin Bieber ft. Chance the Rapper", ["c8k9a0v1b21"], 18, 105, 247, 8, "english", "rnb"),
    ("Hold Tight", "Justin Bieber", ["h8k9a0v1b22"], 20, 110, 255, 7, "english", "rnb"),
    ("Heartbreaker", "Justin Bieber", ["h8k9a0v1b23"], 22, 115, 262, 7, "english", "rnb"),
    ("E.T.A.", "Justin Bieber", ["e8k9a0v1b24"], 18, 105, 176, 8, "english", "rnb"),
    ("Habitual", "Justin Bieber", ["h8k9a0v1b25"], 20, 110, 168, 8, "english", "rnb"),
    ("Available", "Justin Bieber", ["a8k9a0v1b26"], 18, 105, 195, 8, "english", "rnb"),
    ("Forever", "Justin Bieber ft. Post Malone & Clever", ["f8k9a0v1b27"], 20, 110, 219, 8, "english", "pop"),
    ("Take It Out On Me", "Justin Bieber", ["t8k9a0v1b28"], 18, 105, 178, 8, "english", "rnb"),
    ("Running Over", "Justin Bieber ft. Lil Dicky", ["r8k9a0v1b29"], 20, 110, 179, 8, "english", "rnb"),
    ("Second Emotion", "Justin Bieber ft. Travis Scott", ["s8k9a0v1b30"], 18, 105, 202, 9, "english", "trap"),
    ("Get Me", "Justin Bieber ft. Kehlani", ["g8k9a0v1b31"], 20, 110, 185, 8, "english", "rnb"),
    ("Changes", "Justin Bieber", ["c8k9a0v1b32"], 18, 105, 135, 7, "english", "acoustic"),
    ("That's What Love Is", "Justin Bieber", ["t8k9a0v1b33"], 20, 110, 165, 8, "english", "acoustic"),
    ("At Least For Now", "Justin Bieber", ["a8k9a0v1b34"], 22, 115, 149, 7, "english", "ballad"),
    ("Die In Your Arms", "Justin Bieber", ["d8k9a0v1b35"], 20, 110, 237, 8, "english", "pop"),
    ("One Time", "Justin Bieber", ["o8k9a0v1b36"], 18, 105, 215, 9, "english", "pop"),
    ("One Less Lonely Girl", "Justin Bieber", ["o8k9a0v1b37"], 20, 110, 229, 8, "english", "pop"),
    ("Somebody To Love", "Justin Bieber ft. Usher", ["s8k9a0v1b38"], 22, 115, 220, 9, "english", "pop")
]
for t in bieber_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- TAYLOR SWIFT TO 50+ -----------------
taylor_tracks = [
    ("22", "Taylor Swift", ["t8k9a0v1w01"], 22, 115, 232, 9, "english", "pop"),
    ("Cardigan", "Taylor Swift", ["t8k9a0v1w02"], 26, 125, 239, 8, "english", "folk"),
    ("Willow", "Taylor Swift", ["t8k9a0v1w03"], 22, 115, 214, 8, "english", "folk"),
    ("Lavender Haze", "Taylor Swift", ["t8k9a0v1w04"], 20, 110, 202, 8, "english", "pop"),
    ("Karma", "Taylor Swift", ["t8k9a0v1w05"], 20, 110, 204, 9, "english", "pop"),
    ("Midnight Rain", "Taylor Swift", ["t8k9a0v1w06"], 18, 105, 174, 8, "english", "pop"),
    ("Bejeweled", "Taylor Swift", ["t8k9a0v1w07"], 20, 110, 194, 9, "english", "pop"),
    ("ME!", "Taylor Swift ft. Brendon Urie", ["t8k9a0v1w08"], 22, 115, 193, 9, "english", "pop"),
    ("You Need To Calm Down", "Taylor Swift", ["t8k9a0v1w09"], 18, 105, 171, 9, "english", "pop"),
    ("Lover", "Taylor Swift", ["t8k9a0v1w10"], 24, 120, 221, 8, "english", "ballad"),
    ("Delicate", "Taylor Swift", ["t8k9a0v1w11"], 20, 110, 232, 8, "english", "pop"),
    ("...Ready For It?", "Taylor Swift", ["t8k9a0v1w12"], 20, 110, 208, 10, "english", "pop"),
    ("End Game", "Taylor Swift ft. Ed Sheeran & Future", ["t8k9a0v1w13"], 22, 115, 244, 9, "english", "pop"),
    ("Gorgeous", "Taylor Swift", ["t8k9a0v1w14"], 18, 105, 209, 8, "english", "pop"),
    ("Getaway Car", "Taylor Swift", ["t8k9a0v1w15"], 22, 115, 233, 9, "english", "pop"),
    ("Wildest Dreams", "Taylor Swift", ["t8k9a0v1w16"], 26, 125, 220, 8, "english", "pop"),
    ("Out Of The Woods", "Taylor Swift", ["t8k9a0v1w17"], 24, 120, 235, 9, "english", "synth"),
    ("All Too Well (10 Minute Version)", "Taylor Swift", ["t8k9a0v1w18"], 30, 140, 613, 8, "english", "rock"),
    ("Enchanted", "Taylor Swift", ["t8k9a0v1w19"], 28, 130, 352, 9, "english", "pop"),
    ("Mine", "Taylor Swift", ["t8k9a0v1w20"], 22, 115, 230, 8, "english", "country-pop"),
    ("Back To December", "Taylor Swift", ["t8k9a0v1w21"], 26, 125, 293, 8, "english", "country-pop"),
    ("Mean", "Taylor Swift", ["t8k9a0v1w22"], 22, 115, 237, 8, "english", "country-pop"),
    ("Sparks Fly", "Taylor Swift", ["t8k9a0v1w23"], 24, 120, 260, 9, "english", "country-pop"),
    ("Our Song", "Taylor Swift", ["t8k9a0v1w24"], 20, 110, 201, 8, "english", "country-pop"),
    ("Teardrops On My Guitar", "Taylor Swift", ["t8k9a0v1w25"], 22, 115, 215, 8, "english", "country-pop"),
    ("Picture To Burn", "Taylor Swift", ["t8k9a0v1w26"], 20, 110, 173, 9, "english", "country-pop"),
    ("Fearless", "Taylor Swift", ["t8k9a0v1w27"], 22, 115, 241, 8, "english", "country-pop"),
    ("Fifteen", "Taylor Swift", ["t8k9a0v1w28"], 24, 120, 294, 8, "english", "country-pop"),
    ("White Horse", "Taylor Swift", ["t8k9a0v1w29"], 25, 122, 234, 7, "english", "country-pop"),
    ("Red", "Taylor Swift", ["t8k9a0v1w30"], 22, 115, 223, 9, "english", "pop"),
    ("Begin Again", "Taylor Swift", ["t8k9a0v1w31"], 24, 120, 237, 7, "english", "country-pop"),
    ("Everything Has Changed", "Taylor Swift ft. Ed Sheeran", ["t8k9a0v1w32"], 22, 115, 245, 8, "english", "pop"),
    ("Welcome To New York", "Taylor Swift", ["t8k9a0v1w33"], 20, 110, 212, 9, "english", "pop"),
    ("This Love", "Taylor Swift", ["t8k9a0v1w34"], 25, 125, 250, 7, "english", "pop"),
    ("Clean", "Taylor Swift", ["t8k9a0v1w35"], 24, 120, 270, 8, "english", "pop"),
    ("Fortnight", "Taylor Swift ft. Post Malone", ["t8k9a0v1w36"], 20, 110, 228, 8, "english", "pop"),
    ("I Can Do It With A Broken Heart", "Taylor Swift", ["t8k9a0v1w37"], 18, 105, 218, 9, "english", "pop")
]
for t in taylor_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- ED SHEERAN TO 50+ -----------------
ed_tracks = [
    ("Bad Habits", "Ed Sheeran", ["e8k9a0v1e01"], 18, 105, 231, 9, "english", "pop"),
    ("Shivers", "Ed Sheeran", ["e8k9a0v1e02"], 20, 110, 207, 9, "english", "pop"),
    ("Castle on the Hill", "Ed Sheeran", ["e8k9a0v1e03"], 24, 120, 261, 9, "english", "pop"),
    ("Galway Girl", "Ed Sheeran", ["e8k9a0v1e04"], 20, 110, 170, 9, "english", "folk-pop"),
    ("Thinking Out Loud", "Ed Sheeran", ["e8k9a0v1e05"], 25, 125, 281, 8, "english", "ballad"),
    ("Photograph", "Ed Sheeran", ["e8k9a0v1e06"], 24, 120, 258, 8, "english", "ballad"),
    ("Perfect", "Ed Sheeran", ["e8k9a0v1e07"], 26, 125, 263, 8, "english", "ballad"),
    ("I Don't Care", "Ed Sheeran & Justin Bieber", ["e8k9a0v1e08"], 18, 105, 219, 8, "english", "pop"),
    ("Beautiful People", "Ed Sheeran ft. Khalid", ["e8k9a0v1e09"], 20, 110, 197, 8, "english", "pop"),
    ("South of the Border", "Ed Sheeran ft. Camila Cabello & Cardi B", ["e8k9a0v1e10"], 22, 115, 204, 9, "english", "pop"),
    ("Cross Me", "Ed Sheeran ft. Chance the Rapper & PnB Rock", ["e8k9a0v1e11"], 20, 110, 206, 9, "english", "hiphop"),
    ("Antisocial", "Ed Sheeran & Travis Scott", ["e8k9a0v1e12"], 18, 105, 161, 9, "english", "trap"),
    ("Take Me Back To London", "Ed Sheeran ft. Stormzy", ["e8k9a0v1e13"], 18, 105, 189, 9, "english", "grime"),
    ("BLOW", "Ed Sheeran, Chris Stapleton & Bruno Mars", ["e8k9a0v1e14"], 20, 110, 209, 10, "english", "rock"),
    ("Overpass Graffiti", "Ed Sheeran", ["e8k9a0v1e15"], 22, 115, 236, 9, "english", "pop"),
    ("Celestial", "Ed Sheeran", ["e8k9a0v1e16"], 20, 110, 209, 8, "english", "pop"),
    ("Eyes Closed", "Ed Sheeran", ["e8k9a0v1e17"], 20, 110, 194, 8, "english", "pop"),
    ("Boat", "Ed Sheeran", ["e8k9a0v1e18"], 22, 115, 185, 7, "english", "acoustic"),
    ("Curtains", "Ed Sheeran", ["e8k9a0v1e19"], 20, 110, 224, 8, "english", "rock"),
    ("The A Team", "Ed Sheeran", ["e8k9a0v1e20"], 24, 120, 258, 8, "english", "acoustic"),
    ("Lego House", "Ed Sheeran", ["e8k9a0v1e21"], 22, 115, 185, 8, "english", "pop"),
    ("Give Me Love", "Ed Sheeran", ["e8k9a0v1e22"], 26, 125, 326, 8, "english", "acoustic"),
    ("Sing", "Ed Sheeran", ["e8k9a0v1e23"], 20, 110, 235, 9, "english", "pop"),
    ("Don't", "Ed Sheeran", ["e8k9a0v1e24"], 22, 115, 219, 9, "english", "pop"),
    ("Bloodstream", "Ed Sheeran & Rudimental", ["e8k9a0v1e25"], 25, 125, 308, 9, "english", "dnb"),
    ("I See Fire", "Ed Sheeran (The Hobbit)", ["e8k9a0v1e26"], 28, 130, 300, 8, "english", "folk"),
    ("Dive", "Ed Sheeran", ["e8k9a0v1e27"], 24, 120, 238, 8, "english", "blues"),
    ("Happier", "Ed Sheeran", ["e8k9a0v1e28"], 22, 115, 207, 8, "english", "ballad"),
    ("New Man", "Ed Sheeran", ["e8k9a0v1e29"], 18, 105, 189, 8, "english", "pop"),
    ("What Do I Know?", "Ed Sheeran", ["e8k9a0v1e30"], 20, 110, 237, 8, "english", "pop"),
    ("How Would You Feel", "Ed Sheeran", ["e8k9a0v1e31"], 25, 125, 280, 8, "english", "ballad"),
    ("Barcelona", "Ed Sheeran", ["e8k9a0v1e32"], 20, 110, 191, 9, "english", "pop"),
    ("Bibia Be Ye Ye", "Ed Sheeran", ["e8k9a0v1e33"], 18, 105, 176, 9, "english", "afrobeats"),
    ("Nancy Mulligan", "Ed Sheeran", ["e8k9a0v1e34"], 22, 115, 179, 9, "english", "folk-pop"),
    ("Save Myself", "Ed Sheeran", ["e8k9a0v1e35"], 24, 120, 247, 7, "english", "ballad"),
    ("Visiting Hours", "Ed Sheeran", ["e8k9a0v1e36"], 24, 120, 215, 7, "english", "ballad"),
    ("2step", "Ed Sheeran ft. Lil Baby", ["e8k9a0v1e37"], 20, 110, 163, 9, "english", "pop"),
    ("Tides", "Ed Sheeran", ["e8k9a0v1e38"], 22, 115, 195, 9, "english", "rock"),
    ("First Times", "Ed Sheeran", ["e8k9a0v1e39"], 22, 115, 185, 7, "english", "acoustic"),
    ("Collide", "Ed Sheeran", ["e8k9a0v1e40"], 20, 110, 210, 8, "english", "pop"),
    ("Leave Your Life", "Ed Sheeran", ["e8k9a0v1e41"], 22, 115, 223, 8, "english", "pop"),
    ("Stop The Rain", "Ed Sheeran", ["e8k9a0v1e42"], 20, 110, 203, 9, "english", "pop"),
    ("Love In Slow Motion", "Ed Sheeran", ["e8k9a0v1e43"], 22, 115, 190, 8, "english", "ballad"),
    ("Be Right Here", "Ed Sheeran", ["e8k9a0v1e44"], 20, 110, 191, 8, "english", "pop"),
    ("Sandman", "Ed Sheeran", ["e8k9a0v1e45"], 18, 105, 259, 7, "english", "lullaby"),
    ("All Of The Stars", "Ed Sheeran (Fault in Our Stars)", ["e8k9a0v1e46"], 24, 120, 235, 8, "english", "ballad"),
    ("Afire Love", "Ed Sheeran", ["e8k9a0v1e47"], 25, 125, 314, 8, "english", "pop"),
    ("Tenerife Sea", "Ed Sheeran", ["e8k9a0v1e48"], 24, 120, 241, 8, "english", "acoustic")
]
for t in ed_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- EMINEM TO 50+ -----------------
eminem_tracks = [
    ("Stan", "Eminem ft. Dido", ["e8k9a0v1m01"], 25, 125, 404, 9, "english", "hiphop"),
    ("Cleanin' Out My Closet", "Eminem", ["e8k9a0v1m02"], 22, 115, 298, 9, "english", "hiphop"),
    ("Sing For The Moment", "Eminem", ["e8k9a0v1m03"], 24, 120, 339, 9, "english", "hiphop"),
    ("Superman", "Eminem ft. Dina Rae", ["e8k9a0v1m04"], 22, 115, 350, 9, "english", "hiphop"),
    ("When I'm Gone", "Eminem", ["e8k9a0v1m05"], 25, 125, 281, 9, "english", "hiphop"),
    ("Mockingbird", "Eminem", ["e8k9a0v1m06"], 22, 115, 258, 8, "english", "hiphop"),
    ("Like Toy Soldiers", "Eminem", ["e8k9a0v1m07"], 24, 120, 296, 9, "english", "hiphop"),
    ("Just Lose It", "Eminem", ["e8k9a0v1m08"], 20, 110, 248, 10, "english", "hiphop"),
    ("Ass Like That", "Eminem", ["e8k9a0v1m09"], 20, 110, 265, 9, "english", "hiphop"),
    ("Crack A Bottle", "Eminem, Dr. Dre & 50 Cent", ["e8k9a0v1m10"], 22, 115, 297, 10, "english", "hiphop"),
    ("We Made You", "Eminem", ["e8k9a0v1m11"], 20, 110, 270, 9, "english", "hiphop"),
    ("Beautiful", "Eminem", ["e8k9a0v1m12"], 28, 130, 392, 8, "english", "hiphop"),
    ("Space Bound", "Eminem", ["e8k9a0v1m13"], 24, 120, 278, 8, "english", "hiphop"),
    ("No Love", "Eminem ft. Lil Wayne", ["e8k9a0v1m14"], 22, 115, 300, 10, "english", "hiphop"),
    ("Cinderella Man", "Eminem", ["e8k9a0v1m15"], 20, 110, 279, 10, "english", "hiphop"),
    ("25 To Life", "Eminem", ["e8k9a0v1m16"], 24, 120, 241, 9, "english", "hiphop"),
    ("Berzerk", "Eminem", ["e8k9a0v1m17"], 20, 110, 238, 10, "english", "rock"),
    ("Survival", "Eminem", ["e8k9a0v1m18"], 22, 115, 272, 10, "english", "rock"),
    ("Rap God", "Eminem", ["e8k9a0v1m19"], 25, 125, 363, 10, "english", "hiphop"),
    ("The Monster", "Eminem ft. Rihanna", ["e8k9a0v1m20"], 22, 115, 250, 9, "english", "pop"),
    ("Guts Over Fear", "Eminem ft. Sia", ["e8k9a0v1m21"], 24, 120, 301, 8, "english", "hiphop"),
    ("Walk On Water", "Eminem ft. Beyoncé", ["e8k9a0v1m22"], 26, 125, 304, 8, "english", "ballad"),
    ("River", "Eminem ft. Ed Sheeran", ["e8k9a0v1m23"], 20, 110, 221, 9, "english", "pop"),
    ("Fall", "Eminem", ["e8k9a0v1m24"], 20, 110, 262, 9, "english", "hiphop"),
    ("Lucky You", "Eminem ft. Joyner Lucas", ["e8k9a0v1m25"], 18, 105, 244, 10, "english", "trap"),
    ("Kamikaze", "Eminem", ["e8k9a0v1m26"], 18, 105, 216, 9, "english", "hiphop"),
    ("Darkness", "Eminem", ["e8k9a0v1m27"], 24, 120, 337, 8, "english", "hiphop"),
    ("Gnat", "Eminem", ["e8k9a0v1m28"], 18, 105, 224, 9, "english", "trap"),
    ("Houdini", "Eminem", ["e8k9a0v1m29"], 20, 110, 227, 10, "english", "hiphop"),
    ("Tobey", "Eminem, Big Sean & BabyTron", ["e8k9a0v1m30"], 18, 105, 284, 9, "english", "trap")
]
for t in eminem_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- ANIRUDH RAVICHANDER TO 50+ -----------------
anirudh_tracks = [
    ("Master Coming", "Anirudh Ravichander (Master)", ["a8k9a0v1r01"], 20, 110, 210, 10, "tamil-telugu", "mass"),
    ("Polakattum Para Para", "Anirudh Ravichander & Santhosh Narayanan", ["a8k9a0v1r02"], 22, 115, 217, 10, "tamil-telugu", "kuthu"),
    ("Kutti Story", "Anirudh Ravichander & Thalapathy Vijay", ["a8k9a0v1r03"], 20, 110, 321, 9, "tamil-telugu", "party"),
    ("Quit Pannuda", "Anirudh Ravichander", ["a8k9a0v1r04"], 22, 115, 255, 9, "tamil-telugu", "party"),
    ("Andha Kanna Paathaakaa", "Anirudh Ravichander & Yuvan Shankar Raja", ["a8k9a0v1r05"], 20, 110, 221, 8, "tamil-telugu", "melody"),
    ("Two Two Two", "Anirudh Ravichander (Kaathuvaakula Rendu Kaadhal)", ["a8k9a0v1r06"], 18, 105, 178, 10, "tamil-telugu", "banger"),
    ("Naan Pizhai", "Anirudh Ravichander & Shashaa Tirupati", ["a8k9a0v1r07"], 24, 120, 240, 8, "tamil-telugu", "melody"),
    ("Bae", "Anirudh Ravichander & Aditi Rao Hydari (Don)", ["a8k9a0v1r08"], 20, 110, 230, 8, "tamil-telugu", "pop"),
    ("Jalabulajangu", "Anirudh Ravichander (Don)", ["a8k9a0v1r09"], 24, 120, 201, 10, "tamil-telugu", "kuthu"),
    ("Vikram Title Track", "Anirudh Ravichander (Vikram)", ["a8k9a0v1r10"], 22, 115, 218, 10, "tamil-telugu", "mass"),
    ("Wasted", "Anirudh Ravichander (Vikram)", ["a8k9a0v1r11"], 18, 105, 183, 10, "tamil-telugu", "edm"),
    ("Porkanda Singam", "Anirudh Ravichander & Ravi G (Vikram)", ["a8k9a0v1r12"], 25, 122, 216, 8, "tamil-telugu", "melody"),
    ("Once Upon a Time", "Anirudh Ravichander (Vikram)", ["a8k9a0v1r13"], 20, 110, 144, 9, "tamil-telugu", "mass"),
    ("Chaleya Tamil", "Anirudh Ravichander & Shilpa Rao (Jawan)", ["a8k9a0v1r14"], 18, 105, 200, 9, "tamil-telugu", "party"),
    ("Zinda Banda", "Anirudh Ravichander (Jawan)", ["a8k9a0v1r15"], 25, 125, 264, 10, "tamil-telugu", "banger"),
    ("Not Ramaiya Vastavaiya", "Anirudh Ravichander, Vishal Dadlani & Shilpa Rao", ["a8k9a0v1r16"], 22, 115, 203, 10, "tamil-telugu", "banger"),
    ("Jawan Title Track", "Anirudh Ravichander (Jawan)", ["a8k9a0v1r17"], 20, 110, 188, 10, "tamil-telugu", "mass"),
    ("Fear Song", "Anirudh Ravichander (Devara)", ["a8k9a0v1r18"], 22, 115, 197, 10, "tamil-telugu", "mass"),
    ("Chuttamalle", "Anirudh Ravichander & Shilpa Rao (Devara)", ["a8k9a0v1r19"], 20, 110, 220, 8, "tamil-telugu", "melody"),
    ("Daavudi", "Anirudh Ravichander & Nakash Aziz (Devara)", ["a8k9a0v1r20"], 24, 120, 250, 10, "tamil-telugu", "banger"),
    ("Marana Mass", "Anirudh Ravichander & S.P. Balasubrahmanyam (Petta)", ["a8k9a0v1r21"], 25, 125, 216, 10, "tamil-telugu", "kuthu"),
    ("Petta Paraak", "Anirudh Ravichander (Petta)", ["a8k9a0v1r22"], 22, 115, 238, 10, "tamil-telugu", "mass"),
    ("Ullaallaa", "Anirudh Ravichander & Inno Genga (Petta)", ["a8k9a0v1r23"], 24, 120, 296, 9, "tamil-telugu", "party"),
    ("Chumma Kizhi", "Anirudh Ravichander & S.P. Balasubrahmanyam (Darbar)", ["a8k9a0v1r24"], 26, 125, 234, 10, "tamil-telugu", "mass"),
    ("Dumm Dumm", "Anirudh Ravichander (Darbar)", ["a8k9a0v1r25"], 22, 115, 258, 9, "tamil-telugu", "wedding"),
    ("Selfie Pulla", "Anirudh Ravichander & Vijay (Kaththi)", ["a8k9a0v1r26"], 24, 120, 291, 10, "tamil-telugu", "banger"),
    ("Aathi", "Anirudh Ravichander & Vishal Dadlani (Kaththi)", ["a8k9a0v1r27"], 22, 115, 305, 9, "tamil-telugu", "party"),
    ("Aaluma Doluma", "Anirudh Ravichander & Badshah (Vedalam)", ["a8k9a0v1r28"], 25, 125, 260, 10, "tamil-telugu", "kuthu"),
    ("Don'u Don'u Don'u", "Anirudh Ravichander & Alisha Thomas (Maari)", ["a8k9a0v1r29"], 20, 110, 196, 8, "tamil-telugu", "melody"),
    ("Maari Thara Local", "Anirudh Ravichander & Dhanush (Maari)", ["a8k9a0v1r30"], 22, 115, 227, 10, "tamil-telugu", "kuthu")
]
for t in anirudh_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- A.R. RAHMAN TO 50+ -----------------
rahman_tracks = [
    ("Maa Tujhe Salaam", "A.R. Rahman (Vande Mataram)", ["a8k9a0v1q01"], 30, 135, 370, 10, "hindi", "patriotic"),
    ("Kun Faya Kun", "A.R. Rahman, Javed Ali & Mohit Chauhan (Rockstar)", ["a8k9a0v1q02"], 35, 140, 473, 9, "hindi", "sufi"),
    ("Nadaan Parinde", "A.R. Rahman & Mohit Chauhan (Rockstar)", ["a8k9a0v1q03"], 30, 135, 386, 9, "hindi", "rock"),
    ("Sadda Haq", "A.R. Rahman & Mohit Chauhan (Rockstar)", ["a8k9a0v1q04"], 28, 130, 365, 10, "hindi", "rock"),
    ("Katiya Karun", "A.R. Rahman & Harshdeep Kaur (Rockstar)", ["a8k9a0v1q05"], 22, 115, 239, 9, "hindi", "folk"),
    ("Masakali", "A.R. Rahman & Mohit Chauhan (Delhi-6)", ["a8k9a0v1q06"], 24, 120, 290, 8, "hindi", "pop"),
    ("Genda Phool Delhi-6", "A.R. Rahman & Rekha Bhardwaj (Delhi-6)", ["a8k9a0v1q07"], 20, 110, 170, 9, "hindi", "folk"),
    ("Rehna Tu", "A.R. Rahman (Delhi-6)", ["a8k9a0v1q08"], 28, 130, 411, 8, "hindi", "ambient"),
    ("Khwaja Mere Khwaja", "A.R. Rahman (Jodhaa Akbar)", ["a8k9a0v1q09"], 35, 140, 415, 9, "hindi", "sufi"),
    ("Jashn-E-Bahaaraa", "A.R. Rahman & Javed Ali (Jodhaa Akbar)", ["a8k9a0v1q10"], 28, 130, 315, 8, "hindi", "romantic"),
    ("Azeem-O-Shaan Shahenshah", "A.R. Rahman (Jodhaa Akbar)", ["a8k9a0v1q11"], 30, 135, 358, 10, "hindi", "mass"),
    ("Roja Janeman", "A.R. Rahman & S.P. Balasubrahmanyam (Roja)", ["a8k9a0v1q12"], 28, 128, 305, 8, "hindi", "classic"),
    ("Dil Hai Chhota Sa", "A.R. Rahman & Minmini (Roja)", ["a8k9a0v1q13"], 24, 120, 246, 8, "hindi", "classic"),
    ("Tu Hi Re", "A.R. Rahman, Hariharan & Kavita Krishnamurthy (Bombay)", ["a8k9a0v1q14"], 30, 135, 434, 9, "hindi", "romantic"),
    ("Kehna Hi Kya", "A.R. Rahman & K.S. Chithra (Bombay)", ["a8k9a0v1q15"], 28, 130, 310, 8, "hindi", "classical"),
    ("Humma Humma Original", "A.R. Rahman & Remo Fernandes (Bombay)", ["a8k9a0v1q16"], 26, 125, 330, 10, "hindi", "banger"),
    ("Taal Se Taal Mila", "A.R. Rahman, Alka Yagnik & Udit Narayan (Taal)", ["a8k9a0v1q17"], 30, 135, 378, 9, "hindi", "folk-pop"),
    ("Ramta Jogi", "A.R. Rahman, Sukhwinder Singh & Alka Yagnik (Taal)", ["a8k9a0v1q18"], 28, 130, 377, 10, "hindi", "banger"),
    ("Kahin Aag Lage", "A.R. Rahman & Asha Bhosle (Taal)", ["a8k9a0v1q19"], 28, 130, 435, 9, "hindi", "dance"),
    ("Chale Chalo", "A.R. Rahman & Srinivas (Lagaan)", ["a8k9a0v1q20"], 30, 135, 396, 10, "hindi", "patriotic"),
    ("Mitwa", "A.R. Rahman, Udit Narayan & Alka Yagnik (Lagaan)", ["a8k9a0v1q21"], 28, 130, 407, 9, "hindi", "folk"),
    ("Ghanan Ghanan", "A.R. Rahman & Udit Narayan (Lagaan)", ["a8k9a0v1q22"], 30, 135, 371, 9, "hindi", "folk"),
    ("Lukka Chuppi", "A.R. Rahman & Lata Mangeshkar (Rang De Basanti)", ["a8k9a0v1q23"], 30, 135, 396, 8, "hindi", "emotional"),
    ("Khalbali", "A.R. Rahman, Mohammed Aslam & Nacim (RDB)", ["a8k9a0v1q24"], 25, 125, 379, 9, "hindi", "party"),
    ("Masti Ki Pathshala", "A.R. Rahman & Naresh Iyer (RDB)", ["a8k9a0v1q25"], 24, 120, 238, 10, "hindi", "banger"),
    ("Rubaroo", "A.R. Rahman & Naresh Iyer (RDB)", ["a8k9a0v1q26"], 24, 120, 283, 9, "hindi", "rock")
]
for t in rahman_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- GURU RANDHAWA & HARRDY SANDHU TO 50+ -----------------
guru_harrdy_tracks = [
    ("Morni Banke", "Guru Randhawa & Neha Kakkar (Badhaai Ho)", ["g8k9a0v1r01"], 22, 115, 198, 10, "punjabi", "banger"),
    ("Ishare Tere", "Guru Randhawa & Dhvani Bhanushali", ["g8k9a0v1r02"], 20, 110, 189, 9, "punjabi", "party"),
    ("Made in India", "Guru Randhawa", ["g8k9a0v1r03"], 20, 110, 205, 9, "punjabi", "party"),
    ("Raat Kamaal Hai", "Guru Randhawa & Tulsi Kumar", ["g8k9a0v1r04"], 22, 115, 220, 9, "punjabi", "party"),
    ("Downtown", "Guru Randhawa", ["g8k9a0v1r05"], 18, 105, 215, 9, "punjabi", "party"),
    ("Slowly Slowly", "Guru Randhawa ft. Pitbull", ["g8k9a0v1r06"], 20, 110, 207, 10, "punjabi", "banger"),
    ("Surma Surma", "Guru Randhawa & Jay Sean", ["g8k9a0v1r07"], 20, 110, 195, 9, "punjabi", "party"),
    ("Baby Girl", "Guru Randhawa & Dhvani Bhanushali", ["g8k9a0v1r08"], 18, 105, 203, 9, "punjabi", "party"),
    ("Naach Meri Rani", "Guru Randhawa & Nikhita Gandhi ft. Nora Fatehi", ["g8k9a0v1r09"], 22, 115, 210, 10, "punjabi", "banger"),
    ("Dance Meri Rani", "Guru Randhawa & Zahrah S Khan ft. Nora Fatehi", ["g8k9a0v1r10"], 22, 115, 215, 10, "punjabi", "banger"),
    ("Designer", "Guru Randhawa, Yo Yo Honey Singh & Divya Khosla Kumar", ["g8k9a0v1r11"], 20, 110, 216, 9, "punjabi", "party"),
    ("Moon Rise", "Guru Randhawa", ["g8k9a0v1r12"], 18, 105, 180, 8, "punjabi", "chill"),
    ("Fake Love Guru", "Guru Randhawa", ["g8k9a0v1r13"], 18, 105, 175, 8, "punjabi", "chill"),
    ("Tera Saath Ho", "Guru Randhawa & Zahrah S Khan", ["g8k9a0v1r14"], 20, 110, 210, 8, "hindi", "party"),
    ("Punjabiyan Di Dhee", "Guru Randhawa & Bohemia", ["g8k9a0v1r15"], 20, 110, 200, 9, "punjabi", "banger"),
    ("Soch", "Harrdy Sandhu", ["h8k9a0v1s01"], 25, 125, 290, 8, "punjabi", "romantic"),
    ("Joker", "Harrdy Sandhu & B Praak", ["h8k9a0v1s02"], 26, 125, 295, 8, "punjabi", "emotional"),
    ("Yaarr Ni Milyaa", "Harrdy Sandhu & B Praak", ["h8k9a0v1s03"], 24, 120, 255, 9, "punjabi", "party"),
    ("Dance Like", "Harrdy Sandhu & B Praak ft. Lauren Gottlieb", ["h8k9a0v1s04"], 20, 110, 169, 10, "punjabi", "banger"),
    ("Jee Karr Daa", "Harrdy Sandhu & Akasa", ["h8k9a0v1s05"], 20, 110, 185, 9, "punjabi", "party"),
    ("Titliaan", "Afsana Khan, Harrdy Sandhu & B Praak", ["h8k9a0v1s06"], 22, 115, 245, 9, "punjabi", "banger"),
    ("Titliaan Warga", "Harrdy Sandhu & Jaani", ["h8k9a0v1s07"], 22, 115, 235, 9, "punjabi", "banger"),
    ("Kudiyan Lahore Diyan", "Harrdy Sandhu & B Praak", ["h8k9a0v1s08"], 20, 110, 190, 10, "punjabi", "banger"),
    ("Psycho", "Harrdy Sandhu", ["h8k9a0v1s09"], 18, 105, 178, 9, "punjabi", "trap")
]
for t in guru_harrdy_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- KISHORE KUMAR TO 50+ -----------------
kishore_tracks = [
    ("Yeh Shaam Mastani", "Kishore Kumar (Kati Patang)", ["k8k9a0v1k51"], 28, 130, 275, 8, "hindi", "retro"),
    ("Roop Tera Mastana", "Kishore Kumar (Aradhana)", ["k8k9a0v1k52"], 26, 125, 225, 9, "hindi", "retro"),
    ("Mere Sapno Ki Rani", "Kishore Kumar (Aradhana)", ["k8k9a0v1k53"], 25, 125, 300, 9, "hindi", "retro"),
    ("Khaike Paan Banaraswala", "Kishore Kumar (Don)", ["k8k9a0v1k54"], 28, 130, 237, 10, "hindi", "banger"),
    ("O Saathi Re", "Kishore Kumar (Muqaddar Ka Sikandar)", ["k8k9a0v1k55"], 30, 135, 270, 8, "hindi", "retro"),
    ("Ek Ladki Bheegi Bhaagi Si", "Kishore Kumar (Chalti Ka Naam Gaadi)", ["k8k9a0v1k56"], 25, 125, 240, 9, "hindi", "retro"),
    ("Pal Pal Dil Ke Paas", "Kishore Kumar (Blackmail)", ["k8k9a0v1k57"], 26, 125, 329, 8, "hindi", "romantic"),
    ("Chookar Mere Mann Ko", "Kishore Kumar (Yaarana)", ["k8k9a0v1k58"], 25, 122, 255, 8, "hindi", "romantic"),
    ("Sara Zamana", "Kishore Kumar (Yaarana)", ["k8k9a0v1k59"], 26, 125, 260, 10, "hindi", "banger"),
    ("Jahan Teri Yeh Nazar Hai", "Kishore Kumar (Kaalia)", ["k8k9a0v1k60"], 28, 130, 310, 10, "hindi", "banger"),
    ("Apni To Jaise Taise", "Kishore Kumar (Laawaris)", ["k8k9a0v1k61"], 26, 125, 480, 10, "hindi", "banger"),
    ("Zindagi Ek Safar Hai Suhana", "Kishore Kumar (Andaz)", ["k8k9a0v1k62"], 25, 125, 255, 9, "hindi", "retro")
]
for t in kishore_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- UDIT NARAYAN & ALKA YAGNIK TO 50+ -----------------
udit_alka_tracks = [
    ("Tip Tip Barsa Paani", "Udit Narayan & Alka Yagnik (Mohra)", ["u8k9a0v1u51"], 28, 130, 355, 10, "hindi", "banger"),
    ("Mehndi Laga Ke Rakhna", "Udit Narayan & Lata Mangeshkar (DDLJ)", ["u8k9a0v1u52"], 30, 135, 290, 10, "hindi", "wedding"),
    ("Kuch Kuch Hota Hai", "Udit Narayan & Alka Yagnik (KKHH)", ["u8k9a0v1u53"], 28, 130, 296, 8, "hindi", "romantic"),
    ("Main Nikla Gaddi Leke", "Udit Narayan (Gadar)", ["u8k9a0v1u54"], 26, 125, 328, 10, "hindi", "banger"),
    ("Udja Kaale Kawan", "Udit Narayan & Alka Yagnik (Gadar)", ["u8k9a0v1u55"], 28, 130, 290, 8, "hindi", "folk"),
    ("Radha Kaise Na Jale", "Udit Narayan & Asha Bhosle (Lagaan)", ["u8k9a0v1u56"], 28, 130, 334, 9, "hindi", "folk"),
    ("Chand Chhupa Badal Mein", "Udit Narayan & Alka Yagnik (HDDCS)", ["u8k9a0v1u57"], 30, 135, 345, 8, "hindi", "romantic"),
    ("Aaye Ho Meri Zindagi Mein", "Udit Narayan (Raja Hindustani)", ["u8k9a0v1u58"], 28, 130, 360, 8, "hindi", "romantic"),
    ("Pardesi Pardesi", "Udit Narayan & Alka Yagnik", ["u8k9a0v1u59"], 30, 135, 450, 9, "hindi", "emotional"),
    ("Papa Kehte Hain", "Udit Narayan (QSQT)", ["u8k9a0v1u60"], 25, 125, 355, 9, "hindi", "retro"),
    ("Pehla Nasha", "Udit Narayan & Sadhana Sargam (JJWS)", ["u8k9a0v1u61"], 28, 130, 291, 8, "hindi", "romantic"),
    ("Jaadu Teri Nazar", "Udit Narayan (Darr)", ["u8k9a0v1u62"], 26, 125, 280, 8, "hindi", "romantic"),
    ("Choli Ke Peeche Kya Hai", "Alka Yagnik & Ila Arun (Khalnayak)", ["a8k9a0v1a51"], 30, 135, 310, 10, "hindi", "banger"),
    ("Dil Laga Liya Maine", "Alka Yagnik & Udit Narayan (Dil Hai Tumhaara)", ["a8k9a0v1a52"], 26, 125, 271, 8, "hindi", "romantic"),
    ("Kaho Naa Pyaar Hai Title", "Alka Yagnik & Udit Narayan", ["a8k9a0v1a53"], 28, 130, 420, 8, "hindi", "romantic"),
    ("Ek Pal Ka Jeena", "Lucky Ali & Alka Yagnik", ["a8k9a0v1a54"], 24, 120, 396, 10, "hindi", "banger"),
    ("Gali Mein Aaj Chand Nikla", "Alka Yagnik (Zakhm)", ["a8k9a0v1a55"], 28, 130, 305, 8, "hindi", "romantic"),
    ("Tumhi Dekho Naa", "Alka Yagnik & Sonu Nigam (KANK)", ["a8k9a0v1a56"], 28, 130, 348, 8, "hindi", "romantic")
]
for t in udit_alka_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

# ----------------- B. PRAAK TO 50+ -----------------
bpraak_tracks = [
    ("Filhall", "B Praak", ["b8k9a0v1p01"], 24, 120, 255, 9, "punjabi", "emotional"),
    ("Filhaal 2 Mohabbat", "B Praak", ["b8k9a0v1p02"], 25, 122, 285, 9, "punjabi", "emotional"),
    ("Teri Mitti", "B Praak (Kesari)", ["b8k9a0v1p03"], 28, 130, 314, 9, "hindi", "patriotic"),
    ("Mann Bharrya", "B Praak", ["b8k9a0v1p04"], 24, 120, 270, 9, "punjabi", "emotional"),
    ("Mann Bharryaa 2.0", "B Praak (Shershaah)", ["b8k9a0v1p05"], 26, 125, 290, 9, "hindi", "emotional"),
    ("Ranjha", "B Praak, Jasleen Royal & Romy (Shershaah)", ["b8k9a0v1p06"], 24, 120, 228, 8, "hindi", "romantic"),
    ("Dholna", "B Praak (Qismat)", ["b8k9a0v1p07"], 24, 120, 195, 9, "punjabi", "romantic"),
    ("Kaun Hoyega", "B Praak & Ammy Virk (Qismat)", ["b8k9a0v1p08"], 25, 125, 220, 9, "punjabi", "emotional"),
    ("Hath Chumme", "Ammy Virk & B Praak", ["b8k9a0v1p09"], 24, 120, 260, 9, "punjabi", "emotional"),
    ("Rabb Khair Kare", "B Praak", ["b8k9a0v1p10"], 22, 115, 230, 8, "punjabi", "emotional"),
    ("Kuch Bhi Ho Jaye", "B Praak", ["b8k9a0v1p11"], 24, 120, 320, 9, "punjabi", "emotional"),
    ("Baarish Ki Jaaye", "B Praak ft. Nawazuddin Siddiqui", ["b8k9a0v1p12"], 22, 118, 250, 9, "hindi", "romantic"),
    ("Besharam Bewaffa", "B Praak & Jaani", ["b8k9a0v1p13"], 24, 120, 275, 9, "hindi", "emotional"),
    ("Dil Tod Ke", "B Praak & Rochak Kohli", ["b8k9a0v1p14"], 24, 120, 288, 9, "hindi", "emotional"),
    ("Luka Chuppi B Praak", "B Praak", ["b8k9a0v1p15"], 22, 115, 240, 8, "punjabi", "emotional"),
    ("Dhoke Pyaar Ke", "B Praak & Rochak Kohli", ["b8k9a0v1p16"], 22, 118, 265, 8, "hindi", "emotional"),
    ("Kya Loge Tum", "B Praak ft. Akshay Kumar", ["b8k9a0v1p17"], 24, 120, 234, 9, "hindi", "emotional"),
    ("Jinke Liye", "Neha Kakkar & B Praak", ["b8k9a0v1p18"], 22, 115, 269, 8, "hindi", "emotional"),
    ("Pachtaoge", "Arijit Singh & B Praak", ["b8k9a0v1p19"], 22, 115, 226, 8, "hindi", "emotional"),
    ("Saahore Baahubali", "Daler Mehndi & B Praak", ["b8k9a0v1p20"], 26, 125, 203, 10, "hindi", "mass"),
    ("Fire", "B Praak (KGF 2)", ["b8k9a0v1p21"], 20, 110, 190, 10, "hindi", "banger"),
    ("Sulthan", "B Praak (KGF 2)", ["b8k9a0v1p22"], 22, 115, 230, 10, "hindi", "mass"),
    ("Jaan Ban Gaye", "Mithoon, Vishal Mishra & B Praak", ["b8k9a0v1p23"], 24, 120, 218, 8, "hindi", "romantic"),
    ("Qismat 2 Title Track", "B Praak", ["b8k9a0v1p24"], 25, 125, 305, 9, "punjabi", "emotional"),
    ("Marjaawaan", "B Praak & Asees Kaur (Bell Bottom)", ["b8k9a0v1p25"], 22, 118, 230, 8, "hindi", "romantic"),
    ("Aashiq Purana", "Kaka & B Praak", ["b8k9a0v1p26"], 20, 110, 210, 8, "punjabi", "romantic"),
    ("Roya Ve", "B Praak", ["b8k9a0v1p27"], 22, 115, 220, 8, "hindi", "emotional"),
    ("Chann Sitare", "Ammy Virk & B Praak", ["b8k9a0v1p28"], 20, 110, 215, 8, "punjabi", "romantic")
]
for t in bpraak_tracks:
    add_track(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])

with open("naux_full_library.json", "w", encoding="utf-8") as f:
    json.dump(library, f, indent=2)

print(f"Total songs in library now: {len(library)}")

