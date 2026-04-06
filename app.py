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
    page_icon="🧠", 
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- CUSTOM CSS (WARNA KUNING UNTUK TOMBOL) ---
st.markdown(
    """<style>
    div.stButton > button {
        background-color: #FFD700 !important; color: #000000 !important;
        font-weight: bold !important; border: none !important;
        padding: 12px 24px !important; border-radius: 8px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.02); background-color: #FFC107 !important; }
    .ulasan-box {
        background-color: #1e1e1e; padding: 15px; border-radius: 8px;
        border-left: 4px solid #FFD700; margin-bottom: 10px;
    }
    </style>""", unsafe_allow_html=True
)

# --- FUNGSI NYAWA: TYPEWRITER EFFECT ---
def type_effect(text, speed=0.01):
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(full_text)
        time.sleep(speed)

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa yang Luar Biasa"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

# ==========================================
# DATABASE CLOUD: GOOGLE SHEETS (REAL-TIME)
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
    except:
        return []

def kirim_ulasan(nama, rating, komentar):
    try:
        data = urllib.parse.urlencode({"nama": nama, "rating": rating, "komentar": komentar}).encode("utf-8")
        req = urllib.request.Request(URL_POST, data=data)
        urllib.request.urlopen(req)
        return True
    except:
        return False

# --- SIDEBAR PROMOSI & VIDEO ---
with st.sidebar:
    if os.path.exists("baru.jpg.png"):
        try: st.image("baru.jpg.png", use_container_width=True); st.markdown("<br>", unsafe_allow_html=True)
        except: pass
    elif os.path.exists("baru.jpg"): st.image("baru.jpg", use_container_width=True)

    st.markdown(f"### {get_greeting()}")
    st.markdown("### 🎬 Hypno-Video Vault")
    st.caption("Fokuskan pandangan Anda pada video ini sambil menggunakan headphone untuk relaksasi maksimal.")
    st.video("https://youtu.be/kkRcH6aH_lI?si=bpUZF3CWl8DKLw5m")
        
    st.markdown("---")
    st.markdown("## 🧠 Sesi Transformasi")
    st.info("**Reset Pola Pikir Anda**\n\nSering merasa terhambat oleh pikiran sendiri? Mari kita lakukan kalibrasi ulang dalam sesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    
    phone_number_sidebar = "628999771486"
    wa_text_sidebar = "Halo Coach Ahmad, saya tertarik untuk mengamankan jadwal Private Session Hypno-NLP. Apakah masih ada kuota?"
    st.markdown(f"[👉 **Amankan Jadwal Anda**](https://wa.me/{phone_number_sidebar}?text={urllib.parse.quote(wa_text_sidebar)})")
    
    st.markdown("---")
    st.success("**📚 Seni Persuasi NLP**\n\nPelajari bagaimana bahasa bekerja di tingkat bawah sadar untuk meningkatkan pengaruh Anda.")
    st.markdown("[👉 **Akses Modul Lengkap**](https://lynk.id/neuronada/ebook-nlp)")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

# --- INTERFACE UTAMA & BANNER ---
if os.path.exists("banner.jpg"):
    try: st.image("banner.jpg", use_container_width=True)
    except: pass

st.markdown("<h1 style='text-align: center; margin-top: 10px;'>🧠 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #D4AF37;'>Sistem Pemetaan Bawah Sadar & Akselerasi Potensi Diri</p>", unsafe_allow_html=True)
st.markdown("---")

# --- DATA DICTIONARY (UPGRADED: MENDALAM & DINAMIS) ---
vibrasi_nama_dict = {
    1: "Nama Anda memancarkan getaran **KEMANDIRIAN & KEPEMIMPINAN**. Orang sering melihat Anda sebagai sosok alfa yang tangguh dan selalu tahu arah. Namun, di sudut batin terdalam, Anda sebenarnya rindu memiliki satu tempat bersandar dimana Anda tidak perlu berpura-pura kuat.",
    2: "Nama Anda memancarkan getaran **DIPLOMASI & KEDAMAIAN**. Anda bagaikan oase; orang merasa sangat nyaman menumpahkan keluh-kesah pada Anda. Tantangan terbesar Anda adalah: Anda sering menyerap 'sampah emosi' orang lain dan lupa membersihkan emosi Anda sendiri.",
    3: "Nama Anda memancarkan getaran **EKSPRESI & KECERIAAN**. Anda memiliki daya tarik magnetis yang membuat suasana sekaku apapun menjadi cair. Di balik tawa dan keramahan itu, pikiran Anda sebenarnya sangat analitis dan tak henti-hentinya memutar berbagai skenario kehidupan.",
    4: "Nama Anda memancarkan getaran **STRUKTUR & KEDISIPLINAN**. Orang mempercayai Anda karena Anda terlihat kokoh ibarat batu karang. Sisi yang jarang orang tahu: Anda menyimpan kerapuhan saat rencana besar Anda mendadak berantakan oleh hal di luar kendali.",
    5: "Nama Anda memancarkan getaran **KEBEBASAN & DINAMIKA**. Aura Anda penuh kejutan, petualangan, dan sangat sulit ditebak. Sisi gelapnya: ketakutan tersembunyi akan komitmen panjang membuat Anda terkadang merasa kehilangan 'jangkar' yang pasti dalam hidup.",
    6: "Nama Anda memancarkan getaran **TANGGUNG JAWAB & KASIH SAYANG**. Anda adalah pelindung natural. Seringkali Anda mengalah hanya agar orang di sekitar Anda bahagia. Hati-hati, cinta yang berlebihan tanpa batasan (*boundary*) akan menguras habis energi hidup Anda.",
    7: "Nama Anda memancarkan getaran **KEDALAMAN & MISTERI**. Orang melihat Anda sebagai sosok yang cerdas dan sulit ditembus. Faktanya, Anda memang sangat selektif. Anda lebih memilih punya 2 sahabat yang sefrekuensi daripada 100 teman yang obrolannya hanya sebatas kulit luar.",
    8: "Nama Anda memancarkan getaran **OTORITAS & KELIMPAHAN**. Aura Anda beresonansi kuat dengan kesuksesan material. Anda memiliki ketahanan mental layaknya baja. Satu hal yang Anda sembunyikan: rasa kesepian luar biasa ketika berada di puncak pencapaian.",
    9: "Nama Anda memancarkan getaran **IDEALISME & KEMANUSIAAN**. Anda memiliki visi kehidupan yang melampaui ego pribadi. Anda seringkali dikecewakan oleh manusia lain, bukan karena Anda lemah, melainkan karena Anda selalu memberikan standar ketulusan yang terlalu tinggi."
}

data_analisa = {
    1: {"karakter": "Anda pada dasarnya adalah sosok perintis. Seringkali Anda merasa gatal kalau harus menunggu orang lain bergerak lebih dulu. Di luar, Anda mungkin terlihat tangguh dan mandiri, tapi di dalam hati, Anda terkadang merasa lelah memikul semuanya sendirian. Pikiran Anda selalu fokus pada tujuan masa depan.", "asmara": "Anda butuh pasangan yang tidak mengekang tapi tetap bisa mengimbangi langkah cepat Anda. Terkadang tanpa sadar bahasa Anda terdengar seperti 'memerintah' karena Anda ingin semuanya efisien. Cobalah sesekali menurunkan ego dan sekadar mendengarkan."},
    2: {"karakter": "Anda punya bakat alami sebagai 'penyerap energi' orang di sekitar Anda. Anda sangat peka terhadap perubahan suasana hati seseorang meski mereka diam. Kehebatan Anda adalah membuat orang merasa nyaman, namun kelemahan Anda adalah sering mengorbankan perasaan sendiri demi menjaga perasaan orang lain.", "asmara": "Asmara bagi Anda adalah tentang rasa aman secara emosional. Berhentilah menjadi 'Penyelamat' untuk pasangan Anda. Anda berhak menuntut kebahagiaan yang sama rata, bukan sekadar memberi."},
    3: {"karakter": "Pikiran Anda sangat kaya akan imajinasi dan skenario. Anda sering memikirkan banyak ide brilian sekaligus, meski kadang kesulitan menyelesaikannya satu per satu. Anda pandai mencairkan suasana, tapi saat sedang sendirian, Anda sering memutar ulang percakapan masa lalu di kepala Anda.", "asmara": "Anda butuh koneksi yang menyenangkan dan tidak membosankan. Kebisuan adalah hal yang paling menyiksa Anda. Cari pasangan yang bisa menjadi tempat Anda bercerita tanpa dihakimi."},
    4: {"karakter": "Anda adalah perencana yang detail. Anda benci ketidakpastian dan kejutan yang tidak direncanakan. Pikiran Anda bekerja seperti laci-laci yang rapi. Orang mungkin melihat Anda kaku, padahal itu adalah cara bawah sadar Anda untuk memastikan semuanya aman dan terkendali.", "asmara": "Anda sangat setia pada komitmen, namun terkadang lupa untuk memberikan 'bumbu' romantis karena terlalu fokus pada hal logis dan praktis. Ingat, asmara itu urusan hati, bukan sekadar hitung-hitungan logika."},
    5: {"karakter": "Anda benci rutinitas yang monoton. Jiwa Anda butuh ruang gerak yang luas. Anda hebat dalam mencari celah di saat orang lain buntu. Namun di sisi lain, karena terlalu sering berpindah fokus, Anda kadang kehilangan arah dan bingung sebenarnya apa yang paling Anda cari dalam hidup ini.", "asmara": "Kata kunci untuk Anda adalah 'Kebebasan'. Hubungan yang terlalu menuntut akan membuat Anda diam-diam ingin melarikan diri. Anda butuh pasangan yang terasa seperti sahabat petualang."},
    6: {"karakter": "Pusat dari hidup Anda adalah keluarga dan orang-orang yang Anda sayangi. Anda seringkali menempatkan kebutuhan orang lain di atas kebutuhan Anda sendiri. Anda punya standar tanggung jawab yang sangat tinggi, yang terkadang membuat Anda gampang kecewa kalau orang lain tidak melakukan hal yang sama.", "asmara": "Anda sangat peduli, namun terkadang kepedulian Anda terasa seperti sedang 'mengatur'. Belajarlah untuk berhenti menebak-nebak apa yang dipikirkan pasangan. Tanyakan saja langsung padanya."},
    7: {"karakter": "Anda punya intuisi yang sangat tajam; seringkali firasat Anda terbukti benar. Anda bukan tipe orang yang mudah percaya begitu saja pada omongan orang (skeptis). Anda butuh banyak waktu sendirian ('Me Time') untuk menata ulang energi Anda setelah terlalu banyak interaksi sosial.", "asmara": "Anda cukup sulit ditebak dan susah terbuka 100% pada awalnya. Anda mencari pasangan yang obrolannya 'nyambung' sampai ke level yang dalam, bukan sekadar basa-basi cinta."},
    8: {"karakter": "Anda punya dorongan kuat untuk sukses dan memegang kendali. Anda tidak suka diremehkan. Di balik sikap Anda yang terlihat tegas dan logis, sebenarnya ada keinginan kuat untuk diakui dan dihargai atas pencapaian Anda. Anda tahan banting terhadap tekanan mental.", "asmara": "Jangan bawa kebiasaan 'negosiasi keras' Anda dari tempat kerja ke dalam hubungan rumah tangga. Pasangan Anda butuh disentuh hatinya dengan kelembutan, bukan ditundukkan dengan logika."},
    9: {"karakter": "Anda sering merasa menjadi 'jiwa tua' (old soul). Anda peduli pada hal-hal kemanusiaan dan punya standar moral yang tinggi. Anda memandang masalah dari sudut pandang yang sangat luas. Masalahnya, Anda sering merasa kecewa melihat realita dunia yang tidak seindah ekspektasi Anda.", "asmara": "Anda mencari cinta yang ideal, sebuah koneksi jiwa yang murni. Namun ingatlah bahwa manusia tempatnya salah. Menerima ketidaksempurnaan pasangan adalah kunci kedamaian Anda."}
}

tips_zodiak_nlp = {
    "Aries": "**Teknik Pacing (Penyelarasan):** Jangan langsung membantah ego-nya. Dengarkan dan validasi dulu emosinya, baru perlahan 'Lead' (arahkan) pikiran mereka ke logika Anda.",
    "Taurus": "**Teknik Reframing (Pembingkaian Ulang):** Mereka bukan keras kepala, tapi teguh. Jangan paksa mereka berubah cepat; berikan data logis, lalu biarkan mereka merasa itu adalah keputusannya sendiri.",
    "Gemini": "**Teknik Modality Matching:** Ikuti ritme pikiran mereka yang cepat. Jika mereka pakai kata-kata visual ('Coba *lihat* ini'), balas dengan visual ('Iya, *kelihatan* bagus').",
    "Cancer": "**Avoid Negative Anchors:** Mereka mengingat emosi masa lalu dengan sangat kuat. Berhati-hatilah dengan nada suara; bagi mereka *cara* Anda bicara lebih penting dari *isi* pembicaraan.",
    "Leo": "**Teknik Appreciation:** Validasi adalah bahan bakar mereka. Sentuh egonya dengan pujian yang tulus sebelum Anda memberikan kritik atau masukan.",
    "Virgo": "**Teknik Chunking Up:** Saat mereka terlalu rewel soal hal-hal kecil dan detail, tarik perhatian mereka untuk melihat 'Gambaran Besar' (Big Picture) dari masalah tersebut.",
    "Libra": "**Strengthen Internal Reference:** Bantu mereka mengambil keputusan dengan menanyakan apa yang benar-benar *mereka* inginkan, bukan apa yang terbaik untuk orang lain.",
    "Scorpio": "**Deep Rapport:** Jangan pernah menyembunyikan kebohongan kecil. Bangun kepercayaan di level terdalam; sekali mereka percaya, mereka akan loyal seumur hidup.",
    "Sagittarius": "**Future Pacing:** Hubungkan setiap masalah saat ini dengan visi masa depan yang lebih baik. Mereka akan termotivasi jika melihat ujung jalan yang menjanjikan kebebasan.",
    "Capricorn": "**Logic Bridge:** Mulailah semua pembicaraan dari sudut pandang rasional dan fungsional. Setelah logika mereka menerima, baru perlahan masuk ke ranah emosional.",
    "Aquarius": "**Pattern Interrupt:** Saat mereka terlalu asyik dengan dunianya sendiri, berikan kejutan ide yang anti-mainstream untuk merangsang kembali minat intelektual mereka.",
    "Pisces": "**Grounding:** Saat mereka mulai terlalu emosional atau berimajinasi ke arah negatif, tarik pelan-pelan pikiran mereka kembali ke fakta realita saat ini."
}

closing_brutal_dinamis = {
    1: ["Sering overthinking karena merasa hasil kerja 'belum sempurna'", "Memendam lelah sendirian karena gengsi minta tolong orang lain", "Membangun tembok pertahanan ego agar tidak terlihat lemah atau gagal"],
    2: ["Terjebak memuaskan ekspektasi orang lain sampai lupa membahagiakan diri sendiri", "Sulit berkata 'TIDAK' dan memendam amarah yang berujung psikosomatis (sakit fisik)", "Terus mengalah hanya agar tidak terjadi keributan yang dibenci bawah sadarnya"],
    3: ["Menyembunyikan rasa cemas dan gelisah yang intens di balik topeng senyuman", "Sangat gampang kehilangan motivasi jika rutinitas mulai terasa membosankan", "Pikiran yang terlalu penuh sering menyebabkan insomnia dan over-analisa di malam hari"],
    4: ["Sangat rentan stres dan uring-uringan kalau rencana mendadak berubah di luar kendali", "Terjebak di rutinitas yang kaku karena *Amigdala* di otak takut mengambil resiko baru", "Sering dianggap kurang peka perasaannya oleh pasangan karena terlalu mengedepankan logika"],
    5: ["Sindrom 'Cepat Bosan' yang membuat banyak potensi besar berhenti di tengah jalan", "Kelelahan saraf simpatik karena otak tidak pernah benar-benar diizinkan untuk diam", "Terkadang merasa hampa karena kehilangan pijakan hidup akibat terlalu sering 'berlari'"],
    6: ["Kehabisan energi secara drastis (Burnout) karena terlalu sibuk menyelamatkan hidup orang lain", "Cenderung Over-Protective yang diam-diam mematikan ruang gerak pasangan/keluarga", "Merasa bersalah luar biasa saat memakai waktu atau uang murni untuk kesenangan pribadi"],
    7: ["Terjebak dalam labirin analisa pikiran sendiri (Paralysis by Analysis) tanpa eksekusi nyata", "Sering merasa terasing dan merasa tidak ada yang benar-benar memahami kedalaman pikirannya", "Mencurigai niat baik orang lain akibat luka masa lalu yang menjadi *Anchor* negatif"],
    8: ["Sering merasa hampa secara batin justru di saat target finansial atau tahta sudah tercapai", "Sangat sulit melepaskan kendali dan memaafkan kesalahan kecil (terutama pengkhianatan)", "Terus memaksa mesin tubuh bekerja, mengabaikan alarm alamiah demi sebuah ambisi"],
    9: ["Terlalu sering memaklumi orang yang manipulatif dan toxic dengan alasan 'kasihan'", "Sering patah hati karena memproyeksikan ekspektasi kesempurnaan moral pada manusia biasa", "Kelelahan batin karena merasa menanggung beban emosional semesta yang bukan tanggung jawabnya"]
}

potensi_dinamis = {
    1: "memiliki potensi daya dobrak pencapaian yang fenomenal jika sumbatan egonya dilepas.",
    2: "memiliki karunia negosiasi dan resonansi penyembuhan yang luar biasa jika filter *'Gak Enakan'* dicabut.",
    3: "menyimpan daya persuasi dan jenius kreatif yang sangat langka jika loncatan fokusnya dikalibrasi.",
    4: "mampu membangun kerajaan/mahakarya yang solid jika filter perfeksionisme-kaku di pikirannya diubah jadi fleksibel.",
    5: "adalah inovator sejati yang tak terhentikan jika energinya dipusatkan pada satu 'jangkar' yang tepat.",
    6: "mampu menjadi magnet kelimpahan keluarga yang luar biasa jika ia belajar mencintai dirinya sendiri terlebih dahulu.",
    7: "menyimpan intuisi dan kebijaksanaan level tinggi yang siap meledak jika *overthinking*-nya direm.",
    8: "adalah penakluk sejati yang akan memegang dunia di tangannya jika ia berhasil berdamai dengan sisi rapuh emosinya.",
    9: "adalah pembawa cahaya yang luar biasa, jika ia berhenti berharap dunia ini sempurna dan mulai mengeksekusi visi nyatanya."
}

link_produk = {
    1: "http://lynk.id/neuronada/kj98l4zgzwdw/checkout", 2: "http://lynk.id/neuronada/6z23q03121lg/checkout",
    3: "http://lynk.id/neuronada/0rd6gr7nlzxp/checkout", 4: "http://lynk.id/neuronada/elp83loeyggg/checkout",
    5: "http://lynk.id/neuronada/wne9p4q1l3d9/checkout", 6: "http://lynk.id/neuronada/nm840y6nlo21/checkout",
    7: "http://lynk.id/neuronada/vv0797ll7g7o/checkout", 8: "http://lynk.id/neuronada/ropl1lm6rz8g/checkout",
    9: "http://lynk.id/neuronada/704ke23nzmgx/checkout"
}

# --- FUNGSI-FUNGSI LOGIKA MATEMATIKA ---
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
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][tanggal.weekday()]
    pasaran = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"][selisih_hari % 5]
    n_hari = {"Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9}
    n_pas = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
    return n_hari[hari] + n_pas[pasaran], f"{hari} {pasaran}"

def get_zodiak(tanggal):
    d, m = tanggal.day, tanggal.month
    if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "Aries", "Akselerasi & Keberanian"
    elif (m == 4 and d >= 20) or (m == 5 and d <= 20): return "Taurus", "Kestabilan & Resiliensi"
    elif (m == 5 and d >= 21) or (m == 6 and d <= 20): return "Gemini", "Agility (Ketangkasan Pikiran)"
    elif (m == 6 and d >= 21) or (m == 7 and d <= 22): return "Cancer", "Proteksi & Intuisi Batin"
    elif (m == 7 and d >= 23) or (m == 8 and d <= 22): return "Leo", "Kharisma & Ekspresi Alfa"
    elif (m == 8 and d >= 23) or (m == 9 and d <= 22): return "Virgo", "Presisi & Filter Analitis"
    elif (m == 9 and d >= 23) or (m == 10 and d <= 22): return "Libra", "Ekuilibrium & Harmoni"
    elif (m == 10 and d >= 23) or (m == 11 and d <= 21): return "Scorpio", "Intensitas & Radar Emosi"
    elif (m == 11 and d >= 22) or (m == 12 and d <= 21): return "Sagittarius", "Ekspansi & Visioner"
    elif (m == 12 and d >= 22) or (m == 1 and d <= 19): return "Capricorn", "Sistem & Struktur Kuat"
    elif (m == 1 and d >= 20) or (m == 2 and d <= 18): return "Aquarius", "Inovasi & Anti-Mainstream"
    else: return "Pisces", "Empati & Visualisasi Kuantum"

def bioritme_nlp(tanggal_lahir):
    hari_hidup = (datetime.date.today() - tanggal_lahir).days
    fisik = math.sin(2 * math.pi * (hari_hidup / 23)) * 100
    emosi = math.sin(2 * math.pi * (hari_hidup / 28)) * 100
    intelektual = math.sin(2 * math.pi * (hari_hidup / 33)) * 100
    
    if emosi > 50 and intelektual > 50: 
        state = "UPTIME STATE (Gelombang Puncak Kreativitas)"
        saran = "Sistem saraf Anda sedang sangat reseptif. Manfaatkan momentum hari ini untuk mengambil keputusan krusial, berjejaring (networking), atau menyelesaikan tugas berat yang tertunda."
    elif emosi < -50 and fisik < -50: 
        state = "DOWNTIME STATE (Siklus Rest & Kalibrasi)"
        saran = "Baterai alamiah Anda sedang low-bat. Izinkan pikiran Anda beristirahat. Hindari konflik atau adu argumen hari ini karena *Amigdala* Anda sangat mudah terpicu."
    elif intelektual > 50 and fisik < 0: 
        state = "ANALYTICAL STATE (Tajam untuk Perencanaan)"
        saran = "Fisik Anda mungkin terasa malas bergerak, tapi ketajaman otak kiri Anda luar biasa hari ini. Pakai energi ini untuk menyusun strategi, riset data, atau evaluasi."
    else: 
        state = "NEUTRAL STATE (Ekuilibrium Stabil)"
        saran = "Gelombang otak Anda berjalan konstan dan seimbang. Sangat pas untuk menjalankan rutinitas eksekusi dengan tenang tanpa *mood-swing*."
        
    return int(fisik), int(emosi), int(intelektual), state, saran

def get_arketipe(angka):
    arketipe_dict = {
        1: "The Leader (Sang Perintis)", 2: "The Mediator (Sang Penyelaras)",
        3: "The Communicator (Sang Visioner)", 4: "The Architect (Sang Transformator)",
        5: "The Explorer (Sang Penggerak)", 6: "The Nurturer (Sang Harmonizer)",
        7: "The Analyst (Sang Legacy Builder)", 8: "The Strategist (Sang Sovereign)",
        9: "The Humanist (Sang Kesadaran Tinggi)"
    }
    return arketipe_dict.get(angka, "Pribadi Unik")

# --- MENU TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Personal Mapping", "👩‍❤️‍👨 Couple Sync", "🕸️ Audit Pikiran"])

# ==========================================
# TAB 1: PERSONAL MAPPING
# ==========================================
with tab1:
    st.subheader("Bongkar Pola Bawah Sadar Anda")
    nama_user = st.text_input("Nama Lengkap Anda:", placeholder="Masukkan nama panggilan Anda...", key="nama_user_t1")
    tgl_today = datetime.date.today()
    tgl_input = st.date_input("Data Input (Tanggal Lahir):", value=datetime.date(1995, 1, 1), min_value=datetime.date(1920, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")

    if st.button("Mulai Pemetaan Internal"):
        if not nama_user or len(nama_user.strip()) < 3:
            st.error("🚨 Satpam NLP: Mohon masukkan nama dengan benar (minimal 3 huruf) agar vibrasi identitas bisa terbaca akurat.")
        elif tgl_input == tgl_today:
            st.error("🚨 Satpam NLP: Mohon masukkan tanggal lahir Anda yang valid, bukan hari ini.")
        else:
            with st.spinner('Menyelaraskan gelombang otak dan membedah program bawah sadar...'):
                time.sleep(2)
                
                angka_hasil = hitung_angka(tgl_input)
                angka_nama = hitung_angka_nama(nama_user)
                _, weton_hasil = get_neptu_weton(tgl_input)
                zod_nama, zod_sifat = get_zodiak(tgl_input)
                f, e, i, state_harian, saran_harian = bioritme_nlp(tgl_input)
                
                insight = data_analisa.get(angka_hasil)
                arketipe = get_arketipe(angka_hasil)
                pain_points = closing_brutal_dinamis.get(angka_hasil)
                teks_potensi = potensi_dinamis.get(angka_hasil)
            
            st.balloons()
            st.markdown(f"### 🪞 Blueprint Bawah Sadar: {nama_user}")
            st.markdown("---")
            
            st.success(f"🔋 **RADAR ENERGI HARI INI:** Anda berada dalam **{state_harian}**.")
            st.caption(f"Fisik: {f}% | Emosional: {e}% | Intelektual: {i}%")
            st.write(f"💡 **Saran NLP:** {saran_harian}")
            st.markdown("---")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("KODE NAMA", angka_nama)
            c2.metric("KODE PROGRAM", angka_hasil)
            c3.metric("ENERGI WETON", weton_hasil)
            c4.metric("POLA ZODIAK", zod_nama)
            
            st.markdown("---")
            st.subheader("🗣️ Vibrasi Identitas (Duality Level)")
            st.info(vibrasi_nama_dict.get(angka_nama, "Nama Anda memiliki resonansi energi yang unik."))

            st.subheader("🧬 Struktur Karakter (Meta-Program)")
            sintesis = f"Halo **{nama_user}**, sistem mendeteksi filter utama pikiran Anda dipengaruhi gelombang **{zod_nama}** ({zod_sifat}) yang berakar kuat pada frekuensi **{weton_hasil}**. "
            sintesis += insight['karakter']
            st.write(sintesis)

            st.subheader("❤️ Kalibrasi Asmara")
            st.warning(f"**Blind Spot Hubungan:** {insight['asmara']}")
            st.info(f"💡 **Secret NLP Hack untuk Anda:** {tips_zodiak_nlp.get(zod_nama)}")

            st.markdown("---")
            st.markdown(f"""
            <div style="background-color: #3b0000; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
                <h4 style="color: #ff4b4b; margin-top: 0;">🚨 PERINGATAN BAWAH SADAR (Shadow Self)</h4>
                <p style="color: white; font-size: 15px;">Sistem mendeteksi adanya <b>Mental Block (Hambatan Tak Kasat Mata)</b> yang diam-diam menguras energi hidup Anda secara konstan. Jika Anda jujur pada diri sendiri, arketipe <b>{arketipe}</b> dalam diri Anda mungkin sedang mengalami sabotase ini:</p>
                <ul style="color: #ffcccc; font-size: 15px;">
                    <li>{pain_points[0]}</li>
                    <li>{pain_points[1]}</li>
                    <li>{pain_points[2]}</li>
                </ul>
                <p style="color: #FFD700; font-weight: bold; margin-bottom: 0;">Padahal, rancangan asli program Anda {teks_potensi}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            url_tujuan = link_produk.get(angka_hasil, "https://lynk.id/neuronada")
            nama_panggilan = nama_user.split()[0] if nama_user else 'Sahabat'
            
            st.write(f"Modul transformasi khusus **Kode {angka_hasil}** ini diciptakan khusus untuk mereset sumbatan mental di atas. Jangan biarkan *blind spot* Anda terus membatasi rezeki dan kebahagiaan Anda, {nama_panggilan}.")
            
            st.markdown(f"""
            <a href="{url_tujuan}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #FFD700; color: black; padding: 15px; text-align: center; border-radius: 8px; font-weight: bold; font-size: 16px; box-shadow: 0 4px 8px rgba(255, 215, 0, 0.2);">
                    🔓 BONGKAR KUNCI MENTAL KODE {angka_hasil} SEKARANG
                </div>
            </a>
            """, unsafe_allow_html=True)

            st.markdown("---")
            phone_number = "628999771486" 
            wa_text = f"Halo Coach Ahmad, saya {nama_user}. Saya merinding baca hasil mapping Kode {angka_hasil} ({arketipe}). Saya capek jadi korban 'Shadow Self' saya sendiri dan SIAP kalibrasi ulang. Kapan jadwal Private Session terdekat yang masih kosong?"
            encoded_wa = urllib.parse.quote(wa_text)
            wa_link = f"https://wa.me/{phone_number}?text={encoded_wa}"

            st.markdown(f"""
            <div style="text-align: center; padding: 25px; background-color: #1a1a1a; border: 2px solid #25D366; border-radius: 10px;">
                <h3 style="color: #25D366; margin-bottom: 10px;">🧠 Cabut Mental Block Hingga ke Akar</h3>
                <p style="color: #f0f0f0; margin-bottom: 20px;">Membaca saja tidak merubah Nasib. Mari lakukan <i>Deep Re-Programming</i> langsung bersama Coach Ahmad Septian di ruang terapi privat.</p>
                <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 16px;">
                        📲 Konsultasi Jadwal Private Session
                    </div>
                </a>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("❓ Pertanyaan Terkait Pemetaan")
            with st.expander("Bagaimana sistem ini membedah struktur pikiran saya?"):
                st.write("Sistem **Persona-NLP Analis** menggunakan integrasi data kronologis sebagai pintu masuk untuk mengidentifikasi **Meta-Program** atau filter dominan dalam pikiran bawah sadar Anda.")
            with st.expander("Kenapa akurasinya terasa sangat personal?"):
                st.write("Karena Coach **Ahmad Septian** menggabungkan tiga variabel fundamental: Kode Numerik, Energi Weton, dan Pola Zodiak menjadi satu profil psikografis yang utuh (Barnum Effect Precision).")
            with st.expander("Apa langkah selanjutnya setelah mengetahui 'Kode Program' ini?"):
                st.write("Langkah selanjutnya adalah **Re-Programming**. Anda bisa menggunakan modul transformasi PDF yang disediakan di atas atau mendaftar sesi Deep Calibration.")

            st.markdown("---")
            with st.expander("⚖️ Disclaimer & Batasan Layanan"):
                st.caption(f"**PEMBERITAHUAN PENTING:** Analisa Persona-NLP Analis ini dirancang murni untuk tujuan edukasi dan pengembangan diri. Segala keputusan yang diambil oleh **{nama_user}** adalah tanggung jawab pribadi sepenuhnya.\n\n© 2026 Neuro Nada - Ahmad Septian Dwi Cahyo.")

# ==========================================
# TAB 2: COUPLE SYNC 
# ==========================================
with tab2:
    st.subheader("Kalkulator Sinkronisasi Pasangan")
    st.write("Uji kecocokan *Meta-Program* Anda dan pasangan berdasarkan Vibrasi Nama & Weton Primbon Nusantara.")
    
    colA, colB = st.columns(2)
    with colA:
        nama_1 = st.text_input("Nama Anda:", key="c_nama1")
        tgl_1 = st.date_input("Tgl Lahir Anda:", value=datetime.date(1995, 1, 1), min_value=datetime.date(1920, 1, 1), key="c_tgl1")
    with colB:
        nama_2 = st.text_input("Nama Pasangan/Gebetan:", key="c_nama2")
        tgl_2 = st.date_input("Tgl Lahir Pasangan:", value=datetime.date(1995, 1, 1), min_value=datetime.date(1920, 1, 1), key="c_tgl2")
        
    if st.button("Cek Kompatibilitas Bawah Sadar"):
        tgl_today = datetime.date.today()
        if not nama_1 or len(nama_1.strip()) < 3 or not nama_2 or len(nama_2.strip()) < 3:
            st.error("🚨 Satpam NLP: Pastikan KEDUA nama diisi dengan benar (minimal 3 huruf).")
        elif tgl_1 == tgl_today or tgl_2 == tgl_today:
            st.error("🚨 Satpam NLP: Masukkan tanggal lahir yang valid ya!")
        else:
            with st.spinner('Mengkalkulasi Neptu Weton & Frekuensi NLP...'):
                time.sleep(1.5)
                
                neptu1, weton1 = get_neptu_weton(tgl_1)
                neptu2, weton2 = get_neptu_weton(tgl_2)
                total_neptu = neptu1 + neptu2
                sisa_weton = total_neptu % 8
                
                hasil_weton = {
                    1: ("💔 PEGAT (Rawan Gesekan)", "Menurut perhitungan Weton Jodoh, hubungan ini memiliki tantangan berat di area komunikasi. \n\n**Tantangan NLP:** Segera perkuat *Boundary* (batasan) hubungan kalian. Hindari pola '*Mind Reading*'."),
                    2: ("👑 RATU (Harmonis & Disegani)", "Sangat memukau! Hubungan kalian memancarkan kharisma yang membuat kalian dihargai lingkungan sekitar. \n\n**Tantangan NLP:** Jangan sampai terjebak pencitraan eksternal. Jaga kualitas interaksi berdua."),
                    3: ("💞 JODOH (Sinkronisasi Alami)", "Kalian memiliki toleransi dan penerimaan bawah sadar yang luar biasa tinggi. \n\n**Tantangan NLP:** Waspadai zona nyaman yang berlebihan. Sesekali ciptakan kejutan spontan agar romansa tidak pudar."),
                    4: ("🌱 TOPO (Ujian Bertumbuh)", "Awal hubungan mungkin terasa berat dan banyak ujian ego. Jika berhasil melewati fase kalibrasi ini, kalian akan sangat solid. \n\n**Tantangan NLP:** Kuasai teknik '*Reframing*'. Saat ada masalah, ubah sudut pandangnya."),
                    5: ("💰 TINARI (Magnet Rezeki)", "Penyatuan energi kalian membawa hoki yang melimpah dalam urusan karir dan finansial. \n\n**Tantangan NLP:** Jangan jadikan materi sebagai perekat utama. Arahkan fokus ke nilai-nilai spiritual bersama."),
                    6: ("⚡ PADU (Beda Frekuensi)", "Akan sering terjadi letupan perdebatan karena perbedaan cara memproses informasi di kepala masing-masing. \n\n**Tantangan NLP:** Latih teknik '*Pacing - Leading*'. Validasi emosinya dulu sebelum Anda membantah argumennya."),
                    7: ("👁️ SUJANAN (Rawan Asumsi)", "Ada kecenderungan kecemburuan, rasa tidak aman (*insecure*), atau salah paham yang sering muncul secara tiba-tiba. \n\n**Tantangan NLP:** Haram hukumnya menggunakan bahasa '*Generalization*'. Berlatihlah bicara murni berdasarkan fakta."),
                    0: ("🕊️ PESTHI (Damai & Rukun)", "Hubungan yang sangat adem ayem, stabil, dan jauh dari drama yang menguras energi. Sangat cocok untuk pernikahan jangka panjang. \n\n**Tantangan NLP:** Rutinlah melakukan kegiatan baru agar api asmara tetap menyala.")
                }
                
                ang_tgl_1 = hitung_angka(tgl_1)
                ang_tgl_2 = hitung_angka(tgl_2)
                selisih_tgl = abs(ang_tgl_1 - ang_tgl_2)
                
            st.markdown("---")
            nama_panggilan_1 = nama_1.split()[0].capitalize()
            nama_panggilan_2 = nama_2.split()[0].capitalize()
            st.subheader(f"🔮 Hasil Audit Asmara: {nama_panggilan_1} & {nama_panggilan_2}")
            
            st.caption(f"👤 Profil Weton {nama_panggilan_1}: **{weton1}** (Neptu: {neptu1})")
            st.caption(f"👤 Profil Weton {nama_panggilan_2}: **{weton2}** (Neptu: {neptu2})")
            st.caption(f"Total Integrasi Neptu: **{total_neptu}**")
            
            judul_weton, deskripsi_weton = hasil_weton.get(sisa_weton, ("Analisa unik", "Hubungan ini butuh kalibrasi personal."))
            st.info(f"#### {judul_weton}\n{deskripsi_weton}")
            
            st.markdown("---")
            st.markdown("#### Tingkat Sinkronisasi Meta-Program (Pola Pikir):")
            if selisih_tgl in [0, 3, 6, 9]:
                st.success(f"💘 **SKOR RAPPORT: 90% (Sangat Sinkron)**\n\nSecara filter pikiran, kalian sudah sefrekuensi. Resolusi konflik biasanya dapat diselesaikan dengan sangat cepat.")
            elif selisih_tgl in [1, 2, 8]:
                st.warning(f"⚖️ **SKOR RAPPORT: 70% (Saling Melengkapi)**\n\nBanyak perbedaan sudut pandang, namun ini bagus untuk saling belajar dan melengkapi kekurangan satu sama lain.")
            else:
                st.error(f"🔥 **SKOR RAPPORT: 50% (Butuh Kalibrasi Ekstra)**\n\nEgo dan dominasi sering berbenturan keras. Kalian butuh ruang khusus untuk benar-benar mempelajari *Love Language* masing-masing.")
            
            st.markdown("---")
            st.write("Ingin tahu skrip komunikasi NLP rahasia untuk meredam ego pasangan Anda?")
            st.link_button("Booking Sesi Couple Therapy", "https://wa.me/628999771486")

# ==========================================
# TAB 3: AUDIT PIKIRAN (WHEEL OF LIFE)
# ==========================================
with tab3:
    st.subheader("🕸️ Audit Keseimbangan Pikiran")
    
    st.info("**Apa itu Audit Pikiran?**\n\nBayangkan energi mental Anda sebagai sebuah roda penggerak. Jika satu sisi kempes atau bocor, laju hidup Anda pasti tersendat dan terasa *stuck*. \n\nAudit Pikiran adalah teknik pemetaan visual untuk melacak area mana di bawah sadar Anda yang sedang mengalami **kebocoran energi** paling parah.")
    
    st.write("Geser *slider* di bawah (angka 1-10) secara **jujur pada diri sendiri** untuk melihat bentuk riil jaring kehidupan Anda saat ini:")
    st.markdown("---")
    
    skor_mental = st.slider("Kesehatan Mental & Emosi", 1, 10, 5)
    skor_karir = st.slider("Karir & Finansial", 1, 10, 5)
    skor_asmara = st.slider("Hubungan Asmara", 1, 10, 5)
    skor_spiritual = st.slider("Spiritualitas & Makna Hidup", 1, 10, 5)
    skor_fisik = st.slider("Kesehatan Fisik", 1, 10, 5)
    
    kategori = ['Mental', 'Karir/Uang', 'Asmara', 'Spiritual', 'Fisik']
    skor = [skor_mental, skor_karir, skor_asmara, skor_spiritual, skor_fisik]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=skor + [skor[0]], 
        theta=kategori + [kategori[0]],
        fill='toself',
        fillcolor='rgba(212, 175, 55, 0.4)', 
        line=dict(color='#D4AF37')
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    avg_skor = sum(skor) / 5
    
    pesan_rendah = [
        "Peringatan: Roda kehidupan Anda sedang tidak seimbang. Segera benahi area dengan skor terendah sebelum memicu *burnout*.",
        "Sistem mendeteksi ketidakseimbangan fatal. Anda butuh kalibrasi ulang segera agar siklus masalah tidak terulang.",
        "Warning! Terlalu banyak energi mental yang terkuras. Jangan abaikan sisi yang 'bocor' ini jika ingin maju."
    ]
    
    pesan_sedang = [
        "Cukup baik, namun masih ada 'kebocoran' energi di area tertentu yang menghambat Anda melesat maksimal.",
        "Anda sudah di jalur yang benar, tapi ada 'rem tangan' tak kasat mata yang masih menahan laju potensi Anda.",
        "Grafik menunjukkan potensi stabil, namun sinkronisasi belum sempurna. Tutup celah pada skor terendah Anda.",
        "Kondisi mental Anda cukup aman, namun belum mencapai *Peak State*. Fokus perbaiki area yang paling melesak ke dalam."
    ]
    
    pesan_tinggi = [
        "Luar biasa! Kondisi *State of Mind* Anda sedang di puncak. Pertahankan keseimbangan ini.",
        "Sinergi yang sangat mantap! Pikiran bawah sadar Anda sedang berada dalam mode *High Performance*.",
        "Keseimbangan yang langka. Roda kehidupan Anda berputar mulus, ini momentum terbaik untuk mengeksekusi visi besar."
    ]

    if avg_skor < 5:
        st.error(random.choice(pesan_rendah))
    elif avg_skor < 8:
        st.warning(random.choice(pesan_sedang))
    else:
        st.success(random.choice(pesan_tinggi))

# ==========================================
# ULASAN DATABASE GOOGLE SHEETS & MARQUEE
# ==========================================
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #D4AF37;'>Telah Diakses oleh 5.500+ Pengguna</h4>", unsafe_allow_html=True)

# MARQUEE UNTUK SOCIAL PROOF
marquee_html = """
<div style="background-color: #1a1a1a; padding: 12px; border-radius: 8px; border-left: 3px solid #D4AF37; border-right: 3px solid #D4AF37; white-space: nowrap; overflow: hidden; margin-bottom: 20px;">
    <marquee behavior="scroll" direction="left" scrollamount="6" style="color: #f0f0f0; font-size: 15px;">
        <span style="color: #FFD700;">⭐⭐⭐⭐⭐</span> <b>dr. Antonius:</b> "Ini bukan cuma ramalan, ini pemetaan otak yang masuk akal. Investasi terbaik tahun ini!"     |    
        <span style="color: #FFD700;">⭐⭐⭐⭐⭐</span> <b>Andi S. (CEO):</b> "Sebagai tipe 8, saya kaget NLP ini bisa baca pola leadership saya. Mind-blowing!"     |    
        <span style="color: #FFD700;">⭐⭐⭐⭐</span> <b>Sinta W.:</b> "Sangat relate dengan pola asmara 'Gak Enakan'. Makasih Coach!"     |    
        <span style="color: #FFD700;">⭐⭐⭐⭐⭐</span> <b>Dewi Arini:</b> "Baru seminggu praktek, mental block finansial mulai luntur."     |    
        <span style="color: #FFD700;">⭐⭐⭐⭐⭐</span> <b>Budi T.:</b> "Baru sadar selama ini saya sabotase diri karena gampang bosen."     |    
        <span style="color: #FFD700;">⭐⭐⭐⭐</span> <b>Hendra Jaya:</b> "Gak nyangka weton bisa dikawinin sama NLP se-elegan ini."
    </marquee>
</div>
"""
st.markdown(marquee_html, unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Jejak Transformasi Terbaru</h3>", unsafe_allow_html=True)

daftar_ulasan = ambil_ulasan()

if not daftar_ulasan:
    st.caption("Belum ada ulasan terbaru, atau koneksi ke server sedang menyesuaikan.")
else:
    for ulasan in daftar_ulasan[:10]:
        nama = ulasan.get("Nama", "Anonim")
        rating = ulasan.get("Rating", "⭐⭐⭐⭐⭐")
        teks = ulasan.get("Komentar", "")
        if teks: 
            st.markdown(f"""
            <div class="ulasan-box">
                <b>{nama}</b> {rating}<br>
                <i>"{teks}"</i>
            </div>
            """, unsafe_allow_html=True)

with st.expander("💬 Bagikan Pengalaman Anda di sini"):
    with st.form("form_review"):
        rev_nama = st.text_input("Nama Anda")
        rev_rating = st.radio("Rating Bintang", ["⭐⭐⭐⭐⭐ (Sangat Akurat)", "⭐⭐⭐⭐ (Akurat)", "⭐⭐⭐ (Cukup)"], horizontal=True)
        rev_komentar = st.text_area("Tulis ulasan Anda di sini...")
        
        if st.form_submit_button("Kirim Ulasan"):
            if rev_nama and rev_komentar:
                sukses = kirim_ulasan(rev_nama, rev_rating.split(" ")[0], rev_komentar)
                if sukses:
                    st.success("Terima kasih! Ulasan Anda langsung masuk ke dimensi Real-Time. Mengupdate layar...")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("Waduh, koneksi ke database gagal. Coba lagi nanti ya.")
            else:
                st.warning("Mohon isi Nama dan Ulasan Anda terlebih dahulu.")

st.markdown("---")
st.markdown("<center><b>Ahmad Septian Dwi Cahyo</b><br><small>Certified NLP Trainer & Professional Hypnotherapist</small></center>", unsafe_allow_html=True)
