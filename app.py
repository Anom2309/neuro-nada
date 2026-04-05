import streamlit as st
import datetime
import os
import time
import urllib.parse
import math
import plotly.graph_objects as go
import random

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

# --- INIT SESSION STATE UNTUK ULASAN REAL-TIME ---
if 'daftar_ulasan' not in st.session_state:
    st.session_state.daftar_ulasan = [
        {"nama": "dr. Antonius", "rating": "⭐⭐⭐⭐⭐", "teks": "Ini bukan cuma ramalan, ini pemetaan otak yang masuk akal. Investasi terbaik tahun ini!"},
        {"nama": "Andi S. (CEO)", "rating": "⭐⭐⭐⭐⭐", "teks": "Sebagai tipe 8, saya kaget NLP ini bisa baca pola leadership saya. Mind-blowing!"},
        {"nama": "Sinta W.", "rating": "⭐⭐⭐⭐", "teks": "Sangat relate dengan pola asmara 'Gak Enakan'. Makasih Coach!"}
    ]

# --- CUSTOM CSS ---
st.markdown(
    """<style>
    div.stButton > button {
        background-color: #FFD700 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 50px !important;
        width: 100% !important;
        font-size: 16px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        background-color: #FFC107 !important;
    }
    .ulasan-box {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #FFD700;
        margin-bottom: 10px;
    }
    </style>""", 
    unsafe_allow_html=True
)

# --- SIDEBAR PROMOSI & VIDEO ---
with st.sidebar:
    if os.path.exists("baru.jpg.png"):
        st.image("baru.jpg.png", use_container_width=True)
    elif os.path.exists("baru.jpg"):
        st.image("baru.jpg", use_container_width=True)

    st.markdown(f"### {get_greeting()}")
    
    st.markdown("### 🎬 Hypno-Video Vault")
    st.video("https://youtu.be/kkRcH6aH_lI?si=bpUZF3CWl8DKLw5m")
    
    st.markdown("---")
    st.markdown("## 🧠 Sesi Transformasi")
    st.info("**Reset Pola Pikir Anda**\n\nSering merasa terhambat? Mari kita lakukan kalibrasi ulang dalam sesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    
    phone_number_sidebar = "628999771486"
    wa_link_sidebar = f"https://wa.me/{phone_number_sidebar}?text=Halo%20Coach%20Ahmad,%20saya%20siap%20untuk%20sesi%20Transformasi%20Pikiran."
    st.markdown(f"[👉 **Amankan Jadwal Anda**]({wa_link_sidebar})")
    
    st.markdown("---")
    st.success("**📚 Seni Persuasi NLP**\n\nPelajari bagaimana bahasa bekerja di tingkat bawah sadar.")
    st.markdown("[👉 **Akses Modul Lengkap**](https://lynk.id/username_lu/ebook-nlp)")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

# --- INTERFACE UTAMA & BANNER ---
if os.path.exists("banner.jpg"):
    st.image("banner.jpg", use_container_width=True)

st.markdown("<h1 style='text-align: center; margin-top: 10px;'>🧠 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 18px; color: #D4AF37;'>{get_greeting()}</p>", unsafe_allow_html=True)

# --- PEMUTAR MUSIK RELAKSASI DI TENGAH LAYAR ---
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #D4AF37;'>🎧 Soundscape Terapi</h4>", unsafe_allow_html=True)
st.caption("<div style='text-align: center; margin-bottom:10px;'>Putar audio ini untuk menurunkan gelombang otak ke fase relaksasi (Alpha/Theta) sebelum mulai analisa.</div>", unsafe_allow_html=True)

# Menggunakan link MP3 Publik yang 100% stabil di semua perangkat
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
st.markdown("---")

# --- DATABASE ANALISA & POTENSI ---
vibrasi_nama_dict = {
    1: "Nama Anda memancarkan getaran KEMANDIRIAN & KEPEMIMPINAN.",
    2: "Nama Anda memancarkan getaran DIPLOMASI & KEDAMAIAN.",
    3: "Nama Anda memancarkan getaran EKSPRESI & KECERIAAN.",
    4: "Nama Anda memancarkan getaran STRUKTUR & KEDISIPLINAN.",
    5: "Nama Anda memancarkan getaran KEBEBASAN & DINAMIKA.",
    6: "Nama Anda memancarkan getaran TANGGUNG JAWAB & KASIH SAYANG.",
    7: "Nama Anda memancarkan getaran KEDALAMAN & ANALISA.",
    8: "Nama Anda memancarkan getaran OTORITAS & KESUKSESAN.",
    9: "Nama Anda memancarkan getaran KEMANUSIAAN & IDEALISME."
}

data_analisa = {
    1: {"karakter": "Anda memiliki profil 'The Leader (Sang Inisiator / Perintis)'. Meta-program Anda sangat proaktif dan berorientasi pada tujuan (Towards). Secara NLP, Anda sering menggunakan filter 'Self', yang membuat Anda mandiri namun kadang terlihat dominan.", "asmara": "Anda butuh pasangan yang menghargai independensi Anda. Hati-hati dengan pola komunikasi 'Command', cobalah lebih banyak menggunakan 'Request'."},
    2: {"karakter": "Anda adalah 'The Mediator (Sang Penjaga / Penyelaras)'. Kekuatan utama Anda adalah 'Building Rapport' secara instan. Anda sangat sensitif terhadap harmoni lingkungan.", "asmara": "Asmara bagi Anda adalah tentang kedekatan emosional. Waspadai pola 'Pleasing' yang berlebihan."},
    3: {"karakter": "Profil Anda adalah 'The Communicator (Sang Visioner / Ekspresif)'. Anda mahir dalam teknik 'Chunking Up' (melihat gambaran besar). Pikiran Anda sangat visual.", "asmara": "Hubungan yang ideal bagi Anda adalah yang penuh keceriaan. Cari partner yang bisa mengimbangi energi sosial Anda."},
    4: {"karakter": "Anda adalah 'The Architect (Sang Alchemist / Transformator)'. Struktur berpikir Anda sangat detail dan prosedural. Secara NLP, Anda memiliki filter 'Internal Reference' yang kuat.", "asmara": "Anda butuh kepastian dan rencana jangka panjang. Belajarlah sedikit lebih fleksibel dalam menerima perubahan."},
    5: {"karakter": "Profil 'The Explorer (Sang Eksekutor / Penggerak)'. Anda adalah ahli dalam 'Reframing' situasi sulit menjadi peluang. Anda sangat fleksibel.", "asmara": "Anda butuh ruang gerak (freedom). Hubungan yang mengekang akan membuat Anda merasa 'Suffocated'."},
    6: {"karakter": "Anda adalah 'The Nurturer (Sang Harmonizer / Penyeimbang)'. Fokus utama pikiran Anda adalah pada 'Values' dan tanggung jawab keluarga.", "asmara": "Asmara Anda berbasis pengabdian. Namun, hindari pola 'Mind Reading' (menebak-nebak pikiran pasangan)."},
    7: {"karakter": "Profil 'The Analyst (Sang Legacy Builder / Pembangun Makna)'. Anda adalah pemikir 'Deep Structure'. Intuisi Anda sangat kuat jika sudah terkalibrasi.", "asmara": "Anda butuh waktu 'Me Time' yang cukup. Cari pasangan yang menghargai kedalaman intelektual Anda."},
    8: {"karakter": "Anda adalah 'The Strategist (Sang Sovereign / Penguasa Diri)'. Orientasi Anda adalah pada 'Power' dan 'Outcome'.", "asmara": "Jangan bawa gaya 'Negotiation' bisnis ke dalam ranah asmara. Gunakan lebih banyak 'Soft Skills'."},
    9: {"karakter": "Profil 'The Humanist (Sang Ascended / Kesadaran Tinggi)'. Secara NLP, Anda cenderung memandang dunia secara 'Holistik'.", "asmara": "Anda mencari koneksi jiwa (Soulmate). Tetaplah realistis dalam membangun hubungan."}
}

closing_brutal_dinamis = {
    1: ["Terus menunda karena merasa 'belum sempurna'", "Sulit percaya pada orang lain", "Meng-sabotase diri sendiri"],
    2: ["Terjebak memuaskan orang lain", "Takut berkata 'TIDAK'", "Memendam emosi"],
    3: ["Ide brilian tapi jarang selesai", "Mudah teralihkan fokus", "Menutupi kegelisahan"],
    4: ["Stres berat jika rencana berubah", "Stuck dalam rutinitas kaku", "Kurang empati karena terlalu logis"],
    5: ["Berlari tanpa fondasi kuat", "Cepat merasa tercekik rutinitas", "Kehilangan arah"],
    6: ["Kehabisan energi karena menyelamatkan orang lain", "Over-controlling", "Merasa bersalah memprioritaskan diri"],
    7: ["Terjebak Overthinking", "Merasa terisolasi", "Analisa tanpa eksekusi"],
    8: ["Merasa hampa di tengah target", "Terlihat dingin", "Burnout karena tekanan"],
    9: ["Sering kecewa standar moral tinggi", "Mengizinkan orang toksik menetap", "Kewalahan mengeksekusi visi"]
}

# --- FUNGSI LOGIKA ---
def hitung_angka(tanggal):
    tgl_str = tanggal.strftime("%d%m%Y")
    total = sum(int(digit) for digit in tgl_str)
    while total > 9: total = sum(int(digit) for digit in str(total))
    return total

def get_neptu_weton(tanggal):
    anchor_date = datetime.date(2000, 1, 1)
    selisih_hari = (tanggal - anchor_date).days
    hari_masehi = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_jawa = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"]
    hari = hari_masehi[tanggal.weekday()]
    pasaran = pasaran_jawa[selisih_hari % 5]
    neptu_hari = {"Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9}
    neptu_pasaran = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
    return neptu_hari[hari] + neptu_pasaran[pasaran], f"{hari} {pasaran}"

# --- MENU TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Personal Mapping", "👩‍❤️‍👨 Couple Sync", "🕸️ Audit Pikiran"])

# ==========================================
# TAB 1: PERSONAL MAPPING
# ==========================================
with tab1:
    st.subheader("Bongkar Pola Bawah Sadar")
    nama_user = st.text_input("Nama Lengkap Anda:", placeholder="Siapa nama Anda?", key="t1_nama")
    tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date.today(), format="DD/MM/YYYY")

    if st.button("Mulai Kalibrasi"):
        if len(nama_user) < 3 or tgl_input == datetime.date.today():
            st.error("🚨 Mohon isi nama dan tanggal lahir yang benar.")
        else:
            with st.spinner('Menyelaraskan gelombang otak...'):
                time.sleep(1)
                kode_p = hitung_angka(tgl_input)
                nep, wet = get_neptu_weton(tgl_input)
                insight = data_analisa.get(kode_p)
                pains = closing_brutal_dinamis.get(kode_p)
            
            st.balloons()
            st.markdown(f"### Hasil Mapping: {nama_user}")
            st.info(f"**Kode Program: {kode_p}** | **Weton: {wet}**")
            
            st.subheader("💡 Struktur Karakter")
            type_effect(insight['karakter'])
            
            st.subheader("❤️ Pola Asmara")
            st.warning(insight['asmara'])
            
            st.markdown("---")
            st.error(f"🚨 **Peringatan Bawah Sadar:**\nAnda mungkin sering: \n- {pains[0]}\n- {pains[1]}\n- {pains[2]}")
            
            link_p = {i: f"https://lynk.id/neuronada/checkout-kode-{i}" for i in range(1, 10)}
            st.link_button(f"🔓 Ambil Modul Kode {kode_p}", link_p.get(kode_p))

# ==========================================
# TAB 2: COUPLE SYNC (DINAMIS 100%)
# ==========================================
with tab2:
    st.subheader("Sinkronisasi Pasangan")
    c1, c2 = st.columns(2)
    with c1: n1 = st.text_input("Nama Anda", key="n1"); d1 = st.date_input("Lahir Anda", key="d1")
    with c2: n2 = st.text_input("Nama Pasangan", key="n2"); d2 = st.date_input("Lahir Pasangan", key="d2")
    
    if st.button("Cek Keselarasan"):
        if n1 and n2 and d1 != datetime.date.today():
            with st.spinner('Membaca Vibrasi Gabungan...'):
                time.sleep(1.5)
                
                nep1, weton1 = get_neptu_weton(d1)
                nep2, weton2 = get
