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
import hashlib

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

# --- PROCEDURAL TEXT ENGINE (HYPER-DYNAMIC GENERATOR) ---
def generate_seed(base_str):
    return int(hashlib.md5(base_str.encode('utf-8')).hexdigest(), 16) % (10**8)

def proc_arketipe(nama, angka, zodiak, neptu):
    random.seed(generate_seed(f"hyper_ark_{nama}_{angka}_{zodiak}_{neptu}"))
    
    buka = random.choice([
        f"Melalui persilangan matriks waktu dan elemen {zodiak}, DNA numerologi **{nama}** mengunci kuat pada **KODE {angka}**.",
        f"Kalkulasi semesta menyempit di **KODE {angka}**. Ini menandakan bahwa sejak lahir, alam bawah sadar **{nama}**",
        f"Sistem mendeteksi getaran **KODE {angka}** pada diri Anda. Secara genetik dan arsitektur mental, **{nama}**",
        f"Hasil ekstraksi sandi lahir Anda bermuara pada **KODE {angka}**. Di mata semesta, **{nama}** teridentifikasi",
        f"Berdasarkan algoritma kepribadian {zodiak} yang melebur dengan weton, cetak biru **{nama}** adalah **KODE {angka}**."
    ])
    
    inti = {
        1: ["sebagai sosok perintis yang didesain untuk memimpin dan menembus batas.", "memiliki dorongan mutlak untuk mandiri dan benci didikte.", "adalah entitas pengambil risiko yang berani berdiri sendiri."],
        2: ["sebagai Sang Penyelaras yang mampu menetralisir konflik.", "memiliki radar empati tingkat dewa untuk membaca ruang dan emosi.", "berfungsi sebagai jangkar kedamaian bagi orang-orang di sekitar."],
        3: ["sebagai komunikator handal dengan pikiran yang meletup-letup seperti kembang api.", "memiliki anugerah kreativitas tanpa batas yang tak bisa dikerangkeng.", "adalah magnet sosial yang kehadirannya selalu menghidupkan suasana."],
        4: ["sebagai arsitek kehidupan yang sangat sistematis dan presisi.", "memiliki pola pikir logis yang menjadikannya pondasi kuat bagi keluarga.", "adalah sosok praktis yang sangat bisa diandalkan di masa krisis."],
        5: ["sebagai simbol kebebasan yang menolak keras rutinitas monoton.", "memiliki kelincahan otak untuk beradaptasi dengan perubahan seekstrim apapun.", "adalah agen eksplorator yang selalu mencari sudut pandang dan pengalaman baru."],
        6: ["sebagai pelindung sejati dengan insting pengayom yang luar biasa.", "memegang standar tanggung jawab moral yang sangat tinggi demi keluarga.", "menjadikan kebahagiaan orang yang dicintai sebagai bahan bakar utamanya."],
        7: ["sebagai pencari kebenaran esensial dengan intuisi yang tajam.", "tidak pernah puas dengan jawaban dangkal dan selalu menganalisa hingga ke akar.", "memiliki filter batin eksklusif yang sangat selektif menilai kualitas seseorang."],
        8: ["sebagai eksekutor tangguh dengan insting material yang sangat presisi.", "memiliki fokus bawah sadar yang ditarik kuat menuju puncak otoritas.", "adalah sosok pengendali yang tetap berdiri tegak meski ditekan badai besar."],
        9: ["sebagai 'Jiwa Tua' yang memandang dunia dengan kacamata kebijaksanaan.", "memiliki tingkat kepedulian universal yang melampaui kepentingan egonya sendiri.", "selalu terdorong untuk memberikan *legacy* atau dampak positif bagi semesta."]
    }
    
    gaya = {
        1: ["Dalam bekerja, Anda adalah inisiator cepat yang lebih suka bertindak daripada rapat.", "Gaya sosial Anda dominan; Anda memancarkan aura alpha kemanapun Anda pergi."],
        2: ["Di lingkungan sosial, Anda adalah pendengar ulung tempat orang lain membuang keluh kesah.", "Gaya kerja Anda kolaboratif; Anda memastikan semua tim merasa dihargai."],
        3: ["Anda memecahkan masalah dengan ide *out-of-the-box* yang tidak terpikirkan orang lain.", "Gaya sosial Anda ekspresif; Anda ahli mencairkan ketegangan lewat humor."],
        4: ["Anda mengeksekusi visi dengan langkah demi langkah yang terukur dan tanpa cacat.", "Lingkungan melihat Anda sebagai sosok yang dingin namun selalu menyelesaikan tugas."],
        5: ["Anda paling bersinar saat diletakkan di situasi *chaos* yang butuh pemecahan instan.", "Gaya hidup Anda nomaden secara mental; Anda mudah bosan jika terus di tempat yang sama."],
        6: ["Anda memimpin dengan hati, seringkali bertindak layaknya orang tua bagi teman-teman Anda.", "Loyalitas Anda tidak perlu diragukan; Anda akan membela sirkel Anda mati-matian."],
        7: ["Anda mengobservasi dalam diam sebelum mengambil keputusan strategis yang mematikan.", "Gaya sosial Anda misterius; tidak banyak yang benar-benar tahu apa isi kepala Anda."],
        8: ["Anda mengorganisir sumber daya dan manusia dengan tangan besi yang elegan.", "Aura wibawa Anda sering membuat orang segan bahkan sebelum Anda berbicara."],
        9: ["Anda merangkul keberagaman dan memimpin lewat contoh pengorbanan yang nyata.", "Orang sering datang kepada Anda untuk meminta nasihat karena kedewasaan batin Anda."]
    }
    
    shadow = {
        1: ["Sisi gelapnya, Anda rawan terjebak sifat arogan jika ide Anda diremehkan.", "Bahayanya, gengsi Anda terlalu tinggi untuk sekadar meminta bantuan saat lelah.", "Waspadai rasa kesepian akibat ego yang membangun tembok pemisah dengan orang lain."],
        2: ["Tantangannya, Anda sering kehilangan jati diri karena terlalu sibuk menyenangkan orang (People Pleaser).", "Waspadai memendam amarah terus-menerus yang bisa menjadi bom waktu.", "Bahayanya, Anda sering menyerap energi beracun (toxic) dari lingkungan luar."],
        3: ["Musuh terbesar Anda adalah hilangnya fokus, membuat banyak ide brilian berakhir jadi wacana.", "Waspadai kecenderungan memakai topeng komedi untuk menutupi depresi atau luka batin.", "Sisi gelapnya, Anda rawan berbicara impulsif saat harga diri Anda tersinggung."],
        4: ["Anda sangat rawan terkena stres parah jika rencana yang Anda susun mendadak gagal total.", "Bahayanya, Anda sering dinilai tidak punya perasaan karena terlalu kaku pada aturan.", "Waspadai sifat over-micromanaging (mengatur hal kecil) yang membuat orang di sekitar Anda gerah."],
        5: ["Waspadai 'Sindrom Cepat Bosan' yang bisa mensabotase hubungan asmara atau karir jangka panjang.", "Sisi gelapnya, saraf Anda gampang *burnout* karena menolak untuk istirahat dari pencarian adrenalin.", "Bahayanya, Anda cenderung melarikan diri (escapism) saat dituntut tanggung jawab berat."],
        6: ["Anda sangat rentan terkena *burnout* ekstrem akibat terlalu sering mengurus beban hidup orang lain.", "Waspadai sifat *over-protective* yang justru mengekang kebebasan anak atau pasangan.", "Bahayanya, Anda sering dihantui rasa bersalah yang tak masuk akal saat mencoba menikmati *me-time*."],
        7: ["Tantangan utamanya adalah Anda sering terjebak *Paralysis by Analysis* (terlalu banyak overthinking, nol aksi).", "Waspadai kecenderungan mengisolasi diri secara total saat merasa tidak dihargai.", "Sisi gelapnya, sifat skeptis Anda sering membunuh pelan-pelan hubungan yang sebenarnya potensial."],
        8: ["Sisi gelapnya, Anda sangat kesulitan melepaskan kendali (*letting go*) and memaafkan pengkhianatan.", "Waspadai kebiasaan memforsir fisik tanpa ampun demi mengejar validasi kesuksesan.", "Bahayanya, Anda rentan mendominasi pasangan secara emosional tanpa Anda sadari."],
        9: ["Sisi gelapnya, Anda rawan memaklumi parasit (*toxic people*) murni karena rasa kasihan.", "Waspadai rasa patah hati kronis karena ekspektasi luhur Anda berbenturan dengan realitas.", "Bahayanya, energi batin Anda gampang terkuras akibat terlalu memikirkan penderitaan dunia."]
    }
    
    saran = {
        1: "Pesan semesta: Belajarlah mendelegasikan tugas. Meminta tolong bukanlah tanda kelemahan, melainkan taktik kepemimpinan.",
        2: "Pesan semesta: Berlatihlah mengatakan 'TIDAK' tanpa merasa bersalah. Anda tidak bisa menuangkan air dari teko yang kosong.",
        3: "Pesan semesta: Berlatihlah seni penyelesaian. Paksa diri Anda menuntaskan satu proyek kecil hari ini sebelum melompat ke ide berikutnya.",
        4: "Pesan semesta: Biarkan ruang untuk spontanitas. Sesekali, membiarkan segala sesuatunya berantakan adalah bentuk terapi batin.",
        5: "Pesan semesta: Temukan kebebasan dalam komitmen. Kedalaman sebuah ilmu/hubungan seringkali lebih memuaskan daripada sekadar pindah haluan.",
        6: "Pesan semesta: Buatlah batas (*boundaries*) yang tegas. Berhenti menyelamatkan orang yang memang tidak mau diselamatkan.",
        7: "Pesan semesta: Turunkan ekspektasi Anda terhadap manusia. Terkadang ketidaksempurnaan adalah satu-satunya hal yang nyata di dunia ini.",
        8: "Pesan semesta: Latih diri Anda untuk berserah diri di momen istirahat. Kesuksesan material tidak ada artinya jika sistem saraf Anda hancur.",
        9: "Pesan semesta: Anda tidak diutus untuk memikul beban seluruh galaksi. Cintai diri Anda sendiri sebelum Anda mencintai umat manusia."
    }
    
    pilih_inti = random.choice(inti[angka])
    pilih_gaya = random.choice(gaya[angka])
    pilih_shadow = random.choice(shadow[angka])
    pilih_saran = saran[angka]
    
    hasil_dinamis = f"{buka} Anda didesain {pilih_inti} {pilih_gaya} {pilih_shadow} {pilih_saran}"
    return hasil_dinamis

def proc_shadow_list(nama, angka):
    random.seed(generate_seed(f"shd_{nama}_{angka}"))
    semua_shadow = {
        1: ["Gengsi minta tolong saat memikul beban", "Membangun tembok ego untuk menutupi sepi", "Overthinking merasa hasil belum sempurna", "Kesulitan menerima kritik bawahan", "Mengabaikan lelah demi sebuah target"],
        2: ["Mengorbankan kebahagiaan demi ekspektasi", "Sulit berkata TIDAK (People Pleaser)", "Memendam amarah hindari konflik", "Terlalu bergantung pada validasi eksternal", "Menyerap energi toxic dari lingkungan"],
        3: ["Menyembunyikan gelisah di balik topeng ceria", "Cepat kehilangan motivasi pada rutinitas", "Insomnia karena pikiran over-analisa", "Kesulitan fokus pada satu prioritas", "Bicara impulsif saat tersinggung"],
        4: ["Stres parah jika rencana mendadak berubah", "Terjebak di zona nyaman takut risiko", "Sering dinilai terlalu dingin/kaku", "Over-micromanaging pada hal kecil", "Menghakimi orang yang tidak disiplin"],
        5: ["Sindrom Bosan yang mensabotase karya", "Kelelahan saraf karena otak jalan terus", "Merasa hampa kehilangan pijakan", "Cenderung lari (escapism) saat ditekan", "Kesulitan menjaga rutinitas jangka panjang"],
        6: ["Burnout sibuk mengurus hidup orang lain", "Sikap Over-Protective yang mengekang", "Rasa bersalah jika me time", "Terlalu ikut campur urusan keluarga", "Mengharap balasan pamrih secara emosional"],
        7: ["Menganalisa terus tanpa aksi (Paralysis)", "Merasa terasing/tak ada yang sepemikiran", "Mencurigai niat baik orang karena trauma", "Terlalu sinis dan sarkastik", "Menutup diri saat emosinya memuncak"],
        8: ["Sangat sulit melepaskan kontrol/memaafkan", "Memaksa tubuh mengabaikan alarm lelah", "Menilai orang murni dari sisi guna/status", "Ketakutan berlebih menjadi miskin/lemah", "Mendominasi pasangan secara emosional"],
        9: ["Memaklumi orang toxic atas nama kasihan", "Patah hati akibat ekspektasi pada manusia", "Kelelahan batin memikirkan beban semesta", "Sering merasa tidak pantas (Imposter)", "Kehilangan jati diri demi visi luhur"]
    }
    return random.sample(semua_shadow[angka], 3)

def proc_couple_persona(root_c, n1, n2):
    random.seed(generate_seed(f"cp_{n1}_{n2}_{root_c}"))
    buka = random.choice([
        f"Ketika vibrasi nama **{n1}** dan **{n2}** dilebur, hasilnya mengunci di **Root {root_c}**.",
        f"Penyatuan kalkulasi esoterik **{n1}** disilang dengan **{n2}** meledak di **Root {root_c}**.",
        f"Hukum resonansi mencatat bahwa persatuan **{n1}** dan **{n2}** menghasilkan gelombang **Root {root_c}**."
    ])
    
    desc = {
        1: ("THE POWER COUPLE", f"Kalian secara alami memancarkan simbol Alpha. Ketika bersatu, {n1} dan {n2} membentuk entitas yang mandiri, ambisius, dan punya daya dobrak tangguh. Fokus energi kalian tertuju pada kemajuan karir dan peningkatan status bersama."),
        2: ("THE SOULMATES", f"Hubungan ini memiliki 'Wi-Fi' batin yang otomatis terhubung. Sangat mudah bagi {n1} untuk memahami kelelahan atau kebahagiaan {n2} tanpa harus ada kata yang terucap. Harmoni adalah kunci kalian."),
        3: ("THE SOCIALITES", f"Energi yang dihasilkan memancarkan aura magnetis. {n1} dan {n2} adalah tipe pasangan yang menyenangkan, penuh ide spontan, dan kehadiran kalian selalu ditunggu untuk meramaikan suasana pergaulan keluarga atau sirkel teman."),
        4: ("THE BUILDERS", f"Hubungan ini sangat berpijak pada bumi. Fokus utama persatuan {n1} dan {n2} bukanlah drama percintaan ala film, melainkan membangun pondasi aset, merapikan struktur finansial bersama, dan menjaga kesetiaan absolut."),
        5: ("THE ADVENTURERS", f"Hubungan kalian dipenuhi energi kebebasan dan petualangan. Baik {n1} maupun {n2} akan layu jika hubungannya monoton. Kalian butuh kejutan, eksplorasi hal baru, dan tantangan agar api asmara tetap menyala."),
        6: ("THE FAMILY FIRST", f"Ini adalah simbol pengayoman tertinggi. Tingkat pengorbanan {n1} dan {n2} untuk merawat keutuhan rumah tangga, anak, atau menjembatani keluarga besar sungguh luar biasa mendalam. Rumah kalian adalah tempat berpulang ternyaman."),
        7: ("THE DEEP SEEKERS", f"Hubungan ini cenderung tertutup dan eksklusif. {n1} dan {n2} tidak membangun cinta atas dasar materi semata, melainkan koneksi intelektual dan pencarian spiritual. Kalian berdua memiliki benteng privasi yang sulit ditembus orang luar."),
        8: ("THE EMPIRE", f"Angka ini adalah magnet kelimpahan mutlak. Penyatuan ego {n1} dan {n2} secara otomatis memfokuskan energi untuk mengejar kesuksesan bisnis, penumpukan finansial, dan membangun kerajaan keluarga bersama yang tak terhitung."),
        9: ("THE HEALERS", f"Hubungan kalian berada di puncak kedewasaan empati. Interaksi {n1} dan {n2} dipenuhi toleransi. Ketenangan batin kalian berdua sering menjadikan rumah kalian sebagai 'tempat penyembuhan' bagi sirkel yang sedang terluka.")
    }
    gelar, penjelasan = desc.get(root_c, ("UNCHARTED SYNERGY", f"Kombinasi energi {n1} dan {n2} membentuk anomali yang sangat unik dan tak tertebak."))
    return gelar, f"{buka} {penjelasan}"

def proc_weton_kombo(sisa, n1, n2, z1, z2):
    random.seed(generate_seed(f"wt_{n1}_{n2}_{sisa}_{z1}_{z2}"))
    do_list = {
        1: [f"Gunakan teknik *Pacing-Leading*: Validasi dulu perasaan {n2} sebelum memasukkan solusi logis.", f"Beri jeda waktu jika argumen mulai memanas. Biarkan ego {z1} dan {z2} reda dulu."],
        2: [f"Jadikan {n2} sebagai Partner Diskusi Strategis. Berikan pujian tulus saat dia mencapai sesuatu.", f"Bangun kebiasaan diskusi karir bersama, energi {z1} milikmu akan memompa semangat {n2}."],
        3: [f"Ciptakan *Pattern Interrupt* (kejutan). Ajak {n2} kencan dadakan agar hubungan tak hambar.", f"Pancing interaksi *deep-talk* rutin agar koneksi batin {n1} dan {n2} makin tajam."],
        4: [f"Kuasai teknik *Reframing*. Paksa otak {n1} dan {n2} mencari sisi positif saat ada krisis finansial/keluarga.", f"Perkuat daya tahan. Badai di awal hubungan ini adalah ujian semesta untuk rezeki besar nanti."],
        5: [f"Sering lakukan sesi visi masa depan. Kedamaian emosi {n1} dan {n2} adalah kunci rezeki terbuka.", f"Kelola keuangan bersama secara transparan, hoki kalian ada di penyatuan aset."],
        6: [f"Berikan *Space* saat tensi naik. Jangan paksa {n2} bicara saat filter otaknya sedang error.", f"Gunakan humor untuk memecahkan ketegangan argumen sepele antara kalian."],
        7: [f"Biasakan komunikasi berbasis fakta (*Sensory Based*). Bicarakan apa yang terlihat/terdengar, bukan asumsi.", f"Validasi ulang setiap instruksi atau ucapan untuk menghindari salah paham fatal."],
        8: [f"Pertahankan *Rapport* dengan menjelajahi hobi baru berdua agar ada tantangan seru.", f"Sesekali keluar dari zona nyaman agar rukunnya hubungan tidak berujung pada kebosanan."]
    }
    dont_list = {
        1: [f"DILARANG keras *Mind-Reading* (menebak pikiran negatif) dan mengungkit masa lalu {n2}.", f"Jangan beradu argumen saat {n2} sedang lapar atau lelah secara fisik."],
        2: [f"Hindari jebakan pencitraan. Jangan sampai {n1} dan {n2} pura-pura bahagia di luar tapi hancur di dalam.", f"Jangan biarkan campur tangan sirkel pertemanan merusak wibawa hubungan kalian."],
        3: [f"Hati-hati jebakan *Comfort Zone*. Pasangan Jodoh sering malas berjuang karir karena sudah terlalu nyaman.", f"Jangan mengabaikan perawatan diri (fisik/penampilan) hanya karena merasa sudah saling menerima."],
        4: [f"Jangan pernah {n1} memaksakan standar pribadi (gengsi) kepada {n2}. Turunkan ekspektasi.", f"Pantang menyerah di 3 tahun pertama. Ujian berat di awal pantang diselesaikan dengan kata pisah."],
        5: [f"Jangan jadikan uang satu-satunya perekat. Pastikan cinta {n1} dan {n2} utuh saat saldo diuji.", f"Jangan sombong jika pintu rezeki sedang terbuka lebar akibat penyatuan weton ini."],
        6: [f"Jangan pernah {n1} menyerang harga diri {n2} secara frontal saat emosinya di puncak.", f"Dilarang menggunakan *Silent Treatment* (mendiamkan pasangan) selama lebih dari 24 jam."],
        7: [f"DILARANG memakai kata absolut seperti '{n2} SELALU egois!' atau '{n2} TIDAK PERNAH peduli!'.", f"Jangan mengintai privasi digital pasangan secara diam-diam, itu akan menghancurkan *trust*."],
        8: [f"Waspadai sikap *Take it for granted* (menggampangkan pasangan) karena merasa pasti bersama.", f"Jangan biarkan rutinitas mematikan romantisme masa muda {n1} dan {n2}."]
    }
    hasil = {
        1: ("💔 PEGAT (Ujian Ego)", f"Terdapat perbedaan fundamental dalam memproses emosi. Filter {z1} milikmu rawan bentrok dengan {z2} miliknya. Jika ada konflik, sering diwarnai adu argumen keras karena {n1} dan {n2} sama-sama merasa paling rasional dan benar."),
        2: ("👑 RATU (Kharisma Pasangan)", f"Penyatuan vibrasi ini memancarkan wibawa. Orang lain dan keluarga sangat segan melihat kalian berdua. Energi {z1} and {z2} saling menopang satu sama lain dengan sempurna."),
        3: ("💞 JODOH (Sinkronisasi Alami)", f"Penerimaan bawah sadar luar biasa tinggi. Seolah frekuensi {z1} milik {n1} dan {z2} milik {n2} sudah terhubung sejak di kehidupan sebelumnya. Sinkronisasi batin yang kuat."),
        4: ("🌱 TOPO (Ujian Bertumbuh)", f"Fase awal kolaborasi {z1} dan {z2} pasti penuh ujian adaptasi berat. Namun setelah {n1} dan {n2} berhasil melewati masa kritis peleburan ego ini, pondasi kalian takkan tertembus badai apapun."),
        5: ("💰 TINARI (Magnet Rezeki)", f"Persilangan energi {z1} dan {z2} adalah magnet kelimpahan. Pintu kelancaran finansial dan kemudahan duniawi biasanya mendadak terbuka lebar setelah {n1} dan {n2} sepakat bersatu."),
        6: ("⚡ PADU (Beda Frekuensi)", f"Kalian akan sering mengalami letupan perdebatan. Ini terjadi murni karena perbedaan cara otak memfilter informasi. {n1} dan {n2} sering meributkan hal kecil yang sebenarnya tidak prinsipil."),
        7: ("👁️ SUJANAN (Rawan Asumsi)", f"Hubungan ini sangat rawan miskomunikasi dan cemburu buta. Tumpukan asumsi bawah sadar antara {z1} dan {z2} sering memicu salah paham dadakan jika tidak dikomunikasikan jernih."),
        8: ("🕊️ PESTHI (Damai & Rukun)", f"Interaksi antara {n1} and {n2} sangat adem ayem dan minim drama penguras energi. Kehadiran {z1} sering menetralisir stres {z2}, menciptakan ketenangan abadi.")
    }
    judul, desc = hasil.get(sisa)
    do = random.choice(do_list[sisa])
    dont = random.choice(dont_list[sisa])
    return judul, desc, do, dont

def proc_penjelasan_matriks(n1, n2, eso_val, nep_val):
    random.seed(generate_seed(f"pm_v2_{n1}_{n2}_{eso_val}_{nep_val}"))
    
    headers = [
        "⚙️ ARSITEKTUR ANALISA",
        "📡 DEKODE SINYAL KOSMIK",
        "📜 LOGIKA MESIN NEURO",
        "🔍 BEDAH PARAMETER SINERGI"
    ]
    header = random.choice(headers)
    
    eso_start = [
        f"Fusi vibrasi nama <b>{n1}</b> & <b>{n2}</b>",
        f"Ekstraksi sandi <i>Hisab Jummal</i> kalian",
        f"Penyatuan resonansi aksara <b>{n1}</b> dan <b>{n2}</b>"
    ]
    eso_mid = [
        f"menghasilkan angka esoterik <b>{eso_val}</b>.",
        f"mengunci pada frekuensi absolut <b>{eso_val}</b>.",
        f"berhenti di titik koordinat spiritual <b>{eso_val}</b>."
    ]
    eso_end = [
        "Ini adalah 'Wajah' hubungan kalian di mata semesta; mendefinisikan persona yang muncul saat kalian bersama.",
        "Sandi ini menentukan bagaimana kalian berdua dipandang sebagai satu entitas oleh lingkungan luar.",
        "Angka ini mengunci blueprint takdir yang akan mendominasi perjalanan interaksi kalian berdua."
    ]
    
    nep_start = [
        f"Kalkulasi sinkronisasi waktu (Total Neptu <b>{nep_val}</b>)",
        f"Analisa siklus rotasi lahir (Parameter <b>{nep_val}</b>)",
        f"Metode <i>modulo 8</i> pada nilai neptu <b>{nep_val}</b>"
    ]
    nep_mid = [
        "digunakan untuk memetakan dinamika ego bawah sadar.",
        "menjadi radar pengukur stabilitas emosional kalian.",
        "berfungsi sebagai mitigasi benturan watak harian."
    ]
    nep_end = [
        "Sistem menggunakan data ini untuk mendeteksi area rawan konflik sekaligus pintu masuk rezeki bersama.",
        "Parameter ini krusial untuk menjaga harmoni agar riak kecil tidak menjadi badai dalam rumah tangga.",
        "Lewat sandi ini, kita bisa melihat 'Jangkar' apa yang paling kuat mengikat batin kalian saat ini."
    ]
    
    final_eso = f"{random.choice(eso_start)} {random.choice(eso_mid)} {random.choice(eso_end)}"
    final_nep = f"{random.choice(nep_start)} {random.choice(nep_mid)} {random.choice(nep_end)}"
    
    return f"""
<div class="info-metric-box">
<b style="color:#FFD700; font-size:14px;">{header}:</b><br>
• <b style="color:white;">TOTAL ESOTERIK:</b> {final_eso}<br>
• <b style="color:white;">TOTAL NEPTU:</b> {final_nep}
</div>
"""

# --- ENGINE FALAK RUHANI (SPIRITUAL ANCHORING) ---
def proc_falak_ruhani(total_jummal, root_num, nama):
    ruhani_data = {
        1: {"asma": "Ya Fattah (Maha Pembuka)", "vibrasi": "Mendobrak Jalan Buntu & Kesombongan", "tujuan": "Membersihkan hambatan ego, menaklukkan keras kepala, dan membuka pintu rezeki yang terkunci akibat kesombongan tak sadar."},
        2: {"asma": "Ya Salam (Maha Sejahtera)", "vibrasi": "Harmoni & Perisai Mental", "tujuan": "Menetralisir energi beracun (toxic) dari lingkungan sekitar dan menyembuhkan penyakit mental (anxiety)."},
        3: {"asma": "Ya Mushawwir (Maha Pembentuk)", "vibrasi": "Manifestasi Ide ke Realita", "tujuan": "Mengubah pikiran yang overthinking dan ide liar menjadi sebuah karya nyata yang terstruktur."},
        4: {"asma": "Ya Muqit (Maha Pemberi Kecukupan)", "vibrasi": "Stabilitas & Nutrisi Batin", "tujuan": "Menghancurkan 'Mental Miskin' (Scarcity Mindset) dan memberikan rasa aman absolut pada finansial."},
        5: {"asma": "Ya Basith (Maha Melapangkan)", "vibrasi": "Ekspansi & Pembebasan Diri", "tujuan": "Melepaskan perasaan terkekang/stres dan memperluas kapasitas wadah rezeki agar siap menerima hal besar."},
        6: {"asma": "Ya Wadud (Maha Mengasihi)", "vibrasi": "Cinta Universal & Daya Tarik", "tujuan": "Menyembuhkan trauma masa lalu, menumbuhkan self-love, dan memancarkan aura pengasihan (Rapport) alami."},
        7: {"asma": "Ya Batin (Maha Tersembunyi)", "vibrasi": "Intuisi & Hikmah Langit", "tujuan": "Mempertajam indra keenam (intuisi bisnis/hidup) dan kemampuan membaca niat tersembunyi orang lain."},
        8: {"asma": "Ya Ghaniy (Maha Kaya)", "vibrasi": "Otoritas & Kelimpahan Absolut", "tujuan": "Menjadi magnet kekayaan material dan memegang kendali kekuasaan tanpa jatuh pada keserakahan."},
        9: {"asma": "Ya Hakim (Maha Bijaksana)", "vibrasi": "Pencerahan & Kesadaran", "tujuan": "Pelepasan beban karma masa lalu dan menyelaraskan tindakan fisik dengan Misi Semesta (Life Purpose)."}
    }
    data = ruhani_data.get(root_num, ruhani_data[1])
    dzikir_count = total_jummal
    return data["asma"], data["vibrasi"], data["tujuan"], dzikir_count

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

KAMUS_ABJAD = {
    'a': 1, 'b': 2, 'j': 3, 'd': 4, 'h': 5, 'w': 6, 'z': 7, 
    't': 9, 'y': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 
    's': 60, 'f': 80, 'q': 100, 'r': 200, 'c': 3, 'e': 5,
    'g': 1000, 'i': 10, 'o': 6, 'p': 80, 'u': 6, 'v': 6, 'x': 60
}

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
        1: "Pencipta jalan baru (The Leader)", 2: "Penyelaras harmoni (The Peacemaker)",
        3: "Penyampai pesan (The Creator)", 4: "Pembangun sistem (The Builder)",
        5: "Agen transformasi (The Explorer)", 6: "Pengayom sejati (The Caregiver)",
        7: "Pencari esensi (The Seeker)", 8: "Pemegang kendali (The Executive)",
        9: "Kesadaran universal (The Humanitarian)"
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

# --- BYPASS ENGINE (DIRECT WETON INPUT) ---
def hitung_neptu_langsung(hari, pasaran):
    n_hari = {"Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9}
    n_pas = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
    return n_hari.get(hari, 0) + n_pas.get(pasaran, 0)
 
def get_betaljemur_data(neptu, hari):
    lakuning = {
        7: ("Lebu Katiup Angin", "Pikiran dinamis, mudah goyah, sering berpindah fokus."),
        8: ("Lakuning Geni", "Emosi meledak-ledak. Rentan abreaction, butuh teknik pacing tinggi."),
        9: ("Lakuning Angin", "Gampang dipengaruhi sugesti eksternal, adaptif namun labil."),
        10: ("Pandito Mbangun Teki", "Introspektif, cerdas, suka menasihati, pola pikir deep structure."),
        11: ("Aras Tuding", "Sering menjadi telunjuk/perhatian, selalu ditunjuk untuk peluang, pemberani."),
        12: ("Aras Kembang", "Menebar pesona, cinta damai, rapport natural sangat mudah."),
        13: ("Lakuning Lintang", "Suka menyendiri, memancarkan pesona magnetis tanpa banyak bicara."),
        14: ("Lakuning Rembulan", "Penenang batin, pendengar ulung, jangkar emosi bagi orang lain."),
        15: ("Lakuning Srengenge", "Pencerah, berwibawa, sangat logis dan tidak mudah dihipnotis."),
        16: ("Lakuning Banyu", "Kelihatan tenang di permukaan, mematikan jika batasnya dilanggar."),
        17: ("Lakuning Bumi", "Sangat sabar, pengayom, membumi, dan tidak terburu-buru."),
        18: ("Lakuning Paripurna", "Elemen kesempurnaan, memegang kendali otoritas dengan sangat bijak.")
    }
    naga_dina = {
        "Minggu": "Timur", "Senin": "Selatan", "Selasa": "Barat", "Rabu": "Utara",
        "Kamis": "Timur", "Jumat": "Selatan", "Sabtu": "Selatan"
    }
    return lakuning.get(neptu, ("Anomali", "Karakter kompleks"))[0], lakuning.get(neptu, ("Anomali", "Karakter kompleks"))[1], naga_dina.get(hari, "Netral")

def get_rezeki_usaha(neptu):
    mod_rezeki = neptu % 7 if neptu % 7 != 0 else 7
    rezeki = {
        1: ("Wasesa Segara", "Rezeki seluas lautan, pemaaf, dan mudah mencari jalan keluar."),
        2: ("Tunggak Semi", "Rezekinya selalu ada, patah tumbuh hilang berganti."),
        3: ("Satria Wibawa", "Mendapat kemuliaan, keberuntungan, dan dihormati banyak kolega."),
        4: ("Sumur Sinaba", "Menjadi referensi orang, banyak ilmu, dan membawa berkah sekitar."),
        5: ("Bumi Kapetak", "Harus bekerja cerdas dan keras, pantang menyerah sebelum sukses."),
        6: ("Satria Wirang", "Kerap menghadapi rintangan tak terduga, butuh manajemen risiko kuat."),
        7: ("Lebu Katiup Angin", "Rawan kebocoran kas tak terduga, wajib punya aset tetap.")
    }
    mod_usaha = neptu % 5 if neptu % 5 != 0 else 5
    usaha = {
        1: ("Sandang", "Kebutuhan esensial selalu tercukupi, cocok di bisnis komoditas."),
        2: ("Pangan", "Makmur berlimpah, nasib kuat di kuliner atau ritel massal."),
        3: ("Beja", "Nasib dominan baik, punya hoki tinggi di instrumen investasi."),
        4: ("Lara", "Butuh *partner* pendamping untuk mitigasi kerugian mendadak."),
        5: ("Pati", "Hindari spekulasi buta, harus berbasis *data-driven*.")
    }
    return rezeki[mod_rezeki], usaha[mod_usaha]
 
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

# --- SIDEBAR PROMOSI ---
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
cur_planet, cur_instr, cur_color = get_planetary_hour()
st.markdown(f"""
<div style='text-align: right;'>
    <div class='live-badge' style='background: {cur_color};'>🕒 LIVE PLANET: {cur_planet.upper()}</div>
    <div style='font-size: 11px; color: #888; margin-top: 5px;'>{cur_instr}</div>
</div>""", unsafe_allow_html=True)

if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass
 
st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900; color:#FFD700;'>🌌 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #ccc; margin-bottom:0;'>Meretas Realita Melalui Kode Sandi Alam Bawah Sadar</p>", unsafe_allow_html=True)
st.markdown("---")
 
tgl_today = datetime.date.today()
 
# --- MENU TABS ---
tab1, tab2, tab5, tab3, tab4 = st.tabs(["👤 Personal Identity", "👩‍❤️‍👨 Couple Matrix", "⏱️ Quantum Engine", "🌌 Falak Ruhani", "📚 FAQ"])
 
# ==========================================
# TAB 1: IDENTITAS KOSMIK & BETALJEMUR
# ==========================================
with tab1:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("Akses Blueprint Bawah Sadar Anda")
    nama_user = st.text_input("Nama Lengkap:", placeholder="Ketik nama asli Anda...", key="t1_nama")
    
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    st.write("📅 **Data Masehi (Untuk Zodiak & Kode NLP):**")
    tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date(1983, 9, 23), min_value=datetime.date(1900, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")
    
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    st.write("📜 **Data Weton Langsung (Akurasi Primbon 100%):**")
    st.caption("Pilih langsung Weton Anda tanpa konversi kalender Masehi.")
    col_h, col_p = st.columns(2)
    with col_h:
        hari_input = st.selectbox("Hari Lahir", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4, key="h_t1")
    with col_p:
        pasaran_input = st.selectbox("Pasaran Lahir", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=2, key="p_t1")
        
    st.markdown("</div>", unsafe_allow_html=True)
 
    if st.button("Kalkulasi Blueprint (Mulai)"):
        if not nama_user or len(nama_user.strip()) < 3: 
            st.error("🚨 Mohon ketik nama lengkap Anda (minimal 3 huruf) untuk sinkronisasi vibrasi.")
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
                
                nep = hitung_neptu_langsung(hari_input, pasaran_input)
                wet = f"{hari_input} {pasaran_input}"
                zod = get_zodiak(tgl_input)
                
                n_laku, d_laku, arah_naga = get_betaljemur_data(nep, hari_input)
                rezeki_data, usaha_data = get_rezeki_usaha(nep)
                
                punchy = arketipe_punchy.get(angka_hasil, arketipe_punchy[1])
                desk_ark_dinamis = proc_arketipe(safe_name, angka_hasil, zod, nep)
                shadow = proc_shadow_list(safe_name, angka_hasil)
                
                st.snow()
                st.markdown(f"<h3 style='text-align:center;'>🌌 Blueprint Kosmik: {safe_name}</h3>", unsafe_allow_html=True)
                
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
Secara arsitektur Gematria Kuno, total nilai getaran resonansi dari aksara nama <b>{safe_name}</b> adalah:<br>
<code style="color:#25D366; background:transparent; padding:0;">{rincian_jummal} = <b>{nilai_jummal}</b></code></p>
<ol style="margin-left: -15px; margin-bottom: 20px;">
<li><b>Elemen Bawah Sadar:</b> Nilai {nilai_jummal} direduksi menjadi 4 pilar alam semesta, **{safe_name}** berafiliasi dengan elemen <b>{el_nama}</b>.<br><i style="color:#aaa;">{el_desc}</i></li>
<li><b>Inti Jiwa (Root Number):</b> {p_reduk} = {s_reduk} ➡ <b>{r_num}</b>.<br>Angka {r_num} adalah sandi bahwa secara sadar/bawah sadar **{safe_name}** adalah: <b>{r_desc}</b></li>
</ol>
<p><b>2. Sandi Waktu Lahir (Meta-Program NLP)</b><br>
Kalkulasi penyederhanaan (reduksi matriks) dari tanggal lahir Masehi Anda:<br>
<code style="color:#FFD700; background:transparent; padding:0;">{rincian_tgl}</code><br>
<span style="font-size:14px; color:#ccc;">Maka didapatkan <b>KODE {angka_hasil}</b>. Angka ini adalah <i>Blueprint</i> cara otak <b>{safe_name}</b> memproses informasi, mengambil keputusan, dan bereaksi terhadap tekanan.</span></p>
{m_note}
</div>
""", unsafe_allow_html=True)

                st.markdown(f"""
<div class="primbon-box">
<div style="text-align:center; border-bottom:1px solid #D4AF37; padding-bottom:10px; margin-bottom:15px;">
<span style="color:#D4AF37; font-size:14px; font-weight:900; letter-spacing:2px;">📜 PETHIKAN KITAB BETALJEMUR ADAMMAKNA</span>
</div>
<div style="font-size:15px; line-height:1.6; margin-bottom: 15px;">
<span style="color:#aaa;">Berdasarkan weton <b>{wet} (Neptu {nep})</b>, sistem memetakan sandi Pangarasan (Karakter Bawah Sadar) milik <b>{safe_name}</b>, yaitu:</span> <br>
<b style="color:#FFF; font-size:18px;">{n_laku}</b> — <i style="color:#ccc;">"{d_laku}"</i>
</div>
<div style="font-size:15px; line-height:1.6; margin-bottom: 15px; border-top: 1px dashed #555; padding-top: 10px;">
<span style="color:#aaa;">Pembacaan Garis Rezeki & Potensi Usaha:</span><br>
• <b>Rezeki (<span style="color:#FFD700;">{rezeki_data[0]}</span>):</b> <i style="color:#ccc;">{rezeki_data[1]}</i><br>
• <b>Usaha (<span style="color:#25D366;">{usaha_data[0]}</span>):</b> <i style="color:#ccc;">{usaha_data[1]}</i>
</div>
<div style="font-size:15px; line-height:1.6; background: rgba(212,175,55,0.1); padding: 10px; border-radius: 8px;">
<span style="color:#FFD700;">🧭 <b>NAGA DINA (Arah Kejayaan Hari {hari_input}):</b></span> <b style="font-size: 16px;">{arah_naga} (Zona Taktis)</b><br>
<i style="color:#888; font-size:13px;">*ACTIONABLE: Hari ini, posisikan meja kerja atau arah duduk <b>{safe_name}</b> menghadap zona kejayaan di atas saat mengambil keputusan penting.</i>
</div>
</div>
""", unsafe_allow_html=True)
                
                st.markdown(f"### 👁️ Decode Kepribadian Dinamis: {safe_name}")
                st.info(f"Mengacu pada pola unik {safe_name}, arketipe utama dikunci sebagai:\n\n**{punchy['inti']}**")
                st.write(desk_ark_dinamis)
                
                c_kekuatan, c_shadow = st.columns(2)
                with c_kekuatan:
                    st.markdown(f"🔥 **KEKUATAN DOMINAN {safe_name}:**")
                    st.markdown(f"<ul class='list-punchy' style='color:#25D366;'><li>{punchy['kekuatan'][0]}</li><li>{punchy['kekuatan'][1]}</li><li>{punchy['kekuatan'][2]}</li></ul>", unsafe_allow_html=True)
                with c_shadow:
                    st.markdown(f"⚠️ **SHADOW TERSEMBUNYI (SPESIFIK):**")
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
# TAB 2: COUPLE MATRIX (DUAL-ENGINE)
# ==========================================
with tab2:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("Penyatuan Esoterik & Betaljemur (Couple Matrix)")
    st.write("Masukkan Data Masehi (untuk NLP) dan Weton (untuk Primbon) Anda dan Pasangan.")
    
    ca, cb = st.columns(2)
    with ca: 
        st.markdown("<div style='background: rgba(255,215,0,0.05); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,215,0,0.2);'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#FFD700; margin-top:0;'>Data Pihak 1 (Pria)</h4>", unsafe_allow_html=True)
        n1 = st.text_input("Nama Anda", key="n1_c")
        d1 = st.date_input("Tanggal Lahir Masehi", value=datetime.date(1995, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="d1_c")
        st.markdown("<hr style='margin: 10px 0; border-color: #333;'>", unsafe_allow_html=True)
        st.caption("Pilih Weton Pihak 1:")
        hc1 = st.selectbox("Hari Pria", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=4, key="hc1")
        pc1 = st.selectbox("Pasaran Pria", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=2, key="pc1")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with cb: 
        st.markdown("<div style='background: rgba(255,105,180,0.05); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,105,180,0.2);'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#FF69B4; margin-top:0;'>Data Pihak 2 (Wanita)</h4>", unsafe_allow_html=True)
        n2 = st.text_input("Nama Pasangan", key="n2_c")
        d2 = st.date_input("Tanggal Lahir Masehi", value=datetime.date(1995, 1, 1), min_value=datetime.date(1900, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="d2_c")
        st.markdown("<hr style='margin: 10px 0; border-color: #333;'>", unsafe_allow_html=True)
        st.caption("Pilih Weton Pihak 2:")
        hc2 = st.selectbox("Hari Wanita", ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"], index=2, key="hc2")
        pc2 = st.selectbox("Pasaran Wanita", ["Legi", "Pahing", "Pon", "Wage", "Kliwon"], index=0, key="pc2")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
        
    if st.button("Analisis Resonansi Pasangan"):
        if str(n1).strip() and str(n2).strip():
            try:
                st.snow()
                safe_n1 = get_safe_firstname(n1, "Pria")
                safe_n2 = get_safe_firstname(n2, "Wanita")
                zod1 = get_zodiak(d1)
                zod2 = get_zodiak(d2)
                
                nep_1 = hitung_neptu_langsung(hc1, pc1)
                nep_2 = hitung_neptu_langsung(hc2, pc2)
                sel = abs(hitung_angka(d1) - hitung_angka(d2))
                    
                jummal_1 = hitung_nama_esoterik(n1)
                jummal_2 = hitung_nama_esoterik(n2)
                total_couple = jummal_1 + jummal_2
                
                root_c = total_couple
                while root_c > 9: root_c = sum(int(d) for d in str(root_c))
                
                c_title, c_desc = proc_couple_persona(root_c, safe_n1, safe_n2)
                judul_jodoh, desk_jodoh, d_do, d_dont = proc_weton_kombo((nep_1+nep_2)%8 or 8, safe_n1, safe_n2, zod1, zod2)
                
                st.markdown("---")
                st.markdown(f"### 🔮 The Unified Resonance: {safe_n1} & {safe_n2}")
                
                st.markdown(f"""
<div class="matrix-container">
<div class="matrix-item"><div class="matrix-label">Neptu {safe_n1}</div><div class="matrix-value">{hc1} {pc1} ({nep_1})</div></div>
<div class="matrix-item"><div class="matrix-label">Neptu {safe_n2}</div><div class="matrix-value">{hc2} {pc2} ({nep_2})</div></div>
<div class="matrix-item" style="background: rgba(212,175,55,0.2);"><div class="matrix-label" style="color:#FFD700;">TOTAL NEPTU</div><div class="matrix-value matrix-value-special">{nep_1 + nep_2}</div></div>
<div class="matrix-item"><div class="matrix-label">Total Esoterik</div><div class="matrix-value">{total_couple}</div></div>
</div>
""", unsafe_allow_html=True)
                
                st.markdown(proc_penjelasan_matriks(safe_n1, safe_n2, total_couple, (nep_1+nep_2)), unsafe_allow_html=True)
                
                st.markdown(f"""
<div class="dynamic-reading-box" style="border-left-color: #25D366;">
<h4 style="color: #25D366; margin-top:0;">🧬 Persona Pasangan: {c_title}</h4>
<p><i>{c_desc}</i></p>
</div>
""", unsafe_allow_html=True)
                
                st.markdown(f"#### 📜 Titik Benturan Weton: {judul_jodoh.split(' ')[1]}")
                st.info(f"Semesta mencatat takdir persilangan energi (Neptu {nep_1} & {nep_2}) ini sebagai:\n\n**{judul_jodoh}**: {desk_jodoh}")
                
                if sel in [0, 3, 6, 9]: st.success(f"💘 **SKOR META-PROGRAM (NLP): 90% (Sangat Sinkron)** - Peta mental {safe_n1} dan {safe_n2} sangat mirip.")
                elif sel in [1, 2, 8]: st.warning(f"⚖️ **SKOR META-PROGRAM (NLP): 70% (Dinamis)** - {safe_n1} dan {safe_n2} butuh saling toleransi dalam mengambil keputusan.")
                else: st.error(f"🔥 **SKOR META-PROGRAM (NLP): 50% (Rawan Gesekan)** - Sering terjadi perdebatan sudut pandang antara {safe_n1} dan {safe_n2}.")
     
                st.markdown("<br>", unsafe_allow_html=True)
                c_do_c, c_dont_c = st.columns(2)
                with c_do_c: 
                    st.markdown(f"<div style='background:rgba(37,211,102,0.1); padding:20px; border-radius:10px; border:1px solid #25D366;'>✅ <b>LAKUKAN INI (Taktik Dinamis):</b><br><br>{d_do}</div>", unsafe_allow_html=True)
                with c_dont_c: 
                    st.markdown(f"<div style='background:rgba(255,75,75,0.1); padding:20px; border-radius:10px; border:1px solid #ff4b4b;'>❌ <b>HINDARI INI (Bahaya Fatal):</b><br><br>{d_dont}</div>", unsafe_allow_html=True)
     
            except Exception as e:
                st.error(f"Sistem gagal membaca resonansi. Mohon ketik nama dengan benar. (Kode Error: {e})")
        else:
            st.warning("⚠️ Mohon isi kedua nama terlebih dahulu sebelum melakukan analisis.")

# ==========================================
# TAB 5: QUANTUM ENGINE (FATE HACKING)
# ==========================================
with tab5:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("⏱️ Live Cosmic Dashboard (Fate Hacking)")
    st.write("Sistem menyinkronkan data numerologi Anda dengan kalender rotasi planet dan matahari hari ini. Dapatkan taktik tindakan presisi detik ini juga.")
    
    col_qe1, col_qe2 = st.columns(2)
    with col_qe1: 
        qe_nama = st.text_input("Nama Panggilan:", key="qe_n")
    with col_qe2: 
        st.write(" ")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Hack My Reality Now"):
        if qe_nama:
            st.snow()
            safe_qe = get_safe_firstname(qe_nama)
            
            jummal_qe = hitung_nama_esoterik(qe_nama)
            angka_hari_ini = sum(int(d) for d in tgl_today.strftime("%d%m%Y"))
            mod_harian = (jummal_qe + angka_hari_ini) % 7
            
            fase_harian = {
                0: ("🔴 Rest & Reset", f"Energi saraf {safe_qe} di titik nadir. Bahaya mengambil keputusan keuangan/emosional. Lakukan hal repetitif saja."),
                1: ("🟢 Inisiasi", f"Momentum awal. Saatnya {safe_qe} mulai proyek baru, hubungi prospek, atau lempar ide ke atasan!"),
                2: ("🔵 Kolaborasi", f"Jangan kerja sendiri. {safe_qe} wajib cari rekan, negosiasi, atau minta bantuan. Pintu peluang lewat orang lain sedang terbuka."),
                3: ("🟡 Ekspresi", f"Aura komunikasi {safe_qe} sedang sangat terang. Update sosmed, bikin konten, presentasi, atau jual ide lo hari ini."),
                4: ("🟤 Pondasi", f"Fokus pada struktur. Waktunya {safe_qe} merapikan meja, bereskan file admin yang tertunda, atau audit keuangan lo."),
                5: ("🟠 Ekspansi & Risiko", f"Insting tajam. Waktu yang tepat untuk {safe_qe} mencoba rute baru, ambil risiko terkalkulasi, atau berpetualang ke tempat baru."),
                6: ("🟣 Pengayoman", f"Energi perlindungan {safe_qe} sangat tinggi di rumah. Selesaikan konflik batin dengan orang terdekat atau keluarga hari ini.")
            }
            siklus_hari_ini, saran_siklus = fase_harian.get(mod_harian, fase_harian[0])
            
            sun_fase, sun_desc = get_sun_phase()
            planet_live, planet_desc, planet_color = get_planetary_hour()
            
            st.markdown("---")
            st.markdown(f"### 📡 Live Dashboard: {safe_qe}")
            
            st.markdown(f"""
<div class="matrix-container">
<div class="matrix-item"><div class="matrix-label">Fase Bioritme Harian</div><div class="matrix-value">{siklus_hari_ini.split(' ')[1]}</div></div>
<div class="matrix-item"><div class="matrix-label">Posisi Matahari</div><div class="matrix-value matrix-value-special">{sun_fase.split(' ')[0]}</div></div>
<div class="matrix-item" style="border-bottom: 2px solid {planet_color};"><div class="matrix-label">Jam Planet Saat Ini</div><div class="matrix-value" style="color:{planet_color};">{planet_live}</div></div>
</div>
""", unsafe_allow_html=True)
            
            st.markdown(f"""
<div class="live-engine-box">
<h4 style="color: #00FFFF; margin-top:0;">⚡ TACTICAL ACTION PLAN (Untuk 1 Jam ke Depan)</h4>
<p style="color: #ccc; font-size: 15px; line-height: 1.6;">
Berdasarkan modulus angka nama dan kalender, sistem mendeteksi siklus pribadi <b>{safe_qe}</b> hari ini berada di fase <b>{siklus_hari_ini}</b>. <br>
<i>Saran Sistem:</i> {saran_siklus}
<br><br>
Ditambah posisi matahari yang berada di fase <b>{sun_fase}</b> ({sun_desc}), dan Jam Planet yang saat ini dikuasai oleh <b>{planet_live}</b> ({planet_desc}).
<br><br>
<b>🎯 KESIMPULAN TINDAKAN {safe_qe} SAAT INI:</b><br>
Mengacu pada data langit saat ini, Anda <u>diwajibkan</u> memfokuskan energi pada: <br>
<b style="color: #FFD700; font-size: 16px;">➤ Manfaatkan energi {planet_live.split(' ')[0]} ini untuk mengeksekusi misi fase {siklus_hari_ini.split(' ')[1]} Anda. Jangan ditunda, pergerakan energi ini akan bergeser dalam hitungan menit!</b>
</p>
</div>
""", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Ketik nama panggilan Anda untuk mensinkronisasi radar harian.")
 
# ==========================================
# TAB 3: FALAK RUHANI (SPIRITUAL ANCHORING)
# ==========================================
with tab3:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("🌌 Terapi Falak Ruhani (Spiritual Anchoring)")
    st.info("**Apa itu Falak Ruhani?**\n\nSistem mengonversi nama Anda menjadi angka getaran (Hisab Jummal), lalu mencocokkannya dengan frekuensi kosmik (Asmaul Husna) yang paling tepat untuk menghancurkan *mental block* dan menyembuhkan sistem saraf Anda.")
    
    nama_ruhani = st.text_input("Masukkan Nama Lengkap:", placeholder="Ketik nama asli Anda...", key="input_ruhani")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Aktivasi Anchor Spiritual"):
        if nama_ruhani and len(nama_ruhani.strip()) >= 3:
            st.snow()
            safe_nr = get_safe_firstname(nama_ruhani)
            nilai_jummal_r = hitung_nama_esoterik(nama_ruhani)
            
            # Cari Root Number
            r_num_r = nilai_jummal_r
            while r_num_r > 9: r_num_r = sum(int(d) for d in str(r_num_r))
            
            asma_terapi, vibrasi_asma, tujuan_ruhani, jumlah_dzikir = proc_falak_ruhani(nilai_jummal_r, r_num_r, safe_nr)
            
            st.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(10, 20, 40, 0.9) 0%, rgba(20, 10, 40, 0.9) 100%); border-left: 5px solid #00FFFF; padding: 25px; border-radius: 12px; margin-top: 20px; margin-bottom: 20px; box-shadow: 0 8px 25px rgba(0, 255, 255, 0.15);">
    <div style="text-align:center; border-bottom:1px solid #00FFFF; padding-bottom:10px; margin-bottom:15px;">
        <span style="color:#00FFFF; font-size:14px; font-weight:900; letter-spacing:2px;">🔮 PRESKRIPSI RUHANI: {safe_nr}</span>
    </div>
    <p style="color:#ccc; font-size:14px; line-height:1.6;">
        Secara metafisika Islam (Ilmu Al-Tanjim), setiap nama memiliki "Anchor Spiritual" (Jangkar Batin). Untuk menetralisir kelemahan mental (Shadow) dan mengaktifkan gelombang kesuksesan, <b>{safe_nr}</b> diwajibkan menyelaraskan diri dengan frekuensi kosmik berikut:
    </p>
    <div style="background: rgba(0,0,0,0.5); padding: 15px; border-radius: 8px; margin-bottom: 15px;">
        <b style="color:#FFF; font-size:18px;">✨ Frekuensi Asma: <span style="color:#00FFFF;">{asma_terapi}</span></b><br>
        <b style="color:#FFD700; font-size:14px;">Resonansi:</b> <i style="color:#fff;">{vibrasi_asma}</i><br>
        <b style="color:#25D366; font-size:14px;">Tujuan Terapi:</b> <i style="color:#ccc;">{tujuan_ruhani}</i>
    </div>
    <div style="border-top: 1px dashed #555; padding-top: 10px;">
        <b style="color:#FFD700;">⚙️ Taktik Eksekusi (Quantum Habit):</b><br>
        <span style="color:#aaa; font-size:14px;">Gunakan asma di atas sebagai afirmasi batin atau dzikir harian. Rapalkan sebanyak <b><span style="color:#00FFFF; font-size:18px;">{jumlah_dzikir}x</span></b> <i>(Presisi sesuai nilai Gematria nama Anda)</i>. Lakukan saat Jam Planet sedang dikuasai oleh <b>Bulan 🌙</b> (untuk ketenangan) atau <b>Yupiter 🍀</b> (untuk kelancaran bisnis).</span>
    </div>
</div>
""", unsafe_allow_html=True)
            
            # CTA Opsional
            st.markdown(f"""
            <div class="info-metric-box" style="text-align: center;">
            <b style="color:#FFD700;">Butuh panduan suara untuk masuk gelombang Alpha/Theta?</b><br>
            Akses Hypno-Audio Vault untuk mempercepat proses instalasi afirmasi di atas.<br><br>
            <a href="{link_produk.get(r_num_r, 'https://lynk.id/neuronada')}" target="_blank" style="text-decoration: none;">
                <span class="live-badge">🎧 BUKA HYPNO-AUDIO VAULT</span>
            </a>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.warning("⚠️ Mohon ketik nama lengkap Anda (minimal 3 huruf) untuk sinkronisasi vibrasi.")

# ==========================================
# TAB 4: FAQ & DISCLAIMER (WISDOM UPDATE)
# ==========================================
with tab4:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("📚 FAQ & Navigasi Energi")
    
    with st.expander("🤔 1. Apa itu Jam Planet (Planetary Hours)?"):
        st.write("""
        Berbeda dengan jam dinding biasa, **Jam Planet** adalah sistem pembagian waktu astronomi kuno yang membagi siang dan malam menjadi 12 fase energi. 
        Setiap jam dikuasai oleh satu planet yang memengaruhi 'cuaca mental' manusia di bumi.
        """)
        st.markdown("""
        | Planet | Karakter Energi | Tindakan Terbaik |
        | :--- | :--- | :--- |
        | **Matahari** | Otoritas & Fokus | Presentasi, negosiasi, memimpin. |
        | **Venus** | Harmoni & Seni | Kencan, mediasi, mempercantik diri/karya. |
        | **Merkurius** | Logika & Data | Menulis, belajar, kirim email penting. |
        | **Bulan** | Intuisi & Emosi | Refleksi, mendengarkan klien, istirahat. |
        | **Saturnus** | Disiplin & Beban | Beresin admin, audit, bayar hutang. |
        | **Yupiter** | Ekspansi & Hoki | Launching bisnis, investasi, cari peluang. |
        | **Mars** | Aksi & Keberanian | Olahraga, eksekusi tugas berat, debat. |
        """)
        
    with st.expander("🤔 2. Apa itu Hisab Jummal (Angka Esoterik)?"):
        st.write("Hisab Jummal (Gematria Arab) adalah ilmu sains huruf kuno yang memberikan bobot matematika pada setiap aksara. Sistem ini meyakini bahwa nama yang diberikan sejak lahir membawa frekuensi atau getaran energi tertentu yang mempengaruhi sistem saraf dan karakter bawaan Anda.")
        
    with st.expander("🤔 3. Apakah hasil ini 100% mutlak/ramalan pasti?"):
        st.write("TIDAK. Neuro Nada bukan alat peramal nasib, melainkan **Alat Pemetaan Pola (Pattern Mapping)**. Sistem ini menggabungkan Metafisika Kuno (Primbon/Falak) dengan pendekatan Psikologi Modern (Neuro-Linguistic Programming). Tujuannya adalah untuk memberikan *Self-Awareness*.")
        
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
