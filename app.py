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
    page_title="Neuro Nada Cosmic Analysis", 
    page_icon="🌌", 
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- CUSTOM CSS ---
st.markdown(
    """<style>
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    
    div.stButton > button {
        background-color: #FFD700 !important; color: #000000 !important;
        font-weight: bold !important; border: none !important;
        padding: 12px 24px !important; border-radius: 8px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.02); background-color: #FFC107 !important; }
    
    .ulasan-box {
        background-color: #1e1e1e; padding: 15px; border-radius: 8px;
        border-left: 4px solid #FFD700; margin-bottom: 10px; font-size: 14px;
    }
    
    .cosmic-box {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a4a 100%);
        padding: 15px; border-radius: 10px; border: 1px solid #4a4a8a;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5); margin-bottom: 15px;
    }
    
    /* MATRIKS KECIL PROPORSIONAL */
    .matrix-container {
        display: flex; justify-content: space-between; gap: 8px;
        padding: 12px; background-color: #101010; border-radius: 8px;
        border: 1px solid #333; margin-bottom: 20px;
    }
    .matrix-item { flex: 1; text-align: center; padding: 5px; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .matrix-value { font-size: 16px; font-weight: 800; color: white; }
    .matrix-value-special { color: #FFD700; }
    </style>""", unsafe_allow_html=True
)

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa Kosmik"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

# ==========================================
# DATABASE CLOUD: GOOGLE SHEETS
# ==========================================
URL_POST = "https://script.google.com/macros/s/AKfycbwkOL8-E50RKM5BRR8puh_XbfL-K_hQj5cnv0un6UzmFmMBEG6HZZ4aEQmFZj5EMsSBUQ/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2H-IH_8TbdbMRtvZnvza-InIO-Xl-B9YzLYtWtSb8vpUVuM1uZ4FTi6JwOtk2esj7hilwgGCoWex4/pub?output=csv"

def ambil_ulasan():
    try:
        req = urllib.request.Request(URL_CSV)
        with urllib.request.urlopen(req) as response:
            decoded = response.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            return [row for row in reader][::-1]
    except: return []

def kirim_ulasan(nama, rating, komentar):
    try:
        data = urllib.parse.urlencode({"nama": nama, "rating": rating, "komentar": komentar}).encode("utf-8")
        req = urllib.request.Request(URL_POST, data=data)
        urllib.request.urlopen(req)
        return True
    except: return False

# --- SIDEBAR PROMOSI & VIDEO ---
with st.sidebar:
    if os.path.exists("baru.jpg.png"):
        try: st.image("baru.jpg.png", use_container_width=True); st.markdown("<br>", unsafe_allow_html=True)
        except: pass
    elif os.path.exists("baru.jpg"): st.image("baru.jpg", use_container_width=True)

    st.markdown(f"### {get_greeting()}")
    st.markdown("### 🎬 Hypno-Video Vault")
    st.video("https://youtu.be/kkRcH6aH_lI?si=bpUZF3CWl8DKLw5m")
    st.markdown("---")
    st.info("**Reset Pola Pikir Anda**\n\nMari kita lakukan kalibrasi ulang dalam sesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    st.markdown(f"[👉 **Amankan Jadwal Anda**](https://wa.me/628999771486?text={urllib.parse.quote('Halo Coach Ahmad, saya siap kalibrasi.')})")
    st.markdown("---")
    st.success("**📚 Seni Persuasi NLP**\n\nPelajari bagaimana bahasa bekerja di tingkat bawah sadar.")
    st.markdown("[👉 **Akses Modul Lengkap**](https://lynk.id/neuronada/ebook-nlp)")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

# --- INTERFACE UTAMA ---
if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass

st.markdown("<h1 style='text-align: center; margin-top: 10px;'>🌌 Neuro Nada Cosmic Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #D4AF37; margin-bottom:0;'>Integrasi Falak, Weton, Numerologi & Psikologi Bawah Sadar</p>", unsafe_allow_html=True)
st.markdown("---")

# --- DATABASE ARKETIPE (NEW & DEEP) ---
arketipe_deskripsi = {
    1: "**The Leader (Sang Perintis):** Anda lahir untuk memimpin dan membuka jalan. Arketipe ini memiliki dorongan internal yang kuat untuk mandiri dan benci jika harus didikte. Anda adalah pengambil risiko yang berani, namun seringkali merasa kesepian karena merasa harus memikul tanggung jawab sendirian.",
    2: "**The Mediator (Sang Penyelaras):** Anda adalah lem perekat dalam setiap hubungan. Bakat Anda adalah mendengarkan dan menciptakan harmoni. Arketipe ini sangat peka terhadap perasaan orang lain, namun seringkali kehilangan identitas diri karena terlalu sibuk menyenangkan orang lain (*People Pleaser*).",
    3: "**The Communicator (Sang Visioner):** Anda adalah pembawa pesan dan inspirasi. Pikiran Anda bekerja seperti kembang api; penuh warna dan ide kreatif. Anda pandai menarik perhatian, namun tantangan terbesar Anda adalah menyelesaikan apa yang sudah Anda mulai karena mudah teralihkan oleh hal baru.",
    4: "**The Architect (Sang Transformator):** Anda adalah pembangun sistem. Keamanan, keteraturan, dan detail adalah nafas Anda. Anda sangat bisa diandalkan dan praktis. Namun, Arketipe ini sering terjebak dalam kekakuan dan stres luar biasa jika rencana hidup tidak berjalan sesuai jadwal.",
    5: "**The Explorer (Sang Penggerak):** Anda adalah simbol kebebasan dan adaptasi. Arketipe ini haus akan pengalaman baru dan petualangan. Anda sangat cepat belajar hal baru, namun seringkali merasa hampa karena sulit menemukan 'rumah' atau tujuan tetap dalam jangka panjang.",
    6: "**The Nurturer (Sang Harmonizer):** Anda adalah pengayom sejati. Fokus hidup Anda adalah melayani dan merawat orang-orang yang Anda cintai. Anda memiliki standar moral yang tinggi. Sisi gelapnya: Anda sering merasa dieksploitasi karena Anda memberi terlalu banyak tanpa batasan.",
    7: "**The Analyst (Sang Legacy Builder):** Anda adalah pencari kebenaran dan makna terdalam. Pikiran Anda sangat tajam dan intuitif. Anda tidak puas dengan hal permukaan. Namun, Arketipe ini sering mengisolasi diri dan terjebak dalam labirin pikirannya sendiri (*Overthinking*).",
    8: "**The Strategist (Sang Sovereign):** Anda adalah figur otoritas dan kelimpahan. Arketipe ini memiliki visi besar untuk membangun kerajaan finansial atau pengaruh sosial. Anda sangat tangguh, namun tantangan terbesar Anda adalah berdamai dengan sisi rapuh dan emosional dalam diri Anda.",
    9: "**The Humanist (Sang Kesadaran Tinggi):** Anda adalah jiwa tua yang bijaksana. Anda peduli pada kemanusiaan dan cinta universal. Anda memandang dunia dengan kacamata holistik. Tantangannya: Anda sering merasa patah hati melihat realitas dunia yang tidak seindah idealisme Anda."
}

vibrasi_nama_dict = {
    1: "Nama Anda memancarkan getaran **KEMANDIRIAN**. Orang melihat Anda sebagai sosok alfa. Di dalam hati, Anda rindu tempat bersandar tanpa perlu berpura-pura kuat.",
    2: "Nama Anda memancarkan getaran **DIPLOMASI**. Anda bagaikan oase bagi orang lain, namun sering lupa membersihkan emosi Anda sendiri.",
    3: "Nama Anda memancarkan getaran **EKSPRESI**. Daya tarik magnetis Anda kuat, namun pikiran Anda tak henti memutar skenario kehidupan.",
    4: "Nama Anda memancarkan getaran **STRUKTUR**. Orang mempercayai Anda ibarat batu karang. Sisi tersembunyi: Anda menyimpan kecemasan mendalam.",
    5: "Nama Anda memancarkan getaran **KEBEBASAN**. Aura Anda penuh kejutan. Ketakutan akan komitmen membuat Anda terkadang merasa kehilangan 'jangkar'.",
    6: "Nama Anda memancarkan getaran **TANGGUNG JAWAB**. Anda pelindung natural. Hati-hati, cinta tanpa batasan akan menguras habis energi hidup Anda.",
    7: "Nama Anda memancarkan getaran **KEDALAMAN**. Anda cerdas dan selektif. Lebih memilih 2 sahabat sefrekuensi daripada 100 teman kulit luar.",
    8: "Nama Anda memancarkan getaran **OTORITAS**. Anda memiliki ketahanan baja. Sering merasa kesepian justru ketika berada di puncak pencapaian.",
    9: "Nama Anda memancarkan getaran **IDEALISME**. Visi Anda melampaui ego. Sering dikecewakan karena standar ketulusan Anda terlalu tinggi bagi orang lain."
}

data_analisa = {
    1: {"karakter": "Anda merasa gatal kalau harus menunggu orang lain bergerak. Pikiran selalu fokus pada Outcome.", "asmara": "Butuh pasangan yang tidak mengekang tapi seimbang secara ritme."},
    2: {"karakter": "Bakat alami penyerap energi. Sangat peka suasana hati meski orang diam.", "asmara": "Asmara adalah rasa aman emosional. Berhentilah jadi penyelamat pasangan."},
    3: {"karakter": "Kaya imajinasi dan ide brilian. Sering memutar ulang percakapan masa lalu.", "asmara": "Butuh koneksi yang menyenangkan. Kebisuan adalah siksaan bagi Anda."},
    4: {"karakter": "Perencana detail dan benci ketidakpastian. Pikiran seperti laci rapi.", "asmara": "Sangat setia, namun sering lupa bumbu romantis karena terlalu logis."},
    5: {"karakter": "Benci rutinitas monoton. Hebat mencari celah di saat orang lain buntu.", "asmara": "Kata kunci: Kebebasan. Posesif akan memicu insting melarikan diri."},
    6: {"karakter": "Fokus pada Values keluarga. Gampang kecewa kalau orang tidak sepeduli Anda.", "asmara": "Kepedulian kadang terasa mengatur. Berhenti menebak pikiran pasangan."},
    7: {"karakter": "Intuisi tajam; firasat sering terbukti. Butuh Me-Time untuk menata energi.", "asmara": "Sulit ditembus dan tidak mudah terbuka 100%. Cari yang senada jiwanya."},
    8: {"karakter": "Dorongan kuat untuk sukses. Tahan banting terhadap tekanan mental.", "asmara": "Jangan bawa negosiasi bisnis ke rumah. Gunakan validasi emosi."},
    9: {"karakter": "Jiwa tua yang memandang masalah secara holistik. Standar moral tinggi.", "asmara": "Mencari koneksi spiritual. Menerima ketidaksempurnaan adalah kunci kedamaian."}
}

tips_zodiak_nlp = {
    "Aries": "Pacing dulu emosinya, baru perlahan Lead ke logika Anda.", "Taurus": "Berikan data logis, jangan dipaksa berubah cepat.",
    "Gemini": "Ikuti ritme cepatnya dan gunakan bahasa visual.", "Cancer": "Hati-hati nada suara; cara bicara Anda adalah segalanya.",
    "Leo": "Sentuh egonya dengan apresiasi tulus sebelum masukan.", "Virgo": "Tarik perhatiannya ke gambaran besar masalah.",
    "Libra": "Bantu mereka mengambil keputusan dari keinginan internal.", "Scorpio": "Bangun kepercayaan di level terdalam tanpa kebohongan kecil.",
    "Sagittarius": "Hubungkan masalah saat ini dengan visi masa depan.", "Capricorn": "Mulai dari sudut fungsional, baru masuk emosional.",
    "Aquarius": "Berikan kejutan ide anti-mainstream mendadak.", "Pisces": "Tarik pikiran mereka ke fakta saat imajinasi mulai negatif."
}

closing_brutal_dinamis = {
    1: ["Overthinking hasil belum sempurna", "Gengsi minta tolong", "Membangun tembok ego"],
    2: ["Mengorbankan diri demi orang lain", "Sulit berkata TIDAK", "Memendam amarah konflik"],
    3: ["Menyembunyikan gelisah batin", "Gampang hilang motivasi", "Internal Dialogue terlalu berisik"],
    4: ["Stres rencana mendadak berubah", "Takut resiko baru", "Sering dianggap dingin"],
    5: ["Sindrom Cepat Bosan", "Kelelahan saraf", "Kehilangan arah pijakan"],
    6: ["Burnout mengurus hidup orang", "Over-Protective mengekang", "Merasa bersalah memakai waktu diri"],
    7: ["Paralysis by Analysis", "Merasa terasing tak dipahami", "Mencurigai niat akibat luka lama"],
    8: ["Hampa di puncak sukses", "Sulit melepaskan kontrol", "Mengabaikan alarm tubuh"],
    9: ["Memaklumi orang toxic", "Kecewa ekspektasi manusia", "Kelelahan batin mikirin dunia"]
}

potensi_dinamis = {
    1: "daya dobrak kepemimpinan fenomenal jika gengsinya dibersihkan.", 2: "karunia penyembuhan luar biasa jika mental Gak Enakan dicabut.",
    3: "jenius kreatif yang langka jika loncatan fokusnya dikalibrasi.", 4: "mahakarya solid jika filter kaku-perfeksionisnya dilenturkan.",
    5: "inovator tak terhentikan jika energinya dipusatkan pada satu jangkar.", 6: "magnet kelimpahan jika belajar menghargai diri sendiri dulu.",
    7: "intuisi level dewa jika overthinking-nya direm total.", 8: "penakluk sejati jika berhasil berdamai dengan sisi rapuhnya.",
    9: "pembawa cahaya luar biasa jika berhenti berharap dunia ini sempurna."
}

link_produk = {
    1: "http://lynk.id/neuronada/kj98l4zgzwdw/checkout", 2: "http://lynk.id/neuronada/6z23q03121lg/checkout",
    3: "http://lynk.id/neuronada/0rd6gr7nlzxp/checkout", 4: "http://lynk.id/neuronada/elp83loeyggg/checkout",
    5: "http://lynk.id/neuronada/wne9p4q1l3d9/checkout", 6: "http://lynk.id/neuronada/nm840y6nlo21/checkout",
    7: "http://lynk.id/neuronada/vv0797ll7g7o/checkout", 8: "http://lynk.id/neuronada/ropl1lm6rz8g/checkout",
    9: "http://lynk.id/neuronada/704ke23nzmgx/checkout"
}

# --- FUNGSI LOGIKA ---
def hitung_angka(tanggal):
    total = sum(int(digit) for digit in tanggal.strftime("%d%m%Y"))
    while total > 9: total = sum(int(digit) for digit in str(total))
    return total

def hitung_angka_nama(nama):
    huruf_angka = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':1, 'K':2, 'L':3, 'M':4, 'N':5, 'O':6, 'P':7, 'Q':8, 'R':9, 'S':1, 'T':2, 'U':3, 'V':4, 'W':5, 'X':6, 'Y':7, 'Z':8}
    total = sum(huruf_angka.get(h, 0) for h in nama.upper())
    if total == 0: return 1
    while total > 9: total = sum(int(d) for d in str(total))
    return total

def get_neptu_weton(tanggal):
    anchor_date = datetime.date(2000, 1, 1)
    selisih_hari = (tanggal - anchor_date).days
    hari_n = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_n = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"]
    hari = hari_n[tanggal.weekday()]
    pasaran = pasaran_n[selisih_hari % 5]
    n_hari = {"Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9}
    n_pas = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
    return (n_hari[hari] + n_pas[pasaran]), f"{hari} {pasaran}"

def get_zodiak(tanggal):
    d, m = tanggal.day, tanggal.month
    if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "Aries", "Akselerasi & Keberanian"
    elif (m == 4 and d >= 20) or (m == 5 and d <= 20): return "Taurus", "Kestabilan & Resiliensi"
    elif (m == 5 and d >= 21) or (m == 6 and d <= 20): return "Gemini", "Agility (Ketangkasan)"
    elif (m == 6 and d >= 21) or (m == 7 and d <= 22): return "Cancer", "Proteksi & Intuisi Batin"
    elif (m == 7 and d >= 23) or (m == 8 and d <= 22): return "Leo", "Kharisma & Ekspresi"
    elif (m == 8 and d >= 23) or (m == 9 and d <= 22): return "Virgo", "Presisi & Filter Analitis"
    elif (m == 9 and d >= 23) or (m == 10 and d <= 22): return "Libra", "Ekuilibrium & Harmoni"
    elif (m == 10 and d >= 23) or (m == 11 and d <= 21): return "Scorpio", "Intensitas & Radar Emosi"
    elif (m == 11 and d >= 22) or (m == 12 and d <= 21): return "Sagittarius", "Ekspansi & Visioner"
    elif (m == 12 and d >= 22) or (m == 1 and d <= 19): return "Capricorn", "Sistem & Struktur Kuat"
    elif (m == 1 and d >= 20) or (m == 2 and d <= 18): return "Aquarius", "Inovasi & Anti-Mainstream"
    else: return "Pisces", "Empati & Visualisasi Kuantum"

# FUNGSI YANG SEMPAT HILANG: MENDAPATKAN NAMA ARKETIPE
def get_arketipe(angka):
    arketipe_dict = {
        1: "The Leader (Sang Perintis)", 2: "The Mediator (Sang Penyelaras)", 
        3: "The Communicator (Sang Visioner)", 4: "The Architect (Sang Transformator)", 
        5: "The Explorer (Sang Penggerak)", 6: "The Nurturer (Sang Harmonizer)", 
        7: "The Analyst (Sang Legacy Builder)", 8: "The Strategist (Sang Sovereign)", 
        9: "The Humanist (Sang Kesadaran Tinggi)"
    }
    return arketipe_dict.get(angka, "Pribadi Unik")

def get_moon_phase(date):
    epoch = datetime.date(2000, 1, 6)
    days = (date - epoch).days
    lunations = days / 29.53058867
    p = lunations % 1
    if p < 0.03 or p > 0.97: return ("🌑 Bulan Baru", "Inkubasi", "Fokus internal kuat.", "Meditasi & blueprint.", "Eksekusi ide mentah.")
    elif p < 0.22: return ("🌒 Bulan Sabit Awal", "Momentum", "Dorongan batin tinggi.", "Langkah konkrit & relasi.", "Menunda pekerjaan.")
    elif p < 0.28: return ("🌓 Paruh Awal", "Aksi Nyata", "Karakter petarung aktif.", "Ambil risiko & pecahkan masalah.", "Menyerah pada rintangan.")
    elif p < 0.47: return ("🌔 Bulan Cembung", "Penyesuaian", "Fokus tajam detail.", "Cek ulang strategi & skill.", "Cepat puas diri.")
    elif p < 0.53: return ("🌕 Bulan Purnama", "Puncak Ekspresi", "Sangat karismatik.", "Launching & perluas networking.", "Keputusan emosi sesaat.")
    elif p < 0.72: return ("🌖 Bulan Susut", "Distribusi", "Bakat alami Mentor.", "Berbagi ilmu & pengalaman.", "Pelit ilmu & menahan diri.")
    elif p < 0.78: return ("🌗 Paruh Akhir", "Pembersihan", "Berani buang hal toxic.", "Detoks kebiasaan buruk.", "Menyimpan dendam lama.")
    else: return ("🌘 Bulan Sabit Akhir", "Penyembuhan", "Energi Healer intuitif.", "Rehat & lepas ekspektasi.", "Memaksa kerja keras.")

# FUNGSI YANG SEMPAT HILANG: TIMING HARIAN
def get_daily_timing():
    today = datetime.date.today()
    phase_name, _, _, _, _ = get_moon_phase(today)
    if "New Moon" in phase_name or "Crescent" in phase_name: return phase_name, "🟢 WAKTU EKSEKUSI IDE BARU. Bagus untuk memulai project, relasi, atau keputusan besar."
    elif "Full Moon" in phase_name or "Waxing Gibbous" in phase_name: return phase_name, "🔴 WAKTU RAWAN KONFLIK EGO. Tunda negosiasi berat atau perdebatan asmara hari ini."
    else: return phase_name, "🟡 WAKTU EVALUASI & REHAT. Bagus untuk audit diri, introspeksi, dan melepaskan hal toxic."

# --- MENU TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Identitas Kosmik", "👩‍❤️‍👨 Sinkronisasi Asmara", "🕸️ Audit Sistem Saraf"])

# ==========================================
# TAB 1: IDENTITAS KOSMIK
# ==========================================
with tab1:
    st.subheader("Bongkar Blueprint Bawah Sadar Anda")
    nama_user = st.text_input("Nama Lengkap:", placeholder="Ketik nama Anda...", key="t1_nama")
    tgl_today = datetime.date.today()
    tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date(1995, 1, 1), min_value=datetime.date(1920, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")

    if st.button("Kalkulasi Cetak Biru (Blueprint)"):
        if not nama_user or len(nama_user.strip()) < 3: st.error("🚨 Mohon ketik nama lengkap.")
        elif tgl_input == tgl_today: st.error("🚨 Tanggal belum valid.")
        else:
            with st.spinner('Menyelaraskan gelombang kosmik...'):
                time.sleep(2)
                angka_hasil = hitung_angka(tgl_input); angka_nama = hitung_angka_nama(nama_user)
                nep, wet = get_neptu_weton(tgl_input); zod, zod_s = get_zodiak(tgl_input)
                m_p, m_s, m_d, m_do, m_dont = get_moon_phase(tgl_input)
                today_phase, today_guidance = get_daily_timing()
                desk_ark = arketipe_deskripsi.get(angka_hasil)
                ins = data_analisa.get(angka_hasil); ark_n = get_arketipe(angka_hasil)
                pain = closing_brutal_dinamis.get(angka_hasil); pot = potensi_dinamis.get(angka_hasil)
            
            st.balloons()
            st.markdown(f"### 🌌 Blueprint Kosmik: {nama_user}")
            
            # --- DAILY GUIDANCE KOSMIK ---
            st.markdown(f"""
            <div class="cosmic-box">
                <p style="color: #ccc; font-size: 12px; text-align: center; margin:0; text-transform: uppercase; letter-spacing: 1px;">Timing Falak Hari Ini: {today_phase}</p>
                <div style="text-align: center; font-weight: bold; color: white; font-size: 14px; margin-top: 5px;">
                    {today_guidance}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- MATRIKS KECIL ---
            st.markdown(f"""
            <div class="matrix-container">
                <div class="matrix-item"><div class="matrix-label">Kode Nama</div><div class="matrix-value matrix-value-special">{angka_nama}</div></div>
                <div class="matrix-item"><div class="matrix-label">Kode Program</div><div class="matrix-value matrix-value-special">{angka_hasil}</div></div>
                <div class="matrix-item"><div class="matrix-label">Energi Weton</div><div class="matrix-value">{wet}</div></div>
                <div class="matrix-item"><div class="matrix-label">Pola Zodiak</div><div class="matrix-value">{zod}</div></div>
            </div>
            """, unsafe_allow_html=True)
            
            # --- VIBRASI NAMA ---
            st.subheader("🗣️ Vibrasi Identitas")
            st.info(vibrasi_nama_dict.get(angka_nama))

            # --- ARKETIPE (INI YANG KEMBALI DIMUNCULKAN COACH) ---
            st.subheader(f"🧬 Arketipe Inti: {ark_n}")
            st.write(desk_ark)

            # --- FALAK (MOON PHASE) ---
            st.markdown("---")
            st.subheader("🌑 Energi Ilmu Falak (Bulan Lahir)")
            st.write(f"Lahir pada fase **{m_p}**. Karakter: **{m_s}**.\n*{m_d}*")
            c_do, c_dont = st.columns(2)
            c_do.success(f"✅ **LAKUKAN:**\n{m_do}"); c_dont.error(f"❌ **HINDARI:**\n{m_dont}")

            # --- ANALISA NLP & WETON ---
            st.markdown("---")
            st.subheader("🧠 Struktur Bio-Psikologi NLP")
            st.write(f"Perpaduan frekuensi **{wet}**, karakter **{zod}** ({zod_s}), dan arketipe **{ark_n}** membentuk pola unik: {ins['karakter']}")
            st.warning(f"**Blind Spot Asmara:** {ins['asmara']}")
            st.info(f"💡 **Secret NLP Hack:** {tips_zodiak_nlp.get(zod)}")

            # --- SHADOW SELF ---
            st.markdown(f"""
            <div style="background-color: #3b0000; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
                <h4 style="color: #ff4b4b; margin-top: 0;">🚨 DETEKSI KEBOCORAN ENERGI</h4>
                <p style="color: white; font-size: 15px;">Mental Block Anda sering menyabotase potensi arketipe Anda:</p>
                <ul style="color: #ffcccc; font-size: 15px;"><li>{pain[0]}</li><li>{pain[1]}</li><li>{pain[2]}</li></ul>
                <p style="color: #FFD700; font-weight: bold; margin-bottom: 0;">Padahal program asli Anda {pot}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            url_t = link_produk.get(angka_hasil, "https://lynk.id/neuronada")
            st.markdown(f"""
            <a href="{url_t}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #FFD700; color: black; padding: 15px; text-align: center; border-radius: 8px; font-weight: bold; font-size: 16px;">
                    🔓 AMBIL MODUL TERAPI KODE {angka_hasil} SEKARANG
                </div>
            </a>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 2 & 3 (TETAP SAMA)
# ==========================================
with tab2:
    st.subheader("Sinkronisasi Asmara")
    ca, cb = st.columns(2)
    with ca: n1 = st.text_input("Nama Anda", key="n1"); d1 = st.date_input("Lahir Anda", value=datetime.date(1995, 1, 1), key="d1")
    with cb: n2 = st.text_input("Nama Pasangan", key="n2"); d2 = st.date_input("Lahir Pasangan", value=datetime.date(1995, 1, 1), key="d2")
    if st.button("Cek Kompatibilitas"):
        if n1 and n2:
            ne_1, we_1 = get_neptu_weton(d1); ne_2, we_2 = get_neptu_weton(d2)
            sel = abs(hitung_angka(d1) - hitung_angka(d2))
            st.info(f"Weton: **{we_1}** & **{we_2}**. Integrasi Neptu: {ne_1+ne_2}")
            if sel in [0, 3, 6, 9]: st.success("💘 **SKOR NLP: 90% (Sinkron)**")
            else: st.warning("⚖️ **SKOR NLP: 70% (Butuh Kalibrasi)**")

with tab3:
    st.subheader("🕸️ Audit Sistem Saraf")
    sk = [st.slider(k, 1, 10, 5) for k in ['Mental', 'Karir', 'Asmara', 'Spiritual', 'Fisik']]
    if st.button("Lihat Radar"):
        fig = go.Figure(data=go.Scatterpolar(r=sk+[sk[0]], theta=['Mental','Karir','Asmara','Spiritual','Fisik','Mental'], fill='toself', fillcolor='rgba(212, 175, 55, 0.4)', line=dict(color='#D4AF37')))
        st.plotly_chart(fig)

st.markdown("---")
st.markdown("<center><b>Ahmad Septian Dwi Cahyo</b><br><small>Neuro Nada Cosmic © 2026</small></center>", unsafe_allow_html=True)
