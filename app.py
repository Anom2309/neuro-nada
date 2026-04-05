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

# --- SALAM DINAMIS ---
def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa yang Luar Biasa"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

# ==========================================
# DATABASE CLOUD: GOOGLE SHEETS
# ==========================================
URL_POST = "https://script.google.com/macros/s/AKfycbwkOL8-E50RKM5BRR8puh_XbfL-K_hQj5cnv0un6UzmFmMBEG6HZZ4aEQmFZj5EMsSBUQ/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2H-IH_8TbdbMRtvZnvza-InIO-Xl-B9YzLYtWtSb8vpUVuM1uZ4FTi6JwOtk2esj7hilwgGCoWex4/pub?output=csv"

@st.cache_data(ttl=30)
def ambil_ulasan():
    try:
        req = urllib.request.Request(URL_CSV)
        with urllib.request.urlopen(req) as response:
            decoded = response.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            data = [row for row in reader]
            return data[::-1]
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
st.markdown("""<style>
div.stButton > button {
    background-color: #FFD700 !important;
    color: #000000 !important;
    font-weight: bold !important;
    border: none !important;
    padding: 12px 24px !important;
    border-radius: 50px !important;
    width: 100% !important;
}
</style>""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"### {get_greeting()}")

# --- HEADER ---
st.markdown("<h1 style='text-align: center;'>🧠 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)

# ==========================================
# 🎧 PEMUTAR MUSIK RELAKSASI (FIX FINAL)
# ==========================================
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #D4AF37;'>🎧 Soundscape Terapi</h4>", unsafe_allow_html=True)
st.caption("Tekan Play untuk memulai frekuensi relaksasi.")

# STATE
if "music_playing" not in st.session_state:
    st.session_state.music_playing = False

# BUTTON
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Play"):
        st.session_state.music_playing = True

with col2:
    if st.button("⏹️ Stop"):
        st.session_state.music_playing = False

# AUDIO
if os.path.exists("relaksasi.mp3"):
    if st.session_state.music_playing:
        st.audio("relaksasi.mp3", format="audio/mp3")
else:
    st.warning("⚠️ File relaksasi.mp3 belum ada")

st.markdown("---")

# ==========================================
# CONTINUE CODE (TIDAK DIUBAH)
# ==========================================
st.write("Sisa aplikasi tetap berjalan normal...")
