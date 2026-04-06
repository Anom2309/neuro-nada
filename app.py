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
    page_title="Deep Personality Mapping", 
    page_icon="🌌", 
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- CUSTOM CSS (TAMBAHAN EFEK LOCK & BLUR) ---
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
        background: linear-gradient(90deg, #ff4b4b 0%, #cc0000 100%);
        color: white !important; padding: 18px; text-align: center; 
        border-radius: 10px; font-weight: 900; font-size: 17px; 
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.5);
        text-transform: uppercase; letter-spacing: 1px;
        transition: 0.3s; margin-top: 10px; border: 2px solid #ff7a7a;
    }
    .cta-button:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(255, 75, 75, 0.7); }

    .ulasan-box {
        background-color: #1e1e1e; padding: 15px; border-radius: 8px;
        border-left: 4px solid #FFD700; margin-bottom: 10px; font-size: 14px;
    }
    
    .cosmic-box {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a4a 100%);
        padding: 20px; border-radius: 12px; border: 1px solid #4a4a8a;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6); margin-bottom: 15px;
    }

    /* KOTAK TERKUNCI (LOCK SYSTEM) */
    .locked-box {
        background: linear-gradient(180deg, #2a0a0a 0%, #110000 100%);
        padding: 25px; border-radius: 12px; border: 2px dashed #ff4b4b;
        text-align: center; margin-top: 20px; margin-bottom: 20px;
        box-shadow: inset 0 0 20px rgba(255,0,0,0.2);
    }
    .blur-text {
        color: transparent; text-shadow: 0 0 8px rgba(255,255,255,0.7);
        user-select: none;
    }
    
    .matrix-container {
        display: flex; justify-content: space-between; gap: 8px;
        padding: 12px; background-color: #101010; border-radius: 10px;
        border: 1px solid #333; margin-bottom: 20px;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
    }
    .matrix-item { flex: 1; text-align: center; padding: 5px; border-right: 1px solid #333; }
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
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

# --- INTERFACE UTAMA ---
if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass

st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900;'>🌌 Deep Personality Mapping</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #D4AF37; margin-bottom:0;'>Membongkar Matrix Bawah Sadar Lewat Sandi Semesta</p>", unsafe_allow_html=True)
st.markdown("---")

tgl_today = datetime.date.today()

# --- DATABASE ARKETIPE ---
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

tips_zodiak_nlp = {
    "Aries": "Pacing dulu emosinya, baru perlahan Lead ke logika Anda.", "Taurus": "Berikan data logis, biarkan mereka merasa itu keputusannya.",
    "Gemini": "Ikuti ritme cepatnya; gunakan bahasa visual.", "Cancer": "Hati-hati nada suara; cara Anda bicara adalah segalanya.",
    "Leo": "Sentuh egonya dengan apresiasi tulus sebelum memberi kritik.", "Virgo": "Tarik perhatiannya dari detail ke Gambaran Besar.",
    "Libra": "Bantu mereka mengambil keputusan dari keinginan internal mereka.", "Scorpio": "Bangun trust terdalam; pantang berbohong sekecil apapun.",
    "Sagittarius": "Hubungkan masalah saat ini dengan visi masa depan.", "Capricorn": "Mulai dari logika fungsional, lalu turun ke emosional.",
    "Aquarius": "Sajikan ide anti-mainstream untuk memancing intelektualnya.", "Pisces": "Tarik perlahan ke fakta realita saat imajinasinya mulai negatif."
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
        1: "The Leader", 2: "The Mediator", 3: "The Communicator", 4: "The Architect", 
        5: "The Explorer", 6: "The Nurturer", 7: "The Analyst", 8: "The Strategist", 9: "The Humanist"
    }
    return arketipe_dict.get(angka, "Pribadi Unik")

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
    if p < 0.03 or p > 0.97: return "🌑 New Moon", "Kekuatan internal sangat tajam.", "Menyusun target besar secara diam-diam dan rahasia.", "Terlalu cepat mencari validasi publik."
    elif p < 0.22: return "🌒 Waxing Crescent", "Dorongan batin tinggi untuk bertumbuh.", "Berani mengeksekusi ide konkrit pertama.", "Menunda pekerjaan karena pesimis."
    elif p < 0.28: return "🌓 First Quarter", "Karakter petarung aktif saat menghadapi krisis.", "Mengambil risiko terukur memecahkan masalah.", "Menyerah pada rintangan teknis pertama."
    elif p < 0.47: return "🌔 Waxing Gibbous", "Perfeksionis dan teliti.", "Memperhatikan detail dan asah skill.", "Mengabaikan kritik membangun."
    elif p < 0.53: return "🌕 Full Moon", "Gelombang otak puncak, karismatik namun rentan meledak.", "Tampil memimpin di depan publik.", "Membuat keputusan emosional reaktif."
    elif p < 0.72: return "🌖 Waning Gibbous", "Bakat alami sebagai Mentor.", "Berbagi pengalaman pada orang lain.", "Menyombongkan diri dan enggan beradaptasi."
    elif p < 0.78: return "🌗 Last Quarter", "Berani membuang hal yang tak berguna.", "Membersihkan lingkaran toxic.", "Menyimpan dendam masa lalu."
    else: return "🌘 Waning Crescent", "Memancarkan energi Healer intuitif.", "Merawat diri dan melepas ekspektasi.", "Memaksa tubuh bekerja ekstra keras."

def get_daily_dynamic_sync():
    today = datetime.date.today()
    epoch = datetime.date(2000, 1, 6)
    days = (today - epoch).days
    lunations = days / 29.53058867
    p = lunations % 1
    energy_score = int(math.sin(p * math.pi) * 100)
    
    daily_do = {
        "New Moon": ["Reset niat dan susun blueprint jangka panjang hari ini."],
        "Waxing Crescent": ["Baterai mulai terisi. Eksekusi ide konkrit pertama Anda sekarang!"],
        "First Quarter": ["Pecahkan rintangan keras hari ini. Otak Anda sangat reaktif!"],
        "Waxing Gibbous": ["Fokus tinggi! Sempurnakan detail dan asah skill teknis Anda."],
        "Full Moon": ["Puncak daya tarik magnetis! Launching karya atau perluas networking."],
        "Waning Gibbous": ["Fase syukur. Bagikan pengalaman dan mentoring ke orang lain."],
        "Last Quarter": ["Pembersihan total! Putuskan hubungan toxic dan kebiasaan buruk."],
        "Waning Crescent": ["Fase penyembuhan batin. Istirahatkan sistem saraf Anda."]
    }
    
    daily_dont = {
        "New Moon": ["Grasa-grusu mengambil keputusan tanpa data valid."],
        "Waxing Crescent": ["Prokrastinasi dan meragukan kemampuan diri sendiri."],
        "First Quarter": ["Menyerah pada halangan teknis pertama yang muncul."],
        "Waxing Gibbous": ["Terjebak ilusi kesempurnaan (Perfeksionis berlebihan)."],
        "Full Moon": ["Berdebat emosional dan membuat keputusan reaktif."],
        "Waning Gibbous": ["Egois, pelit ilmu, dan menolak perubahan."],
        "Last Quarter": ["Menyimpan dendam dan bernostalgia pada masa lalu kelam."],
        "Waning Crescent": ["Memaksakan diri bekerja ekstra keras (Hustle culture)."]
    }
    
    if p < 0.03 or p > 0.97: k = "New Moon"
    elif p < 0.22: k = "Waxing Crescent"
    elif p < 0.28: k = "First Quarter"
    elif p < 0.47: k = "Waxing Gibbous"
    elif p < 0.53: k = "Full Moon"
    elif p < 0.72: k = "Waning Gibbous"
    elif p < 0.78: k = "Last Quarter"
    else: k = "Waning Crescent"
    
    return k, energy_score, random.choice(daily_do[k]), random.choice(daily_dont[k])

# --- MENU TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Identitas Kosmik", "👩‍❤️‍👨 Couple Sync", "🕸️ Audit Sistem Saraf"])

# ==========================================
# TAB 1: IDENTITAS KOSMIK (FUNNELING MODE ON)
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
            status_text.markdown("⏳ *Menghubungkan ke gelombang kosmik...*")
            time.sleep(0.7)
            status_text.markdown("⏳ *Mengekstraksi sandi tanggal lahir & Weton...*")
            time.sleep(0.7)
            status_text.empty()
            
            angka_hasil = hitung_angka(tgl_input)
            angka_nama = hitung_angka_nama(nama_user)
            nep, wet = get_neptu_weton(tgl_input)
            zod = get_zodiak(tgl_input)
            ark_n = get_arketipe(angka_hasil)
            
            m_phase, m_sifat, _, _ = get_birth_moon(tgl_input)
            today_phase, today_energy, today_do, today_dont = get_daily_dynamic_sync()
            punchy = arketipe_punchy.get(angka_hasil)
            
            st.snow()
            st.markdown(f"<h3 style='text-align:center;'>🌌 Blueprint Kosmik: {nama_user.upper()}</h3>", unsafe_allow_html=True)
            
            # --- DAILY GUIDANCE KOSMIK ---
            if today_energy > 70: warna_baterai, glow = "#25D366", "rgba(37, 211, 102, 0.5)"
            elif today_energy > 40: warna_baterai, glow = "#FFD700", "rgba(255, 215, 0, 0.5)"
            else: warna_baterai, glow = "#ff4b4b", "rgba(255, 75, 75, 0.5)"
            
            st.markdown(f"""
            <div class="cosmic-box" style="box-shadow: 0 4px 15px {glow};">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #333; padding-bottom:10px; margin-bottom:10px;">
                    <span style="color:#888; font-size:12px; font-weight:bold; letter-spacing:1px;">DAILY SYNC (HARI INI)</span>
                    <span style="color:{warna_baterai}; font-weight:900; font-size:14px; text-shadow: 0 0 8px {warna_baterai};">BATERAI EMOSI: {today_energy}%</span>
                </div>
                <div style="font-size:14px; line-height:1.6;">
                    <span style="color:#FFD700;">✅ <b>FOKUS HARI INI:</b></span> {today_do}<br>
                    <span style="color:#ff4b4b;">❌ <b>HINDARI:</b></span> {today_dont}
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
            
            # --- THE HOOK (BAGIAN GRATIS YANG BIKIN PENASARAN) ---
            st.markdown("### 👁️ Identitas Bawah Sadar Anda")
            st.info(f"Sistem mendeteksi Anda memiliki arketipe **{ark_n}**. Anda memiliki potensi luar biasa. \n\n**IDENTITAS INTI:** {punchy['inti']}")
            
            st.markdown("🔥 **KEKUATAN DOMINAN ANDA:**")
            st.markdown(f"""
            <ul class="list-punchy" style="color:#25D366;">
                <li>{punchy['kekuatan'][0]}</li>
                <li>{punchy['kekuatan'][1]}</li>
                <li>{punchy['kekuatan'][2]}</li>
            </ul>
            """, unsafe_allow_html=True)

            # --- SIMULASI PENASARAN (PSYCHO TRIGGER) ---
            st.markdown("---")
            loading_shadow = st.empty()
            loading_shadow.warning("⚠️ Menganalisa rekam jejak kegagalan Anda...")
            time.sleep(1.5)
            loading_shadow.error("⚠️ Menemukan pola sabotase bawah sadar!")
            time.sleep(1)
            loading_shadow.empty()

            # --- THE LOCK (PAYWALL) ---
            st.markdown(f"""
            <div class="locked-box">
                <h3 style="color:#ff4b4b; margin-top:0;">🔒 DATA TERKUNCI (SHADOW SELF)</h3>
                <p style="color:#f0f0f0; font-size:15px; margin-bottom:15px;">Kenapa hidup Anda terasa <i>stuck</i> padahal Anda punya potensi besar? Karena ada pola bawah sadar yang diam-diam menahan Anda. Kami mendeteksi <b>3 Konflik Fatal</b> dalam pikiran Anda:</p>
                <ul style="list-style:none; padding:0; font-size:16px;">
                    <li style="margin-bottom:8px;">❌ <span class="blur-text">Mengorbankan kebahagiaan diri demi ekspektasi orang lain yang berlebihan.</span></li>
                    <li style="margin-bottom:8px;">❌ <span class="blur-text">Sulit melepaskan kontrol dan memaksa tubuh mengabaikan rasa lelah.</span></li>
                    <li style="margin-bottom:8px;">❌ <span class="blur-text">Sering memaklumi orang toxic atas nama kasihan hingga batin hancur.</span></li>
                </ul>
                <p style="color:#FFD700; font-weight:bold; font-size:14px; margin-top:15px;">Jika dibiarkan, pola ini akan terus mengulang kegagalan karir dan asmara Anda!</p>
            </div>
            """, unsafe_allow_html=True)
            
            # --- CTA MAUT MENUJU LYNK.ID ---
            url_t = link_produk.get(angka_hasil, "https://lynk.id/neuronada")
            st.markdown(f"""
            <a href="{url_t}" target="_blank" style="text-decoration: none;">
                <div class="cta-button">
                    🔓 BONGKAR FULL BLUEPRINT & HANCURKAN POLA GAGAL (RP 39.000)
                </div>
            </a>
            """, unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-size:12px; color:#888; margin-top:5px;'>Dapatkan Laporan PDF Premium berisi Penjelasan Karakter Mendalam, Sisi Gelap, Trik Komunikasi Asmara, dan Modul Terapi Audio khusus Kode Anda.</p>", unsafe_allow_html=True)
            
            # --- VIRAL LOOP (SHARE) ---
            st.markdown("---")
            wa_share = f"Gila, Blueprint Kosmik ini akurat banget baca potensi gue! Coba cek takdir bawah sadar lo di sini: https://mail.site.lu/"
            st.markdown(f"<center><a href='https://api.whatsapp.com/send?text={urllib.parse.quote(wa_share)}' target='_blank' style='text-decoration:none;'><div style='background-color:#111; color:white; padding:10px 20px; border-radius:8px; display:inline-block; font-weight:bold; border: 1px solid #333;'>📤 Share ke WhatsApp (Coba Cek Pasangan Lo)</div></a></center>", unsafe_allow_html=True)

# ==========================================
# TAB 2: COUPLE SYNC 
# ==========================================
with tab2:
    st.subheader("Sinkronisasi Asmara")
    st.write("Analisis benturan ego dan resonansi kosmik antara Anda dan pasangan.")
    ca, cb = st.columns(2)
    with ca: 
        n1 = st.text_input("Nama Anda", key="n1")
        d1 = st.date_input("Lahir Anda", value=datetime.date(1995, 1, 1), min_value=datetime.date(1940, 1, 1), max_value=tgl_today, key="d1")
    with cb: 
        n2 = st.text_input("Nama Pasangan", key="n2")
        d2 = st.date_input("Lahir Pasangan", value=datetime.date(1995, 1, 1), min_value=datetime.date(1940, 1, 1), max_value=tgl_today, key="d2")
        
    if st.button("Cek Kompatibilitas Bawah Sadar"):
        if n1 and n2:
            st.snow()
            
            zod1 = get_zodiak(d1); ne_1, we_1 = get_neptu_weton(d1)
            m_phase1, _, _, _ = get_birth_moon(d1)
            fase1_nama = m_phase1.split(" ", 1)[1] 
            
            zod2 = get_zodiak(d2); ne_2, we_2 = get_neptu_weton(d2)
            m_phase2, _, _, _ = get_birth_moon(d2)
            fase2_nama = m_phase2.split(" ", 1)[1]
            
            sel = abs(hitung_angka(d1) - hitung_angka(d2))
            sisa_weton = (ne_1 + ne_2) % 8
            
            hasil_weton_kombo = {
                1: ("💔 PEGAT (Ujian Ego)", "Terdapat perbedaan mendasar dalam cara memproses emosi dan dominasi ego.", "Turunkan ego. Gunakan teknik Pacing (menyelaraskan) sebelum berargumen.", "Mind-Reading dan mengungkit masa lalu."),
                2: ("👑 RATU (Kharisma & Harmoni)", "Penyatuan vibrasi ini memancarkan wibawa. Orang sekitar segan melihat kalian.", "Fokus pada apresiasi harian. Jadikan pasangan partner diskusi.", "Terjebak pencitraan eksternal."),
                3: ("💞 JODOH (Sinkronisasi Alami)", "Penerimaan bawah sadar luar biasa tinggi. Seperti sudah saling mengenal lama.", "Ciptakan kejutan spontan agar romansa tidak monoton.", "Terjebak di zona nyaman yang membosankan."),
                4: ("🌱 TOPO (Ujian Bertumbuh)", "Awal hubungan butuh kalibrasi, namun akan sangat solid jika melewati badai.", "Kuasai teknik Reframing (ubah sudut pandang) saat krisis.", "Memaksakan standar nilai pribadi yang kaku."),
                5: ("💰 TINARI (Magnet Rezeki)", "Vibrasi kalian jika disatukan akan menarik kelancaran finansial dan hoki.", "Bangun nilai spiritual bersama dalam bisnis/ide.", "Menjadikan materi sebagai satu-satunya perekat."),
                6: ("⚡ PADU (Beda Frekuensi)", "Sering terjadi letupan perdebatan karena beda cara filter informasi di otak.", "Validasi emosinya lebih dulu sebelum membantah logikanya.", "Konfrontasi langsung saat emosi sedang tinggi."),
                7: ("👁️ SUJANAN (Rawan Asumsi)", "Kecenderungan muncul rasa insecure, cemburu, atau salah paham mendadak.", "Buka komunikasi transparan berdasarkan fakta.", "Menggunakan bahasa generalisasi ('Kamu selalu...')."),
                0: ("🕊️ PESTHI (Damai & Rukun)", "Hubungan yang stabil, adem ayem, dan jauh dari drama penguras energi mental.", "Rutin mencari aktivitas atau liburan baru bersama.", "Saking damainya bisa terasa hambar.")
            }
            
            judul_weton, desk_weton, saran_do, saran_dont = hasil_weton_kombo.get(sisa_weton, ("Analisa Unik", "Butuh kalibrasi", "Perbaiki komunikasi", "Jangan egois"))
            
            st.markdown("---")
            st.markdown(f"### 🔮 Analisis Resonansi: {n1.split()[0].capitalize()} & {n2.split()[0].capitalize()}")
            st.info(f"Menyatukan filter pikiran **{zod1}** dengan **{zod2}** ibarat menggabungkan dua elemen. Frekuensi kosmik **{fase1_nama}** beresonansi dengan **{fase2_nama}** milik pasangan. Berdasarkan akar budaya **{we_1} & {we_2}**:")
            
            st.markdown(f"#### {judul_weton}")
            st.write(desk_weton)
            
            if sel in [0, 3, 6, 9]: st.success("💘 **SKOR META-PROGRAM (NLP): 90% (Sangat Sinkron)**")
            elif sel in [1, 2, 8]: st.warning("⚖️ **SKOR META-PROGRAM (NLP): 70% (Dinamis)**")
            else: st.error("🔥 **SKOR META-PROGRAM (NLP): 50% (Rawan Gesekan)**")

            # LOCK SYSTEM DI SINKRONISASI ASMARA
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background:#2a0a0a; padding:15px; border-radius:8px; border:1px solid #ff4b4b; text-align:center;">
                <p style="color:#ff4b4b; font-weight:bold; margin:0;">🔒 TRIK KOMUNIKASI BAWAH SADAR TERKUNCI</p>
                <p style="font-size:12px; color:#aaa;">Ingin tahu cara menundukkan ego pasangan dan panduan <b>DO'S & DONT'S</b> lengkap? Dapatkan Blueprint Premium Anda.</p>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 3: AUDIT SISTEM SARAF
# ==========================================
with tab3:
    st.subheader("🕸️ Audit Sistem Saraf (Wheel of Life)")
    st.info("**Apa itu Audit Sistem Saraf?**\n\nDalam dunia psikologi, energi mengalir layaknya jaring roda. Jika satu area sangat rendah, roda hidup akan 'oleng' menciptakan kebocoran energi *(Burnout)*.")

    kategori_label = ['Kesehatan Mental', 'Karir & Finansial', 'Asmara', 'Spiritual', 'Fisik']
    sk = [st.slider(k, 1, 10, 5) for k in kategori_label]
    
    if st.button("Mulai Audit Radar"):
        fig = go.Figure(data=go.Scatterpolar(
            r=sk+[sk[0]], theta=['Mental','Karir','Asmara','Spiritual','Fisik','Mental'], 
            fill='toself', fillcolor='rgba(212, 175, 55, 0.4)', line=dict(color='#D4AF37')
        ))
        st.plotly_chart(fig)
        avg = sum(sk)/5
        
        pesan_rendah = ["🚨 **KONDISI KRITIS:** Sistem saraf kelelahan parah. Lakukan Detoks Mental.", "⚠️ **KEBOCORAN FATAL:** Roda kehidupan sangat oleng. Selamatkan kewarasan batin Anda."]
        pesan_sedang = ["⚖️ **FASE STAGNAN:** Kondisi aman, tapi tidak maksimal. Tutup celah skor terendah.", "🟡 **ZONA NYAMAN MENIPU:** Selesaikan area terlemah Anda untuk melesat."]
        pesan_tinggi = ["🔥 **PEAK STATE:** Sinkronisasi sempurna. Eksekusi visi Anda sekarang!", "🌟 **HIGH PERFORMANCE:** Anda memancarkan aura magnetis untuk menarik peluang."]

        st.markdown("---")
        if avg < 5: st.error(random.choice(pesan_rendah))
        elif avg < 8: st.warning(random.choice(pesan_sedang))
        else: st.success(random.choice(pesan_tinggi))

st.markdown("---")
st.markdown("<center><b>Ahmad Septian Dwi Cahyo</b><br><small>Deep Personality Mapping © 2026</small></center>", unsafe_allow_html=True)
