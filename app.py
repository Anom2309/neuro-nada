import streamlit as st
import datetime
import os

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Peta Karakter, Weton & Zodiak", page_icon="✨", layout="centered")

# --- SIDEBAR PROMOSI ---
with st.sidebar:
    st.markdown("## 🌟 Layanan Eksklusif")
    st.info("**🧠 Sesi Private Hypnotherapy**\n\nLepaskan mental block bersama Ahmad Septian.")
    st.markdown("[👉 Booking Jadwal](https://lynk.id/username_lu/private-hypnotherapy)")
    st.markdown("---")
    st.success("**📚 E-Book: NLP Persuasi**\n\nKuasai teknik komunikasi bawah sadar.")
    st.markdown("[👉 Download Sekarang](https://lynk.id/username_lu/ebook-nlp)")

# --- TAMPILKAN BANNER ---
if os.path.exists("banner.jpg"):
    st.image("banner.jpg", use_container_width=True)

# --- FUNGSI LOGIKA ---
def hitung_angka(tanggal):
    tgl_str = tanggal.strftime("%d%m%Y")
    total = sum(int(digit) for digit in tgl_str)
    while total > 9: total = sum(int(digit) for digit in str(total))
    return total

def hitung_weton(tanggal):
    anchor_date = datetime.date(2000, 1, 1)
    selisih_hari = (tanggal - anchor_date).days
    hari_masehi = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_jawa = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"]
    return f"{hari_masehi[tanggal.weekday()]} {pasaran_jawa[selisih_hari % 5]}"

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

# --- INTERFACE UTAMA ---
st.title("✨ Peta Karakter Bawah Sadar")
st.write("Temukan potensi tersembunyi melalui perpaduan Numerologi, Weton, dan Zodiak.")

# BARIS NAMA (YANG HILANG)
nama_user = st.text_input("Siapa nama lengkapmu?", placeholder="Contoh: .....")

# INPUT TANGGAL
tgl_lahir = st.date_input("Kapan kamu lahir?", min_value=datetime.date(1920, 1, 1))

st.markdown("---")

# TOMBOL ANALISA DENGAN SISTEM "SATPAM"
if st.button("Analisa Karakter Saya Sekarang", type="primary"):
    if not nama_user:
        st.error("🚨 **Eits, tunggu dulu!** Silakan isi namamu dulu ya sebelum lanjut.")
    else:
        angka = hitung_angka(tgl_lahir)
        weton = hitung_weton(tgl_lahir)
        zodiak = hitung_zodiak(tgl_lahir)
        
        st.balloons()
        st.success(f"Halo **{nama_user}**, ini adalah hasil pembacaan awalmu:")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Angka Karakter", angka)
        c2.metric("Weton Jawa", weton)
        c3.metric("Zodiak", zodiak)
        
        st.info(f"Sebagai seorang **{zodiak}** dengan weton **{weton}**, kamu memiliki energi dasar yang sangat unik. Namun, ada satu titik buta psikologis yang sering menghambatmu...")
        
        st.markdown(f"### 🔓 Buka Rahasia Lengkapmu, {nama_user}!")
        st.link_button("👉 DOWNLOAD VIDEO ANALISA MENDALAM", f"https://lynk.id/username_lu/produk-{angka}", type="primary")

# --- TENTANG KREATOR ---
st.markdown("---")
st.write(f"Aplikasi ini dikembangkan oleh **Ahmad Septian Dwi Cahyo**, seorang Trainer NLP & Hipnoterapis.")
