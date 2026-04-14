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

def generate_seed(base_str):
    return int(hashlib.md5(base_str.encode('utf-8')).hexdigest(), 16) % (10**8)

# --- ENGINE FALAK RUHANI (SPIRITUAL ANCHORING) ---
def proc_falak_ruhani(total_jummal, root_num, nama):
    ruhani_data = {
        1: {"asma": "Ya Fattah (Maha Pembuka)", "vibrasi": "Mendobrak Jalan Buntu & Ego", "tujuan": "Membersihkan hambatan ego, menaklukkan keras kepala, dan membuka pintu rezeki yang terkunci akibat kesombongan tak sadar."},
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

# --- PROTOKOL TERAPI DINAMIS ---
def get_protokol_terapi(root_num, nama):
    random.seed(generate_seed(f"pt_{nama}_{root_num}"))
    
    b1 = random.choice([
        f"Ego Supremacy. Anda ({nama}) cenderung menolak bantuan karena merasa harus bisa sendiri. Ujungnya? Kelelahan ekstrem (Burnout).",
        f"Lone Wolf Syndrome. Gengsi {nama} terlalu tinggi untuk minta tolong. Bahayanya, Anda sering merasa berjuang sendirian di dunia ini."
    ])
    a1 = random.choice([
        f"Saya, {nama}, dengan sadar menurunkan perisai ego saya. Meminta tolong adalah bentuk pendelegasian, bukan kelemahan. Saya mengizinkan Semesta bekerja membantu saya.",
        f"Mulai detik ini, saya ({nama}) sadar bahwa kolaborasi adalah kunci. Saya pantas dibantu, dan saya membuka diri untuk menerima kemudahan."
    ])
    h1 = random.choice([
        "Hari ini, cari 1 tugas sepele dan minta tolong orang lain untuk mengerjakannya. Ucapkan terima kasih dengan tulus tanpa mengkritik hasilnya.",
        "Hubungi satu teman atau mentor hari ini, ceritakan satu kendala kecil Anda, dan mintalah saran mereka tanpa berdebat."
    ])

    b2 = random.choice([
        f"People Pleasing. {nama} sering menyerap energi negatif orang lain dan menekan kemarahan diri sendiri demi 'terlihat rukun'.",
        f"Spons Emosi. Anda terlalu gampang merasa nggak enakan. Hidup {nama} sering tersabotase demi menjaga perasaan orang yang bahkan nggak peduli."
    ])
    a2 = random.choice([
        f"Saya, {nama}, memegang kendali penuh atas energi saya. Kebahagiaan saya adalah prioritas utama, dan batas (boundaries) saya adalah suci.",
        f"Saya ({nama}) melepaskan rasa bersalah. Saya tidak bertanggung jawab atas kekecewaan orang lain saat saya memilih untuk merawat diri saya sendiri."
    ])
    h2 = random.choice([
        "Berlatih berkata 'Tidak' pada satu permintaan kecil hari ini tanpa memberikan alasan panjang lebar atau basa-basi.",
        "Matikan notifikasi chat dari grup/orang yang paling sering menyerap energi Anda selama minimal 6 jam hari ini."
    ])

    b3 = random.choice([
        f"Scattered Focus. Otak {nama} memproduksi ratusan ide brilian tapi nol eksekusi. Energi habis di overthinking.",
        f"Impulsivitas Ide. Anda ({nama}) gampang bosan. Baru mulai satu hal, udah lompat ke hal lain. Potensi besar yang menguap jadi wacana."
    ])
    a3 = random.choice([
        f"Saya, {nama}, menyalurkan kreativitas ke dalam struktur yang nyata. Satu eksekusi kecil jauh lebih berharga daripada seribu ide yang melayang.",
        f"Pikiran saya jernih. Saya ({nama}) mengizinkan diri saya untuk menyelesaikan apa yang sudah saya mulai dengan penuh ketenangan."
    ])
    h3 = random.choice([
        "Pilih 1 ide saja. Tulis di kertas, lalu kerjakan langkah pertamanya selama 15 menit tanpa membuka HP/Sosmed sama sekali.",
        "Rapikan meja kerja atau kamar Anda hari ini. Kekacauan fisik adalah cerminan kekacauan isi kepala Anda."
    ])

    b4 = random.choice([
        f"Scarcity Mindset. Ketakutan bawah sadar akan kegagalan, membuat pola pikir {nama} menjadi sangat kaku dan pelit pada diri sendiri.",
        f"Mental Block Kemiskinan. Anda ({nama}) sering merasa 'harus nabung untuk jaga-jaga hal buruk', yang secara tak sadar justru menarik nasib buruk."
    ])
    a4 = random.choice([
        f"Saya, {nama}, melepaskan rasa takut akan kekurangan. Sumber daya Semesta tidak terbatas. Saya aman dan rezeki mengalir dalam harmoni.",
        f"Saya ({nama}) layak hidup berkelimpahan. Uang adalah energi yang baik, dan saya mengizinkannya datang dari arah yang tak terduga."
    ])
    h4 = random.choice([
        "Beri hadiah kecil (reward) untuk diri sendiri hari ini (ngopi enak atau beli sesuatu), rasakan emosi kelimpahannya.",
        "Lakukan sedekah subuh/pagi hari ini berapapun nominalnya, niatkan secara sadar untuk 'melatih otot melepaskan'."
    ])

    b5 = random.choice([
        f"Escapism. {nama} sering kabur dari tanggung jawab jangka panjang dengan dalih 'mencari kebebasan'.",
        f"Sindrom Cepat Bosan. Saat menghadapi tekanan yang butuh konsistensi, saraf {nama} mendadak mati rasa dan ingin menyerah."
    ])
    a5 = random.choice([
        f"Saya, {nama}, menemukan kedalaman sejati di dalam komitmen. Menetap bukanlah penjara, melainkan pondasi kesuksesan saya.",
        f"Saya ({nama}) mengontrol rasa bosan saya. Saya menanam akar yang kuat hari ini untuk memanen kebebasan finansial esok hari."
    ])
    h5 = random.choice([
        "Selesaikan satu pekerjaan membosankan yang sudah Anda tunda berminggu-minggu sampai 100% tuntas hari ini.",
        "Lakukan rutinitas pagi yang sama persis selama 3 hari berturut-turut tanpa mengubah polanya sedikitpun."
    ])

    b6 = random.choice([
        f"Savior Complex. {nama} sering merasa bersalah jika menikmati hidup sementara orang di sekitarnya masih susah.",
        f"Luka Pengorbanan. Anda ({nama}) memberikan 100% energi untuk keluarga/teman, tapi diam-diam merasa kosong dan tidak dihargai."
    ])
    a6 = random.choice([
        f"Saya, {nama}, mengizinkan diri saya bahagia. Merawat diri sendiri adalah syarat mutlak sebelum merawat orang lain.",
        f"Cinta saya berlimpah, dan penerima pertama cinta itu adalah saya sendiri. Saya ({nama}) berhak menikmati keringat saya."
    ])
    h6 = random.choice([
        "Ambil waktu 30 menit murni untuk 'Me-Time' tanpa memikirkan urusan anak, pasangan, atau pekerjaan.",
        "Beli makanan kesukaan Anda hari ini, dan makanlah pelan-pelan sendirian tanpa membaginya atau memikirkan orang rumah."
    ])

    b7 = random.choice([
        f"Paralysis by Analysis. {nama} terlalu banyak menganalisa niat orang lain, ujungnya memenjarakan diri dalam rasa curiga.",
        f"Trust Issue. Sifat skeptis ekstrim membuat {nama} sering menolak peluang bagus karena selalu mencari 'di mana celahnya'."
    ])
    a7 = random.choice([
        f"Saya, {nama}, menyeimbangkan logika saya dengan intuisi. Saya mempercayai proses, dan saya mengizinkan hal baik terjadi tanpa dianalisa berlebihan.",
        f"Saya ({nama}) melepaskan kebutuhan untuk mengetahui segalanya. Saya aman berada di momen saat ini."
    ])
    h7 = random.choice([
        "Lakukan 'Silence Meditation' (diam total tanpa HP) selama 10 menit, amati saja napas tanpa memikirkan masalah apapun.",
        "Percayai satu ucapan/janji orang hari ini tanpa Anda *cross-check* atau Anda pertanyakan motivasinya."
    ])

    b8 = random.choice([
        f"Control Freak. {nama} memforsir tubuh dan orang lain tanpa ampun demi mengejar validasi kesuksesan material.",
        f"Obsesi Material. Ambisi {nama} sangat membakar, tapi seringkali menghancurkan kedamaian batin dan menjauhkan orang yang peduli."
    ])
    a8 = random.choice([
        f"Saya, {nama}, adalah saluran kelimpahan, bukan budak ambisi. Kekuatan sejati saya terletak pada kemampuan untuk berserah setelah berusaha.",
        f"Saya ({nama}) melepaskan kendali yang menyiksa. Saya sukses, berwibawa, namun hati saya tetap lembut dan damai."
    ])
    h8 = random.choice([
        "Delegasikan satu kendali hari ini. Biarkan orang lain yang menyetir atau mengambil keputusan tempat makan, dan nikmati saja prosesnya.",
        "Berhenti bekerja tepat jam 5 sore hari ini. Matikan laptop, dan jangan sentuh urusan bisnis sampai besok pagi."
    ])

    b9 = random.choice([
        f"Toxic Empathy. {nama} terlalu gampang merasa kasihan pada orang toxic, dan memikul kesedihan dunia di bahu sendiri.",
        f"Luka Ekspektasi Luluh. Karena standar moral {nama} sangat tinggi, Anda sering kecewa parah saat melihat realita manusia yang egois."
    ])
    a9 = random.choice([
        f"Saya, {nama}, melepaskan apa yang berada di luar kendali saya. Saya membiarkan setiap jiwa bertumbuh melalui ujiannya masing-masing.",
        f"Tugas saya ({nama}) bukanlah menyelamatkan semua orang. Energi saya suci dan saya menjaganya dari hal-hal yang tidak memberdayakan."
    ])
    h9 = random.choice([
        "Detoks informasi negatif. Jangan tonton berita duka atau baca keluh kesah orang di sosmed selama 24 jam penuh.",
        "Berhenti memberikan nasihat/solusi kepada siapapun hari ini kecuali jika mereka secara eksplisit memintanya."
    ])

    protokol = {
        1: {"block": b1, "afirmasi": a1, "habit": h1},
        2: {"block": b2, "afirmasi": a2, "habit": h2},
        3: {"block": b3, "afirmasi": a3, "habit": h3},
        4: {"block": b4, "afirmasi": a4, "habit": h4},
        5: {"block": b5, "afirmasi": a5, "habit": h5},
        6: {"block": b6, "afirmasi": a6, "habit": h6},
        7: {"block": b7, "afirmasi": a7, "habit": h7},
        8: {"block": b8, "afirmasi": a8, "habit": h8},
        9: {"block": b9, "afirmasi": a9, "habit": h9}
    }
    return protokol.get(root_num, protokol[1])

def proc_arketipe(nama, angka, zodiak, neptu):
    random.seed(generate_seed(f"hyper_ark_{nama}_{angka}_{zodiak}_{neptu}"))
    buka = random.choice([
        f"Melalui persilangan matriks waktu dan elemen {zodiak}, DNA numerologi **{nama}** mengunci kuat pada **KODE {angka}**.",
        f"Kalkulasi semesta menyempit di **KODE {angka}**. Ini menandakan bahwa sejak lahir, alam bawah sadar **{nama}**",
        f"Sistem mendeteksi getaran **KODE {angka}** pada diri Anda. Secara genetik dan arsitektur mental, **{nama}**",
        f"Berdasarkan algoritma kepribadian {zodiak} yang melebur dengan weton, cetak biru **{nama}** adalah **KODE {angka}**."
    ])
    inti = {
        1: ["sebagai sosok perintis yang didesain untuk memimpin dan menembus batas.", "memiliki dorongan mutlak untuk mandiri dan benci didikte."],
        2: ["sebagai Sang Penyelaras yang mampu menetralisir konflik.", "memiliki radar empati tingkat dewa untuk membaca ruang dan emosi."],
        3: ["sebagai komunikator handal dengan pikiran yang meletup-letup seperti kembang api.", "memiliki anugerah kreativitas tanpa batas."],
        4: ["sebagai arsitek kehidupan yang sangat sistematis dan presisi.", "memiliki pola pikir logis yang menjadikannya pondasi kuat."],
        5: ["sebagai simbol kebebasan yang menolak keras rutinitas monoton.", "memiliki kelincahan otak untuk beradaptasi cepat."],
        6: ["sebagai pelindung sejati dengan insting pengayom yang luar biasa.", "memegang standar tanggung jawab moral yang sangat tinggi."],
        7: ["sebagai pencari kebenaran esensial dengan intuisi yang tajam.", "tidak pernah puas dengan jawaban dangkal dan selalu menganalisa."],
        8: ["sebagai eksekutor tangguh dengan insting material yang sangat presisi.", "memiliki fokus bawah sadar yang ditarik kuat menuju puncak otoritas."],
        9: ["sebagai 'Jiwa Tua' yang memandang dunia dengan kacamata kebijaksanaan.", "memiliki tingkat kepedulian universal yang melampaui ego."]
    }
    gaya = {
        1: ["Anda adalah inisiator cepat yang lebih suka bertindak daripada rapat.", "Anda memancarkan aura alpha kemanapun Anda pergi."],
        2: ["Anda adalah pendengar ulung tempat orang lain membuang keluh kesah.", "Gaya kerja Anda kolaboratif; memastikan tim merasa dihargai."],
        3: ["Anda memecahkan masalah dengan ide *out-of-the-box*.", "Anda ahli mencairkan ketegangan lewat humor spontan."],
        4: ["Anda mengeksekusi visi dengan langkah terukur dan tanpa cacat.", "Lingkungan melihat Anda sebagai sosok yang dingin namun selalu selesai tugas."],
        5: ["Anda paling bersinar saat diletakkan di situasi *chaos* yang butuh pemecahan instan.", "Gaya hidup Anda nomaden secara mental; mudah bosan."],
        6: ["Anda memimpin dengan hati, bertindak layaknya orang tua bagi teman-teman Anda.", "Loyalitas Anda tidak perlu diragukan untuk membela sirkel."],
        7: ["Anda mengobservasi dalam diam sebelum mengambil keputusan strategis.", "Gaya sosial Anda misterius; tidak banyak yang tahu isi kepala Anda."],
        8: ["Anda mengorganisir sumber daya dengan tangan besi yang elegan.", "Aura wibawa Anda sering membuat orang segan sebelum Anda bicara."],
        9: ["Anda merangkul keberagaman dan memimpin lewat contoh pengorbanan.", "Orang sering datang meminta nasihat karena kedewasaan batin Anda."]
    }
    shadow = {
        1: ["Waspadai rasa kesepian akibat ego yang membangun tembok pemisah.", "Sisi gelapnya, Anda rawan terjebak sifat arogan."],
        2: ["Waspadai memendam amarah terus-menerus yang bisa jadi bom waktu.", "Bahayanya, Anda sering menyerap energi beracun (toxic)."],
        3: ["Sisi gelapnya, rawan berbicara impulsif saat harga diri tersinggung.", "Musuh terbesar Anda adalah hilangnya fokus."],
        4: ["Bahayanya, dinilai tidak punya perasaan karena kaku pada aturan.", "Waspadai sifat over-micromanaging yang membuat gerah."],
        5: ["Waspadai 'Sindrom Cepat Bosan' yang mensabotase karir/asmara.", "Bahayanya, cenderung melarikan diri (escapism) dari komitmen berat."],
        6: ["Sangat rentan *burnout* ekstrem mengurus beban orang lain.", "Bahayanya, dihantui rasa bersalah tak masuk akal saat *me-time*."],
        7: ["Sering terjebak *Paralysis by Analysis* (overthinking tanpa aksi).", "Waspadai kecenderungan mengisolasi diri saat merasa tidak dihargai."],
        8: ["Kesulitan melepaskan kendali dan memaafkan pengkhianatan.", "Rentang mendominasi pasangan secara emosional tanpa sadar."],
        9: ["Rawan patah hati kronis karena ekspektasi luhur berbenturan realitas.", "Energi batin gampang terkuras memikirkan penderitaan dunia."]
    }
    saran = {
        1: "Belajarlah mendelegasikan tugas. Meminta tolong adalah taktik kepemimpinan.",
        2: "Berlatihlah mengatakan 'TIDAK' tanpa merasa bersalah.",
        3: "Paksa diri Anda menuntaskan satu proyek kecil hari ini sebelum melompat ke ide lain.",
        4: "Biarkan ruang untuk spontanitas. Kadang berantakan sedikit adalah terapi.",
        5: "Temukan kebebasan dalam komitmen panjang.",
        6: "Buatlah batas yang tegas. Berhenti menyelamatkan orang toxic.",
        7: "Turunkan ekspektasi Anda terhadap ketidaksempurnaan manusia.",
        8: "Latih diri berserah di momen istirahat. Kesuksesan butuh sistem saraf sehat.",
        9: "Anda tidak diutus memikul galaksi. Cintai diri sendiri dulu."
    }
    return f"{buka} Anda didesain {random.choice(inti[angka])} {random.choice(gaya[angka])} {random.choice(shadow[angka])} Pesan Semesta: {saran[angka]}"

def proc_shadow_list(nama, angka):
    random.seed(generate_seed(f"shd_{nama}_{angka}"))
    semua_shadow = {
        1: ["Gengsi minta tolong saat memikul beban", "Membangun tembok ego untuk menutupi sepi", "Overthinking merasa hasil belum sempurna", "Kesulitan menerima kritik", "Mengabaikan lelah demi target"],
        2: ["Mengorbankan kebahagiaan demi ekspektasi", "Sulit berkata TIDAK (People Pleaser)", "Memendam amarah hindari konflik", "Terlalu bergantung validasi", "Menyerap energi toxic"],
        3: ["Menyembunyikan gelisah di balik topeng ceria", "Cepat kehilangan motivasi", "Insomnia karena over-analisa", "Kesulitan fokus prioritas", "Bicara impulsif saat tersinggung"],
        4: ["Stres parah jika rencana mendadak berubah", "Terjebak zona nyaman takut risiko", "Sering dinilai terlalu dingin", "Over-micromanaging", "Menghakimi orang tak disiplin"],
        5: ["Sindrom Bosan mensabotase karya", "Kelelahan saraf otak jalan terus", "Merasa hampa hilang pijakan", "Lari (escapism) saat ditekan", "Kesulitan rutinitas panjang"],
        6: ["Burnout mengurus hidup orang lain", "Sikap Over-Protective mengekang", "Rasa bersalah jika me time", "Terlalu ikut campur keluarga", "Mengharap balasan emosional"],
        7: ["Menganalisa terus tanpa aksi (Paralysis)", "Merasa terasing/tak sepemikiran", "Mencurigai niat baik orang", "Sinis dan sarkastik", "Menutup diri saat emosi memuncak"],
        8: ["Sulit melepaskan kontrol/memaafkan", "Memaksa tubuh abaikan alarm lelah", "Menilai orang dari sisi guna/status", "Ketakutan berlebih menjadi lemah", "Mendominasi pasangan"],
        9: ["Memaklumi toxic atas nama kasihan", "Patah hati akibat ekspektasi manusia", "Kelelahan memikirkan beban semesta", "Sering merasa tidak pantas", "Kehilangan jati diri demi visi"]
    }
    return random.sample(semua_shadow[angka], 3)

def proc_couple_persona(root_c, n1, n2):
    random.seed(generate_seed(f"cp_{n1}_{n2}_{root_c}"))
    buka = random.choice([
        f"Ketika vibrasi nama **{n1}** dan **{n2}** dilebur, hasilnya mengunci di **Root {root_c}**.",
        f"Hukum resonansi mencatat persatuan **{n1}** dan **{n2}** menghasilkan gelombang **Root {root_c}**."
    ])
    desc = {
        1: ("THE POWER COUPLE", f"Kalian memancarkan simbol Alpha. {n1} dan {n2} membentuk entitas ambisius, fokus pada kemajuan karir."),
        2: ("THE SOULMATES", f"Kalian memiliki 'Wi-Fi' batin. Mudah bagi {n1} memahami emosi {n2} tanpa banyak kata. Harmoni adalah kunci."),
        3: ("THE SOCIALITES", f"Aura kalian magnetis. {n1} dan {n2} adalah pasangan menyenangkan yang selalu menghidupkan suasana sirkel."),
        4: ("THE BUILDERS", f"Hubungan ini berpijak pada bumi. Fokus {n1} dan {n2} adalah membangun aset keluarga dan kesetiaan absolut."),
        5: ("THE ADVENTURERS", f"Kalian dipenuhi energi kebebasan. {n1} maupun {n2} butuh kejutan dan tantangan agar cinta tetap menyala."),
        6: ("THE FAMILY FIRST", f"Simbol pengayoman tertinggi. Pengorbanan {n1} dan {n2} untuk merawat keutuhan rumah tangga sangat mendalam."),
        7: ("THE DEEP SEEKERS", f"Hubungan tertutup dan eksklusif. {n1} dan {n2} membangun koneksi intelektual dengan privasi yang sulit ditembus."),
        8: ("THE EMPIRE", f"Magnet kelimpahan mutlak. Penyatuan ego {n1} dan {n2} mengejar kesuksesan bisnis dan membangun kerajaan keluarga."),
        9: ("THE HEALERS", f"Puncak kedewasaan empati. Interaksi {n1} dan {n2} dipenuhi toleransi dan menjadi tempat penyembuhan bagi sirkel sekitar.")
    }
    return desc.get(root_c, ("UNCHARTED SYNERGY", "Anomali energi tak tertebak."))[0], f"{buka} {desc.get(root_c)[1]}"

def proc_weton_kombo(sisa, n1, n2, z1, z2):
    random.seed(generate_seed(f"wt_{n1}_{n2}_{sisa}_{z1}_{z2}"))
    do_list = {
        1: [f"Gunakan *Pacing-Leading*: Validasi perasaan {n2} dulu.", f"Beri jeda saat argumen memanas, biarkan ego {z1} & {z2} reda."],
        2: [f"Jadikan {n2} Partner Strategis.", f"Bangun diskusi karir, energi {z1} mu akan memompa {n2}."],
        3: [f"Ciptakan *Pattern Interrupt*. Kencan dadakan agar tak hambar.", f"Pancing *deep-talk* rutin agar koneksi {n1} & {n2} tajam."],
        4: [f"Kuasai *Reframing* saat krisis.", f"Perkuat daya tahan. Badai di awal adalah ujian rezeki besar."],
        5: [f"Sesi visi masa depan. Kedamaian emosi adalah kunci rezeki.", f"Kelola keuangan bersama transparan."],
        6: [f"Berikan *Space* saat tensi naik.", f"Gunakan humor untuk memecah ketegangan argumen."],
        7: [f"Komunikasi berbasis fakta (*Sensory Based*).", f"Validasi ulang setiap instruksi menghindari salah paham dadakan."],
        8: [f"Pertahankan *Rapport* dengan hobi baru.", f"Sesekali keluar dari zona nyaman."]
    }
    dont_list = {
        1: [f"DILARANG keras *Mind-Reading* negatif ke {n2}.", f"Jangan adu argumen saat {n2} lapar/lelah fisik."],
        2: [f"Hindari jebakan pencitraan. Pura-pura bahagia di luar.", f"Jangan biarkan campur tangan sirkel merusak wibawa."],
        3: [f"Hati-hati *Comfort Zone*. Malas berjuang karir.", f"Jangan abaikan perawatan diri karena merasa aman."],
        4: [f"Jangan paksakan gengsi {n1} kepada {n2}.", f"Pantang menyerah di 3 tahun pertama."],
        5: [f"Jangan jadikan uang satu-satunya perekat {n1} & {n2}.", f"Jangan sombong saat pintu rezeki terbuka."],
        6: [f"Jangan serang harga diri {n2} secara frontal.", f"Dilarang *Silent Treatment* lebih dari 24 jam."],
        7: [f"DILARANG pakai kata absolut ('TIDAK PERNAH peduli!').", f"Jangan mengintai privasi digital pasangan secara diam-diam."],
        8: [f"Waspadai sikap *Take it for granted* menggampangkan pasangan.", f"Jangan biarkan rutinitas mematikan romantisme."]
    }
    hasil = {
        1: ("💔 PEGAT (Ujian Ego)", "Terdapat perbedaan fundamental memproses emosi. Sering adu argumen keras karena sama-sama rasional."),
        2: ("👑 RATU (Kharisma Pasangan)", "Memancarkan wibawa. Orang lain segan melihat kalian berdua. Saling menopang sempurna."),
        3: ("💞 JODOH (Sinkronisasi Alami)", "Penerimaan bawah sadar tinggi. Seolah sudah terhubung sejak kehidupan sebelumnya."),
        4: ("🌱 TOPO (Ujian Bertumbuh)", "Awal kolaborasi penuh ujian adaptasi berat. Lewati kritis ini, pondasi kalian takkan tertembus badai."),
        5: ("💰 TINARI (Magnet Rezeki)", "Magnet kelimpahan. Kelancaran finansial biasanya mendadak terbuka lebar setelah sepakat bersatu."),
        6: ("⚡ PADU (Beda Frekuensi)", "Sering ada letupan perdebatan karena beda filter informasi. Meributkan hal kecil tak prinsipil."),
        7: ("👁️ SUJANAN (Rawan Asumsi)", "Rawan miskomunikasi dan cemburu buta. Asumsi bawah sadar memicu salah paham jika tak dikomunikasikan."),
        8: ("🕊️ PESTHI (Damai & Rukun)", "Interaksi adem ayem minim drama. Kehadiran pasangan menetralisir stres harian.")
    }
    return hasil[sisa][0], hasil[sisa][1], random.choice(do_list[sisa]), random.choice(dont_list[sisa])

def proc_penjelasan_matriks(n1, n2, eso_val, nep_val):
    random.seed(generate_seed(f"pm_v2_{n1}_{n2}_{eso_val}_{nep_val}"))
    header = random.choice(["⚙️ ARSITEKTUR ANALISA", "📡 DEKODE SINYAL KOSMIK", "📜 LOGIKA MESIN NEURO"])
    f_eso = random.choice([f"Fusi nama <b>{n1}</b> & <b>{n2}</b> mengunci di <b>{eso_val}</b>. Ini adalah persona yang muncul saat kalian bersama.", f"Ekstraksi sandi menghasilkan <b>{eso_val}</b>. Menentukan bagaimana kalian dipandang sebagai entitas."])
    f_nep = random.choice([f"Kalkulasi sinkronisasi waktu (Total Neptu <b>{nep_val}</b>) memetakan dinamika ego bawah sadar.", f"Analisa siklus (Parameter <b>{nep_val}</b>) menjadi radar pengukur stabilitas emosi kalian."])
    return f'<div class="info-metric-box"><b style="color:#FFD700; font-size:14px;">{header}:</b><br>• <b style="color:white;">TOTAL ESOTERIK:</b> {f_eso}<br>• <b style="color:white;">TOTAL NEPTU:</b> {f_nep}</div>'

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

KAMUS_ABJAD = {
    'a': 1, 'b': 2, 'j': 3, 'd': 4, 'h': 5, 'w': 6, 'z': 7, 
    't': 9, 'y': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 
    's': 60, 'f': 80, 'q': 100, 'r': 200, 'c': 3, 'e': 5,
    'g': 1000, 'i': 10, 'o': 6, 'p': 80, 'u': 6, 'v': 6, 'x': 60
}

def hitung_nama_esoterik(nama):
    nama_clean = ''.join(filter(str.isalpha, str(nama).lower()))
    return sum(KAMUS_ABJAD.get(huruf, 0) for huruf in nama_clean) or 1

def get_rincian_esoterik(nama):
    r = [f"{h.upper()}({KAMUS_ABJAD.get(h,0)})" for h in ''.join(filter(str.isalpha, str(nama).lower())) if KAMUS_ABJAD.get(h,0)>0]
    return " + ".join(r) if r else "0"

def generate_dynamic_reading(total_jummal):
    mod = total_jummal % 4 if total_jummal % 4 != 0 else 4
    el = {1: ("🔥 API (Nar)", "Sistem saraf eksekusi cepat, Anda inisiator."), 2: ("🌍 TANAH (Turab)", "Fondasi logis dan membumi."), 3: ("💨 UDARA (Hawa)", "Konseptor ide tanpa henti."), 4: ("💧 AIR (Ma')", "Emosional peka, empati beradaptasi.")}
    p_red = " + ".join(list(str(total_jummal)))
    s_red = sum(int(d) for d in str(total_jummal))
    r_num = s_red
    while r_num > 9: r_num = sum(int(d) for d in str(r_num))
    r_dict = {1:"Pencipta jalan baru", 2:"Penyelaras harmoni", 3:"Penyampai pesan", 4:"Pembangun sistem", 5:"Agen transformasi", 6:"Pengayom sejati", 7:"Pencari esensi", 8:"Pemegang kendali", 9:"Kesadaran universal"}
    m_note = "<div style='background:rgba(212,175,55,0.1); padding:10px; border-radius:5px;'><span style='color:#FFD700;'>⚡ <b>KODE MASTER:</b></span> Intuisi Spiritual Tinggi Terdeteksi.</div>" if any(m in str(total_jummal) for m in ["11","22","33"]) else ""
    return el[mod][0], el[mod][1], p_red, s_red, r_num, r_dict.get(r_num,""), m_note

def hitung_angka(tanggal):
    try:
        t = sum(int(digit) for digit in tanggal.strftime("%d%m%Y"))
        while t > 9: t = sum(int(digit) for digit in str(t))
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

def hitung_neptu_langsung(hari, pasaran):
    return {"Minggu":5,"Senin":4,"Selasa":3,"Rabu":7,"Kamis":8,"Jumat":6,"Sabtu":9}.get(hari,0) + {"Legi":5,"Pahing":9,"Pon":7,"Wage":4,"Kliwon":8}.get(pasaran,0)
 
def get_betaljemur_data(neptu, hari):
    lk = {7:("Lebu Katiup Angin","Pikiran dinamis"),8:("Lakuning Geni","Emosi meledak-ledak"),9:("Lakuning Angin","Adaptif namun labil"),10:("Pandito Mbangun Teki","Introspektif, cerdas"),11:("Aras Tuding","Pemberani, ditunjuk peluang"),12:("Aras Kembang","Menebar pesona"),13:("Lakuning Lintang","Magnetis menyendiri"),14:("Lakuning Rembulan","Penenang batin"),15:("Lakuning Srengenge","Pencerah logis"),16:("Lakuning Banyu","Ketenangan mematikan"),17:("Lakuning Bumi","Sabar membumi"),18:("Lakuning Paripurna","Pemegang kendali bijak")}
    nd = {"Minggu":"Timur", "Senin":"Selatan", "Selasa":"Barat", "Rabu":"Utara", "Kamis":"Timur", "Jumat":"Selatan", "Sabtu":"Selatan"}
    return lk.get(neptu,("Anomali",""))[0], lk.get(neptu,("Anomali",""))[1], nd.get(hari,"Netral")

def get_rezeki_usaha(neptu):
    r = {1:("Wasesa Segara","Rezeki seluas lautan"),2:("Tunggak Semi","Patah tumbuh hilang berganti"),3:("Satria Wibawa","Dihormati kolega"),4:("Sumur Sinaba","Menjadi referensi, membawa berkah"),5:("Bumi Kapetak","Kerja cerdas dan keras"),6:("Satria Wirang","Rawan rintangan"),7:("Lebu Katiup Angin","Wajib punya aset tetap")}[neptu%7 or 7]
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

def get_safe_firstname(name_str, default="User"):
    return str(name_str).strip().split()[0].upper() if str(name_str).strip() else default

# --- SIDEBAR PROMOSI ---
with st.sidebar:
    if os.path.exists("baru.jpg.png"):
        try: st.image("baru.jpg.png", use_container_width=True); st.markdown("<br>", unsafe_allow_html=True)
        except: pass
    elif os.path.exists("baru.jpg"): st.image("baru.jpg", use_container_width=True)
 
    st.markdown(f"### {get_greeting()}")
    st.info("**Reset Pola Pikir Anda**\n\nSesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    st.markdown(f"[👉 **Amankan Jadwal Anda**](https://wa.me/628999771486?text={urllib.parse.quote('Halo Coach Ahmad, saya siap kalibrasi.')})")
    st.caption("© 2026 Neuro Nada Academy")
 
# --- INTERFACE UTAMA ---
cur_planet, cur_instr, cur_color = get_planetary_hour()
st.markdown(f"""
<div style='text-align: right;'>
    <div class='live-badge' style='background: {cur_color};'>🕒 LIVE PLANET: {cur_planet.upper()}</div>
    <div style='font-size: 11px; color: #888; margin-top: 5px;'>{cur_instr}</div>
</div>""", unsafe_allow_html=True)
 
st.markdown("<h1 style='text-align: center; margin-top: 10px; font-weight: 900; color:#FFD700;'>🌌 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #ccc; margin-bottom:0;'>Meretas Realita Melalui Kode Sandi Alam Bawah Sadar</p>", unsafe_allow_html=True)
st.markdown("---")
 
tgl_today = datetime.date.today()
tab1, tab2, tab5, tab3, tab4 = st.tabs(["👤 Personal Identity", "👩‍❤️‍👨 Couple Matrix", "⏱️ Quantum Engine", "🌌 Falak Ruhani", "📚 FAQ"])
 
# ==========================================
# TAB 1: IDENTITAS KOSMIK
# ==========================================
with tab1:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("Akses Blueprint Bawah Sadar Anda")
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
 
    if st.button("Kalkulasi Blueprint (Mulai)"):
        if not nama_user or len(nama_user.strip()) < 3: 
            st.error("🚨 Mohon ketik nama lengkap Anda (minimal 3 huruf).")
        else:
            try:
                st.snow()
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
                
                st.markdown(f"<h3 style='text-align:center;'>🌌 Blueprint Kosmik: {safe_name}</h3>", unsafe_allow_html=True)
                
                st.markdown(f"""
<div class="matrix-container">
<div class="matrix-item"><div class="matrix-label">Nilai Esoterik</div><div class="matrix-value matrix-value-special">{nilai_jummal}</div></div>
<div class="matrix-item"><div class="matrix-label">Elemen Dasar</div><div class="matrix-value">{el_nama.split(' ')[1] if len(el_nama.split(' '))>1 else el_nama}</div></div>
<div class="matrix-item"><div class="matrix-label">Meta-Program</div><div class="matrix-value matrix-value-special">KODE {angka_hasil}</div></div>
<div class="matrix-item"><div class="matrix-label">Filter Zodiak</div><div class="matrix-value">{zod}</div></div>
<div class="matrix-item"><div class="matrix-label">Energi Weton</div><div class="matrix-value">{wet} ({nep})</div></div>
</div>
""", unsafe_allow_html=True)
                
                st.markdown(f"""
<div class="dynamic-reading-box">
<h4 style="color: #FFD700; margin-top:0;">🔍 Bedah DNA Angka & Waktu Lahir</h4>
<p><b>1. Sandi Esoterik Nama (Hisab Jummal)</b><br>
<code style="color:#25D366; background:transparent; padding:0;">{rincian_jummal} = <b>{nilai_jummal}</b></code></p>
<ul style="margin-left: -15px; margin-bottom: 20px;">
<li><b>Elemen Bawah Sadar:</b> {el_nama} - <i style="color:#aaa;">{el_desc}</i></li>
<li><b>Inti Jiwa (Root Number):</b> {p_reduk} = {s_reduk} ➡ <b>{r_num}</b> ({r_desc})</li>
</ul>
<p><b>2. Sandi Waktu Lahir (Meta-Program NLP)</b><br>
<code style="color:#FFD700; background:transparent; padding:0;">{rincian_tgl}</code><br>
<span style="font-size:14px; color:#ccc;">Maka didapatkan <b>KODE {angka_hasil}</b>. Angka ini adalah <i>Blueprint</i> otak <b>{safe_name}</b> memproses informasi.</span></p>
{m_note}
</div>
""", unsafe_allow_html=True)

                st.markdown(f"""
<div class="primbon-box">
<div style="text-align:center; border-bottom:1px solid #D4AF37; padding-bottom:10px; margin-bottom:15px;">
<span style="color:#D4AF37; font-size:14px; font-weight:900; letter-spacing:2px;">📜 PETHIKAN KITAB BETALJEMUR ADAMMAKNA</span>
</div>
<div style="font-size:15px; line-height:1.6; margin-bottom: 15px;">
<b style="color:#FFF; font-size:18px;">{n_laku}</b> — <i style="color:#ccc;">"{d_laku}"</i>
</div>
<div style="font-size:15px; line-height:1.6; margin-bottom: 15px; border-top: 1px dashed #555; padding-top: 10px;">
• <b>Rezeki (<span style="color:#FFD700;">{rezeki_data[0]}</span>):</b> <i style="color:#ccc;">{rezeki_data[1]}</i><br>
• <b>Usaha (<span style="color:#25D366;">{usaha_data[0]}</span>):</b> <i style="color:#ccc;">{usaha_data[1]}</i>
</div>
<div style="font-size:15px; line-height:1.6; background: rgba(212,175,55,0.1); padding: 10px; border-radius: 8px;">
<span style="color:#FFD700;">🧭 <b>NAGA DINA (Arah Kejayaan Hari {hari_input}):</b></span> <b style="font-size: 16px;">{arah_naga}</b><br>
<i style="color:#888; font-size:13px;">*ACTIONABLE: Posisikan diri Anda menghadap <b>{arah_naga}</b> saat mengambil keputusan penting hari ini.</i>
</div>
</div>
""", unsafe_allow_html=True)
                
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
                
                st.info("💡 Lanjutkan ke Tab **🌌 Falak Ruhani** untuk mendapatkan resep terapi dan afirmasi spesifik Anda.")
                
            except Exception as e:
                st.error(f"Sistem gagal melakukan komputasi: {e}")
 
# ==========================================
# TAB 2: COUPLE MATRIX
# ==========================================
with tab2:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("Penyatuan Esoterik & Betaljemur (Couple Matrix)")
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
        
    if st.button("Analisis Resonansi Pasangan"):
        if str(n1).strip() and str(n2).strip():
            try:
                st.snow()
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
                st.markdown(f"""
<div class="matrix-container">
<div class="matrix-item"><div class="matrix-label">Neptu {safe_n1}</div><div class="matrix-value">{hc1} {pc1} ({nep_1})</div></div>
<div class="matrix-item"><div class="matrix-label">Neptu {safe_n2}</div><div class="matrix-value">{hc2} {pc2} ({nep_2})</div></div>
<div class="matrix-item" style="background: rgba(212,175,55,0.2);"><div class="matrix-label" style="color:#FFD700;">TOTAL NEPTU</div><div class="matrix-value matrix-value-special">{nep_1 + nep_2}</div></div>
<div class="matrix-item"><div class="matrix-label">Total Esoterik</div><div class="matrix-value">{total_couple}</div></div>
</div>
""", unsafe_allow_html=True)
                st.markdown(proc_penjelasan_matriks(safe_n1, safe_n2, total_couple, (nep_1+nep_2)), unsafe_allow_html=True)
                st.markdown(f'<div class="dynamic-reading-box" style="border-left-color: #25D366;"><h4 style="color: #25D366; margin-top:0;">🧬 Persona Pasangan: {c_title}</h4><p><i>{c_desc}</i></p></div>', unsafe_allow_html=True)
                st.info(f"**Titik Benturan Weton ({judul_jodoh}):**\n{desk_jodoh}")
                
                if sel in [0, 3, 6, 9]: st.success(f"💘 **SKOR META-PROGRAM (NLP): Sangat Sinkron**")
                elif sel in [1, 2, 8]: st.warning(f"⚖️ **SKOR META-PROGRAM (NLP): Dinamis** - Butuh toleransi.")
                else: st.error(f"🔥 **SKOR META-PROGRAM (NLP): Rawan Gesekan**")
     
                c_do_c, c_dont_c = st.columns(2)
                with c_do_c: st.markdown(f"<div style='background:rgba(37,211,102,0.1); padding:20px; border-radius:10px; border:1px solid #25D366;'>✅ <b>LAKUKAN INI:</b><br><br>{d_do}</div>", unsafe_allow_html=True)
                with c_dont_c: st.markdown(f"<div style='background:rgba(255,75,75,0.1); padding:20px; border-radius:10px; border:1px solid #ff4b4b;'>❌ <b>HINDARI INI:</b><br><br>{d_dont}</div>", unsafe_allow_html=True)
            except Exception as e: st.error(f"Error komputasi: {e}")

# ==========================================
# TAB 5: QUANTUM ENGINE
# ==========================================
with tab5:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("⏱️ Live Cosmic Dashboard (Fate Hacking)")
    qe_nama = st.text_input("Nama Panggilan:", key="qe_n")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Hack My Reality Now"):
        if qe_nama:
            st.snow()
            safe_qe = get_safe_firstname(qe_nama)
            jummal_qe = hitung_nama_esoterik(qe_nama)
            mod_harian = (jummal_qe + sum(int(d) for d in tgl_today.strftime("%d%m%Y"))) % 7
            
            fase_harian = {
                0: ("🔴 Rest & Reset", f"Energi di titik nadir. Lakukan hal repetitif saja."),
                1: ("🟢 Inisiasi", f"Momentum awal. Saatnya eksekusi proyek baru!"),
                2: ("🔵 Kolaborasi", f"Cari rekan, negosiasi, atau minta bantuan. Pintu peluang lewat orang lain."),
                3: ("🟡 Ekspresi", f"Aura komunikasi terang. Update sosmed, bikin presentasi."),
                4: ("🟤 Pondasi", f"Fokus struktur. Rapikan meja, bereskan file admin/keuangan."),
                5: ("🟠 Ekspansi & Risiko", f"Waktu tepat mencoba rute baru/ambil risiko terkalkulasi."),
                6: ("🟣 Pengayoman", f"Energi perlindungan tinggi. Selesaikan konflik dengan orang terdekat.")
            }
            siklus_hari_ini, saran_siklus = fase_harian.get(mod_harian, fase_harian[0])
            sun_fase, sun_desc = get_sun_phase()
            planet_live, planet_desc, planet_color = get_planetary_hour()
            
            st.markdown(f"### 📡 Live Dashboard: {safe_qe}")
            st.markdown(f"""
<div class="matrix-container">
<div class="matrix-item"><div class="matrix-label">Fase Harian</div><div class="matrix-value">{siklus_hari_ini.split(' ')[1]}</div></div>
<div class="matrix-item"><div class="matrix-label">Matahari</div><div class="matrix-value matrix-value-special">{sun_fase.split(' ')[0]}</div></div>
<div class="matrix-item" style="border-bottom: 2px solid {planet_color};"><div class="matrix-label">Jam Planet</div><div class="matrix-value" style="color:{planet_color};">{planet_live}</div></div>
</div>
""", unsafe_allow_html=True)
            st.markdown(f'<div class="live-engine-box"><h4 style="color: #00FFFF; margin-top:0;">⚡ TACTICAL ACTION PLAN</h4><p style="color: #ccc;">Fase Bioritme Anda: <b>{siklus_hari_ini}</b>. <i>Saran: {saran_siklus}</i><br><br><b>🎯 KESIMPULAN:</b> Manfaatkan energi {planet_live.split(" ")[0]} ini untuk mengeksekusi misi fase {siklus_hari_ini.split(" ")[1]} Anda. Jangan ditunda!</p></div>', unsafe_allow_html=True)

# ==========================================
# TAB 3: FALAK RUHANI (PROTOKOL TERAPI)
# ==========================================
with tab3:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.subheader("🌌 Terapi Falak Ruhani & Hypno-NLP")
    st.info("**Reset Ulang Saraf Anda**\n\nSistem mengonversi nama Anda menjadi angka getaran, lalu mencocokkannya dengan frekuensi Asmaul Husna dan Afirmasi Bawah Sadar untuk menghancurkan *Mental Block*.")
    nama_ruhani = st.text_input("Masukkan Nama Lengkap Anda:", placeholder="Ketik nama asli...", key="input_ruhani")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Aktivasi Anchor Spiritual"):
        if nama_ruhani and len(nama_ruhani.strip()) >= 3:
            st.snow()
            safe_nr = get_safe_firstname(nama_ruhani)
            nilai_jummal_r = hitung_nama_esoterik(nama_ruhani)
            
            r_num_r = nilai_jummal_r
            while r_num_r > 9: r_num_r = sum(int(d) for d in str(r_num_r))
            
            asma_terapi, vibrasi_asma, tujuan_ruhani, jumlah_dzikir = proc_falak_ruhani(nilai_jummal_r, r_num_r, safe_nr)
            protokol_nlp = get_protokol_terapi(r_num_r, safe_nr)
            
            st.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(10, 20, 40, 0.9) 0%, rgba(20, 10, 40, 0.9) 100%); border-left: 5px solid #00FFFF; padding: 25px; border-radius: 12px; margin-top: 20px; box-shadow: 0 8px 25px rgba(0, 255, 255, 0.15);">
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
        <span style="color:#aaa; font-size:14px;">Ucapkan kalimat ini di dalam hati dengan penuh keyakinan menjelang tidur (Gelombang Theta):</span><br>
        <i style="color:#fff; font-size:16px; line-height:1.6;">"{protokol_nlp['afirmasi']}"</i>
    </div>

    <div style="border-top: 1px dashed #555; padding-top: 15px;">
        <b style="color:#25D366; font-size:16px;">🏃‍♂️ 3. QUANTUM HABIT (Tindakan Fisik Hari Ini)</b><br>
        <span style="color:#ccc; font-size:15px; line-height:1.6;">Semesta merespons tindakan nyata. Untuk menghancurkan Mental Block Anda, eksekusi tugas ini hari ini:<br>
        <b style="color:#FFF;">{protokol_nlp['habit']}</b></span>
    </div>
</div>
""", unsafe_allow_html=True)
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
