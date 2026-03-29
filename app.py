import streamlit as st
import datetime
import os
import time
import urllib.parse

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="NLP Deep Analysis | Neuro Nada", 
    page_icon="🧠", 
    layout="centered"
)

# --- DATA ARKETIPE (NEW) ---
nama_arketipe = {
    1: "Sang Inisiator",
    2: "Sang Penjaga",
    3: "Sang Visioner",
    4: "Sang Alchemist",
    5: "Sang Eksekutor",
    6: "Sang Harmonizer",
    7: "Sang Legacy Builder",
    8: "Sang Sovereign",
    9: "Sang Ascended"
}

deskripsi_arketipe = {
    1: "Energi memulai, memimpin, dan menciptakan arah baru.",
    2: "Energi menjaga, menopang, dan membangun kestabilan.",
    3: "Energi intuisi, visi, dan pemahaman mendalam.",
    4: "Energi transformasi dan penyembuhan.",
    5: "Energi aksi dan eksekusi nyata.",
    6: "Energi keseimbangan dan hubungan.",
    7: "Energi pembangunan dan legacy.",
    8: "Energi kekuasaan dan kendali.",
    9: "Energi kesadaran dan pelepasan."
}

compatibility = {
    1: "Penjaga & Harmonizer",
    2: "Inisiator & Visioner",
    3: "Alchemist & Ascended",
    4: "Visioner & Harmonizer",
    5: "Inisiator & Sovereign",
    6: "Penjaga & Ascended",
    7: "Sovereign & Visioner",
    8: "Eksekutor & Legacy Builder",
    9: "Visioner & Harmonizer"
}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🧠 Sesi Transformasi")
    st.info("Reset pola pikir melalui sesi Private Hypno-NLP")

# --- FUNGSI ---
def hitung_angka(tanggal):
    tgl_str = tanggal.strftime("%d%m%Y")
    total = sum(int(d) for d in tgl_str)
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total

def hitung_zodiak(tanggal):
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

# --- UI ---
st.title("🧠 NLP Deep Analysis")

nama_user = st.text_input("Nama Anda")
tgl_input = st.date_input("Tanggal Lahir")

if st.button("Mulai Analisa"):

    angka_hasil = hitung_angka(tgl_input)
    zodiak = hitung_zodiak(tgl_input)

    arketipe = nama_arketipe.get(angka_hasil)

    # 🔥 HEADER HASIL
    st.markdown(f"# 🔮 {arketipe}")
    st.caption(deskripsi_arketipe.get(angka_hasil))

    # 🔥 GAMBAR ARKETIPE
    image_path = f"assets/arketipe_{angka_hasil}.png"
    if os.path.exists(image_path):
        st.image(image_path)

    # 🔥 INSIGHT EMOSIONAL
    st.success(f"""
    {nama_user}, pola hidup Anda sangat dipengaruhi oleh arketipe **{arketipe}**.

    Ini bisa menjadi kekuatan terbesar Anda...
    atau pola yang terus berulang tanpa Anda sadari.
    """)

    # 🔥 OPEN LOOP (IMPORTANT)
    st.warning(f"""
    ⚠️ Ada pola tersembunyi dalam arketipe Anda yang belum terbuka:

    - Blok rezeki bawah sadar
    - Pola sabotase diri
    - Siklus hubungan berulang

    👉 Ini hanya muncul di versi lanjutan
    """)

    # 🔥 ARKETIPE SEKUNDER
    angka_2 = sum(int(d) for d in str(tgl_input.day))
    while angka_2 > 9:
        angka_2 = sum(int(d) for d in str(angka_2))

    arketipe_2 = nama_arketipe.get(angka_2)

    st.markdown(f"""
    ### 🧬 Arketipe Sekunder: {arketipe_2}

    Ini mempengaruhi cara Anda:
    - bereaksi
    - mengambil keputusan
    """)

    # 🔥 COMPATIBILITY
    st.markdown(f"""
    ### ❤️ Kecocokan Anda:
    👉 {compatibility.get(angka_hasil)}
    """)

    # 🔥 CTA
    st.markdown("## 🔓 Buka Versi Lengkap")
    st.link_button("Akses Modul Transformasi", "https://lynk.id")

    # 🔥 SHARE
    hasil_text = f"Saya adalah {arketipe}"
    st.download_button("Download Hasil", hasil_text)
