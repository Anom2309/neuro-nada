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

# --- CUSTOM CSS ---
st.markdown(
    """<style>
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    
    /* Tombol Utama */
    div.stButton > button {
        background-color: #FFD700 !important; color: #000000 !important;
        font-weight: 800 !important; border: none !important;
        padding: 12px 24px !important; border-radius: 8px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
        box-shadow: 0 4px 10px rgba(255,215,0,0.3);
    }
    div.stButton > button:hover { transform: scale(1.02); background-color: #FFC107 !important; }
    
    /* Tombol CTA Maut */
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
        border-left: 4px solid #FFD700; margin-bottom: 10px; font-size: 14px;
    }
    
    .cosmic-box {
        background: linear-gradient(135deg, #0a0a2a 0%, #1a1a4a 100%);
        padding: 20px; border-radius: 12px; border: 1px solid #4a4a8a;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6); margin-bottom: 15px;
    }
    
    /* MATRIKS KECIL PROPORSIONAL */
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
    
    /* List Kekuatan & Shadow */
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
st.markdown("<p style='text-align: center; font-size: 16px; color: #D4AF37; margin-bottom:0;'>Blueprint Jiwa Berbasis Waktu Lahir</p>", unsafe_allow_html=True)
st.markdown("---")

# --- PUNCHY DATABASE (THE HOOK) ---
# Format: Inti, 3 Kekuatan
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

closing_brutal_dinamis = {
    1: ["Overthinking karena merasa hasil 'belum sempurna'", "Gengsi minta tolong saat memikul beban sendirian", "Membangun tembok ego untuk menutupi rasa sepi"],
    2: ["Mengorbankan kebahagiaan diri demi ekspektasi orang lain", "Sulit berkata 'TIDAK' yang berujung kelelahan mental", "Memendam amarah dalam hati demi menghindari konflik"],
    3: ["Menyembunyikan gelisah batin di balik topeng senyuman", "Cepat kehilangan motivasi jika rutinitas membosankan", "Insomnia karena pikiran terlalu berisik (Over-analisa)"],
    4: ["Stres parah jika rencana mendadak berubah di luar kendali", "Terjebak di zona nyaman karena takut ambil resiko baru", "Sering dinilai terlalu dingin/kaku oleh pasangan"],
    5: ["Sindrom 'Cepat Bosan' yang mensabotase karya/hubungan", "Kelelahan saraf karena otak tak pernah diizinkan istirahat", "Merasa hampa karena kehilangan pijakan komitmen"],
    6: ["Burnout ekstrim karena sibuk mengurus hidup orang lain", "Sikap Over-Protective yang diam-diam mengekang", "Rasa bersalah luar biasa jika memakai waktu untuk diri sendiri"],
    7: ["Paralysis by Analysis (Menganalisa terus tanpa aksi nyata)", "Merasa terasing karena merasa tak ada yang sepemikiran", "Mencurigai niat baik orang akibat luka masa lalu"],
    8: ["Merasa hampa dan kosong di saat mencapai puncak sukses", "Sangat sulit melepaskan kontrol dan memaafkan", "Memaksa tubuh bekerja dan mengabaikan alarm lelah"],
    9: ["Sering memaklumi orang toxic atas nama 'kasihan'", "Patah hati hebat akibat ekspektasi berlebihan pada manusia", "Kelelahan batin memikirkan beban dunia yang bukan tanggung jawabnya"]
}

tips_zodiak_nlp = {
    "Aries": "Pacing dulu emosinya, baru perlahan Lead ke logika Anda.", "Taurus": "Berikan data logis, biarkan mereka merasa itu keputusannya.",
    "Gemini": "Ikuti ritme cepatnya; gunakan bahasa visual.", "Cancer": "Hati-hati nada suara; *cara* Anda bicara adalah segalanya.",
    "Leo": "Sentuh egonya dengan apresiasi tulus sebelum memberi kritik.", "Virgo": "Tarik perhatiannya dari detail ke 'Gambaran Besar'.",
    "Libra": "Bantu mereka mengambil keputusan dari keinginan *internal* mereka.", "Scorpio": "Bangun trust terdalam; pantang berbohong sekecil apapun.",
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

def get_moon_energy(date):
    # Mengembalikan Fase Bulan, Energy Score (%), Saran Action
    epoch = datetime.date(2000, 1, 6)
    days = (date - epoch).days
    lunations = days / 29.53058867
    p = lunations % 1
    
    # Falak Energy Score (Sine Wave mapping 0 -> 100 -> 0)
    energy_score = int(math.sin(p * math.pi) * 100)
    
    if p < 0.03 or p > 0.97: return "🌑 New Moon", energy_score, "Waktu terbaik reset niat. Susun blueprint jangka panjang.", "Terburu-buru mencari validasi publik."
    elif p < 0.22: return "🌒 Waxing Crescent", energy_score, "Baterai mulai terisi. Eksekusi ide konkrit pertama Anda.", "Prokrastinasi & meragukan diri sendiri."
    elif p < 0.28: return "🌓 First Quarter", energy_score, "Pecahkan rintangan keras hari ini. Otak sangat reaktif.", "Menyerah pada halangan teknis pertama."
    elif p < 0.47: return "🌔 Waxing Gibbous", energy_score, "Fokus tinggi. Sempurnakan detail dan asah skill teknis.", "Cepat puas & mengabaikan kritik."
    elif p < 0.53: return "🌕 Full Moon", energy_score, "Puncak daya tarik magnetis. Launching atau perluas networking.", "Berdebat emosional & keputusan reaktif."
    elif p < 0.72: return "🌖 Waning Gibbous", energy_score, "Fase syukur. Bagikan pengalaman dan mentoring ke orang lain.", "Egois & menolak perubahan."
    elif p < 0.78: return "🌗 Last Quarter", energy_score, "Pembersihan total. Putuskan hubungan toxic dan kebiasaan buruk.", "Menyimpan dendam & nostalgia masa lalu."
    else: return "🌘 Waning Crescent", energy_score, "Fase penyembuhan batin. Istirahatkan sistem saraf Anda.", "Memaksakan diri bekerja ekstra keras (Hustle)."

# --- MENU TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Identitas Kosmik", "👩‍❤️‍👨 Couple Sync", "🕸️ Audit Sistem Saraf"])

# ==========================================
# TAB 1: IDENTITAS KOSMIK (CINEMATIC & PUNCHY)
# ==========================================
with tab1:
    st.subheader("Akses Blueprint Bawah Sadar Anda")
    nama_user = st.text_input("Nama Lengkap:", placeholder="Ketik nama asli Anda...", key="t1_nama")
    tgl_today = datetime.date.today()
    tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date(1995, 1, 1), min_value=datetime.date(1920, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")

    if st.button("Kalkulasi Blueprint (Mulai)"):
        if not nama_user or len(nama_user.strip()) < 3: 
            st.error("🚨 Mohon ketik nama lengkap untuk sinkronisasi vibrasi.")
        elif tgl_input == tgl_today: 
            st.error("🚨 Tanggal lahir tidak valid.")
        else:
            # CINEMATIC LOADING
            status_text = st.empty()
            status_text.markdown("⏳ *Menghubungkan ke gelombang kosmik...*")
            time.sleep(0.7)
            status_text.markdown("⏳ *Mengekstraksi sandi tanggal lahir & Weton...*")
            time.sleep(0.7)
            status_text.markdown("⏳ *Mendeteksi konflik batin dan pola sabotase diri...*")
            time.sleep(0.9)
            status_text.empty()
            
            # Kalkulasi
            angka_hasil = hitung_angka(tgl_input); angka_nama = hitung_angka_nama(nama_user)
            nep, wet = get_neptu_weton(tgl_input); zod = get_zodiak(tgl_input)
            
            m_phase, m_energy, m_do, m_dont = get_moon_energy(tgl_input)
            today_phase, today_energy, today_do, today_dont = get_moon_energy(tgl_today)
            
            punchy = arketipe_punchy.get(angka_hasil)
            shadow = closing_brutal_dinamis.get(angka_hasil)
            
            # Dynamic Hook
            hook_text = random.choice([
                "Sistem mendeteksi adanya anomali unik pada arketipe Anda.",
                "Ada pola tersembunyi yang jarang Anda sadari selama ini.",
                "Gelombang bawah sadar Anda menunjukkan sinkronisasi yang menarik."
            ])
            
            st.balloons()
            st.markdown(f"<h3 style='text-align:center;'>🌌 Blueprint Kosmik: {nama_user.upper()}</h3>", unsafe_allow_html=True)
            
            # --- DAILY GUIDANCE KOSMIK (SUBSCRIPTION VIBE) ---
            warna_baterai = "#25D366" if today_energy > 60 else "#FFD700" if today_energy > 30 else "#ff4b4b"
            st.markdown(f"""
            <div class="cosmic-box">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #333; padding-bottom:10px; margin-bottom:10px;">
                    <span style="color:#888; font-size:12px; font-weight:bold; letter-spacing:1px;">DAILY SYNC (HARI INI)</span>
                    <span style="color:{warna_baterai}; font-weight:900; font-size:14px;">BATERAI EMOSI: {today_energy}%</span>
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
            
            # --- THE DEEP READING (PUNCHY FORMAT) ---
            st.markdown("### 👁️ Decode Kepribadian Bawah Sadar")
            st.info(f"*{hook_text}* Perpaduan fase bulan **{m_phase}** dan weton **{wet}** melahirkan arketipe Anda:\n\n**IDENTITAS INTI:** {punchy['inti']}")
            
            st.markdown("🔥 **3 KEKUATAN DOMINAN:**")
            st.markdown(f"""
            <ul class="list-punchy" style="color:#25D366;">
                <li>{punchy['kekuatan'][0]}</li>
                <li>{punchy['kekuatan'][1]}</li>
                <li>{punchy['kekuatan'][2]}</li>
            </ul>
            """, unsafe_allow_html=True)
            
            st.markdown("⚠️ **SISI GELAP (SHADOW SELF):**")
            st.markdown(f"""
            <ul class="list-punchy" style="color:#ff4b4b;">
                <li>{shadow[0]}</li>
                <li>{shadow[1]}</li>
                <li>{shadow[2]}</li>
            </ul>
            <p style="font-size:14px; color:#aaa; font-style:italic;">Catatan: Pola sabotase diri ini akan terus membatasi rezeki dan asmara Anda jika tidak segera di-kalibrasi.</p>
            """, unsafe_allow_html=True)
            
            # --- PSYCHOLOGICAL CTA (PAIN-BASED) ---
            st.markdown("<br>", unsafe_allow_html=True)
            url_t = link_produk.get(angka_hasil, "https://lynk.id/neuronada")
            st.markdown(f"""
            <a href="{url_t}" target="_blank" style="text-decoration: none;">
                <div class="cta-button">
                    ⚠️ BONGKAR MENTAL BLOCK KODE {angka_hasil} & REBUT KENDALI HIDUP ANDA
                </div>
            </a>
            """, unsafe_allow_html=True)
            st.caption("<center>Modul PDF ini memuat skrip re-programming alam bawah sadar khusus untuk mematikan pola sabotase diri Anda.</center>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("<h4 style='text-align:center;'>🚀 Tindakan Ekstra</h4>", unsafe_allow_html=True)
            wa_text = f"Coach Ahmad, saya merinding baca hasil mapping Kode {angka_hasil}. Saya capek jadi korban 'Shadow Self'. Saya siap kalibrasi di Private Session."
            c_share, c_wa = st.columns(2)
            
            with c_share:
                # Share Button Mockup (Bikin Viral Loop)
                wa_share = f"Gila, akurat banget! Cek Blueprint Kosmik lu di sini: https://mail.site.lu/"
                st.markdown(f"<a href='https://wa.me/?text={urllib.parse.quote(wa_share)}' target='_blank'><div style='background-color:#333; color:white; padding:10px; text-align:center; border-radius:8px; font-weight:bold;'>📤 Bagikan ke Teman</div></a>", unsafe_allow_html=True)
            with c_wa:
                st.markdown(f"<a href='https://wa.me/628999771486?text={urllib.parse.quote(wa_text)}' target='_blank'><div style='background-color:#25D366; color:white; padding:10px; text-align:center; border-radius:8px; font-weight:bold;'>📲 Tanya Jadwal Private</div></a>", unsafe_allow_html=True)

# ==========================================
# TAB 2 & 3 (TETAP AMAN)
# ==========================================
with tab2:
    st.subheader("Sinkronisasi Asmara")
    st.write("Analisis tingkat benturan ego vs resonansi jiwa Anda dan pasangan.")
    ca, cb = st.columns(2)
    with ca: n1 = st.text_input("Nama Anda", key="n1"); d1 = st.date_input("Lahir Anda", value=datetime.date(1995, 1, 1), key="d1")
    with cb: n2 = st.text_input("Nama Pasangan", key="n2"); d2 = st.date_input("Lahir Pasangan", value=datetime.date(1995, 1, 1), key="d2")
    if st.button("Cek Kompatibilitas"):
        if n1 and n2:
            ne_1, we_1 = get_neptu_weton(d1); ne_2, we_2 = get_neptu_weton(d2)
            sel = abs(hitung_angka(d1) - hitung_angka(d2))
            st.markdown("---")
            st.info(f"**Integrasi Weton:** {we_1} & {we_2}")
            if sel in [0, 3, 6, 9]: st.success("💘 **SKOR NLP: 90% (Sinkron Alami)**\nSangat mudah memahami *Love Language* pasangan.")
            elif sel in [1, 2, 8]: st.warning("⚖️ **SKOR NLP: 70% (Dinamis)**\nBanyak beda sudut pandang, butuh kedewasaan untuk saling melengkapi.")
            else: st.error("🔥 **SKOR NLP: 50% (Rawan Gesekan)**\nEgo tinggi sering berbenturan. Butuh teknik komunikasi khusus.")
            
            zod1 = get_zodiak(d1)
            st.write(f"💡 **Trik Komunikasi untuk menaklukkan {zod1}:** {tips_zodiak_nlp.get(zod1)}")

with tab3:
    st.subheader("🕸️ Audit Sistem Saraf")
    st.caption("Jika jaring ini tidak seimbang, artinya ada kebocoran energi parah di bawah sadar Anda.")
    sk = [st.slider(k, 1, 10, 5) for k in ['Mental', 'Karir', 'Asmara', 'Spiritual', 'Fisik']]
    if st.button("Lihat Radar"):
        fig = go.Figure(data=go.Scatterpolar(r=sk+[sk[0]], theta=['Mental','Karir','Asmara','Spiritual','Fisik','Mental'], fill='toself', fillcolor='rgba(212, 175, 55, 0.4)', line=dict(color='#D4AF37')))
        st.plotly_chart(fig)
        avg = sum(skor)/5 if 'skor' in locals() else sum(sk)/5
        if avg < 5: st.error("🚨 Warning: Sistem mendeteksi kelelahan mental parah (Burnout).")
        elif avg < 8: st.warning("⚖️ Roda kehidupan stabil, tapi ada rem yang menahan laju potensi Anda.")
        else: st.success("🔥 Peak State! Ambil keputusan besar hari ini.")

# ==========================================
# SOCIAL PROOF (ULASAN)
# ==========================================
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Jejak Transformasi</h3>", unsafe_allow_html=True)

marquee_html = """
<div style="background-color: #1a1a1a; padding: 12px; border-radius: 8px; border-left: 3px solid #D4AF37; border-right: 3px solid #D4AF37; white-space: nowrap; overflow: hidden; margin-bottom: 20px;">
    <marquee behavior="scroll" direction="left" scrollamount="6" style="color: #f0f0f0; font-size: 15px;">
        <span style="color: #FFD700;">⭐⭐⭐⭐⭐</span> <b>dr. Antonius:</b> "Format barunya ngeri, bener-bener nelanjangin shadow self gue!" | 
        <span style="color: #FFD700;">⭐⭐⭐⭐⭐</span> <b>Andi S:</b> "Daily Sync-nya nagih, gue buka tiap pagi sblm meeting." | 
        <span style="color: #FFD700;">⭐⭐⭐⭐⭐</span> <b>Dewi A:</b> "Modul PDF-nya worth it parah. Mental block finansial gue luntur."
    </marquee>
</div>
"""
st.markdown(marquee_html, unsafe_allow_html=True)

daftar_ulasan = ambil_ulasan()
for u in daftar_ulasan[:3]:
    if u.get("Komentar"): st.markdown(f'<div class="ulasan-box"><b>{u.get("Nama")}</b> ⭐⭐⭐⭐⭐<br><i>"{u.get("Komentar")}"</i></div>', unsafe_allow_html=True)

with st.expander("💬 Bagikan Pengalaman Anda"):
    with st.form("form_review"):
        rn = st.text_input("Nama")
        rk = st.text_area("Ulasan (Gimana akurasinya?)")
        if st.form_submit_button("Kirim Ulasan") and rn and rk:
            if kirim_ulasan(rn, "5", rk): st.success("Terkirim!"); time.sleep(1); st.rerun()

st.markdown("---")
st.markdown("<center><b>Ahmad Septian Dwi Cahyo</b><br><small>Deep Personality Mapping © 2026</small></center>", unsafe_allow_html=True))
