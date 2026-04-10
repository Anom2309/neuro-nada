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
 
# --- CUSTOM CSS ---
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
        text-transform: uppercase; letter-spacing: 1px; transition: 0.3s;
    }
    .cta-button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(255, 75, 75, 0.6); }
 
    .ulasan-box {
        background: rgba(30, 30, 30, 0.6); backdrop-filter: blur(10px);
        padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700; 
        margin-bottom: 12px; font-size: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .glass-container {
        background: rgba(25, 25, 25, 0.5); backdrop-filter: blur(12px);
        padding: 20px; border-radius: 12px; border: 1px solid rgba(212,175,55,0.2);
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.4); margin-bottom: 15px;
    }
    
    .primbon-box {
        background: linear-gradient(135deg, rgba(43,27,5,0.8) 0%, rgba(74,48,0,0.8) 100%);
        backdrop-filter: blur(10px); padding: 25px; border-radius: 12px; 
        border: 1px solid #D4AF37; box-shadow: 0 8px 25px rgba(212,175,55,0.3); 
        margin-top: 20px; margin-bottom: 20px;
    }

    .dynamic-reading-box {
        background: rgba(20, 20, 20, 0.7); backdrop-filter: blur(5px);
        padding: 20px; border-radius: 12px; border-left: 5px solid #FFD700;
        margin-top: 15px; margin-bottom: 15px; font-size: 15px; line-height: 1.6;
    }
    
    .matrix-container {
        display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap;
        padding: 15px; background: rgba(10,10,10,0.8); border-radius: 10px;
        border: 1px solid #333; margin-bottom: 5px; box-shadow: inset 0 2px 15px rgba(0,0,0,0.6);
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

    .info-metric-box {
        background: rgba(255,215,0,0.05); border: 1px solid rgba(255,215,0,0.2);
        padding: 15px; border-radius: 8px; font-size: 13px; color: #ccc;
        margin-bottom: 20px; line-height: 1.5;
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
    return planets[datetime.datetime.now().hour % 7]
 
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

KAMUS_ABJAD = {
    'a': 1, 'b': 2, 'j': 3, 'd': 4, 'h': 5, 'w': 6, 'z': 7, 
    't': 9, 'y': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 
    's': 60, 'f': 80, 'q': 100, 'r': 200, 'c': 3, 'e': 5,
    'g': 1000, 'i': 10, 'o': 6, 'p': 80, 'u': 6, 'v': 6, 'x': 60
}

# --- ERROR-PROOF FUNCTIONS ---
def hitung_nama_esoterik(nama):
    nama_clean = ''.join(filter(str.isalpha, str(nama).lower()))
    total = sum(KAMUS_ABJAD.get(huruf, 0) for huruf in nama_clean)
    return total if total > 0 else 1

def get_rincian_esoterik(nama):
    nama_clean = ''.join(filter(str.isalpha, str(nama).lower()))
    rincian = []
    for huruf in nama_clean:
        nilai = KAMUS_ABJAD.get(huruf, 0)
        if nilai > 0: rincian.append(f"{huruf.upper()}({nilai})")
    return " + ".join(rincian) if rincian else "0"

def generate_dynamic_reading(total_jummal):
    mod = total_jummal % 4 if total_jummal % 4 != 0 else 4
    elemen_dict = {
        1: ("🔥 API (Nar)", "Sistem saraf Anda didesain untuk eksekusi cepat. Anda adalah inisiator. Anda tidak betah pada penundaan. Namun, waspadai ego yang terlalu dominan."),
        2: ("🌍 TANAH (Turab)", "Anda adalah fondasi. Sistem pikiran Anda praktis, sangat logis, dan membumi. Waspadai kekakuan pola pikir jika ada perubahan mendadak di hidup Anda."),
        3: ("💨 UDARA (Hawa)", "Anda adalah Sang Komunikator & Konseptor. Otak Anda memproduksi ide tanpa henti. Karena udara tak bisa digenggam, waspadai energi saraf yang gampang *burnout* akibat *Overthinking*."),
        4: ("💧 AIR (Ma')", "Sistem emosional Anda paling peka. Anda punya empati tinggi untuk beradaptasi dan membaca perasaan orang lain. Waspadai menyerap toxic dari lingkungan luar.")
    }
    el_nama, el_desc = elemen_dict.get(mod, ("Anomali", "Karakter tidak terdefinisi"))

    str_jummal = str(total_jummal)
    proses_reduksi = " + ".join(list(str_jummal))
    sum_reduksi = sum(int(d) for d in str_jummal) if str_jummal.isdigit() else 1
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

    return el_nama, el_desc, proses_reduksi, sum_reduksi, root_num, root_dict.get(root_num, "Anomali"), master_note

def hitung_angka(tanggal):
    try:
        total = sum(int(digit) for digit in tanggal.strftime("%d%m%Y"))
        while total > 9: total = sum(int(digit) for digit in str(total))
        return total
    except:
        return 1

def get_rincian_tanggal(tanggal):
    try:
        tgl_str = tanggal.strftime("%d%m%Y")
        rincian_awal = " + ".join(list(tgl_str))
        total = sum(int(digit) for digit in tgl_str)
        proses = f"{rincian_awal} = {total}"
        while total > 9:
            rincian_lanjut = " + ".join(list(str(total)))
            total = sum(int(digit) for digit in str(total))
            proses += f" ➡ {rincian_lanjut} = {total}"
        return proses
    except:
        return "1 = 1"
 
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
    return lakuning.get(neptu, ("Anomali", "Karakter kompleks"))[0], lakuning.get(neptu, ("Anomali", "Karakter kompleks"))[1], pancasuda.get(mod_panca, ("Anomali", "Karakter kompleks"))[0], pancasuda.get(mod_panca, ("Anomali", "Karakter kompleks"))[1], naga_dina.get(hari, "Arah Netral")
 
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

def get_safe_firstname(name_str, default="User"):
    stripped = str(name_str).strip()
    return stripped.split()[0].upper() if stripped else default
 
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
            st.error("🚨 Mohon ketik nama lengkap Anda (minimal 3 huruf) untuk sinkronisasi vibrasi.")
        elif tgl_input == tgl_today: 
            st.error("🚨 Tanggal lahir tidak valid. Silakan pilih tanggal lahir Anda yang sebenarnya.")
        else:
            try:
                status_text = st.empty()
                status_text.markdown("⏳ *Mengekstraksi sandi Hisab Jummal (Ilmu Huruf)...*")
                time.sleep(0.5)
                status_text.markdown("⏳ *Membuka segel Kitab Betaljemur Adammakna...*")
                time.sleep(0.5)
                status_text.empty()
                
                safe_name = get_safe_firstname(nama_user)
                angka_hasil = hitung_angka(tgl_input)
                rincian_tgl = get_rincian_tanggal(tgl_input)
                
                nilai_jummal = hitung_nama_esoterik(nama_user)
                rincian_jummal = get_rincian_esoterik(nama_user)
                
                el_nama, el_desc, p_reduk, s_reduk, r_num, r_desc, m_note = generate_dynamic_reading(nilai_jummal)
                
                nep, hari, pasaran = get_neptu_weton(tgl_input)
                wet = f"{hari} {pasaran}"
                zod = get_zodiak(tgl_input)
                
                n_laku, d_laku, n_panca, d_panca, arah_naga = get_betaljemur_data(nep, hari)
                
                punchy = arketipe_punchy.get(angka_hasil, arketipe_punchy[1])
                desk_ark = arketipe_deskripsi.get(angka_hasil, "Karakter Anda sangat kompleks dan unik.")
                shadow = closing_brutal_dinamis.get(angka_hasil, ["Overthinking", "Menyembunyikan gelisah", "Sering memendam masalah"])
                
                st.snow()
                st.markdown(f"<h3 style='text-align:center;'>🌌 Blueprint Kosmik: {safe_name}</h3>", unsafe_allow_html=True)
                
# MULAI DARI SINI SEMUA HTML RATA KIRI AGAR TIDAK JADI MARKDOWN CODE BLOCK
                st.markdown(f"""
<div class="matrix-container">
<div class="matrix-item"><div class="matrix-label">Nilai Esoterik</div><div class="matrix-value matrix-value-special">{nilai_jummal}</div></div>
<div class="matrix-item"><div class="matrix-label">Elemen Dasar</div><div class="matrix-value">{el_nama.split(' ')[1] if len(el_nama.split(' '))>1 else el_nama}</div></div>
<div class="matrix-item"><div class="matrix-label">Meta-Program</div><div class="matrix-value matrix-value-special">KODE {angka_hasil}</div></div>
<div class="matrix-item"><div class="matrix-label">Filter Zodiak</div><div class="matrix-value">{zod}</div></div>
<div class="matrix-item"><div class="matrix-label">Energi Weton</div><div class="matrix-value">{wet} (Neptu {nep})</div></div>
</div>
""", unsafe_allow_html=True)
                
                st.markdown(f"""
<div class="dynamic-reading-box">
<h4 style="color: #FFD700; margin-top:0;">🔍 Bedah DNA Angka & Waktu Lahir</h4>
<p><b>1. Sandi Esoterik Nama (Hisab Jummal)</b><br>
Secara arsitektur Gematria Kuno, total nilai getaran resonansi dari aksara nama Anda:<br>
<code style="color:#25D366; background:transparent; padding:0;">{rincian_jummal} = <b>{nilai_jummal}</b></code></p>
<ol style="margin-left: -15px; margin-bottom: 20px;">
<li><b>Elemen Bawah Sadar:</b> Nilai {nilai_jummal} direduksi menjadi 4 pilar alam semesta, Anda berafiliasi dengan <b>{el_nama}</b>.<br><i style="color:#aaa;">{el_desc}</i></li>
<li><b>Inti Jiwa (Root Number):</b> {p_reduk} = {s_reduk} ➡ <b>{r_num}</b>.<br>Angka {r_num} adalah sandi bahwa secara sadar/bawah sadar Anda adalah: <b>{r_desc}</b></li>
</ol>
<p><b>2. Sandi Waktu Lahir (Meta-Program NLP)</b><br>
Kalkulasi penyederhanaan (reduksi matriks) dari tanggal lahir Anda ({tgl_input.strftime('%d-%m-%Y')}):<br>
<code style="color:#FFD700; background:transparent; padding:0;">{rincian_tgl}</code><br>
<span style="font-size:14px; color:#ccc;">Maka didapatkan <b>KODE {angka_hasil}</b>. Angka ini adalah <i>Blueprint</i> cara otak Anda memproses informasi, mengambil keputusan, dan bereaksi terhadap tekanan.</span></p>
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
                st.info(f"Berdasarkan **KODE {angka_hasil}**, sistem mengkunci arketipe utama Anda:\n\n**IDENTITAS INTI:** {punchy['inti']}")
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
<div class="cta-button">⚠️ BONGKAR MENTAL BLOCK KODE {angka_hasil} & REBUT KENDALI HIDUP ANDA</div>
</a>
""", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Sistem gagal melakukan komputasi. Harap periksa kembali ejaan nama Anda. (Error Code: {e})")
 
# ==========================================
# TAB 2: COUPLE MATRIX (ULTIMATE UPGRADE)
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
        if str(n1).strip() and str(n2).strip():
            try:
                st.snow()
                safe_n1 = get_safe_firstname(n1, "P1")
                safe_n2 = get_safe_firstname(n2, "P2")
                
                zod1 = get_zodiak(d1); ne_1, _, _ = get_neptu_weton(d1)
                zod2 = get_zodiak(d2); ne_2, _, _ = get_neptu_weton(d2)
                sel = abs(hitung_angka(d1) - hitung_angka(d2))
                sisa_weton = (ne_1 + ne_2) % 8
                
                jummal_1 = hitung_nama_esoterik(n1)
                jummal_2 = hitung_nama_esoterik(n2)
                total_couple = jummal_1 + jummal_2
                
                root_c = total_couple
                while root_c > 9: root_c = sum(int(d) for d in str(root_c))
                
                # DATABASE PERSONA PASANGAN (SANGAT DETAIL)
                couple_persona = {
                    1: ("THE POWER COUPLE", "Angka 1 adalah simbol Alpha dan Dominasi. Ketika vibrasi kalian berdua disatukan, kalian membentuk entitas yang mandiri, berwibawa, dan punya daya dobrak besar. Jika kalian punya satu target bersama (bisnis atau aset), semesta seolah membuka jalan karena fokus kalian luar biasa."),
                    2: ("THE SOULMATES", "Angka 2 adalah energi keharmonisan. Kalian berdua memiliki ibarat 'Wi-Fi' batin yang otomatis terhubung tanpa *password*. Sangat mudah memahami perasaan satu sama lain tanpa harus banyak bicara. Empati adalah perekat utama kalian."),
                    3: ("THE SOCIALITES", "Angka 3 membawa energi ekspresif dan magnetis. Kalian adalah pasangan yang ceria, penuh ide spontan, dan biasanya asyik diajak ngobrol. Aura hubungan ini sangat disukai oleh lingkaran pergaulan kalian yang luas."),
                    4: ("THE BUILDERS", "Angka 4 adalah fondasi murni. Hubungan kalian sangat solid, praktis, dan logis. Fokus utama persatuan ini adalah membangun keamanan masa depan, merapikan finansial, dan menjaga kesetiaan jangka panjang tanpa banyak drama."),
                    5: ("THE ADVENTURERS", "Angka 5 benci rutinitas. Hubungan kalian dipenuhi energi kebebasan dan petualangan. Kalian anti-monoton, suka tantangan, dan hubungan ini selalu dipenuhi kejutan atau perubahan tak terduga."),
                    6: ("THE FAMILY FIRST", "Angka 6 adalah simbol pengayoman sejati. Tingkat pengorbanan dan dedikasi kalian untuk membangun rumah tangga, merawat anak, dan menjaga kelestarian keluarga besar sungguh luar biasa. Rumah adalah segalanya."),
                    7: ("THE DEEP SEEKERS", "Angka 7 memancarkan aura eksklusif. Koneksi kalian tidak cuma sebatas fisik atau materi, tapi sangat dalam secara intelektual dan spiritual. Kalian cenderung lebih suka privasi tinggi dan *quality time* jauh dari keramaian."),
                    8: ("THE EMPIRE", "Angka 8 adalah magnet kelimpahan dan kontrol. Penyatuan ego kalian secara bawah sadar ditarik kuat menuju kesuksesan material, ekspansi bisnis, dan pencapaian status sosial yang lebih tinggi di masyarakat."),
                    9: ("THE HEALERS", "Angka 9 adalah puncak toleransi. Hubungan kalian dipenuhi keikhlasan yang dalam. Seringkali, ketenangan batin dari kalian berdua menjadikan rumah kalian sebagai tempat bersandar/curhat bagi orang-orang di sekitar.")
                }
                c_title, c_desc = couple_persona.get(root_c, ("Uncharted", "Kombinasi unik yang terus beradaptasi dengan waktu."))
                
                # DATABASE WETON KOMBO (DETAIL DO & DON'T)
                hasil_weton_kombo = {
                    1: ("💔 PEGAT (Ujian Ego)", "Sangat rawan terjadi adu argumen keras karena cara otak kalian memproses masalah dan emosi sangat bertolak belakang.", "Gunakan taktik **Pacing-Leading**: Validasi dulu perasaannya ('Aku paham kamu capek...') sebelum kamu mulai memberikan solusi atau argumen logismu.", "DILARANG KERAS melakukan *Mind-Reading* (menebak-nebak pikiran negatifnya sendiri) dan jangan pernah mengungkit kesalahan masa lalunya sebagai senjata."),
                    2: ("👑 RATU (Kharisma & Harmoni)", "Penyatuan ini memancarkan kharisma yang kuat. Orang lain dan keluarga besar sangat segan dan menghormati posisi kalian berdua.", "Jadikan pasangan sebagai **Partner Diskusi Strategis**. Berikan afirmasi positif setiap kali ia berhasil melakukan pencapaian sekecil apapun di luar rumah.", "Hindari jebakan *Pencitraan*. Jangan berpura-pura bahagia di luar hanya demi terlihat 'sempurna', tapi menyimpan bom waktu di dalam rumah."),
                    3: ("💞 JODOH (Sinkronisasi Alami)", "Kecocokan bawah sadar kalian berada di tingkat tertinggi. Penolakan ego sangat minim, ibarat kepingan *puzzle* yang langsung klik tanpa dipaksa.", "Ciptakan **Pattern Interrupt** (kejutan acak) secara rutin. Ajak kencan dadakan atau kasih kejutan kecil agar hubungan tetap *spark* dan tidak terasa hambar.", "Hati-hati dengan jebakan *Comfort Zone* (Zona Nyaman). Sangat sering pasangan berstatus Jodoh mengalami kemandekan karir karena sudah merasa terlalu santai dan malas berjuang lagi."),
                    4: ("🌱 TOPO (Ujian Bertumbuh)", "Fase awal hubungan ini akan penuh ujian adaptasi. Tapi jika kalian berhasil melewati kalibrasi ego ini, pondasi kalian tidak akan tertembus.", "Kuasai teknik **Reframing** (*Bingkai Ulang*). Saat ada masalah berat, paksa diri kalian berdua untuk mencari sudut pandang positif dari kejadian tersebut.", "Jangan pernah memaksakan *Map of the World* (standar kebenaran/gengsi pribadimu) kepada pasangan. Belajarlah menurunkan ekspektasi."),
                    5: ("💰 TINARI (Magnet Rezeki)", "Penyatuan ini adalah magnet rezeki. Pintu kelancaran finansial dan kemudahan urusan duniawi biasanya terbuka lebar setelah kalian bersatu.", "Sering-sering lakukan sesi *Goal Setting* (visi masa depan) berdua. Ketahuilah bahwa harmonisasi emosi di antara kalian adalah kunci utama keran rezeki itu terbuka.", "Jangan jadikan uang sebagai satu-satunya perekat hubungan kalian. Pastikan cinta kalian tetap utuh di saat kondisi dompet sedang diuji oleh semesta."),
                    6: ("⚡ PADU (Beda Frekuensi)", "Kalian akan sering mengalami letupan perdebatan sepele. Ini terjadi murni karena perbedaan filter otak kalian dalam mencerna informasi yang masuk.", "Berikan *Space* (ruang sendiri) saat tensi mulai naik. Gunakan teknik **Yes-Set** (buat dia mengatakan kata 'Ya' 3 kali) untuk menurunkan emosinya secara perlahan.", "Jangan pernah menyerang harga dirinya secara frontal saat *state* emosinya sedang di puncak. Jangan menggunakan nada tinggi untuk membalas."),
                    7: ("👁️ SUJANAN (Rawan Asumsi)", "Sangat rawan miskomunikasi, saling curiga, cemburu buta, atau salah paham dadakan yang diakibatkan oleh asumsi bawah sadar yang menumpuk.", "Biasakan komunikasi murni berbasis fakta objektif (*Sensory Based*), bukan sekadar 'katanya' atau 'aku merasa dia begitu'. Bicarakan apa yang terlihat dan terdengar saja.", "DILARANG memakai kata generalisasi absolut saat berantem, seperti: 'Kamu SELALU egois!' atau 'Kamu TIDAK PERNAH mengerti!'. Itu merusak alam bawah sadarnya."),
                    0: ("🕊️ PESTHI (Damai & Rukun)", "Hubungan kalian adem ayem, rukun, stabil, dan sangat minim drama yang menguras energi saraf. Kehadiran masing-masing menetralisir stres.", "Pertahankan *Rapport* batin dengan melakukan *Deep-Talk* rutin sebelum tidur. Sesekali jelajahi hobi baru bersama agar ada tantangan seru di hidup kalian.", "Waspadai sikap *Take it for granted* (menggampangkan pasangan). Jangan biarkan api asmara padam cuma karena kalian merasa dia tidak akan ke mana-mana.")
                }
                judul_weton, desk_weton, saran_do, saran_dont = hasil_weton_kombo.get(sisa_weton, ("Analisa Unik", "Butuh kalibrasi ego yang mendalam", "Perbaiki pola komunikasi", "Jangan memaksakan kehendak"))
                
                st.markdown("---")
                st.markdown(f"### 🔮 The Unified Resonance: {safe_n1} & {safe_n2}")
                
                st.markdown(f"""
<div class="matrix-container">
<div class="matrix-item"><div class="matrix-label">Vibrasi {safe_n1}</div><div class="matrix-value">{jummal_1}</div></div>
<div class="matrix-item"><div class="matrix-label">Vibrasi {safe_n2}</div><div class="matrix-value">{jummal_2}</div></div>
<div class="matrix-item" style="background: rgba(212,175,55,0.2);"><div class="matrix-label" style="color:#FFD700;">TOTAL ENERGI</div><div class="matrix-value matrix-value-special">{total_couple}</div></div>
<div class="matrix-item"><div class="matrix-label">Weton Kombo</div><div class="matrix-value">{sisa_weton}</div></div>
</div>
""", unsafe_allow_html=True)
                
                st.markdown("""
<div class="info-metric-box">
<b style="color:#FFD700; font-size:14px;">💡 PENJELASAN MATRIKS:</b><br>
• <b style="color:white;">TOTAL ENERGI:</b> Hasil penyatuan murni dari getaran Esoterik (Jummal) nama Anda berdua. Ibarat dua gelombang suara yang saling bertabrakan, 'Total Energi' menciptakan satu frekuensi baru. Angka inilah yang membentuk DNA atau <i>Persona Pasangan</i> kalian di mata semesta.<br>
• <b style="color:white;">WETON KOMBO:</b> Kalkulasi matematis siklus waktu lahir (Neptu Jawa). Weton Kombo menganalisis titik temu ego bawah sadar, memetakan rawan konflik (Shadow) dan potensi harmoni (Light) dalam memproses stimulus sehari-hari.
</div>
""", unsafe_allow_html=True)
                
                st.markdown(f"""
<div class="dynamic-reading-box" style="border-left-color: #25D366;">
<h4 style="color: #25D366; margin-top:0;">🧬 Persona Pasangan: {c_title}</h4>
<p>Ketika nilai esoterik <b>{jummal_1}</b> dan <b>{jummal_2}</b> disatukan menjadi <b>{total_couple}</b>, ia menghasilkan resonansi inti (root number) <b>{root_c}</b>.<br>
<i>{c_desc}</i></p>
</div>
""", unsafe_allow_html=True)
                
                st.markdown(f"#### 📜 Titik Benturan Weton: {judul_weton}")
                st.info(f"Menyatukan filter pikiran **{zod1}** dengan **{zod2}** ibarat menggabungkan dua elemen alam. Ditambah algoritma Primbon (Neptu {ne_1} disilang Neptu {ne_2}), menghasilkan takdir energi:\n\n{desk_weton}")
                
                if sel in [0, 3, 6, 9]: st.success("💘 **SKOR META-PROGRAM (NLP): 90% (Sangat Sinkron)** - Peta mental kalian sangat mirip.")
                elif sel in [1, 2, 8]: st.warning("⚖️ **SKOR META-PROGRAM (NLP): 70% (Dinamis)** - Butuh toleransi dalam mengambil keputusan.")
                else: st.error("🔥 **SKOR META-PROGRAM (NLP): 50% (Rawan Gesekan)** - Sering terjadi perbedaan sudut pandang.")
     
                st.markdown("<br>", unsafe_allow_html=True)
                c_do_c, c_dont_c = st.columns(2)
                with c_do_c: 
                    st.markdown(f"<div style='background:rgba(37,211,102,0.1); padding:20px; border-radius:10px; border:1px solid #25D366;'>✅ <b>LAKUKAN INI (NLP TACTICS):</b><br><br>{saran_do}</div>", unsafe_allow_html=True)
                with c_dont_c: 
                    st.markdown(f"<div style='background:rgba(255,75,75,0.1); padding:20px; border-radius:10px; border:1px solid #ff4b4b;'>❌ <b>HINDARI INI (FATAL ERRORS):</b><br><br>{saran_dont}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Sistem gagal membaca resonansi. Mohon ketik nama dengan benar. (Kode Error: {e})")
        else:
            st.warning("⚠️ Mohon isi kedua nama terlebih dahulu sebelum melakukan analisis.")
 
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
