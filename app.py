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

# --- DATABASE ANALISA SPESIFIK (NLP BASED) ---
data_analisa = {
    1: {
        "karakter": "Anda memiliki profil 'The Leader'. Meta-program Anda sangat proaktif dan berorientasi pada tujuan (Towards). Secara NLP, Anda sering menggunakan filter 'Self', yang membuat Anda mandiri namun kadang terlihat dominan.",
        "asmara": "Dalam asmara, Anda butuh pasangan yang menghargai independensi Anda. Hati-hati dengan pola komunikasi 'Command', cobalah lebih banyak menggunakan 'Request' agar pasangan merasa lebih nyaman."
    },
    2: {
        "karakter": "Anda adalah 'The Mediator'. Kekuatan utama Anda adalah 'Building Rapport' secara instan. Anda sangat sensitif terhadap harmoni lingkungan, namun seringkali mengabaikan kebutuhan diri sendiri (Filter: Others).",
        "asmara": "Asmara bagi Anda adalah tentang kedekatan emosional. Anda cenderung menghindari konflik, namun waspadai pola 'Pleasing' yang berlebihan. Komunikasikan batasan Anda dengan teknik Assertive Communication."
    },
    3: {
        "karakter": "Profil Anda adalah 'The Communicator'. Anda mahir dalam teknik 'Chunking Up' (melihat gambaran besar) dan menginspirasi orang lain. Pikiran Anda sangat visual dan cepat dalam memproses ide kreatif.",
        "asmara": "Hubungan yang ideal bagi Anda adalah yang penuh keceriaan dan stimulasi intelektual. Pasangan yang membosankan bisa memicu 'Internal Dialogue' negatif pada diri Anda. Cari partner yang bisa mengimbangi energi sosial Anda."
    },
    4: {
        "karakter": "Anda adalah 'The Architect'. Struktur berpikir Anda sangat detail dan prosedural. Secara NLP, Anda memiliki filter 'Internal Reference' yang kuat, sehingga Anda tidak mudah goyah oleh opini luar jika sudah punya data.",
        "asmara": "Dalam asmara, Anda butuh kepastian dan rencana jangka panjang. Spontanitas berlebihan dari pasangan bisa membuat sistem internal Anda 'Error'. Belajarlah sedikit lebih fleksibel dalam menerima perubahan rencana."
    },
    5: {
        "karakter": "Profil 'The Visionary/Explorer'. Anda adalah ahli dalam 'Reframing' situasi sulit menjadi peluang. Anda sangat fleksibel dan benci dengan batasan atau prosedur yang terlalu kaku.",
        "asmara": "Anda butuh ruang gerak (freedom). Hubungan yang mengekang akan membuat Anda merasa 'Suffocated'. Komunikasikan kebutuhan Anda akan petualangan baru agar pasangan tidak salah paham."
    },
    6: {
        "karakter": "Anda adalah 'The Nurturer'. Fokus utama pikiran Anda adalah pada 'Values' dan tanggung jawab keluarga. Anda memiliki kapasitas empati yang luar biasa besar melalui kalibrasi emosi yang tajam.",
        "asmara": "Asmara Anda berbasis pengabdian. Anda adalah pasangan yang sangat suportif. Namun, hindari pola 'Mind Reading' (menebak-nebak pikiran pasangan) yang bisa berujung pada rasa kecewa jika ekspektasi tidak terpenuhi."
    },
    7: {
        "karakter": "Profil 'The Analyst'. Anda adalah pemikir 'Deep Structure'. Anda tidak puas dengan informasi permukaan dan selalu mencari makna di balik segalanya. Intuisi Anda sangat kuat jika sudah terkalibrasi dengan baik.",
        "asmara": "Anda butuh waktu 'Me Time' yang cukup untuk memproses pikiran Anda. Pasangan yang terlalu menuntut perhatian setiap saat bisa membuat Anda mundur. Cari pasangan yang menghargai kedalaman intelektual Anda."
    },
    8: {
        "karakter": "Anda adalah 'The Strategist'. Orientasi Anda adalah pada 'Power' dan 'Outcome'. Anda sangat efisien dalam mengelola sumber daya dan memiliki kepercayaan diri yang solid dalam mengambil risiko.",
        "asmara": "Dalam hubungan, Anda cenderung menjadi pelindung dan penyedia. Namun, jangan bawa gaya 'Negotiation' bisnis ke dalam ranah asmara. Gunakan lebih banyak 'Soft Skills' dan sentuhan afeksi yang tulus."
    },
    9: {
        "karakter": "Profil 'The Humanist'. Anda memiliki 'State of Mind' yang inklusif dan bijaksana. Secara NLP, Anda cenderung memandang dunia secara 'Holistik' dan memiliki misi hidup yang melampaui kepentingan pribadi.",
        "asmara": "Anda mencari koneksi jiwa (Soulmate). Anda sangat pemaaf, namun waspadai pola 'Generalization' yang membuat Anda sering memaklumi kesalahan pasangan berulang kali. Tetaplah realistis dalam membangun hubungan."
    }
}

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
            
            # Ambil analisa spesifik dari database
            insight = data_analisa.get(angka_hasil)
        
        st.markdown(f"### 📋 Hasil Mapping: {nama_user}")
        st.divider()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("KODE PROGRAM", angka_hasil)
        c2.metric("ENERGI WETON", weton_hasil)
        c3.metric("POLA ZODIAK", zodiak_hasil)
        
        st.markdown("---")
        
        # --- HASIL 1: KARAKTER (SUDAH SPESIFIK) ---
        st.subheader("💡 Struktur Karakter & Mental")
        st.write(f"Halo **{nama_user}**, sistem mendeteksi filter utama pikiran Anda dipengaruhi pola **{zodiak_hasil}** dengan pondasi energi **{weton_hasil}**.")
        st.info(f"{insight['karakter']}")

        # --- HASIL 2: PERCINTAAN (SUDAH SPESIFIK) ---
        st.subheader("❤️ Pola Hubungan & Asmara")
        st.write(f"Dalam dinamika hubungan, perpaduan **{zodiak_hasil}** dan **{weton_hasil}** membuat Anda memiliki cara unik dalam mengekspresikan kasih sayang.")
        st.warning(f"**Insight Asmara:** {insight['asmara']}")

        # --- CTA ---
        link_produk = {
            1: "https://lynk.id/neuronada/kj98l4zgzwdw",
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

        # --- BAGIAN FAQ ---
        st.markdown("---")
        st.subheader("❓ Pertanyaan Sering Diajukan (FAQ)")
        
        with st.expander("Apakah ini sama dengan ramalan nasib?"):
            st.write("Bukan. Analisa ini menggunakan data personal sebagai 'pintu masuk' untuk memetakan pola pikiran bawah sadar Anda. NLP fokus pada bagaimana Anda mengolah informasi.")
            
        with st.expander("Kenapa hasilnya bisa berbeda dengan zodiak/weton biasa?"):
            st.write("Karena Ahmad Septian menggabungkan ketiga variabel tersebut untuk melihat 'Meta-Program' yang lebih spesifik.")

        # --- BAGIAN DISCLAIMER ---
        st.markdown("---")
        with st.expander("⚖️ Disclaimer & Batasan Layanan"):
            st.caption("Analisa ini bertujuan sebagai alat edukasi dan refleksi diri, bukan diagnosis medis.")

        # --- INTEGRASI WHATSAPP ---
        phone_number = "628999771486" 
        wa_text = (
            f"Halo Coach Ahmad, saya {nama_user}. Saya baru saja mencoba Persona-NLP Analis dengan hasil Kode {angka_hasil}. "
            "Ulasan karakter dan asmaranya sangat akurat! Saya tertarik untuk konsultasi lebih dalam. Boleh dibantu jadwalnya?"
        )
        encoded_wa = urllib.parse.quote(wa_text)
        wa_link = f"https://wa.me/{phone_number}?text={encoded_wa}"

        st.markdown(f"""
            <div style="text-align: center; margin-top: 30px; padding: 20px; background-color: #f0f2f6; border-radius: 15px;">
                <h4 style="color: #1f1f1f; margin-bottom: 15px;">Butuh Kalibrasi Pikiran Lebih Dalam?</h4>
                <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                    <button style="
                        width: 100%;
                        background-color: #25D366;
                        color: white;
                        padding: 16px;
                        border: none;
                        border-radius: 12px;
                        font-weight: bold;
                        cursor: pointer;
                        font-size: 18px;
                        box-shadow: 0px 4px 12px rgba(37, 211, 102, 0.3);">
                        💬 Maksimalkan Potensi NLP Saya
                    </button>
                </a>
                <p style="font-size: 13px; color: #666; margin-top: 12px;">
                    Konsultasi langsung dengan Coach Ahmad Septian
                </p>
            </div>
            """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.write(f"**Ahmad Septian Dwi Cahyo** - Certified NLP Trainer & Professional Hypnotherapist.")
