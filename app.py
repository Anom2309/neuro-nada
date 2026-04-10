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
    page_title="Neuro Nada Deep Analysis", 
    page_icon="🌌", 
    layout="centered", # Tetap centered agar fokus, namun konten di dalamnya "Mahal"
    initial_sidebar_state="collapsed" 
)

# --- CUSTOM CSS (LUXURY DARK GOLD) ---
st.markdown(
    """<style>
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; background-color: #0a0a0a; }
    
    /* Button Style */
    div.stButton > button {
        background: linear-gradient(90deg, #FFD700 0%, #B8860B 100%) !important;
        color: #000000 !important; font-weight: 800 !important;
        border: none !important; padding: 12px 24px !important;
        border-radius: 8px !important; width: 100% !important;
        font-size: 16px !important; transition: 0.3s;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3);
    }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255,215,0,0.5); }
    
    /* Box & Container Style */
    .cosmic-box {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a4a 100%);
        padding: 20px; border-radius: 12px; border: 1px solid #4a4a8a;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6); margin-bottom: 15px;
    }
    
    .primbon-box {
        background: linear-gradient(135deg, #2b1b05 0%, #4a3000 100%);
        padding: 20px; border-radius: 15px; border: 1px solid #D4AF37;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin: 20px 0;
    }
    
    .matrix-container {
        display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap;
        padding: 15px; background-color: #101010; border-radius: 10px;
        border: 1px solid #333; margin-bottom: 20px;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
    }
    .matrix-item { flex: 1; min-width: 80px; text-align: center; padding: 5px; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    .matrix-value { font-size: 16px; font-weight: 900; color: white; }
    .matrix-value-special { color: #FFD700; }

    .cta-button {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff0000 100%);
        color: white !important; padding: 15px; text-align: center; 
        border-radius: 8px; font-weight: 900; font-size: 16px; 
        text-transform: uppercase; letter-spacing: 1px;
    }
    </style>""", unsafe_allow_html=True
)

# --- ENGINE: LIVE PLANETARY CLOCK ---
def get_planetary_hour():
    planets = ["Matahari (Otoritas)", "Venus (Asmara/Uang)", "Merkurius (Komunikasi)", "Bulan (Intuisi)", "Saturnus (Disiplin/Karma)", "Yupiter (Ekspansi)", "Mars (Aksi)"]
    now = datetime.datetime.now()
    index = now.hour % 7
    return planets[index]

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa Kosmik"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

# --- CORE LOGIC: GEMATRIA & BETALJEMUR ---
def hitung_nama_esoterik(nama):
    abjad_values = {'a':1, 'b':2, 'j':3, 'd':4, 'h':5, 'w':6, 'z':7, 't':9, 'y':10, 'k':20, 'l':30, 'm':40, 'n':50, 's':60, 'f':80, 'q':100, 'r':200, 'g':1000, 'i':10}
    nama_clean = ''.join(filter(str.isalpha, nama.lower()))
    return sum(abjad_values.get(huruf, 0) for huruf in nama_clean) if nama_clean else 1

def get_betaljemur_engine(tanggal):
    anchor = datetime.date(1900, 1, 1) # FLEKSIBEL SEJAK 1900
    diff = (tanggal - anchor).days
    hari_n = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_n = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"]
    h_idx = tanggal.weekday()
    p_idx = diff % 5
    n_hari = [4, 3, 7, 8, 6, 9, 5]
    n_pas = [9, 7, 4, 8, 5]
    neptu = n_hari[h_idx] + n_pas[p_idx]
    
    lakuning = {
        7: ("Lebu Katiup Angin", "Pikiran dinamis, mudah goyah, butuh anchoring kuat."),
        8: ("Lakuning Geni", "Emosi meledak-ledak. Punya daya dobrak tinggi."),
        9: ("Lakuning Angin", "Gampang dipengaruhi sugesti, sangat adaptif."),
        10: ("Pandito Mbangun Teki", "Introspektif, pola pikir deep structure."),
        11: ("Macan Ketawan", "Aura pemimpin tajam, benci dikontrol."),
        12: ("Lakuning Kembang", "Menebar pesona, rapport natural sangat mudah."),
        13: ("Lakuning Lintang", "Kharisma misterius, kuat dalam kesendirian."),
        14: ("Lakuning Rembulan", "Penenang batin, jangkar emosi bagi orang lain."),
        15: ("Lakuning Srengenge", "Pencerah, sangat logis, berwibawa tinggi."),
        16: ("Lakuning Banyu", "Tenang tapi menghanyutkan, keras jika dilanggar."),
        17: ("Lakuning Bumi", "Sangat sabar, membumi, pengayom sejati."),
        18: ("Paripurna", "Kekuatan utuh, otoritas bijak tingkat tinggi.")
    }
    # NAGA DINA (Arah Kejayaan)
    naga = ["TIMUR", "SELATAN", "BARAT", "UTARA", "TIMUR", "SELATAN", "SELATAN"][h_idx]
    
    return neptu, f"{hari_n[h_idx]} {pasaran_n[p_idx]}", lakuning.get(neptu, ("Unik", "Kompleks")), naga

# --- UI INTERFACE ---
st.markdown(f"<div style='text-align:right;'><span style='background:#D4AF37; color:black; padding:5px 10px; border-radius:20px; font-size:10px; font-weight:900;'>LIVE NOW: {get_planetary_hour().upper()}</span></div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; font-weight: 900;'>🌌 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #D4AF37;'>Meretas Realita Melalui Kode Sandi Alam Bawah Sadar</p>", unsafe_allow_html=True)

# TAB 1: IDENTITAS KOSMIK
tab1, tab2, tab3 = st.tabs(["👤 Identitas Kosmik", "👩‍❤️‍👨 Couple Sync", "🕸️ Audit Saraf"])

with tab1:
    nama_user = st.text_input("Nama Lengkap:", placeholder="Ketik nama asli Anda...")
    # TAHUN FLEKSIBEL SEJAK 1900
    tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date(1995, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())

    if st.button("MULAI DEEP SCAN"):
        if nama_user:
            val_jum = hitung_nama_esoterik(nama_user)
            nep, weton, laku, arah = get_betaljemur_engine(tgl_input)
            
            # THE MATRIX METRICS
            st.markdown(f"""
            <div class="matrix-container">
                <div class="matrix-item"><div class="matrix-label">Nilai Esoterik</div><div class="matrix-value matrix-value-special">{val_jum}</div></div>
                <div class="matrix-item"><div class="matrix-label">Weton</div><div class="matrix-value">{weton}</div></div>
                <div class="matrix-item"><div class="matrix-label">Neptu</div><div class="matrix-value">{nep}</div></div>
                <div class="matrix-item"><div class="matrix-label">Momentum</div><div class="matrix-value-special" style="font-size:10px;">{get_planetary_hour().split()[0]}</div></div>
            </div>
            """, unsafe_allow_html=True)
            
            # BETALJEMUR BOX (ACTIONABLE INTELLIGENCE)
            st.markdown(f"""
            <div class="primbon-box">
                <div style="text-align:center; border-bottom:1px solid #D4AF37; padding-bottom:10px; margin-bottom:15px;">
                    <span style="color:#D4AF37; font-size:12px; font-weight:900; letter-spacing:2px;">📜 ANALISIS BETALJEMUR & NLP</span>
                </div>
                <div style="margin-bottom: 15px;">
                    <span style="color:#aaa; font-size:12px;">Sandi Pangarasan (Meta-Program):</span><br>
                    <b style="color:#FFF; font-size:18px;">{laku[0]}</b><br>
                    <i style="color:#ccc;">"{laku[1]}"</i>
                </div>
                <div style="background: rgba(255,215,0,0.1); padding: 10px; border-radius: 8px;">
                    <span style="color:#FFD700; font-weight:900;">🧭 ARAH KEJAYAAN: {arah}</span><br>
                    <span style="color:#888; font-size:11px;">Gunakan arah {arah} saat negosiasi atau bekerja untuk sinkronisasi vibrasi bumi.</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success(f"Analisis Selesai! Nama Anda bergetar pada frekuensi **{val_jum}**. Saat ini jam **{get_planetary_hour()}** sedang aktif, ini adalah waktu yang tepat untuk tindakan strategis.")

# (Tab 2 dan 3 bisa lo isi dengan logika Couple Sync & Audit Saraf yang sama, tinggal sesuaikan UI-nya dengan style box di atas)

st.markdown("---")
st.markdown("<center><b>Ahmad Septian Dwi Cahyo</b><br><small>Certified NLP Trainer & Professional Hypnotherapist © 2026</small></center>", unsafe_allow_html=True)
