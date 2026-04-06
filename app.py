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
    page_title="Neuro Nada Cosmic Analysis", 
    page_icon="🌌", 
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- CUSTOM CSS ---
st.markdown(
    """<style>
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    
    div.stButton > button {
        background-color: #FFD700 !important; color: #000000 !important;
        font-weight: bold !important; border: none !important;
        padding: 12px 24px !important; border-radius: 8px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.02); background-color: #FFC107 !important; }
    
    .ulasan-box {
        background-color: #1e1e1e; padding: 15px; border-radius: 8px;
        border-left: 4px solid #FFD700; margin-bottom: 10px; font-size: 14px;
    }
    
    .cosmic-box {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a4a 100%);
        padding: 15px; border-radius: 10px; border: 1px solid #4a4a8a;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5); margin-bottom: 15px;
    }
    
    /* MATRIKS KECIL PROPORSIONAL */
    .matrix-container {
        display: flex; justify-content: space-between; gap: 8px;
        padding: 12px; background-color: #101010; border-radius: 8px;
        border: 1px solid #333; margin-bottom: 20px;
    }
    .matrix-item { flex: 1; text-align: center; padding: 5px; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .matrix-value { font-size: 16px; font-weight: 800; color: white; }
    .matrix-value-special { color: #FFD700; }
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
    st.markdown("---")
    st.success("**📚 Seni Persuasi NLP**\n\nPelajari bagaimana bahasa bekerja di tingkat bawah sadar.")
    st.markdown("[👉 **Akses Modul Lengkap**](https://lynk.id/neuronada/ebook-nlp)")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

# --- INTERFACE UTAMA ---
if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass

st.markdown("<h1 style='text-align: center; margin-top: 10px;'>🌌 Neuro Nada Cosmic Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #D4AF37; margin-bottom:0;'>Integrasi Falak, Weton, Numerologi & Psikologi Bawah Sadar</p>", unsafe_allow_html=True)
st.markdown("---")

# --- DATABASE ARKETIPE (NEW & DEEP) ---
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

vibrasi_nama_dict = {
    1: "Nama Anda memancarkan getaran **KEMANDIRIAN**. Orang melihat Anda sebagai sosok alfa. Di dalam hati, Anda rindu tempat bersandar tanpa perlu berpura-pura kuat.",
    2: "Nama Anda memancarkan getaran **DIPLOMASI**. Anda bagaikan oase bagi orang lain, namun sering lupa membersihkan emosi Anda sendiri.",
    3: "Nama Anda memancarkan getaran **EKSPRESI**. Daya tarik magnetis Anda kuat, namun pikiran Anda tak henti memutar skenario kehidupan.",
    4: "Nama Anda memancarkan getaran **STRUKTUR**. Orang mempercayai Anda ibarat batu karang. Sisi tersembunyi: Anda menyimpan kecemasan mendalam.",
    5: "Nama Anda memancarkan getaran **KEBEBASAN**. Aura Anda penuh kejutan. Ketakutan akan komitmen membuat Anda terkadang merasa kehilangan 'jangkar'.",
    6: "Nama Anda memancarkan getaran **TANGGUNG JAWAB**. Anda pelindung natural. Hati-hati, cinta tanpa batasan akan menguras habis energi hidup Anda.",
    7: "Nama Anda memancarkan getaran **KEDALAMAN**. Anda cerdas dan selektif. Lebih memilih 2 sahabat sefrekuensi daripada 100 teman kulit luar.",
    8: "Nama Anda memancarkan getaran **OTORITAS**. Anda memiliki ketahanan baja. Sering merasa kesepian justru ketika berada di puncak pencapaian.",
    9: "Nama Anda memancarkan getaran **IDEALISME**. Visi Anda melampaui ego. Sering dikecewakan karena standar ketulusan Anda terlalu tinggi bagi orang lain."
}

data_analisa = {
    1: {"karakter": "Anda merasa gatal kalau harus menunggu orang lain bergerak. Pikiran selalu fokus pada Outcome.", "asmara": "Butuh pasangan yang tidak mengekang tapi seimbang secara ritme."},
    2: {"karakter": "Bakat alami penyerap energi. Sangat peka suasana hati meski orang diam.", "asmara": "Asmara adalah rasa aman emosional. Berhentilah jadi penyelamat pasangan."},
    3: {"karakter": "Kaya imajinasi dan ide brilian. Sering memutar ulang percakapan masa lalu.", "asmara": "Butuh koneksi yang menyenangkan. Kebisuan adalah siksaan bagi Anda."},
    4: {"karakter": "Perencana detail dan benci ketidakpastian. Pikiran seperti laci rapi.", "asmara": "Sangat setia, namun sering lupa bumbu romantis karena terlalu logis."},
    5: {"karakter": "Benci rutinitas monoton. Hebat mencari celah di saat orang lain buntu.", "asmara": "Kata kunci: Kebebasan. Posesif akan memicu insting melarikan diri."},
    6: {"karakter": "Fokus pada Values keluarga. Gampang kecewa kalau orang tidak sepeduli Anda.", "asmara": "Kepedulian kadang terasa mengatur. Berhenti menebak pikiran pasangan."},
    7: {"karakter": "Intuisi tajam; firasat sering terbukti. Butuh Me-Time untuk menata energi.", "asmara": "Sulit ditembus dan tidak mudah terbuka 100%. Cari yang senada jiwanya."},
    8: {"karakter": "Dorongan kuat untuk sukses. Tahan banting terhadap tekanan mental.", "asmara": "Jangan bawa negosiasi bisnis ke rumah. Gunakan validasi emosi."},
    9: {"karakter": "Jiwa tua yang memandang masalah secara holistik. Standar moral tinggi.", "asmara": "Mencari koneksi spiritual. Menerima ketidaksempurnaan adalah kunci kedamaian."}
}

tips_zodiak_nlp = {
    "Aries": "Pacing dulu emosinya, baru perlahan Lead ke logika Anda.", "Taurus": "Berikan data logis, jangan dipaksa berubah cepat.",
    "Gemini": "Ikuti ritme cepatnya dan gunakan bahasa visual.", "Cancer": "Hati-hati nada suara; cara bicara Anda adalah segalanya.",
    "Leo": "Sentuh egonya dengan apresiasi tulus sebelum masukan.", "Virgo": "Tarik perhatiannya ke gambaran besar masalah.",
    "Libra": "Bantu mereka mengambil keputusan dari keinginan internal.", "Scorpio": "Bangun kepercayaan di level terdalam tanpa kebohongan kecil.",
    "Sagittarius": "Hubungkan masalah saat ini dengan visi masa depan.", "Capricorn": "Mulai dari sudut fungsional, baru masuk emosional.",
    "Aquarius": "Berikan kejutan ide anti-mainstream mendadak.", "Pisces": "Tarik pikiran mereka ke fakta saat imajinasi mulai negatif."
}

closing_brutal_dinamis = {
    1: ["Overthinking hasil belum sempurna", "Gengsi minta tolong", "Membangun tembok ego"],
    2: ["Mengorbankan diri demi orang lain", "Sulit berkata TIDAK", "Memendam amarah konflik"],
    3: ["Menyembunyikan gelisah batin", "Gampang hilang motivasi", "Internal Dialogue terlalu berisik"],
    4: ["Stres rencana mendadak berubah", "Takut resiko baru", "Sering dianggap dingin"],
    5: ["Sindrom Cepat Bosan", "Kelelahan saraf", "Kehilangan arah pijakan"],
    6: ["Burnout mengurus hidup orang", "Over-Protective mengekang", "Merasa bersalah memakai waktu diri"],
    7: ["Paralysis by Analysis", "Merasa terasing tak dipahami", "Mencurigai niat akibat luka lama"],
    8: ["Hampa di puncak sukses", "Sulit melepaskan
