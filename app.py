import streamlit as st
import datetime
import os
import time
import urllib.parse
import urllib.request
import math
import plotly.graph_objects as go
import random
import csv
import io

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

# ==========================================
# DATABASE CLOUD: GOOGLE SHEETS
# ==========================================
URL_POST = "https://script.google.com/macros/s/AKfycbwkOL8-E50RKM5BRR8puh_XbfL-K_hQj5cnv0un6UzmFmMBEG6HZZ4aEQmFZj5EMsSBUQ/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2H-IH_8TbdbMRtvZnvza-InIO-Xl-B9YzLYtWtSb8vpUVuM1uZ4FTi6JwOtk2esj7hilwgGCoWex4/pub?output=csv"

@st.cache_data(ttl=30) # Mesin akan menarik data baru dari Excel setiap 30 detik
def ambil_ulasan():
    try:
        req = urllib.request.Request(URL_CSV)
        with urllib.request.urlopen(req) as response:
            decoded = response.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            data = [row for row in reader]
            return data[::-1] # Dibalik urutannya biar ulasan paling baru ada di atas
    except:
        return []

def kirim_ulasan(nama, rating, komentar):
    try:
        data = urllib.parse.urlencode({"nama": nama, "rating": rating, "komentar": komentar}).encode("utf-8")
        req = urllib.request.Request(URL_POST, data=data)
        urllib.request.urlopen(req)
        return True
    except:
        return False

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

# --- PEMUTAR MUSIK RELAKSASI ---
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #D4AF37;'>🎧 Soundscape Terapi</h4>", unsafe_allow_html=True)
st.caption("<div style='text-align: center; margin-bottom:10px;'>Tekan Play untuk memulai frekuensi relaksasi khusus dari Coach Ahmad Septian.</div>", unsafe_allow_html=True)

if os.path.exists("relaksasi.mp3"):
    st.audio("relaksasi.mp3", format="audio/mp3")
else:
    st.warning("⚠️ Menunggu file 'relaksasi.mp3' diupload ke GitHub.")
st.markdown("---")

# --- DATABASE ANALISA & POTENSI ---
vibrasi_nama_dict = {
    1: "Nama Anda memancarkan getaran KEMANDIRIAN & KEPEMIMPINAN. Orang melihat Anda sebagai sosok yang berani mengambil inisiatif.",
    2: "Nama Anda memancarkan getaran DIPLOMASI & KEDAMAIAN. Orang merasa nyaman dan aman saat berinteraksi dengan Anda.",
    3: "Nama Anda memancarkan getaran EKSPRESI & KECERIAAN. Anda memiliki daya tarik komunikasi yang membuat orang mudah menyukai Anda.",
    4: "Nama Anda memancarkan getaran STRUKTUR & KEDISIPLINAN. Orang mempercayai Anda karena Anda terlihat solid dan bisa diandalkan.",
    5: "Nama Anda memancarkan getaran KEBEBASAN & DINAMIKA. Aura Anda penuh dengan petualangan dan perubahan yang memikat orang lain.",
    6: "Nama Anda memancarkan getaran TANGGUNG JAWAB & KASIH SAYANG. Anda memancarkan aura pengayom yang membuat orang ingin bersandar pada Anda.",
    7: "Nama Anda memancarkan getaran KEDALAMAN & ANALISA. Orang melihat Anda sebagai sosok yang misterius, cerdas, dan pencari kebenaran.",
    8: "Nama Anda memancarkan getaran OTORITAS & KESUKSESAN. Aura nama Anda sangat kuat dalam menarik kelimpahan dan kekuasaan.",
    9: "Nama Anda memancarkan getaran KEMANUSIAAN & IDEALISME. Anda dilihat sebagai sosok berjiwa besar yang peduli pada banyak orang."
}

data_analisa = {
    1: {"karakter": "Anda memiliki profil 'The Leader (Sang Inisiator / Perintis)'. Meta-program Anda sangat proaktif dan berorientasi pada tujuan (Towards). Secara NLP, Anda sering menggunakan filter 'Self', yang membuat Anda mandiri namun kadang terlihat dominan.", "asmara": "Anda butuh pasangan yang menghargai independensi Anda. Hati-hati dengan pola komunikasi 'Command', cobalah lebih banyak menggunakan 'Request' agar pasangan merasa lebih nyaman."},
    2: {"karakter": "Anda adalah 'The Mediator (Sang Penjaga / Penyelaras)'. Kekuatan utama Anda adalah 'Building Rapport' secara instan. Anda sangat sensitif terhadap harmoni lingkungan, namun seringkali mengabaikan kebutuhan diri sendiri (Filter: Others).", "asmara": "Asmara bagi Anda adalah tentang kedekatan emosional. Anda cenderung menghindari konflik, namun waspadai pola 'Pleasing' yang berlebihan. Komunikasikan batasan Anda dengan teknik Assertive Communication."},
    3: {"karakter": "Profil Anda adalah 'The Communicator (Sang Visioner / Ekspresif)'. Anda mahir dalam teknik 'Chunking Up' (melihat gambaran besar) dan menginspirasi orang lain. Pikiran Anda sangat visual dan cepat dalam memproses ide kreatif.", "asmara": "Hubungan yang ideal bagi Anda adalah yang penuh keceriaan dan stimulasi intelektual. Pasangan yang membosankan bisa memicu 'Internal Dialogue' negatif pada diri Anda. Cari partner yang bisa mengimbangi energi sosial Anda."},
    4: {"karakter": "Anda adalah 'The Architect (Sang Alchemist / Transformator)'. Struktur berpikir Anda sangat detail dan prosedural. Secara NLP, Anda memiliki filter 'Internal Reference' yang kuat, sehingga Anda tidak mudah goyah oleh opini luar jika sudah punya data.", "asmara": "Anda butuh kepastian dan rencana jangka panjang. Spontanitas berlebihan dari pasangan bisa membuat sistem internal Anda 'Error'. Belajarlah sedikit lebih fleksibel dalam menerima perubahan rencana."},
    5: {"karakter": "Profil 'The Explorer (Sang Eksekutor / Penggerak)'. Anda adalah ahli dalam 'Reframing' situasi sulit menjadi peluang. Anda sangat fleksibel dan benci dengan batasan atau prosedur yang terlalu kaku.", "asmara": "Anda butuh ruang gerak (freedom). Hubungan yang mengekang akan membuat Anda merasa 'Suffocated'. Komunikasikan kebutuhan Anda akan petualangan baru agar pasangan tidak salah paham."},
    6: {"karakter": "Anda adalah 'The Nurturer (Sang Harmonizer / Penyeimbang)'. Fokus utama pikiran Anda adalah pada 'Values' dan tanggung jawab keluarga. Anda memiliki kapasitas empati yang luar biasa besar melalui kalibrasi emosi yang tajam.", "asmara": "Asmara Anda berbasis pengabdian. Anda adalah pasangan yang sangat suportif. Namun, hindari pola 'Mind Reading' (menebak-nebak pikiran pasangan) yang bisa berujung pada rasa kecewa jika ekspektasi tidak terpenuhi."},
    7: {"karakter": "Profil 'The Analyst (Sang Legacy Builder / Pembangun Makna)'. Anda adalah pemikir 'Deep Structure'. Anda tidak puas dengan informasi permukaan dan selalu mencari makna di balik segalanya. Intuisi Anda sangat kuat jika sudah terkalibrasi dengan baik.", "asmara": "Anda butuh waktu 'Me Time' yang cukup untuk memproses pikiran Anda. Pasangan yang terlalu menuntut perhatian setiap saat bisa membuat Anda mundur. Cari pasangan yang menghargai kedalaman intelektual Anda."},
    8: {"karakter": "Anda adalah 'The Strategist (Sang Sovereign / Penguasa Diri)'. Orientasi Anda adalah pada 'Power' dan 'Outcome'. Anda sangat efisien dalam mengelola sumber daya dan memiliki kepercayaan diri yang solid dalam mengambil risiko.", "asmara": "Dalam hubungan, Anda cenderung menjadi pelindung dan penyedia. Namun, jangan bawa gaya 'Negotiation' bisnis ke dalam ranah asmara. Gunakan lebih banyak 'Soft Skills' dan sentuhan afeksi yang tulus."},
    9: {"karakter": "Profil 'The Humanist (Sang Ascended / Kesadaran Tinggi)'. Anda memiliki 'State of Mind' yang inklusif dan bijaksana. Secara NLP, Anda cenderung memandang dunia secara 'Holistik' dan memiliki misi hidup yang melampaui kepentingan pribadi.", "asmara": "Anda mencari koneksi jiwa (Soulmate). Anda sangat pemaaf, namun waspadai pola 'Generalization' yang membuat Anda sering memaklumi kesalahan pasangan berulang kali. Tetaplah realistis dalam membangun hubungan."}
}

tips_zodiak_nlp = {
    "Aries": "Gunakan teknik 'Pacing' emosi yang lebih sabar.",
    "Taurus": "Berikan ruang untuk 'Reframing' perbedaan pendapat.",
    "Gemini": "Fokus pada 'Deep Rapport' daripada obrolan permukaan.",
    "Cancer": "Hati-hati dengan pola 'Anchor' negatif dari masa lalu.",
    "Leo": "Gunakan bahasa 'Appreciation' untuk pasangan.",
    "Virgo": "Kurangi filter 'Detail', gunakan 'Chunk Up'.",
    "Libra": "Pastikan 'Internal Reference' Anda kuat.",
    "Scorpio": "Bangun 'Trust', hindari 'Mind Reading'.",
    "Sagittarius": "Jaga komitmen melalui 'Value Alignment'.",
    "Capricorn": "Seimbangkan karier dengan kehadiran emosional.",
    "Aquarius": "Hubungkan visi idealis dengan realitas emosional.",
    "Pisces": "Bedakan imajinasi dengan kenyataan."
}

closing_brutal_dinamis = {
    1: ["Terus menunda karena merasa 'belum sempurna' atau takut gagal", "Merasa sendirian memikul beban karena sulit percaya pada orang lain", "Punya ambisi besar, tapi stuck karena meng-sabotase diri sendiri"],
    2: ["Terjebak memuaskan orang lain hingga mengorbankan diri sendiri", "Merasa lelah dan tidak dihargai, tapi takut untuk berkata 'TIDAK'", "Terus memendam emosi demi menghindari konflik"],
    3: ["Memiliki banyak ide brilian, tapi jarang ada yang selesai", "Mudah teralihkan fokusnya dan cepat merasa bosan", "Menutupi kegelisahan sejati di balik candaan"],
    4: ["Stres berat jika rencana berubah atau berhadapan ketidakpastian", "Stuck dalam rutinitas yang kaku dan takut mengambil risiko baru", "Sering dinilai kaku atau kurang empati karena terlalu logis"],
    5: ["Terus berlari dari satu hal ke hal lain tanpa fondasi kuat", "Merasa cepat 'tercekik' oleh rutinitas dan komitmen", "Sulit fokus pada satu tujuan jangka panjang"],
    6: ["Kehabisan energi karena selalu sibuk menyelamatkan orang lain", "Cenderung over-controlling karena rasa khawatir berlebihan", "Merasa bersalah jika harus memprioritaskan diri sendiri"],
    7: ["Terjebak dalam Overthinking dan sulit bertindak nyata", "Merasa terisolasi karena tidak ada yang sefrekuensi", "Terlalu lama menganalisa tanpa eksekusi"],
    8: ["Merasa hampa meskipun sudah mencapai target material", "Terlihat dingin dan menciptakan jarak emosional", "Burnout karena tekanan untuk selalu kuat"],
    9: ["Sering kecewa karena standar moral terlalu tinggi", "Mengizinkan orang yang toksik menetap karena rasa kasihan", "Punya visi mulia, tapi kewalahan mengeksekusinya"]
}

potensi_dinamis = {
    1: """punya potensi kepemimpinan dan daya dobrak luar biasa besar jika ego-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... ambisi ini bisa jadi pola penjara mental yang membelenggu Anda dalam kelelahan kronis seumur hidup.""",
    2: """punya potensi penyembuhan dan diplomasi luar biasa besar jika filter 'Gak Enakan'-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... rasa empati ini bisa jadi pola penjara mental yang terus mengorbankan diri Anda seumur hidup.""",
    3: """punya potensi persuasi dan kreativitas luar biasa besar jika fokusnya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... ide-ide brilian ini bisa jadi pola penjara mental yang membuat Anda jalan di tempat seumur hidup.""",
    4: """punya potensi membangun mahakarya luar biasa besar jika filter kaku-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... perfeksionisme ini bisa jadi pola penjara mental yang membelenggu kebahagiaan Anda seumur hidup.""",
    5: """punya potensi inovasi dan pencapaian luar biasa besar jika filter kebosanannya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... energi petualang ini bisa jadi pola penjara mental yang membuat Anda kehilangan arah seumur hidup.""",
    6: """punya potensi mengayomi dan membina luar biasa besar jika filter 'Mind Reading'-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... pengorbanan buta ini bisa jadi pola penjara mental yang mencekik batin Anda seumur hidup.""",
    7: """punya potensi kebijaksanaan dan analisa luar biasa besar jika filter overthinking-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... isi kepala ini bisa jadi pola penjara mental yang mengisolasi Anda dari realita seumur hidup.""",
    8: """punya potensi eksekusi dan pencapaian luar biasa besar jika filter kontrolnya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... kekuatan ini bisa jadi pola penjara mental yang membuat Anda kesepian di puncak seumur hidup.""",
    9: """punya potensi kesadaran dan harmoni luar biasa besar jika filter ekspektasinya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... idealisme ini bisa jadi pola penjara mental yang penuh kekecewaan seumur hidup."""
}

# --- FUNGSI-FUNGSI LOGIKA (DIPERBARUI DENGAN NEPTU WETON) ---
def hitung_angka(tanggal):
    tgl_str = tanggal.strftime("%d%m%Y")
    total = sum(int(digit) for digit in tgl_str)
    while total > 9: total = sum(int(digit) for digit in str(total))
    return total

def hitung_angka_nama("nama_user"):
    huruf_angka = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':1, 'K':2, 'L':3, 'M':4, 'N':5, 'O':6, 'P':7, 'Q':8, 'R':9, 'S':1, 'T':2, 'U':3, 'V':4, 'W':5, 'X':6, 'Y':7, 'Z':8}
    total = sum(huruf_angka.get(h, 0) for h in nama.upper())
    if total == 0: return 1
    while total > 9: total = sum(int(d) for d in str(total))
    return total

def get_neptu_weton(tanggal):
    anchor_date = datetime.date(2000, 1, 1) # Sabtu Pahing
    selisih_hari = (tanggal - anchor_date).days
    
    hari_masehi = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_jawa = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"]
    
    hari = hari_masehi[tanggal.weekday()]
    pasaran = pasaran_jawa[selisih_hari % 5]
    
    neptu_hari = {"Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9}
    neptu_pasaran = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
    
    total_neptu = neptu_hari[hari] + neptu_pasaran[pasaran]
    nama_weton = f"{hari} {pasaran}"
    return total_neptu, nama_weton

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

def bioritme_nlp(tanggal_lahir):
    hari_hidup = (datetime.date.today() - tanggal_lahir).days
    fisik = math.sin(2 * math.pi * (hari_hidup / 23)) * 100
    emosi = math.sin(2 * math.pi * (hari_hidup / 28)) * 100
    intelektual = math.sin(2 * math.pi * (hari_hidup / 33)) * 100
    
    if emosi > 50 and intelektual > 50: state = "UPTIME STATE (Puncak Kreativitas & Sosial)"
    elif emosi < -50 and fisik < -50: state = "DOWNTIME STATE (Butuh Me-Time & Refleksi)"
    elif intelektual > 50 and fisik < 0: state = "ANALYTICAL STATE (Tajam untuk Perencanaan)"
    else: state = "NEUTRAL STATE (Stabil & Seimbang)"
    
    return int(fisik), int(emosi), int(intelektual), state

def get_arketipe(angka):
    arketipe_dict = {
        1: "The Leader (Sang Inisiator / Perintis)",
        2: "The Mediator (Sang Penjaga / Penyelaras)",
        3: "The Communicator (Sang Visioner / Ekspresif)",
        4: "The Architect (Sang Alchemist / Transformator)",
        5: "The Explorer (Sang Eksekutor / Penggerak)",
        6: "The Nurturer (Sang Harmonizer / Penyeimbang)",
        7: "The Analyst (Sang Legacy Builder / Pembangun Makna)",
        8: "The Strategist (Sang Sovereign / Penguasa Diri)",
        9: "The Humanist (Sang Ascended / Kesadaran Tinggi)"
    }
    return arketipe_dict.get(angka, "Pribadi Unik")

# --- MENU TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Personal Mapping", "👩‍❤️‍👨 Couple Sync", "🕸️ Audit Pikiran"])

# ==========================================
# TAB 1: PERSONAL MAPPING
# ==========================================
with tab1:
    st.subheader("Bongkar Pola Bawah Sadar Anda")
    nama_user = st.text_input("Nama Lengkap Anda:", placeholder="Masukkan nama panggilan Anda...", key="nama_user_t1")
    tgl_today = datetime.date.today()
    tgl_input = st.date_input("Data Input (Tanggal Lahir):", value=tgl_today, min_value=datetime.date(1920, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")

    if st.button("Mulai Pemetaan Internal"):
        if not nama_user or len(nama_user.strip()) < 3:
            st.error("🚨 Satpam NLP: Mohon masukkan nama dengan benar (minimal 3 huruf) agar vibrasi identitas bisa terbaca akurat.")
        elif tgl_input == tgl_today:
            st.error("🚨 Satpam NLP: Mohon masukkan tanggal lahir Anda yang valid, bukan hari ini.")
        else:
            with st.spinner('Melakukan kalibrasi pola pikiran Anda...'):
                time.sleep(1)
                
                angka_hasil = hitung_angka(tgl_input)
                angka_nama = hitung_angka_nama(nama_user)
                _, weton_hasil = get_neptu_weton(tgl_input)
                zodiak_hasil = hitung_zodiak(tgl_input)
                f, e, i, state_harian = bioritme_nlp(tgl_input)
                
                insight = data_analisa.get(angka_hasil)
                arketipe = get_arketipe(angka_hasil)
                pain_points = closing_brutal_dinamis.get(angka_hasil, ["Terjebak dalam pola yang sama", "Merasa stuck", "Butuh perubahan"])
                teks_potensi = potensi_dinamis.get(angka_hasil, "punya potensi luar biasa besar jika filternya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... itu bisa jadi pola penjara mental yang membelenggu seumur hidup.")
            
            st.markdown(f"### 📋 Hasil Mapping: {nama_user}")
            st.markdown("---")
            
            st.success(f"📊 **RADAR ENERGI HARI INI:** Anda sedang berada dalam **{state_harian}**.")
            st.caption(f"Kapasitas Fisik: {f}% | Emosional: {e}% | Intelektual: {i}%")
            st.markdown("---")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("KODE NAMA", angka_nama)
            c2.metric("KODE PROGRAM", angka_hasil)
            c3.metric("ENERGI WETON", weton_hasil)
            c4.metric("POLA ZODIAK", zodiak_hasil)
            
            st.markdown("---")
            
            st.subheader("🗣️ Vibrasi Identitas (Nama)")
            st.info(vibrasi_nama_dict.get(angka_nama, "Nama Anda memiliki resonansi energi yang unik."))

            st.subheader("💡 Struktur Karakter & Mental")
            st.write(f"Halo **{nama_user}**, sistem mendeteksi filter utama pikiran Anda dipengaruhi pola **{zodiak_hasil}** dengan pondasi energi **{weton_hasil}**.")
            st.info(insight['karakter'])

            st.subheader("❤️ Pola Hubungan & Asmara")
            st.warning(f"**Insight Asmara:** {insight['asmara']}")
            st.info(f"**Tips Komunikasi NLP:** {tips_zodiak_nlp.get(zodiak_hasil)}")

            st.markdown("---")
            st.error(f"🚨 **PERHATIAN {nama_user.upper()}**\n\nPola arketipe **{arketipe}** Anda saat ini belum berjalan maksimal.")
            st.markdown(f"**Karena hambatan mental (Mental Block), Anda mungkin sering:**\n- {pain_points[0]}\n- {pain_points[1]}\n- {pain_points[2]}")
            st.warning("👉 **Mau tetap membiarkan pola merusak ini terjadi?** atau\n👉 **Siap melakukan Re-Programming sekarang?**")
            
            st.success(f"Arketipe **{arketipe}** {teks_potensi}")

            link_produk = {
                1: "http://lynk.id/neuronada/kj98l4zgzwdw/checkout",
                2: "http://lynk.id/neuronada/6z23q03121lg/checkout",
                3: "http://lynk.id/neuronada/0rd6gr7nlzxp/checkout",
                4: "http://lynk.id/neuronada/elp83loeyggg/checkout",
                5: "http://lynk.id/neuronada/wne9p4q1l3d9/checkout",
                6: "http://lynk.id/neuronada/nm840y6nlo21/checkout",
                7: "http://lynk.id/neuronada/vv0797ll7g7o/checkout",
                8: "http://lynk.id/neuronada/ropl1lm6rz8g/checkout",
                9: "http://lynk.id/neuronada/704ke23nzmgx/checkout"
            }
            url_tujuan = link_produk.get(angka_hasil, "https://lynk.id/username_lu")
            nama_panggilan = nama_user.split()[0] if nama_user else 'Sahabat'
            
            st.markdown("---")
            st.markdown(f"#### 🔓 Keputusan Ada di Tangan Anda Sekarang, {nama_panggilan}.")
            st.write("Modul ini bukan sekadar e-book, ini adalah **'Kunci Pas'** untuk membongkar mesin bawah sadar Anda. Jangan tunda lagi.")
            
            st.markdown(f"""
            <a href="{url_tujuan}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #d4af37; color: black; padding: 15px; text-align: center; border-radius: 8px; font-weight: bold; font-size: 16px;">
                    👉 YA! SAYA SIAP AMBIL MODUL KODE {angka_hasil}
                </div>
            </a>
            """, unsafe_allow_html=True)

            st.markdown("---")
            phone_number = "628999771486" 
            wa_text = f"Halo Coach Ahmad, saya {nama_user}. Saya sudah baca hasil mapping Kode {angka_hasil} ({arketipe}) saya. Saya lelah terjebak di pola yang sama dan SIAP melakukan Re-Programming. Kapan jadwal Private Session terdekat yang masih kosong?"
            encoded_wa = urllib.parse.quote(wa_text)
            wa_link = f"https://wa.me/{phone_number}?text={encoded_wa}"

            st.markdown(f"""
            <div style="text-align: center; padding: 25px; background-color: #1a1a1a; border: 2px solid #d4af37; border-radius: 10px;">
                <h3 style="color: #d4af37; margin-bottom: 10px;">🔥 Siap Membongkar Mental Block Anda?</h3>
                <p style="color: #f0f0f0; margin-bottom: 20px;">Teori tak mengubah realita. Cabut akar <i>mental block</i> Anda melalui kalibrasi bawah sadar.</p>
                <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 16px;">
                        💬 Amankan Jadwal Sesi Saya
                    </div>
                </a>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("❓ Pertanyaan Terkait Pemetaan")
            with st.expander("Bagaimana sistem ini membedah struktur pikiran saya?"):
                st.write("Sistem **Persona-NLP Analis** menggunakan integrasi data kronologis (tanggal lahir) sebagai pintu masuk untuk mengidentifikasi **Meta-Program** atau filter dominan dalam pikiran bawah sadar Anda. Ini bukan ramalan nasib, melainkan pemetaan kecenderungan perilaku dan gaya pemrosesan informasi Anda.")
            with st.expander("Kenapa akurasinya terasa sangat personal?"):
                st.write("Karena Coach **Ahmad Septian** menggabungkan tiga variabel fundamental: Kode Numerik, Energi Weton, dan Pola Zodiak menjadi satu profil psikografis yang utuh.")
            with st.expander("Apa langkah selanjutnya setelah mengetahui 'Kode Program' ini?"):
                st.write("Langkah selanjutnya adalah **Re-Programming**. Anda bisa menggunakan modul transformasi yang disediakan di atas atau melakukan sesi Deep Calibration secara Private bersama Coach Ahmad.")

            st.markdown("---")
            with st.expander("⚖️ Disclaimer & Batasan Layanan"):
                st.caption(f"**PEMBERITAHUAN PENTING:** Analisa Persona-NLP Analis ini dirancang murni untuk tujuan edukasi dan pengembangan diri. Hasil analisa ini bukan merupakan diagnosis medis atau psikologi klinis. Segala keputusan yang diambil oleh **{nama_user}** setelah membaca analisa ini adalah tanggung jawab pribadi sepenuhnya.\n\n© 2026 Neuro Nada - Ahmad Septian Dwi Cahyo.")

# ==========================================
# TAB 2: COUPLE SYNC (DINAMIS 100%)
# ==========================================
with tab2:
    st.subheader("Sinkronisasi Pasangan")
    c1, c2 = st.columns(2)

    # BATAS TANGGAL
    min_date = datetime.date(1901, 1, 1)
    max_date = datetime.date.today()

    with c1:
        n1 = st.text_input("Nama Anda", key="n1")
        d1 = st.date_input("Lahir Anda", min_value=min_date, max_value=max_date, key="d1")

    with c2:
        n2 = st.text_input("Nama Pasangan", key="n2")
        d2 = st.date_input("Lahir Pasangan", min_value=min_date, max_value=max_date, key="d2")
    
    if st.button("Cek Keselarasan"):

        # VALIDASI UMUR
        umur1 = (datetime.date.today() - d1).days // 365
        umur2 = (datetime.date.today() - d2).days // 365

        if umur1 < 15 or umur2 < 15:
            st.error("🚫 Minimal usia 15 tahun untuk menggunakan fitur ini.")

        elif n1 and n2:
            with st.spinner('Membaca Vibrasi Gabungan...'):
                time.sleep(1.5)
                
                nep1, weton1 = get_neptu_weton(d1)
                nep2, weton2 = get_neptu_weton(d2)
                res = (nep1 + nep2) % 8
                
                hasil_weton_dinamis = {
                    1: [("💔 PEGAT", "Tantangan komunikasi. Latih asertif."), ("💔 PEGAT", "Jaga boundary.")],
                    2: [("👑 RATU", "Harmonis & Disegani."), ("👑 RATU", "Power Couple.")],
                    3: [("💞 JODOH", "Soulmate sejati."), ("💞 JODOH", "Koneksi batin kuat.")],
                    4: [("🌱 TOPO", "Ujian bertumbuh."), ("🌱 TOPO", "Fase kalibrasi.")],
                    5: [("💰 TINARI", "Magnet Rezeki."), ("💰 TINARI", "Kelimpahan karir.")],
                    6: [("⚡ PADU", "Beda Frekuensi."), ("⚡ PADU", "Gesekan logika.")],
                    7: [("👁️ SUJANAN", "Rawan Asumsi."), ("👁️ SUJANAN", "Ujian kepercayaan.")],
                    0: [("🕊️ PESTHI", "Damai & Rukun."), ("🕊️ PESTHI", "Ketenangan batin.")]
                }
                
                judul_dinamis, desc_dinamis = random.choice(hasil_weton_dinamis.get(res, hasil_weton_dinamis[0]))
                ang_tgl_1 = hitung_angka(d1)
                ang_tgl_2 = hitung_angka(d2)
                selisih_tgl = abs(ang_tgl_1 - ang_tgl_2)
                
                pesan_rapport = {
                    0: "💘 **SKOR RAPPORT: 95%**\nFrekuensi Identik.",
                    3: "💘 **SKOR RAPPORT: 90%**\nSangat Sinkron.",
                    6: "💘 **SKOR RAPPORT: 88%**\nHarmoni Alam Bawah Sadar.",
                    9: "💘 **SKOR RAPPORT: 92%**\nKoneksi Kuat.",
                    1: "⚖️ **SKOR RAPPORT: 75%**\nSaling Melengkapi.",
                    2: "⚖️ **SKOR RAPPORT: 70%**\nButuh Penyesuaian.",
                    8: "⚖️ **SKOR RAPPORT: 78%**\nDinamis & Berkembang.",
                }
                rapport_text = pesan_rapport.get(selisih_tgl, "🔥 **SKOR RAPPORT: 50%**\nButuh Kalibrasi Ekstra.")

            st.markdown("---")
            st.subheader(f"🔮 Hasil Audit Asmara: {n1.split()[0].capitalize()} & {n2.split()[0].capitalize()}")
            st.info(f"#### {judul_dinamis}\n{desc_dinamis}")
            
            st.markdown("#### Tingkat Sinkronisasi Pola Pikir (NLP):")
            if selisih_tgl in [0,3,6,9]: st.success(rapport_text)
            elif selisih_tgl in [1,2,8]: st.warning(rapport_text)
            else: st.error(rapport_text)
            
            st.markdown("---")
            st.link_button("Booking Sesi Couple Therapy", "https://wa.me/628999771486")
        else:
            st.warning("Pastikan data diisi dengan lengkap.")
# ==========================================
# TAB 3: AUDIT PIKIRAN
# ==========================================
with tab3:
    st.subheader("🕸️ Audit Keseimbangan Pikiran")
    skor = [st.slider(k, 1, 10, 5) for k in ['Mental', 'Karir', 'Asmara', 'Spiritual', 'Fisik']]
    if st.button("Lihat Radar"):
        fig = go.Figure(data=go.Scatterpolar(r=skor+[skor[0]], theta=['Mental','Karir','Asmara','Spiritual','Fisik','Mental'], fill='toself'))
        st.plotly_chart(fig)
        avg = sum(skor)/5
        msgs = ["Butuh Kalibrasi Segera!", "Kondisi Stabil.", "Luar Biasa, Anda di Peak State!"]
        if avg < 5: st.error(random.choice(msgs[:1]))
        elif avg < 8: st.warning(random.choice(msgs[1:2]))
        else: st.success(random.choice(msgs[2:]))

# ==========================================
# ULASAN DATABASE GOOGLE SHEETS
# ==========================================
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Suara Transformasi</h3>", unsafe_allow_html=True)
st.write("Lihat apa kata mereka yang telah membongkar pola bawah sadarnya di Neuro Nada.")

# Menarik data ulasan dari Google Sheets
daftar_ulasan = ambil_ulasan()

# Tampilkan Maksimal 10 Ulasan Teratas
for ulasan in daftar_ulasan[:10]:
    nama = ulasan.get("Nama", "Anonim")
    rating = ulasan.get("Rating", "⭐⭐⭐⭐⭐")
    teks = ulasan.get("Komentar", "")
    
    if teks: # Hanya tampilkan jika kolom komentar tidak kosong
        st.markdown(f"""
        <div class="ulasan-box">
            <b>{nama}</b> {rating}<br>
            <i>"{teks}"</i>
        </div>
        """, unsafe_allow_html=True)

# Form Input Ulasan Baru ke Excel
with st.expander("💬 Bagikan Pengalaman Anda di sini"):
    with st.form("form_review"):
        rev_nama = st.text_input("Nama Anda")
        rev_rating = st.radio("Rating Bintang", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐"], horizontal=True)
        rev_komentar = st.text_area("Tulis ulasan Anda di sini...")
        
        if st.form_submit_button("Kirim Ulasan"):
            if rev_nama and rev_komentar:
                # Mengirim data ke Google Sheets
                sukses = kirim_ulasan(rev_nama, rev_rating, rev_komentar)
                if sukses:
                    st.success("Terkirim! Terima kasih atas ulasan Anda. Memperbarui layar...")
                    st.cache_data.clear() # Membersihkan ingatan agar ulasan baru langsung terbaca
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Waduh, koneksi ke database gagal. Coba lagi nanti ya.")
            else:
                st.warning("Mohon isi Nama dan Ulasan Anda terlebih dahulu.")

st.markdown("---")
st.markdown("<center><b>Neuro Nada Academy</b><br><small>Ahmad Septian Dwi Cahyo</small></center>", unsafe_allow_html=True)
