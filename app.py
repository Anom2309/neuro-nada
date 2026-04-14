import streamlit as st
import datetime
import os
import time
import urllib.parse
import urllib.request
import math
import random
import csv
import io
import hashlib

# --- INIT SESSION STATE (PAYWALL) ---
if 'premium' not in st.session_state:
    st.session_state.premium = False

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="Neuron AI Ultimate OS", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- CUSTOM CSS & SOFT ANIMATION ---
st.markdown(
    """<style>
    @keyframes softFade {
        0% { opacity: 0; transform: translateY(20px); filter: blur(5px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px rgba(212,175,55,0.2); }
        50% { box-shadow: 0 0 25px rgba(212,175,55,0.6); }
        100% { box-shadow: 0 0 10px rgba(212,175,55,0.2); }
    }
    .soft-fade {
        animation: softFade 1.2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }
    
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
    planets = [
        ("Matahari ☀️", "Fokus pada otoritas, presentasi, dan mengambil kendali.", "#FFD700"), 
        ("Venus 💖", "Waktu emas untuk negosiasi, asmara, dan melobi orang.", "#FF69B4"), 
        ("Merkurius 📝", "Eksekusi semua urusan email, naskah, dan komunikasi.", "#00FFFF"), 
        ("Bulan 🌙", "Waktu intuitif. Bagus untuk brainstorming atau istirahat.", "#F0F8FF"), 
        ("Saturnus 🪐", "Energi berat. Fokus pada pekerjaan repetitif dan audit.", "#8B4513"), 
        ("Yupiter 🍀", "Pintu rezeki terbuka. Waktu terbaik investasi/pitching.", "#32CD32"), 
        ("Mars ⚔️", "Energi agresif tinggi. Cocok untuk olahraga/eksekusi berani.", "#FF4500")
    ]
    return planets[datetime.datetime.now().hour % 7]

def get_sun_phase():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 8: return "Sunrise (Inisiasi)", "Gelombang otak beralih ke Alpha. Ideal untuk setting niat harian."
    elif 8 <= hour < 12: return "Morning (Akselerasi)", "Energi memuncak. Eksekusi tugas paling sulit sekarang."
    elif 12 <= hour < 15: return "Zenith (Konsolidasi)", "Matahari di puncak. Waktu untuk evaluasi dan re-kalibrasi."
    elif 15 <= hour < 18: return "Golden Hour (Refleksi)", "Waktu terbaik untuk kreativitas dan menyelesaikan urusan harian."
    elif 18 <= hour < 20: return "Sunset (Pelepasan)", "Tutup sistem saraf Anda dari beban kerja."
    else: return "Night Void (Regenerasi)", "Fase Delta. Dilarang mengambil keputusan besar di jam ini."

# --- DATABASE CLOUD ---
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

def generate_seed(base_str):
    return int(hashlib.md5(base_str.encode('utf-8')).hexdigest(), 16) % (10**8)

# --- PROCEDURAL TACTICAL PLAN ---
def proc_tactical_plan(nama, mod_harian, planet_live, planet_desc, sun_fase, sun_desc):
    random.seed(generate_seed(f"tac_{nama}_{mod_harian}_{planet_live}"))
    fase_detail = {
        0: {"nama": "🔴 FASE NADIR (Rest & Reset)", "analisa": f"Sistem saraf dan gelombang otak {nama} sedang berada di titik terendah siklusnya. Tubuh eterik Anda sedang melakukan 'reboot' sistem internal. Memaksakan ambisi besar hari ini sama dengan memacu mobil dengan gigi satu, mesin saraf Anda akan cepat aus dan *burnout*.", "do": ["Kerjakan hal-hal repetitif yang tidak butuh mikir keras.", "Lakukan *Deep Rest*, *stretching* fisik, atau perbanyak tidur."], "dont": "DILARANG KERAS membuat keputusan finansial besar atau memulai konflik emosional hari ini. Filter logika sedang lemah."},
        1: {"nama": "🟢 FASE INISIASI (The Spark)", "analisa": f"Ini adalah momentum ledakan energi pertama Anda, {nama}! Pintu kosmik terbuka lebar untuk niat-niat baru. Segala sesuatu yang Anda mulai hari ini memiliki daya dorong 3x lipat lebih kuat.", "do": ["Luncurkan ide baru, kirim proposal, atau hubungi prospek/klien target.", "Lakukan gebrakan eksekusi pertama, walau hanya 5 menit."], "dont": "HINDARI sifat *over-analysis*. Bertindaklah sekarang!"},
        2: {"nama": "🔵 FASE SINKRONISASI (Kolaborasi)", "analisa": f"Energi independen {nama} sedang menurun, digantikan daya magnetisme sosial. Hari ini, rezeki Anda kemungkinan besar datang dari tangan orang lain.", "do": ["Ajak negosiasi pihak yang tadinya alot.", "Delegasikan tugas yang bikin pusing ke tim/ahlinya."], "dont": "JANGAN berjuang sendirian (Lone Wolf) hari ini. Anda akan kehabisan daya."},
        3: {"nama": "🟡 FASE RESONANSI (Ekspresi Diri)", "analisa": f"Cakra komunikasi {nama} sedang menyala terang. Frekuensi suara Anda memiliki daya tembus alam bawah sadar yang luar biasa kepada siapapun yang mendengarnya.", "do": ["Buat konten, presentasi, atau pitching.", "*Speak up*! Sampaikan keluhan atau ide ke atasan/pasangan."], "dont": "JANGAN berdiam diri. Energi persuasi magis ini terbuang percuma jika Anda diam."},
        4: {"nama": "🟤 FASE MATERIALISASI (Pondasi)", "analisa": f"Gelombang otak {nama} sedang sangat rasional dan membumi. Ini bukan waktunya berkhayal. Hari ini murni tentang mengamankan dan merawat apa yang sudah Anda bangun.", "do": ["Audit total arus kas (keuangan) Anda.", "Fokus pada detail operasional yang membosankan namun vital."], "dont": "DILARANG mengambil risiko spekulatif (judi, trading asal, foya-foya)."},
        5: {"nama": "🟠 FASE EKSPANSI (Tantangan Ekstrim)", "analisa": f"Adrenalin kosmik {nama} memuncak tajam! Batas ketakutan (mental block) melemah, memberikan celah terbuka untuk terobosan radikal.", "do": ["Eksekusi satu hal yang paling Anda takuti minggu ini.", "Uji coba strategi bisnis yang berisiko."], "dont": "JANGAN biarkan diri terjebak kebosanan. Diam hari ini berubah menjadi *Anxiety*."},
        6: {"nama": "🟣 FASE ELEVASI (Pengayoman & Karma)", "analisa": f"Vibrasi jiwa {nama} menembus urusan duniawi hari ini. Anda memancarkan energi *Healer*. Alam semesta menuntut Anda sejenak kembali ke 'akar'.", "do": ["Perbaiki hubungan yang retak.", "Lakukan *Charity* atau bantu kesulitan orang lain secara anonim."], "dont": "HINDARI perdebatan ego atau ambisi memanipulasi orang. Karma instan berlaku hari ini."}
    }
    fd = fase_detail[mod_harian]
    buka = random.choice([f"Berdasarkan algoritma langit, sistem mendeteksi lonjakan energi pada **{nama}**.", f"Peringatan Taktis! Gelombang kosmik berpusat pada sektor tindakan **{nama}**."])
    planet_murni = planet_live.split(' ')[0]
    matahari_murni = sun_fase.split(' ')[0]
    koneksi = random.choice([f"Intervensi jam {planet_murni} pada fase {matahari_murni} menciptakan momentum eksekusi absolut.", f"Tabrakan resonansi {planet_murni} dan siklus {matahari_murni} mengunci otak dalam sadar penuh."])
    do_html = "".join([f"<li style='margin-bottom: 8px;'>{item}</li>" for item in random.sample(fd["do"], 2)])

    html_output = f"""<div class="live-engine-box soft-fade" style="background: rgba(20,20,25,0.9); border-left: 4px solid #00FFFF; padding: 25px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,255,255,0.1);">
<h4 style="color: #00FFFF; margin-top:0; letter-spacing: 1px; font-weight:900;">⚡ TACTICAL ACTION PLAN <span style="font-size:12px; color:#ff4b4b; font-weight:normal;">(⏳ Valid 24 Jam)</span></h4>
<p style="color: #ccc; font-size: 15px; line-height: 1.6; margin-bottom:20px;">
{buka}<br><br>
<b style="color:#FFF; font-size:16px;">STATUS BIORITME ANDA: <span style="color:#FFD700;">{fd['nama'].split('(')[0].strip()}</span></b><br>
{fd['analisa']}<br><br>
<i style="color:#888;">Sinkronisasi Kosmik:</i> {koneksi} ({planet_desc})
</p>
<div style="background: rgba(37,211,102,0.1); border: 1px solid rgba(37,211,102,0.4); padding: 15px; border-radius: 8px; margin-bottom: 15px;">
<b style="color: #25D366; font-size:15px;">🎯 PROTOKOL EKSEKUSI (LAKUKAN SEKARANG):</b>
<ul style="color: #e0e0e0; font-size: 15px; margin-top: 10px; margin-bottom: 0; padding-left: 20px; line-height:1.5;">
{do_html}
</ul>
</div>
<div style="background: rgba(255,75,75,0.1); border: 1px solid rgba(255,75,75,0.4); padding: 15px; border-radius: 8px;">
<b style="color: #ff4b4b; font-size:15px;">🛑 RED ZONE (HINDARI MUTLAK):</b><br>
<span style="color: #ccc; font-size: 14px; display:inline-block; margin-top:5px; line-height:1.5;">{fd['dont']}</span>
</div>
<p style="font-size:12px; color:#ff4b4b; margin-top:10px; font-weight:bold;">⏳ Sistem mendeteksi perubahan energi dalam beberapa jam ke depan. Jangan tunda eksekusi!</p>
</div>"""
    return fd['nama'], html_output

# --- ENGINE FALAK RUHANI ---
def proc_falak_ruhani(total_jummal, root_num, nama):
    ruhani_data = {
        1: {"asma": "Ya Fattah (Maha Pembuka)", "vibrasi": "Mendobrak Jalan Buntu & Ego", "tujuan": "Membersihkan ego masa lalu dan mendobrak pintu rezeki."},
        2: {"asma": "Ya Salam (Maha Sejahtera)", "vibrasi": "Harmoni & Perisai Mental", "tujuan": "Menetralisir energi beracun dan menyembuhkan lelah mental."},
        3: {"asma": "Ya Mushawwir (Maha Pembentuk)", "vibrasi": "Manifestasi Ide ke Realita", "tujuan": "Menarik pikiran liar menjadi karya fisik berstruktur."},
        4: {"asma": "Ya Muqit (Maha Pemberi Kecukupan)", "vibrasi": "Stabilitas & Nutrisi Batin", "tujuan": "Menghancurkan 'Mental Miskin' agar finansial stabil."},
        5: {"asma": "Ya Basith (Maha Melapangkan)", "vibrasi": "Ekspansi & Pembebasan Diri", "tujuan": "Menghilangkan rasa terkekang dan memperluas wadah rezeki."},
        6: {"asma": "Ya Wadud (Maha Mengasihi)", "vibrasi": "Cinta Universal & Daya Tarik", "tujuan": "Menyembuhkan trauma luka dan memancarkan aura pengasihan."},
        7: {"asma": "Ya Batin (Maha Tersembunyi)", "vibrasi": "Intuisi & Hikmah Langit", "tujuan": "Mempertajam insting dan menjernihkan intuisi bisnis."},
        8: {"asma": "Ya Ghaniy (Maha Kaya)", "vibrasi": "Otoritas & Kelimpahan Absolut", "tujuan": "Menjadi magnet kekayaan murni dan pemegang kendali."},
        9: {"asma": "Ya Hakim (Maha Bijaksana)", "vibrasi": "Pencerahan & Kesadaran", "tujuan": "Melepas beban karma dan menyelaraskan aksi dengan Misi Semesta."}
    }
    data = ruhani_data.get(root_num, ruhani_data[1])
    return data["asma"], data["vibrasi"], data["tujuan"], total_jummal

# --- PROTOKOL TERAPI DINAMIS ---
def get_protokol_terapi(root_num, nama):
    random.seed(generate_seed(f"pt_{nama}_{root_num}"))
    b1 = random.choice([f"**Ego Supremacy.** {nama} menolak bantuan karena merasa 'harus bisa sendiri'. Ujungnya Burnout.", f"**Ilusi Kontrol Sempurna.** Gengsi {nama} terlalu tinggi untuk minta tolong, menyabotase kolaborasi."])
    a1 = random.choice([f"Saya, {nama}, menurunkan perisai ego. Minta tolong adalah kecerdasan. Saya mengizinkan bantuan datang.", f"Mulai napas ini, {nama} menyadari kolaborasi adalah kunci. Saya pantas dibantu."])
    h1 = random.choice(["Cari 1 tugas hari ini dan mintalah tolong orang lain mengerjakannya.", "Hubungi mentor/teman. Ceritakan kendala Anda dan dengarkan sarannya."])

    b2 = random.choice([f"**People Pleaser.** {nama} memenjarakan suara hati demi orang lain. Sering jadi 'Spons Emosi' yang toxic.", f"**Luka Abandonment.** {nama} terlalu gampang 'nggak enakan' sampai mengorbankan diri sendiri."])
    a2 = random.choice([f"Saya, {nama}, memegang kendali atas kewarasan saya. Kebahagiaan saya adalah prioritas.", f"{nama} melepaskan rasa bersalah palsu ini. Merawat diri sendiri adalah yang utama."])
    h2 = random.choice(["Berlatih berani: Katakan 'TIDAK' pada satu ajakan hari ini dengan tegas.", "Lakukan Digital Detoxing. Matikan notifikasi dari sirkel toxic selama 12 jam."])

    b3 = random.choice([f"**Scattered Focus.** Otak {nama} produksi ratusan ide tapi eksekusi nol. Energi habis di overthinking.", f"**Impulsivitas.** {nama} kecanduan 'awal yang baru' sehingga gampang bosan di tengah jalan."])
    a3 = random.choice([f"Saya, {nama}, memerintahkan pikiran melambat. Satu eksekusi selesai lebih berharga dari seribu wacana.", f"Pikiran {nama} setajam laser. Saya akan menyelesaikan apa yang saya mulai."])
    h3 = random.choice(["Gunakan Timeboxing. Pilih 1 tugas, pasang timer 20 menit, kerjakan tanpa henti.", "Rapikan meja kerja atau bersihkan file sampah di HP hari ini."])

    b4 = random.choice([f"**Scarcity Mindset.** Ada ketakutan parah akan kegagalan. {nama} jadi terlalu kaku dan pelit pada diri sendiri.", f"**Sabotase Zona Nyaman.** {nama} beralasan 'nabung jaga-jaga' tapi malah menarik nasib buruk."])
    a4 = random.choice([f"Saya, {nama}, melepaskan takut akan kekurangan. Sumber daya Semesta berlimpah.", f"{nama} layak hidup berlimpah. Uang adalah energi yang baik."])
    h4 = random.choice(["Beri reward pada diri sendiri hari ini. Saat membayar, tersenyumlah.", "Lakukan sedekah subuh atau bantu orang secara impulsif hari ini."])

    b5 = random.choice([f"**Escapism.** {nama} lari saat dihadapkan pada tanggung jawab berat dengan dalih 'mencari kebebasan'.", f"**Korsleting Rutinitas.** Saat ditekan konsistensi, saraf {nama} mati rasa dan mendadak hampa."])
    a5 = random.choice([f"Saya, {nama}, menemukan makna dalam komitmen stabil. Ini pondasi baja, bukan penjara.", f"{nama} berdamai dengan proses repetitif dan menanam akar yang kuat."])
    h5 = random.choice(["Pilih 1 pekerjaan membosankan yang Anda tunda, selesaikan 100% hari ini.", "Lakukan rutinitas pagi yang SAMA PERSIS 3 hari berturut-turut."])

    b6 = random.choice([f"**Savior Complex.** {nama} merasa bersalah jika bahagia sementara ada yang susah. Kuras energi obatin orang lain.", f"**Pengorbanan Palsu.** {nama} kasih 100% ke orang terdekat tapi diam-diam merasa hatinya kosong."])
    a6 = random.choice([f"Saya, {nama}, mengizinkan diri saya bahagia. Mencintai diri sendiri adalah syarat mutlak.", f"Penerima kelimpahan pertama adalah saya sendiri. {nama} berhak menikmati keringatnya."])
    h6 = random.choice(["Ambil waktu 'Me-Time' 45 menit murni tanpa interupsi hari ini.", "Beli makanan mewah kesukaan Anda, makan sendirian, jangan dibagi."])

    b7 = random.choice([f"**Paralysis by Analysis.** Otak {nama} over-analyzing niat orang lain sampai berbalik menyiksa diri sendiri.", f"**Trust Issue.** Masa lalu bikin {nama} sangat curiga, menolak peluang dan cinta tulus."])
    a7 = random.choice([f"Saya, {nama}, menyeimbangkan logika dan intuisi. Saya mempercayai proses Semesta.", f"{nama} melepaskan kebutuhan ego untuk tahu rahasia segalanya. Saya pasrah."])
    h7 = random.choice(["Lakukan Meditasi Hening 15 menit. Duduk diam amati napas tanpa mikir.", "Percayai satu tindakan niat baik dari orang hari ini TANPA Anda cross-check."])

    b8 = random.choice([f"**Control Freak.** {nama} memforsir tubuh demi mengejar standar yang tak ada garis finishnya.", f"**Obsesi Material.** Insting bisnis {nama} terang, tapi sering menghancurkan kedamaian batin sendiri."])
    a8 = random.choice([f"Saya, {nama}, adalah saluran damai, bukan budak ambisi. Saya bersinar saat berserah.", f"{nama} ikhlas melepaskan ilusi kendali. Saya sukses, berwibawa, dan damai."])
    h8 = random.choice(["Praktik Delegasi Radikal. Serahkan satu keputusan kendali pada orang lain hari ini.", "Terapkan Hard Stop: Berhenti sentuh urusan kerja tepat pukul 17:00 hari ini."])

    b9 = random.choice([f"**Toxic Empathy.** {nama} terlalu peka, gampang kasihan bahkan pada orang yang manipulatif.", f"**Patah Hati Universal.** Standar luhur {nama} berbenturan dengan realitas, bikin gampang kecewa."])
    a9 = random.choice([f"Saya, {nama}, melepaskan hal di luar kendali. Biarkan tiap jiwa memikul karmanya.", f"Tugas {nama} bukanlah menyelamatkan dunia. Energi saya suci dan saya jaga."])
    h9 = random.choice(["Detoksifikasi Negatif. Blokir gosip/berita tragedi selama 24 jam.", "Hari ini, BERHENTI memberikan nasihat/solusi KECUALI diminta."])

    protokol = {1: {"block": b1, "afirmasi": a1, "habit": h1}, 2: {"block": b2, "afirmasi": a2, "habit": h2}, 3: {"block": b3, "afirmasi": a3, "habit": h3}, 4: {"block": b4, "afirmasi": a4, "habit": h4}, 5: {"block": b5, "afirmasi": a5, "habit": h5}, 6: {"block": b6, "afirmasi": a6, "habit": h6}, 7: {"block": b7, "afirmasi": a7, "habit": h7}, 8: {"block": b8, "afirmasi": a8, "habit": h8}, 9: {"block": b9, "afirmasi": a9, "habit": h9}}
    return protokol.get(root_num, protokol[1])

# --- DATABASE BLUEPRINT ---
arketipe_punchy = {
    1: {"inti": "Sang Perintis (Dominator & Visioner Masa Depan)", "kekuatan": ["Daya dobrak tinggi & berani ambil risiko", "Mandiri secara absolut", "Fokus eksekusi"]},
    2: {"inti": "Sang Penyelaras (Negosiator & Pembaca Emosi)", "kekuatan": ["Kapasitas empati tinggi", "Negosiator ulung", "Kemampuan adaptasi emosional"]},
    3: {"inti": "Sang Visioner (Kreator Ide & Komunikator Handal)", "kekuatan": ["Komunikasi memikat", "Kreativitas tanpa batas", "Ahli mencairkan suasana"]},
    4: {"inti": "Sang Transformator (Ahli Strategi & Pembangun Sistem)", "kekuatan": ["Pola pikir sangat terstruktur", "Bisa diandalkan 100%", "Ketelitian tingkat dewa"]},
    5: {"inti": "Sang Penggerak (Eksplorator & Pemecah Kebuntuan)", "kekuatan": ["Kelincahan berpikir", "Inovator pemecah kebuntuan", "Keberanian mengeksplorasi"]},
    6: {"inti": "Sang Harmonizer (Pengayom & Pelindung Natural)", "kekuatan": ["Insting pengayom", "Tanggung jawab moral tinggi", "Loyalitas tanpa pamrih"]},
    7: {"inti": "Sang Legacy Builder (Pemikir Analitik & Spiritualis)", "kekuatan": ["Kemampuan analisa", "Intuisi sering akurat", "Sangat selektif menilai kualitas"]},
    8: {"inti": "Sang Sovereign (Eksekutor Otoritas & Magnet Material)", "kekuatan": ["Tahan banting mental", "Insting bisnis tajam", "Kemampuan memegang kendali"]},
    9: {"inti": "Sang Kesadaran Tinggi (Old Soul & Empati Universal)", "kekuatan": ["Kebijaksanaan luas", "Kepedulian universal", "Melihat 'Big Picture'"]}
}

link_produk = {
    1: "http://lynk.id/neuronada/kj98l4zgzwdw/checkout", 2: "http://lynk.id/neuronada/6z23q03121lg/checkout",
    3: "http://lynk.id/neuronada/0rd6gr7nlzxp/checkout", 4: "http://lynk.id/neuronada/elp83loeyggg/checkout",
    5: "http://lynk.id/neuronada/wne9p4q1l3d9/checkout", 6: "http://lynk.id/neuronada/nm840y6nlo21/checkout",
    7: "http://lynk.id/neuronada/vv0797ll7g7o/checkout", 8: "http://lynk.id/neuronada/ropl1lm6rz8g/checkout",
    9: "http://lynk.id/neuronada/704ke23nzmgx/checkout"
}

def proc_arketipe(nama, angka, zodiak, neptu):
    random.seed(generate_seed(f"hyper_ark_{nama}_{angka}_{zodiak}_{neptu}"))
    buka = random.choice([
        f"Melalui persilangan matriks waktu dan elemen {zodiak}, DNA numerologi **{nama}** mengunci kuat pada **KODE {angka}**.",
        f"Kalkulasi semesta menyempit di **KODE {angka}**. Sejak lahir, alam bawah sadar **{nama}**",
        f"Sistem mendeteksi getaran **KODE {angka}** pada diri Anda. Arsitektur mental **{nama}**",
        f"Berdasarkan algoritma {zodiak} yang melebur dengan weton, cetak biru **{nama}** adalah **KODE {angka}**."
    ])
    inti = {
        1: ["didesain memimpin dan menembus batas.", "dorongan mutlak mandiri dan benci didikte."],
        2: ["Penyelaras yang menetralisir konflik.", "memiliki radar empati tinggi untuk baca emosi."],
        3: ["komunikator handal dengan ide meletup.", "memiliki kreativitas tanpa batas."],
        4: ["arsitek kehidupan yang sistematis.", "berpola pikir logis sebagai pondasi kuat."],
        5: ["simbol kebebasan yang tolak monoton.", "memiliki otak lincah adaptasi cepat."],
        6: ["pelindung sejati dengan insting pengayom.", "memegang tanggung jawab moral tinggi."],
        7: ["pencari kebenaran dengan intuisi tajam.", "menganalisa esensi secara mendalam."],
        8: ["eksekutor tangguh dengan insting material presisi.", "fokus mengejar puncak otoritas."],
        9: ["'Jiwa Tua' yang penuh kebijaksanaan.", "memiliki kepedulian universal melampaui ego."]
    }
    gaya = {
        1: ["Anda alpha inisiator cepat yang lebih suka bertindak."], 2: ["Anda pendengar dan negosiator kolaboratif."],
        3: ["Anda pencipta solusi *out-of-the-box* yang humoris."], 4: ["Anda eksekutor visi terukur tanpa cacat."],
        5: ["Anda paling bersinar pecahkan masalah saat *chaos*."], 6: ["Anda memimpin dengan hati dan loyalitas tinggi."],
        7: ["Anda pengobservasi misterius dan strategis."], 8: ["Anda mengorganisir sumber daya dengan tangan besi elegan."],
        9: ["Anda merangkul keberagaman dan pemberi nasihat bijak."]
    }
    shadow = {
        1: ["Sisi gelap: Rentan kesepian karena tembok ego."], 2: ["Sisi gelap: Menyerap energi beracun (*toxic*) orang lain."],
        3: ["Sisi gelap: Hilang fokus dan bicara impulsif."], 4: ["Sisi gelap: Terlalu kaku dan over-micromanaging."],
        5: ["Sisi gelap: 'Sindrom Cepat Bosan' yang mensabotase."], 6: ["Sisi gelap: Rentan *burnout* urus beban orang lain."],
        7: ["Sisi gelap: *Paralysis by Analysis* (overthinking tanpa aksi)."], 8: ["Sisi gelap: Kesulitan melepas kendali/memaafkan."],
        9: ["Sisi gelap: Patah hati akibat ekspektasi ke manusia."]
    }
    return f"{buka} Anda {random.choice(inti[angka])} {random.choice(gaya[angka])} {random.choice(shadow[angka])}"

def proc_shadow_list(nama, angka):
    random.seed(generate_seed(f"shd_{nama}_{angka}"))
    semua_shadow = {
        1: ["Gengsi minta tolong saat memikul beban", "Membangun tembok ego untuk menutupi sepi", "Overthinking merasa hasil belum sempurna"],
        2: ["Mengorbankan kebahagiaan demi ekspektasi", "Sulit berkata TIDAK (People Pleaser)", "Memendam amarah hindari konflik"],
        3: ["Menyembunyikan gelisah di balik topeng ceria", "Cepat kehilangan motivasi", "Insomnia karena over-analisa"],
        4: ["Stres parah jika rencana mendadak berubah", "Terjebak zona nyaman takut risiko", "Sering dinilai terlalu dingin"],
        5: ["Sindrom Bosan mensabotase karya", "Kelelahan saraf otak jalan terus", "Lari (escapism) saat ditekan"],
        6: ["Burnout mengurus hidup orang lain", "Sikap Over-Protective mengekang", "Rasa bersalah jika me time"],
        7: ["Menganalisa terus tanpa aksi (Paralysis)", "Merasa terasing/tak sepemikiran", "Mencurigai niat baik orang"],
        8: ["Sulit melepaskan kontrol/memaafkan", "Memaksa tubuh abaikan alarm lelah", "Ketakutan berlebih menjadi lemah"],
        9: ["Memaklumi toxic atas nama kasihan", "Patah hati akibat ekspektasi manusia", "Kelelahan memikirkan beban semesta"]
    }
    return random.sample(semua_shadow[angka], 3)

def proc_couple_persona(root_c, n1, n2):
    random.seed(generate_seed(f"cp_{n1}_{n2}_{root_c}"))
    buka = random.choice([
        f"Ketika vibrasi **{n1}** dan **{n2}** dilebur, hasilnya mengunci di **Root {root_c}**.",
        f"Hukum resonansi persatuan **{n1}** dan **{n2}** menghasilkan gelombang **Root {root_c}**."
    ])
    desc = {
        1: ("THE POWER COUPLE", f"Entitas alpha ambisius. Kalian fokus pada pencapaian karir."),
        2: ("THE SOULMATES", f"Kalian memiliki 'Wi-Fi' batin. Mudah memahami emosi pasangan tanpa banyak kata."),
        3: ("THE SOCIALITES", f"Aura magnetis. Kalian adalah pasangan menyenangkan yang menghidupkan suasana."),
        4: ("THE BUILDERS", f"Berpijak pada bumi. Fokus kalian adalah membangun aset dan kesetiaan mutlak."),
        5: ("THE ADVENTURERS", f"Energi kebebasan. Kalian butuh kejutan dan tantangan agar cinta tetap menyala."),
        6: ("THE FAMILY FIRST", f"Simbol pengayoman. Pengorbanan merawat keutuhan rumah tangga sangat dalam."),
        7: ("THE DEEP SEEKERS", f"Hubungan eksklusif. Kalian membangun koneksi intelektual dengan privasi tinggi."),
        8: ("THE EMPIRE", f"Magnet kelimpahan. Penyatuan ego mengejar kesuksesan bisnis dan membangun kerajaan."),
        9: ("THE HEALERS", f"Puncak empati. Interaksi penuh toleransi dan penyembuhan bagi sirkel sekitar.")
    }
    return desc.get(root_c, ("UNCHARTED SYNERGY", "Anomali energi tak tertebak."))[0], f"{buka} {desc.get(root_c)[1]}"

def proc_weton_kombo(sisa, n1, n2, z1, z2):
    random.seed(generate_seed(f"wt_{n1}_{n2}_{sisa}_{z1}_{z2}"))
    do_list = {
        1: [f"Gunakan teknik *Pacing-Leading*. Validasi dulu emosi {n2} dengan mendengarkan aktif.", f"Beri jeda *Time-Out* saat perdebatan menajam."],
        2: [f"Jadikan {n2} *Partner Mastermind*. Libatkan ia dalam diskusi visi masa depan.", f"Bangun *Rapport* berbasis pencapaian bersama."],
        3: [f"Ciptakan *Pattern Interrupt*. Lakukan kencan dadakan pancing dopamin.", f"Pancing *deep-talk* rutin bulanan."],
        4: [f"Kuasai teknik *Reframing*. Pandang krisis sebagai tim: 'Kita vs Masalah'.", f"Perkuat daya tahan mental di fase adaptasi."],
        5: [f"Gelar sesi 'Visi Masa Depan'. Transparansi kunci magnet rezeki.", f"Sinkronkan frekuensi kelimpahan. Tarik pasangan ke mode optimis."],
        6: [f"Berikan *Space* saat tensi naik. Mundur selangkah.", f"Gunakan humor sebagai penetralisir racun ketegangan."],
        7: [f"Komunikasi berbasis fakta. Klarifikasi pesan agar tidak asumsi.", f"Tingkatkan intensitas bahasa cinta primer pasangan."],
        8: [f"Pertahankan *Rapport* dengan hobi baru bersama.", f"Keluarlah dari zona nyaman rutinitas kalian berdua."]
    }
    dont_list = {
        1: [f"DILARANG KERAS asumsi niat jahat {n2} tanpa klarifikasi.", f"Pantang konfrontasi saat kondisi *H.A.L.T* (Lapar, Marah, Lelah)."],
        2: [f"Hindari jebakan pencitraan bahagia di luar tapi dingin di dalam.", f"Jangan biarkan intervensi keluarga/teman merusak wibawa rumah tangga."],
        3: [f"Hati-hati ilusi *Comfort Zone*. Jangan malas berjuang.", f"Jangan abaikan perawatan diri karena merasa sudah 'aman'."],
        4: [f"Jangan jadikan gengsi senjata penikam. Kompromi krusial.", f"Pantang ucapkan kata perpisahan saat emosi memuncak."],
        5: [f"Jangan jadikan uang satu-satunya perekat jiwa.", f"Dilarang meremehkan orang lain saat rezeki pasangan terbuka."],
        6: [f"Jangan serang kelemahan masa lalu/harga diri saat berdebat.", f"Dilarang mendiamkan pasangan (*Silent Treatment*) lebih dari 24 jam."],
        7: [f"DILARANG MENGGUNAKAN kata absolut: 'Kamu TIDAK PERNAH peduli!'.", f"Jangan mengintai ponsel pasangan. *Trust issue* mematikan cinta."],
        8: [f"Waspadai menggampangkan pasangan. Teruslah beri *effort*.", f"Jangan biarkan rutinitas mematikan romantisme."]
    }
    hasil = {
        1: ("💔 PEGAT (Ujian Ego)", "Sering adu argumen tajam karena ego defensif bawaan."),
        2: ("👑 RATU (Kharisma Pasangan)", "Kehadiran kalian memicu respek alami dari lingkungan."),
        3: ("💞 JODOH (Sinkronisasi Alami)", "Koneksi batin instan, seolah frekuensi jiwa sudah pernah terhubung."),
        4: ("🌱 TOPO (Ujian Bertumbuh)", "Awal penuh gesekan, tapi jika lolos, pondasi tak tertembus badai."),
        5: ("💰 TINARI (Magnet Rezeki)", "Entitas memancarkan kelimpahan. Macet finansial mendadak terurai."),
        6: ("⚡ PADU (Beda Frekuensi)", "Sering letupan perdebatan karena beda filter logika."),
        7: ("👁️ SUJANAN (Rawan Asumsi)", "Vibrasi energi rawan menarik miskomunikasi dan cemburu buta."),
        8: ("🕊️ PESTHI (Damai & Rukun)", "Adem ayem, kehadiran fisik menetralisir stres kehidupan.")
    }
    return hasil[sisa][0], hasil[sisa][1], random.choice(do_list[sisa]), random.choice(dont_list[sisa])

def proc_penjelasan_matriks(n1, n2, eso_val, nep_val):
    random.seed(generate_seed(f"pm_v2_{n1}_{n2}_{eso_val}_{nep_val}"))
    header = random.choice(["⚙️ ARSITEKTUR ANALISA", "📡 DEKODE SINYAL KOSMIK"])
    f_eso = random.choice([f"Fusi nama mengunci <b>{eso_val}</b>.", f"Sandi menghasilkan <b>{eso_val}</b>."])
    f_nep = random.choice([f"Sinkronisasi waktu Neptu <b>{nep_val}</b> memetakan ego.", f"Analisa siklus Neptu <b>{nep_val}</b> menjadi radar emosi."])
    return f'<div class="info-metric-box"><b style="color:#FFD700; font-size:14px;">{header}:</b><br>• <b style="color:white;">TOTAL ESOTERIK:</b> {f_eso}<br>• <b style="color:white;">TOTAL NEPTU:</b> {f_nep}</div>'

KAMUS_ABJAD = {'a':1,'b':2,'j':3,'d':4,'h':5,'w':6,'z':7,'t':9,'y':10,'k':20,'l':30,'m':40,'n':50,'s':60,'f':80,'q':100,'r':200,'c':3,'e':5,'g':1000,'i':10,'o':6,'p':80,'u':6,'v':6,'x':60}
def hitung_nama_esoterik(nama): return sum(KAMUS_ABJAD.get(h,0) for h in ''.join(filter(str.isalpha, str(nama).lower()))) or 1
def get_rincian_esoterik(nama): 
    r = [f"{h.upper()}({KAMUS_ABJAD.get(h,0)})" for h in ''.join(filter(str.isalpha, str(nama).lower())) if KAMUS_ABJAD.get(h,0)>0]
    return " + ".join(r) if r else "0"

def generate_dynamic_reading(total_jummal):
    mod = total_jummal % 4 if total_jummal % 4 != 0 else 4
    el = {1: ("🔥 API (Nar)", "Sistem saraf eksekusi cepat."), 2: ("🌍 TANAH (Turab)", "Fondasi logis dan membumi."), 3: ("💨 UDARA (Hawa)", "Konseptor ide tanpa henti."), 4: ("💧 AIR (Ma')", "Emosional peka, empati adaptif.")}
    p_red = " + ".join(list(str(total_jummal)))
    s_red = sum(int(d) for d in str(total_jummal))
    r_num = s_red
    while r_num > 9: r_num = sum(int(d) for d in str(r_num))
    r_dict = {1:"Pencipta jalan baru", 2:"Penyelaras harmoni", 3:"Penyampai pesan", 4:"Pembangun sistem", 5:"Agen transformasi", 6:"Pengayom sejati", 7:"Pencari esensi", 8:"Pemegang kendali", 9:"Kesadaran universal"}
    m_note = "<div style='background:rgba(212,175,55,0.1); padding:10px; border-radius:5px;'><span style='color:#FFD700;'>⚡ <b>KODE MASTER:</b></span> Intuisi Spiritual Tinggi Terdeteksi.</div>" if any(m in str(total_jummal) for m in ["11","22","33"]) else ""
    return el[mod][0], el[mod][1], p_red, s_red, r_num, r_dict.get(r_num,""), m_note

def hitung_angka(tanggal):
    try:
        t = sum(int(d) for d in tanggal.strftime("%d%m%Y"))
        while t > 9: t = sum(int(d) for d in str(t))
        return t
    except: return 1

def get_rincian_tanggal(tanggal):
    try:
        ts = tanggal.strftime("%d%m%Y")
        p = f"{' + '.join(list(ts))} = {sum(int(d) for d in ts)}"
        t = sum(int(d) for d in ts)
        while t > 9:
            p += f" ➡ {' + '.join(list(str(t)))} = {sum(int(d) for d in str(t))}"
            t = sum(int(d) for d in str(t))
        return p
    except: return "1 = 1"

def hitung_neptu_langsung(hari, pasaran): return {"Minggu":5,"Senin":4,"Selasa":3,"Rabu":7,"Kamis":8,"Jumat":6,"Sabtu":9}.get(hari,0) + {"Legi":5,"Pahing":9,"Pon":7,"Wage":4,"Kliwon":8}.get(pasaran,0)
 
def get_betaljemur_data(neptu, hari):
    lk = {7:("Lebu Katiup Angin","Pikiran dinamis"),8:("Lakuning Geni","Emosi meledak-ledak"),9:("Lakuning Angin","Adaptif namun labil"),10:("Pandito Mbangun Teki","Introspektif, cerdas"),11:("Aras Tuding","Pemberani, ditunjuk peluang"),12:("Aras Kembang","Menebar pesona"),13:("Lakuning Lintang","Magnetis menyendiri"),14:("Lakuning Rembulan","Penenang batin"),15:("Lakuning Srengenge","Pencerah logis"),16:("Lakuning Banyu","Ketenangan mematikan"),17:("Lakuning Bumi","Sabar membumi"),18:("Lakuning Paripurna","Pemegang kendali bijak")}
    nd = {"Minggu":"Timur", "Senin":"Selatan", "Selasa":"Barat", "Rabu":"Utara", "Kamis":"Timur", "Jumat":"Selatan", "Sabtu":"Selatan"}
    return lk.get(neptu,("Anomali",""))[0], lk.get(neptu,("Anomali",""))[1], nd.get(hari,"Netral")

def get_rezeki_usaha(neptu):
    r = {1:("Wasesa Segara","Rezeki seluas lautan"),2:("Tunggak Semi","Patah tumbuh hilang berganti"),3:("Satria Wibawa","Dihormati kolega"),4:("Sumur Sinaba","Menjadi referensi membawa berkah"),5:("Bumi Kapetak","Kerja cerdas dan keras"),6:("Satria Wirang","Rawan rintangan"),7:("Lebu Katiup Angin","Wajib punya aset tetap")}[neptu%7 or 7]
    u = {1:("Sandang","Bisnis komoditas"),2:("Pangan","Kuliner/ritel"),3:("Beja","Instrumen investasi"),4:("Lara","Butuh partner mitigasi"),5:("Pati","Hindari spekulasi buta")}[neptu%5 or 5]
    return r, u
 
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

def get_safe_firstname(name_str, default="User"): return str(name_str).strip().split()[0].upper() if str(name_str).strip() else default

# --- SIDEBAR PROMOSI & LOGIN ---
with st.sidebar:
    # BANNER CSS KILLER MENGGANTIKAN BARU.JPG
    st.markdown("""
    <div class="soft-fade" style="background: radial-gradient(circle at center, #2b1d05 0%, #050505 100%); padding: 25px 15px; border-radius: 12px; border: 1px solid #D4AF37; text-align: center; margin-bottom: 25px; box-shadow: 0 5px 25px rgba(212,175,55,0.2); position: relative; overflow: hidden;">
        <h2 style="margin:0; color:#FFD700; font-weight:900; letter-spacing: 3px; font-size: 24px; text-transform: uppercase; text-shadow: 0 2px 10px rgba(255,215,0,0.5);">NEURON AI</h2>
        <div style="background: #ff4b4b; color: white; font-size: 10px; font-weight: bold; letter-spacing: 2px; padding: 3px 10px; border-radius: 20px; display: inline-block; margin-top: 5px; margin-bottom: 12px;">ULTIMATE OS</div>
        <p style="color:#e0e0e0; font-size:12px; line-height:1.5; margin:0; letter-spacing: 1px;">DECODE YOUR DESTINY<br><span style="color:#888;">HACK YOUR REALITY</span></p>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown(f"### {get_greeting()}")
    
    # SYSTEM LOCK / MEMBERSHIP
    st.markdown("---")
    st.markdown("### 🔓 Akses Premium")
    if not st.session_state.premium:
        kode_input = st.text_input("Punya Kode Akses? Ketik di sini:", type="password")
        if kode_input:
            if kode_input.upper() == "NEUROVIP":
                st.session_state.premium = True
                st.success("✅ Akses Terbuka! Selamat Datang.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Kode Salah atau Kadaluarsa.")
        st.markdown("<p style='font-size:13px; color:#888;'>Dapatkan Kode Akses via <a href='https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuron%20AI.' target='_blank' style='color:#25D366; font-weight:bold; text-decoration:none;'>WhatsApp</a></p>", unsafe_allow_html=True)
    else:
        st.success("👑 Status: VIP MEMBER")
        if st.button("Logout"):
            st.session_state.premium = False
            st.rerun()
    
    # WA CTA (URGENT & AGGRESSIVE)
    st.markdown("---")
    st.markdown("""<div style='background: linear-gradient(135deg, #ff0000 0%, #8b0000 100%); padding: 18px; border-radius: 10px; text-align: center; border: 1px solid #ff4b4b; box-shadow: 0 5px 15px rgba(255,0,0,0.3);'>
<b style='color: white; font-size: 16px; letter-spacing: 1px;'>🔥 BUTUH ANALISA LEBIH DALAM?</b><br>
<span style='color: #ccc; font-size: 12px; display:block; margin-top:5px;'>Beberapa hasil tidak bisa ditampilkan di sistem.</span>
<span style='color: #FFD700; font-size: 13px; display:inline-block; margin-top:5px; margin-bottom:12px;'>Konsultasi langsung dengan Coach (Slot Terbatas Hari Ini)</span><br>
<a href='https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20butuh%20sesi%20kalibrasi%20private%20hari%20ini' target='_blank' style='background: #25D366; color: white; padding: 10px 20px; border-radius: 25px; text-decoration: none; font-weight: 900; font-size: 14px; display: inline-block; box-shadow: 0 4px 10px rgba(37,211,102,0.4);'>💬 KLIK DI SINI SEKARANG</a>
</div>""", unsafe_allow_html=True)
    st.markdown("<br><center><small style='color:#666;'>© 2026 Neuron AI Academy</small></center>", unsafe_allow_html=True)
 
# --- INTERFACE UTAMA (HERO SECTION) ---
cur_planet, cur_instr, cur_color = get_planetary_hour()
st.markdown(f"""<div style='text-align: right;'><div class='live-badge' style='background: {cur_color};'>🕒 LIVE PLANET: {cur_planet.upper()}</div><div style='font-size: 11px; color: #888; margin-top: 5px;'>{cur_instr}</div></div>""", unsafe_allow_html=True)
 
st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900; color:#FFD700; letter-spacing: 1px;'>🌌 BUKA KODE HIDUP ANDA HARI INI</h1>", unsafe_allow_html=True)
st.markdown("""<p style='text-align: center; font-size: 16px; color: #ccc;'>Bukan ramalan biasa. Ini adalah hasil decoding energi nama, tanggal lahir, dan siklus waktu Anda.<br><br><b style='color:#FFF;'>⚡ Dalam 10 detik, Anda akan tahu:</b><br><span style='color:#D4AF37;'>• Arah rezeki hari ini<br>• Keputusan yang HARUS diambil<br>• Risiko yang WAJIB dihindari</span></p>""", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; margin-bottom:20px;'><span style='background:rgba(255,75,75,0.2); color:#ff4b4b; padding:8px 15px; border-radius:5px; font-size:13px; font-weight:bold; letter-spacing:1px;'>⚠️ Jangan baca ini kalau belum siap tahu kebenaran tentang diri Anda.</span></div>", unsafe_allow_html=True)
st.markdown("---")
 
tgl_today = datetime.date.today()
tab1, tab2, tab5, tab3, tab4 = st.tabs(["👤 Personal Identity", "👩‍❤️‍👨 Couple Matrix 🔒", "⏱️ Quantum Engine 🔒", "🌌 Falak Ruhani 🔒", "📚 FAQ"])
 
# ==========================================
# TAB 1: IDENTITAS KOSMIK (HOOK & PAYWALL)
# ==========================================
with tab1:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#fff;'>👇 Masukkan data Anda sekarang</h4>", unsafe_allow_html=True)
    nama_user = st.text_input("Nama Lengkap:", placeholder="Ketik nama asli Anda...", key="t1_nama")
    
    col_tgl, col_wt = st.columns(2)
    with col_tgl:
        st.write("📅 **Data Masehi:**")
        tgl_input = st.date_input("Tanggal Lahir", value=datetime.date(1983, 9, 23), min_value=datetime.date(1900, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")
    with col_wt:
        st.write("📜 **Data Weton:**")
        hari_input = st.selectbox("Hari", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4, key="h_t1")
        pasaran_input = st.selectbox("Pasaran", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=2, key="p_t1")
    st.markdown("</div>", unsafe_allow_html=True)
 
    if st.button("🔓 Buka Hasil Saya"):
        if not nama_user or len(nama_user.strip()) < 3: 
            st.error("🚨 Mohon ketik nama lengkap Anda (minimal 3 huruf).")
        else:
            try:
                with st.spinner('Menyelaraskan frekuensi kosmik...'):
                    time.sleep(1.5)
                
                safe_name = get_safe_firstname(nama_user)
                angka_hasil = hitung_angka(tgl_input)
                rincian_tgl = get_rincian_tanggal(tgl_input)
                
                nilai_jummal = hitung_nama_esoterik(nama_user)
                rincian_jummal = get_rincian_esoterik(nama_user)
                el_nama, el_desc, p_reduk, s_reduk, r_num, r_desc, m_note = generate_dynamic_reading(nilai_jummal)
                
                nep = hitung_neptu_langsung(hari_input, pasaran_input)
                wet = f"{hari_input} {pasaran_input}"
                zod = get_zodiak(tgl_input)
                
                n_laku, d_laku, arah_naga = get_betaljemur_data(nep, hari_input)
                rezeki_data, usaha_data = get_rezeki_usaha(nep)
                
                punchy = arketipe_punchy.get(angka_hasil, arketipe_punchy[1])
                desk_ark_dinamis = proc_arketipe(safe_name, angka_hasil, zod, nep)
                shadow = proc_shadow_list(safe_name, angka_hasil)
                
                # --- HASIL CEPAT 10 DETIK (HOOK - SELALU MUNCUL) ---
                st.markdown(f"""<div class="soft-fade" style="background: rgba(255,215,0,0.1); border-left: 5px solid #FFD700; padding: 25px; border-radius: 12px; margin-bottom: 25px; border: 1px solid rgba(255,215,0,0.3);">
<h3 style="margin-top:0; color:#FFD700; font-weight:900; letter-spacing:1px;">🎯 HASIL ANDA HARI INI</h3>
<ul style="font-size: 17px; line-height: 1.8; color: #fff; list-style-type: none; padding-left: 0;">
<li style="margin-bottom: 10px;">💰 <b>REZEKI:</b> <span style="color:#25D366; font-weight:bold;">TERBUKA</span> <i style="color:#aaa; font-size:14px;">(Momentum tinggi - {rezeki_data[0]})</i></li>
<li style="margin-bottom: 10px;">⚡ <b>AKSI:</b> Hubungi seseorang yang sudah lama Anda tunda.</li>
<li style="margin-bottom: 10px;">🚫 <b>LARANGAN:</b> Jangan ambil keputusan finansial besar hari ini (Waspadai sifat {shadow[0].lower()}).</li>
</ul>
<div style="background: rgba(255,75,75,0.2); padding: 8px 15px; border-radius: 5px; display: inline-block; margin-top: 10px;">
<b style="color:#ff4b4b; font-size:13px;">⏳ Energi ini hanya berlaku sampai 24 jam ke depan</b>
</div>
</div>""", unsafe_allow_html=True)
                
                # --- PAYWALL: CEK STATUS PREMIUM ---
                if not st.session_state.premium:
                    st.markdown("""<div class="glass-container soft-fade" style="text-align:center; border: 2px solid #ff4b4b; padding: 30px 20px;">
<h3 style="color:#ff4b4b; margin-top:0;">🔓 Anda baru melihat 20% dari hasil Anda...</h3>
<div style="background: rgba(0,0,0,0.4); padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: left; display: inline-block;">
<span style="color:#ccc; font-size: 15px;">Di dalam analisa lengkap:</span><br>
<b style="color:#fff;">• Blueprint kepribadian terdalam Anda</b><br>
<b style="color:#fff;">• Titik kebocoran rezeki Anda</b><br>
<b style="color:#fff;">• Strategi spesifik 60 menit ke depan</b><br>
<b style="color:#fff;">• Analisa hubungan & jodoh (jika ada pasangan)</b>
</div>
<p style="color:#FFD700; font-size: 16px;"><b>🔥 Ini bukan informasi umum.<br>Ini PERSONAL — hanya untuk Anda.</b></p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuron%20AI." target="_blank" style="text-decoration:none;">
<div class="cta-button" style="font-size:18px; margin-top: 10px;">🚀 AKTIFKAN ANALISA LENGKAP</div>
</a>
<p style="font-size:14px; color:#ccc; margin-top:15px; margin-bottom: 5px;">Hanya <b>Rp 19.000</b><br><i style="color:#888;">(Lebih murah dari kopi, tapi bisa ubah arah hidup Anda)</i></p>
<span style="background:rgba(255,75,75,0.2); color:#ff4b4b; padding:4px 10px; border-radius:3px; font-size:12px; font-weight:bold;">⚠️ Harga bisa naik kapan saja | Akses langsung terbuka</span>
<div style="margin-top: 25px; border-top: 1px dashed #555; padding-top: 15px;">
<span style="font-size:14px; color:#25D366; font-weight:bold;">🔥 1.287 orang sudah membuka analisa mereka hari ini.</span><br>
<span style="font-size:13px; color:#888;">Jangan jadi yang ketinggalan momentum.</span>
</div>
</div>""", unsafe_allow_html=True)
                else:
                    # --- DEEP ANALYSIS (HANYA JIKA PREMIUM) ---
                    st.markdown(f"<h3 style='text-align:center;'>🌌 Deep Analysis: {safe_name}</h3>", unsafe_allow_html=True)
                    st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Nilai Esoterik</div><div class="matrix-value matrix-value-special">{nilai_jummal}</div></div><div class="matrix-item"><div class="matrix-label">Elemen Dasar</div><div class="matrix-value">{el_nama.split(' ')[1] if len(el_nama.split(' '))>1 else el_nama}</div></div><div class="matrix-item"><div class="matrix-label">Meta-Program</div><div class="matrix-value matrix-value-special">KODE {angka_hasil}</div></div><div class="matrix-item"><div class="matrix-label">Filter Zodiak</div><div class="matrix-value">{zod}</div></div><div class="matrix-item"><div class="matrix-label">Energi Weton</div><div class="matrix-value">{wet} ({nep})</div></div></div>""", unsafe_allow_html=True)
                    st.markdown(f"""<div class="dynamic-reading-box soft-fade"><h4 style="color: #FFD700; margin-top:0;">🔍 Bedah DNA Angka & Waktu Lahir</h4><p><b>1. Sandi Esoterik Nama (Hisab Jummal)</b><br><code style="color:#25D366; background:transparent; padding:0;">{rincian_jummal} = <b>{nilai_jummal}</b></code></p><ul style="margin-left: -15px; margin-bottom: 20px;"><li><b>Elemen Bawah Sadar:</b> {el_nama} - <i style="color:#aaa;">{el_desc}</i></li><li><b>Inti Jiwa (Root Number):</b> {p_reduk} = {s_reduk} ➡ <b>{r_num}</b> ({r_desc})</li></ul><p><b>2. Sandi Waktu Lahir (Meta-Program NLP)</b><br><code style="color:#FFD700; background:transparent; padding:0;">{rincian_tgl}</code><br><span style="font-size:14px; color:#ccc;">Maka didapatkan <b>KODE {angka_hasil}</b>. Angka ini adalah <i>Blueprint</i> otak <b>{safe_name}</b> memproses informasi.</span></p>{m_note}</div>""", unsafe_allow_html=True)
                    st.markdown(f"""<div class="primbon-box soft-fade"><div style="text-align:center; border-bottom:1px solid #D4AF37; padding-bottom:10px; margin-bottom:15px;"><span style="color:#D4AF37; font-size:14px; font-weight:900; letter-spacing:2px;">📜 PETHIKAN KITAB BETALJEMUR ADAMMAKNA</span></div><div style="font-size:15px; line-height:1.6; margin-bottom: 15px;"><b style="color:#FFF; font-size:18px;">{n_laku}</b> — <i style="color:#ccc;">"{d_laku}"</i></div><div style="font-size:15px; line-height:1.6; margin-bottom: 15px; border-top: 1px dashed #555; padding-top: 10px;">• <b>Rezeki (<span style="color:#FFD700;">{rezeki_data[0]}</span>):</b> <i style="color:#ccc;">{rezeki_data[1]}</i><br>• <b>Usaha (<span style="color:#25D366;">{usaha_data[0]}</span>):</b> <i style="color:#ccc;">{usaha_data[1]}</i></div><div style="font-size:15px; line-height:1.6; background: rgba(212,175,55,0.1); padding: 10px; border-radius: 8px;"><span style="color:#FFD700;">🧭 <b>NAGA DINA (Arah Kejayaan Hari {hari_input}):</b></span> <b style="font-size: 16px;">{arah_naga}</b><br><i style="color:#888; font-size:13px;">*ACTIONABLE: Posisikan diri Anda menghadap <b>{arah_naga}</b> saat mengambil keputusan penting hari ini.</i></div></div>""", unsafe_allow_html=True)
                    st.markdown(f"### 👁️ Decode Kepribadian Dinamis: {safe_name}")
                    st.info(f"Mengacu pada pola unik {safe_name}, arketipe utama dikunci sebagai:\n\n**{punchy['inti']}**")
                    st.write(desk_ark_dinamis)
                    
                    c_kekuatan, c_shadow = st.columns(2)
                    with c_kekuatan:
                        st.markdown(f"🔥 **KEKUATAN DOMINAN:**")
                        st.markdown(f"<ul class='list-punchy' style='color:#25D366;'><li>{punchy['kekuatan'][0]}</li><li>{punchy['kekuatan'][1]}</li><li>{punchy['kekuatan'][2]}</li></ul>", unsafe_allow_html=True)
                    with c_shadow:
                        st.markdown(f"⚠️ **SHADOW TERSEMBUNYI:**")
                        st.markdown(f"<ul class='list-punchy' style='color:#ff4b4b;'><li>{shadow[0]}</li><li>{shadow[1]}</li><li>{shadow[2]}</li></ul>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Sistem gagal melakukan komputasi: {e}")
 
# ==========================================
# TAB 2: COUPLE MATRIX (LOCKED)
# ==========================================
with tab2:
    if not st.session_state.premium:
        st.markdown("""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h3 style='color: #ff4b4b; font-weight: 900; margin-top:0;'>💞 CEK KECOCOKAN ANDA & DIA</h3>
<p style='color: #ccc; font-size: 16px; margin-bottom: 20px;'>Apakah hubungan ini:<br><b style='color:#ff4b4b;'>❤️ JODOH?</b> | <b style='color:#FFD700;'>⚡ Ujian?</b> | <b style='color:#888;'>💔 Atau sebenarnya tidak cocok?</b></p>
<p style='font-size: 14px; color: #aaa; margin-bottom: 30px;'>Masukkan 2 nama dan lihat hasilnya sekarang.<br><i style='color:#ff4b4b;'>⚠️ Banyak yang kaget setelah lihat hasilnya.</i></p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuron%20AI." target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 DAPATKAN KODE VIA WHATSAPP (Rp 19.000)</div>
</a>
<p style='font-size:13px; color:#25D366; font-weight:bold; margin-top:15px;'>🔥 1.287 orang sudah membuka analisa mereka hari ini.</p>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("💞 Penyatuan Esoterik & Betaljemur (Couple Matrix)")
        ca, cb = st.columns(2)
        with ca: 
            st.markdown("<h4 style='color:#FFD700;'>Pihak 1 (Pria)</h4>", unsafe_allow_html=True)
            n1 = st.text_input("Nama Anda", key="n1_c")
            d1 = st.date_input("Lahir Masehi", value=datetime.date(1995, 1, 1), format="DD/MM/YYYY", key="d1_c")
            hc1 = st.selectbox("Hari Pria", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4, key="hc1")
            pc1 = st.selectbox("Pasaran Pria", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=2, key="pc1")
        with cb: 
            st.markdown("<h4 style='color:#FF69B4;'>Pihak 2 (Wanita)</h4>", unsafe_allow_html=True)
            n2 = st.text_input("Nama Pasangan", key="n2_c")
            d2 = st.date_input("Lahir Wanita", value=datetime.date(1995, 1, 1), format="DD/MM/YYYY", key="d2_c")
            hc2 = st.selectbox("Hari Wanita", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=2, key="hc2")
            pc2 = st.selectbox("Pasaran Wanita", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=0, key="pc2")
        st.markdown("</div>", unsafe_allow_html=True)
            
        if st.button("🚀 Lihat Nasib Saya Hari Ini", key="btn_couple"):
            if str(n1).strip() and str(n2).strip():
                try:
                    with st.spinner('Menghitung benturan energi pasangan...'):
                        time.sleep(1.5)
                    
                    safe_n1, safe_n2 = get_safe_firstname(n1, "Pria"), get_safe_firstname(n2, "Wanita")
                    zod1, zod2 = get_zodiak(d1), get_zodiak(d2)
                    nep_1, nep_2 = hitung_neptu_langsung(hc1, pc1), hitung_neptu_langsung(hc2, pc2)
                    sel = abs(hitung_angka(d1) - hitung_angka(d2))
                    
                    jummal_1, jummal_2 = hitung_nama_esoterik(n1), hitung_nama_esoterik(n2)
                    total_couple = jummal_1 + jummal_2
                    root_c = total_couple
                    while root_c > 9: root_c = sum(int(d) for d in str(root_c))
                    
                    c_title, c_desc = proc_couple_persona(root_c, safe_n1, safe_n2)
                    judul_jodoh, desk_jodoh, d_do, d_dont = proc_weton_kombo((nep_1+nep_2)%8 or 8, safe_n1, safe_n2, zod1, zod2)
                    
                    st.markdown(f"### 🔮 The Unified Resonance: {safe_n1} & {safe_n2}")
                    st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Neptu {safe_n1}</div><div class="matrix-value">{hc1} {pc1} ({nep_1})</div></div><div class="matrix-item"><div class="matrix-label">Neptu {safe_n2}</div><div class="matrix-value">{hc2} {pc2} ({nep_2})</div></div><div class="matrix-item" style="background: rgba(212,175,55,0.2);"><div class="matrix-label" style="color:#FFD700;">TOTAL NEPTU</div><div class="matrix-value matrix-value-special">{nep_1 + nep_2}</div></div><div class="matrix-item"><div class="matrix-label">Total Esoterik</div><div class="matrix-value">{total_couple}</div></div></div>""", unsafe_allow_html=True)
                    st.markdown(proc_penjelasan_matriks(safe_n1, safe_n2, total_couple, (nep_1+nep_2)), unsafe_allow_html=True)
                    st.markdown(f'<div class="dynamic-reading-box soft-fade" style="border-left-color: #25D366;"><h4 style="color: #25D366; margin-top:0;">🧬 Persona Pasangan: {c_title}</h4><p><i>{c_desc}</i></p></div>', unsafe_allow_html=True)
                    st.info(f"**Titik Benturan Weton ({judul_jodoh}):**\n{desk_jodoh}")
                    
                    if sel in [0, 3, 6, 9]: st.success(f"💘 **SKOR META-PROGRAM (NLP): Sangat Sinkron**")
                    elif sel in [1, 2, 8]: st.warning(f"⚖️ **SKOR META-PROGRAM (NLP): Dinamis** - Butuh toleransi.")
                    else: st.error(f"🔥 **SKOR META-PROGRAM (NLP): Rawan Gesekan**")
         
                    c_do_c, c_dont_c = st.columns(2)
                    with c_do_c: st.markdown(f"<div class='soft-fade' style='background:rgba(37,211,102,0.1); padding:20px; border-radius:10px; border:1px solid #25D366; height:100%;'><b style='color:#25D366; font-size:16px;'>✅ LAKUKAN INI:</b><br><br><span style='color:#e0e0e0; line-height:1.6;'>{d_do}</span></div>", unsafe_allow_html=True)
                    with c_dont_c: st.markdown(f"<div class='soft-fade' style='background:rgba(255,75,75,0.1); padding:20px; border-radius:10px; border:1px solid #ff4b4b; height:100%;'><b style='color:#ff4b4b; font-size:16px;'>❌ HINDARI INI:</b><br><br><span style='color:#e0e0e0; line-height:1.6;'>{d_dont}</span></div>", unsafe_allow_html=True)
                except Exception as e: st.error(f"Error komputasi: {e}")

# ==========================================
# TAB 5: QUANTUM ENGINE (LOCKED)
# ==========================================
with tab5:
    if not st.session_state.premium:
        st.markdown("""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h2 style='color: #ff4b4b; font-weight: 900;'>🔒 FITUR PREMIUM DIKUNCI</h2>
<p style='color: #ccc; font-size: 16px; margin-bottom: 30px;'>Anda sedang mengakses versi Gratis. Buka akses <b>Tactical Action Plan (Pemetaan Aksi Taktis Harian)</b> yang dikalibrasi real-time dengan energi planet Anda.</p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuron%20AI." target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 DAPATKAN KODE VIA WHATSAPP (Rp 19.000)</div>
</a>
<p style='font-size:13px; color:#25D366; font-weight:bold; margin-top:15px;'>🔥 1.287 orang sudah membuka analisa mereka hari ini.</p>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("⏱️ Live Cosmic Dashboard (Fate Hacking)")
        qe_nama = st.text_input("Nama Panggilan:", key="qe_n")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🚀 Lihat Nasib Saya Hari Ini", key="btn_qe"):
            if qe_nama:
                with st.spinner('Menarik data pergerakan planet...'):
                    time.sleep(1.2)
                
                safe_qe = get_safe_firstname(qe_nama)
                jummal_qe = hitung_nama_esoterik(qe_nama)
                mod_harian = (jummal_qe + sum(int(d) for d in tgl_today.strftime("%d%m%Y"))) % 7
                
                sun_fase, sun_desc = get_sun_phase()
                planet_live, planet_desc, planet_color = get_planetary_hour()
                
                siklus_nama, html_plan = proc_tactical_plan(safe_qe, mod_harian, planet_live, planet_desc, sun_fase, sun_desc)
                
                st.markdown(f"### 📡 Live Dashboard: {safe_qe}")
                st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Fase Harian</div><div class="matrix-value">{siklus_nama.split('(')[0].strip()}</div></div><div class="matrix-item"><div class="matrix-label">Matahari</div><div class="matrix-value matrix-value-special">{sun_fase.split(' ')[0]}</div></div><div class="matrix-item" style="border-bottom: 2px solid {planet_color};"><div class="matrix-label">Jam Planet</div><div class="matrix-value" style="color:{planet_color};">{planet_live}</div></div></div>""", unsafe_allow_html=True)
                
                st.markdown(html_plan, unsafe_allow_html=True)

# ==========================================
# TAB 3: FALAK RUHANI (LOCKED)
# ==========================================
with tab3:
    if not st.session_state.premium:
        st.markdown("""<div class='glass-container soft-fade' style='text-align: center; padding: 40px 20px;'>
<h2 style='color: #ff4b4b; font-weight: 900;'>🔒 FITUR PREMIUM DIKUNCI</h2>
<p style='color: #ccc; font-size: 16px; margin-bottom: 30px;'>Anda sedang mengakses versi Gratis. Buka resep <b>Terapi Falak Ruhani, Afirmasi NLP Khusus, & Penawar Mental Block</b> dengan Akses Premium.</p>
<a href="https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20mau%20beli%20Kode%20Akses%20Premium%20Neuron%20AI." target="_blank" style="text-decoration: none;">
<div class="cta-button" style="display: inline-block; padding: 15px 40px; font-size: 18px;">🚀 DAPATKAN KODE VIA WHATSAPP (Rp 19.000)</div>
</a>
<p style='font-size:13px; color:#25D366; font-weight:bold; margin-top:15px;'>🔥 1.287 orang sudah membuka analisa mereka hari ini.</p>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.subheader("🌌 Terapi Falak Ruhani & Hypno-NLP")
        st.info("**Reset Ulang Saraf Anda**\n\nSistem mengonversi nama Anda menjadi angka getaran, lalu mencocokkannya dengan frekuensi Asmaul Husna dan Afirmasi Bawah Sadar untuk menghancurkan *Mental Block*.")
        nama_ruhani = st.text_input("Masukkan Nama Lengkap Anda:", placeholder="Ketik nama asli...", key="input_ruhani")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🔓 Buka Hasil Saya", key="btn_ruhani"):
            if nama_ruhani and len(nama_ruhani.strip()) >= 3:
                try:
                    with st.spinner('Mengekstrak sandi penyembuhan Anda...'):
                        time.sleep(1.5)
                        
                    safe_nr = get_safe_firstname(nama_ruhani)
                    nilai_jummal_r = hitung_nama_esoterik(nama_ruhani)
                    
                    r_num_r = nilai_jummal_r
                    while r_num_r > 9: r_num_r = sum(int(d) for d in str(r_num_r))
                    
                    asma_terapi, vibrasi_asma, tujuan_ruhani, jumlah_dzikir = proc_falak_ruhani(nilai_jummal_r, r_num_r, safe_nr)
                    protokol_nlp = get_protokol_terapi(r_num_r, safe_nr)
                    
                    st.markdown(f"""<div class="soft-fade" style="background: linear-gradient(135deg, rgba(10, 20, 40, 0.9) 0%, rgba(20, 10, 40, 0.9) 100%); border-left: 5px solid #00FFFF; padding: 25px; border-radius: 12px; margin-top: 20px; box-shadow: 0 8px 25px rgba(0, 255, 255, 0.15);">
<div style="text-align:center; border-bottom:1px solid #00FFFF; padding-bottom:10px; margin-bottom:20px;">
<span style="color:#00FFFF; font-size:16px; font-weight:900; letter-spacing:2px;">🧠 PROTOKOL TERAPI KOMPREHENSIF: {safe_nr}</span>
</div>
<div style="margin-bottom: 20px;">
<b style="color:#ff4b4b; font-size:16px;">⚠️ MENTAL BLOCK (Virus Bawah Sadar):</b><br>
<span style="color:#ccc; font-size:15px; line-height:1.6;">{protokol_nlp['block']}</span>
</div>
<div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
<b style="color:#FFF; font-size:16px;">✨ 1. ANCHOR SPIRITUAL (Falak Ruhani)</b><br>
<span style="color:#aaa; font-size:14px;">Gunakan Asma ini sebagai Dzikir penenang hati:</span><br>
<b style="color:#00FFFF; font-size:20px;">{asma_terapi}</b> <span style="color:#FFD700; font-weight:bold;">(BACA {jumlah_dzikir}x)</span><br>
<i style="color:#ccc; font-size:14px;">Fungsi: {tujuan_ruhani}</i>
</div>
<div style="background: rgba(255,215,0,0.05); border-left: 4px solid #FFD700; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
<b style="color:#FFD700; font-size:16px;">🗣️ 2. SUGESTI HYPNO-NLP (Afirmasi Diri)</b><br>
<span style="color:#aaa; font-size:14px;">Ucapkan kalimat ini berulang di dalam hati dengan penuh keyakinan menjelang tidur (Gelombang Theta):</span><br>
<i style="color:#fff; font-size:16px; line-height:1.6;">"{protokol_nlp['afirmasi']}"</i>
</div>
<div style="border-top: 1px dashed #555; padding-top: 15px; padding-bottom: 5px;">
<b style="color:#25D366; font-size:16px;">🏃‍♂️ 3. QUANTUM HABIT (Tindakan Fisik Hari Ini)</b><br>
<span style="color:#ccc; font-size:15px; line-height:1.6;">Semesta merespons tindakan nyata. Untuk menghancurkan rantai Mental Block Anda secara instan, eksekusi satu tugas ini hari ini juga:<br>
<b style="color:#FFF;">{protokol_nlp['habit']}</b></span>
</div>
<p style="font-size:12px; color:#ff4b4b; margin-top:15px; font-weight:bold;">⏳ Sistem mendeteksi perubahan energi. Lakukan protokol ini sebelum siklus berganti!</p>
</div>""", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses sandi terapi: {e}")
                
            else:
                st.warning("⚠️ Ketik nama lengkap Anda (minimal 3 huruf) untuk sinkronisasi.")

# ==========================================
# TAB 4: FAQ
# ==========================================
with tab4:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("📚 FAQ & Navigasi Energi")
    with st.expander("🤔 1. Apa itu Jam Planet?"): st.write("Pembagian waktu astronomi kuno yang membagi siang/malam menjadi 12 fase energi.")
    with st.expander("🤔 2. Apa itu Hisab Jummal?"): st.write("Sains huruf kuno (Gematria Arab) yang memberi bobot matematika pada tiap aksara.")
    with st.expander("🤔 3. Apakah hasil ini mutlak?"): st.write("TIDAK. Ini adalah Alat Pemetaan Pola (Pattern Mapping) untuk Self-Awareness.")
    st.error("**⚠️ DISCLAIMER:** Bukan saran medis profesional.")
    st.markdown("</div>", unsafe_allow_html=True)
 
# ==========================================
# SOCIAL PROOF
# ==========================================
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Jejak Transformasi</h3>", unsafe_allow_html=True)
daftar_ulasan = ambil_ulasan()
if daftar_ulasan:
    marquee_content = " | ".join([f"<span style='color: #FFD700;'>{u.get('Rating', '⭐⭐⭐⭐⭐')}</span> <b>{u.get('Nama', 'User')}:</b> \"{u.get('Komentar', '')[:50]}...\"" for u in daftar_ulasan[:3]])
    st.markdown(f'<div style="background-color: #1a1a1a; padding: 12px; border-radius: 8px; border-left: 3px solid #D4AF37; border-right: 3px solid #D4AF37; white-space: nowrap; overflow: hidden; margin-bottom: 20px;"><marquee behavior="scroll" direction="left" scrollamount="6" style="color: #f0f0f0; font-size: 15px;">{marquee_content}</marquee></div>', unsafe_allow_html=True)
    for u in daftar_ulasan[:5]:
        if u.get("Komentar", ""): st.markdown(f'<div class="ulasan-box"><span style="color: #FFD700; font-size: 12px;">{u.get("Rating", "⭐⭐⭐⭐⭐")}</span><br><b>{u.get("Nama", "Jiwa")}</b><br><i style="color: #ccc;">"{u.get("Komentar", "")}"</i></div>', unsafe_allow_html=True)

with st.expander("💬 Bagikan Pengalaman Anda"):
    with st.form("form_review"):
        rn, rr, rk = st.text_input("Nama"), st.radio("Rating", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"], horizontal=True), st.text_area("Ulasan")
        if st.form_submit_button("Kirim") and rn and rk:
            if kirim_ulasan(rn, rr, rk): 
                st.success("Terkirim!")
                time.sleep(1)
                st.rerun()
 
st.markdown("---")
st.markdown("<center><b>Ahmad Septian Dwi Cahyo</b><br><small>Certified NLP Trainer & Professional Hypnotherapist © 2026</small></center>", unsafe_allow_html=True)
