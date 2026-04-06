import streamlit as st
import datetime
import os
import time
import urllib.parse
import urllib.request
import math
import plotly.graph_objects as go
import random
import csv
import io

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="Deep Personality Mapping", 
    page_icon="🌌", 
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- CUSTOM CSS ---
st.markdown(
    """<style>
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    
    /* Tombol Utama */
    div.stButton > button {
        background-color: #FFD700 !important; color: #000000 !important;
        font-weight: 800 !important; border: none !important;
        padding: 12px 24px !important; border-radius: 8px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
        box-shadow: 0 4px 10px rgba(255,215,0,0.3);
    }
    div.stButton > button:hover { transform: scale(1.02); background-color: #FFC107 !important; }
    
    /* Tombol CTA Maut */
    .cta-button {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff0000 100%);
        color: white !important; padding: 15px; text-align: center; 
        border-radius: 8px; font-weight: 900; font-size: 16px; 
        box-shadow: 0 6px 15px rgba(255, 75, 75, 0.4);
        text-transform: uppercase; letter-spacing: 1px;
        transition: 0.3s;
    }
    .cta-button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(255, 75, 75, 0.6); }

    .ulasan-box {
        background-color: #1e1e1e; padding: 15px; border-radius: 8px;
        border-left: 4px solid #FFD700; margin-bottom: 10px; font-size: 14px;
    }
    
    .cosmic-box {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a4a 100%);
        padding: 20px; border-radius: 12px; border: 1px solid #4a4a8a;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6); margin-bottom: 15px;
    }
    
    /* MATRIKS KECIL PROPORSIONAL */
    .matrix-container {
        display: flex; justify-content: space-between; gap: 8px;
        padding: 12px; background-color: #101010; border-radius: 10px;
        border: 1px solid #333; margin-bottom: 20px;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
    }
    .matrix-item { flex: 1; text-align: center; padding: 5px; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .matrix-value { font-size: 16px; font-weight: 900; color: white; }
    .matrix-value-special { color: #FFD700; }
    
    /* List Kekuatan & Shadow */
    .list-punchy { padding-left: 20px; margin-bottom: 15px; font-size: 15px; }
    .list-punchy li { margin-bottom: 8px; }
    </style>""", unsafe_allow_html=True
)

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa Kosmik"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

# ==========================================
# DATABASE CLOUD: GOOGLE SHEETS
# ==========================================
URL_POST = "https://script.google.com/macros/s/AKfycbwkOL8-E50RKM5BRR8puh_XbfL-K_hQj5cnv0un6UzmFmMBEG6HZZ4aEQmFZj5EMsSBUQ/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2H-IH_8TbdbMRtvZnvza-InIO-Xl-B9YzLYtWtSb8vpUVuM1uZ4FTi6JwOtk2esj7hilwgGCoWex4/pub?output=csv"

def ambil_ulasan():
    try:
        req = urllib.request.Request(URL_CSV)
        with urllib.request.urlopen(req) as response:
            decoded = response.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            return [row for row in reader][::-1]
    except: return []

def kirim_ulasan(nama, rating, komentar):
    try:
        data = urllib.parse.urlencode({"nama": nama, "rating": rating, "komentar": komentar}).encode("utf-8")
        req = urllib.request.Request(URL_POST, data=data)
        urllib.request.urlopen(req)
        return True
    except: return False

# --- SIDEBAR PROMOSI & VIDEO ---
with st.sidebar:
    if os.path.exists("baru.jpg.png"):
        try: st.image("baru.jpg.png", use_container_width=True); st.markdown("<br>", unsafe_allow_html=True)
        except: pass
    elif os.path.exists("baru.jpg"): st.image("baru.jpg", use_container_width=True)

    st.markdown(f"### {get_greeting()}")
    st.markdown("### 🎬 Hypno-Video Vault")
    st.video("https://youtu.be/kkRcH6aH_lI?si=bpUZF3CWl8DKLw5m")
    st.markdown("---")
    st.info("**Reset Pola Pikir Anda**\n\nMari kita lakukan kalibrasi ulang dalam sesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    st.markdown(f"[👉 **Amankan Jadwal Anda**](https://wa.me/628999771486?text={urllib.parse.quote('Halo Coach Ahmad, saya siap kalibrasi.')})")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

# --- INTERFACE UTAMA ---
if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass

st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900;'>🌌 Deep Personality Mapping</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #D4AF37; margin-bottom:0;'>Blueprint Jiwa Berbasis Waktu Lahir</p>", unsafe_allow_html=True)
st.markdown("---")

# --- DATABASE ARKETIPE (DEEP & PUNCHY) ---
arketipe_punchy = {
    1: {"inti": "Sang Perintis yang lahir untuk memimpin, benci didikte, dan selalu fokus pada tujuan masa depan.", "kekuatan": ["Daya dobrak tinggi & berani ambil risiko", "Mandiri secara absolut", "Fokus eksekusi (Outcome-oriented)"]},
    2: {"inti": "Sang Penyelaras yang menjadi lem perekat hubungan, sangat peka membaca emosi lingkungan sekitar.", "kekuatan": ["Kapasitas empati level tinggi", "Negosiator & pencipta harmoni ulung", "Kemampuan adaptasi emosional (Rapport)"]},
    3: {"inti": "Sang Visioner dengan pikiran bak kembang api; kaya ide, ekspresif, dan magnetis dalam pergaulan.", "kekuatan": ["Komunikasi memikat (Persuasif)", "Kreativitas & imajinasi tanpa batas", "Ahli mencairkan suasana beku"]},
    4: {"inti": "Sang Transformator yang bertumpu pada struktur, detail, dan keteraturan hidup yang logis.", "kekuatan": ["Pola pikir sangat terstruktur & rapi", "Pekerja keras yang bisa diandalkan 100%", "Ketelitian tingkat dewa (Prosedural)"]},
    5: {"inti": "Sang Penggerak yang memuja kebebasan, haus petualangan, dan tercepat beradaptasi dengan perubahan.", "kekuatan": ["Kelincahan berpikir (Agility)", "Inovator & pemecah kebuntuan", "Keberanian mengeksplorasi hal baru"]},
    6: {"inti": "Sang Harmonizer yang menjadi pelindung natural, rela berkorban demi merawat lingkaran terdekatnya.", "kekuatan": ["Insting pengayom yang luar biasa", "Tanggung jawab moral level tinggi", "Loyalitas & dedikasi tanpa pamrih"]},
    7: {"inti": "Sang Legacy Builder yang haus kebenaran, pemikir mendalam, dan memiliki intuisi spiritual tajam.", "kekuatan": ["Kemampuan analisa (Deep Structure)", "Intuisi & firasat yang sering akurat", "Sangat selektif menilai kualitas"]},
    8: {"inti": "Sang Sovereign dengan visi kerajaan. Eksekutor ulung yang memancarkan otoritas dan kelimpahan materi.", "kekuatan": ["Tahan banting terhadap tekanan mental", "Insting bisnis & strategi tajam", "Kemampuan memegang kendali (Leader)"]},
    9: {"inti": "Sang Kesadaran Tinggi (Old Soul) yang memandang dunia secara holistik dengan idealisme luhur.", "kekuatan": ["Kebijaksanaan & pemikiran luas", "Kepedulian universal (Humanisme)", "Mampu melihat 'Big Picture' kehidupan"]}
}

arketipe_deskripsi = {
    1: "**The Leader (Sang Perintis):** Anda lahir untuk memimpin dan membuka jalan. Arketipe ini memiliki dorongan internal yang kuat untuk mandiri dan benci jika harus didikte. Anda adalah pengambil risiko yang berani, namun seringkali merasa kesepian karena merasa harus memikul tanggung jawab sendirian.",
    2: "**The Mediator (Sang Penyelaras):** Anda adalah lem perekat dalam setiap hubungan. Bakat Anda adalah mendengarkan dan menciptakan harmoni. Arketipe ini sangat peka terhadap perasaan orang lain, namun seringkali kehilangan identitas diri karena terlalu sibuk menyenangkan orang lain (*People Pleaser*).",
    3: "**The Communicator (Sang Visioner):** Anda adalah pembawa pesan dan inspirasi. Pikiran Anda bekerja seperti kembang api; penuh warna dan ide kreatif. Anda pandai menarik perhatian, namun tantangan terbesar Anda adalah menyelesaikan apa yang sudah Anda mulai karena mudah teralihkan oleh hal baru.",
    4: "**The Architect (Sang Transformator):** Anda adalah pembangun sistem. Keamanan, keteraturan, dan detail adalah nafas Anda. Anda sangat bisa diandalkan dan praktis. Namun, Arketipe ini sering terjebak dalam kekakuan dan stres luar biasa jika rencana hidup tidak berjalan sesuai jadwal.",
    5: "**The Explorer (Sang Penggerak):** Anda adalah simbol kebebasan dan adaptasi. Arketipe ini haus akan pengalaman baru dan petualangan. Anda sangat cepat belajar hal baru, namun seringkali merasa hampa karena sulit menemukan 'rumah' atau tujuan tetap dalam jangka panjang.",
    6: "**The Nurturer (Sang Harmonizer):** Anda adalah pengayom sejati. Fokus hidup Anda adalah melayani dan merawat orang-orang yang Anda cintai. Anda memiliki standar moral yang tinggi. Sisi gelapnya: Anda sering merasa dieksploitasi karena Anda memberi terlalu banyak tanpa batasan.",
    7: "**The Analyst (Sang Legacy Builder):** Anda adalah pencari kebenaran dan makna terdalam. Pikiran Anda sangat tajam dan intuitif. Anda tidak puas dengan hal permukaan. Namun, Arketipe ini sering mengisolasi diri dan terjebak dalam labirin pikirannya sendiri (*Overthinking*).",
    8: "**The Strategist (Sang Sovereign):** Anda adalah figur otoritas dan kelimpahan. Arketipe ini memiliki visi besar untuk membangun kerajaan finansial atau pengaruh sosial. Anda sangat tangguh, namun tantangan terbesar Anda adalah berdamai dengan sisi rapuh dan emosional dalam diri Anda.",
    9: "**The Humanist (Sang Kesadaran Tinggi):** Anda adalah jiwa tua yang bijaksana. Anda peduli pada kemanusiaan dan cinta universal. Anda memandang dunia dengan kacamata holistik. Tantangannya: Anda sering merasa patah hati melihat realitas dunia yang tidak seindah idealisme Anda."
}

closing_brutal_dinamis = {
    1: ["Overthinking karena merasa hasil 'belum sempurna'", "Gengsi minta tolong saat memikul beban sendirian", "Membangun tembok ego untuk menutupi rasa sepi"],
    2: ["Mengorbankan kebahagiaan diri demi ekspektasi orang lain", "Sulit berkata 'TIDAK' yang berujung kelelahan mental", "Memendam amarah dalam hati demi menghindari konflik"],
    3: ["Menyembunyikan gelisah batin di balik topeng senyuman", "Cepat kehilangan motivasi jika rutinitas membosankan", "Insomnia karena pikiran terlalu berisik (Over-analisa)"],
    4: ["Stres parah jika rencana mendadak berubah di luar kendali", "Terjebak di zona nyaman karena takut ambil resiko baru", "Sering dinilai terlalu dingin/kaku oleh pasangan"],
    5: ["Sindrom 'Cepat Bosan' yang mensabotase karya/hubungan", "Kelelahan saraf karena otak tak pernah diizinkan istirahat", "Merasa hampa karena kehilangan pijakan komitmen"],
    6: ["Burnout ekstrim karena sibuk mengurus hidup orang lain", "Sikap Over-Protective yang diam-diam mengekang", "Rasa bersalah luar biasa jika memakai waktu untuk diri sendiri"],
    7: ["Paralysis by Analysis (Menganalisa terus tanpa aksi nyata)", "Merasa terasing karena merasa tak ada yang sepemikiran", "Mencurigai niat baik orang akibat luka masa lalu"],
    8: ["Merasa hampa dan kosong di saat mencapai puncak sukses", "Sangat sulit melepaskan kontrol dan memaafkan", "Mem
