import streamlit as st
import datetime
import os

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Peta Karakter Bawah Sadar", page_icon="✨", layout="centered")

# --- SIDEBAR PROMOSI ---
with st.sidebar:
    st.markdown("## 🌟 Layanan Eksklusif")
    st.info("**🧠 Sesi Private Hypnotherapy**\n\nLepaskan mental block bersama Ahmad Septian.")
    st.markdown("[👉 Booking Jadwal](https://lynk.id/username_lu/private-hypnotherapy)")
    st.markdown("---")
    st.success("**📚 E-Book: NLP Persuasi**\n\nKuasai teknik komunikasi bawah sadar.")
    st.markdown("[👉 Download Sekarang](https://lynk.id/username_lu/ebook-nlp)")
    st.markdown("---")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

# --- TAMPILKAN BANNER ---
if os.path.exists("banner.jpg"):
    st.image("banner.jpg", use_container_width=True)

# --- FUNGSI LOGIKA PERHITUNGAN ---
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

st.markdown("---")

# 1. KOLOM NAMA (MANUAL)
nama_user = st.text_input("Siapa nama lengkapmu?", placeholder="Ketik namamu di sini...")

# 2. KOLOM TANGGAL LAHIR (KOSONG DI AWAL)
tgl_input = st.date_input(
    "Kapan kamu lahir?",
    value=None, # Membuat kolom kosong/manual
    min_value=datetime.date(1920, 1, 1),
    max_value=datetime.date.today(),
    format="DD/MM/YYYY",
    placeholder="Pilih tanggal lahirmu"
)

st.markdown("---")

# 3. TOMBOL ANALISA DENGAN LOGIKA PENOLAKAN (SATPAM)
if st.button("Analisa Karakter Saya Sekarang", type="primary"):
    # VALIDASI KETAT
    if not nama_user or tgl_input is None:
        st.error("🚨 **Akses Ditolak:** Mohon isi Nama Lengkap dan Pilih Tanggal Lahirmu terlebih dahulu untuk melanjutkan analisa.")
    else:
        # Menghitung Hasil
        angka = hitung_angka(tgl_input)
        weton = hitung_weton(tgl_input)
        zodiak = hitung_zodiak(tgl_input)
        
        # Efek Visual Berhasil
        st.balloons()
        st.success(f"Halo **{nama_user}**, Analisa Karaktermu telah siap!")
        
        # Menampilkan Hasil (Metric)
        col1, col2, col3 = st.columns(3)
        col1.metric("Angka Karakter", angka)
        col2.metric("Weton Jawa", weton)
        col3.metric("Zodiak", zodiak)
        
        st.markdown("---")
        
        # Copywriting Curiosity NLP
        st.info(f"Kombinasi energi **{zodiak}** dan weton **{weton}** menunjukkan pola pikiran bawah sadar yang sangat spesifik. Namun, sebagai pemilik **Angka Karakter {angka}**, ada 'Mental Block' tersembunyi yang mungkin selama ini menghambat potensi terbaikmu.")
        
        # Call to Action (Ganti 'username_lu' dengan link aslimu)
        st.markdown(f"### 🔓 Buka Rahasia Penuh Potensimu, {nama_user}!")
        url_tujuan = f"https://lynk.id/username_lu/produk-{angka}"
        st.link_button("👉 KLIK DI SINI UNTUK DOWNLOAD ANALISA LENGKAP", url_tujuan, type="primary")

# --- PROFIL KREATOR ---
st.markdown("---")
st.markdown("### 👤 Tentang Kreator")
st.write("**Ahmad Septian Dwi Cahyo** adalah seorang Trainer NLP & Profesional Hipnoterapis yang mendedikasikan ilmunya untuk membantu Anda mengenali potensi pikiran bawah sadar.")
