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
    /* Mengubah font global agar lebih clean */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Warna tombol utama (Kuning Emas) */
    div.stButton > button {
        background-color: #FFD700 !important; color: #000000 !important;
        font-weight: bold !important; border: none !important;
        padding: 10px 20px !important; border-radius: 8px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.01); background-color: #FFC107 !important; }
    
    /* Box Ulasan */
    .ulasan-box {
        background-color: #1e1e1e; padding: 12px; border-radius: 8px;
        border-left: 3px solid #FFD700; margin-bottom: 8px; font-size: 14px;
    }
    
    /* Box Cosmic Timing */
    .cosmic-box {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a4a 100%);
        padding: 15px; border-radius: 10px; border: 1px solid #4a4a8a;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5); margin-bottom: 15px;
    }
    
    /* --- CSS UNTUK MATRIKS IDENTITAS KECIL (THE FIX) --- */
    .matrix-container {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        padding: 10px;
        background-color: #101010;
        border-radius: 8px;
        border: 1px solid #333;
        margin-bottom: 15px;
    }
    .matrix-item {
        flex: 1;
        text-align: center;
        padding: 5px;
        border-right: 1px solid #333;
    }
    .matrix-item:last-child {
        border-right: none;
    }
    .matrix-label {
        font-size: 11px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 2px;
    }
    .matrix-value {
        font-size: 16px;
        font-weight: 800;
        color: white;
    }
    .matrix-value-special {
        color: #FFD700; /* Warna kuning untuk angka */
    }
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

st.markdown("<h1 style='text-align: center; margin-top: 10px;'>🌌 Neuro Nada Cosmic Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #D4AF37; margin-bottom:0;'>Integrasi Falak, Weton, Numerologi & Psikologi Bawah Sadar</p>", unsafe_allow_html=True)
st.markdown("---")

# --- FUNGSI FALAK & WAKTU (MOON PHASE ENGINE) ---
def get_moon_phase(date):
    epoch = datetime.date(2000, 1, 6)
    days = (date - epoch).days
    lunations = days / 29.53058867
    phase = lunations % 1
    if phase < 0.03 or phase > 0.97: return "🌑 Bulan Baru (New Moon)", "Introspeksi Dalam, Tersembunyi, Potensi Inkubasi", "Fokus internal sedang sangat kuat. Anda menyerap banyak energi alam bawah sadar."
    elif phase < 0.22: return "🌒 Bulan Sabit Awal (Waxing Crescent)", "Niat Eksekusi, Momentum, Pertumbuhan Awal", "Anda memiliki dorongan alami untuk memulai hal baru dan menarik peluang."
    elif phase < 0.28: return "🌓 Paruh Awal (First Quarter)", "Aksi Nyata, Menerobos Hambatan, Analitis", "Fase ini memberikan Anda karakter petarung yang cepat bereaksi terhadap rintangan."
    elif phase < 0.47: return "🌔 Bulan Cembung (Waxing Gibbous)", "Penyempurnaan, Penyesuaian Emosional, Teliti", "Fokus Anda tajam pada detail. Anda terus mengevaluasi sebelum mencapai titik final."
    elif phase < 0.53: return "🌕 Bulan Purnama (Full Moon)", "Puncak Emosi, Ekspresif, Daya Tarik Magis", "Gelombang otak Anda saat lahir dalam kondisi puncak. Anda karismatik namun rentan meledak."
    elif phase < 0.72: return "🌖 Bulan Susut (Waning Gibbous)", "Syukur, Melepaskan, Distribusi Pengetahuan", "Anda memiliki bakat menjadi mentor dan merasa damai ketika membagikan pencapaian."
    elif phase < 0.78: return "🌗 Paruh Akhir (Last Quarter)", "Transisi, Pembersihan Mental, Evaluasi Keras", "Anda sangat berani membuang hal-hal toxic dan tidak suka menyimpan masa lalu."
    else: return "🌘 Bulan Sabit Akhir (Waning Crescent)", "Istirahat, Penyembuhan Jiwa, Persiapan", "Anda memancarkan energi penyembuh (Healer) dan sangat intuitif."

def get_daily_timing():
    today = datetime.date.today()
    phase_name, _, _ = get_moon_phase(today)
    if "New Moon" in phase_name or "Crescent" in phase_name: return phase_name, "🟢 WAKTU EKSEKUSI IDE BARU. Bagus untuk memulai project atau keputusan besar."
    elif "Full Moon" in phase_name or "Waxing Gibbous" in phase_name: return phase_name, "🔴 WAKTU RAWAN KONFLIK EGO. Tunda negosiasi berat atau perdebatan asmara hari ini."
    else: return phase_name, "🟡 WAKTU EVALUASI & REHAT. Bagus untuk audit diri dan melepaskan hal toxic."

# --- FUNGSI LOGIKA MATEMATIKA, WETON, ZODIAK (TETAP SAMA) ---
def hitung_angka(tanggal):
    total = sum(int(digit) for digit in tanggal.strftime("%d%m%Y"))
    while total > 9: total = sum(int(digit) for digit in str(total))
    return total

def hitung_angka_nama(nama):
    huruf_angka = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':1, 'K':2, 'L':3, 'M':4, 'N':5, 'O':6, 'P':7, 'Q':8, 'R':9, 'S':1, 'T':2, 'U':3, 'V':4, 'W':5, 'X':6, 'Y':7, 'Z':8}
    total = sum(huruf_angka.get(h, 0) for h in nama.upper())
    if total == 0: return 1
    while total > 9: total = sum(int(d) for d in str(total))
    return total

def get_neptu_weton(tanggal):
    anchor_date = datetime.date(2000, 1, 1)
    selisih_hari = (tanggal - anchor_date).days
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][tanggal.weekday()]
    pasaran = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"][selisih_hari % 5]
    return f"{hari} {pasaran}"

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

def get_arketipe(angka):
    arketipe_dict = {1: "The Leader", 2: "The Mediator", 3: "The Communicator", 4: "The Architect", 5: "The Explorer", 6: "The Nurturer", 7: "The Analyst", 8: "The Strategist", 9: "The Humanist"}
    return arketipe_dict.get(angka, "Pribadi Unik")

# --- MENU TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Identitas Kosmik", "👩‍❤️‍👨 Sinkronisasi Asmara", "🕸️ Audit Sistem Saraf"])

# ==========================================
# TAB 1: IDENTITAS KOSMIK (FIXED SIZE SECTION)
# ==========================================
with tab1:
    st.subheader("Bongkar Blueprint Bawah Sadar Anda")
    nama_user = st.text_input("Nama Lengkap:", placeholder="Ketik nama Anda...", key="t1_nama")
    tgl_today = datetime.date.today()
    tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date(1995, 1, 1), min_value=datetime.date(1920, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")

    if st.button("Kalkulasi Cetak Biru (Blueprint)"):
        if not nama_user or len(nama_user.strip()) < 3:
            st.error("🚨 Mohon ketik nama lengkap agar vibrasi identitas akurat.")
        elif tgl_input == tgl_today:
            st.error("🚨 Tanggal lahir belum valid.")
        else:
            with st.spinner('Menghitung posisi langit dan algoritma pikiran...'):
                time.sleep(2)
                
                angka_hasil = hitung_angka(tgl_input)
                angka_nama = hitung_angka_nama(nama_user)
                weton_hasil = get_neptu_weton(tgl_input)
                zod_nama = get_zodiak(tgl_input)
                moon_phase, moon_sifat, moon_detail = get_moon_phase(tgl_input)
                today_phase, today_guidance = get_daily_timing()
                arketipe = get_arketipe(angka_hasil)
            
            st.balloons()
            st.markdown(f"### 🌌 Hasil Mapping Kosmik: {nama_user}")
            
            # --- DAILY GUIDANCE KOSMIK ---
            st.markdown(f"""
            <div class="cosmic-box">
                <p style="color: #ccc; font-size: 12px; text-align: center; margin:0;">Timing Falak Hari Ini: {today_phase}</p>
                <div style="text-align: center; font-weight: bold; color: white; font-size: 14px;">
                    {today_guidance}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- MATRIKS IDENTITAS (THE FIX: HTML & CSS CUSTOM FOR SMALL SIZE) ---
            st.markdown(f"""
            <div class="matrix-container">
                <div class="matrix-item">
                    <div class="matrix-label">Kode Nama</div>
                    <div class="matrix-value matrix-value-special">{angka_nama}</div>
                </div>
                <div class="matrix-item">
                    <div class="matrix-label">Kode Program</div>
                    <div class="matrix-value matrix-value-special">{angka_hasil}</div>
                </div>
                <div class="matrix-item">
                    <div class="matrix-label">Energi Weton</div>
                    <div class="matrix-value">{weton_hasil}</div>
                </div>
                <div class="matrix-item">
                    <div class="matrix-label">Pola Zodiak</div>
                    <div class="matrix-value">{zod_nama}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- HASIL LENGKAP JADI JELAS KELIHATAN DI BAWAHNYA ---
            st.subheader("🌑 Fase Bulan Lahir (Falak)")
            st.info(f"Fase **{moon_phase}**. Karakter: **{moon_sifat}**.\n\n{moon_detail}")

            st.subheader("🧬 Analisis Bio-Psikologi NLP")
            st.write(f"Perpaduan energi langit **{moon_phase}**, arketipe dasar **{arketipe}**, dan akar budaya **{weton_hasil}** membentuk algoritma pikiran yang unik pada diri Anda.")

            st.markdown("---")
            st.error(f"🚨 **DETEKSI KEBOCORAN ENERGI (Shadow Self)**\n\nSistem membaca adanya hambatan bawah sadar yang sering menyabotase potensi **{arketipe}** Anda. Pola ini akan terus berulang jika tidak segera di-kalibrasi.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <a href="https://lynk.id/neuronada" target="_blank" style="text-decoration: none;">
                <div style="background-color: #FFD700; color: black; padding: 12px; text-align: center; border-radius: 8px; font-weight: bold; font-size: 16px;">
                    🔓 AMBIL MODUL TERAPI KODE {angka_hasil} SEKARANG
                </div>
            </a>
            """, unsafe_allow_html=True)
            st.markdown("---")

# ==========================================
# TAB 2 & 3 (TETAP SAMA)
# ==========================================
with tab2:
    st.subheader("Sinkronisasi Asmara")
    c1, c2 = st.columns(2)
    with c1: 
        n1 = st.text_input("Nama Anda", key="n1")
        d1 = st.date_input("Lahir Anda", value=datetime.date(1995, 1, 1), key="d1")
    with c2: 
        n2 = st.text_input("Nama Pasangan", key="n2")
        d2 = st.date_input("Lahir Pasangan", value=datetime.date(1995, 1, 1), key="d2")
        
    if st.button("Cek Kompatibilitas"):
        if n1 and n2:
            neptu1 = get_neptu_weton(d1); neptu2 = get_neptu_weton(d2)
            selisih = abs(hitung_angka(d1) - hitung_angka(d2))
            st.markdown("---")
            st.info(f"Analisis Weton: **{neptu1}** & **{neptu2}**. Hubungan kalian unik.")
            if selisih in [0, 3, 6, 9]: st.success("💘 **SKOR NLP: SANGAT SINKRON (90%)**")
            else: st.warning("⚖️ **SKOR NLP: BUTUH KALIBRASI (70%)**")

with tab3:
    st.subheader("🕸️ Audit Keseimbangan Pikiran")
    skor = [st.slider(k, 1, 10, 5) for k in ['Mental', 'Karir', 'Asmara', 'Spiritual', 'Fisik']]
    if st.button("Lihat Radar"):
        fig = go.Figure(data=go.Scatterpolar(r=skor+[skor[0]], theta=['Mental','Karir','Asmara','Spiritual','Fisik','Mental'], fill='toself'))
        st.plotly_chart(fig)

# ==========================================
# ULASAN
# ==========================================
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Jejak Transformasi Terbaru</h3>", unsafe_allow_html=True)
daftar_ulasan = ambil_ulasan()
for u in daftar_ulasan[:5]:
    if u.get("Komentar"): 
        st.markdown(f'<div class="ulasan-box"><b>{u.get("Nama")}</b> ⭐⭐⭐⭐⭐<br><i>"{u.get("Komentar")}"</i></div>', unsafe_allow_html=True)

with st.expander("💬 Tinggalkan Jejak Transformasi"):
    with st.form("form_review"):
        rn = st.text_input("Nama")
        rk = st.text_area("Ulasan")
        if st.form_submit_button("Kirim") and rn and rk:
            if kirim_ulasan(rn, "5", rk): st.success("Terkirim!"); time.sleep(1); st.rerun()

st.markdown("---")
st.markdown("<center><b>Ahmad Septian Dwi Cahyo</b><br><small>Neuro Nada Cosmic © 2026</small></center>", unsafe_allow_html=True)
