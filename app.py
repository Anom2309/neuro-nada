import streamlit as st
import datetime
import os
import time
import urllib.parse
import urllib.request
import math
import random
import csv
import io
import hashlib

# --- INIT SESSION STATE (PAYWALL) ---
if 'premium' not in st.session_state:
    st.session_state.premium = False

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="Neuro Nada Ultimate OS", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- CUSTOM CSS & SOFT ANIMATION ---
st.markdown(
    """<style>
    @keyframes softFade {
        0% { opacity: 0; transform: translateY(20px); filter: blur(5px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }
    .soft-fade {
        animation: softFade 1.2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; background-color: #050505; color: #e0e0e0; }
    .stApp { background: radial-gradient(circle at top, #111 0%, #000 100%); }
    div.stButton > button {
        background: linear-gradient(90deg, #FFD700 0%, #B8860B 100%) !important; color: #000000 !important;
        font-weight: 900 !important; border: none !important;
        padding: 15px 24px !important; border-radius: 8px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3); letter-spacing: 1px;
    }
    div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(255,215,0,0.5); }
    .cta-button {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff0000 100%);
        color: white !important; padding: 15px; text-align: center; 
        border-radius: 8px; font-weight: 900; font-size: 16px; 
        box-shadow: 0 6px 15px rgba(255, 75, 75, 0.4);
        text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;
    }
    .cta-button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(255, 75, 75, 0.6); }
    .ulasan-box { background: rgba(30, 30, 30, 0.6); backdrop-filter: blur(10px); padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700; margin-bottom: 12px; font-size: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .glass-container { background: rgba(25, 25, 25, 0.5); backdrop-filter: blur(12px); padding: 20px; border-radius: 12px; border: 1px solid rgba(212,175,55,0.2); box-shadow: 0 8px 32px 0 rgba(0,0,0,0.4); margin-bottom: 15px; }
    .primbon-box { background: linear-gradient(135deg, rgba(43,27,5,0.8) 0%, rgba(74,48,0,0.8) 100%); backdrop-filter: blur(10px); padding: 25px; border-radius: 12px; border: 1px solid #D4AF37; box-shadow: 0 8px 25px rgba(212,175,55,0.3); margin-top: 20px; margin-bottom: 20px; }
    .dynamic-reading-box { background: rgba(20, 20, 20, 0.7); backdrop-filter: blur(5px); padding: 20px; border-radius: 12px; border-left: 5px solid #FFD700; margin-top: 15px; margin-bottom: 15px; font-size: 15px; line-height: 1.6; }
    .matrix-container { display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap; padding: 15px; background: rgba(10,10,10,0.8); border-radius: 10px; border: 1px solid #333; margin-bottom: 5px; box-shadow: inset 0 2px 15px rgba(0,0,0,0.6); }
    .matrix-item { flex: 1; min-width: 80px; text-align: center; padding: 5px; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .matrix-value { font-size: 18px; font-weight: 900; color: white; }
    .matrix-value-special { color: #FFD700; }
    .list-punchy { padding-left: 20px; margin-bottom: 15px; font-size: 15px; }
    .list-punchy li { margin-bottom: 8px; }
    .live-badge { background: linear-gradient(90deg, #D4AF37, #FFD700); color: #000; padding: 8px 20px; border-radius: 30px; font-weight: 900; font-size: 14px; letter-spacing: 1px; display: inline-block; box-shadow: 0 4px 15px rgba(255,215,0,0.4); }
    .info-metric-box { background: rgba(255,215,0,0.05); border: 1px solid rgba(255,215,0,0.2); padding: 15px; border-radius: 8px; font-size: 14px; color: #ccc; margin-bottom: 20px; line-height: 1.6; }
    </style>""", unsafe_allow_html=True
)

def get_dynamic_count():
    start_date = datetime.date(2026, 4, 15) 
    today = datetime.date.today()
    delta = (today - start_date).days
    return f"{1287 + (max(0, delta) * 5):,}".replace(",", ".")

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa Kosmik"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

def get_planetary_hour():
    planets = [
        ("Matahari ☀️", "Fokus pada otoritas, presentasi, dan mengambil kendali.", "#FFD700"), 
        ("Venus 💖", "Waktu emas untuk negosiasi, asmara, dan melobi orang.", "#FF69B4"), 
        ("Merkurius 📝", "Eksekusi semua urusan email, naskah, dan komunikasi.", "#00FFFF"), 
        ("Bulan 🌙", "Waktu intuitif. Bagus untuk brainstorming atau istirahat.", "#F0F8FF"), 
        ("Saturnus 🪐", "Energi berat. Fokus pada pekerjaan repetitif dan audit.", "#8B4513"), 
        ("Yupiter 🍀", "Pintu rezeki terbuka. Waktu terbaik investasi/pitching.", "#32CD32"), 
        ("Mars ⚔️", "Energi agresif tinggi. Cocok untuk olahraga/eksekusi berani.", "#FF4500")
    ]
    return planets[datetime.datetime.now().hour % 7]

def get_sun_phase():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 8: return "Sunrise (Inisiasi)", "Gelombang otak beralih ke Alpha. Ideal untuk setting niat harian."
    elif 8 <= hour < 12: return "Morning (Akselerasi)", "Energi memuncak. Eksekusi tugas paling sulit sekarang."
    elif 12 <= hour < 15: return "Zenith (Konsolidasi)", "Matahari di puncak. Waktu untuk evaluasi dan re-kalibrasi."
    elif 15 <= hour < 18: return "Golden Hour (Refleksi)", "Waktu terbaik untuk kreativitas dan menyelesaikan urusan harian."
    elif 18 <= hour < 20: return "Sunset (Pelepasan)", "Tutup sistem saraf Anda dari beban kerja."
    else: return "Night Void (Regenerasi)", "Fase Delta. Dilarang mengambil keputusan besar di jam ini."

URL_POST = "https://script.google.com/macros/s/AKfycbwkOL8-E50RKM5BRR8puh_XbfL-K_hQj5cnv0un6UzmFmMBEG6HZZ4aEQmFZj5EMsSBUQ/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2H-IH_8TbdbMRtvZnvza-InIO-Xl-B9YzLYtWtSb8vpUVuM1uZ4FTi6JwOtk2esj7hilwgGCoWex4/pub?output=csv"

def ambil_ulasan():
    try:
        req = urllib.request.Request(URL_CSV)
        with urllib.request.urlopen(req) as response:
            return [row for row in csv.DictReader(io.StringIO(response.read().decode('utf-8')))][::-1]
    except: return []

def kirim_ulasan(nama, rating, komentar):
    try:
        data = urllib.parse.urlencode({"nama": nama, "rating": rating, "komentar": komentar}).encode("utf-8")
        urllib.request.urlopen(urllib.request.Request(URL_POST, data=data))
        return True
    except: return False

def generate_seed(base_str): return int(hashlib.md5(base_str.encode('utf-8')).hexdigest(), 16) % (10**8)
def get_safe_firstname(name_str, default="User"): return str(name_str).strip().split()[0].upper() if str(name_str).strip() else default

# --- TAB 5: QUANTUM ENGINE (AWAM-FRIENDLY & DEEP) ---
def proc_tactical_plan(nama, mod_harian, planet_live, planet_desc, sun_fase, sun_desc):
    random.seed(generate_seed(f"tac_{nama}_{mod_harian}_{planet_live}"))
    fase_detail = {
        0: {"nama": "🔴 FASE NADIR (Titik Terendah Baterai Mental)", "analisa": f"Sistem saraf dan gelombang otak {nama} sedang berada di titik paling lemah hari ini. Ibarat HP, baterai mental Anda sedang merah di 5%. Tubuh batin Anda sedang menuntut 'reboot' sistem. Memaksakan ambisi besar, lembur, atau mikir keras di jam ini sama dengan merusak mesin. Otak Anda sulit diajak kompromi dan sangat sensitif.", "do": ["Pilih pekerjaan bodoh/repetitif yang tidak butuh mikir (balas email basa-basi, rapihin meja, hapus file laptop).", "Lakukan *Deep Rest*. Tutup mata 15 menit, atau lakukan peregangan badan. Biarkan otak Anda bernapas."], "dont": "DILARANG KERAS ngambil keputusan duit yang besar, memulai proyek baru, atau ngajak pasangan ribut hari ini. Filter logika Anda lagi eror, Anda rawan salah langkah!"},
        1: {"nama": "🟢 FASE INISIASI (Percikan Api Pertama)", "analisa": f"Ini adalah momentum emas Anda, {nama}! Ibarat mobil balap, lampu hijau baru saja menyala. Ada ledakan energi segar di alam bawah sadar Anda. Apapun—sekecil apapun—tindakan yang Anda mulai di jam ini punya daya dorong (momentum) 3x lipat lebih mulus dibanding hari biasa. Semesta sedang berpihak pada keberanian Anda.", "do": ["Jangan mikir panjang, langsung GAS. Luncurkan ide yang lama tertunda, hubungi prospek penting, atau kirim proposal sekarang juga.", "Lakukan langkah pertama walau jelek. Hari ini adalah tentang 'Yang penting mulai dulu', bukan mencari kesempurnaan."], "dont": "HINDARI sifat *over-analysis* (kebanyakan mikir). Berdiam diri atau menunda pekerjaan hari ini adalah dosa besar terhadap potensi rezeki Anda."},
        2: {"nama": "🔵 FASE SINKRONISASI (Magnet Bantuan Orang Lain)", "analisa": f"Mode 'Pahlawan Super Sendirian' {nama} sedang dinonaktifkan oleh Semesta. Energi hari ini mendesak Anda untuk sadar bahwa rezeki dan solusi masalah Anda saat ini TIDAK ADA di tangan Anda sendiri, melainkan dititipkan lewat orang lain. Aura Anda sedang sangat magnetis dan mudah dipercaya oleh lawan bicara.", "do": ["Hubungi orang yang biasanya kaku atau susah di-lobby. Aura persuasif Anda hari ini lagi bagus-bagusnya.", "Delegasikan tugas! Serahkan pekerjaan yang bikin Anda pusing ke tim, rekan, atau bayar orang yang lebih ahli."], "dont": "JANGAN memaksakan diri sok jago berjuang sendirian (*Lone Wolf Syndrome*). Anda cuma akan kehabisan tenaga, stres, dan hasil akhirnya berantakan."},
        3: {"nama": "🟡 FASE RESONANSI (Daya Tembus Kata-Kata)", "analisa": f"Sirkuit komunikasi (Cakra Tenggorokan) {nama} sedang menyala terang benderang. Ibarat punya *amplifier* gaib, kata-kata yang Anda ucapkan atau tulis hari ini punya daya tembus yang langsung masuk ke alam bawah sadar orang yang membacanya/mendengarnya.", "do": ["Ini hari wajib untuk jualan! Buat konten *copywriting*, bikin video sosmed, lakukan presentasi, atau *Live*. Jangan diam!", "*Speak up*. Kalau ada ganjalan di hati ke pasangan atau rekan kerja, sampaikan sekarang. Mereka lebih mudah menerima."], "dont": "SANGAT DISAYANGKAN kalau Anda memilih ngumpet di goa atau diam saja seharian ini. Energi magis persuasi Anda akan terbuang sia-sia."},
        4: {"nama": "🟤 FASE MATERIALISASI (Kunci Gembok Keuangan)", "analisa": f"Gelombang otak {nama} sedang berubah wujud menjadi sangat realistis, dingin, dan perhitungan. Ini bukan waktunya ngayal babu atau bikin visi 5 tahun ke depan. Energi hari ini murni tentang 'Sapu Bersih'. Semesta menyuruh Anda mengamankan pondasi, ngecek uang keluar, dan beresin hal-hal membosankan tapi penting.", "do": ["Buka mutasi rekening Anda. Audit pengeluaran bocor minggu ini. Rapikan catatan keuangan bisnis Anda.", "Fokus kerjakan hal-hal teknis/operasional (SOP) yang membosankan yang selama ini Anda hindari."], "dont": "DILARANG KERAS spekulasi! Jangan *trading* asal-asalan, jangan investasi tanpa data pasti, dan jangan pinjamin uang ke orang. Kunci dompet Anda!"},
        5: {"nama": "🟠 FASE EKSPANSI (Dobrak Tembok Ketakutan)", "analisa": f"Adrenalin kosmik {nama} lagi memuncak tajam! Batas ketakutan dan rasa *insecure* (Mental Block) Anda sedang rapuh. Ini adalah jam yang tepat untuk 'Ngamuk' secara positif. Kalau Anda butuh melakukan hal ekstrem untuk kemajuan karir/bisnis, inilah saatnya. Tubuh Anda siap menghadapi penolakan.", "do": ["Pilih 1 hal yang paling bikin Anda merinding/takut minggu ini (misal: telepon bos besar, *cold calling* klien kakap) dan EKSEKUSI sekarang.", "Lakukan cara *marketing* atau pendekatan bisnis yang nekat, *out of the box*, dan beda dari biasanya."], "dont": "JANGAN biarkan diri Anda gabut atau bengong. Energi besar ini kalau didiamkan akan berbalik menyerang otak Anda menjadi *Anxiety* (kecemasan gelisah)."},
        6: {"nama": "🟣 FASE ELEVASI (Tabungan Karma Baik)", "analisa": f"Radar spiritual {nama} menembus urusan materi hari ini. Anda memancarkan vibrasi seorang *Healer* (Penyembuh/Pengayom). Semesta meminta Anda sejenak melupakan ambisi gila-gilaan soal uang, dan menyuruh Anda kembali ke 'Akar': keluarga, hati nurani, dan memaafkan rasa sakit masa lalu.", "do": ["Hubungi orang tua atau pasangan, tanyakan kabarnya dari hati ke hati. Minta maaf kalau gengsi Anda selama ini ketinggian.", "Pancing keajaiban rezeki lewat *Charity* (sedekah kejutan). Bantu orang kecil secara anonim (tanpa pamer)."], "dont": "HINDARI debat kusir, ngotot-ngototan adu ego, atau memanipulasi celah orang lain demi keuntungan uang. Hukum karma hari ini dibayar kontan!"}
    }
    fd = fase_detail[mod_harian]
    buka = random.choice([
        f"Melalui pembacaan algoritma waktu lahir Anda dan posisi langit detik ini, sistem mendeteksi adanya transisi energi yang sangat tajam pada diri Anda, **{nama}**. Ini artinya, cara Anda bertindak jam ini harus menyesuaikan mode di bawah.", 
        f"Peringatan Taktis untuk **{nama}**! Gelombang kosmik sedang berpusat membedah sektor eksekusi Anda. Ibarat sedang main catur, ini adalah langkah krusial. Jika Anda salah langkah di jam ini, momentum emas bisa hangus terbakar."
    ])
    planet_murni = planet_live.split(' ')[0]
    matahari_murni = sun_fase.split(' ')[0]
    koneksi = random.choice([
        f"Diperkuat oleh tarikan gravitasi Jam {planet_murni} yang sedang mengintervensi Fase {matahari_murni} di tubuh Anda, situasi ini menciptakan desakan absolut untuk bertindak sekarang juga.", 
        f"Resonansi magis dari {planet_murni} sedang bertabrakan dengan ritme sirkadian {matahari_murni} Anda. Ini mengunci otak bawah sadar Anda dalam mode siaga tingkat tinggi."
    ])
    
    do_html = "".join([f"<li style='margin-bottom: 10px;'>{item}</li>" for item in random.sample(fd["do"], 2)])
    html_output = f"""<div class="live-engine-box soft-fade" style="background: rgba(20,20,25,0.9); border-left: 4px solid #00FFFF; padding: 25px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,255,255,0.1);">
<h4 style="color: #00FFFF; margin-top:0; letter-spacing: 1px; font-weight:900;">⚡ TACTICAL ACTION PLAN <span style="font-size:12px; color:#ff4b4b; font-weight:normal;">(⏳ Valid 24 Jam)</span></h4>
<p style="color: #ccc; font-size: 15px; line-height: 1.7; margin-bottom:20px;">
{buka}<br><br>
<b style="color:#FFF; font-size:16px;">STATUS MESIN MENTAL ANDA: <span style="color:#FFD700;">{fd['nama']}</span></b><br>
<span style="color:#e0e0e0;">{fd['analisa']}</span><br><br>
<i style="color:#888;">Sinkronisasi Kosmik:</i> {koneksi} ({planet_desc})
</p>
<div style="background: rgba(37,211,102,0.1); border: 1px solid rgba(37,211,102,0.4); padding: 18px; border-radius: 8px; margin-bottom: 15px;">
<b style="color: #25D366; font-size:15px; letter-spacing:1px;">🎯 PROTOKOL EKSEKUSI (WAJIB LAKUKAN HARI INI):</b>
<ul style="color: #e0e0e0; font-size: 15px; margin-top: 10px; margin-bottom: 0; padding-left: 20px; line-height:1.6;">
{do_html}
</ul>
</div>
<div style="background: rgba(255,75,75,0.1); border: 1px solid rgba(255,75,75,0.4); padding: 18px; border-radius: 8px;">
<b style="color: #ff4b4b; font-size:15px; letter-spacing:1px;">🛑 RED ZONE (PANTANGAN MUTLAK):</b><br>
<span style="color: #e0e0e0; font-size: 15px; display:inline-block; margin-top:8px; line-height:1.6;">{fd['dont']}</span>
</div>
<p style="font-size:13px; color:#ff4b4b; margin-top:15px; font-weight:bold; text-align:center;">⏳ Sistem mendeteksi perubahan energi secara konstan. Ambil tindakan sebelum *window of opportunity* ini tertutup!</p>
</div>"""
    return fd['nama'].split('(')[0].strip(), html_output

# --- TAB 3: FALAK RUHANI (AWAM-FRIENDLY) ---
def proc_falak_ruhani(total_jummal, root_num, nama):
    ruhani_data = {
        1: {"asma": "Ya Fattah (Maha Pembuka)", "vibrasi": "Mendobrak Jalan Buntu & Gengsi Ego", "tujuan": "Asma ini ibarat linggis gaib. Fungsinya untuk membongkar paksa pintu rezeki yang selama ini nyangkut karena kesombongan, sifat keras kepala, atau gengsi Anda yang terlalu tinggi dalam meminta tolong."},
        2: {"asma": "Ya Salam (Maha Sejahtera)", "vibrasi": "Membangun Perisai Anti-Stres", "tujuan": "Asma ini adalah rompi anti-peluru untuk mental Anda. Gunanya untuk menetralisir energi *toxic* (beracun) dari lingkungan kerja/keluarga, dan meredakan dada yang sesak akibat terlalu sering mendem perasaan demi orang lain."},
        3: {"asma": "Ya Mushawwir (Maha Pembentuk)", "vibrasi": "Menarik Ide Liar Menjadi Uang Nyata", "tujuan": "Khusus untuk otak yang *overthinking* dan kebanyakan ide. Energi Asma ini mengikat angan-angan Anda ke bumi, memaksa sifat malas Anda hilang, sehingga wacana yang dari dulu cuma di kepala akhirnya bisa terwujud jadi karya fisik/bisnis nyata."},
        4: {"asma": "Ya Muqit (Maha Pemberi Kecukupan)", "vibrasi": "Menghancurkan 'Mental Miskin'", "tujuan": "Obat keras untuk Anda yang punya ketakutan berlebih soal kehabisan uang (*Scarcity Mindset*). Asma ini diprogram untuk memotong urat takut miskin, memberikan rasa aman total, dan memancing stabilitas aset material jangka panjang."},
        5: {"asma": "Ya Basith (Maha Melapangkan)", "vibrasi": "Memperbesar Kapasitas Wadah Rezeki", "tujuan": "Ibarat membesarkan ukuran ember sebelum diisi air hujan. Asma ini bekerja melepaskan rasa sumpek/terkekang dalam hidup Anda, melenyapkan kebosanan rutinitas, dan menyiapkan mental Anda untuk menerima uang dalam jumlah yang jauh lebih masif."},
        6: {"asma": "Ya Wadud (Maha Mengasihi)", "vibrasi": "Membangkitkan Magnet Pengasihan Alami", "tujuan": "Lebih ampuh dari pelet. Ini adalah tentang menyembuhkan *Inner-Child* (luka batin masa kecil). Jika diri Anda sudah sembuh, Asma ini otomatis akan membuat aura wajah Anda memancarkan daya tarik, respek, dan kasih sayang yang membuat orang tulus pada Anda."},
        7: {"asma": "Ya Batin (Maha Tersembunyi)", "vibrasi": "Membuka Mata Batin & Firasat Bisnis", "tujuan": "Asma ini bertindak seperti radar pendeteksi kebohongan. Fungsinya menajamkan intuisi (indra ke-6) Anda agar peka membaca niat busuk orang lain dari bahasa tubuhnya, sehingga Anda tidak mudah tertipu dalam investasi atau asmara."},
        8: {"asma": "Ya Ghaniy (Maha Kaya)", "vibrasi": "Mengunci Vibrasi Sultan & Otoritas Mutlak", "tujuan": "Dikhususkan untuk Anda yang memang ditakdirkan mengejar puncak piramida. Asma ini menyelaraskan sel tubuh Anda menjadi magnet uang murni, sekaligus menjaga hati Anda agar tidak gila kuasa atau hancur karena keserakahan."},
        9: {"asma": "Ya Hakim (Maha Bijaksana)", "vibrasi": "Pencerahan & Pemutus Rantai Karma Negatif", "tujuan": "Sebagai penghapus *cache* (sampah dosa masa lalu). Berfungsi merilis rasa bersalah yang diam-diam menahan laju sukses Anda. Asma ini menyingkirkan kekecewaan pada manusia dan menyambungkan hidup Anda dengan Tujuan Utama (Life Purpose)."}
    }
    data = ruhani_data.get(root_num, ruhani_data[1])
    return data["asma"], data["vibrasi"], data["tujuan"], total_jummal

def get_protokol_terapi(root_num, nama):
    random.seed(generate_seed(f"pt_deep_{nama}_{root_num}"))
    b1 = random.choice([
        f"**Sindrom Superman (Gengsi Minta Tolong):** Otak bawah sadar Anda ({nama}) terlanjur diprogram untuk merasa 'semua harus gue yang kerjain sendiri biar bener'. Padahal, sikap sok jago ini justru bikin Anda *burnout* (stres fisik parah) dan nutup pintu rezeki dari kolaborasi tim.", 
        f"**Gila Kontrol (Control Freak):** Anda ({nama}) punya ketakutan mendalam kalau pekerjaan diserahkan ke orang lain, hasilnya bakal hancur. Akhirnya, Anda mikul beban 10 orang sendirian. Rezeki Anda mentok karena kapasitas energi fisik Anda sebagai manusia ada batasnya."
    ])
    a1 = random.choice([
        f"Saya, {nama}, dengan ikhlas menurunkan tembok gengsi saya malam ini. Saya paham bahwa meminta bantuan orang lain adalah taktik orang cerdas, bukan tanda kelemahan. Saya mengizinkan kemudahan datang ke hidup saya.", 
        f"Mulai malam ini, saya ({nama}) berhenti memforsir tubuh saya seperti mesin. Saya layak dibantu. Saya layak istirahat. Semesta punya banyak tangan untuk membantu menyelesaikan masalah saya."
    ])
    h1 = random.choice(["Cari 1 tugas hari ini yang BISA Anda kerjakan sendiri, tapi secara sengaja **mintalah tolong** ke pasangan/rekan untuk mengerjakannya. Latih ego Anda untuk menerima bantuan.", "Curhat teknis: Hubungi satu mentor atau sahabat kompeten hari ini. Ceritakan kendala Anda dan cukup dengarkan nasihat mereka tanpa membantah sedikitpun."])

    b2 = random.choice([
        f"**Penyakit Nggak Enakan (People Pleaser):** Ini bahaya laten Anda, {nama}. Anda ibarat spons yang nyerap masalah dan keluh-kesah orang lain. Anda mengorbankan kebahagiaan dan uang Anda sendiri demi menjaga perasaan teman/keluarga yang *toxic*.", 
        f"**Takut Ditinggalkan (Abandonment Issue):** Hidup {nama} sering hancur karena Anda selalu mendahulukan kepentingan orang lain, hanya karena takut dijauhi. Anda lupa, orang yang Anda layani itu belum tentu memprioritaskan Anda saat Anda jatuh."
    ])
    a2 = random.choice([
        f"Saya, {nama}, memegang kendali penuh atas kewarasan saya. Kebahagiaan saya adalah prioritas nomor satu. Mulai saat ini, saya tidak peduli jika harus mengecewakan orang lain demi melindungi energi saya.", 
        f"Saya ({nama}) dengan sadar melepaskan rasa bersalah palsu ini. Saya menolak menjadi tempat sampah emosi orang lain. Bilang 'TIDAK' adalah hak asasi saya yang suci."
    ])
    h2 = random.choice(["Terapi Ketegasan: Berlatihlah bilang 'TIDAK' atau 'Maaf gue gak bisa' pada satu ajakan/permintaan hari ini. Jangan beri alasan panjang lebar, cukup tolak dengan sopan dan tegas.", "Puasa Orang Toxic: Matikan notifikasi grup WhatsApp atau *mute* satu orang yang paling sering ngeluh/nyedot energi Anda selama 24 jam penuh."])

    # ... (Protokol 3 sampai 9 gue kembangin bahasanya biar lebih awam dan ngena) ...
    b3 = random.choice([f"**Lompatan Kera (Fokus Berserakan):** Otak Anda ({nama}) itu pabrik ide cemerlang, tapi eksekusinya NOL. Anda terlalu cepat bosan. Baru mulai belajar A, besok udah pindah ke B karena liat peluang baru. Akhirnya nggak ada yang jadi duit.", f"**Mabuk Dopamin Awal:** Anda ({nama}) cuma semangat di 'awal' mula sebuah proyek. Pas udah masuk fase teknis yang ribet dan butuh konsistensi, Anda mendadak kabur nyari inspirasi lain. Ini sabotase paling nyata."])
    a3 = random.choice([f"Saya, {nama}, memerintahkan pikiran liar saya untuk diam dan membumi. Saya sadar, satu karya kecil yang SELESAI jauh lebih menghasilkan uang daripada seribu ide jenius yang cuma ada di angan-angan.", f"Pikiran saya setajam laser. Saya ({nama}) berjanji pada diri sendiri untuk menahan rasa bosan dan menyelesaikan apa yang sudah saya mulai sampai tuntas 100%."])
    h3 = random.choice(["Gunakan teknik Alarm 20 Menit. Pilih 1 kerjaan paling penting, set alarm 20 menit, dan paksa tangan Anda kerja tanpa buka WA atau YouTube sama sekali sampai alarm bunyi.", "Terapi Rapi-rapi: Pikiran yang ruwet berawal dari tempat yang berantakan. Bereskan total meja kerja Anda atau hapus file-file sampah di laptop hari ini juga."])

    b4 = random.choice([f"**Mental Melarat (Scarcity Mindset):** Di bawah sadar {nama}, ada ketakutan parah kalau besok bakal kehabisan uang. Ketakutan ini bikin Anda pelit (bahkan untuk *upgrade* diri sendiri) dan terlalu main aman, sehingga peluang besar selalu lewat.", f"**Jebakan Zona Nyaman (Anti-Risiko):** Anda ({nama}) sering berlindung di balik kata 'Nabung buat jaga-jaga'. Padahal secara energi, fokus Anda pada 'jaga-jaga hal buruk' justru menarik kesialan itu datang ke hidup Anda."])
    a4 = random.choice([f"Saya, {nama}, hari ini membuang jauh-jauh rasa takut jatuh miskin. Saya menyadari rezeki Tuhan itu nggak ada batasnya. Kondisi dompet saya aman, energi kelimpahan mengalir deras ke saya.", f"Saya ({nama}) layak menikmati kemewahan dan kelimpahan. Uang adalah energi cahaya yang baik, dan saya membuka pintu hati saya lebar-lebar untuk menyambutnya."])
    h4 = random.choice(["Terapi *Letting Go* (Melepaskan): Pergi keluar hari ini dan beli satu makanan/barang yang agak mahal khusus untuk menghargai diri Anda sendiri. Saat bayar, jangan ada rasa nyesel di hati.", "Pecah Urat Takut: Lakukan transfer sedekah *random* ke orang yang nggak terduga hari ini (nominal bebas). Niatkan untuk membongkar mental pelit di alam bawah sadar."])

    b5 = random.choice([f"**Sindrom Kabur (Escapism):** Tiap kali dihadapkan pada rutinitas yang menuntut tanggung jawab dan konsistensi panjang, sistem saraf {nama} mendadak eror. Anda gatal pengen melarikan diri mencari 'kebebasan' palsu.", f"**Alergi Komitmen:** Kunci sukses Anda tertahan karena Anda ({nama}) nggak kuat menahan rasa jenuh. Saat bisnis/hubungan mulai masuk fase stabil yang datar, Anda malah mensabotase diri dengan mencari masalah/distraksi baru."])
    a5 = random.choice([f"Saya, {nama}, kini menyadari bahwa kedamaian justru ada di dalam konsistensi. Rutinitas bukanlah penjara yang mengekang saya, melainkan pondasi baja untuk membangun kerajaan saya.", f"Saya ({nama}) memegang kendali penuh atas rasa bosan di otak saya. Saya berdamai dengan keringat dan proses yang berulang-ulang."])
    h5 = random.choice(["Pilih SATU pekerjaan yang paling ngebosenin dan udah Anda tunda berminggu-minggu. Paksa bokong Anda duduk diam dan selesaikan itu hari ini juga sampai tuntas 100%.", "Terapi Repetisi: Buat satu rutinitas pagi yang sangat sederhana (misal: minum air putih hangat sambil dengerin instrumental). Lakukan persis sama selama 3 hari berturut-turut tanpa diubah."])

    b6 = random.choice([f"**Sindrom Pahlawan Kesiangan (Savior Complex):** Anda ({nama}) merasa berdosa kalau hidup enak sendirian sementara ada keluarga/teman yang susah. Ujung-ujungnya, hasil keringat Anda habis buat nalangin masalah orang yang *toxic*.", f"**Luka Pengorbanan Bertepuk Sebelah Tangan:** Anda ({nama}) jor-joran ngasih uang, waktu, dan hati ke orang terdekat. Tapi jauh di lubuk batin, Anda depresi karena merasa nggak ada satupun yang peduli balik saat Anda lagi hancur."])
    a6 = random.choice([f"Saya, {nama}, dengan sadar mengizinkan diri saya bahagia duluan. Tangki cinta dan uang saya harus luber dulu, baru saya bisa membaginya ke orang lain. Diri saya adalah prioritas suci.", f"Saya ({nama}) menolak menjadi mesin ATM atau tong sampah emosi bagi siapapun. Saya berhak menikmati 100% keringat dan hasil jerih payah saya sendiri."])
    h6 = random.choice(["Terapi Ego Positif: Blokir waktu minimal 1 jam hari ini murni untuk 'Me-Time'. Matikan koneksi, lakukan hobi Anda, dan HARAM hukumnya mikirin masalah orang lain di jam tersebut.", "Pergi ke kafe enak sendirian. Pesan menu kesukaan Anda. Makan pelan-pelan, nikmati tiap suapannya, dan sadari bahwa Anda sangat berharga."])

    b7 = random.choice([f"**Lumpuh Logika (Paralysis by Analysis):** Otak {nama} itu terlalu pinter, tapi kepinteran ini berbalik jadi bumerang. Anda memikirkan risiko A sampai Z secara *overthinking* sampai akhirnya Anda panik dan nggak jadi *action* apa-apa.", f"**Penyakit Susah Percaya (Trust Issue):** Luka masa lalu bikin otak {nama} punya radar curiga yang kebangetan. Anda sering menolak peluang duit atau niat baik orang hanya karena paranoid takut ditipu lagi."])
    a7 = random.choice([f"Saya, {nama}, melepaskan ilusi bahwa saya harus tahu semua ujung dari suatu rencana. Saya mengizinkan diri saya melangkah dulu sambil memperbaiki jalan, percaya bahwa Semesta melindungi saya.", f"Saya ({nama}) memaafkan trauma masa lalu yang membuat saya sinis. Saya membuka diri pada keajaiban. Tidak semua orang di dunia ini berniat jahat pada saya."])
    h7 = random.choice(["Terapi Kekosongan Hening: Duduk santai tanpa HP, tanpa musik. Diam total selama 15 menit. Kalau pikiran aneh-aneh muncul, biarkan saja numpang lewat, jangan dianalisa.", "Latih Otot Percaya: Hari ini, terima satu pujian, tawaran, atau niat baik dari seseorang secara mentah-mentah tanpa berusaha mencari 'apa maksud tersembunyinya'."])

    b8 = random.choice([f"**Diktator Bawah Sadar (Control Freak):** Di balik wibawa {nama}, ada ego rapuh yang takut banget dibilang 'lemah' atau 'gagal'. Ini bikin Anda maksa diri sendiri dan nekan orang di sekitar Anda tanpa ampun demi ngejar uang/target.", f"**Terpenjara Ambisi Sendiri:** Insting bisnis {nama} emang luar biasa tajam. Tapi ambisi material yang nggak ada garis *finish*-nya ini udah merampok kedamaian tidur dan kebahagiaan batin Anda."])
    a8 = random.choice([f"Saya, {nama}, sadar bahwa saya tidak bisa mengontrol seluruh dunia. Kekuatan sejati saya justru muncul di saat saya pasrah dan membiarkan Tuhan mengambil alih kemudi.", f"Saya ({nama}) melepaskan belenggu ambisi buta ini. Uang mengalir kepada saya dengan mudah dan damai. Keberhasilan saya tidak harus dibayar dengan kehancuran sistem saraf saya."])
    h8 = random.choice(["Latihan Lepas Kendali: Hari ini, biarkan rekan, bawahan, atau pasangan Anda yang ngambil keputusan operasional. Apapun hasilnya (walau jelek), Anda dilarang ikut campur atau ngomel.", "Aturan Berhenti Keras (Hard Stop): Teng jam 17:00, matikan laptop dan HP kerja. Dilarang keras nyentuh atau bahas urusan duit/kerjaan sampai besok pagi."])

    b9 = random.choice([f"**Empati Beracun (Toxic Empathy):** Kesadaran nurani {nama} itu levelnya ketinggian. Anda jadi gampang banget kasihan dan selalu ngasih 'kesempatan kedua' ke orang *toxic* yang udah jelas-jelas nipu/manfaatin Anda berkali-kali.", f"**Patah Hati Paradigma (Ekspektasi Hancur):** Anda ({nama}) mandang hidup pake standar moral malaikat. Pas turun ke lapangan dan liat betapa licik/kejamnya sifat manusia, batin Anda kelelahan, stres, dan hilang harapan."])
    a9 = random.choice([f"Saya, {nama}, menyadari bahwa tugas suci saya BUKAN untuk menyelamatkan semua orang di bumi. Saya membiarkan mereka memikul karmanya masing-masing tanpa harus saya tanggung.", f"Energi batin saya ({nama}) sangat mahal dan suci. Saya berhenti memaklumi orang yang dengan sengaja merugikan saya. Saya lindungi kewarasan saya hari ini."])
    h9 = random.choice(["Detoks Sampah Negatif: Pantang nonton berita politik, tragedi, kriminal, atau *scroll* curhatan drama sosmed selama 24 jam penuh. Jaga pikiran Anda tetap steril.", "Terapi Tutup Mulut: Sepanjang hari ini, berhentilah bertindak sok bijak. Jangan kasih nasihat, wejangan, atau solusi ke siapapun KECUALI mereka yang ngemis minta diajarin."])

    protokol = {1: {"block": b1, "afirmasi": a1, "habit": h1}, 2: {"block": b2, "afirmasi": a2, "habit": h2}, 3: {"block": b3, "afirmasi": a3, "habit": h3}, 4: {"block": b4, "afirmasi": a4, "habit": h4}, 5: {"block": b5, "afirmasi": a5, "habit": h5}, 6: {"block": b6, "afirmasi": a6, "habit": h6}, 7: {"block": b7, "afirmasi": a7, "habit": h7}, 8: {"block": b8, "afirmasi": a8, "habit": h8}, 9: {"block": b9, "afirmasi": a9, "habit": h9}}
    return protokol.get(root_num, protokol[1])

# --- TAB 1: IDENTITAS KOSMIK (AWAM-FRIENDLY) ---
arketipe_punchy = {
    1: {"inti": "Sang Perintis (Dominator & Pendobrak Batas)", "kekuatan": ["Nyali gede buat ambil risiko ekstrem yang orang lain takut lakuin", "Kemandirian mutlak (nggak suka disetir atau nunggu arahan)", "Insting eksekusi cepat, anti kebanyakan rapat/wacana"]},
    2: {"inti": "Sang Penyelaras (Negosiator & Radar Emosi)", "kekuatan": ["Punya empati tajam, bisa ngerasain *mood* ruangan dalam sedetik", "Jago lobi-lobi dan mencairkan hati klien yang keras", "Bisa nengahin konflik panas tanpa bikin orang sakit hati"]},
    3: {"inti": "Sang Visioner (Pabrik Ide & Si Lidah Emas)", "kekuatan": ["Daya tarik komunikasi tingkat dewa (cocok buat *sales/marketing*)", "Otaknya selalu *out of the box*, nggak pernah kehabisan ide kreatif", "Bisa nge-hipnotis keramaian cuma pake gaya bicara dan presentasi"]},
    4: {"inti": "Sang Transformator (Arsitek Sistem & Mesin Fondasi)", "kekuatan": ["Pola pikir sangat logis, presisi, dan benci sama hal yang berantakan", "Punya loyalitas baja, orang yang bisa diandalkan jaga rahasia/aset", "Jago banget ngerjain SOP detail yang bikin orang lain nyerah/bosan"]},
    5: {"inti": "Sang Penggerak (Si Kutu Loncat Pemecah Masalah)", "kekuatan": ["Sangat lincah di situasi krisis/chaos saat orang lain panik", "Inovator nekat, berani nyoba rute *marketing* yang belum pernah ada", "Kecepatan adaptasi tinggi terhadap teknologi/tren pasar terbaru"]},
    6: {"inti": "Sang Harmonizer (Pengayom & Mesin Penyembuh)", "kekuatan": ["Insting ngerawat dan melindungi sirkel terdekatnya sangat luar biasa", "Punya aura 'Aman' yang bikin orang gampang percaya naruh duit/rahasia", "Tanggung jawab moral tinggi, anti kabur dari hutang/tugas"]},
    7: {"inti": "Sang Legacy Builder (Radar Kebohongan & Penganalisa Murni)", "kekuatan": ["Mata batinnya tajam, mustahil bisa ditipu sama *fake framing* (pencitraan)", "Logika analisanya berlapis, selalu mikir *worst case scenario* (risiko terburuk)", "Sangat selektif milih sirkel, sehingga kualitas kerjanya selalu *high-end*"]},
    8: {"inti": "Sang Sovereign (Eksekutor Boss & Magnet Duit)", "kekuatan": ["Tahan banting luar biasa dihajar stres bisnis atau tekanan hidup", "Insting nyium peluang duit dan investasi sangat presisi (Radar Cuan)", "Wibawa bawaannya bikin orang segan/nurut tanpa perlu dia marah-marah"]},
    9: {"inti": "Sang Kesadaran Tinggi (Jiwa Tua & Empati Universal)", "kekuatan": ["Pandangannya luas (Helicopter View), nggak gampang emosi karena hal sepele", "Bisa memahami titik penderitaan klien/pasar sehingga jualan jadi lebih kena", "Bijaksana alami, sering jadi tempat curhat atau minta saran dari orang-orang hebat"]}
}

def proc_arketipe(nama, angka, zodiak, neptu):
    random.seed(generate_seed(f"hyper_ark_deep_{nama}_{angka}_{zodiak}_{neptu}"))
    buka = random.choice([
        f"Ibarat setiap HP punya Sistem Operasi (Android/iOS) bawaan pabrik, otak bawah sadar **{nama}** secara genetik terkunci di **KODE {angka}** semenjak tarikan napas pertama.",
        f"Hasil persilangan garis lintang kelahiran dan unsur elemen {zodiak} memetakan DNA psikologis **{nama}** secara presisi di **KODE {angka}**."
    ])
    
    inti = {
        1: "Ini berarti Anda adalah mesin eksekusi bertipe Sang Perintis. Anda dilahirkan dengan *mental block* penolakan terhadap aturan kaku. Anda benci disetir. Otak Anda berfungsi maksimal saat dikasih kebebasan membuka lahan bisnis atau proyek baru yang belum pernah disentuh orang.",
        2: "Ini berarti Anda adalah Sang Penyelaras alami. Anda dibekali radar empati sensitif layaknya spons penyerap air. Anda bisa 'membaca' karakter asli seseorang dari bahasa tubuhnya dalam hitungan menit. Ini membuat Anda menjadi negosiator ulung di balik meja.",
        3: "Ini berarti Anda adalah mesin Komunikator Magnetis. Senjata utama pencetak uang Anda bukan di otot, tapi di lidah dan ekspresi. Otak Anda meletup-letup dengan ratusan ide kreatif per jam. Kalau Anda diam saja, rezeki Anda mati.",
        4: "Ini berarti Anda adalah Arsitek Sistem (Sang Pembangun). Anda menolak hidup yang cuma modal nekat. Otak Anda didesain beroperasi secara sistematis, terstruktur, dan presisi tinggi. Perusahaan hancur tanpa orang berkarakter pondasi baja seperti Anda di belakang layar.",
        5: "Ini berarti jiwa Anda terkunci pada mode Eksplorator (Pencari Kebebasan). Anda punya alergi kronis terhadap rutinitas *9-to-5* yang itu-itu saja. Kecerdasan otak Anda baru akan meledak keluar saat Anda berada di bawah tekanan (*chaos*) atau saat bepergian ke tempat baru.",
        6: "Ini berarti Anda diutus ke bumi membawa energi Pengayom (Sang Healer). Tanggung jawab moral di pundak Anda selalu terasa berat karena insting Anda selalu ingin merawat, melindungi, dan menanggung beban penderitaan orang-orang terdekat Anda.",
        7: "Ini berarti Anda memiliki sirkuit otak bertipe Analitik Forensik. Anda adalah pencari kebenaran sejati. Filter logika Anda sangat tebal, membuat Anda tidak akan pernah sudi ditipu oleh janji manis atau omong kosong. Keputusan Anda selalu berbasis data dan intuisi tajam.",
        8: "Ini berarti Anda memancarkan gravitasi Sang Sovereign (Pemegang Otoritas). Secara alami, fokus bawah sadar Anda ditarik agresif menuju puncak rantai makanan (kekuasaan & uang). Wibawa dominan Anda seringkali membuat lawan bicara ciut nyali sebelum Anda bertindak.",
        9: "Ini berarti Anda membawa energi *Old Soul* (Jiwa Tua yang Bijaksana). Kacamata Anda dalam memandang kerasnya dunia jauh lebih luas dari orang seumuran Anda. Anda dikaruniai empati universal yang memampukan Anda melihat 'gambaran besar' dari sebuah tragedi atau masalah bisnis."
    }
    
    shadow = {
        1: "Namun hati-hati, ego mandiri Anda sering berubah menjadi 'Sombong Bawah Sadar'. Anda saking gengsinya minta tolong, akhirnya sering kelelahan (*burnout*) memikul beban sendirian yang rawan bikin Anda sakit fisik.",
        2: "Sisi gelapnya, radar empati Anda itu bocor. Anda sering kena 'Sindrom Nggak Enakan', menekan perasaan sendiri demi menyenangkan orang lain (klien/keluarga). Ujung-ujungnya, Anda stres menampung emosi sampah mereka.",
        3: "Penyakit kronis Anda adalah 'Fokus Berserakan'. Ide ada seratus, yang selesai nol. Anda gampang bosan dan sering ganti-ganti arah sebelum panen hasil. Selain itu, mulut Anda bisa sangat berbisa kalau lagi emosi.",
        4: "Jebakan mematikan Anda adalah *Micro-managing* (cerewet soal detail kecil). Saking takutnya sistem berantakan, Anda jadi kaku, anti-risiko, dan rawan melewatkan peluang emas hanya karena datanya 'kurang lengkap'.",
        5: "Waspadai penyakit 'Kabur dari Komitmen'. Seringkali pas bisnis atau asmara Anda udah hampir sampai di puncak sukses, mendadak Anda bosan, mensabotase diri, lalu kabur mencari mainan baru.",
        6: "Sifat pengayom Anda sering berubah jadi 'Penyelamat Berlebihan'. Anda nguras habis-habisan uang dan mental Anda demi nolong orang *toxic* yang bahkan nggak tau diri, sementara batin Anda menjerit kesepian.",
        7: "Kelemahan fatal Anda adalah *Paralysis by Analysis* (Lumpuh karena kebanyakan mikir). Anda terlalu lama menganalisa risiko sampai akhirnya momentum cuannya hilang diambil orang. Sifat curigaan Anda juga sering merusak relasi.",
        8: "Sisi gelap arsitektur boss ini adalah ketakutan luar biasa terlihat 'Lemah'. Sifat gila kontrol Anda bikin Anda stres kronis. Sulit sekali bagi Anda untuk pasrah, berserah diri pada Tuhan, atau memaafkan pengkhianatan di masa lalu.",
        9: "Karena standar moral Anda ketinggian, penyakit mental Anda adalah gampang kecewa parah ngeliat kelakuan minus manusia lain. Energi welas asih Anda rawan dimanipulasi/dimanfaatkan habis-habisan oleh para *scammer* emosional."
    }
    
    return f"{buka} {inti[angka]}<br><br><span style='color:#ccc;'>{shadow[angka]}</span>"

def get_betaljemur_data(neptu, hari):
    lk = {
        7: ("Lebu Katiup Angin (Rentan Bocor)", "Ibarat debu ditiup angin badai. Fokus pikiran dan dompet Anda hari ini sangat gampang terombang-ambing godaan impulsif. Anda butuh 'jangkar' berupa rutinitas ketat. Kalau nggak hati-hati, uang atau waktu Anda bakal menguap entah kemana."),
        8: ("Lakuning Geni (Elemen Api Menyala)", "Sistem emosi Anda hari ini mirip bensin yang ketemu percikan korek. Senggol dikit bacok! Tapi di sisi positif, ambisi kerja Anda lagi menyala terang benderang. Kendalikan lidah Anda, jangan sampai kata-kata kasar hari ini membakar relasi yang udah capek-capek dibangun."),
        9: ("Lakuning Angin (Cepat & Labil)", "Sistem saraf Anda sangat lincah adaptasi hari ini, tapi sayangnya *mood* Anda jadi susah ditebak kayak cuaca. Vibrasi ini sangat *super power* kalau dipakai buat negosiasi kilat atau *closing* cepat, tapi jelek banget kalau dipakai buat neken kontrak komitmen 5 tahun ke depan."),
        10: ("Pandito Mbangun Teki (Aura Sang Pertapa)", "Energi hening dan misterius menyelimuti Anda. Hari ini adalah hari emas untuk introspeksi, menyusun strategi secara diam-diam, dan menajamkan mata batin. Kecerdasan otak logis Anda mampu membongkar masalah bisnis yang paling rumit sekalipun."),
        11: ("Aras Tuding (Tertunjuk Semesta)", "Ada aura kepeloporan dan keberanian ekstrem yang aktif di sel Anda hari ini. Anda bakal sering 'ditunjuk' secara gaib oleh keadaan—entah itu ditunjuk buat nyelesain krisis mendadak, atau ditunjuk oleh peluang duit tak terduga. Ambil panggungnya, jangan malu-malu!"),
        12: ("Aras Kembang (Magnet Kharisma)", "Tingkat pesona dan daya tarik visual (*Magnetic Aura*) Anda sedang mekar maksimal! Gelombang energi ini bikin apapun yang keluar dari mulut Anda lebih gampang dituruti. Ini *cheat code* (kode curang) hari ini buat melobi calon mertua, atasan, atau klien kelas VVIP."),
        13: ("Lakuning Lintang (Bintang Kesepian)", "Anda memancarkan pesona misterius yang diam-diam diperhatiin banyak orang, tapi batin Anda rasanya pengen menyendiri di kamar. Fase ini memperingatkan: Jangan kelamaan ngumpet di zona nyaman! Ada peluang kolaborasi duit di luar sana yang nunggu Anda keluar goa."),
        14: ("Lakuning Rembulan (Penenang Batin)", "Kehadiran fisik Anda hari ini bertindak ibarat obat penenang alami (*sedative*) buat lingkungan sekitar. Orang yang lagi panik bakal merasa aman kalau deket Anda. Gunakan intuisi tajam Anda hari ini untuk ngambil keputusan bisnis yang *win-win solution*."),
        15: ("Lakuning Srengenge (Matahari Siang Bolong)", "Aura wibawa Anda sepanas dan semenyilaukan matahari jam 12 siang. Sangat logis, galak, terang, dan dominan! Kata-kata Anda nggak bisa dibantah bawahan/pasangan. Pakai energi banteng ini buat nge-gas *project* yang macet atau nebang benalu di perusahaan Anda."),
        16: ("Lakuning Banyu (Air Tenang Menghanyutkan)", "Ibarat air sungai yang keliatan tenang di atas tapi arusnya deras di bawah. Anda kelihatan super sabar dan luwes ngadepin orang hari ini, tapi otak Anda menyimpan strategi presisi mematikan. Sangat pas untuk mengamati celah saingan secara diam-diam, lalu 'menerkam' di menit akhir."),
        17: ("Lakuning Bumi (Baja Fondasi)", "Energi otak Anda sangat membumi, keras kepala, dan super terstruktur. Hari ini pikiran Anda nolak wacana motivasi basi. Fokus pakai energi ini untuk 'nyapu bersih': audit mutasi rekening, cek stok, dan nambal kebocoran SOP bisnis Anda."),
        18: ("Lakuning Paripurna (Sabda Pandita Ratu)", "Ini adalah fase puncak pemegang kendali! Aura Anda ibarat raja yang bijaksana. Peringatan Ekstrem: Perkataan Anda hari ini mengandung energi 'Tuah' atau kutukan. DILARANG KERAS ngeluh, nyumpahin orang jelek, atau ngomong miskin, karena manifestasi malaikat bisa langsung kejadian hari ini!")
    }
    nd = {"Minggu":"Timur", "Senin":"Selatan", "Selasa":"Barat", "Rabu":"Utara", "Kamis":"Timur", "Jumat":"Selatan", "Sabtu":"Selatan"}
    return lk.get(neptu,("Anomali Kosmik","Energi tak terpetakan. Logika tidak berlaku, pakai intuisi liar Anda hari ini."))[0], lk.get(neptu,("Anomali",""))[1], nd.get(hari,"Netral")

def get_rezeki_usaha(neptu):
    r = {
        1: ("Wasesa Segara (Lautan Kelimpahan)", "Kran rezeki Anda lagi masuk mode 'Bypass' (tanpa hambatan) sebesar samudra. Kejutan finansial sering datang dari arah yang sama sekali nggak masuk logika Excel Anda. Syarat aktifnya: Buang keraguan, berani ambil *action* ekstrem hari ini juga!"),
        2: ("Tunggak Semi (Regenerasi Otomatis)", "Vibrasinya ibarat ranting pohon: dipatahkan satu, tumbuh tiga yang baru. Kalau hari ini Anda ditolak klien, rugi *trading*, atau kecurian, JANGAN STRES. Algoritma gaib Anda sudah di-setting untuk memantulkan kerugian itu dengan profit yang jauh lebih brutal minggu depan."),
        3: ("Satria Wibawa (Mata Uang Kehormatan)", "Harap diingat: Rezeki Anda hari ini bentuknya bukan *transferan cash* instan! Rezeki Anda turun dalam bentuk 'Trust' (Kepercayaan) dan *Networking* dari orang penting ber-uang banyak. Jaga penampilan, wangi badan, dan tutur kata. Respek mereka adalah kunci brankas Anda."),
        4: ("Sumur Sinaba (Oasis Ilmu)", "Vibrasi energi Anda lagi bertindak kayak sumur air di tengah gurun. Orang-orang bakal datang nyamperin Anda buat nanya solusi, minta nasihat, atau numpang curhat. Jangan pelit ngasih *value* gratisan! Karena dari obrolan itulah konversi duit *closing* Anda bakal tercipta malam ini."),
        5: ("Bumi Kapetak (Panen Keringat Cerdas)", "Maaf, nggak ada keajaiban pesugihan instan hari ini. Mesin ATM Anda minta *password* berupa pembuktian kerja keras gila-gilaan dan strategi jitu. Kalau Anda mau nurunin ego buat turun gunung ngerjain hal teknis yang capek, panen rupiah gede nunggu di akhir hari."),
        6: ("Satria Wirang (Kawah Ujian Mental)", "AWAS! Anda lagi masuk zona turbulensi. Bakal ada gesekan, rasa malu, fitnah kecil, atau ujian mental dadakan. Ini bukan sial! Ini cara Semesta ngetes kelayakan *mindset* Anda sebelum ngebuka akses uang level lebih tinggi. Jangan reaktif, diam dan tetaplah *low-profile*."),
        7: ("Lebu Katiup Angin (Bahaya Dompet Jebol)", "Status lampu kuning buat arus kas (*cashflow*) Anda! Potensi duit masuk emang gede, tapi 'angin' hasrat pengeluaran foya-foya / *impulse buying* bertiup lebih kencang lagi. Amankan aset! Begitu duit cair hari ini, langsung pindahin ke reksa dana, emas, atau rekening mati.")
    }[neptu%7 or 7]
    u = {
        1: ("Sandang (Kebutuhan Permukaan)", "Gelombang hoki Anda nyetrum kuat kalau Anda ngurusin komoditas sekunder, urusan gaya hidup (*lifestyle*), *fashion*, atau produk/jasa yang bikin orang lain terlihat lebih keren dan pede."),
        2: ("Pangan (Suntikan Nutrisi Esensial)", "Vibrasi bisnis paling gacor berputar di urusan perut (F&B, kuliner) atau urusan asupan otak (seperti jualan kelas edukasi, *training*, buku, dan konsultasi *mindset*)."),
        3: ("Beja (Hoki Bandar Murni)", "Sektor hoki Anda lagi nggak masuk akal! Ini adalah waktu terbaik buat eksekusi instrumen investasi, neken kontrak gede, peluncuran produk digital SaaS, atau negoisasi alot. Tingkat keberuntungan Anda lagi di- *buff*."),
        4: ("Lara (Zona Rawan Blunder)", "Peringatan Siaga 1! Otak Anda lagi rawan bikin *blunder*. Haram hukumnya ngambil keputusan bisnis ekspansi gede secara sendirian. Anda diwajibkan nanya *second opinion* (pendapat pihak ketiga) sebelum *transfer* dana."),
        5: ("Pati (Titik Buta Fatal)", "Tutup aplikasi *trading* Anda! Dilarang keras ngelakuin spekulasi buta, masukin duit ke *crypto* asal-asalan, atau judi *online*. Energi Anda lagi 'Mati'. Fokusin tenaga murni cuma buat perbaikan sistem *error* atau ngerapihin meja kerja.")
    }[neptu%5 or 5]
    return r, u
 
def get_zodiak(tanggal):
    d, m = tanggal.day, tanggal.month
    if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "Aries"
    elif (m == 4 and d >= 20) or (m == 5 and d <= 20): return "Taurus"
    elif (m == 5 and d >= 21) or (m == 6 and d <= 20): return "Gemini"
    elif (m == 6 and d >= 21) or (m == 7 and d <= 22): return "Cancer"
    elif (m == 7 and d >= 23) or (m == 8 and d <= 22): return "Leo"
    elif (m == 8 and d >= 23) or (m == 9 and d <= 22): return "Virgo"
    elif (m == 9 and d >= 23) or (m == 10 and d <= 22): return "Libra"
    elif (m == 10 and d >= 23) or (m == 11 and d <= 21): return "Scorpio"
    elif (m == 11 and d >= 22) or (m == 12 and d <= 21): return "Sagittarius"
    elif (m == 12 and d >= 22) or (m == 1 and d <= 19): return "Capricorn"
    elif (m == 1 and d >= 20) or (m == 2 and d <= 18): return "Aquarius"
    else: return "Pisces"

# --- TAB 2: COUPLE MATRIX (AWAM-FRIENDLY & DEEP) ---
def proc_penjelasan_matriks(n1, n2, eso_val, nep_val):
    random.seed(generate_seed(f"pm_v4_{n1}_{n2}_{eso_val}_{nep_val}"))
    header = random.choice(["⚙️ BEDAH MESIN NEURO-RELATIONSHIP", "📡 DEKODE SINYAL KOSMIK PASANGAN", "📜 LOGIKA ALGORITMA PENYATUAN EGO"])
    
    f_eso = random.choice([
        f"Fusi vibrasi dari nama <b>{n1}</b> dan <b>{n2}</b> bukan kebetulan matematis. Hasil ekstraksinya mengunci kuat di Frekuensi <b>{eso_val}</b>. Angka ini mencerminkan 'Wajah Ketiga'—yaitu bagaimana sirkel pertemanan dan orang luar menilai/merasakan aura kalian saat kalian berdua jalan bareng.", 
        f"Gesekan energi dari struktur huruf panggilan <b>{n1}</b> dan <b>{n2}</b> menciptakan pusaran resonansi di angka <b>{eso_val}</b>. Ini mendefinisikan *Soul Purpose* (Tujuan Gaib) kenapa semesta iseng mempertemukan kalian berdua di bumi ini."
    ])
    
    f_nep = random.choice([
        f"Hitungan benturan gravitasi lahir (Total Neptu <b>{nep_val}</b>) memetakan titik buta (*Blind Spot*) dari ego purba kalian berdua. Ini ibarat peta ranjau darat—titik-titik sensitif di mana konflik bodoh akan selalu meledak berulang kali kalau kalian nggak sadar.", 
        f"Analisa siklus tarikan kalender (Parameter Neptu <b>{nep_val}</b>) jadi radar pendeteksi stabilitas mental hubungan. Angka ini membongkar rahasia: Bagaimana wujud asli filter otak kalian saat lagi berantem hebat karena stres finansial/kerjaan."
    ])
    
    return f'<div class="info-metric-box"><b style="color:#FFD700; font-size:15px; letter-spacing:1px;">{header}:</b><br><br>• <b style="color:white;">TOTAL FREKUENSI ESOTERIK:</b><br><span style="color:#ccc; display:inline-block; margin-top:4px; margin-bottom:12px; font-size:14px;">{f_eso}</span><br>• <b style="color:white;">TOTAL BENTURAN NEPTU:</b><br><span style="color:#ccc; display:inline-block; margin-top:4px; font-size:14px;">{f_nep}</span></div>'

def proc_couple_persona(root_c, n1, n2):
    random.seed(generate_seed(f"cp_deep_{n1}_{n2}_{root_c}"))
    buka = random.choice([
        f"Hukum tarikan resonansi mencatat bahwa penyatuan DNA psikologis **{n1}** dan **{n2}** menghasilkan gelombang **Root {root_c}**.",
        f"Ketika ego **{n1}** dilebur dengan frekuensi **{n2}**, sistem mendeteksi lahirnya entitas baru yang terkunci di **Root {root_c}**."
    ])
    
    desc = {
        1: ("THE EMPIRE BUILDERS (Mesin Ambisi & Dominasi)", f"Penyatuan kalian berdua memancarkan aura Alpha yang sangat tajam dan intimidatif. Saat {n1} dan {n2} bersatu, obrolan kalian bukan lagi cuma urusan romansa *menye-menye*, melainkan ambisi mutlak untuk numpuk aset, ngejar target karir, dan naikin status sosial! Waspadai persaingan gengsi di atas kasur; jangan sampai kalian berdua berantem berebut setir kendali di rumah."),
        2: ("THE EMPATHIC RESONANCE (Telepati Batin Instan)", f"Selamat, kalian diberkahi dengan 'Wi-Fi Batin' berfrekuensi tinggi! Sangat mudah bagi {n1} maupun {n2} untuk tahu *mood* pasangan lagi jelek cuma dari dengerin helaan napas atau lirikannya, tanpa perlu nanya 'Kamu kenapa?'. Kekuatan gaib hubungan kalian adalah kemampuan menetralisir racun *anxiety* (kepanikan) satu sama lain saat dunia luar lagi gila."),
        3: ("THE MAGNETIC CHARM (Daya Tarik Keramaian)", f"Vibrasi gabungan kalian bertindak ibarat lampu sorot di tengah pesta. {n1} dan {n2} adalah tipe pasangan asik yang bisa ngidupin sirkel nongkrong yang tadinya garing jadi penuh tawa. Energi komunikasi gaul kalian sangat membius, bikin relasi bisnis, mertua, dan koneksi tingkat tinggi gampang kepincut buat bantuin kalian."),
        4: ("THE ARCHITECTS OF REALITY (Pondasi Baja Anti-Badai)", f"Hubungan kalian ini nggak dibangun di atas awan rayuan gombal yang gampang pudar, melainkan dipaku pake paku bumi di atas kerasnya realitas! Otak {n1} dan {n2} secara otomatis mikirin masa depan: cicilan rumah, tabungan anak, dan kesetiaan buta. Badai ekonomi sekencang apapun bakal susah ngerobohin akar kalian."),
        5: ("THE QUANTUM NOMADS (Pecandu Adrenalin & Kebebasan)", f"Kalian berdua ini bensin ketemu api! Rutinitas pacaran/nikah yang ngebosenin dan gitu-gitu aja adalah racun pembunuh buat hubungan ini. Cinta dan nafsu antara {n1} dan {n2} cuma bakal terus nyala gila-gilaan kalau kalian berdua rajin nyari *traveling* ekstrem, nyoba gaya baru, dan nolak nurut sama aturan tradisional keluarga."),
        6: ("THE SANCTUARY (Benteng Penampungan Emosi)", f"Kalian berdua adalah lambang pengayom tertinggi. Rumah tangga/hubungan {n1} dan {n2} bertindak layaknya 'Klinik Trauma'. Anehnya, bukan cuma kalian berdua yang saling nyembuhin luka masa lalu, tapi sirkel temen dan keponakan sering banget numpang nongkrong di kalian cuma buat nyari perlindungan batin dari stresnya hidup."),
        7: ("THE MYSTIC SYNERGY (Koneksi Spiritual Eksklusif)", f"Aura hubungan kalian sangat tertutup, misterius, dan punya kedalaman intelektual/obrolan malam yang *deep* banget, yang mana mustahil dimengerti sama temen-temen luarnya. {n1} dan {n2} jauh lebih milih mojok hening berdua ngomongin konspirasi alam semesta ketimbang validasi *flexing* di Instagram."),
        8: ("THE MATERIAL GRAVITY (Mesin Penyedot Uang Mutlak)", f"Catat ini: Kalau ego gengsi kalian berdua berhasil ditundukkan jadi satu visi, penyatuan {n1} dan {n2} adalah mesin pencetak kekayaan material yang brutal! Alam semesta merespons niat kalian dengan bukain pintu bos-bos besar. Tapi awas karma: Uang bisa berubah jadi alat ukur cinta kalau kalian lupa sama rasa syukur."),
        9: ("THE CONSCIOUS UNION (Pemutus Rantai Trauma)", f"Tingkat penerimaan batin kalian udah tembus level dewa, melampaui urusan fisik. {n1} dan {n2} secara mistis dipertemukan oleh Tuhan buat saling nyembuhin trauma parah (luka *Inner-Child*) asmara kalian di masa lalu. Interaksi kalian dipenuhi welas asih. Kalian adalah obat penawar bagi penderitaan satu sama lain.")
    }
    
    data = desc.get(root_c, ("UNCHARTED ANOMALY", "Entitas frekuensi tak tertebak."))
    return data[0], f"{buka} {data[1]}"

def proc_weton_kombo(sisa, n1, n2, z1, z2):
    random.seed(generate_seed(f"wt_deep_{n1}_{n2}_{sisa}_{z1}_{z2}"))
    do_list = {
        1: [f"Pake taktik psikologi *Pacing-Leading*. Pas dia mulai ngomel panas, TAHAN MULUT ANDA dari ngebantah! Validasi dulu emosinya (misal: 'Iya aku ngerti kamu capek...'), baru pelan-pelan suntikin logika Anda.", f"Wajib pake aturan *Time-Out*! Pas nada suara udah naik satu oktaf, langsung minggat 15 menit ke kamar sebelah. Biirin bagian otak hewan (Amygdala) si {z1} dan {z2} *cooling down* dulu biar nggak kelepasan ngomong kasar."],
        2: [f"Angkat derajat {n2} sebagai rekan setara (*Mastermind Partner*). Haram hukumnya ngambil keputusan bisnis/duit gede diam-diam di belakang dia! Libatkan dia, karena rezeki gaib kalian ngalir dari restu dia.", f"Bangun keakraban (*Rapport*) batin dengan pujian mikroskopis. Jangan nunggu dia ngasih kejutan baru dipuji. Puji hal sepele yang dilakuin {n1} tiap hari. Wibawa ranjang dan dompet kalian mekar dari validasi sepele ini."],
        3: [f"Kejutkan otaknya! Suntikin *Pattern Interrupt* (Pola Perusak Rutinitas). Ganti rute pulang, *booking* hotel dadakan, atau lakuin hal absurd berdua. Kalau sirkuit dopamin (hormon *happy*) kalian mati rasa, cinta bisa garing seketika.", f"Jadwalin sesi *Deep-Talk* (obrolan dari hati ke hati) tanpa pegang HP sama sekali sebulan sekali. Bedah ulang kecemasan masa depan bareng-bareng buat mastiin frekuensi batin kalian nggak belok."],
        4: [f"Gunakan ilmu *Reframing* (Ubah Sudut Pandang) pas kalian lagi dihantam badai krisis (misal: bokek/utang). Ganti *mindset* dari 'Gara-gara kamu kita gini' jadi 'KITA BERDUA vs Dunia/Masalah Ini'. Rapatkan barisan pelindung!", f"Sadari ilmu tempa baja: Badai cekcok mulut di awal hubungan/adaptasi ini cuma tes ombak dari Semesta buat ngetes mental kalian. Telen gengsi Anda! Ini tiket masuk VIP menuju pintu kelimpahan materi."],
        5: [f"Gelar sesi transparansi duit secara telanjang. Bicarain cicilan, utang, dan target aset tanpa ada yang ditutup-tutupin. Sinkronisasi getaran rasa syukur berdua adalah tombol rahasia penyedot rezeki kalian.", f"Jadilah jangkar emosi (*Emotional Anchor*)! Pas salah satu dari kalian mentalnya lagi jatuh/pesimis parah soal masa depan, tugas mutlak pasangannya buat nyuci otaknya lagi biar balik sadar dan optimis."],
        6: [f"Kasih 'Jarak Napas' (*Space*) sejenak waktu urat leher udah mulai tegang. Otak kalian berdua itu ibarat pake kacamata yang beda warna; Anda liat merah, dia liat hijau. Pas sadar mulai miskomunikasi, mundur selangkah biar nggak meledak.", f"Jadikan selera humor *absurd* receh sebagai obat penawar racun ego. Pas kalian lagi debat tegang berjam-jam sampe sesak napas, ledakan tawa konyol dadakan sangat sakti buat ngereset saraf otak yang tegang."],
        7: [f"Kunci komunikasi: Harus berbasis FAKTA INDRAWI, bukan nebak pikiran. Kalau ragu, wajib nanya: 'Tadi maksud muka kamu cemberut gitu marah ke aku atau capek kerja?'. Bunuh bibit cemburu buta sebelum jadi naga!", f"Banjiri pasangan Anda pakai *Love Language* (Bahasa Cinta) utamanya! Perbanyak sentuhan kulit (*Physical Touch*) atau kasih hadiah kecil buat membungkam suara *insecurity* gaib di kepala pasangan yang suka curigaan."],
        8: [f"Lawan kebosanan mati rasa dengan adrenalin! Hubungan kalian saking amannya sampe rawan hampa dan garing. Cari proyek bisnis nekat atau lakuin hobi baru bareng yang bikin jantung deg-degan biar *spark*-nya nyala lagi.", f"Jangan biarin rasa aman yang monoton nidurin insting pemburu Anda! Tetep jaga *grooming* (penampilan fisik) dan lakuin *upgrade* diri, biar pasangan terus punya alasan buat ngerasa kagum tiap pagi."]
    }
    dont_list = {
        1: [f"DILARANG KERAS ngelakuin *Mind-Reading* negatif (Sok Cenayang)! Haram hukumnya Anda mikir '{n2} sengaja nyuekin gue biar gue menderita' tanpa nanya langsung alasan aslinya.", f"Pantang bikin konfrontasi beda pendapat pas kalian lagi mode *H.A.L.T* (Lapar, Marah, Kesepian, Kecapekan). Logika lagi tumpul, yang bakal debat cuma ego binatang buas di kepala kalian."],
        2: [f"Jauhi jebakan 'Pencitraan Sempurna' di Instagram! Jangan pencitraan keliatan *couple goals* di luar, padahal pas di mobil kalian saling diam-diaman dingin. Kepalsuan ini bakal nebas wibawa hoki kalian.", f"Dilarang keras ngasih celah buat ibu mertua, ipar, atau bestie buat ikut campur ngatur ritme aturan rumah tangga/pacaran kalian! Bos pengambil keputusan absolut cuma boleh kalian berdua."],
        3: [f"Awas masuk perangkap *Comfort Zone* (Zona Nyaman Bikin Miskin). Mentang-mentang udah nyaman rebahan bareng, jangan sampe kalian berdua jadi males ngambis ngejar cuan dan karir karena ngerasa 'cinta aja cukup'.", f"Dilarang cuek bebek sama perawatan fisik cuma gara-gara ngerasa udah 'laku' dan dapet hatinya {n1}. Hilangnya daya tarik visual bisa ngebunuh gairah selera secara perlahan tapi pasti."],
        4: [f"Jangan pernah pake masa lalu yang kelam atau gengsi ego Anda sebagai pisau buat nikam harga diri {n2} pas lagi emosi. Adaptasi ini nuntut Anda ngebakar watak *toxic* lama buat bertahan hidup.", f"Pantang ngomong kata 'Putus/Cerai' secapek apapun Anda di masa transisi awal ini. Ngancem bubaran pas lagi kesetanan emosi adalah bom nuklir yang bakal ngancurin pondasi *Trust* selamanya."],
        5: [f"Haram hukumnya jadiin nominal duit masuk sebagai satu-satunya lem perekat nyawa hubungan {n1} dan {n2}. Kalau fondasi spiritual dilupain, duit miliaran malah bakal ngebakar mental kalian berdua.", f"Awas Virus Kesombongan Bawah Sadar! Dilarang keras ngeremehin orang gembel atau saingan bisnis pas pintu duit kalian berdua lagi meledak kebuka. Sombong dikit, keran berkah diputus seketika sama Yang Di Atas."],
        6: [f"Catat baik-baik: Kalau lagi ngamuk, DILARANG KERAS nyerang kekurangan fisik ( *body shaming* ), ngungkit aib keluarga, atau nginjak harga diri paling dalam si {n2}. Mau marah silahkan, tapi martabat pantang diinjak!", f"Hindari pake senjata *Silent Treatment* (Bungkam seribu bahasa berminggu-minggu) buat ngehukum dia! Ini bukan mendidik, tapi ini bentuk manipulasi mental sadis yang nyiptain luka trauma dalam."],
        7: [f"DILARANG PAKE kata-kata sapu jagat pas lagi berantem, misal: 'Kamu SELALU egois!' atau 'Kamu NGGAK PERNAH ngertiin!'. Kalimat ini adalah *virus* NLP yang bikin otak pasangan langsung mode perang defensif.", f"Jangan turun kasta jadi detektif abal-abal yang diem-diem ngorek isi WhatsApp atau DM Instagram pasangan. Penyakit *Trust Issue* (curigaan parah) adalah kanker stadium 4 pembunuh kedamaian batin."],
        8: [f"Waspadai virus *Take it for granted* (Ngerasa dia nggak bakal kemana-mana)! Dilarang stop ngasih *effort* (usaha mati-matian) buat naklukin hatinya {n2} layaknya waktu pertama kali ngejar dulu.", f"Jangan biarin rutinitas mesin robot (bangun-kerja-pulang-tidur) matiin insting keromantisan liar Anda. Kasur yang dingin butuh dipancing pake kejutan-kejutan nakal biar energi kehidupan nggak lumutan."]
    }
    hasil = {
        1: ("💔 SINDROM PEGAT (Ranjau Ujian Ego Fatal)", "Kalkulasi membaca perbedaan arsitektur otak yang sangat tajam dalam cara kalian merespons stres. Ibarat dua kutub magnet yang sama-sama dominan, kalian bakal sering tabrakan adu argumen keras yang bisa melukai harga diri terdalam kalau gengsi nggak buruan ditekuk."),
        2: ("👑 RESONANSI RATU (Pancaran Kharisma Level Atas)", "Bawaan energi kalian berdua ini sangat berkelas! Ada magnet gaib yang bikin kolega kerja, mertua, dan sirkel sosial kalian otomatis naruh *respect* dan segan ngeliat wibawa kalian berdua pas lagi bareng. Cocok banget buat merintis *empire* bisnis gabungan."),
        3: ("💞 FREKUENSI JODOH (Klik Jiwa Instan)", "Koneksi batin kalian nggak perlu dipaksa. Ada tingkat kemistri bawah sadar yang *deep* banget, seolah cetak biru (*Blueprint*) jiwa kalian berdua udah pernah terikat di kehidupan sebelumnya. Perbedaan nyebelin apapun bakal gampang dicarikan komprominya."),
        4: ("🌱 FASE TOPO (Ujian Transmutasi Kepompong)", "Ibarat ulat gatal yang lagi proses hancur jadi kupu-kupu dalam kepompong! Fase awal penyatuan kalian dijamin penuh gesekan adaptasi emosi yang bikin kepala mau pecah. Tapi ingat: kalau ego kalian berdua *survive* ngelewatin krisis ini, fondasi baja kalian di masa depan mustahil bisa dijebol badai/pelakor."),
        5: ("💰 ALGORITMA TINARI (Sistem Penyedot Rezeki)", "Bersyukurlah! Entitas persatuan kalian berdua memancarkan frekuensi pemanggil kelimpahan duit kelas kakap. Coba perhatiin, banyak kemacetan rezeki atau hutang masa lalu yang pelan-pelan mendadak lunas dan terbuka pintu cuannya sejak kalian memutuskan serius bersatu."),
        6: ("⚡ FRIKSI PADU (Benturan Filter Realitas)", "Sistem NLP mendeteksi adanya *noise* (kebisingan statis) di cara kalian ngobrol. Bersiaplah ngadepin debat kusir yang repetitif (diulang-ulang). Ini bukan karena kalian nggak cinta, tapi murni karena filter kacamata otak kalian beda warna; yang satu liat realita sebagai angka logis, yang satu baperan pake perasaan."),
        7: ("👁️ JEBAKAN SUJANAN (Ilusi Paranoid Cemburu Buta)", "Waspada! Vibrasi penyatuan ini secara aneh punya sifat 'menarik fitnah' dan kesalahpahaman konyol. Bakal banyak banget asumsi ilusi (pikiran curiga yang nggak nyata) yang nebak-nebak di kepala kalian, yang ujungnya bikin kalian berantem hebat gara-gara masalah yang aslinya nggak ada."),
        8: ("🕊️ ANCHOR PESTHI (Zona Kedamaian Anti-Stres)", "Selamat, kehadiran fisik satu sama lain adalah 'Oasis' di tengah padang pasir kerasnya hidup. Kalian adalah netralisir racun hormon stres (Kortisol) bagi pasangan. Relasi ini jalannya bakal adem ayem banget, minim drama sinetron, dan sangat stabil ngejaga kewarasan mental.")
    }
    return hasil[sisa][0], hasil[sisa][1], random.choice(do_list[sisa]), random.choice(dont_list[sisa])

KAMUS_ABJAD = {'a': 1, 'b': 2, 'j': 3, 'd': 4, 'h': 5, 'w': 6, 'z': 7, 't': 9, 'y': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 's': 60, 'f': 80, 'q': 100, 'r': 200, 'c': 3, 'e': 5, 'g': 1000, 'i': 10, 'o': 6, 'p': 80, 'u': 6, 'v': 6, 'x': 60}
def hitung_nama_esoterik(nama): return sum(KAMUS_ABJAD.get(h, 0) for h in ''.join(filter(str.isalpha, str(nama).lower()))) or 1
def get_rincian_esoterik(nama):
    r = [f"{h.upper()}({KAMUS_ABJAD.get(h,0)})" for h in ''.join(filter(str.isalpha, str(nama).lower())) if KAMUS_ABJAD.get(h,0)>0]
    return " + ".join(r) if r else "0"

def generate_dynamic_reading(total_jummal):
    mod = total_jummal % 4 if total_jummal % 4 != 0 else 4
    el = {1: ("🔥 API (Nar)", "Sistem saraf eksekusi cepat, sumbu pendek, dan berjiwa pelopor yang nggak takut nabrak aturan."), 2: ("🌍 TANAH (Turab)", "Pola pikir sangat realistis, keras kepala pada prinsip, dan fokus mutlak pada stabilitas harta/aset."), 3: ("💨 UDARA (Hawa)", "Mesin otak yang liar memproduksi ide, gampang bosan, lihai beradaptasi, dan pintar merayu (persuasif)."), 4: ("💧 AIR (Ma')", "Radar emosi tingkat tinggi, fleksibel ngikutin arus masalah, tapi bisa mematikan kalau udah ngamuk dari dalam.")}
    p_red = " + ".join(list(str(total_jummal)))
    s_red = sum(int(d) for d in str(total_jummal))
    r_num = s_red
    while r_num > 9: r_num = sum(int(d) for d in str(r_num))
    r_dict = {1:"Pencipta jalan baru & Dominator", 2:"Penyelaras harmoni batin & Negosiator", 3:"Penyampai pesan & Manipulator persepsi publik", 4:"Pembangun fondasi logika & Arsitek SOP", 5:"Agen transformasi & Penantang risiko ekstrem", 6:"Pengayom sejati & Pelindung sirkel ring-1", 7:"Pencari esensi spiritual & Analis data tingkat dewa", 8:"Pemegang otoritas kemudi & Mesin penyedot duit", 9:"Kesadaran universal spiritual & *Healer* luka masa lalu"}
    
    m_note = "<div style='background:rgba(212,175,55,0.1); padding:15px; border-radius:8px; border-left: 4px solid #FFD700; margin-top:15px; margin-bottom:15px; box-shadow: 0 4px 15px rgba(212,175,55,0.2);'><span style='color:#FFD700; font-size:16px; letter-spacing:1px; font-weight:900;'>⚡ ANOMALI KODE MASTER TERDETEKSI!</span><br><span style='color:#e0e0e0; font-size:14px; line-height:1.6; display:inline-block; margin-top:5px;'>Sistem membaca adanya lonjakan vibrasi gaib positif (Angka Master) pada inti identitas Anda. Radar indra ke-6 Anda sedang *on-fire* (terbuka lebar) di gelombang otak Theta hari ini. Firasat aneh, bisikan hati nurani, atau tebakan acak yang muncul di kepala Anda detik ini bukanlah halusinasi—itu adalah bocoran *cheat code* dari *Higher Self* Anda! Matikan sejenak logika pintar Anda, dan ikuti kompas batin tersebut buat ngeksekusi proyek penting hari ini!</span></div>" if any(m in str(total_jummal) for m in ["11","22","33"]) else ""
    return el[mod][0], el[mod][1], p_red, s_red, r_num, r_dict.get(r_num,""), m_note

def hitung_angka(tanggal):
    try:
        t = sum(int(digit) for digit in tanggal.strftime("%d%m%Y"))
        while t > 9: t = sum(int(digit) for digit in str(t))
        return t
    except: return 1

def get_rincian_tanggal(tanggal):
    try:
        ts = tanggal.strftime("%d%m%Y")
        p = f"{' + '.join(list(ts))} = {sum(int(d) for d in ts)}"
        t = sum(int(d) for d in ts)
        while t > 9:
            p += f" ➡ {' + '.join(list(str(t)))} = {sum(int(d) for d in str(t))}"
            t = sum(int(d) for d in str(t))
        return p
    except: return "1 = 1"

def hitung_neptu_langsung(hari, pasaran): return {"Minggu":5,"Senin":4,"Selasa":3,"Rabu":7,"Kamis":8,"Jumat":6,"Sabtu":9}.get(hari,0) + {"Legi":5,"Pahing":9,"Pon":7,"Wage":4,"Kliwon":8}.get(pasaran,0)

dynamic_users = get_dynamic_count()

# --- SIDEBAR PROMOSI & LOGIN ---
with st.sidebar:
    if os.path.exists("baru.jpg.png"):
        try: st.image("baru.jpg.png", use_container_width=True); st.markdown("<br>", unsafe_allow_html=True)
        except: pass
 
    st.markdown(f"### {get_greeting()}")
    st.markdown("---")
    st.markdown("### 🔓 Akses Premium")
    if not st.session_state.premium:
        kode_input = st.text_input("Punya Kode Akses? Ketik di sini:", type="password")
        if kode_input:
            if kode_input.upper() == "NEUROVIP": 
                st.session_state.premium = True
                st.toast("Akses Terbuka! Selamat Datang di Mode VIP.", icon="👑")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Kode Salah atau Kadaluarsa.")
        st.markdown("<p style='font-size:13px; color:#888;'>Dapatkan Kode Akses via <a href='https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy.' target='_blank' style='color:#25D366; font-weight:bold; text-decoration:none;'>WhatsApp</a></p>", unsafe_allow_html=True)
    else:
        st.success("👑 Status: VIP MEMBER")
        if st.button("Logout"):
            st.session_state.premium = False
            st.rerun()
    
    st.markdown("---")
    st.markdown("""<div style='background: linear-gradient(135deg, #ff0000 0%, #8b0000 100%); padding: 18px; border-radius: 10px; text-align: center; border: 1px solid #ff4b4b; box-shadow: 0 5px 15px rgba(255,0,0,0.3);'>
<b style='color: white; font-size: 16px; letter-spacing: 1px;'>🔥 BUTUH ANALISA LEBIH DALAM?</b><br>
<span style='color: #ccc; font-size: 12px; display:block; margin-top:5px;'>Beberapa hasil (Blok Mental Spesifik) tidak bisa ditampilkan di sistem terbuka.</span>
<span style='color: #FFD700; font-size: 13px; display:inline-block; margin-top:5px; margin-bottom:12px;'>Konsultasi Private dengan Coach (Slot Terbatas)</span><br>
<a href='https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20butuh%20sesi%20kalibrasi%20private%20hari%20ini' target='_blank' style='background: #25D366; color: white; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-weight: 900; font-size: 14px; display: inline-block; box-shadow: 0 4px 10px rgba(37,211,102,0.4);'>💬 KLIK DI SINI SEKARANG</a>
</div>""", unsafe_allow_html=True)
    st.markdown("<br><center><small style='color:#666;'>© 2026 Neuro Nada Academy</small></center>", unsafe_allow_html=True)

# --- INTERFACE UTAMA ---
if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass

cur_planet, cur_instr, cur_color = get_planetary_hour()
st.markdown(f"""<div style='text-align: right;'><div class='live-badge' style='background: {cur_color};'>🕒 LIVE PLANET: {cur_planet.upper()}</div><div style='font-size: 11px; color: #888; margin-top: 5px;'>{cur_instr}</div></div>""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900; color:#FFD700;'>🌌 BUKA KODE HIDUP ANDA HARI INI</h1>", unsafe_allow_html=True)
st.markdown("""<p style='text-align: center; font-size: 16px; color: #ccc;'>Ini bukanlah Ramalan dukun konvensional. Ini adalah pemetaan presisi tinggi berdasarkan cetak biru nama (Sandi Frekuensi), garis waktu kelahiran (Meta-Program NLP Otak), dan *real-time* bioritme planet Anda.<br><br><b style='color:#FFF;'>⚡ Dalam 10 detik, Anda akan meretas:</b><br><span style='color:#D4AF37;'>• Fluktuasi momentum rezeki & cuan hari ini<br>• Celah *Blind Spot* yang HARUS dieksekusi sekarang juga<br>• Virus sabotase mental bawah sadar yang WAJIB dihindari</span></p>""", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; margin-bottom:20px;'><span style='background:rgba(255,75,75,0.2); color:#ff4b4b; padding:8px 15px; border-radius:5px; font-size:13px; font-weight:bold; letter-spacing:1px;'>⚠️ PERINGATAN: Jangan teruskan jika mental Anda belum siap menghadapi cermin kebenaran ego Anda yang ditelanjangi oleh sistem ini.</span></div>", unsafe_allow_html=True)
st.markdown("---")
 
tgl_today = datetime.date.today()
tab1, tab2, tab5, tab3, tab6, tab4 = st.tabs(["👤 Personal Identity", "👩‍❤️‍👨 Couple Matrix 🔒", "⏱️ Quantum Engine 🔒", "🌌 Falak Ruhani 🔒", "📚 Neuro-Insights", "❓ FAQ & Disclaimer"])
 
# ==========================================
# TAB 1: IDENTITAS KOSMIK
# ==========================================
with tab1:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#fff;'>👇 Masukkan parameter Anda sekarang untuk di-decode</h4>", unsafe_allow_html=True)
    nama_user = st.text_input("Nama Lengkap Sesuai Identitas Asli:", placeholder="Ketik nama lengkap Anda di sini...", key="t1_nama")
    
    col_tgl, col_wt = st.columns(2)
    with col_tgl:
        st.write("📅 **Data Masehi:**")
        # FIXED DATE DEFAULT (1995-01-01) & WIDE RANGE (1930)
        tgl_input = st.date_input("Tanggal Lahir", value=datetime.date(1995, 1, 1), min_value=datetime.date(1930, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")
    with col_wt:
        st.write("📜 **Data Weton:**")
        hari_input = st.selectbox("Hari Kelahiran", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4, key="h_t1")
        pasaran_input = st.selectbox("Pasaran Kelahiran", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=2, key="p_t1")
    st.markdown("</div>", unsafe_allow_html=True)
 
    if st.button("🚀 Retas Sabotase Otak Saya Hari Ini", key="btn_t1"):
        if not nama_user or len(nama_user.strip()) < 3: 
            st.error("🚨 Filter Keamanan: Mohon ketik nama lengkap Anda (minimal 3 karakter).")
        else:
            try:
                with st.spinner('Menyelaraskan *mapping* frekuensi kosmik dengan arsitektur NLP otak Anda...'): time.sleep(1.5)
                st.toast("Kalibrasi sukses! Tembok bawah sadar Anda berhasil dijebol sistem.", icon="⚡")
                
                safe_name = get_safe_firstname(nama_user)
                angka_hasil = hitung_angka(tgl_input)
                rincian_tgl = get_rincian_tanggal(tgl_input)
                nilai_jummal = hitung_nama_esoterik(nama_user)
                rincian_jummal = get_rincian_esoterik(nama_user)
                el_nama, el_desc, p_reduk, s_reduk, r_num, r_desc, m_note = generate_dynamic_reading(nilai_jummal)
                nep = hitung_neptu_langsung(hari_input, pasaran_input)
                wet = f"{hari_input} {pasaran_input}"
                zod = get_zodiak(tgl_input)
                n_laku, d_laku, arah_naga = get_betaljemur_data(nep, hari_input)
                rezeki_data, usaha_data = get_rezeki_usaha(nep)
                punchy = arketipe_punchy.get(angka_hasil, arketipe_punchy[1])
                desk_ark_dinamis = proc_arketipe(safe_name, angka_hasil, zod, nep)
                shadow = proc_shadow_list(safe_name, angka_hasil)
                
                aksi_list = [
                    f"Jebol kebuntuan mental Anda hari ini. Segera ambil HP dan hubungi satu prospek, klien, atau koneksi kunci yang selama ini penanganannya Anda tunda terus-terusan cuma karena gengsi atau rasa takut ditolak.",
                    f"Lakukan 'Sapu Bersih' energi otak. Identifikasi dengan jujur lalu hentikan SATU interaksi pertemanan atau tugas repetitif hari ini yang diam-diam nyedot kewarasan jiwa Anda tanpa ngasih profit.",
                    f"Praktikkan delegasi (lempar tugas) secara radikal! Ada satu beban teknis remeh yang selama ini nahan omset besar Anda. Lepaskan ego *Superman* Anda dan suruh orang lain yang ngerjain hari ini juga."
                ]
                aksi_teks = random.choice(aksi_list)
                core_shadow_raw = shadow[0]
                core_shadow_title = core_shadow_raw.split("**")[1].replace(":", "") if "**" in core_shadow_raw else core_shadow_raw.split(":")[0]
                
                st.markdown(f"""<div class="soft-fade" style="background: rgba(255,215,0,0.1); border-left: 5px solid #FFD700; padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid rgba(255,215,0,0.3);">
<h3 style="margin-top:0; color:#FFD700; font-weight:900; letter-spacing:1px;">🎯 HASIL KEPUTUSAN SISTEM HARI INI</h3>
<ul style="font-size: 16px; line-height: 1.8; color: #fff; list-style-type: none; padding-left: 0;">
<li style="margin-bottom: 15px; background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px;">
💰 <b>STATUS REZEKI (<span style='color:#FFD700;'>{rezeki_data[0].split('(')[0].strip()}</span>):</b><br>
<span style='color:#25D366; font-weight:bold; font-size:15px;'>MOMENTUM UANG AKTIF.</span> <span style="color:#e0e0e0; font-size:14px; line-height:1.7;">{rezeki_data[1]}</span>
</li>
<li style="margin-bottom: 15px; background: rgba(37,211,102,0.1); border-left: 4px solid #25D366; padding: 15px; border-radius: 8px;">
⚡ <b>INSTRUKSI TINDAKAN FISIK (WAJIB):</b><br>
<span style="color:#e0e0e0; font-size:14px; line-height:1.7;">{aksi_teks}</span>
</li>
<li style="margin-bottom: 10px; background: rgba(255,75,75,0.1); border-left: 4px solid #ff4b4b; padding: 15px; border-radius: 8px;">
🚫 <b>RED FLAG (PANTANGAN HARAM):</b><br>
<span style="color:#ff4b4b; font-size:14px; font-weight:bold;">Waspadai letupan {core_shadow_title}!</span><br>
<span style="color:#e0e0e0; font-size:14px; line-height:1.7;">Sistem membaca celah kelemahan ego Anda lagi terbuka lebar hari ini. Tahan kuat-kuat dorongan panik impulsif atau gengsi buta Anda sebelum mutusin tanda tangan kontrak, mutusin asmara, atau transfer duit puluhan juta.</span>
</li>
</ul>
<div style="background: rgba(255,75,75,0.2); padding: 8px 15px; border-radius: 5px; display: inline-block; margin-top: 10px;">
<b style="color:#ff4b4b; font-size:13px;">⏳ Fluktuasi algoritma nasib ini cuma dijamin valid hingga pergantian siklus (24 jam ke depan). Action sekarang.</b>
</div>
</div>""", unsafe_allow_html=True)
                
                if not st.session_state.premium:
                    st.markdown(f"""<div class="glass-container soft-fade" style="text-align:center; border: 2px solid #ff4b4b; padding: 30px 20px;">
<h3 style="color:#ff4b4b; margin-top:0;">🔓 Anda baru aja ngintip 15% dari hasil rahasia *Decoding* Anda...</h3>
<div style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: left; display: inline-block;">
<span style="color:#ccc; font-size: 15px;">Di dalam zona Premium (Tanpa Sensor):</span><br>
<b style="color:#fff;">• Blueprint kepribadian terdalam & Arsitektur Rahasia Ego Anda yang selama ini ngumpet</b><br>
<b style="color:#fff;">• 3 Titik Penyakit Mental Beracun (Shadow) yang diem-diem selalu mensabotase omset bisnis Anda</b><br>
<b style="color:#fff;">• Kompas Arah Mata Angin (Naga Dina) gaib penarik hoki hari ini</b><br>
<b style="color:#fff;">• Tab Matrix Pasangan: Bongkar cocok/hancurnya ego Anda pas disatuin sama si 'Dia'</b>
</div>
<p style="color:#FFD700; font-size: 16px;"><b>🔥 Catat ini: Laporan setajam ini mustahil Anda temukan di dukun *Google* gratisan.<br>Ini murni bedah *mindset* PERSONAL — cuma buat Anda doang.</b></p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy." target="_blank" style="text-decoration:none;">
<div class="cta-button" style="font-size:18px; margin-top: 10px;">🚀 SIKAT, AKTIFKAN FULL REPORT SEKARANG!</div>
</a>
<p style="font-size:14px; color:#ccc; margin-top:15px; margin-bottom: 5px;">Investasi Receh: <b>Cuma Rp 19.000</b><br><i style="color:#888;">(Harga perkenalan platform beta. Anda bebas akses ngecek siapapun selama 1 bulan penuh.)</i></p>
<span style="background:rgba(255,75,75,0.2); color:#ff4b4b; padding:4px 10px; border-radius:3px; font-size:12px; font-weight:bold;">⚠️ Harga sistem diprogram naik otomatis menyesuaikan *traffic* *server* besok.</span>
<div style="margin-top: 25px; border-top: 1px dashed #555; padding-top: 15px;">
<span style="font-size:14px; color:#25D366; font-weight:bold;">🔥 {dynamic_users} bos-bos dan profesional udah nge-kalibrasi nasib mereka di sini.</span><br>
<span style="font-size:13px; color:#888;">Keluar dari kebingungan konyol Anda hari ini juga.</span>
</div>
</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h3 style='text-align:center;'>🌌 Laporan Intelijen Pribadi: {safe_name}</h3>", unsafe_allow_html=True)
                    st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Nilai Esoterik Nama</div><div class="matrix-value matrix-value-special">{nilai_jummal}</div></div><div class="matrix-item"><div class="matrix-label">Elemen Inti Jiwa</div><div class="matrix-value">{el_nama.split(' ')[1] if len(el_nama.split(' '))>1 else el_nama}</div></div><div class="matrix-item"><div class="matrix-label">OS Otak (Meta-Program)</div><div class="matrix-value matrix-value-special">KODE {angka_hasil}</div></div><div class="matrix-item"><div class="matrix-label">Filter Zodiak</div><div class="matrix-value">{zod}</div></div><div class="matrix-item"><div class="matrix-label">Gravitasi Weton</div><div class="matrix-value">{wet} ({nep})</div></div></div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"""<div class="dynamic-reading-box soft-fade"><h4 style="color: #FFD700; margin-top:0;">🔍 Dekoding Arsitektur Mesin Diri (DNA Numerologi)</h4><p><b>1. Sandi Esoterik Nama (Aura Tarikan Hoki):</b><br><code style="color:#25D366; background:transparent; padding:0; font-size:15px;">{rincian_jummal} = <b>{nilai_jummal}</b></code></p><ul style="margin-left: -15px; margin-bottom: 20px; color:#ccc; line-height:1.7;"><li><b>Mesin Bawah Sadar:</b> {el_nama} - <i>{el_desc}</i></li><li><b>Tujuan Diciptakan (Root Purpose):</b> {p_reduk} = {s_reduk} ➡ <b>{r_num}</b> ({r_desc})</li></ul><p><b>2. Sandi Garis Waktu Lahir (Meta-Program NLP Otak):</b><br><code style="color:#FFD700; background:transparent; padding:0; font-size:15px;">{rincian_tgl}</code><br><span style="font-size:14px; color:#ccc; display:inline-block; margin-top:8px; line-height:1.7;">Ekstraksi ekstrem di atas nge-gembok rahasia Anda pada <b>KODE {angka_hasil}</b>. Ingat, angka final ini bukan tebak-tebakan ramalan bintang abal-abal! Ini adalah wujud kerangka *Blueprint* (cetak biru) genetik yang ngejelasin secara *logis* gimana cara otak <b>{safe_name}</b> memproses informasi kalau lagi stres dikejar target, filter penerimaan *bullshit* dari orang, dan gaya Anda ngambil keputusan finansial sejak bayi di perut ibu.</span></p>{m_note}</div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"""<div class="primbon-box soft-fade"><div style="text-align:center; border-bottom:1px solid #D4AF37; padding-bottom:10px; margin-bottom:15px;"><span style="color:#D4AF37; font-size:14px; font-weight:900; letter-spacing:2px;">📜 ALGORITMA NUSANTARA: BETALJEMUR ADAMMAKNA</span></div>
<div style="font-size:15px; line-height:1.7; margin-bottom: 20px;"><b style="color:#FFF; font-size:18px; letter-spacing:1px;">{n_laku}</b><br><i style="color:#ccc; display:inline-block; margin-top:5px;">{d_laku}</i></div>
<div style="font-size:15px; line-height:1.7; margin-bottom: 20px; border-top: 1px dashed #555; border-bottom: 1px dashed #555; padding-top: 15px; padding-bottom: 15px;">
• <b style="color:#FFF;">Siklus Uang Beredar (<span style="color:#FFD700;">{rezeki_data[0]}</span>):</b><br><span style="color:#ccc; display:inline-block; margin-top:5px; margin-bottom:12px;">{rezeki_data[1]}</span><br>
• <b style="color:#FFF;">Radar Sektor Cuan (<span style="color:#25D366;">{usaha_data[0]}</span>):</b><br><span style="color:#ccc; display:inline-block; margin-top:5px;">{usaha_data[1]}</span>
</div>
<div style="font-size:15px; line-height:1.7; background: rgba(212,175,55,0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700;">
<span style="color:#FFD700;">🧭 <b>NAGA DINA (Kompas Geomansi Hari {hari_input}):</b></span> <b style="font-size: 18px; color:#FFF;">{arah_naga}</b><br>
<i style="color:#e0e0e0; font-size:14px; display:inline-block; margin-top:8px;">*PRAKTIK LAPANGAN: Kalau Anda mau *closing* kontrak puluhan juta, ngirim email lamaran penting, nembak cewek, atau mimpin *meeting* alot hari ini, posisikan kursi/tubuh fisik Anda menghadap ke <b>{arah_naga}</b>! Ini bukan klenik, ini ilmu penyelarasan magnetik kuno untuk menembus 'Blind Spot' hambatan energi di ruang kerja Anda. Buktikan hasilnya.</i>
</div></div>""", unsafe_allow_html=True)
                    
                    st.markdown(f"<h3 style='margin-bottom:5px;'>👁️ Telanjang Kepribadian: Bedah Psikologi {safe_name}</h3>", unsafe_allow_html=True)
                    st.info(f"Sistem telah meretas tuntas topeng pencitraan Anda. Arsitektur mental terdalam (Arketipe) Anda tidak bisa bohong, terkunci mutlak sebagai:\n\n### **{punchy['inti']}**")
                    st.markdown(f"<p style='font-size:15px; line-height:1.7; color:#ccc; margin-bottom:25px;'>{desk_ark_dinamis}</p>", unsafe_allow_html=True)
                    
                    c_kekuatan, c_shadow = st.columns(2)
                    with c_kekuatan:
                        st.markdown(f"🔥 <b style='color:#FFF; font-size:16px;'>SENJATA UTAMA PENCETAK UANG:</b>", unsafe_allow_html=True)
                        st.markdown(f"<ul class='list-punchy' style='color:#25D366; line-height:1.7;'><li>{punchy['kekuatan'][0]}</li><li style='margin-top:8px;'>{punchy['kekuatan'][1]}</li><li style='margin-top:8px;'>{punchy['kekuatan'][2]}</li></ul>", unsafe_allow_html=True)
                    with c_shadow:
                        st.markdown(f"⚠️ <b style='color:#FFF; font-size:16px;'>SHADOW (VIRUS PARASIT BAWAH SADAR):</b>", unsafe_allow_html=True)
                        st.markdown(f"<ul class='list-punchy' style='color:#ff4b4b; line-height:1.7;'><li><span style='color:#e0e0e0'>{shadow[0]}</span></li><li style='margin-top:10px;'><span style='color:#e0e0e0'>{shadow[1]}</span></li><li style='margin-top:10px;'><span style='color:#e0e0e0'>{shadow[2]}</span></li></ul>", unsafe_allow_html=True)
                
            except Exception as e: st.error(f"Sistem gagal melakukan komputasi otak tingkat tinggi: {e}")
 
# ==========================================
# TAB 2: COUPLE MATRIX
# ==========================================
with tab2:
    if not st.session_state.premium:
        st.markdown(f"""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h3 style='color: #ff4b4b; font-weight: 900; margin-top:0;'>💞 KALIBRASI PERANG EGO BAWAH SADAR</h3>
<p style='color: #ccc; font-size: 16px; margin-bottom: 20px;'>Bongkar habis-habisan rahasia ketidakcocokan Anda dengan si 'Dia'. Sebenernya status hubungan bisnis/asmara ini apa sih?<br><b style='color:#ff4b4b;'>❤️ Pertemuan Jodoh Pilihan Tuhan?</b> | <b style='color:#FFD700;'>⚡ Cuma Kawah Ujian Kesabaran Mental?</b> | <b style='color:#888;'>💔 Atau Bom Waktu Berdarah yang Tinggal Nunggu Meledak?</b></p>
<p style='font-size: 14px; color: #aaa; margin-bottom: 30px;'>Ketik 2 nama (pasangan asmara atau bos/rekan bisnis) dan temukan di titik mana argumen konyol kalian selalu mentok muter-muter aja.<br><i style='color:#ff4b4b;'>⚠️ Warning Keras: Hasil algoritma *engine* ini sangat telanjang, kasar, dan *to-the-point* nonjok ego. Jangan nangis kalau nggak kuat liat kenyataannya!</i></p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy." target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 SIKAT, MINTA KODE AKSES VIA WA (Rp 19.000)</div>
</a>
<p style='font-size:13px; color:#25D366; font-weight:bold; margin-top:15px;'>🔥 Akses ini udah satu paket di dalam VIP Member 1 Bulan.</p>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("💞 Penyatuan Esoterik & Benturan Betaljemur (Couple Matrix)")
        ca, cb = st.columns(2)
        with ca: 
            st.markdown("<h4 style='color:#FFD700;'>Pihak 1 (Aktor Pendobrak / Pria)</h4>", unsafe_allow_html=True)
            n1 = st.text_input("Ketik Nama Panggilan Pihak 1", key="n1_c")
            # FIXED DEFAULT DATE TAB 2
            d1 = st.date_input("Lahir Masehi Pihak 1", value=datetime.date(1995, 1, 1), min_value=datetime.date(1930, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="d1_c")
            hc1 = st.selectbox("Hari Pihak 1", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4, key="hc1")
            pc1 = st.selectbox("Pasaran Pihak 1", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=2, key="pc1")
        with cb: 
            st.markdown("<h4 style='color:#FF69B4;'>Pihak 2 (Reaktor Penyeimbang / Wanita)</h4>", unsafe_allow_html=True)
            n2 = st.text_input("Ketik Nama Panggilan Pihak 2", key="n2_c")
            d2 = st.date_input("Lahir Masehi Pihak 2", value=datetime.date(1998, 5, 10), min_value=datetime.date(1930, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="d2_c")
            hc2 = st.selectbox("Hari Pihak 2", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=2, key="hc2")
            pc2 = st.selectbox("Pasaran Pihak 2", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=0, key="pc2")
        st.markdown("</div>", unsafe_allow_html=True)
            
        if st.button("🚀 Retas Rahasia Perang Otak Pasangan", key="btn_couple"):
            if str(n1).strip() and str(n2).strip():
                try:
                    with st.spinner('Membedah benturan frekuensi kasar dan menumbuk ego kedua belah pihak...'): time.sleep(1.5)
                    st.toast("Analisa sinkronisasi brutal sukses diekstrak!", icon="💞")
                    
                    safe_n1, safe_n2 = get_safe_firstname(n1, "Pria"), get_safe_firstname(n2, "Wanita")
                    zod1, zod2 = get_zodiak(d1), get_zodiak(d2)
                    nep_1, nep_2 = hitung_neptu_langsung(hc1, pc1), hitung_neptu_langsung(hc2, pc2)
                    sel = abs(hitung_angka(d1) - hitung_angka(d2))
                    jummal_1, jummal_2 = hitung_nama_esoterik(n1), hitung_nama_esoterik(n2)
                    total_couple = jummal_1 + jummal_2
                    root_c = total_couple
                    while root_c > 9: root_c = sum(int(d) for d in str(root_c))
                    
                    c_title, c_desc = proc_couple_persona(root_c, safe_n1, safe_n2)
                    judul_jodoh, desk_jodoh, d_do, d_dont = proc_weton_kombo((nep_1+nep_2)%8 or 8, safe_n1, safe_n2, zod1, zod2)
                    
                    st.markdown(f"### 🔮 The Unified Resonance: {safe_n1} 💥 {safe_n2}")
                    st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Beban Neptu Keras {safe_n1}</div><div class="matrix-value">{hc1} {pc1} ({nep_1})</div></div><div class="matrix-item"><div class="matrix-label">Beban Neptu Keras {safe_n2}</div><div class="matrix-value">{hc2} {pc2} ({nep_2})</div></div><div class="matrix-item" style="background: rgba(212,175,55,0.2); border-left: 1px solid #D4AF37; border-right: 1px solid #D4AF37;"><div class="matrix-label" style="color:#FFD700;">TOTAL LEDAKAN BENTURAN NEPTU</div><div class="matrix-value matrix-value-special">{nep_1 + nep_2}</div></div><div class="matrix-item"><div class="matrix-label">Total Fusi Frekuensi Esoterik</div><div class="matrix-value">{total_couple}</div></div></div>""", unsafe_allow_html=True)
                    
                    st.markdown(proc_penjelasan_matriks(safe_n1, safe_n2, total_couple, (nep_1+nep_2)), unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="dynamic-reading-box soft-fade" style="border-left-color: #25D366; background: rgba(10,30,15,0.8);"><h4 style="color: #25D366; margin-top:0; letter-spacing:1px;">🧬 Wujud Persona Entitas Baru (Saat Bareng): {c_title}</h4><p style="color:#e0e0e0; line-height:1.7; font-size:15px;">{c_desc}</p></div>', unsafe_allow_html=True)
                    
                    st.markdown(f"""<div class="soft-fade" style="background: rgba(30,20,20,0.8); border: 1px solid #ff4b4b; border-left: 5px solid #ff4b4b; padding: 20px; border-radius: 8px; margin-bottom:20px;">
                    <b style="color:#ff4b4b; font-size:16px;">Titik Ranjau Benturan Gesekan Bawah Sadar ({judul_jodoh}):</b><br>
                    <span style="color:#ccc; display:inline-block; margin-top:8px; line-height:1.7; font-size:15px;">{desk_jodoh}</span>
                    </div>""", unsafe_allow_html=True)
                    
                    if sel in [0, 3, 6, 9]: 
                        st.markdown(f"<div class='info-metric-box soft-fade' style='border-color:#25D366; background:rgba(37,211,102,0.05);'><span style='font-size:24px;'>💘</span> <b style='color:#25D366; font-size:15px;'>SKOR META-PROGRAM NLP: Resonansi Mulus (Sangat Sinkron).</b><br><span style='color:#ccc; margin-top:5px; display:inline-block; line-height:1.6;'>Otak sadar maupun saraf bawah sadar kalian berdua memproses cara manajemen emosi pakai *coding* bahasa ego yang plek-ketiplek (identik). Kalau ngomong, pesannya langsung tembus ke hati tanpa distorsi sinyal.</span></div>", unsafe_allow_html=True)
                    elif sel in [1, 2, 8]: 
                        st.markdown(f"<div class='info-metric-box soft-fade' style='border-color:#FFD700; background:rgba(255,215,0,0.05);'><span style='font-size:24px;'>⚖️</span> <b style='color:#FFD700; font-size:15px;'>SKOR META-PROGRAM NLP: Dinamika Panas-Dingin (Bisa Diakali).</b><br><span style='color:#ccc; margin-top:5px; display:inline-block; line-height:1.6;'>Hubungan model ginian butuh stok kalibrasi kewarasan tingkat tinggi secara rutin! Gelombang radio kalian tuh sering numpuk tabrakan; di satu waktu bisa sehati banget nebak pikiran, eh di jam berikutnya malah diem-dieman karena miskomunikasi bodoh.</span></div>", unsafe_allow_html=True)
                    else: 
                        st.markdown(f"<div class='info-metric-box soft-fade' style='border-color:#ff4b4b; background:rgba(255,75,75,0.05);'><span style='font-size:24px;'>🔥</span> <b style='color:#ff4b4b; font-size:15px;'>SKOR META-PROGRAM NLP: Rawan Gesekan Berdarah / Beda Alam!</b><br><span style='color:#ccc; margin-top:5px; display:inline-block; line-height:1.6;'>Lampu Merah! Secara genetik otak, kalian berdua punya filter penerimaan realita (*Map of the World*) yang beda server. Ibarat Anda ngomong pake bahasa Arab, pasangan nangkapnya pake bahasa Mandarin. Pantesan debatnya nggak pernah ketemu titik terang! Butuh toleransi hati baja murni.</span></div>", unsafe_allow_html=True)
         
                    c_do_c, c_dont_c = st.columns(2)
                    with c_do_c: st.markdown(f"<div class='soft-fade' style='background:rgba(37,211,102,0.05); padding:20px; border-radius:10px; border:1px solid #25D366; height:100%; box-shadow: inset 0 0 20px rgba(37,211,102,0.05);'><b style='color:#25D366; font-size:16px; letter-spacing:1px;'>✅ PROTOKOL PENYELAMATAN HUBUNGAN (DO):</b><hr style='border-color:rgba(37,211,102,0.2); margin-top:10px; margin-bottom:15px;'><span style='color:#e0e0e0; line-height:1.7; font-size:14px;'>{d_do}</span></div>", unsafe_allow_html=True)
                    with c_dont_c: st.markdown(f"<div class='soft-fade' style='background:rgba(255,75,75,0.05); padding:20px; border-radius:10px; border:1px solid #ff4b4b; height:100%; box-shadow: inset 0 0 20px rgba(255,75,75,0.05);'><b style='color:#ff4b4b; font-size:16px; letter-spacing:1px;'>❌ ZONA NERAKA (HARAM DI LAKUKAN):</b><hr style='border-color:rgba(255,75,75,0.2); margin-top:10px; margin-bottom:15px;'><span style='color:#e0e0e0; line-height:1.7; font-size:14px;'>{d_dont}</span></div>", unsafe_allow_html=True)
                except Exception as e: st.error(f"Error mesin gagal me-load benturan ego: {e}")

# ==========================================
# TAB 5: QUANTUM ENGINE
# ==========================================
with tab5:
    if not st.session_state.premium:
        st.markdown(f"""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h2 style='color: #ff4b4b; font-weight: 900;'>🔒 FITUR EKSKLUSIF BOS DIKUNCI</h2>
<p style='color: #ccc; font-size: 16px; margin-bottom: 30px;'>Mohon maaf, Anda lagi muter-muter di batas kuota *Free Tier* gratisan. Buka gembok akses <b>Tactical Action Plan (Peta Rahasia Aksi Eksekusi Harian Berbasis Menit)</b> yang sistemnya nge-sinkron *real-time* dengan tarikan energi rotasi planet di atas langit Anda sekarang juga!</p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy." target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 MINTA KODE AKSESNYA VIA WA DONG (Rp 19.000)</div>
</a>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("⏱️ Live Cosmic Dashboard (Sistem *Hack* Nasib Harian)")
        st.write("Ibarat nyetir mobil di jalan tol, jangan asal injek gas kalau lagi nanjak! Sinkronkan langkah ambisi Anda dengan ritme rotasi jam planet dan siklus sirkadian matahari untuk bikin efisiensi tenaga kerja Anda naik 10x lipat lebih mulus tanpa perlu ngotot-ngototan.")
        qe_nama = st.text_input("Ketik Nama Panggilan Target (Anda sendiri):", key="qe_n")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🚀 Sedot Data Radar Taktis Saat Ini", key="btn_qe"):
            if qe_nama:
                with st.spinner('Membaca sinyal pergerakan astronomi di langit secara *real-time*...'): time.sleep(1.2)
                st.toast("Dashboard Taktis sukses dipaksa *update* ulang!", icon="⏱️")
                
                safe_qe = get_safe_firstname(qe_nama)
                jummal_qe = hitung_nama_esoterik(qe_nama)
                mod_harian = (jummal_qe + sum(int(d) for d in tgl_today.strftime("%d%m%Y"))) % 7
                sun_fase, sun_desc = get_sun_phase()
                planet_live, planet_desc, planet_color = get_planetary_hour()
                
                siklus_nama, html_plan = proc_tactical_plan(safe_qe, mod_harian, planet_live, planet_desc, sun_fase, sun_desc)
                
                st.markdown(f"### 📡 Live Dashboard Ruang Komando Tempur: {safe_qe}")
                st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Fase Baterai Bioritme Harian</div><div class="matrix-value">{siklus_nama}</div></div><div class="matrix-item"><div class="matrix-label">Siklus Jam Biologis Matahari</div><div class="matrix-value matrix-value-special">{sun_fase.split(' ')[0]}</div></div><div class="matrix-item" style="border-bottom: 2px solid {planet_color};"><div class="matrix-label">Intervensi Penguasa Jam Planet</div><div class="matrix-value" style="color:{planet_color};">{planet_live}</div></div></div>""", unsafe_allow_html=True)
                st.markdown(html_plan, unsafe_allow_html=True)

# ==========================================
# TAB 3: FALAK RUHANI
# ==========================================
with tab3:
    if not st.session_state.premium:
        st.markdown(f"""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h2 style='color: #ff4b4b; font-weight: 900;'>🔒 KLINIK PENYEMBUHAN JIWA DIKUNCI</h2>
<p style='color: #ccc; font-size: 16px; margin-bottom: 30px;'>Pintu akses digembok. Hanya pemegang kunci VIP yang diizinkan bongkar resep <b>Terapi Falak Ruhani, Suntikan Dzikir Khusus Nama Anda, Afirmasi NLP Terdalam, & Tindakan Fisik Penawar Virus *Mental Block* Keuangan</b>.</p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuro%20Nada%20Academy." target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 SIKAT, KLIK MINTA KUNCI VIA WA SEKARANG (Rp 19.000)</div>
</a>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("🌌 Ruang Terapi Falak Ruhani & Suntikan Hypno-NLP")
        st.info("**Reset Ulang Mesin Saraf Otak Anda yang Rusak**\n\nCara kerjanya gini: Sistem mesin ini bakal ngunyah nama lengkap Anda buat di-konversi jadi angka getaran khusus. Terus, angka itu dicocokin buat nyari frekuensi obat Asmaul Husna (sebagai *Anchor* / Jangkar Spiritual penenang batin) dipadu sama kalimat Afirmasi Bawah Sadar (Sugesti NLP modern). Resep ini diracik mutlak cuma buat ngehancurin *Mental Block* paling bahaya di kepala Anda doang.")
        nama_ruhani = st.text_input("Ketik Ulang Nama Lengkap Anda (Buat ngunci presisi sinkronisasi Dzikir):", placeholder="Ketik nama asli...", key="input_ruhani")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🚀 Produksi Resep Terapi Mental Saya", key="btn_ruhani"):
            if nama_ruhani and len(nama_ruhani.strip()) >= 3:
                try:
                    with st.spinner('Memeras sandi penyembuhan dari kedalaman matriks Anda...'): time.sleep(1.5)
                    st.toast("Protokol Terapi Obat Keras berhasil diturunkan!", icon="✨")
                        
                    safe_nr = get_safe_firstname(nama_ruhani)
                    nilai_jummal_r = hitung_nama_esoterik(nama_ruhani)
                    r_num_r = nilai_jummal_r
                    while r_num_r > 9: r_num_r = sum(int(d) for d in str(r_num_r))
                    
                    asma_terapi, vibrasi_asma, tujuan_ruhani, jumlah_dzikir = proc_falak_ruhani(nilai_jummal_r, r_num_r, safe_nr)
                    protokol_nlp = get_protokol_terapi(r_num_r, safe_nr)
                    
                    st.markdown(f"""<div class="soft-fade" style="background: linear-gradient(135deg, rgba(10, 20, 40, 0.9) 0%, rgba(20, 10, 40, 0.9) 100%); border-left: 5px solid #00FFFF; padding: 25px; border-radius: 12px; margin-top: 20px; box-shadow: 0 8px 25px rgba(0, 255, 255, 0.15);">
<div style="text-align:center; border-bottom:1px solid #00FFFF; padding-bottom:10px; margin-bottom:20px;">
<span style="color:#00FFFF; font-size:16px; font-weight:900; letter-spacing:2px;">🧠 RESEP PROTOKOL TERAPI KOMPREHENSIF: BAPAK/IBU {safe_nr.upper()}</span>
</div>
<div style="margin-bottom: 20px;">
<b style="color:#ff4b4b; font-size:16px; letter-spacing:1px;">⚠️ SUMBER PENYAKIT (Virus Sabotase Bawah Sadar Anda):</b><br>
<span style="color:#ccc; font-size:15px; line-height:1.7; display:inline-block; margin-top:8px;">{protokol_nlp['block']}</span>
</div>
<div style="background: rgba(0,0,0,0.5); padding: 18px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #00FFFF;">
<b style="color:#FFF; font-size:16px; letter-spacing:1px;">✨ 1. KUNCI ANCHOR SPIRITUAL (Obat Penenang Gaib Falak Ruhani)</b><br>
<span style="color:#aaa; font-size:14px; display:inline-block; margin-bottom:12px; line-height:1.6;">Aturan pakai: Jadikan lafaz Asma ini sebagai Dzikir penarik napas saat dada Anda lagi sesak, panik, mikir utang, atau saat otak lagi super *chaos* nggak bisa mikir jernih. Tarik napas dalem, baca di batin:</span><br>
<b style="color:#00FFFF; font-size:24px;">{asma_terapi}</b> <span style="color:#FFD700; font-weight:bold; font-size:16px; margin-left:10px; background:rgba(255,215,0,0.2); padding:4px 8px; border-radius:5px;">(BACA {jumlah_dzikir}x DALAM HATI)</span><br>
<i style="color:#ccc; font-size:14px; display:inline-block; margin-top:12px; padding-top:12px; border-top:1px dashed #444; line-height:1.6;"><b>Tujuan Suntikan Batin ini:</b> {tujuan_ruhani}</i>
</div>
<div style="background: rgba(255,215,0,0.05); border-left: 4px solid #FFD700; padding: 18px; border-radius: 8px; margin-bottom: 20px;">
<b style="color:#FFD700; font-size:16px; letter-spacing:1px;">🗣️ 2. SUGESTI HYPNO-NLP (Afirmasi Cuci Otak Pembongkar Rantai Kere)</b><br>
<span style="color:#aaa; font-size:14px; display:inline-block; margin-bottom:12px; line-height:1.6;">Aturan pakai: Mulut ngoceh doang nggak ada gunanya kalau hati mati rasa! Ucapin kalimat sugesti ini berulang kali di batin sambil dihayati banget, resapi rasa leganya sampai mau nangis, lakukan tepat 5 menit sebelum Anda merem tidur malam ini (Karena saat itu gelombang otak Theta yang mengontrol 95% nasib Anda lagi kebuka lebar total):</span><br>
<div style="background: rgba(0,0,0,0.6); padding: 15px; border-radius:6px; border:1px solid rgba(255,215,0,0.2);"><i style="color:#fff; font-size:16px; line-height:1.7;">"{protokol_nlp['afirmasi']}"</i></div>
</div>
<div style="border-top: 1px dashed #555; padding-top: 20px; padding-bottom: 5px;">
<b style="color:#25D366; font-size:16px; letter-spacing:1px;">🏃‍♂️ 3. QUANTUM HABIT (Tindakan Fisik Pengunci Nasib Hari Ini)</b><br>
<span style="color:#ccc; font-size:15px; line-height:1.7; display:inline-block; margin-top:8px;">Hukum mutlak Semesta: Cuma rebahan baca ginian nggak bakal ngubah nasib, karena hukum tarik-menarik dunia nyata cuma merespons *Gerak Fisik/Action*. Untuk mecahin kaca *Mental Block* tebal Anda, secara sadar paksa bokong Anda gerak buat ngeksekusi satu tugas aneh ini hari ini juga:<br><br>
<div style="background: rgba(37,211,102,0.1); border: 1px solid #25D366; padding: 15px; border-radius: 8px;"><b style="color:#FFF; font-size:16px; line-height:1.6;">{protokol_nlp['habit']}</b></div></span>
</div>
<p style="font-size:13px; color:#ff4b4b; margin-top:25px; font-weight:bold; text-align:center;">⏳ Ingat! Sistem terus memonitor kebocoran arus mental Anda. Sikat lakuin 3 protokol di atas MALAM INI JUGA sebelum siklus tidur nge-reset semua momentum ini jadi nol lagi besok pagi!</p>
</div>""", unsafe_allow_html=True)
                except Exception as e: st.error(f"Mesin ngaco saat mikir sandi terapi *deep level*: {e}")
            else: st.warning("⚠️ Filter Keamanan Otak: Ketik nama asli lengkap Anda (minimal 3 huruf) biar sinkronisasinya akurat sasaran.")

# ==========================================
# TAB 6 & 4 (SAMA SEPERTI SEBELUMNYA)
# ==========================================
with tab6:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("📚 Neuro-Insights: Kalibrasi Mindset Otoritatif")
    st.write("Jelajahi pemikiran terdalam, modifikasi bawah sadar, dan telaah esoterik Nusantara langsung dari sudut pandang *Hypno-Copywriting*.")
    with st.expander("🧠 1. Kenapa Logika Super Pintar Anda Sering Kalah Telak Sama Perasaan Baper?"):
        st.markdown("""**Oleh: Coach Ahmad Septian (NLP Trainer & Hypnotherapist)**\n\nBanyak eksekutif dan pengusaha sombong mengira tiap keputusan bisnis/keluarga yang mereka ambil itu murni hasil mikir rasional yang cerdas. Fakta *neuro-science* brutalnya: **95% nasib/keputusan manusia dikendalikan mutlak sama pikiran bawah sadar**—yang bahasa mesinnya itu bukan data/angka, melainkan 'RASA' (Emosi).\n\nKalau otak sadar (logika) teriak "Kerjain proposal sekarang biar dapet duit", tapi hati kecil ngomong "Tapi males banget ada rasa takut ditolak klien", siapa bos yang menang? SELALU EMOSI YANG MENANG. Logika Anda yang pinter itu cuma bakal nyari seribu alasan *ngeles* buat membenarkan kemalasan tadi.\n\n**Cara Hack-nya (NLP Reframing):** Jangan musuhin dan debat logika Anda sendiri, bakal cape. Anda cukup perlu mengubah 'Rasa' (*Anchor* Emosi) yang nempel di kebiasaan buruk itu. Cuci otak Anda sendiri dengan menggabungkan kata 'Bertindak Berani' = 'Sensasi Kelegaan yang Enak Banget'.""")
    with st.expander("💰 2. Rahasia Bocornya Pipa Rezeki Anda di Balik Sandi Huruf Nama"):
        st.markdown("""Pernah ngerasa gini: Udah *hustle* banting tulang sampe asam lambung naik, ngorbanin me-time, tapi duitnya kok selalu kerasa 'numpang lewat doang' di ATM? Atau kalaupun *closing* gede, besokannya pasti ada aja mobil rusak lah, apalah yang bikin duit ludes.\n\nDi dalam ilmu mistik angka Nusantara (Hisab Jummal), ini nggak ada urusannya sama kebetulan. **Setiap abjad di nama Anda yang dipanggil miliaran kali seumur hidup itu bawa setruman beban psikologis!** Kalau nama panggilan Anda terlalu didominasi getaran "Api" yang bikin ego gampang meledak tanpa dikasih rem "Air" ketenangan, wajar aja secara refleks bawah sadar Anda jadi gampang nekat judi *trading*, rakus jangka pendek, dan akhirnya ngancurin cuan hasil panen sendiri.\n\n**Solusinya:** Bukan, Anda nggak disuruh ribet ke Kelurahan ganti KTP. Cukup *hack* pakai frekuensi penyeimbang. Cari Asma/Dzikir khusus (*Falak Ruhani*) dan jadiin itu pegangan (*Anchor*) tiap kali tangan Anda gatal mau ngambil keputusan fatal.""")
    with st.expander("⚡ 3. Sindrom Lone Wolf: Ilusi Konyol di Balik Kata Keren 'Gue Mandiri'"):
        st.markdown("""Di zaman orang pada mabuk *Hustle-Culture* di TikTok, jadi manusia serba bisa (Super-Soloist) kesannya ngeboss banget. Anda maksain diri *design* logo sendiri, jualan sendiri, *packing* sendiri, dan muter otak sendiri.\n\nRealita nyebelinnya: Sikap sok "Mandiri" ini cuma topeng kardus buat nutupin penyakit *Mental Block* terdalam Anda, yaitu: **INSECURITY dan Gengsi Kegedean Buat Minta Tolong!** Anda egois merasa orang lain kerjanya lebih goblok dari Anda.\n\nHukum gravitasi tarik uang itu sangat jelas: Tuhan membagikan uang dan kelimpahannya mutlak lewat perantara *TANGAN ORANG LAIN* (Kerja sama & lempar tanggung jawab). Kalau Anda terus-terusan ngunci gembok nggak mau ngelepasin kerjaan ke tim karena sok merasa paling bener, tunggu aja tanggal mainnya mesin saraf Anda meledak (*Burnout* / Tipus). Uang miliaran masuk ke kantong orang yang punya sistem efisien, BUKAN ke orang yang kecapekan kurang tidur.""")
    st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("❓ Parameter Sistem & Aturan Main Legal")
    with st.expander("🤔 1. Mesin algoritma Neuro Nada OS ini pake ilmu santet atau gimana sih?"): 
        st.write("Sama sekali nggak ada unsur syirik atau klenik di sini. Platform Neuro Nada OS adalah eksperimen murni persilangan *cyber-esoteric*. Kami mengawinkan kalkulasi matematika aksara kuno (Gematria Arab / Hisab Jummal) dan data kalender siklus alam (Primbon Betaljemur Jawa), lalu kami bedah ulang pakai pisau bedah psikologi modern bernama NLP (*Neuro-Linguistic Programming*). Kami nggak ngasih janji ramalan masa depan kayak dukun pinggir jalan. Kami memetakan algoritma OS otak Anda, biar Anda sadar letak kelemahan Anda, lalu Anda sendiri yang nyetir nasib Anda (Fate Hacking).")
    with st.expander("🤔 2. Kok bahasa jawabannya kasar, *to the point*, dan nyesek banget di hati?"): 
        st.write("Ibarat dokter bedah, kami nggak mungkin ngebedah tumor pasien pakai pisau karet mainan! Sistem ini diprogram murni objektif dan dingin tanpa perasaan. Algoritma ini sengaja **BUKAN** dibuat buat ngejilat ego atau ngasih motivasi bacot-manis penyenang hati. Fungsi mesin ini adalah 'Menelanjangi' titik buta kemunafikan (*Blind Spot*) dan sisi gelap (*Shadow*) yang selama ini mati-matian Anda tutupi. Kedewasaan mental cuma bakal lahir kalau kebusukan ego ditonjok secara frontal di depan kaca.")
    with st.expander("🤔 3. Kalau disuruh ngadep mata angin 'Naga Dina', itu sifatnya wajib tahayul atau gimana?"): 
        st.write("Di dunia vibrasi energi gaib kuno, aturan *Naga Dina* itu ibarat rumus Fisika Magnet Bumi (*Geomansi*). Tujuannya buat nyamain kutub energi tubuh Anda sama tarikan magnet lokasi ruangan biar urusan lancar dan nggak nabrak 'dinding penolakan' saat nego bisnis. Tapi logikanya: Mau Anda ngadep kiblat mana aja, kalau *skill* ngomong Anda ampas dan produk Anda jelek, ya nggak bakal *closing*! Aksi fisik Anda nyumbang 90% porsi kesuksesan, kompas energi cuma dorong 10%-nya.")
    st.markdown("<hr style='border-top: 1px dashed #555;'>", unsafe_allow_html=True)
    st.error("""**⚠️ DISCLAIMER LEGAL & ETIKA (BACA SEBELUM ANDA BAPER):**\nSeluruh laporan sadis hasil *Decoding*, prediksi jam planet kosmik, dan obat resep Terapi di atas disediakan semata-mata sebagai cermin introspeksi kesadaran diri yang menghibur (*Self-Awareness Tool*), dan bahan eksperimen psikologi.\n\nPlatform *software* ini dan *developer*-nya (Coach Ahmad Septian) **SAMA SEKALI BUKAN** penyedia layanan pialang saham, bukan dokter medis bersertifikat, dan bukan psikiater klinis tempat buang sampah. \n\nTanggung jawab eksekusi bisnis, putus cinta, cerai, transfer duit ratusan juta, atau perubahan gaya hidup yang Anda lakuin habis baca ginian adalah 100% mutlak *risiko tanggung sendiri* pakai kehendak bebas otak Anda. Kami nggak melayani komplain tuntutan hukum ganti rugi materiil gara-gara Anda salah nebak tafsir aplikasi ini.""")
    st.markdown("</div>", unsafe_allow_html=True)
 
# ==========================================
# SOCIAL PROOF & FOOTER
# ==========================================
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Jejak Para Eksekutor yang Berhasil Nabrak Ego</h3>", unsafe_allow_html=True)
daftar_ulasan = ambil_ulasan()
if daftar_ulasan:
    marquee_content = " | ".join([f"<span style='color: #FFD700;'>{u.get('Rating', '⭐⭐⭐⭐⭐')}</span> <b>{u.get('Nama', 'User')}:</b> \"{u.get('Komentar', '')[:50]}...\"" for u in daftar_ulasan[:3]])
    st.markdown(f'<div style="background-color: #1a1a1a; padding: 12px; border-radius: 8px; border-left: 3px solid #D4AF37; border-right: 3px solid #D4AF37; white-space: nowrap; overflow: hidden; margin-bottom: 20px;"><marquee behavior="scroll" direction="left" scrollamount="6" style="color: #f0f0f0; font-size: 15px;">{marquee_content}</marquee></div>', unsafe_allow_html=True)
    for u in daftar_ulasan[:5]:
        if u.get("Komentar", ""): st.markdown(f'<div class="ulasan-box"><span style="color: #FFD700; font-size: 12px;">{u.get("Rating", "⭐⭐⭐⭐⭐")}</span><br><b style="font-size:15px;">{u.get("Nama", "Entitas")}</b><br><i style="color: #ccc; line-height:1.6; display:inline-block; margin-top:5px;">"{u.get("Komentar", "")}"</i></div>', unsafe_allow_html=True)

with st.expander("💬 Tinggalkan Jejak Pengakuan Dosa / Testimoni Anda"):
    with st.form("form_review"):
        rn, rr, rk = st.text_input("Nama Samaran Bosque"), st.radio("Seberapa Nonjok Kalibrasinya?", ["⭐⭐⭐⭐⭐ (Parah Nembus Otak)", "⭐⭐⭐⭐ (Ngena Banget)", "⭐⭐⭐ (Biasa Aja)", "⭐⭐ (Kurang Sadis)", "⭐ (Meleset)"], horizontal=True), st.text_area("Tumpahin Curhatan/Dampak Sadisnya di Sini")
        if st.form_submit_button("Suntikkan Kesaksian ke Server") and rn and rk:
            if kirim_ulasan(rn, rr.split(' ')[0], rk): 
                st.toast("Jejak keberanian Anda berhasil ngerekam di *database* pusat. Mantap jiwa!", icon="🔥")
                time.sleep(1)
                st.rerun()
 
st.markdown("---")
st.markdown("<center><b style='color:#FFF; letter-spacing:1px; font-size:16px;'>Ahmad Septian Dwi Cahyo</b><br><span style='color:#888; font-size:13px; display:inline-block; margin-top:5px;'>Certified NLP Trainer & Professional Hypnotherapist<br>Hak Cipta © 2026 Neuro Nada Academy (Build-V4 Ultimate Awam-Edition)</span></center>", unsafe_allow_html=True)
