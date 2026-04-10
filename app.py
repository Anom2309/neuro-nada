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

# ==========================================
# 🌌 NEURO NADA ULTIMATE ENGINE v2.0
# ==========================================

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="Neuro Nada Ultimate Analysis", 
    page_icon="🌌", 
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- CUSTOM CSS (DARK GOLD LUXURY) ---
st.markdown(
    """<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; background-color: #050505; }
    
    .stApp { background-color: #050505; }
    
    div.stButton > button {
        background: linear-gradient(90deg, #D4AF37 0%, #FFD700 100%) !important;
        color: #000 !important; font-weight: 900 !important;
        border: none !important; padding: 15px !important; border-radius: 12px !important;
        transition: 0.3s; box-shadow: 0 4px 15px rgba(212,175,55,0.4);
    }
    div.stButton > button:hover { transform: scale(1.02); box-shadow: 0 6px 20px rgba(212,175,55,0.6); }

    .matrix-container {
        display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap;
        padding: 15px; background: rgba(20,20,20,0.8); border-radius: 12px;
        border: 1px solid #333; margin-bottom: 25px;
    }
    .matrix-item { flex: 1; min-width: 90px; text-align: center; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    .matrix-value { font-size: 18px; font-weight: 900; color: #FFD700; }

    .primbon-box {
        background: linear-gradient(135deg, #1a1202 0%, #2d1e00 100%);
        padding: 25px; border-radius: 15px; border: 1px solid #D4AF37;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8); margin: 20px 0;
    }
    
    .naga-dina-badge {
        background: #D4AF37; color: #000; padding: 5px 12px;
        border-radius: 20px; font-weight: 900; font-size: 12px;
    }
    </style>""", unsafe_allow_html=True
)

# ==========================================
# 🔢 CORE LOGIC: THE ANCIENT ALGORITHMS
# ==========================================

# 1. HISAB JUMMAL (ILMU HURUF)
def hitung_jummal(nama):
    # Mapping Abjad Esoterik (Nilai Getaran)
    abjad_values = {
        'a': 1, 'b': 2, 'j': 3, 'd': 4, 'h': 5, 'w': 6, 'z': 7, 
        't': 9, 'y': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 
        's': 60, 'f': 80, 'q': 100, 'r': 200, 'g': 1000, 'i': 10
    }
    nama_clean = ''.join(filter(str.isalpha, nama.lower()))
    total = sum(abjad_values.get(h, 0) for h in nama_clean)
    return total if total > 0 else 1

# 2. BETALJEMUR ADAMMAKNA (WETON & PANGARASAN)
def get_betaljemur_engine(tanggal):
    anchor = datetime.date(2000, 1, 1) # Sabtu Legi
    diff = (tanggal - anchor).days
    
    hari_n = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_n = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
    
    hari = hari_n[tanggal.weekday()]
    pasaran = pasaran_n[diff % 5]
    
    n_hari = {"Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9}
    n_pas = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
    
    neptu = n_hari[hari] + n_pas[pasaran]
    
    # Pangarasan (Meta-Program Jawa)
    lakuning = {
        7: ("Lebu Katiup Angin", "Fokus mudah goyah, butuh anchoring kuat."),
        8: ("Lakuning Geni", "Emosi meledak, punya daya dobrak besar."),
        9: ("Lakuning Angin", "Sangat adaptif, namun mudah kena sugesti."),
        10: ("Pandito Mbangun Teki", "Pola pikir Deep Structure, suka analisa."),
        11: ("Macan Ketawan", "Otoritas tinggi, benci dikontrol orang."),
        12: ("Lakuning Kembang", "Rapport natural, ahli diplomasi."),
        13: ("Lakuning Lintang", "Kharisma misterius, suka menyendiri."),
        14: ("Lakuning Rembulan", "Penenang batin, empati level tinggi."),
        15: ("Lakuning Srengenge", "Logis, berwibawa, pencerah kegelapan."),
        16: ("Lakuning Banyu", "Tenang tapi menghanyutkan, prinsip kuat."),
        17: ("Lakuning Bumi", "Penyabar, pengayom, fondasi yang kokoh."),
        18: ("Paripurna", "Otoritas mutlak, pemimpin para pemimpin.")
    }
    
    # Naga Dina (Arah Kejayaan - Fitur Gila lo, Bro)
    naga_dina = {
        "Minggu": "TIMUR (Kejayaan)", "Senin": "SELATAN (Kejayaan)",
        "Selasa": "BARAT (Kejayaan)", "Rabu": "UTARA (Kejayaan)",
        "Kamis": "TIMUR (Kejayaan)", "Jumat": "SELATAN (Kejayaan)",
        "Sabtu": "SELATAN (Kejayaan)"
    }
    
    laku_nama, laku_desc = lakuning.get(neptu, ("Anomali", "Karakter unik"))
    return neptu, f"{hari} {pasaran}", laku_nama, laku_desc, naga_dina.get(hari)

# ==========================================
# 🖥️ INTERFACE UTAMA
# ==========================================

st.markdown("<h1 style='text-align: center; font-weight: 900; color: #FFD700;'>🌌 NEURO NADA ULTIMATE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Sistem Navigasi Takdir: Gematria, Betaljemur, & NLP Alignment</p>", unsafe_allow_html=True)

# INPUT DATA
col_a, col_b = st.columns(2)
with col_a:
    nama = st.text_input("Nama Lengkap (Asli):", placeholder="Contoh: Ahmad Septian")
with col_b:
    dob = st.date_input("Tanggal Lahir:", value=datetime.date(1995, 1, 1))

if st.button("RUN DEEP ANALYSIS"):
    if nama:
        # Jalankan Mesin
        val_jummal = hitung_jummal(nama)
        neptu, weton, laku_n, laku_d, arah = get_betaljemur_engine(dob)
        elemen = {1: "🔥 API", 2: "🌍 TANAH", 3: "💨 UDARA", 0: "💧 AIR"}.get(val_jummal % 4)
        
        # --- 1. THE MATRIX METRICS ---
        st.markdown(f"""
        <div class="matrix-container">
            <div class="matrix-item"><div class="matrix-label">Vibrasi Nama</div><div class="matrix-value">{val_jummal}</div></div>
            <div class="matrix-item"><div class="matrix-label">Elemen</div><div class="matrix-value">{elemen}</div></div>
            <div class="matrix-item"><div class="matrix-label">Weton</div><div class="matrix-value">{weton}</div></div>
            <div class="matrix-item"><div class="matrix-label">Neptu</div><div class="matrix-value">{neptu}</div></div>
        </div>
        """, unsafe_allow_html=True)

        # --- 2. FITUR GILA: BETALJEMUR INSIGHT ---
        st.markdown(f"""
        <div class="primbon-box">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <span style="color: #D4AF37; font-weight: 900; letter-spacing: 1px;">📜 KODE BETALJEMUR ADAMMAKNA</span>
                <span class="naga-dina-badge">🧭 ARAH HOKI: {arah}</span>
            </div>
            <h2 style="color: #FFF; margin: 0;">{laku_n}</h2>
            <p style="color: #CCC; font-style: italic; font-size: 16px;">"{laku_d}"</p>
            <hr style="border-color: #444;">
            <p style="color: #AAA; font-size: 14px;">
                <b>Strategi Usaha:</b> Berdasarkan Naga Dina hari lahir Anda, posisi terbaik saat melakukan negosiasi bisnis atau membangun toko adalah menghadap ke <b>{arah.split()[0]}</b>. Ini akan menyelaraskan bio-elektromagnetik tubuh Anda dengan energi bumi.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # --- 3. AUDIT SISTEM SARAF (NLP WHEEL) ---
        st.subheader("🕸️ Audit Resonansi Saat Ini")
        kategori = ['Mental', 'Finansial', 'Asmara', 'Spiritual', 'Fisik']
        values = [random.randint(5, 10) for _ in range(5)] # Placeholder Audit
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],
            theta=kategori + [kategori[0]],
            fill='toself',
            fillcolor='rgba(212, 175, 55, 0.3)',
            line=dict(color='#D4AF37')
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False, paper_bgcolor="#050505", plot_bgcolor="#050505")
        st.plotly_chart(fig)

        # --- 4. CTA REPROGRAMMING ---
        st.success(f"### Analisis Selesai, {nama.split()[0]}!")
        st.write(f"Vibrasi nama Anda (**{val_jummal}**) menunjukkan potensi hambatan pada area komunikasi. Gunakan arah **{arah}** sebagai jangkar (anchor) saat memulai meditasi atau bekerja.")
        
        st.markdown(f"""
        <a href="https://wa.me/628999771486" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(90deg, #ff4b4b 0%, #ff0000 100%); color: white; padding: 20px; text-align: center; border-radius: 12px; font-weight: 900; box-shadow: 0 6px 15px rgba(255, 75, 75, 0.4);">
                🔥 KALIBRASI ULANG SISTEM SARAF ANDA (PRIVATE SESSION)
            </div>
        </a>
        """, unsafe_allow_html=True)

else:
    st.info("Masukkan Nama dan Tanggal Lahir untuk meretas sandi takdir Anda.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<center><small>© 2026 Neuro Nada Ultimate | Crafted by Ahmad Septian</small></center>", unsafe_allow_html=True)
