import streamlit as st
import datetime
import os
import time
import urllib.parse
import urllib.request
import plotly.graph_objects as go
import random
import csv
import io

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="Neuro Nada Deep Analysis", 
    page_icon="🧠", 
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- FUNGSI NYAWA: TYPEWRITER EFFECT ---
def type_effect(text, speed=0.01):
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(full_text)
        time.sleep(speed)

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa yang Luar Biasa"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

# ==========================================
# DATABASE CLOUD: GOOGLE SHEETS (REAL-TIME)
# ==========================================
URL_POST = "https://script.google.com/macros/s/AKfycbwkOL8-E50RKM5BRR8puh_XbfL-K_hQj5cnv0un6UzmFmMBEG6HZZ4aEQmFZj5EMsSBUQ/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2H-IH_8TbdbMRtvZnvza-InIO-Xl-B9YzLYtWtSb8vpUVuM1uZ4FTi6JwOtk2esj7hilwgGCoWex4/pub?output=csv"

# Tanpa Cache agar ulasan tampil Real-Time
def ambil_ulasan():
    try:
        req = urllib.request.Request(URL_CSV)
        with urllib.request.urlopen(req) as response:
            decoded = response.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            return [row for row in reader][::-1]
    except:
        return []

def kirim_ulasan(nama, rating, komentar):
    try:
        data = urllib.parse.urlencode({"nama": nama, "rating": rating, "komentar": komentar}).encode("utf-8")
        req = urllib.request.Request(URL_POST, data=data)
        urllib.request.urlopen(req)
        return True
    except:
        return False

# --- CUSTOM CSS ---
st.markdown(
    """<style>
    div.stButton > button {
        background-color: #FFD700 !important; color: #000000 !important;
        font-weight: bold !important; border: none !important;
        padding: 12px 24px !important; border-radius: 50px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.02); background-color: #FFC107 !important; }
    .ulasan-box {
        background-color: #1e1e1e; padding: 15px; border-radius: 8px;
        border-left: 4px solid #FFD700; margin-bottom: 10px;
    }
    </style>""", unsafe_allow_html=True
)

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("baru.jpg"): st.image("baru.jpg", use_container_width=True)
    st.markdown(f"### {get_greeting()}")
    st.markdown("### 🎬 Hypno-Video Vault")
    st.video("https://youtu.be/kkRcH6aH_lI?si=bpUZF3CWl8DKLw5m")
    st.markdown("---")
    st.info("**Sesi Transformasi Pikiran**\n\nMari kita lakukan kalibrasi ulang dalam sesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    st.link_button("👉 Amankan Jadwal Anda", "https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20siap%20kalibrasi.")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

# --- INTERFACE UTAMA ---
if os.path.exists("banner.jpg"): st.image("banner.jpg", use_container_width=True)
st.markdown("<h1 style='text-align: center; margin-top: 10px;'>🧠 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 18px; color: #D4AF37;'>{get_greeting()}</p>", unsafe_allow_html=True)
st.markdown("---")

# --- LOGIKA MATEMATIKA, WETON & ZODIAK ---
def hitung_angka(tanggal):
    total = sum(int(digit) for digit in tanggal.strftime("%d%m%Y"))
    while total > 9: total = sum(int(digit) for digit in str(total))
    return total

def get_neptu_weton(tanggal):
    anchor_date = datetime.date(2000, 1, 1)
    selisih_hari = (tanggal - anchor_date).days
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][tanggal.weekday()]
    pasaran = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"][selisih_hari % 5]
    n_hari = {"Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9}
    n_pas = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
    return n_hari[hari] + n_pas[pasaran], f"{hari} {pasaran}"

def get_zodiak(tanggal):
    d, m = tanggal.day, tanggal.month
    if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "Aries", "Keberanian & Eksekusi"
    elif (m == 4 and d >= 20) or (m == 5 and d <= 20): return "Taurus", "Kestabilan & Ketekunan"
    elif (m == 5 and d >= 21) or (m == 6 and d <= 20): return "Gemini", "Komunikasi & Fleksibilitas"
    elif (m == 6 and d >= 21) or (m == 7 and d <= 22): return "Cancer", "Perasaan & Perlindungan"
    elif (m == 7 and d >= 23) or (m == 8 and d <= 22): return "Leo", "Kharisma & Kepemimpinan"
    elif (m == 8 and d >= 23) or (m == 9 and d <= 22): return "Virgo", "Analisa & Kesempurnaan"
    elif (m == 9 and d >= 23) or (m == 10 and d <= 22): return "Libra", "Keseimbangan & Harmoni"
    elif (m == 10 and d >= 23) or (m == 11 and d <= 21): return "Scorpio", "Intensitas & Ketajaman Insting"
    elif (m == 11 and d >= 22) or (m == 12 and d <= 21): return "Sagittarius", "Kebebasan & Visi Luas"
    elif (m == 12 and d >= 22) or (m == 1 and d <= 19): return "Capricorn", "Struktur & Kedisiplinan"
    elif (m == 1 and d >= 20) or (m == 2 and d <= 18): return "Aquarius", "Inovasi & Anti-Mainstream"
    else: return "Pisces", "Empati & Imajinasi Kuat"

# --- DATABASE ANALISA (BAHASA MERAKYAT TAPI MENDALAM) ---
data_analisa = {
    1: {"karakter": "Anda pada dasarnya adalah sosok perintis. Seringkali Anda merasa gatal kalau harus menunggu orang lain bergerak lebih dulu. Di luar, Anda mungkin terlihat tangguh dan mandiri, tapi di dalam hati, Anda terkadang merasa lelah memikul semuanya sendirian. Pikiran Anda selalu fokus pada tujuan masa depan.", "asmara": "Anda butuh pasangan yang tidak mengekang tapi tetap bisa mengimbangi langkah cepat Anda. Terkadang tanpa sadar bahasa Anda terdengar seperti 'memerintah' karena Anda ingin semuanya efisien. Cobalah sesekali menurunkan ego dan sekadar mendengarkan."},
    2: {"karakter": "Anda punya bakat alami sebagai 'penyerap energi' orang di sekitar Anda. Anda sangat peka terhadap perubahan suasana hati seseorang meski mereka diam. Kehebatan Anda adalah membuat orang merasa nyaman (Rapport), namun kelemahan Anda adalah sering mengorbankan perasaan sendiri demi menjaga perasaan orang lain.", "asmara": "Asmara bagi Anda adalah tentang rasa aman secara emosional. Berhentilah menjadi 'Penyelamat' untuk pasangan Anda. Anda berhak menuntut kebahagiaan yang sama rata, bukan sekadar memberi."},
    3: {"karakter": "Pikiran Anda sangat kaya akan imajinasi dan skenario. Anda sering memikirkan banyak ide brilian sekaligus, meski kadang kesulitan menyelesaikannya satu per satu. Anda pandai mencairkan suasana, tapi saat sedang sendirian, Anda sering memutar ulang percakapan masa lalu di kepala Anda.", "asmara": "Anda butuh koneksi yang menyenangkan dan tidak membosankan. Kebisuan adalah hal yang paling menyiksa Anda. Cari pasangan yang bisa menjadi tempat Anda bercerita tanpa dihakimi."},
    4: {"karakter": "Anda adalah perencana yang detail. Anda benci ketidakpastian dan kejutan yang tidak direncanakan. Pikiran Anda bekerja seperti laci-laci yang rapi. Orang mungkin melihat Anda kaku, padahal itu adalah cara bawah sadar Anda untuk memastikan semuanya aman dan terkendali.", "asmara": "Anda sangat setia pada komitmen, namun terkadang lupa untuk memberikan 'bumbu' romantis karena terlalu fokus pada hal logis dan praktis. Ingat, asmara itu urusan hati, bukan sekadar hitung-hitungan logika."},
    5: {"karakter": "Anda benci rutinitas yang monoton. Jiwa Anda butuh ruang gerak yang luas. Anda hebat dalam mencari celah di saat orang lain buntu. Namun di sisi lain, karena terlalu sering berpindah fokus, Anda kadang kehilangan arah dan bingung sebenarnya apa yang paling Anda cari dalam hidup ini.", "asmara": "Kata kunci untuk Anda adalah 'Kebebasan'. Hubungan yang terlalu menuntut akan membuat Anda diam-diam ingin melarikan diri. Anda butuh pasangan yang terasa seperti sahabat petualang."},
    6: {"karakter": "Pusat dari hidup Anda adalah keluarga dan orang-orang yang Anda sayangi. Anda seringkali menempatkan kebutuhan orang lain di atas kebutuhan Anda sendiri. Anda punya standar tanggung jawab yang sangat tinggi, yang terkadang membuat Anda gampang kecewa kalau orang lain tidak melakukan hal yang sama.", "asmara": "Anda sangat peduli, namun terkadang kepedulian Anda terasa seperti sedang 'mengatur'. Belajarlah untuk berhenti menebak-nebak apa yang dipikirkan pasangan.", unsafe_allow_html=True)
