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
        font-weight: 800 !important; border: none !important;
        padding: 12px 24px !important; border-radius: 8px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
        box-shadow: 0 4px 10px rgba(255,215,0,0.3);
    }
    div.stButton > button:hover { transform: scale(1.02); background-color: #FFC107 !important; }
    
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
        background-color: #1e1e1e; padding: 15px; border-radius: 8px;
        border-left: 4px solid #FFD700; margin-bottom: 12px; font-size: 14px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .cosmic-box {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a4a 100%);
        padding: 20px; border-radius: 12px; border: 1px solid #4a4a8a;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6); margin-bottom: 15px;
    }
    
    .primbon-box {
        background: linear-gradient(135deg, #2b1b05 0%, #4a3000 100%);
        padding: 20px; border-radius: 12px; border: 1px solid #D4AF37;
        box-shadow: 0 8px 20px rgba(212,175,55,0.2); margin-top: 20px; margin-bottom: 20px;
    }
    
    .matrix-container {
        display: flex; justify-content: space-between; gap: 8px; flex-wrap: wrap;
        padding: 12px; background-color: #101010; border-radius: 10px;
        border: 1px solid #333; margin-bottom: 20px;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
    }
    .matrix-item { flex: 1; min-width: 80px; text-align: center; padding: 5px; border-right: 1px solid #333; }
    .matrix-item:last-child { border-right: none; }
    .matrix-label { font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .matrix-value { font-size: 16px; font-weight: 900; color: white; }
    .matrix-value-special { color: #FFD700; }
    
    .list-punchy { padding-left: 20px; margin-bottom: 15px; font-size: 15px; }
    .list-punchy li { margin-bottom: 8px; }
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
    st.caption("© 2026 Neuro Nada Academy")

# --- INTERFACE UTAMA ---
if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass

st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900;'>🌌 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #D4AF37; margin-bottom:0;'>Meretas Realita Melalui Kode Sandi Alam Bawah Sadar</p>", unsafe_allow_html=True)
st.markdown("---")

tgl_today = datetime.date.today()

# --- DATABASE ARKETIPE NLP ---
arketipe_punchy = {
    1: {"inti": "Sang Perintis yang lahir untuk memimpin, benci didikte, dan selalu fokus pada tujuan masa depan.", "kekuatan": ["Daya dobrak tinggi & berani ambil risiko", "Mandiri secara absolut", "Fokus eksekusi (Outcome-oriented)"]},
    2: {"inti": "Sang Penyelaras yang menjadi lem perekat hubungan, sangat peka membaca emosi lingkungan sekitar.", "kekuatan": ["Kapasitas empati level tinggi", "Negosiator & pencipta harmoni ulung", "Kemampuan adaptasi emosional (Rapport)"]},
    3: {"inti": "Sang Visioner dengan pikiran bak kembang api; kaya ide, ekspresif, dan magnetis dalam pergaulan.", "kekuatan": ["Komunikasi memikat (Persuasif)", "Kreativitas & imajinasi tanpa batas", "Ahli mencairkan suasana beku"]},
    4: {"inti": "Sang Transformator yang bertumpu pada struktur, detail, dan keteraturan hidup yang logis.", "kekuatan": ["Pola pikir sangat terstruktur & rapi", "Pekerja keras yang bisa diandalkan 100%", "Ketelitian tingkat dewa (Prosedural)"]},
    5: {"inti": "Sang Penggerak yang memuja kebebasan, haus petualangan, dan tercepat beradaptasi dengan perubahan.", "kekuatan": ["Kelincahan berpikir (Agility)", "Inovator & pemecah kebuntuan", "Keberanian mengeksplorasi hal baru"]},
    6: {"inti": "Sang Harmonizer yang menjadi pelindung natural, rela berkorban demi merawat lingkaran terdekatnya.", "kekuatan": ["Insting pengayom yang luar biasa", "Tanggung jawab moral level tinggi", "Loyalitas & dedikasi tanpa pamrih"]},
    7: {"inti": "Sang Legacy Builder yang haus kebenaran, pemikir mendalam, dan memiliki intuisi spiritual tajam.", "kekuatan": ["Kemampuan analisa (Deep Structure)", "Intuisi & firasat yang sering akurat", "Sangat selektif menilai kualitas"]},
    8: {"inti": "Sang Sovereign dengan visi kerajaan. Eksekutor ulung yang memancarkan otoritas dan kelimpahan materi.", "kekuatan": ["Tahan banting terhadap tekanan mental", "Insting bisnis & strategi tajam", "Kemampuan memegang kendali (Leader)"]},
    9: {"inti": "Sang Kesadaran Tinggi (Old Soul) yang memandang dunia secara holistik dengan idealisme luhur.", "kekuatan": ["Kebijaksanaan & pemikiran luas", "Kepedulian universal (Humanisme)", "Mampu melihat 'Big Picture' kehidupan"]}
}

arketipe_deskripsi = {
    1: "Anda lahir untuk memimpin dan membuka jalan. Arketipe ini memiliki dorongan internal yang kuat untuk mandiri dan benci jika harus didikte.",
    2: "Anda adalah lem perekat dalam setiap hubungan. Bakat Anda adalah mendengarkan dan menciptakan harmoni.",
    3: "Anda adalah pembawa pesan dan inspirasi. Pikiran Anda bekerja seperti kembang api; penuh warna dan ide kreatif.",
    4: "Anda adalah pembangun sistem. Keamanan, keteraturan, dan detail adalah nafas Anda.",
    5: "Anda adalah simbol kebebasan dan adaptasi. Arketipe ini haus akan pengalaman baru dan petualangan.",
    6: "Anda adalah pengayom sejati. Fokus hidup Anda adalah melayani dan merawat orang-orang yang Anda cintai.",
    7: "Anda adalah pencari kebenaran dan makna terdalam. Pikiran Anda sangat tajam dan intuitif.",
    8: "Anda adalah figur otoritas dan kelimpahan. Arketipe ini memiliki visi besar untuk membangun kerajaan finansial atau pengaruh sosial.",
    9: "Anda adalah jiwa tua yang bijaksana. Anda peduli pada kemanusiaan dan cinta universal."
}

closing_brutal_dinamis = {
    1: ["Overthinking karena merasa hasil belum sempurna", "Gengsi minta tolong saat memikul beban sendirian", "Membangun tembok ego untuk menutupi rasa sepi"],
    2: ["Mengorbankan kebahagiaan diri demi ekspektasi orang lain", "Sulit berkata TIDAK yang berujung kelelahan mental", "Memendam amarah dalam hati demi menghindari konflik"],
    3: ["Menyembunyikan gelisah batin di balik topeng senyuman", "Cepat kehilangan motivasi jika rutinitas membosankan", "Insomnia karena pikiran terlalu berisik dan over-analisa"],
    4: ["Stres parah jika rencana mendadak berubah di luar kendali", "Terjebak di zona nyaman karena takut ambil resiko baru", "Sering dinilai terlalu dingin atau kaku oleh pasangan"],
    5: ["Sindrom Cepat Bosan yang mensabotase karya dan hubungan", "Kelelahan saraf karena otak tak pernah diizinkan istirahat", "Merasa hampa karena kehilangan pijakan komitmen"],
    6: ["Burnout ekstrim karena sibuk mengurus hidup orang lain", "Sikap Over-Protective yang diam-diam mengekang", "Rasa bersalah luar biasa jika memakai waktu untuk diri sendiri"],
    7: ["Menganalisa terus tanpa aksi nyata (Paralysis by Analysis)", "Merasa terasing karena merasa tak ada yang sepemikiran", "Mencurigai niat baik orang akibat luka masa lalu"],
    8: ["Merasa hampa dan kosong di saat mencapai puncak sukses", "Sangat sulit melepaskan kontrol dan memaafkan", "Memaksa tubuh bekerja dan mengabaikan alarm lelah"],
    9: ["Sering memaklumi orang toxic atas nama kasihan", "Patah hati hebat akibat ekspektasi berlebihan pada manusia", "Kelelahan batin memikirkan beban dunia yang bukan tanggung jawabnya"]
}

link_produk = {
    1: "http://lynk.id/neuronada/kj98l4zgzwdw/checkout", 2: "http://lynk.id/neuronada/6z23q03121lg/checkout",
    3: "http://lynk.id/neuronada/0rd6gr7nlzxp/checkout", 4: "http://lynk.id/neuronada/elp83loeyggg/checkout",
    5: "http://lynk.id/neuronada/wne9p4q1l3d9/checkout", 6: "http://lynk.id/neuronada/nm840y6nlo21/checkout",
    7: "http://lynk.id/neuronada/vv0797ll7g7o/checkout", 8: "http://lynk.id/neuronada/ropl1lm6rz8g/checkout",
    9: "http://lynk.id/neuronada/704ke23nzmgx/checkout"
}

# --- FUNGSI LOGIKA NUMERIK & FALAK ---
def get_arketipe(angka):
    arketipe_dict = {
        1: "The Leader", 2: "The Mediator", 3: "The Communicator", 
        4: "The Architect", 5: "The Explorer", 6: "The Nurturer", 
        7: "The Analyst", 8: "The Strategist", 9: "The Humanist"
    }
    return arketipe_dict.get(angka, "Pribadi Unik")

def hitung_angka(tanggal):
    total = sum(int(digit) for digit in tanggal.strftime("%d%m%Y"))
    while total > 9: total = sum(int(digit) for digit in str(total))
    return total

def hitung_nama_esoterik(nama):
    abjad_values = {
        'a': 1, 'b': 2, 'j': 3, 'd': 4, 'h': 5, 'w': 6, 'z': 7, 
        't': 9, 'y': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 
        's': 60, 'f': 80, 'q': 100, 'r': 200, 'c': 3, 'e': 5,
        'g': 1000, 'i': 10, 'o': 6, 'p': 80, 'u': 6, 'v': 6, 'x': 60
    }
    nama_clean = ''.join(filter(str.isalpha, nama.lower()))
    total = sum(abjad_values.get(huruf, 0) for huruf in nama_clean)
    return total if total > 0 else 1

def get_elemen_esoterik(nilai_jummal):
    mod = nilai_jummal % 4
    if mod == 0: mod = 4
    elemen = {1: "🔥 Api", 2: "🌍 Tanah", 3: "💨 Udara", 4: "💧 Air"}
    return elemen.get(mod, "Unknown")

def get_elemen_combo(e1, e2):
    e1_base = e1.split(" ")[1]
    e2_base = e2.split(" ")[1]
    pair = set([e1_base, e2_base])
    
    if len(pair) == 1: return "🔥 Sinergi Identik", "Sangat sepemikiran, namun rawan kebosanan atau benturan ego karena karakter yang sama persis."
    if pair == {"Api", "Udara"}: return "🌪️ Saling Menghidupkan", "Udara meniup Api makin besar. Ide dan eksekusi berjalan sangat dinamis dan progresif."
    if pair == {"Air", "Tanah"}: return "🌱 Kesuburan & Stabilitas", "Air menutrisi Tanah. Emosi yang mengalir saling melengkapi dengan realitas materi yang stabil. Sangat ideal."
    if pair == {"Api", "Air"}: return "⚔️ Benturan Keras", "Saling mematikan. Api benci diatur emosi (Air), Air merasa Api terlalu agresif. Butuh toleransi ego yang sangat besar."
    if pair == {"Api", "Tanah"}: return "🌋 Dinamika Vulkanik", "Tanah bisa meredam agresivitas Api. Hubungan cukup solid asalkan Api tidak membakar habis kesabaran Tanah."
    if pair == {"Udara", "Tanah"}: return "🏜️ Badai Debu", "Logika dan kebebasan (Udara) sering berbenturan dengan aturan dan realita (Tanah). Rawan cekcok urusan prinsip."
    if pair == {"Udara", "Air"}: return "🌊 Ombak Besar", "Fakta logika (Udara) vs Perasaan (Air). Sering terjadi miskomunikasi karena bahasa cinta (Love Language) yang sangat bertolak belakang."
    return "Sinkronisasi Unik", "Kombinasi elemen menciptakan dinamika yang tak terduga."

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
        7: "Lebu Katiup Angin", 8: "Lakuning Geni", 9: "Lakuning Angin", 10: "Pandito Mbangun Teki",
        11: "Macan Ketawan", 12: "Lakuning Kembang", 13: "Lakuning Lintang", 14: "Lakuning Rembulan",
        15: "Lakuning Srengenge", 16: "Lakuning Banyu", 17: "Lakuning Bumi", 18: "Paripurna"
    }
    mod_panca = neptu % 5
    if mod_panca == 0: mod_panca = 5
    pancasuda = {1: "Sri (Kemakmuran)", 2: "Lungguh (Tahta)", 3: "Gedhong (Kekayaan)", 4: "Loro (Ujian)", 5: "Pati (Rintangan)"}
    naga_dina = {
        "Minggu": "Timur (Kejayaan)", "Senin": "Selatan (Kejayaan)", "Selasa": "Barat (Kejayaan)", 
        "Rabu": "Utara (Kejayaan)", "Kamis": "Timur (Kejayaan)", "Jumat": "Selatan (Kejayaan)", "Sabtu": "Selatan (Kejayaan)"
    }
    return lakuning.get(neptu, "Anomali"), pancasuda.get(mod_panca), naga_dina.get(hari)

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

def get_birth_moon(date):
    epoch = datetime.date(2000, 1, 6)
    days = (date - epoch).days
    lunations = days / 29.53058867
    p = lunations % 1
    if p < 0.03 or p > 0.97: return "🌑 New Moon", "Kekuatan internal sangat tajam.", "Menyusun target besar.", "Mencari validasi."
    elif p < 0.22: return "🌒 Waxing Crescent", "Dorongan batin tinggi.", "Eksekusi konkrit.", "Pesimis bawaan."
    elif p < 0.28: return "🌓 First Quarter", "Karakter petarung.", "Risiko terukur.", "Ceroboh."
    elif p < 0.47: return "🌔 Waxing Gibbous", "Perfeksionis.", "Memperhatikan detail.", "Abaikan kritik."
    elif p < 0.53: return "🌕 Full Moon", "Gelombang otak puncak.", "Tampil publik.", "Keputusan emosional."
    elif p < 0.72: return "🌖 Waning Gibbous", "Mentor alami.", "Distribusi ilmu.", "Enggan adaptasi."
    elif p < 0.78: return "🌗 Last Quarter", "Berani amputasi toxic.", "Rekomposisi hidup.", "Simpan dendam."
    else: return "🌘 Waning Crescent", "Energi Healer.", "Rawat diri.", "Memaksakan tubuh."

def get_daily_dynamic_sync():
    today = datetime.date.today()
    epoch = datetime.date(2000, 1, 6)
    days = (today - epoch).days
    lunations = days / 29.53058867
    p = lunations % 1
    energy_score = int(math.sin(p * math.pi) * 100)
    
    if p < 0.03 or p > 0.97: k = "New Moon"
    elif p < 0.22: k = "Waxing Crescent"
    elif p < 0.28: k = "First Quarter"
    elif p < 0.47: k = "Waxing Gibbous"
    elif p < 0.53: k = "Full Moon"
    elif p < 0.72: k = "Waning Gibbous"
    elif p < 0.78: k = "Last Quarter"
    else: k = "Waning Crescent"
    
    daily_do = {"New Moon": "Reset niat", "Waxing Crescent": "Langkah pertama", "First Quarter": "Pecahkan rintangan", "Waxing Gibbous": "Sempurnakan detail", "Full Moon": "Networking", "Waning Gibbous": "Mentoring", "Last Quarter": "Detoks", "Waning Crescent": "Healing batin"}
    daily_dont = {"New Moon": "Grasa-grusu", "Waxing Crescent": "Prokrastinasi", "First Quarter": "Menyerah", "Waxing Gibbous": "Perfeksionis buta", "Full Moon": "Debat kusir", "Waning Gibbous": "Pelit ilmu", "Last Quarter": "Nostalgia toxic", "Waning Crescent": "Kerja lembur"}
    
    return f"{k}", f"Energi selaras dengan {k}", energy_score, daily_do[k], daily_dont[k]

# --- MENU TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Personal Identity", "👩‍❤️‍👨 Couple Sync", "🕸️ Audit Sistem Saraf"])

# ==========================================
# TAB 1: IDENTITAS KOSMIK & BETALJEMUR
# ==========================================
with tab1:
    st.subheader("Akses Blueprint Bawah Sadar Anda")
    nama_user = st.text_input("Nama Lengkap:", placeholder="Ketik nama asli Anda...", key="t1_nama")
    tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date(1995, 1, 1), min_value=datetime.date(1920, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")

    if st.button("Kalkulasi Blueprint (Mulai)"):
        if not nama_user or len(nama_user.strip()) < 3: 
            st.error("🚨 Mohon ketik nama lengkap untuk sinkronisasi vibrasi.")
        elif tgl_input == tgl_today: 
            st.error("🚨 Tanggal lahir tidak valid.")
        else:
            status_text = st.empty()
            status_text.markdown("⏳ *Mengekstraksi sandi Hisab Jummal & Kitab Betaljemur...*")
            time.sleep(1)
            status_text.empty()
            
            angka_hasil = hitung_angka(tgl_input)
            nilai_jummal = hitung_nama_esoterik(nama_user)
            elemen_dasar = get_elemen_esoterik(nilai_jummal)
            nep, hari, pasaran = get_neptu_weton(tgl_input)
            wet = f"{hari} {pasaran}"
            zod = get_zodiak(tgl_input)
            ark_n = get_arketipe(angka_hasil)
            
            n_laku, n_panca, arah_naga = get_betaljemur_data(nep, hari)
            today_phase, today_desc, today_energy, today_do, today_dont = get_daily_dynamic_sync()
            punchy = arketipe_punchy.get(angka_hasil)
            desk_ark = arketipe_deskripsi.get(angka_hasil)
            shadow = closing_brutal_dinamis.get(angka_hasil)
            
            st.snow()
            st.markdown(f"<h3 style='text-align:center;'>🌌 Blueprint Kosmik: {nama_user.upper()}</h3>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="matrix-container">
                <div class="matrix-item"><div class="matrix-label">Nilai Esoterik</div><div class="matrix-value matrix-value-special">{nilai_jummal}</div></div>
                <div class="matrix-item"><div class="matrix-label">Elemen Dasar</div><div class="matrix-value">{elemen_dasar}</div></div>
                <div class="matrix-item"><div class="matrix-label">Meta-Program</div><div class="matrix-value matrix-value-special">KODE {angka_hasil}</div></div>
                <div class="matrix-item"><div class="matrix-label">Filter Zodiak</div><div class="matrix-value">{zod}</div></div>
                <div class="matrix-item"><div class="matrix-label">Energi Weton</div><div class="matrix-value">{wet} ({nep})</div></div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="primbon-box">
                <div style="text-align:center; border-bottom:1px solid #D4AF37; padding-bottom:10px; margin-bottom:15px;">
                    <span style="color:#D4AF37; font-size:12px; font-weight:900; letter-spacing:2px;">📜 PETHIKAN KITAB BETALJEMUR ADAMMAKNA</span>
                </div>
                <div style="font-size:14px; line-height:1.6; margin-bottom: 10px;">
                    <span style="color:#aaa;">Sandi Pangarasan (Meta-Program Bawah Sadar):</span> <b style="color:#FFF;">{n_laku}</b><br>
                    <span style="color:#aaa;">Sandi Pancasuda (Potensi Roda Kehidupan):</span> <b style="color:#FFF;">{n_panca}</b><br>
                    <span style="color:#FFD700;">🧭 <b>NAGA DINA (Arah Energi Hari {hari}):</b> {arah_naga}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 👁️ Decode Kepribadian Inti")
            st.info(f"Sistem mengkalkulasi nama Anda menghasilkan Nilai Energi **{nilai_jummal}** yang berafiliasi dengan **{elemen_dasar}**. Saat dipadukan dengan Pangarasan **{n_laku}** dan zodiak **{zod}**, ini mengunci arketipe utama Anda:\n\n**IDENTITAS INTI:** {punchy['inti']}")
            
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

# ==========================================
# TAB 2: COUPLE SYNC (SUPERIOR APP + BEDAH ALGORITMA DINAMIS)
# ==========================================
with tab2:
    st.subheader("Superior Couple Sync 👩‍❤️‍👨")
    st.write("Sistem X-Ray hubungan tingkat tinggi memadukan Esoterik Nama, Astrologi, Primbon Betaljemur, dan Psikologi Bawah Sadar.")
    
    ca, cb = st.columns(2)
    with ca: 
        n1 = st.text_input("Nama Anda", key="n1")
        d1 = st.date_input("Lahir Anda", value=datetime.date(1995, 1, 1), min_value=datetime.date(1940, 1, 1), max_value=tgl_today, key="d1")
    with cb: 
        n2 = st.text_input("Nama Pasangan", key="n2")
        d2 = st.date_input("Lahir Pasangan", value=datetime.date(1995, 1, 1), min_value=datetime.date(1940, 1, 1), max_value=tgl_today, key="d2")
        
    if st.button("Jalankan Pemindaian Hubungan"):
        if n1 and n2:
            st.snow()
            
            # Ekstraksi Data Pihak 1
            zod1 = get_zodiak(d1); ne_1, hari1, pas1 = get_neptu_weton(d1)
            nj1 = hitung_nama_esoterik(n1); el1 = get_elemen_esoterik(nj1)
            laku1, panca1, _ = get_betaljemur_data(ne_1, hari1)
            
            # Ekstraksi Data Pihak 2
            zod2 = get_zodiak(d2); ne_2, hari2, pas2 = get_neptu_weton(d2)
            nj2 = hitung_nama_esoterik(n2); el2 = get_elemen_esoterik(nj2)
            laku2, panca2, _ = get_betaljemur_data(ne_2, hari2)
            
            # Komparasi Visual Identitas
            st.markdown("---")
            st.markdown(f"""
            <div style="display:flex; gap:10px; margin-bottom:20px; flex-wrap: wrap;">
                <div class="cosmic-box" style="flex:1; padding:15px; min-width: 280px;">
                    <h4 style="text-align:center; color:#D4AF37; margin-top:0; border-bottom:1px solid #4a4a8a; padding-bottom:8px;">{n1.upper()}</h4>
                    <div style="font-size:14px; line-height:1.8;">
                        <b>Nilai Esoterik:</b> {nj1} <br>
                        <b>Elemen Jiwa:</b> {el1}<br>
                        <b>Pangarasan:</b> {laku1}<br>
                        <b>Energi Weton:</b> {hari1} {pas1} (Neptu {ne_1})<br>
                        <b>Filter Zodiak:</b> {zod1}
                    </div>
                </div>
                <div class="cosmic-box" style="flex:1; padding:15px; min-width: 280px;">
                    <h4 style="text-align:center; color:#D4AF37; margin-top:0; border-bottom:1px solid #4a4a8a; padding-bottom:8px;">{n2.upper()}</h4>
                    <div style="font-size:14px; line-height:1.8;">
                        <b>Nilai Esoterik:</b> {nj2} <br>
                        <b>Elemen Jiwa:</b> {el2}<br>
                        <b>Pangarasan:</b> {laku2}<br>
                        <b>Energi Weton:</b> {hari2} {pas2} (Neptu {ne_2})<br>
                        <b>Filter Zodiak:</b> {zod2}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Lapis 1: Benturan Elemen Esoterik
            st.markdown("### 🧬 Lapis 1: Benturan Elemen Nama")
            el_judul, el_desk = get_elemen_combo(el1, el2)
            st.info(f"Menyatukan frekuensi nama **{el1}** dengan **{el2}** menciptakan resonansi:\n\n**{el_judul}**\n\n*{el_desk}*")
            
            # Lapis 2: Primbon Betaljemur Adammakna
            st.markdown("### 📜 Lapis 2: Resonansi Primbon (Siklus 8)")
            
            total_neptu = ne_1 + ne_2
            sisa_weton = total_neptu % 8
            sisa_tampil = 8 if sisa_weton == 0 else sisa_weton
            hasil_bagi = total_neptu // 8
            
            # DATABASE DINAMIS UNTUK HASIL WETON (3 Variasi per Angka)
            db_weton_dinamis = {
                1: [
                    ("💔 PEGAT (Ujian Ego)", "Terdapat perbedaan mendasar dalam cara memproses emosi dan dominasi ego.", "Turunkan ego. Gunakan teknik Pacing (menyelaraskan) sebelum berargumen.", "Mind-Reading (berharap pasangan peka tanpa diberi tahu) dan mengungkit masa lalu."),
                    ("💔 PEGAT (Benturan Kutub)", "Siklus ini menuntut kelonggaran hati. Ego kalian sering bertabrakan layaknya dua kutub magnet yang sama.", "Banyakin jeda nafas sebelum merespon kritikan pasangan.", "Menghakimi secara sepihak saat pasangan sedang butuh didengarkan."),
                    ("💔 PEGAT (Fase Gesekan)", "Rawan terjadi 'gesekan' karena ekspektasi yang tidak terucap namun dituntut untuk dipenuhi.", "Gunakan pola bahasa yang lembut (Softener) untuk meluluhkan pertahanan bawah sadarnya.", "Adu gengsi siapa yang harus minta maaf duluan setelah bertengkar.")
                ],
                2: [
                    ("👑 RATU (Kharisma & Harmoni)", "Penyatuan vibrasi ini memancarkan wibawa. Orang sekitar segan melihat kalian.", "Fokus pada apresiasi harian. Jadikan pasangan sebagai partner diskusi strategis.", "Terjebak pencitraan eksternal (terlihat sempurna di luar tapi rapuh saat berdua)."),
                    ("👑 RATU (Sinergi Otoritas)", "Aura kalian saling menguatkan. Saat bersama, kalian memancarkan kharisma yang membuat orang lain nyaman sekaligus segan.", "Jaga keterbukaan komunikasi dan jadikan dia penasihat utamamu.", "Terlalu fokus menjaga image di luar tapi lupa membangun kemesraan di dalam rumah."),
                    ("👑 RATU (Sovereign Link)", "Kombinasi ini melahirkan energi kepemimpinan. Kalian cocok membangun bisnis atau proyek bersama.", "Beri apresiasi tulus setiap hari, sekecil apapun usahanya.", "Merasa paling benar sendiri karena merasa posisi sudah 'di atas angin'.")
                ],
                3: [
                    ("💞 JODOH (Sinkronisasi Alami)", "Penerimaan bawah sadar luar biasa tinggi. Kalian seperti sudah saling mengenal lama.", "Ciptakan kejutan-kejutan spontan agar romansa tidak monoton.", "Terjebak di zona nyaman yang membosankan dan berhenti meng-upgrade diri."),
                    ("💞 JODOH (Magnetic Pull)", "Ada tarikan magnetis yang sangat natural. Alam bawah sadar kalian sudah saling mengunci.", "Eksplorasi tempat baru berdua agar memori kebersamaan terus ter-update.", "Terlena dengan rutinitas hambar yang pelan-pelan mematikan percikan asmara."),
                    ("💞 JODOH (Resonansi Pikiran)", "Frekuensi pikiran kalian berjalan di gelombang yang sama. Seringkali kalian memikirkan hal yang sama di waktu bersamaan.", "Perkuat visi masa depan bersama, karena fondasi kalian sudah sangat solid.", "Berhenti memberikan kejutan karena merasa sudah 'memiliki' seutuhnya.")
                ],
                4: [
                    ("🌱 TOPO (Ujian Bertumbuh)", "Awal hubungan butuh banyak kalibrasi, namun akan sangat solid jika melewati badai.", "Kuasai teknik Reframing (ubah sudut pandang) saat krisis melanda.", "Memaksakan standar nilai pribadi ke pasangan dan bersikap kaku."),
                    ("🌱 TOPO (Fase Tempaan)", "Fase awal penuh tantangan adaptasi, tapi jika kalian lulus, ikatan ini akan sekuat baja.", "Perbanyak sesi 'Deep Talk' untuk membedah isi kepala masing-masing tanpa menghakimi.", "Memaksakan pasangan berubah drastis sesuai dengan blueprint ideal di kepala Anda."),
                    ("🌱 TOPO (Evolusi Jiwa)", "Hubungan ini adalah 'guru' bagi kalian berdua. Banyak air mata dan tawa yang akan mendewasakan emosi.", "Terapkan kesabaran ekstra tinggi. Pahami bahwa dia punya ritme pertumbuhannya sendiri.", "Membesar-besarkan masalah sepele menjadi drama besar.")
                ],
                5: [
                    ("💰 TINARI (Magnet Rezeki)", "Vibrasi kalian jika disatukan akan menarik kelancaran finansial dan hoki.", "Bangun nilai spiritual bersama, kolaborasi dalam ide atau bisnis.", "Menjadikan materi atau uang sebagai satu-satunya perekat hubungan."),
                    ("💰 TINARI (Gerbang Kelimpahan)", "Penyatuan aura kalian membuka gerbang kelimpahan. Banyak jalan rezeki tak terduga saat kalian bersatu.", "Buat rekening bersama atau proyek investasi yang dikelola berdua.", "Menghitung-hitung pengorbanan materi dan saling perhitungan soal uang."),
                    ("💰 TINARI (Hoki Sinergi)", "Energi rumah tangga kalian memancarkan daya tarik hoki. Sangat cocok jadi partner bisnis.", "Bersedekah atas nama bersama untuk melipatgandakan energi magnetis kalian.", "Terjebak gaya hidup hedon karena merasa rezeki mengalir gampang.")
                ],
                6: [
                    ("⚡ PADU (Beda Frekuensi)", "Sering terjadi letupan perdebatan karena beda cara filter informasi di otak.", "Validasi emosinya lebih dulu sebelum membantah logikanya (Teknik Yes-Set).", "Konfrontasi langsung saat emosi sedang tinggi (Baterai Emosi sedang merah)."),
                    ("⚡ PADU (Miskomunikasi Logika)", "Filter pikiran (Metaprogram) kalian cukup berseberangan, sehingga komunikasi sering salah tangkap (Miskom).", "Kalau dia mulai naik pitam, diam dulu. Jangan membalas api dengan api.", "Menggunakan kata-kata kasar yang bisa merusak jangkaran (anchor) positif di otaknya."),
                    ("⚡ PADU (Dinamika Berisik)", "Dinamika hubungan yang 'berisik'. Banyak perdebatan kecil yang sebenarnya cuma masalah beda sudut pandang.", "Sering-sering pelukan (Physical Touch) untuk meredakan ketegangan sistem saraf.", "Berdebat panjang lebar via chat teks yang sangat rawan disalahartikan nadanya.")
                ],
                7: [
                    ("👁️ SUJANAN (Rawan Asumsi)", "Ada kecenderungan muncul rasa insecure, cemburu, atau salah paham mendadak.", "Buka komunikasi transparan, bicarakan sesuatu murni berdasarkan fakta.", "Menggunakan bahasa generalisasi ('Kamu selalu begini', 'Kamu gapernah gitu')."),
                    ("👁️ SUJANAN (Ilusi Pikiran)", "Bayangan masa lalu atau rasa insecure seringkali muncul dan menyabotase kedamaian hubungan ini.", "Klarifikasi langsung jika ada yang janggal, jangan dipendam jadi asumsi.", "Mengecek HP pasangan diam-diam atau cemburu buta tanpa bukti valid."),
                    ("👁️ SUJANAN (Distorsi Kognitif)", "Pola pikiran kalian rawan terjebak distorsi kognitif (membaca pikiran pasangan secara negatif).", "Bangun Trust secara konsisten dengan menepati janji-janji kecil.", "Bermain playing victim untuk mendapatkan perhatian.")
                ],
                8: [
                    ("🕊️ PESTHI (Damai & Rukun)", "Hubungan yang stabil, adem ayem, dan jauh dari drama penguras energi mental.", "Rutin mencari aktivitas, liburan, atau hobi baru bersama.", "Saking damainya bisa terasa hambar, jangan biarkan api asmara padam begitu saja."),
                    ("🕊️ PESTHI (Air Tenang)", "Siklus air tenang. Hubungan kalian berjalan harmonis, stabil, dan jauh dari prahara besar.", "Agendakan 'Date Night' rutin setiap bulan untuk menjaga romantisme.", "Terlalu pasif dan membiarkan urusan asmara berjalan autopilot."),
                    ("🕊️ PESTHI (Gelombang Alpha)", "Gelombang otak kalian berada pada fase Alpha saat bersama. Sangat rileks dan menenangkan.", "Kembangkan hobi bersama yang menstimulasi adrenalin biar nggak bosan.", "Menganggap remeh hal-hal kecil karena merasa hubungan sudah pasti aman.")
                ]
            }
            
            # Pilihan fallback jika key tidak ditemukan
            fallback_data = [("Analisa Unik", "Butuh kalibrasi", "Perbaiki komunikasi", "Jangan egois")]
            
            # Pemilihan acak dari database variasi (DINAMIS)
            judul_weton, desk_weton, saran_do, saran_dont = random.choice(db_weton_dinamis.get(sisa_tampil, fallback_data))
            
            # ---- UI BOX: BEDAH ALGORITMA KESERUAN BARU ----
            st.markdown(f"""
            <div style="background: linear-gradient(180deg, #111 0%, #000 100%); border: 1px solid #D4AF37; padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: center; box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.2);">
                <p style="color: #888; font-size: 12px; font-weight: bold; letter-spacing: 2px; margin-bottom: 5px;">LIVE CALCULATION: ENGINE BETALJEMUR</p>
                <div style="display: flex; justify-content: center; align-items: center; gap: 15px; margin-bottom: 15px;">
                    <div style="font-size: 18px; color: #FFF;">Neptu {n1.split()[0]}<br><span style="color: #D4AF37; font-size: 24px; font-weight: bold;">{ne_1}</span></div>
                    <div style="font-size: 24px; font-weight: bold; color: #FF4B4B;">+</div>
                    <div style="font-size: 18px; color: #FFF;">Neptu {n2.split()[0]}<br><span style="color: #D4AF37; font-size: 24px; font-weight: bold;">{ne_2}</span></div>
                    <div style="font-size: 24px; font-weight: bold; color: #FF4B4B;">=</div>
                    <div style="font-size: 18px; color: #FFF;">Total Fusi<br><span style="color: #25D366; font-size: 24px; font-weight: bold;">{total_neptu}</span></div>
                </div>
                <div style="background-color: #222; padding: 10px; border-radius: 8px; border-left: 4px solid #FF4B4B; text-align: left;">
                    <span style="color: #FFF; font-size: 14px;">Menurut hukum <b>Salaki Rabi</b>, rotasi semesta berputar dalam 8 fase. Kita ekstrak energi kalian:</span><br>
                    <code style="font-size: 16px; color: #FFD700; background: none;">{total_neptu} ÷ 8 = {hasil_bagi} sisa <b style="font-size: 20px;">{sisa_tampil}</b></code>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success(f"Karena perhitungan jatuh pada angka sisa **{sisa_tampil}**, maka alam bawah sadar hubungan kalian otomatis terkunci di frekuensi:\n\n**{judul_weton}**\n\n*{desk_weton}*")
            
            # Lapis 3: Skor NLP Meta-Program
            st.markdown("### 🧠 Lapis 3: Skor Meta-Program (Kecerdasan Komunikasi)")
            sel = abs(hitung_angka(d1) - hitung_angka(d2))
            if sel in [0, 3, 6, 9]: st.warning("💘 **SKOR NLP: 90% (Sangat Sinkron)** - Sangat mudah memahami *Love Language* satu sama lain tanpa banyak bicara.")
            elif sel in [1, 2, 8]: st.warning("⚖️ **SKOR NLP: 70% (Dinamis)** - Banyak beda sudut pandang, butuh kedewasaan untuk saling melengkapi.")
            else: st.error("🔥 **SKOR NLP: 50% (Rawan Gesekan)** - Ego tinggi sering berbenturan keras. Butuh teknik komunikasi bawah sadar khusus.")

            # Panduan
            st.markdown("<br>", unsafe_allow_html=True)
            c_do_c, c_dont_c = st.columns(2)
            with c_do_c: st.success(f"✅ **LAKUKAN INI:**\n\n{saran_do}")
            with c_dont_c: st.error(f"❌ **HINDARI INI:**\n\n{saran_dont}")

# ==========================================
# TAB 3: AUDIT SISTEM SARAF
# ==========================================
with tab3:
    st.subheader("🕸️ Audit Sistem Saraf (Wheel of Life)")
    st.info("**Apa itu Audit Sistem Saraf?**\n\nEnergi manusia mengalir layaknya jaring. Geser *slider* sejujur-jujurnya untuk melihat kebocoran energi Anda saat ini.")

    kategori_label = ['Kesehatan Mental', 'Karir & Finansial', 'Asmara', 'Spiritual', 'Fisik']
    sk = [st.slider(k, 1, 10, 5) for k in kategori_label]
    
    if st.button("Mulai Audit Radar"):
        fig = go.Figure(data=go.Scatterpolar(
            r=sk+[sk[0]], theta=['Mental','Karir','Asmara','Spiritual','Fisik','Mental'], 
            fill='toself', fillcolor='rgba(212, 175, 55, 0.4)', line=dict(color='#D4AF37')
        ))
        st.plotly_chart(fig)
        
        avg = sum(sk)/5
        if avg < 5: st.error("🚨 **KONDISI KRITIS (ALARM BERBUNYI)**\n\nSistem saraf Anda sedang kelelahan parah. Anda butuh 'Detoks Mental' secepatnya sebelum berujung pada psikosomatis.")
        elif avg < 8: st.warning("🟡 **ZONA NYAMAN YANG MENIPU**\n\nSistem mendeteksi Anda memendam potensi besar yang tertahan. Selesaikan area terlemah Anda, dan lihat keajaiban terjadi.")
        else: st.success("🔥 **PEAK STATE (GELOMBANG EMAS)**\n\nSinkronisasi otak dan tindakan Anda sangat sempurna. Ini momentum terbaik mengeksekusi visi Anda!")

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
