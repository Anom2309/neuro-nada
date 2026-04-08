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
    
    .gate-box {
        background: rgba(10, 10, 42, 0.9); padding: 30px; border-radius: 15px; 
        border: 2px solid #D4AF37; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        margin-top: 20px; margin-bottom: 40px;
    }
    </style>""", unsafe_allow_html=True
)

# --- SESSION STATE UNTUK LOGIN / SIGN UP ---
if 'akses_terbuka' not in st.session_state:
    st.session_state.akses_terbuka = False

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

# ==========================================
# GERBANG SIGN-UP (LEAD MAGNET GATE)
# ==========================================
if not st.session_state.akses_terbuka:
    st.markdown("""
    <div class="gate-box">
        <h2 style="color: #FFD700; margin-top: 0;">Akses Superior Terkunci 🔒</h2>
        <p style="color: #ccc; font-size: 15px;">Sistem pemindaian ini menggunakan komputasi Astrologi, Esoterik Nama, dan Primbon Betaljemur Adammakna tingkat tinggi. Untuk menjaga eksklusivitas energi, silahkan registrasi akses Anda secara <b>GRATIS</b> di bawah ini.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("form_signup"):
        st.markdown("### 📝 Form Registrasi Akses")
        col_nama, col_wa = st.columns(2)
        with col_nama:
            lead_nama = st.text_input("Nama Panggilan:")
        with col_wa:
            lead_wa = st.text_input("Nomor WhatsApp Aktif:")
            
        lead_email = st.text_input("Email (Opsional):")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("Buka Akses Analisa Sekarang 🔓")
        
        if submit_btn:
            if len(lead_nama) < 3 or len(lead_wa) < 9:
                st.error("⚠️ Mohon lengkapi Nama dan Nomor WhatsApp yang valid untuk sinkronisasi.")
            else:
                # Disini lu bisa nambahin script buat ngelempar data leads (Nama, WA, Email) ke Google Sheets baru lu.
                # Untuk sekarang, kita bypass masuk ke aplikasi.
                st.session_state.akses_terbuka = True
                st.success("✅ Sinkronisasi berhasil! Membuka gerbang dimensi...")
                time.sleep(1.5)
                st.rerun()

# JIKA AKSES SUDAH TERBUKA, TAMPILKAN APLIKASI UTAMA
else:
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
                nj2 = hitung_
