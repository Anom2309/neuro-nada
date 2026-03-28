import streamlit as st
import datetime
import os
import time

# --- PENGATURAN HALAMAN (Tab Browser) ---
st.set_page_config(
    page_title="NLP Deep Analysis | Ahmad Septian", 
    page_icon="🧠", 
    layout="centered"
)

# --- SIDEBAR PROMOSI ---
with st.sidebar:
    st.markdown("## 🧠 Layanan NLP Eksklusif")
    st.markdown("---")
    st.info("**Update Program Pikiranmu!**\n\nSering merasa 'mentok' atau sulit maju? Itu tanda ada program lama yang perlu di-Update. Beresin bareng **Ahmad Septian** lewat sesi *Private Hypno-NLP*.")
    st.markdown("[👉 **Atur Jadwal Re-Programming**](https://lynk.id/username_lu/private-hypnotherapy)")
    st.markdown("---")
    st.success("**📚 Ilmu Persuasi NLP**\n\nBongkar rahasia cara kerja otak agar omonganmu lebih didengar dan meyakinkan orang lain.")
    st.markdown("[👉 **Ambil Modul NLP**](https://lynk.id/username_lu/ebook-nlp)")
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

# --- INTERFACE UTAMA (Halaman Web) ---
st.title("🧠 NLP Deep Analysis")
st.subheader("Mapping Your Internal Program")
st.write("Identifikasi pola pikiran bawah sadar melalui sinkronisasi Numerologi, Weton, dan Zodiak.")
st.markdown("---")

nama_user = st.text_input("Siapa nama panggilan Anda?", placeholder="Input Nama...")

tgl_today = datetime.date.today()
tgl_input = st.date_input(
    "Data Input (Tanggal Lahir):",
    value=tgl_today,
    min_value=datetime.date(1920, 1, 1),
    max_value=tgl_today,
    format="DD/MM/YYYY"
)

st.markdown("---")

# --- PROSES ANALISA ---
if st.button("Mulai Pemetaan NLP", type="primary"):
    if not nama_user:
        st.error("🚨 **Maaf:** Nama diperlukan untuk kalibrasi data.")
    elif tgl_input == tgl_today:
        st.error("🚨 **Maaf:** Silakan pilih tanggal lahir Anda yang benar.")
    else:
        with st.spinner('Menganalisa struktur program pikiran Anda...'):
            time.sleep(2) 
            
            angka_hasil = hitung_angka(tgl_input)
            weton_hasil = hitung_weton(tgl_input)
            zodiak_hasil = hitung_zodiak(tgl_input)
        
        st.markdown(f"### 📋 Mapping Result: {nama_user}")
        st.divider()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("KODE PROGRAM", angka_hasil)
        c2.metric("VAR WETON", weton_hasil)
        c3.metric("VAR ZODIAK", zodiak_hasil)
        
        st.markdown("---")
        
        st.write(f"Halo **{nama_user}**, sistem mendeteksi bahwa filter pikiran Anda dipengaruhi oleh pola **{zodiak_hasil}** dan **{weton_hasil}**.")
        
        st.info(f"**Analisa NLP:**\n\nSebagai pemilik **Kode Program {angka_hasil}**, struktur pikiran Anda punya potensi luar biasa. Namun dalam istilah NLP, ada *Mental Block* (hambatan mental) yang sering membuat Anda merasa 'jalan di tempat'. Anda butuh teknik *Reframing* (mengubah sudut pandang) agar potensi asli Anda bisa keluar.")
        
        link_produk = {
            1: "https://lynk.id/username_lu/produk-angka-1",
            2: "https://lynk.id/username_lu/produk-angka-2",
            3: "https://lynk.id/username_lu/produk-angka-3",
            4: "https://lynk.id/username_lu/produk-angka-4",
            5: "https://lynk.id/username_lu/produk-angka-5",
            6: "https://lynk.id/username_lu/produk-angka-6",
            7: "https://lynk.id/username_lu/produk-angka-7",
            8: "https://lynk.id/username_lu/produk-angka-8",
            9: "https://lynk.id/username_lu/produk-angka-9"
        }
        
        url_tujuan = link_produk.get(angka_hasil, "https://lynk.id/username_lu")
        
        st.markdown(f"#### 🔓 Lakukan Re-Programming Sekarang!")
        st.write(f"Khusus untuk pemilik Kode {angka_hasil}, temukan cara menghapus hambatan mental Anda dengan teknik NLP yang praktis.")
        
        st.link_button(f"👉 DOWNLOAD PANDUAN RE-PROGRAMMING (KODE {angka_hasil})", url_tujuan, type="primary")

# --- FOOTER ---
st.markdown("---")
st.write(f"Developed by **Ahmad Septian Dwi Cahyo** - Certified NLP Trainer & Hypnotherapist.")
