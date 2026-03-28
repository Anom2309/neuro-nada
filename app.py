import streamlit as st
import datetime
import os
import time

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Peta Karakter Bawah Sadar", page_icon="✨", layout="centered")

# --- SIDEBAR PROMOSI ---
with st.sidebar:
    st.markdown("## 🌟 Layanan Eksklusif")
    st.markdown("---")
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
st.write("Analisa pola pikiran melalui perpaduan Numerologi, Weton, dan Zodiak.")
st.markdown("---")

nama_user = st.text_input("Siapa nama lengkapmu?", placeholder="Ketik namamu di sini...")

tgl_today = datetime.date.today()
tgl_input = st.date_input(
    "Pilih Tanggal Lahirmu:",
    value=tgl_today,
    min_value=datetime.date(1920, 1, 1),
    max_value=tgl_today,
    format="DD/MM/YYYY"
)

st.markdown("---")

# --- PROSES ANALISA ---
if st.button("Mulai Analisa Mendalam", type="primary"):
    if not nama_user:
        st.error("🚨 **Akses Ditolak:** Nama Lengkap tidak boleh kosong!")
    elif tgl_input == tgl_today:
        st.error("🚨 **Akses Ditolak:** Silakan pilih Tanggal Lahir Anda yang benar.")
    else:
        # Efek Loading Elegan
        with st.spinner('Menghubungkan pola bawah sadar...'):
            time.sleep(2) 
            
            # Hitung Hasil
            angka_hasil = hitung_angka(tgl_input)
            weton_hasil = hitung_weton(tgl_input)
            zodiak_hasil = hitung_zodiak(tgl_input)
        
        # Tampilan Hasil
        st.markdown(f"### 🖋️ Laporan Analisa: {nama_user}")
        st.divider()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Angka Dominan", angka_hasil)
        c2.metric("Energi Weton", weton_hasil)
        c3.metric("Rasi Bintang", zodiak_hasil)
        
        st.markdown("---")
        
        st.write(f"Berdasarkan pola frekuensi Anda, perpaduan antara **{zodiak_hasil}** dan **{weton_hasil}** menciptakan struktur kepribadian yang unik. Sebagai pemilik **Angka Karakter {angka_hasil}**, Anda memiliki potensi besar yang sering kali terhambat oleh hambatan mental yang tidak disadari.")
        
        # Call to Action Dinamis (PASTI SESUAI ANGKA)
        st.info(f"**Insight untuk {nama_user}:** Titik balik kesuksesan Anda ada pada pemahaman 'Blind Spot' psikologis Anda sendiri.")
        
        # LOGIKA LINK DINAMIS (Ganti link di bawah ini sesuai link produk Lynk.id lu)
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
        
        st.markdown(f"### 🔓 Buka Rahasia Penuh Potensimu, {nama_user}!")
        st.link_button(f"👉 DOWNLOAD ANALISA LENGKAP ANGKA {angka_hasil}", url_tujuan, type="primary")

# --- FOOTER ---
st.markdown("---")
st.write(f"Dikembangkan secara profesional oleh **Ahmad Septian Dwi Cahyo**.")
