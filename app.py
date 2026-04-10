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
    page_title="Neuro Nada Ultimate OS", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="collapsed" 
)
 
# --- CUSTOM CSS ---
st.markdown(
    """<style>
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
 
    .ulasan-box {
        background: rgba(30, 30, 30, 0.6); backdrop-filter: blur(10px);
        padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700; 
        margin-bottom: 12px; font-size: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .glass-container {
        background: rgba(25, 25, 25, 0.5); backdrop-filter: blur(12px);
        padding: 20px; border-radius: 12px; border: 1px solid rgba(212,175,55,0.2);
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.4); margin-bottom: 15px;
    }
    
    .primbon-box {
        background: linear-gradient(135deg, rgba(43,27,5,0.8) 0%, rgba(74,48,0,0.8) 100%);
        backdrop-filter: blur(10px); padding: 25px; border-radius: 12px; 
        border: 1px solid #D4AF37; box-shadow: 0 8px 25px rgba(212,175,55,0.3); 
        margin-top: 20px; margin-bottom: 20px;
    }

    .dynamic-reading-box {
        background: rgba(20, 20, 20, 0.7); backdrop-filter: blur(5px);
        padding: 20px; border-radius: 12px; border-left: 5px solid #FFD700;
        margin-top: 15px; margin-bottom: 15px; font-size: 15px; line-height: 1.6;
    }
    
    .matrix-container {
        display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap;
        padding: 15px; background: rgba(10,10,10,0.8); border-radius: 10px;
        border: 1px solid #333; margin-bottom: 5px; box-shadow: inset 0 2px 15px rgba(0,0,0,0.6);
    }
    .matrix-item { flex: 1; min-width: 80px; text-align: center; padding: 5px; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .matrix-value { font-size: 18px; font-weight: 900; color: white; }
    .matrix-value-special { color: #FFD700; }
    
    .list-punchy { padding-left: 20px; margin-bottom: 15px; font-size: 15px; }
    .list-punchy li { margin-bottom: 8px; }
    
    .live-badge {
        background: linear-gradient(90deg, #D4AF37, #FFD700);
        color: #000; padding: 8px 20px; border-radius: 30px;
        font-weight: 900; font-size: 14px; letter-spacing: 1px;
        display: inline-block; box-shadow: 0 4px 15px rgba(255,215,0,0.4);
    }
    </style>""", unsafe_allow_html=True
)
 
def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa Kosmik"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

def get_planetary_hour():
    planets = [
        ("Matahari ☀️", "Fokus otoritas & eksekusi.", "#FFD700"), 
        ("Venus 💖", "Negosiasi & pesona.", "#FF69B4"), 
        ("Merkurius 📝", "Komunikasi & ide.", "#00FFFF"), 
        ("Bulan 🌙", "Waktu intuitif & tenang.", "#F0F8FF"), 
        ("Saturnus 🪐", "Energi berat & disiplin.", "#8B4513"), 
        ("Yupiter 🍀", "Pintu rezeki & ekspansi.", "#32CD32"), 
        ("Mars ⚔️", "Agresi & aksi cepat.", "#FF4500")
    ]
    return planets[datetime.datetime.now().hour % 7]

# --- SIDEBAR PROMOSI ---
with st.sidebar:
    st.markdown(f"### {get_greeting()}")
    st.info("**Reset Pola Pikir Anda**\n\nSesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    st.markdown(f"[👉 **Amankan Jadwal Anda**](https://wa.me/628999771486)")
    st.caption("© 2026 Neuro Nada Academy")
 
# --- INTERFACE UTAMA ---
cur_planet, _, cur_color = get_planetary_hour()
st.markdown(f"<div style='text-align: right;'><div class='live-badge' style='background: {cur_color};'>🕒 LIVE PLANET: {cur_planet.upper()}</div></div>", unsafe_allow_html=True)
 
st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900; color:#FFD700;'>🌌 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown("---")
 
tgl_today = datetime.date.today()

# --- NEW: WETON ENGINE V2 (ACCURATE MODULE) ---
def get_neptu_weton(tanggal, is_after_sunset=False, kalibrasi_pasaran=0):
    # Aturan Sunset: Jika lahir setelah maghrib, masuk ke hari kalender Jawa berikutnya
    if is_after_sunset:
        tanggal = tanggal + datetime.timedelta(days=1)
        
    # Anchor Valid 1 Januari 2000 = Sabtu Legi
    anchor_date = datetime.date(2000, 1, 1)
    selisih_hari = (tanggal - anchor_date).days
    
    hari_n = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_n = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
    
    # 1 Jan 2000 adalah Sabtu (index 5)
    hari_idx = (5 + selisih_hari) % 7
    # 1 Jan 2000 adalah Legi (index 0). Kalibrasi ditambahkan untuk override manual Mazhab
    pasaran_idx = (selisih_hari + kalibrasi_pasaran) % 5
    
    hari = hari_n[hari_idx]
    pasaran = pasaran_n[pasaran_idx]
    
    # Nilai Mutlak dari Gramedia & UNESA
    n_hari = {"Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9}
    n_pas = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
    
    return (n_hari[hari] + n_pas[pasaran]), hari, pasaran

def get_rezeki_usaha(neptu):
    # Modulo 7 untuk Arah Rezeki
    mod_rezeki = neptu % 7 if neptu % 7 != 0 else 7
    rezeki = {
        1: ("Wasesa Segara", "Rezeki seluas lautan, pemaaf, dan mudah mencari sandang pangan."),
        2: ("Tunggak Semi", "Rezekinya selalu ada, patah tumbuh hilang berganti."),
        3: ("Satria Wibawa", "Mendapat kemuliaan, keberuntungan, dan dihormati banyak orang."),
        4: ("Sumur Sinaba", "Menjadi tempat bertanya, banyak ilmu, dan membawa berkah bagi sekitar."),
        5: ("Bumi Kapetak", "Harus bekerja sangat keras dan tahan banting, rawan kekecewaan."),
        6: ("Satria Wirang", "Sering menemui rintangan berat, rawan dipermalukan atau jatuh miskin."),
        7: ("Lebu Katiup Angin", "Rezeki cepat habis, rawan boros, dan cita-cita sering tidak menentu.")
    }
    
    # Modulo 5 untuk Potensi Usaha
    mod_usaha = neptu % 5 if neptu % 5 != 0 else 5
    usaha = {
        1: ("Sandang", "Kebutuhan dasar selalu tercukupi, sangat cocok untuk bisnis pakaian/kebutuhan pokok."),
        2: ("Pangan", "Makmur, rezeki berlimpah, garisan nasib sangat kuat di bisnis kuliner."),
        3: ("Beja", "Nasib selalu baik, kaya raya, dan penuh keberuntungan di segala bidang usaha."),
        4: ("Lara", "Rawan sakit hati/rugi dalam bisnis, butuh mitra yang tepat untuk mem-backup."),
        5: ("Pati", "Bahaya kerugian besar atau bangkrut, hindari spekulasi liar dan bisnis tanpa perhitungan.")
    }
    return rezeki[mod_rezeki], usaha[mod_usaha]

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

def get_dynamic_weton_kombo(neptu1, neptu2):
    # Menggunakan Modulo 8 (Standar Perjodohan)
    sisa = (neptu1 + neptu2) % 8
    if sisa == 0: sisa = 8
    
    hasil = {
        1: ("💔 PEGAT (Ujian Berat)", "Hubungan ini rentan terhadap masalah ekonomi, perselingkuhan, hingga potensi perpisahan. Membutuhkan kedewasaan ekstrem untuk bertahan."),
        2: ("👑 RATU (Kharisma Pasangan)", "Kalian berdua adalah pasangan yang sangat disegani. Banyak orang iri melihat keharmonisan kalian. Rezeki mengalir lancar."),
        3: ("💞 JODOH (Sinkronisasi Batin)", "Penerimaan bawah sadar luar biasa tinggi. Kalian menemukan kecocokan yang tidak bisa dijelaskan logika. Diramalkan rukun sampai tua."),
        4: ("🌱 TOPO (Ujian Bertumbuh)", "Fase awal pernikahan pasti penuh kesulitan dan adaptasi berat. Namun setelah melewati ujian masa krisis, kalian berdua akan sangat kaya dan bahagia."),
        5: ("💰 TINARI (Magnet Rezeki)", "Penyatuan energi kalian adalah magnet kelimpahan murni. Pintu rezeki akan selalu mudah terbuka, dan hidup tidak akan pernah kekurangan."),
        6: ("⚡ PADU (Gesekan Argumen)", "Rawan pertengkaran dan adu mulut. Meski sering ribut karena masalah sepele, pertengkaran ini jarang berujung pada perceraian."),
        7: ("👁️ SUJANAN (Rawan Curiga)", "Hubungan ini penuh dengan kecemburuan dan curiga. Rawan godaan pihak ketiga. Komunikasi harus ekstra transparan."),
        8: ("🕊️ PESTHI (Damai & Rukun)", "Hubungan yang adem ayem, rukun, dan minim masalah. Meski tidak terlalu kaya raya, namun hidup tangga kalian sangat damai sampai tua.")
    }
    return hasil.get(sisa)
 
# --- MENU TABS ---
tab1, tab2 = st.tabs(["👤 Personal Identity", "👩‍❤️‍👨 Couple Matrix (Jodoh)"])
 
# ==========================================
# TAB 1: IDENTITAS KOSMIK & REZEKI
# ==========================================
with tab1:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("Akses Blueprint Weton & Rezeki")
    nama_user = st.text_input("Nama Lengkap:", key="t1_nama")
    tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date(1983, 9, 23), min_value=datetime.date(1900, 1, 1), max_value=tgl_today, format="DD/MM/YYYY")
    
    # FITUR SAKTI PENYELESAI BENTROK KALENDER
    st.info("💡 **Tips Akurasi:** Jika hasil Weton tidak sesuai dengan yang Anda ketahui, gunakan tuas kalibrasi di bawah ini untuk menggeser perhitungan kalender masehi.")
    col_a, col_b = st.columns(2)
    with col_a:
        is_maghrib = st.checkbox("🌙 Lahir Setelah Maghrib (18:00+)?", help="Dalam kalender Jawa, hari berganti saat matahari terbenam.")
    with col_b:
        kalibrasi_p = st.number_input("⚙️ Koreksi Pasaran (Geser Manual)", min_value=-2, max_value=2, value=0, help="Gunakan ini jika weton meleset karena perbedaan Mazhab Keraton (Aboge/Asapon).")
    st.markdown("</div>", unsafe_allow_html=True)
 
    if st.button("Kalkulasi Takdir"):
        if nama_user:
            st.snow()
            nep, hari, pasaran = get_neptu_weton(tgl_input, is_maghrib, kalibrasi_p)
            wet = f"{hari} {pasaran}"
            zod = get_zodiak(tgl_input)
            
            rezeki_data, usaha_data = get_rezeki_usaha(nep)
            
            st.markdown(f"<h3 style='text-align:center;'>🌌 Blueprint Kosmik: {nama_user}</h3>", unsafe_allow_html=True)
            st.markdown(f"""
<div class="matrix-container">
<div class="matrix-item"><div class="matrix-label">Filter Zodiak</div><div class="matrix-value">{zod}</div></div>
<div class="matrix-item"><div class="matrix-label">Weton Asli</div><div class="matrix-value matrix-value-special">{wet}</div></div>
<div class="matrix-item"><div class="matrix-label">Total Neptu</div><div class="matrix-value">{nep}</div></div>
</div>
""", unsafe_allow_html=True)

            st.markdown(f"""
<div class="primbon-box">
<h4 style="color: #D4AF37; margin-top:0;">📊 Pembacaan Garis Rezeki & Usaha (Mod 7 & Mod 5)</h4>
<p style="color:#aaa;">Sistem membedah nilai neptu <b>{nep}</b> Anda menggunakan pembagi matematis primbon untuk mengetahui arketipe kekayaan Anda:</p>
<ul style="line-height: 1.8;">
<li><b>Arah Rezeki Harian: <span style="color:#FFD700;">{rezeki_data[0]}</span></b><br><i>"{rezeki_data[1]}"</i></li>
<li><b>Potensi Karir/Usaha: <span style="color:#25D366;">{usaha_data[0]}</span></b><br><i>"{usaha_data[1]}"</i></li>
</ul>
</div>
""", unsafe_allow_html=True)
 
# ==========================================
# TAB 2: COUPLE MATRIX (MODULO 8)
# ==========================================
with tab2:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("Sistem Kalkulasi Perjodohan")
    st.write("Menggunakan algoritma Penjumlahan Neptu (Sisa Pembagian 8).")
    
    ca, cb = st.columns(2)
    with ca: 
        n1 = st.text_input("Nama Pria", key="n1")
        d1 = st.date_input("Lahir Pria", value=datetime.date(1983, 9, 23), key="d1")
        m1 = st.checkbox("🌙 Lahir Setelah Maghrib?", key="m1")
        k1 = st.number_input("⚙️ Koreksi Pasaran", min_value=-2, max_value=2, value=0, key="k1")
    with cb: 
        n2 = st.text_input("Nama Wanita", key="n2")
        d2 = st.date_input("Lahir Wanita", value=datetime.date(1984, 6, 13), key="d2")
        m2 = st.checkbox("🌙 Lahir Setelah Maghrib?", key="m2")
        k2 = st.number_input("⚙️ Koreksi Pasaran", min_value=-2, max_value=2, value=0, key="k2")
    st.markdown("</div>", unsafe_allow_html=True)
        
    if st.button("Bedah Takdir Hubungan"):
        if n1 and n2:
            st.snow()
            nep_1, hari1, pas1 = get_neptu_weton(d1, m1, k1)
            nep_2, hari2, pas2 = get_neptu_weton(d2, m2, k2)
            
            total_neptu = nep_1 + nep_2
            judul_jodoh, desk_jodoh = get_dynamic_weton_kombo(nep_1, nep_2)
            
            st.markdown("---")
            st.markdown(f"### 🔮 Matriks Penyatuan: {n1} & {n2}")
            
            st.markdown(f"""
<div class="matrix-container">
<div class="matrix-item"><div class="matrix-label">Neptu Pria</div><div class="matrix-value">{hari1} {pas1} ({nep_1})</div></div>
<div class="matrix-item"><div class="matrix-label">Neptu Wanita</div><div class="matrix-value">{hari2} {pas2} ({nep_2})</div></div>
<div class="matrix-item" style="background: rgba(212,175,55,0.2);"><div class="matrix-label" style="color:#FFD700;">TOTAL NEPTU</div><div class="matrix-value matrix-value-special">{total_neptu}</div></div>
</div>
""", unsafe_allow_html=True)
            
            st.markdown(f"""
<div class="dynamic-reading-box" style="border-left-color: #25D366;">
<h4 style="color: #25D366; margin-top:0;">{judul_jodoh}</h4>
<p>Berdasarkan sisa pembagian algoritma pernikahan Jawa (Pegat, Ratu, Jodoh, Topo, Tinari, Padu, Sujanan, Pesthi), takdir hubungan kalian terkunci di hasil ini:<br><br>
<b>{desk_jodoh}</b></p>
</div>
""", unsafe_allow_html=True)
