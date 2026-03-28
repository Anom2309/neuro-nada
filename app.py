import streamlit as st
import datetime
import os

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Peta Karakter, Weton & Zodiak", page_icon="✨", layout="centered")

# --- SIDEBAR (MENU SAMPING BUAT PROMO) ---
with st.sidebar:
    st.markdown("## 🌟 Layanan Eksklusif")
    st.write("Tingkatkan potensi dirimu lebih jauh bersama kami.")
    st.markdown("---")
    
    # Promo 1: Private Hypnotherapy
    st.info("**🧠 Sesi Private Hypnotherapy**\n\nLepaskan mental block, trauma, atau kecemasan yang selama ini menahan potensimu. Sesi 1-on-1 eksklusif.")
    st.markdown("[👉 **Booking Jadwal Konsultasi**](https://lynk.id/username_lu/private-hypnotherapy)")
    
    st.markdown("---")
    
    # Promo 2: Kelas/E-book NLP
    st.success("**📚 E-Book: Rahasia Persuasi NLP**\n\nKuasai teknik komunikasi bawah sadar untuk karir, bisnis, dan hubungan yang lebih baik.")
    st.markdown("[👉 **Download Sekarang**](https://lynk.id/username_lu/ebook-nlp)")
    
    st.markdown("---")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo C.MH, C.PHT, C.T NNLP. All rights reserved.")

# --- MENAMPILKAN BANNER ESTETIK ---
if os.path.exists("banner.jpg"):
    st.image("banner.jpg", use_container_width=True)

# --- FUNGSI MENGHITUNG ANGKA KARAKTER ---
def hitung_angka(tanggal):
    tgl_str = tanggal.strftime("%d%m%Y")
    total = sum(int(digit) for digit in tgl_str)
    while total > 9:
        total = sum(int(digit) for digit in str(total))
    return total

# --- FUNGSI MENGHITUNG WETON JAWA ---
def hitung_weton(tanggal):
    anchor_date = datetime.date(2000, 1, 1)
    selisih_hari = (tanggal - anchor_date).days
    hari_masehi = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_jawa = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"]
    hari = hari_masehi[tanggal.weekday()]
    pasaran = pasaran_jawa[selisih_hari % 5]
    return f"{hari} {pasaran}"

# --- FUNGSI MENGHITUNG ZODIAK ---
def hitung_zodiak(tanggal):
    hari = tanggal.day
    bulan = tanggal.month
    
    if (bulan == 3 and hari >= 21) or (bulan == 4 and hari <= 19): return "Aries"
    elif (bulan == 4 and hari >= 20) or (bulan == 5 and hari <= 20): return "Taurus"
    elif (bulan == 5 and hari >= 21) or (bulan == 6 and hari <= 20): return "Gemini"
    elif (bulan == 6 and hari >= 21) or (bulan == 7 and hari <= 22): return "Cancer"
    elif (bulan == 7 and hari >= 23) or (bulan == 8 and hari <= 22): return "Leo"
    elif (bulan == 8 and hari >= 23) or (bulan == 9 and hari <= 22): return "Virgo"
    elif (bulan == 9 and hari >= 23) or (bulan == 10 and hari <= 22): return "Libra"
    elif (bulan == 10 and hari >= 23) or (bulan == 11 and hari <= 21): return "Scorpio"
    elif (bulan == 11 and hari >= 22) or (bulan == 12 and hari <= 21): return "Sagittarius"
    elif (bulan == 12 and hari >= 22) or (bulan == 1 and hari <= 19): return "Capricorn"
    elif (bulan == 1 and hari >= 20) or (bulan == 2 and hari <= 18): return "Aquarius"
    else: return "Pisces"

# --- DATABASE TEASER KARAKTER ---
teaser_angka = {
    1: "Kamu memiliki jiwa kepemimpinan alami dan kemandirian yang kuat.",
    2: "Kamu adalah sosok pembawa kedamaian yang punya empati luar biasa.",
    3: "Kreativitas dan kemampuan komunikasimu adalah senjata utamamu.",
    4: "Kamu sangat logis, terstruktur, dan bisa diandalkan dalam krisis.",
    5: "Kamu mencintai kebebasan, adaptif, dan selalu mencari pengalaman baru.",
    6: "Kamu punya insting mengayomi dan sangat peduli pada harmoni keluarga.",
    7: "Kamu pemikir yang dalam, analitis, dan sangat intuitif.",
    8: "Kamu punya ambisi besar, materialisasi kuat, dan bakat eksekutor.",
    9: "Kamu memiliki jiwa kemanusiaan yang tinggi dan visi yang luas."
}

# --- DATABASE LINK LYNK.ID ---
link_lynk_id = {
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

# --- HEADER APLIKASI ---
st.title("✨ Peta Karakter Bawah Sadar")
st.write("Temukan pola pikiran bawah sadar, energi kearifan lokal, dan rasi bintang yang tersembunyi di balik tanggal lahirmu.")
st.markdown("---")

# --- INPUT TANGGAL ---
st.write("Silakan masukkan tanggal lahirmu di bawah ini:")
tgl_lahir = st.date_input("", min_value=datetime.date(1920, 1, 1), max_value=datetime.date.today())

# --- TOMBOL ANALISA ---
if st.button("Analisa Karakter Saya Sekarang", type="primary"):
    angka_hasil = hitung_angka(tgl_lahir)
    weton_hasil = hitung_weton(tgl_lahir)
    zodiak_hasil = hitung_zodiak(tgl_lahir)
    
    st.markdown("### 🔍 Hasil Analisa Awal:")
    
    # Bikin 3 kolom biar rapi
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success(f"**Angka:** {angka_hasil}")
    with col2:
        st.info(f"**Weton:** {weton_hasil}")
    with col3:
        st.warning(f"**Zodiak:** {zodiak_hasil}")
    
    st.markdown("### Sekilas Tentang Polamu:")
    st.write(f"Secara psikologis, {teaser_angka.get(angka_hasil, '')} Namun, bagaimana energi dominan ini berinteraksi dengan karakter *{weton_hasil}* dan sifat dasar *{zodiak_hasil}* kamu?")
    
    # --- COPYWRITING CURIOSITY ---
    st.error(f"**Tunggu dulu...** Perpaduan antara Angka {angka_hasil}, Weton {weton_hasil}, dan Zodiak {zodiak_hasil} ini ternyata menyimpan **satu titik buta (blind spot)** psikologis. Ada sisi tersembunyi yang mungkin selama ini tanpa sadar sering menguras energimu, atau justru bisa menjadi kekuatan terbesarmu jika diaktifkan dengan benar.")
    
    # --- DISCLAIMER ---
    st.markdown("---")
    st.caption("📌 **Catatan Penting (Disclaimer):**\n\nAnalisa karakter ini merupakan pemetaan kecenderungan pola dasar manusia yang digabungkan dengan kearifan lokal dan astrologi. **Hasil ini tidak bersifat mutlak 100%**, karena manusia adalah makhluk dinamis yang terus berkembang. Ambil insight positifnya sebagai sugesti untuk memberdayakan dirimu.")
    
    # --- CALL TO ACTION (LYNK.ID) ---
    st.markdown("---")
    st.markdown("### 🔓 Buka Rahasia Penuh Potensimu!")
    st.write("Jangan biarkan potensi terbaikmu terkunci. Dapatkan analisa mendalam berupa **Video Eksklusif & Panduan Psikologis** yang dirancang spesifik untuk kombinasimu.")
    
    url_tujuan = link_lynk_id.get(angka_hasil)
    st.link_button("👉 KLIK DI SINI UNTUK DOWNLOAD HASIL LENGKAPNYA", url_tujuan, type="primary")

# --- PROFIL OTORITAS & FAQ ---
st.markdown("---")
st.markdown("### 👤 Tentang Kreator")
st.write("**Ahmad Septian Dwi Cahyo C.MH, C.PHT, C.T NNLP** adalah seorang Trainer Neuro-Linguistic Programming (NLP) dan Profesional Hipnoterapis yang mendedikasikan ilmunya untuk membantu setiap individu mengenali dan memaksimalkan potensi pikiran bawah sadar mereka, berpadu harmonis dengan kebijaksanaan lokal.")

# Kolom expander biar layar tetep bersih tapi isinya padat
with st.expander("Pertanyaan yang Sering Diajukan (FAQ)"):
    st.write("**Apakah analisa ini akurat?**")
    st.write("Analisa ini memetakan kecenderungan dasar dari ilmu numerologi, primbon, dan astrologi. Namun nasib dan karakter akhir tetap dipengaruhi oleh lingkungan dan kehendak bebas manusia.")
    st.write("**Bentuk file apa yang akan saya dapatkan?**")
    st.write("Kamu akan mendapatkan file Video Estetik lengkap dengan pembacaan psikologis yang mendalam untuk kombinasimu.")
