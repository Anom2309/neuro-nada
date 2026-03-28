import streamlit as st
import datetime
import os

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Peta Karakter Bawah Sadar", page_icon="✨", layout="centered")

# --- SIDEBAR PROMOSI (KALIMAT BARU LEBIH MAUT) ---
with st.sidebar:
    st.markdown("## 🌟 Layanan Eksklusif")
    st.markdown("---")
    
    # Versi yang paling 'Punchy' dan NLP banget
    st.info("**🧠 Break Your Limits!**\n\nJangan biarkan pikiranmu sendiri jadi penjara. Bebaskan potensi terbaikmu melalui sesi *Private Hypnotherapy* eksklusif bersama **Ahmad Septian**.")
    st.markdown("[👉 **Booking Jadwal Konsultasi**](https://lynk.id/username_lu/private-hypnotherapy)")
    
    st.markdown("---")
    
    st.success("**📚 E-Book: NLP Persuasi**\n\nKuasai teknik komunikasi bawah sadar untuk karir dan hubungan.")
    st.markdown("[👉 **Download Sekarang**](https://lynk.id/username_lu/ebook-nlp)")
    
    st.markdown("---")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

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

st.markdown("---")

# 1. INPUT NAMA
nama_user = st.text_input("Siapa nama lengkapmu?", placeholder="Ketik namamu di sini...")

# 2. INPUT TANGGAL (Default ke hari ini biar gak error, tapi ada satpam)
tgl_today = datetime.date.today()
tgl_input = st.date_input(
    "Pilih Tanggal Lahirmu:",
    value=tgl_today,
    min_value=datetime.date(1920, 1, 1),
    max_value=tgl_today,
    format="DD/MM/YYYY"
)

st.markdown("---")

# 3. TOMBOL ANALISA + SATPAM KETAT
if st.button("Analisa Karakter Saya Sekarang", type="primary"):
    if not nama_user:
        st.error("🚨 **Akses Ditolak:** Nama Lengkap tidak boleh kosong!")
    elif tgl_input == tgl_today:
        st.error("🚨 **Akses Ditolak:** Silakan pilih Tanggal Lahir Anda yang benar (jangan biarkan tanggal hari ini).")
    else:
        # Menghitung Hasil
        angka_hasil = hitung_angka(tgl_input)
        weton_hasil = hitung_weton(tgl_input)
        zodiak_hasil = hitung_zodiak(tgl_input)
        
        st.balloons()
        st.success(f"Halo **{nama_user}**, Analisa Karaktermu telah siap!")
        
        # Tampilan Hasil (Metric)
        c1, c2, c3 = st.columns(3)
        c1.metric("Angka Karakter", angka_hasil)
        c2.metric("Weton Jawa", weton_hasil)
        c3.metric("Zodiak", zodiak_hasil)
        
        st.markdown("---")
        st.info(f"Kombinasi energi **{zodiak_hasil}** dan weton **{weton_hasil}** menunjukkan pola pikiran bawah sadar yang unik. Sebagai pemilik **Angka Karakter {angka_hasil}**, ada rahasia mental yang perlu Anda ketahui.")
        
        # Call to Action
        st.markdown(f"### 🔓 Buka Rahasia Penuh Potensimu, {nama_user}!")
        url_lynk = f"https://lynk.id/username_lu/produk-{angka_hasil}"
        st.link_button("👉 KLIK UNTUK DOWNLOAD ANALISA LENGKAP", url_lynk, type="primary")

# --- PROFIL KREATOR ---
st.markdown("---")
st.markdown("### 👤 Tentang Kreator")
st.write("**Ahmad Septian Dwi Cahyo C.MH, C.PHt, C.T NNLP** adalah seorang Trainer NLP & Profesional Hipnoterapis yang membantu Anda memaksimalkan potensi pikiran bawah sadar.")
