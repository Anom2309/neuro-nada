import streamlit as st
import datetime
import os
import time

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="NLP Deep Analysis | Ahmad Septian", 
    page_icon="🧠", 
    layout="centered"
)

# --- SIDEBAR PROMOSI ---
with st.sidebar:
    st.markdown("## 🧠 Sesi Transformasi")
    st.markdown("---")
    st.info("**Reset Pola Pikir Anda**\n\nSering merasa terhambat oleh pikiran sendiri? Mari kita lakukan kalibrasi ulang dalam sesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    st.markdown("[👉 **Amankan Jadwal Anda**](https://lynk.id/username_lu/private-hypnotherapy)")
    st.markdown("---")
    st.success("**📚 Seni Persuasi NLP**\n\nPelajari bagaimana bahasa bekerja di tingkat bawah sadar untuk meningkatkan pengaruh Anda.")
    st.markdown("[👉 **Akses Modul Lengkap**](https://lynk.id/username_lu/ebook-nlp)")
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
    elif (m == 12 and d >= 22) or (m == 13 and d <= 19): return "Capricorn"
    elif (m == 1 and d >= 20) or (m == 2 and d <= 18): return "Aquarius"
    else: return "Pisces"

# --- INTERFACE UTAMA ---
st.title("🧠 NLP Deep Analysis")
st.subheader("Membedah Struktur Pikiran & Potensi Diri")
st.write("Sinkronisasi data personal Anda untuk memetakan program bawah sadar dalam aspek Karakter dan Asmara.")
st.markdown("---")

nama_user = st.text_input("Siapa nama lengkap Anda?", placeholder="Masukkan nama panggilan Anda...")

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
if st.button("Mulai Pemetaan Internal", type="primary"):
    if not nama_user:
        st.error("🚨 **Peringatan:** Nama diperlukan untuk proses identifikasi pola.")
    elif tgl_input == tgl_today:
        st.error("🚨 **Peringatan:** Mohon masukkan tanggal lahir Anda yang valid.")
    else:
        with st.spinner('Melakukan kalibrasi pola pikiran Anda...'):
            time.sleep(2) 
            
            angka_hasil = hitung_angka(tgl_input)
            weton_hasil = hitung_weton(tgl_input)
            zodiak_hasil = hitung_zodiak(tgl_input)
        
        st.markdown(f"### 📋 Hasil Mapping: {nama_user}")
        st.divider()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("KODE PROGRAM", angka_hasil)
        c2.metric("ENERGI WETON", weton_hasil)
        c3.metric("POLA ZODIAK", zodiak_hasil)
        
        st.markdown("---")
        
        # --- HASIL 1: KARAKTER ---
        st.subheader("💡 Struktur Karakter & Mental")
        st.write(f"Halo **{nama_user}**, sistem mendeteksi bahwa filter utama pikiran Anda dipengaruhi oleh pola **{zodiak_hasil}** dengan pondasi energi **{weton_hasil}**.")
        st.info(f"Sebagai pemilik **Kode {angka_hasil}**, Anda memiliki spek berpikir yang tajam namun sering kali terhambat oleh 'program lama' yang tidak lagi relevan. Secara NLP, Anda membutuhkan proses *Reframing* agar hambatan mental yang sering muncul bisa berubah menjadi kekuatan pendorong kesuksesan.")

        # --- HASIL 2: PERCINTAAN ---
        st.subheader("❤️ Pola Hubungan & Asmara")
        st.write(f"Dalam dinamika hubungan, perpaduan **{zodiak_hasil}** dan **{weton_hasil}** membuat Anda memiliki cara unik dalam mengekspresikan kasih sayang.")
        st.warning(f"**Insight Asmara:** Kode **{angka_hasil}** menunjukkan bahwa Anda cenderung mencari kedalaman komunikasi. Belajar memahami sistem komunikasi pasangan akan membuat hubungan Anda jauh lebih harmonis.")

        # --- CTA ---
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
        
        st.markdown("---")
        st.markdown(f"#### 🔓 Ingin Memprogram Ulang Hidup Anda, {nama_user}?")
        st.link_button(f"👉 DOWNLOAD MODUL TRANSFORMASI (KODE {angka_hasil})", url_tujuan, type="primary")

        # --- BAGIAN FAQ (BARU) ---
        st.markdown("---")
        st.subheader("❓ Pertanyaan Sering Diajukan (FAQ)")
        
        with st.expander("Apakah ini sama dengan ramalan nasib?"):
            st.write("Bukan. Analisa ini menggunakan data personal sebagai 'pintu masuk' untuk memetakan pola pikiran bawah sadar Anda. NLP fokus pada bagaimana Anda mengolah informasi, bukan meramal masa depan.")
            
        with st.expander("Kenapa hasilnya bisa berbeda dengan zodiak/weton biasa?"):
            st.write("Karena Ahmad Septian menggabungkan ketiga variabel tersebut untuk melihat 'Meta-Program' yang lebih spesifik. Ini adalah analisa yang dipersonalisasi khusus untuk struktur mental Anda.")
            
        with st.expander("Bagaimana cara hasil ini membantu hidup saya?"):
            st.write("Dengan mengetahui 'Kode Program' Anda, Anda bisa lebih mudah mengenali kenapa Anda sering melakukan pola yang sama (misal: sering gagal di titik yang sama). Ini adalah langkah awal untuk melakukan Re-Programming.")

        # --- BAGIAN DISCLAIMER ---
        st.markdown("---")
        with st.expander("⚖️ Disclaimer & Batasan Layanan"):
            st.caption("""
            Analisa ini bertujuan sebagai alat edukasi dan refleksi diri, bukan diagnosis medis atau psikologis klinis.
            Ahmad Septian Dwi Cahyo tidak bertanggung jawab atas keputusan pribadi yang diambil pengguna berdasarkan hasil analisa ini.
            """)

# --- FOOTER ---
st.markdown("---")
st.write(f"**Ahmad Septian Dwi Cahyo** - Certified NLP Trainer & Professional Hypnotherapist.")
