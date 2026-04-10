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
    page_title="Neuro Nada Ultimate OS", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="collapsed" 
)
 
# --- CUSTOM CSS (GLASSMORPHISM & DARK GOLD) ---
st.markdown(
    """<style>
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; background-color: #050505; color: #e0e0e0; }
    
    .stApp { background: radial-gradient(circle at top, #111 0%, #000 100%); }
    
    div.stButton > button {
        background: linear-gradient(90deg, #FFD700 0%, #B8860B 100%) !important; color: #000000 !important;
        font-weight: 900 !important; border: none !important;
        padding: 15px 24px !important; border-radius: 8px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3); letter-spacing: 1px;
    }
    div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(255,215,0,0.5); }
    
    .cta-button {
        background: linear-gradient(90deg, #ff4b4b 0%, #ff0000 100%);
        color: white !important; padding: 15px; text-align: center; 
        border-radius: 8px; font-weight: 900; font-size: 16px; 
        box-shadow: 0 6px 15px rgba(255, 75, 75, 0.4);
        text-transform: uppercase; letter-spacing: 1px;
        transition: 0.3s;
    }
    .cta-button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(255, 75, 75, 0.6); }
 
    .ulasan-box {
        background: rgba(30, 30, 30, 0.6); backdrop-filter: blur(10px);
        padding: 15px; border-radius: 8px;
        border-left: 4px solid #FFD700; margin-bottom: 12px; font-size: 14px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .glass-container {
        background: rgba(25, 25, 25, 0.5); backdrop-filter: blur(12px);
        padding: 20px; border-radius: 12px; border: 1px solid rgba(212,175,55,0.2);
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.4); margin-bottom: 15px;
    }
    
    .primbon-box {
        background: linear-gradient(135deg, rgba(43,27,5,0.8) 0%, rgba(74,48,0,0.8) 100%);
        backdrop-filter: blur(10px);
        padding: 25px; border-radius: 12px; border: 1px solid #D4AF37;
        box-shadow: 0 8px 25px rgba(212,175,55,0.3); margin-top: 20px; margin-bottom: 20px;
    }

    .dynamic-reading-box {
        background: rgba(20, 20, 20, 0.7); backdrop-filter: blur(5px);
        padding: 20px; border-radius: 12px; border-left: 5px solid #FFD700;
        margin-top: 15px; margin-bottom: 15px; font-size: 15px; line-height: 1.6;
    }
    
    .matrix-container {
        display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap;
        padding: 15px; background: rgba(10,10,10,0.8); border-radius: 10px;
        border: 1px solid #333; margin-bottom: 5px;
        box-shadow: inset 0 2px 15px rgba(0,0,0,0.6);
    }
    .matrix-item { flex: 1; min-width: 80px; text-align: center; padding: 5px; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .matrix-value { font-size: 18px; font-weight: 900; color: white; }
    .matrix-value-special { color: #FFD700; }
    
    .list-punchy { padding-left: 20px; margin-bottom: 15px; font-size: 15px; }
    .list-punchy li { margin-bottom: 8px; }
    
    .live-badge {
        background: linear-gradient(90deg, #D4AF37, #FFD700);
        color: #000; padding: 8px 20px; border-radius: 30px;
        font-weight: 900; font-size: 14px; letter-spacing: 1px;
        display: inline-block; box-shadow: 0 4px 15px rgba(255,215,0,0.4);
    }
    </style>""", unsafe_allow_html=True
)
 
def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa Kosmik"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

def get_planetary_hour():
    planets = ["Matahari (Otoritas) ☀️", "Venus (Asmara/Uang) 💖", "Merkurius (Komunikasi) 📝", "Bulan (Intuisi) 🌙", "Saturnus (Karma) 🪐", "Yupiter (Ekspansi) 🍀", "Mars (Aksi) ⚔️"]
    now = datetime.datetime.now()
    return planets[now.hour % 7]
 
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
    st.caption("© 2026 Neuro Nada Academy")
 
# --- INTERFACE UTAMA ---
st.markdown(f"<div style='text-align: right;'><div class='live-badge'>🕒 LIVE PLANET: {get_planetary_hour().upper()}</div></div>", unsafe_allow_html=True)

if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass
 
st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900; color:#FFD700;'>🌌 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #ccc; margin-bottom:0;'>Meretas Realita Melalui Kode Sandi Alam Bawah Sadar</p>", unsafe_allow_html=True)
st.markdown("---")
 
tgl_today = datetime.date.today()
 
# --- DATABASE ARKETIPE NLP & PRIMBON ---
arketipe_punchy = {
    1: {"inti": "Sang Perintis yang lahir untuk memimpin, benci didikte, dan selalu fokus pada tujuan masa depan.", "kekuatan": ["Daya dobrak tinggi & berani ambil risiko", "Mandiri secara absolut", "Fokus eksekusi"]},
    2: {"inti": "Sang Penyelaras yang menjadi lem perekat hubungan, sangat peka membaca emosi lingkungan.", "kekuatan": ["Kapasitas empati tinggi", "Negosiator ulung", "Kemampuan adaptasi emosional"]},
    3: {"inti": "Sang Visioner dengan pikiran bak kembang api; kaya ide, ekspresif, dan magnetis.", "kekuatan": ["Komunikasi memikat", "Kreativitas tanpa batas", "Ahli mencairkan suasana"]},
    4: {"inti": "Sang Transformator yang bertumpu pada struktur, detail, dan keteraturan hidup yang logis.", "kekuatan": ["Pola pikir sangat terstruktur", "Bisa diandalkan 100%", "Ketelitian tingkat dewa"]},
    5: {"inti": "Sang Penggerak yang memuja kebebasan, haus petualangan, dan tercepat beradaptasi.", "kekuatan": ["Kelincahan berpikir", "Inovator pemecah kebuntuan", "Keberanian mengeksplorasi"]},
    6: {"inti": "Sang Harmonizer yang menjadi pelindung natural, rela berkorban merawat lingkaran terdekatnya.", "kekuatan": ["Insting pengayom", "Tanggung jawab moral tinggi", "Loyalitas tanpa pamrih"]},
    7: {"inti": "Sang Legacy Builder yang haus kebenaran, pemikir mendalam, dan intuisi spiritual tajam.", "kekuatan": ["Kemampuan analisa", "Intuisi sering akurat", "Sangat selektif menilai kualitas"]},
    8: {"inti": "Sang Sovereign dengan visi kerajaan. Eksekutor ulung yang memancarkan otoritas.", "kekuatan": ["Tahan banting mental", "Insting bisnis tajam", "Kemampuan memegang kendali"]},
    9: {"inti": "Sang Kesadaran Tinggi (Old Soul) yang memandang dunia secara holistik dengan idealisme luhur.", "kekuatan": ["Kebijaksanaan luas", "Kepedulian universal", "Melihat 'Big Picture'"]}
}
 
arketipe_deskripsi = {
    1: "Anda lahir untuk memimpin dan membuka jalan. Arketipe ini memiliki dorongan internal yang kuat untuk mandiri dan benci jika harus didikte. Anda adalah pengambil risiko yang berani, namun seringkali merasa kesepian karena merasa harus memikul tanggung jawab sendirian.",
    2: "Anda adalah lem perekat dalam setiap hubungan. Bakat Anda adalah mendengarkan dan menciptakan harmoni. Arketipe ini sangat peka terhadap perasaan orang lain, namun seringkali kehilangan identitas diri karena terlalu sibuk menyenangkan orang lain.",
    3: "Anda adalah pembawa pesan dan inspirasi. Pikiran Anda bekerja seperti kembang api; penuh warna dan ide kreatif. Anda pandai menarik perhatian, namun tantangan terbesar Anda adalah menyelesaikan apa yang sudah Anda mulai.",
    4: "Anda adalah pembangun sistem. Keamanan, keteraturan, dan detail adalah nafas Anda. Anda sangat bisa diandalkan dan praktis. Namun, Arketipe ini sering terjebak dalam kekakuan dan stres luar biasa jika rencana mendadak berubah.",
    5: "Anda adalah simbol kebebasan dan adaptasi. Arketipe ini haus akan pengalaman baru dan petualangan. Anda sangat cepat belajar hal baru, namun seringkali merasa hampa karena sulit menemukan 'rumah' jangka panjang.",
    6: "Anda adalah pengayom sejati. Fokus hidup Anda adalah melayani dan merawat orang-orang yang Anda cintai. Anda memiliki standar moral yang tinggi. Sisi gelapnya: Anda sering merasa dieksploitasi karena memberi tanpa batasan.",
    7: "Anda adalah pencari kebenaran dan makna terdalam. Pikiran Anda sangat tajam dan intuitif. Anda tidak puas dengan hal permukaan. Namun, Arketipe ini sering mengisolasi diri dan terjebak dalam labirin pikirannya sendiri.",
    8: "Anda adalah figur otoritas dan kelimpahan. Arketipe ini memiliki visi besar untuk membangun kerajaan finansial atau pengaruh sosial. Anda sangat tangguh, namun tantangan terbesar Anda adalah berdamai dengan sisi emosional Anda.",
    9: "Anda adalah jiwa tua yang bijaksana. Anda peduli pada kemanusiaan dan cinta universal. Anda memandang dunia dengan kacamata holistik. Tantangannya: Anda sering merasa patah hati melihat realitas dunia yang tak sesuai idealisme Anda."
}
 
closing_brutal_dinamis = {
    1: ["Overthinking karena merasa hasil belum sempurna", "Gengsi minta tolong saat memikul beban", "Membangun tembok ego untuk menutupi sepi"],
    2: ["Mengorbankan kebahagiaan diri demi ekspektasi", "Sulit berkata TIDAK yang berujung kelelahan mental", "Memendam amarah demi menghindari konflik"],
    3: ["Menyembunyikan gelisah di balik topeng senyuman", "Cepat kehilangan motivasi jika rutinitas membosankan", "Insomnia karena pikiran terlalu over-analisa"],
    4: ["Stres parah jika rencana mendadak berubah", "Terjebak di zona nyaman karena takut ambil resiko", "Sering dinilai terlalu dingin oleh pasangan"],
    5: ["Sindrom Cepat Bosan yang mensabotase karya", "Kelelahan saraf karena otak tak pernah istirahat", "Merasa hampa kehilangan pijakan komitmen"],
    6: ["Burnout ekstrim sibuk mengurus hidup orang lain", "Sikap Over-Protective yang mengekang", "Rasa bersalah luar biasa memakai waktu untuk diri sendiri"],
    7: ["Menganalisa terus tanpa aksi (Paralysis by Analysis)", "Merasa terasing karena merasa tak ada yang sepemikiran", "Mencurigai niat baik orang akibat luka masa lalu"],
    8: ["Merasa hampa dan kosong di puncak sukses", "Sangat sulit melepaskan kontrol dan memaafkan", "Memaksa tubuh bekerja mengabaikan alarm lelah"],
    9: ["Sering memaklumi orang toxic atas nama kasihan", "Patah hati hebat akibat ekspektasi pada manusia", "Kelelahan batin memikirkan beban dunia"]
}
 
link_produk = {
    1: "http://lynk.id/neuronada/kj98l4zgzwdw/checkout", 2: "http://lynk.id/neuronada/6z23q03121lg/checkout",
    3: "http://lynk.id/neuronada/0rd6gr7nlzxp/checkout", 4: "http://lynk.id/neuronada/elp83loeyggg/checkout",
    5: "http://lynk.id/neuronada/wne9p4q1l3d9/checkout", 6: "http://lynk.id/neuronada/nm840y6nlo21/checkout",
    7: "http://lynk.id/neuronada/vv0797ll7g7o/checkout", 8: "http://lynk.id/neuronada/ropl1lm6rz8g/checkout",
    9: "http://lynk.id/neuronada/704ke23nzmgx/checkout"
}

# --- KAMUS ESOTERIK & FUNGSI DYNAMIC READING ---
KAMUS_ABJAD = {
    'a': 1, 'b': 2, 'j': 3, 'd': 4, 'h': 5, 'w': 6, 'z': 7, 
    't': 9, 'y': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 
    's': 60, 'f': 80, 'q': 100, 'r': 200, 'c': 3, 'e': 5,
    'g': 1000, 'i': 10, 'o': 6, 'p': 80, 'u': 6, 'v': 6, 'x': 60
}

def hitung_nama_esoterik(nama):
    nama_clean = ''.join(filter(str.isalpha, nama.lower()))
    total = sum(KAMUS_ABJAD.get(huruf, 0) for huruf in nama_clean)
    return total if total > 0 else 1

def get_rincian_esoterik(nama):
    nama_clean = ''.join(filter(str.isalpha, nama.lower()))
    rincian = []
    for huruf in nama_clean:
        nilai = KAMUS_ABJAD.get(huruf, 0)
        if nilai > 0: rincian.append(f"{huruf.upper()}({nilai})")
    return " + ".join(rincian)

def generate_dynamic_reading(total_jummal):
    mod = total_jummal % 4 if total_jummal % 4 != 0 else 4
    elemen_dict = {
        1: ("🔥 API (Nar)", "Sistem saraf Anda didesain untuk eksekusi cepat. Anda adalah inisiator. Anda tidak betah pada penundaan. Namun, waspadai ego yang terlalu dominan."),
        2: ("🌍 TANAH (Turab)", "Anda adalah fondasi. Sistem pikiran Anda praktis, sangat logis, dan membumi. Waspadai kekakuan pola pikir jika ada perubahan mendadak di hidup Anda."),
        3: ("💨 UDARA (Hawa)", "Anda adalah Sang Komunikator & Konseptor. Otak Anda memproduksi ide tanpa henti. Karena udara tak bisa digenggam, waspadai energi saraf yang gampang *burnout* akibat *Overthinking*."),
        4: ("💧 AIR (Ma')", "Sistem emosional Anda paling peka. Anda punya empati tinggi untuk beradaptasi dan membaca perasaan orang lain. Waspadai menyerap toxic dari lingkungan luar.")
    }
    el_nama, el_desc = elemen_dict[mod]

    str_jummal = str(total_jummal)
    proses_reduksi = " + ".join(list(str_jummal))
    sum_reduksi = sum(int(d) for d in str_jummal)
    root_num = sum_reduksi
    while root_num > 9: root_num = sum(int(d) for d in str(root_num))
    
    root_dict = {
        1: "Pencipta jalan baru (The Leader). Kebebasan bertindak adalah segalanya.",
        2: "Penyelaras harmoni (The Peacemaker). Kuat di diplomasi dan seni mendengarkan.",
        3: "Penyampai pesan (The Creator). Ekspresi verbal dan ide brilian adalah senjata utama.",
        4: "Pembangun sistem (The Builder). Mencari keamanan melalui struktur dan logika.",
        5: "Agen transformasi (The Explorer). Membenci rutinitas, haus pengalaman baru.",
        6: "Pengayom sejati (The Caregiver). Tanggung jawab moral kuat pada lingkaran terdekat.",
        7: "Pencari esensi (The Seeker). Pikiran selalu menggali makna di balik permukaan.",
        8: "Pemegang kendali (The Executive). DNA dirancang untuk mengelola material dan otoritas.",
        9: "Kesadaran universal (The Humanitarian). Visi melampaui kepentingan pribadi."
    }

    master_note = ""
    if any(m in str_jummal for m in ["11", "22", "33"]):
        master_note = f"<div style='background:rgba(212,175,55,0.1); padding:10px; border-radius:5px; margin-top:10px;'><span style='color:#FFD700;'>⚡ <b>KODE MASTER TERDETEKSI:</b></span> Di dalam komposisi angka Anda terdapat repetisi sakral. Ini menandakan <b>Intuisi Spiritual Tingkat Tinggi</b>. Anda sering kali bisa 'membaca' karakter orang sebelum mereka berbicara (Rapport Otomatis).</div>"

    return el_nama, el_desc, proses_reduksi, sum_reduksi, root_num, root_dict[root_num], master_note

def hitung_angka(tanggal):
    total = sum(int(digit) for digit in tanggal.strftime("%d%m%Y"))
    while total > 9: total = sum(int(digit) for digit in str(total))
    return total
 
def get_neptu_weton(tanggal):
    anchor_date = datetime.date(2000, 1, 1)
    selisih_hari = (tanggal - anchor_date).days
    hari_n = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_n = ["Legi", "Pahing", "Pon", "Wage", "Kliwon"]
    hari = hari_n[tanggal.weekday()]
    pasaran = pasaran_n[selisih_hari % 5]
    n_hari = {"Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9}
    n_pas = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
    return (n_hari[hari] + n_pas[pasaran]), hari, pasaran
 
def get_betaljemur_data(neptu, hari):
    lakuning = {
        7: ("Lebu Katiup Angin", "Pikiran dinamis, mudah goyah, sering berpindah fokus."),
        8: ("Lakuning Geni", "Emosi meledak-ledak. Rentan abreaction, butuh teknik pacing tinggi."),
        9: ("Lakuning Angin", "Gampang dipengaruhi sugesti eksternal, adaptif namun labil."),
        10: ("Pandito Mbangun Teki", "Introspektif, suka menasihati, pola pikir deep structure."),
        11: ("Macan Ketawan", "Aura pemimpin tajam, pemberani, ego dominan saat dikritik."),
        12: ("Lakuning Kembang", "Menebar pesona, cinta damai, rapport natural sangat mudah."),
        13: ("Lakuning Lintang", "Suka menyendiri, memancarkan pesona magnetis tanpa banyak bicara."),
        14: ("Lakuning Rembulan", "Penenang batin, pendengar ulung, jangkar emosi bagi orang lain."),
        15: ("Lakuning Srengenge", "Pencerah, berwibawa, sangat logis dan tidak mudah dihipnotis."),
        16: ("Lakuning Banyu", "Kelihatan tenang di permukaan, mematikan jika batasnya dilanggar."),
        17: ("Lakuning Bumi", "Sangat sabar, pengayom, membumi, dan tidak terburu-buru."),
        18: ("Paripurna", "Elemen kesempurnaan, memegang kendali otoritas dengan sangat bijak.")
    }
    mod_panca = neptu % 5 if neptu % 5 != 0 else 5
    pancasuda = {
        1: ("Sri (Kemakmuran)", "Potensi rezeki dan kelimpahan sangat terbuka lebar."),
        2: ("Lungguh (Tahta/Posisi)", "Garis nasib kuat di area karir, pengaruh, dan jabatan."),
        3: ("Gedhong (Kekayaan)", "Aura penarik aset material dan fondasi bisnis yang kuat."),
        4: ("Loro (Ujian/Sakit)", "Rentan kebocoran energi saraf (burnout) atau ujian hidup panjang."),
        5: ("Pati (Rintangan)", "Sering menemui jalan buntu jika tidak menggunakan strategi kalibrasi.")
    }
    naga_dina = {
        "Minggu": "Timur (Kejayaan)", "Senin": "Selatan (Kejayaan)",
        "Selasa": "Barat (Kejayaan)", "Rabu": "Utara (Kejayaan)",
        "Kamis": "Timur (Kejayaan)", "Jumat": "Selatan (Kejayaan)", "Sabtu": "Selatan (Kejayaan)"
    }
    return lakuning.get(neptu, ("Anomali", "Karakter kompleks"))[0], lakuning.get(neptu, ("Anomali", "Karakter kompleks"))[1], pancasuda.get(mod_panca)[0], pancasuda.get(mod_panca)[1], naga_dina.get(hari)
 
def get_zodiak(tanggal):
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
 
# --- MENU TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["👤 Personal Identity", "👩‍❤️‍👨 Couple Matrix", "🕸️ Audit Sistem Saraf", "📚 FAQ & Disclaimer"])
 
# ==========================================
# TAB 1: IDENTITAS KOSMIK & BETALJEMUR
# ==========================================
with tab1:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("Akses Blueprint Bawah Sadar Anda")
    nama_user = st.text_input("Nama Lengkap:", placeholder="Ketik nama asli Anda...", key="t1_nama")
    tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date(1995, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")
    st.markdown("</div>", unsafe_allow_html=True)
 
    if st.button("Kalkulasi Blueprint (Mulai)"):
        if not nama_user or len(nama_user.strip()) < 3: 
            st.error("🚨 Mohon ketik nama lengkap untuk sinkronisasi vibrasi.")
        elif tgl_input == tgl_today: 
            st.error("🚨 Tanggal lahir tidak valid.")
        else:
            status_text = st.empty()
            status_text.markdown("⏳ *Mengekstraksi sandi Hisab Jummal (Ilmu Huruf)...*")
            time.sleep(0.5)
            status_text.markdown("⏳ *Membuka segel Kitab Betaljemur Adammakna...*")
            time.sleep(0.5)
            status_text.empty()
            
            angka_hasil = hitung_angka(tgl_input)
            nilai_jummal = hitung_nama_esoterik(nama_user)
            rincian_jummal = get_rincian_esoterik(nama_user)
            
            el_nama, el_desc, p_reduk, s_reduk, r_num, r_desc, m_note = generate_dynamic_reading(nilai_jummal)
            
            nep, hari, pasaran = get_neptu_weton(tgl_input)
            wet = f"{hari} {pasaran}"
            zod = get_zodiak(tgl_input)
            
            n_laku, d_laku, n_panca, d_panca, arah_naga = get_betaljemur_data(nep, hari)
            
            punchy = arketipe_punchy.get(angka_hasil)
            desk_ark = arketipe_deskripsi.get(angka_hasil)
            shadow = closing_brutal_dinamis.get(angka_hasil)
            
            st.snow()
            st.markdown(f"<h3 style='text-align:center;'>🌌 Blueprint Kosmik: {nama_user.upper()}</h3>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="matrix-container">
                <div class="matrix-item"><div class="matrix-label">Nilai Esoterik</div><div class="matrix-value matrix-value-special">{nilai_jummal}</div></div>
                <div class="matrix-item"><div class="matrix-label">Elemen Dasar</div><div class="matrix-value">{el_nama.split(' ')[1]}</div></div>
                <div class="matrix-item"><div class="matrix-label">Meta-Program</div><div class="matrix-value matrix-value-special">KODE {angka_hasil}</div></div>
                <div class="matrix-item"><div class="matrix-label">Filter Zodiak</div><div class="matrix-value">{zod}</div></div>
                <div class="matrix-item"><div class="matrix-label">Energi Weton</div><div class="matrix-value">{wet} (Neptu {nep})</div></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="dynamic-reading-box">
                <h4 style="color: #FFD700; margin-top:0;">🔍 Bedah DNA Angka Anda</h4>
                <p>Secara arsitektur Gematria Kuno (Hisab Jummal), total nilai getaran aksara nama Anda adalah: <br>
                <code style="color:#25D366; background:transparent; padding:0;">{rincian_jummal} = <b>{nilai_jummal}</b></code></p>
                <ol style="margin-left: -15px;">
                    <li><b>Elemen Bawah Sadar:</b> Nilai {nilai_jummal} direduksi menjadi 4 pilar alam semesta, Anda berafiliasi dengan <b>{el_nama}</b>.<br><i style="color:#aaa;">{el_desc}</i></li>
                    <li><b>Inti Jiwa (Root Number):</b> {p_reduk} = {s_reduk} ➡ <b>{r_num}</b>.<br>Angka {r_num} adalah sandi bahwa secara sadar/bawah sadar Anda adalah: <b>{r_desc}</b></li>
                </ol>
                {m_note}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="primbon-box">
                <div style="text-align:center; border-bottom:1px solid #D4AF37; padding-bottom:10px; margin-bottom:15px;">
                    <span style="color:#D4AF37; font-size:14px; font-weight:900; letter-spacing:2px;">📜 PETHIKAN KITAB BETALJEMUR ADAMMAKNA</span>
                </div>
                <div style="font-size:15px; line-height:1.6; margin-bottom: 15px;">
                    <span style="color:#aaa;">Sandi Pangarasan (Meta-Program Bawah Sadar):</span> <br>
                    <b style="color:#FFF; font-size:18px;">{n_laku}</b> — <i style="color:#ccc;">"{d_laku}"</i>
                </div>
                <div style="font-size:15px; line-height:1.6; background: rgba(212,175,55,0.1); padding: 10px; border-radius: 8px;">
                    <span style="color:#FFD700;">🧭 <b>NAGA DINA (Arah Kejayaan Hari {hari}):</b></span> <b style="font-size: 16px;">{arah_naga}</b><br>
                    <i style="color:#888; font-size:13px;">*ACTIONABLE: Posisikan meja kerja atau arah duduk Anda menghadap zona kejayaan di atas saat mengambil keputusan penting hari ini.</i>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 👁️ Decode Kepribadian Inti")
            st.info(f"Sistem mengkunci arketipe utama Anda:\n\n**IDENTITAS INTI:** {punchy['inti']}")
            st.write(desk_ark)
            
            c_kekuatan, c_shadow = st.columns(2)
            with c_kekuatan:
                st.markdown("🔥 **KEKUATAN DOMINAN:**")
                st.markdown(f"<ul class='list-punchy' style='color:#25D366;'><li>{punchy['kekuatan'][0]}</li><li>{punchy['kekuatan'][1]}</li><li>{punchy['kekuatan'][2]}</li></ul>", unsafe_allow_html=True)
            with c_shadow:
                st.markdown("⚠️ **SISI GELAP (SHADOW SELF):**")
                st.markdown(f"<ul class='list-punchy' style='color:#ff4b4b;'><li>{shadow[0]}</li><li>{shadow[1]}</li><li>{shadow[2]}</li></ul>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            url_t = link_produk.get(angka_hasil, "https://lynk.id/neuronada")
            st.markdown(f"""
            <a href="{url_t}" target="_blank" style="text-decoration: none;">
                <div class="cta-button">
                    ⚠️ BONGKAR MENTAL BLOCK KODE {angka_hasil} & REBUT KENDALI HIDUP ANDA
                </div>
            </a>
            """, unsafe_allow_html=True)
 
# ==========================================
# TAB 2: COUPLE MATRIX (UPDATED)
# ==========================================
with tab2:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("Penyatuan Esoterik & Betaljemur (Couple Matrix)")
    st.write("Analisis benturan ego dan peleburan frekuensi kosmik antara Anda dan pasangan secara mendalam.")
    ca, cb = st.columns(2)
    with ca: 
        n1 = st.text_input("Nama Anda", key="n1")
        d1 = st.date_input("Lahir Anda", value=datetime.date(1995, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=tgl_today, key="d1")
    with cb: 
        n2 = st.text_input("Nama Pasangan", key="n2")
        d2 = st.date_input("Lahir Pasangan", value=datetime.date(1995, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=tgl_today, key="d2")
    st.markdown("</div>", unsafe_allow_html=True)
        
    if st.button("Analisis Resonansi Pasangan"):
        if n1 and n2:
            st.snow()
            # Kalkulasi Weton & NLP
            zod1 = get_zodiak(d1); ne_1, _, _ = get_neptu_weton(d1)
            zod2 = get_zodiak(d2); ne_2, _, _ = get_neptu_weton(d2)
            sel = abs(hitung_angka(d1) - hitung_angka(d2))
            sisa_weton = (ne_1 + ne_2) % 8
            
            # Kalkulasi Jummal Couple
            jummal_1 = hitung_nama_esoterik(n1)
            jummal_2 = hitung_nama_esoterik(n2)
            total_couple = jummal_1 + jummal_2
            
            # Root hitung untuk Persona Pasangan
            root_c = total_couple
            while root_c > 9: root_c = sum(int(d) for d in str(root_c))
            
            couple_persona = {
                1: ("THE POWER COUPLE", "Penyatuan dua nama ini menghasilkan vibrasi dominan. Kalian adalah entitas yang mandiri, ambisius, dan selalu ingin menjadi yang terdepan."),
                2: ("THE SOULMATES", "Vibrasi yang terbentuk sangat harmonis. Masing-masing pihak tahu cara melengkapi dan membaca perasaan pasangannya tanpa harus bicara."),
                3: ("THE SOCIALITES", "Energi yang dihasilkan memancarkan aura ekspresif. Kalian adalah pasangan yang menyenangkan, penuh ide, dan punya circle pergaulan yang luas."),
                4: ("THE BUILDERS", "Penyatuan nama menciptakan vibrasi yang solid dan struktural. Fokus hubungan ini adalah fondasi yang kuat, kesetiaan, dan pembangunan aset masa depan."),
                5: ("THE ADVENTURERS", "Vibrasi kebebasan sangat pekat. Pasangan yang anti-monoton, suka pengalaman baru, dan hubungan kalian penuh dengan kejutan tak terduga."),
                6: ("THE FAMILY FIRST", "Energi yang dihasilkan murni berpusat pada rumah dan kasih sayang. Tingkat pengorbanan kalian terhadap kelestarian keluarga sangat luar biasa."),
                7: ("THE DEEP SEEKERS", "Vibrasi eksklusif dan tertutup. Hubungan kalian dibangun di atas koneksi intelektual dan spiritual. Kalian seringkali lebih suka privasi tinggi."),
                8: ("THE EMPIRE", "Penyatuan dua nama ini menciptakan magnet kelimpahan. Fokus energi kalian secara bawah sadar ditarik menuju kesuksesan finansial dan kekuasaan."),
                9: ("THE HEALERS", "Energi toleransi level tertinggi. Hubungan kalian mengedepankan keikhlasan dan sering menjadi tempat curhat/sandaran bagi orang lain di sekitar kalian.")
            }
            c_title, c_desc = couple_persona.get(root_c, ("Uncharted", "Kombinasi unik yang terus beradaptasi."))
            
            hasil_weton_kombo = {
                1: ("💔 PEGAT (Ujian Ego)", "Terdapat perbedaan mendasar dalam memproses emosi. Jika ada konflik, seringkali diwarnai adu argumen keras.", "Gunakan teknik **Pacing-Leading**: Validasi dulu perasaannya ('Aku ngerti kamu kesal...') sebelum memasukkan argumen/solusi logis Anda.", "DILARANG keras melakukan *Mind-Reading* (menebak-nebak pikiran negatif) dan jangan pernah mengungkit kesalahan masa lalunya."),
                2: ("👑 RATU (Kharisma & Harmoni)", "Penyatuan vibrasi ini memancarkan wibawa dan respek dari lingkungan sekitar. Energi kepemimpinannya saling mendukung.", "Jadikan pasangan sebagai *Partner Diskusi Strategis*. Berikan afirmasi positif setiap kali dia berhasil melakukan pencapaian kecil.", "Hindari terjebak pada pencitraan eksternal. Jangan menyembunyikan masalah nyata hanya demi terlihat 'sempurna' di mata orang lain."),
                3: ("💞 JODOH (Sinkronisasi Alami)", "Penerimaan bawah sadar luar biasa tinggi. Kalian menemukan kecocokan yang tidak bisa dijelaskan secara logis.", "Ciptakan **Pattern Interrupt** (kejutan kecil/hal tak terduga) secara rutin agar hubungan tetap *spark* dan tidak terasa membosankan.", "Jangan jadikan kecocokan ini sebagai alasan kemalasan (*Comfort Zone*). Seringkali pasangan Jodoh mandek secara karir karena terlalu santai."),
                4: ("🌱 TOPO (Ujian Bertumbuh)", "Fase awal penuh gesekan dan kesalahpahaman. Namun jika berhasil melewati kalibrasi awal, hubungannya sangat kokoh.", "Kuasai teknik **Reframing** saat krisis. Temukan hikmah atau sudut pandang positif di setiap masalah yang mendera hubungan kalian.", "Hindari memaksakan *Map of the World* (standar nilai pribadi/gengsi) Anda kepada pasangan. Belajarlah menurunkan ego masing-masing."),
                5: ("💰 TINARI (Magnet Rezeki)", "Penyatuan vibrasi nama dan waktu lahir ini menarik kelancaran energi material. Pintu rezeki terbuka lebar setelah bersatu.", "Fokuskan komunikasi pada perencanaan visi masa depan dan *Goal Setting* bersama. Harmonisasi kalian adalah kunci kelancaran finansial.", "Jangan menjadikan uang/materi sebagai satu-satunya perekat hubungan. Jika salah satu bangkrut, hubungan bisa sangat rentan bubar."),
                6: ("⚡ PADU (Beda Frekuensi)", "Kerap terjadi letupan perdebatan karena beda filter informasi. Cara otak memproses stimulus sangat berbeda.", "Berikan ruang (Space) saat emosi memuncak. Gunakan teknik **Yes-Set** (membuat pasangan berkata 'Ya' 3x) untuk meredakan tensinya.", "Hindari konfrontasi langsung saat *state* emosinya sedang tinggi. Jangan gunakan kalimat provokatif yang menyerang harga dirinya."),
                7: ("👁️ SUJANAN (Rawan Asumsi)", "Ada kecenderungan kecemburuan atau salah paham mendadak karena miskomunikasi bawah sadar yang sering menumpuk.", "Biasakan komunikasi murni berbasis *Sensory Based* (Fakta yang terlihat/terdengar), bukan berdasarkan asumsi atau 'perasaan' semata.", "DILARANG keras menggunakan bahasa *Generalisasi* seperti: 'Kamu SELALU begini!', 'Kamu TIDAK PERNAH peduli!'. Itu merusak alam bawah sadarnya."),
                0: ("🕊️ PESTHI (Damai & Rukun)", "Hubungan yang stabil, adem ayem, rukun, dan minim drama. Energi kalian menetralisir stres satu sama lain.", "Pertahankan *Rapport* (kedekatan batin) dengan deep-talk rutin. Eksplorasi hobi baru bersama untuk menjaga gairah kehidupan.", "Jangan membiarkan api asmara padam karena hubungan terasa terlalu hambar/lurus-lurus saja. Hindari sikap *Take it for granted* (meremehkan).")
            }
            judul_weton, desk_weton, saran_do, saran_dont = hasil_weton_kombo.get(sisa_weton, ("Analisa Unik", "Butuh kalibrasi", "Perbaiki komunikasi", "Jangan egois"))
            
            st.markdown("---")
            st.markdown(f"### 🔮 The Unified Resonance: {n1.split()[0].upper()} & {n2.split()[0].upper()}")
            
            # THE COUPLE MATRIX BOX (NEW)
            st.markdown(f"""
            <div class="matrix-container">
                <div class="matrix-item"><div class="matrix-label">Vibrasi {n1.split()[0]}</div><div class="matrix-value">{jummal_1}</div></div>
                <div class="matrix-item"><div class="matrix-label">Vibrasi {n2.split()[0]}</div><div class="matrix-value">{jummal_2}</div></div>
                <div class="matrix-item" style="background: rgba(212,175,55,0.2);"><div class="matrix-label" style="color:#FFD700;">TOTAL ENERGI</div><div class="matrix-value matrix-value-special">{total_couple}</div></div>
                <div class="matrix-item"><div class="matrix-label">Weton Kombo</div><div class="matrix-value">{sisa_weton}</div></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="dynamic-reading-box" style="border-left-color: #25D366;">
                <h4 style="color: #25D366; margin-top:0;">🧬 Persona Pasangan: {c_title}</h4>
                <p>Ketika nilai esoterik <b>{jummal_1}</b> dan <b>{jummal_2}</b> disatukan, ia menghasilkan resonansi root number <b>{root_c}</b>.<br>
                <i>{c_desc}</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"#### 📜 Titik Benturan Weton: {judul_weton}")
            st.info(f"Menyatukan filter pikiran **{zod1}** dengan **{zod2}** ibarat menggabungkan dua elemen alam. Ditambah algoritma Primbon (Neptu {ne_1} disilang Neptu {ne_2}), menghasilkan takdir:\n\n{desk_weton}")
            
            if sel in [0, 3, 6, 9]: st.success("💘 **SKOR META-PROGRAM (NLP): 90% (Sangat Sinkron)** - Peta mental kalian sangat mirip.")
            elif sel in [1, 2, 8]: st.warning("⚖️ **SKOR META-PROGRAM (NLP): 70% (Dinamis)** - Butuh toleransi dalam mengambil keputusan.")
            else: st.error("🔥 **SKOR META-PROGRAM (NLP): 50% (Rawan Gesekan)** - Sering terjadi perbedaan *Point of View*.")
 
            st.markdown("<br>", unsafe_allow_html=True)
            c_do_c, c_dont_c = st.columns(2)
            with c_do_c: 
                st.markdown(f"<div style='background:rgba(37,211,102,0.1); padding:20px; border-radius:10px; border:1px solid #25D366;'>✅ <b>LAKUKAN INI (NLP TACTICS):</b><br><br>{saran_do}</div>", unsafe_allow_html=True)
            with c_dont_c: 
                st.markdown(f"<div style='background:rgba(255,75,75,0.1); padding:20px; border-radius:10px; border:1px solid #ff4b4b;'>❌ <b>HINDARI INI (FATAL ERRORS):</b><br><br>{saran_dont}</div>", unsafe_allow_html=True)
 
# ==========================================
# TAB 3: AUDIT SISTEM SARAF
# ==========================================
with tab3:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("🕸️ Audit Sistem Saraf (Wheel of Life)")
    st.info("**Apa itu Audit Sistem Saraf?**\n\nEnergi manusia mengalir layaknya jaring. Geser *slider* sejujur-jujurnya untuk melihat kebocoran energi Anda saat ini.")
    kategori_label = ['Kesehatan Mental', 'Karir & Finansial', 'Asmara', 'Spiritual', 'Fisik']
    sk = [st.slider(k, 1, 10, 5) for k in kategori_label]
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Mulai Audit Radar"):
        fig = go.Figure(data=go.Scatterpolar(
            r=sk+[sk[0]], theta=['Mental','Karir','Asmara','Spiritual','Fisik','Mental'], 
            fill='toself', fillcolor='rgba(212, 175, 55, 0.4)', line=dict(color='#D4AF37')
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
        st.plotly_chart(fig)
        avg = sum(sk)/5
        if avg < 5: st.error("🚨 **KONDISI KRITIS (ALARM BERBUNYI)**\n\nSistem saraf Anda sedang kelelahan parah. Anda butuh 'Detoks Mental' secepatnya sebelum berujung pada psikosomatis.")
        elif avg < 8: st.warning("🟡 **ZONA NYAMAN YANG MENIPU**\n\nSistem mendeteksi Anda memendam potensi besar yang tertahan. Selesaikan area terlemah Anda, dan lihat keajaiban terjadi.")
        else: st.success("🔥 **PEAK STATE (GELOMBANG EMAS)**\n\nSinkronisasi otak dan tindakan Anda sangat sempurna. Ini momentum terbaik mengeksekusi visi Anda!")

# ==========================================
# TAB 4: FAQ & DISCLAIMER
# ==========================================
with tab4:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("📚 FAQ & Informasi Sistem")
    
    with st.expander("🤔 1. Apa itu Hisab Jummal (Angka Esoterik)?"):
        st.write("Hisab Jummal (Gematria Arab) adalah ilmu sains huruf kuno yang memberikan bobot matematika pada setiap aksara. Sistem ini meyakini bahwa nama yang diberikan sejak lahir membawa frekuensi atau getaran energi tertentu yang mempengaruhi sistem saraf dan karakter bawaan Anda.")
        
    with st.expander("🤔 2. Apakah hasil ini 100% mutlak/ramalan pasti?"):
        st.write("TIDAK. Neuro Nada bukan alat peramal nasib, melainkan **Alat Pemetaan Pola (Pattern Mapping)**. Sistem ini menggabungkan Metafisika Kuno (Primbon/Falak) dengan pendekatan Psikologi Modern (Neuro-Linguistic Programming). Tujuannya adalah untuk memberikan *Self-Awareness* agar Anda bisa memaksimalkan potensi dan mengatasi 'Shadow Self' (Sisi Gelap) Anda.")
        
    with st.expander("🤔 3. Kenapa saya harus pakai Nama Asli/KTP?"):
        st.write("Frekuensi energi paling fundamental terikat pada niat dan getaran nama pertama yang disematkan oleh orang tua Anda saat lahir. Nama panggilan hanya mencerminkan 'Topeng Sosial' (Persona) Anda, bukan cetak biru (Blueprint) jiwa Anda yang sebenarnya.")
        
    with st.expander("🤔 4. Bagaimana cara menggunakan info 'Arah Kejayaan'?"):
        st.write("Arah Naga Dina adalah kompas energi geomagnetik harian. Jika sistem mengarahkan Anda ke 'Timur', posisikan tempat duduk kerja, arah meja negoisasi, atau posisi Anda saat melakukan presentasi menghadap ke arah Timur untuk menyelaraskan gelombang otak Anda dengan energi alam hari tersebut.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.error("**⚠️ DISCLAIMER LEGAL & ETIS:**")
    st.markdown("""
    * **Bukan Saran Medis/Psikologis Profesional:** Hasil analisis ini bersifat edukasional dan optimalisasi pengembangan diri. Jika Anda mengalami gangguan depresi klinis atau trauma berat, silakan hubungi psikolog atau psikiater berlisensi.
    * **Kendali di Tangan Anda:** Aplikasi ini hanya membedah potensi *bawah sadar*. Nasib dan takdir sepenuhnya adalah hak prerogatif Tuhan Yang Maha Esa dan merupakan hasil dari tindakan sadar Anda sendiri.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
 
# ==========================================
# SOCIAL PROOF (ULASAN DINAMIS)
# ==========================================
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Jejak Transformasi</h3>", unsafe_allow_html=True)
 
daftar_ulasan = ambil_ulasan()
 
if daftar_ulasan:
    pilihan_marquee = daftar_ulasan[:3]
    marquee_content = " | ".join([f"<span style='color: #FFD700;'>{u.get('Rating', '⭐⭐⭐⭐⭐')}</span> <b>{u.get('Nama', 'User')}:</b> \"{u.get('Komentar', '')[:50]}...\"" for u in pilihan_marquee])
    st.markdown(f"""
    <div style="background-color: #1a1a1a; padding: 12px; border-radius: 8px; border-left: 3px solid #D4AF37; border-right: 3px solid #D4AF37; white-space: nowrap; overflow: hidden; margin-bottom: 20px;">
        <marquee behavior="scroll" direction="left" scrollamount="6" style="color: #f0f0f0; font-size: 15px;">{marquee_content}</marquee>
    </div>
    """, unsafe_allow_html=True)
 
    for u in daftar_ulasan[:5]:
        if u.get("Komentar", ""): 
            st.markdown(f"""
            <div class="ulasan-box">
                <span style="color: #FFD700; font-size: 12px;">{u.get("Rating", "⭐⭐⭐⭐⭐")}</span><br>
                <b>{u.get("Nama", "Jiwa Kosmik")}</b><br>
                <i style="color: #ccc;">"{u.get("Komentar", "")}"</i>
            </div>
            """, unsafe_allow_html=True)
else:
    st.caption("<center>Belum ada ulasan terbaru.</center>", unsafe_allow_html=True)
 
with st.expander("💬 Bagikan Pengalaman Anda"):
    with st.form("form_review"):
        rn = st.text_input("Nama")
        rr = st.radio("Rating Bintang", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"], horizontal=True)
        rk = st.text_area("Ulasan (Gimana akurasinya?)")
        if st.form_submit_button("Kirim Ulasan") and rn and rk:
            if kirim_ulasan(rn, rr, rk): 
                st.success("Terkirim! Testimoni Anda akan muncul setelah refresh.")
                time.sleep(1)
                st.rerun()
 
st.markdown("---")
st.markdown("<center><b>Ahmad Septian Dwi Cahyo</b><br><small>Certified NLP Trainer & Professional Hypnotherapist © 2026</small></center>", unsafe_allow_html=True)
