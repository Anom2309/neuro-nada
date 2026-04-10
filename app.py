import streamlit as st
import datetime
import math
import random
import plotly.graph_objects as go
from datetime import time as dt_time

# ==========================================
# 🌌 NEURO NADA: BADAI ULTIMATE v3.0
# ==========================================

st.set_page_config(
    page_title="NEURO NADA: BADAI ULTIMATE",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- LUXURY CSS BEYOND LIMITS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;800&display=swap');
    
    .stApp { background: radial-gradient(circle at top, #1a1a2e 0%, #050505 100%); }
    
    h1 { font-family: 'Orbitron', sans-serif; color: #FFD700; text-shadow: 0 0 20px rgba(255,215,0,0.5); }
    
    .ultimate-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }
    
    .metric-box {
        text-align: center;
        padding: 15px;
        border-right: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    .status-badge {
        background: linear-gradient(90deg, #D4AF37, #FFD700);
        color: black;
        padding: 4px 12px;
        border-radius: 50px;
        font-weight: 900;
        font-size: 12px;
        text-transform: uppercase;
    }

    div.stButton > button {
        background: linear-gradient(45deg, #B8860B 0%, #FFD700 100%) !important;
        color: black !important; font-weight: 900 !important;
        letter-spacing: 2px !important; border: none !important;
        padding: 20px !important; border-radius: 50px !important;
        transition: 0.5s ease;
    }
    div.stButton > button:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(255,215,0,0.4); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 ULTIMATE LOGIC ENGINES
# ==========================================

def get_jummal(nama):
    values = {'a':1, 'b':2, 'j':3, 'd':4, 'h':5, 'w':6, 'z':7, 't':9, 'y':10, 'k':20, 'l':30, 'm':40, 'n':50, 's':60, 'f':80, 'q':100, 'r':200, 'g':1000, 'i':10}
    clean = ''.join(filter(str.isalpha, nama.lower()))
    return sum(values.get(h, 0) for h in clean) if clean else 1

def get_planetary_hour():
    # Logika Jam Planet (Simplified for Real-time App)
    planets = ["Matahari (Otoritas)", "Venus (Asmara/Uang)", "Merkurius (Komunikasi)", "Bulan (Intuisi)", "Saturnus (Disiplin/Karma)", "Yupiter (Ekspansi)", "Mars (Aksi)"]
    now = datetime.datetime.now()
    index = now.hour % 7
    return planets[index]

def get_betaljemur_full(tanggal):
    anchor = datetime.date(1900, 1, 1) # Support sejak 1900
    diff = (tanggal - anchor).days
    
    hari_n = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_n = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"] # Adjusted for 1900 anchor
    
    h_idx = tanggal.weekday()
    p_idx = diff % 5
    
    n_hari = [4, 3, 7, 8, 6, 9, 5] # Sen, Sel, Rab, Kam, Jum, Sab, Min
    n_pas = [9, 7, 4, 8, 5] # Pah, Pon, Wag, Kli, Leg
    
    neptu = n_hari[h_idx] + n_pas[p_idx]
    
    lakuning = {
        7: ("Lebu Katiup Angin", "Pikiran liar, butuh grounding."),
        8: ("Lakuning Geni", "Energi api, cocok untuk eksekutor."),
        9: ("Lakuning Angin", "Adaptif, mudah bergaul, gampang dipengaruhi."),
        10: ("Pandito Mbangun Teki", "Jiwa guru, suka menolong, pemikir dalam."),
        11: ("Macan Ketawan", "Garis pemimpin, tidak suka diperintah."),
        12: ("Lakuning Kembang", "Magnetis, disukai banyak orang secara natural."),
        13: ("Lakuning Lintang", "Kharisma misterius, kuat dalam kesunyian."),
        14: ("Lakuning Rembulan", "Penenang, pembawa solusi, sangat empati."),
        15: ("Lakuning Srengenge", "Wibawa matahari, logis, keras kepala."),
        16: ("Lakuning Banyu", "Tenang tapi mampu menghancurkan rintangan."),
        17: ("Lakuning Bumi", "Sangat stabil, tempat bersandar yang kuat."),
        18: ("Paripurna", "Kekuatan utuh, visioner tingkat tinggi.")
    }
    
    naga = ["TIMUR", "SELATAN", "BARAT", "UTARA", "TIMUR", "SELATAN", "SELATAN"][h_idx]
    
    return neptu, f"{hari_n[h_idx]} {pasaran_n[p_idx]}", lakuning.get(neptu, ("Unik", "Kompleks")), naga

# ==========================================
# 🏗️ THE APP INTERFACE
# ==========================================

st.markdown("<h1 style='text-align: center;'>👑 NEURO NADA: BADAI ULTIMATE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #D4AF37; letter-spacing: 5px; font-weight: bold;'>DECODE YOUR DESTINY ENGINE</p>", unsafe_allow_html=True)

# --- LIVE TRACKER BAR ---
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='status-badge'>🕒 Jam Planet: {get_planetary_hour()}</div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='status-badge'>📅 {datetime.datetime.now().strftime('%d %B %Y')}</div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='status-badge'>🛰️ GPS: TANGERANG ALIGNED</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- INPUT AREA ---
with st.container():
    st.markdown("<div class='ultimate-card'>", unsafe_allow_html=True)
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        u_nama = st.text_input("NAMA LENGKAP", placeholder="Ketik nama Anda...")
    with col_in2:
        # TAHUN TERBUKA DARI 1900
        u_dob = st.date_input("TANGGAL LAHIR", value=datetime.date(1990, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2026, 12, 31))
    
    btn = st.button("EXECUTE SYSTEM SCAN")
    st.markdown("</div>", unsafe_allow_html=True)

if btn and u_nama:
    with st.spinner("🌀 Meretas Frekuensi Alam Semesta..."):
        # Processing
        v_jum = get_jummal(u_nama)
        v_nep, v_wet, v_laku, v_naga = get_betaljemur_full(u_dob)
        v_elemen = ["💧 AIR", "🔥 API", "🌍 TANAH", "💨 UDARA"][v_jum % 4]
        
        # --- OUTPUT AREA ---
        st.balloons()
        
        # 1. THE MATRIX BOX
        st.markdown(f"""
        <div class='ultimate-card'>
            <div style='display: flex; justify-content: space-around; flex-wrap: wrap;'>
                <div class='metric-box'><small>VIBRASI NAMA</small><br><span style='font-size: 24px; font-weight: 900; color: #FFD700;'>{v_jum}</span></div>
                <div class='metric-box'><small>WETON</small><br><span style='font-size: 24px; font-weight: 900;'>{v_wet}</span></div>
                <div class='metric-box'><small>NEPTU</small><br><span style='font-size: 24px; font-weight: 900;'>{v_nep}</span></div>
                <div class='metric-box' style='border:none;'><small>ELEMEN</small><br><span style='font-size: 24px; font-weight: 900; color: #FFD700;'>{v_elemen}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. THE DEEP INSIGHT
        res_col1, res_col2 = st.columns([2, 1])
        
        with res_col1:
            st.markdown(f"""
            <div class='ultimate-card'>
                <h3 style='color:#FFD700;'>📜 Arketipe: {v_laku[0]}</h3>
                <p style='font-size: 18px; line-height: 1.6;'>"{v_laku[1]}"</p>
                <hr style='border: 0.5px solid rgba(212,175,55,0.2);'>
                <p><b>ANALISIS NLP:</b> Nama Anda bergetar pada frekuensi <b>{v_jum}</b>. Dalam pola pikir bawah sadar, Anda cenderung <b>{v_laku[0]}</b>. Ini berarti saat Anda di bawah tekanan, sistem saraf Anda akan mencari keseimbangan melalui elemen <b>{v_elemen}</b>.</p>
                <p style='color: #25D366;'><b>🧭 ARAH KEJAYAAN: {v_naga}</b></p>
                <small>*Gunakan arah {v_naga} saat memulai bisnis atau menghadap meja kerja untuk sinkronisasi energi bumi.</small>
            </div>
            """, unsafe_allow_html=True)
            
        with res_col2:
            st.markdown(f"""
            <div class='ultimate-card' style='text-align: center;'>
                <h4 style='color:#FFD700;'>MOMENTUM LIVE</h4>
                <p>Saat ini adalah jam:</p>
                <div style='background: #D4AF37; color: black; padding: 10px; border-radius: 10px; font-weight: 900;'>{get_planetary_hour().upper()}</div>
                <p style='font-size: 12px; margin-top: 10px;'>Waktu terbaik untuk melakukan tindakan yang selaras dengan energi planet tersebut.</p>
            </div>
            """, unsafe_allow_html=True)

        # 3. CALL TO ACTION BRUTAL
        st.markdown(f"""
        <a href="https://wa.me/628999771486?text=Coach%20Ahmad,%20saya%20siap%20bedah%20Kode%20{v_jum}%20dan%20Weton%20{v_wet}" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(90deg, #ff4b4b, #8b0000); color: white; padding: 25px; text-align: center; border-radius: 15px; font-weight: 900; font-size: 20px; box-shadow: 0 10px 30px rgba(255,0,0,0.3);">
                🚨 RE-PROGRAM ALAM BAWAH SADAR ANDA SEKARANG
            </div>
        </a>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><center><p style='color: #555;'>Neuro Nada BADAI ULTIMATE Engine © 2026<br>Designed for Ahmad Septian Dwi Cahyo</p></center>", unsafe_allow_html=True)
