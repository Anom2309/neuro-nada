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

# --- FUNGSI NYAWA: TYPEWRITER EFFECT ---
def type_effect(text, speed=0.01):
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(full_text)
        time.sleep(speed)

# --- SALAM DINAMIS ---
def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 11: return "Selamat Pagi, Jiwa yang Luar Biasa"
    elif hour < 15: return "Selamat Siang, Sosok Visioner"
    elif hour < 18: return "Selamat Sore, Sang Pencari Makna"
    else: return "Selamat Malam, Pribadi yang Tenang"

# ==========================================
# DATABASE CLOUD: GOOGLE SHEETS
# ==========================================
URL_POST = "https://script.google.com/macros/s/AKfycbwkOL8-E50RKM5BRR8puh_XbfL-K_hQj5cnv0un6UzmFmMBEG6HZZ4aEQmFZj5EMsSBUQ/exec"
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2H-IH_8TbdbMRtvZnvza-InIO-Xl-B9YzLYtWtSb8vpUVuM1uZ4FTi6JwOtk2esj7hilwgGCoWex4/pub?output=csv"

@st.cache_data(ttl=30) # Mesin akan menarik data baru dari Excel setiap 30 detik
def ambil_ulasan():
    try:
        req = urllib.request.Request(URL_CSV)
        with urllib.request.urlopen(req) as response:
            decoded = response.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            data = [row for row in reader]
            return data[::-1] # Dibalik urutannya biar ulasan paling baru ada di atas
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

# --- CUSTOM CSS ---
st.markdown(
    """<style>
    div.stButton > button {
        background-color: #FFD700 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 50px !important;
        width: 100% !important;
        font-size: 16px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        background-color: #FFC107 !important;
    }
    .ulasan-box {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #FFD700;
        margin-bottom: 10px;
    }
    </style>""", 
    unsafe_allow_html=True
)

# --- SIDEBAR PROMOSI & VIDEO ---
with st.sidebar:
    if os.path.exists("baru.jpg.png"):
        st.image("baru.jpg.png", use_container_width=True)
    elif os.path.exists("baru.jpg"):
        st.image("baru.jpg", use_container_width=True)

    st.markdown(f"### {get_greeting()}")
    
    st.markdown("### 🎬 Hypno-Video Vault")
    st.video("https://youtu.be/kkRcH6aH_lI?si=bpUZF3CWl8DKLw5m")
    
    st.markdown("---")
    st.markdown("## 🧠 Sesi Transformasi")
    st.info("**Reset Pola Pikir Anda**\n\nSering merasa terhambat? Mari kita lakukan kalibrasi ulang dalam sesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    
    phone_number_sidebar = "628999771486"
    wa_link_sidebar = f"https://wa.me/{phone_number_sidebar}?text=Halo%20Coach%20Ahmad,%20saya%20siap%20untuk%20sesi%20Transformasi%20Pikiran."
    st.markdown(f"[👉 **Amankan Jadwal Anda**]({wa_link_sidebar})")
    
    st.markdown("---")
    st.success("**📚 Seni Persuasi NLP**\n\nPelajari bagaimana bahasa bekerja di tingkat bawah sadar.")
    st.markdown("[👉 **Akses Modul Lengkap**](https://lynk.id/username_lu/ebook-nlp)")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

# --- INTERFACE UTAMA & BANNER ---
if os.path.exists("banner.jpg"):
    st.image("banner.jpg", use_container_width=True)

st.markdown("<h1 style='text-align: center; margin-top: 10px;'>🧠 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 18px; color: #D4AF37;'>{get_greeting()}</p>", unsafe_allow_html=True)

# --- PEMUTAR MUSIK RELAKSASI ---
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #D4AF37;'>🎧 Soundscape Terapi</h4>", unsafe_allow_html=True)
st.caption("<div style='text-align: center; margin-bottom:10px;'>Tekan Play untuk memulai frekuensi relaksasi khusus dari Coach Ahmad Septian.</div>", unsafe_allow_html=True)

if os.path.exists("relaksasi.mp3"):
    st.audio("relaksasi.mp3", format="audio/mp3")
else:
    st.warning("⚠️ Menunggu file 'relaksasi.mp3' diupload ke GitHub.")
st.markdown("---")

# --- DATABASE ANALISA & POTENSI ---
vibrasi_nama_dict = {
    1: "Nama Anda memancarkan getaran KEMANDIRIAN & KEPEMIMPINAN.",
    2: "Nama Anda memancarkan getaran DIPLOMASI & KEDAMAIAN.",
    3: "Nama Anda memancarkan getaran EKSPRESI & KECERIAAN.",
    4: "Nama Anda memancarkan getaran STRUKTUR & KEDISIPLINAN.",
    5: "Nama Anda memancarkan getaran KEBEBASAN & DINAMIKA.",
    6: "Nama Anda memancarkan getaran TANGGUNG JAWAB & KASIH SAYANG.",
    7: "Nama Anda memancarkan getaran KEDALAMAN & ANALISA.",
    8: "Nama Anda memancarkan getaran OTORITAS & KESUKSESAN.",
    9: "Nama Anda memancarkan getaran KEMANUSIAAN & IDEALISME."
}

data_analisa = {
    1: {"karakter": "Anda memiliki profil 'The Leader (Sang Inisiator / Perintis)'. Meta-program Anda sangat proaktif dan berorientasi pada tujuan (Towards). Secara NLP, Anda sering menggunakan filter 'Self', yang membuat Anda mandiri namun kadang terlihat dominan.", "asmara": "Anda butuh pasangan yang menghargai independensi Anda. Hati-hati dengan pola komunikasi 'Command', cobalah lebih banyak menggunakan 'Request'."},
    2: {"karakter": "Anda adalah 'The Mediator (Sang Penjaga / Penyelaras)'. Kekuatan utama Anda adalah 'Building Rapport' secara instan. Anda sangat sensitif terhadap harmoni lingkungan.", "asmara": "Asmara bagi Anda adalah tentang kedekatan emosional. Waspadai pola 'Pleasing' yang berlebihan."},
    3: {"karakter": "Profil Anda adalah 'The Communicator (Sang Visioner / Ekspresif)'. Anda mahir dalam teknik 'Chunking Up' (melihat gambaran besar). Pikiran Anda sangat visual.", "asmara": "Hubungan yang ideal bagi Anda adalah yang penuh keceriaan. Cari partner yang bisa mengimbangi energi sosial Anda."},
    4: {"karakter": "Anda adalah 'The Architect (Sang Alchemist / Transformator)'. Struktur berpikir Anda sangat detail dan prosedural. Secara NLP, Anda memiliki filter 'Internal Reference' yang kuat.", "asmara": "Anda butuh kepastian dan rencana jangka panjang. Belajarlah sedikit lebih fleksibel dalam menerima perubahan."},
    5: {"karakter": "Profil 'The Explorer (Sang Eksekutor / Penggerak)'. Anda adalah ahli dalam 'Reframing' situasi sulit menjadi peluang. Anda sangat fleksibel.", "asmara": "Anda butuh ruang gerak (freedom). Hubungan yang mengekang akan membuat Anda merasa 'Suffocated'."},
    6: {"karakter": "Anda adalah 'The Nurturer (Sang Harmonizer / Penyeimbang)'. Fokus utama pikiran Anda adalah pada 'Values' dan tanggung jawab keluarga.", "asmara": "Asmara Anda berbasis pengabdian. Namun, hindari pola 'Mind Reading' (menebak-nebak pikiran pasangan)."},
    7: {"karakter": "Profil 'The Analyst (Sang Legacy Builder / Pembangun Makna)'. Anda adalah pemikir 'Deep Structure'. Intuisi Anda sangat kuat jika sudah terkalibrasi.", "asmara": "Anda butuh waktu 'Me Time' yang cukup. Cari pasangan yang menghargai kedalaman intelektual Anda."},
    8: {"karakter": "Anda adalah 'The Strategist (Sang Sovereign / Penguasa Diri)'. Orientasi Anda adalah pada 'Power' dan 'Outcome'.", "asmara": "Jangan bawa gaya 'Negotiation' bisnis ke dalam ranah asmara. Gunakan lebih banyak 'Soft Skills'."},
    9: {"karakter": "Profil 'The Humanist (Sang Ascended / Kesadaran Tinggi)'. Secara NLP, Anda cenderung memandang dunia secara 'Holistik'.", "asmara": "Anda mencari koneksi jiwa (Soulmate). Tetaplah realistis dalam membangun hubungan."}
}

closing_brutal_dinamis = {
    1: ["Terus menunda karena merasa 'belum sempurna'", "Sulit percaya pada orang lain", "Meng-sabotase diri sendiri"],
    2: ["Terjebak memuaskan orang lain", "Takut berkata 'TIDAK'", "Memendam emosi"],
    3: ["Ide brilian tapi jarang selesai", "Mudah teralihkan fokus", "Menutupi kegelisahan"],
    4: ["Stres berat jika rencana berubah", "Stuck dalam rutinitas kaku", "Kurang empati karena terlalu logis"],
    5: ["Berlari tanpa fondasi kuat", "Cepat merasa tercekik rutinitas", "Kehilangan arah"],
    6: ["Kehabisan energi karena menyelamatkan orang lain", "Over-controlling", "Merasa bersalah memprioritaskan diri"],
    7: ["Terjebak Overthinking", "Merasa terisolasi", "Analisa tanpa eksekusi"],
    8: ["Merasa hampa di tengah target", "Terlihat dingin", "Burnout karena tekanan"],
    9: ["Sering kecewa standar moral tinggi", "Mengizinkan orang toksik menetap", "Kewalahan mengeksekusi visi"]
}

# --- FUNGSI LOGIKA ---
def hitung_angka(tanggal):
    tgl_str = tanggal.strftime("%d%m%Y")
    total = sum(int(digit) for digit in tgl_str)
    while total > 9: total = sum(int(digit) for digit in str(total))
    return total

def get_neptu_weton(tanggal):
    anchor_date = datetime.date(2000, 1, 1)
    selisih_hari = (tanggal - anchor_date).days
    hari_masehi = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_jawa = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"]
    hari = hari_masehi[tanggal.weekday()]
    pasaran = pasaran_jawa[selisih_hari % 5]
    neptu_hari = {"Minggu": 5, "Senin": 4, "Selasa": 3, "Rabu": 7, "Kamis": 8, "Jumat": 6, "Sabtu": 9}
    neptu_pasaran = {"Legi": 5, "Pahing": 9, "Pon": 7, "Wage": 4, "Kliwon": 8}
    return neptu_hari[hari] + neptu_pasaran[pasaran], f"{hari} {pasaran}"

# --- MENU TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Personal Mapping", "👩‍❤️‍👨 Couple Sync", "🕸️ Audit Pikiran"])

# ==========================================
# TAB 1: PERSONAL MAPPING
# ==========================================
with tab1:
    st.subheader("Bongkar Pola Bawah Sadar")
    nama_user = st.text_input("Nama Lengkap Anda:", placeholder="Siapa nama Anda?", key="t1_nama")
    tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date.today(), format="DD/MM/YYYY")

    if st.button("Mulai Kalibrasi"):
        if len(nama_user) < 3 or tgl_input == datetime.date.today():
            st.error("🚨 Mohon isi nama dan tanggal lahir yang benar.")
        else:
            with st.spinner('Menyelaraskan gelombang otak...'):
                time.sleep(1)
                kode_p = hitung_angka(tgl_input)
                nep, wet = get_neptu_weton(tgl_input)
                insight = data_analisa.get(kode_p)
                pains = closing_brutal_dinamis.get(kode_p)
            
            st.balloons()
            st.markdown(f"### Hasil Mapping: {nama_user}")
            st.info(f"**Kode Program: {kode_p}** | **Weton: {wet}**")
            
            st.subheader("💡 Struktur Karakter")
            type_effect(insight['karakter'])
            
            st.subheader("❤️ Pola Asmara")
            st.warning(insight['asmara'])
            
            st.markdown("---")
            st.error(f"🚨 **Peringatan Bawah Sadar:**\nAnda mungkin sering: \n- {pains[0]}\n- {pains[1]}\n- {pains[2]}")
            
            link_p = {i: f"https://lynk.id/neuronada/checkout-kode-{i}" for i in range(1, 10)}
            st.link_button(f"🔓 Ambil Modul Kode {kode_p}", link_p.get(kode_p))

# ==========================================
# TAB 2: COUPLE SYNC (WETON & NLP INTEGRATION)
# ==========================================
with tab2:
    st.subheader("Kalkulator Sinkronisasi Pasangan")
    st.write("Uji kecocokan *Meta-Program* Anda dan pasangan berdasarkan Vibrasi Nama & Weton Primbon Nusantara.")
    
    colA, colB = st.columns(2)
    with colA:
        nama_1 = st.text_input("Nama Anda:", key="c_nama1")
        tgl_1 = st.date_input("Tgl Lahir Anda:", min_value=datetime.date(1920, 1, 1), key="c_tgl1")
    with colB:
        nama_2 = st.text_input("Nama Pasangan/Gebetan:", key="c_nama2")
        tgl_2 = st.date_input("Tgl Lahir Pasangan:", min_value=datetime.date(1920, 1, 1), key="c_tgl2")
        
    if st.button("Cek Kompatibilitas Bawah Sadar"):
        tgl_today = datetime.date.today()
        
        # PASUKAN SATPAM NLP
        if not nama_1 or len(nama_1.strip()) < 3 or not nama_2 or len(nama_2.strip()) < 3:
            st.error("🚨 Satpam NLP: Pastikan KEDUA nama diisi dengan benar (minimal 3 huruf) agar vibrasi hubungan bisa dihitung sempurna.")
        elif tgl_1 == tgl_today or tgl_2 == tgl_today:
            st.error("🚨 Satpam NLP: Masa iya lahirnya hari ini langsung pacaran? Masukkan tanggal lahir yang valid ya!")
        else:
            with st.spinner('Mengkalkulasi Neptu Weton & Frekuensi NLP...'):
                time.sleep(1.5)
                
            # 1. LOGIKA NEPTU WETON (PRIMBON JODOH)
            neptu1, weton1 = get_neptu_weton(tgl_1)
            neptu2, weton2 = get_neptu_weton(tgl_2)
            total_neptu = neptu1 + neptu2
            sisa_weton = total_neptu % 8
            
            # DATABASE WETON & NLP TANTANGAN
            hasil_weton = {
                1: ("💔 PEGAT (Rawan Gesekan)", "Menurut perhitungan Weton Jodoh, hubungan ini memiliki tantangan berat di area komunikasi dan kecenderungan campur tangan pihak luar. \n\n**Tantangan NLP:** Segera perkuat *Boundary* (batasan) hubungan kalian. Hindari pola '*Mind Reading*' (berharap pasangan ngerti tanpa diomongin)."),
                2: ("👑 RATU (Harmonis & Disegani)", "Sangat memukau! Hubungan kalian memancarkan kharisma yang membuat kalian dihargai dan disegani oleh lingkungan sekitar. \n\n**Tantangan NLP:** Jangan sampai terjebak pencitraan eksternal (Filter *Others*). Pastikan komunikasi internal saat berdua sama baiknya dengan saat di depan publik."),
                3: ("💞 JODOH (Sinkronisasi Alami)", "Kalian memiliki toleransi dan penerimaan bawah sadar yang luar biasa tinggi satu sama lain. Definisi *Soulmate* sejati. \n\n**Tantangan NLP:** Waspadai zona nyaman yang berlebihan. Sesekali ciptakan percikan '*Break State*' (kejutan spontan) agar romansa tidak pudar ditelan rutinitas."),
                4: ("🌱 TOPO (Ujian Bertumbuh)", "Awal hubungan mungkin terasa berat dan banyak ujian ego. Namun jika berhasil melewati fase kalibrasi ini, kalian akan sangat solid. \n\n**Tantangan NLP:** Kuasai teknik '*Reframing*'. Saat ada masalah, ubah sudut pandangnya dari 'dia nyari ribut' menjadi 'dia sedang berusaha menyampaikan kebutuhannya'."),
                5: ("💰 TINARI (Magnet Rezeki)", "Penyatuan energi kalian membawa hoki yang melimpah. Ada saja jalan kemudahan dalam urusan karir dan finansial saat kalian bersama. \n\n**Tantangan NLP:** Jangan jadikan materi sebagai satu-satunya perekat. Arahkan fokus ke '*Outcome*' yang lebih besar, seperti membangun nilai-nilai spiritual bersama."),
                6: ("⚡ PADU (Beda Frekuensi)", "Akan sering terjadi letupan perdebatan atau cekcok ringan karena perbedaan cara memproses informasi di kepala masing-masing. \n\n**Tantangan NLP:** Latih keras teknik '*Pacing - Leading*'. Selalu setujui/validasi emosinya dulu sebelum Anda membantah argumennya."),
                7: ("👁️ SUJANAN (Rawan Asumsi)", "Ada kecenderungan kecemburuan, rasa tidak aman (*insecure*), atau salah paham yang sering muncul secara tiba-tiba. \n\n**Tantangan NLP:** Haram hukumnya menggunakan bahasa '*Generalization*' (misal: 'Kamu emang SELALU begini!'). Berlatihlah bicara murni berdasarkan data dan fakta hari itu saja."),
                0: ("🕊️ PESTHI (Damai & Rukun)", "Hubungan yang sangat adem ayem, stabil, dan jauh dari drama yang menguras energi. Sangat cocok untuk pernikahan jangka panjang. \n\n**Tantangan NLP:** Saking damainya, hubungan bisa terasa hambar. Rutinlah melakukan '*Pattern Interrupt*' (kegiatan baru yang belum pernah dilakukan) agar api asmara tetap menyala.")
            }
            
            # 2. LOGIKA TANGGAL LAHIR (RAPPORT)
            ang_tgl_1 = hitung_angka(tgl_1)
            ang_tgl_2 = hitung_angka(tgl_2)
            selisih_tgl = abs(ang_tgl_1 - ang_tgl_2)
            
            st.markdown("---")
            nama_panggilan_1 = nama_1.split()[0].capitalize()
            nama_panggilan_2 = nama_2.split()[0].capitalize()
            st.subheader(f"🔮 Hasil Audit Asmara: {nama_panggilan_1} & {nama_panggilan_2}")
            
            # Menampilkan Neptu
            st.caption(f"🧩 Profil Weton {nama_panggilan_1}: **{weton1}** (Neptu: {neptu1})")
            st.caption(f"🧩 Profil Weton {nama_panggilan_2}: **{weton2}** (Neptu: {neptu2})")
            st.caption(f"Total Integrasi Neptu: **{total_neptu}**")
            
            # Menampilkan Hasil Kombinasi Weton & NLP
            judul_weton, deskripsi_weton = hasil_weton.get(sisa_weton, ("Analisa unik", "Hubungan ini butuh kalibrasi personal."))
            st.info(f"#### {judul_weton}\n{deskripsi_weton}")
            
            # Menampilkan Skor Sinkronisasi Meta-Program (Sebagai pendukung)
            st.markdown("---")
            st.markdown("#### Tingkat Sinkronisasi Meta-Program (Pola Pikir):")
            if selisih_tgl == 0 or selisih_tgl == 3 or selisih_tgl == 6 or selisih_tgl == 9:
                st.success(f"💘 **SKOR RAPPORT: 90% (Sangat Sinkron)**\n\nSecara filter pikiran, kalian sudah sefrekuensi. Resolusi konflik biasanya dapat diselesaikan dengan sangat cepat.")
            elif selisih_tgl == 1 or selisih_tgl == 2 or selisih_tgl == 8:
                st.warning(f"⚖️ **SKOR RAPPORT: 70% (Saling Melengkapi)**\n\nBanyak perbedaan sudut pandang, namun ini bagus untuk saling belajar dan melengkapi kekurangan satu sama lain.")
            else:
                st.error(f"🔥 **SKOR RAPPORT: 50% (Butuh Kalibrasi Ekstra)**\n\nEgo dan dominasi sering berbenturan keras. Kalian butuh ruang khusus untuk benar-benar mempelajari *Love Language* masing-masing.")
            
            st.markdown("---")
            st.write("Ingin tahu skrip komunikasi NLP rahasia untuk meredam ego pasangan Anda? Konsultasikan secara privat bersama Coach Ahmad.")
            st.link_button("Booking Sesi Couple Therapy", "https://wa.me/628999771486")
# ==========================================
# TAB 3: AUDIT PIKIRAN
# ==========================================
with tab3:
    st.subheader("🕸️ Audit Keseimbangan Pikiran")
    skor = [st.slider(k, 1, 10, 5) for k in ['Mental', 'Karir', 'Asmara', 'Spiritual', 'Fisik']]
    if st.button("Lihat Radar"):
        fig = go.Figure(data=go.Scatterpolar(r=skor+[skor[0]], theta=['Mental','Karir','Asmara','Spiritual','Fisik','Mental'], fill='toself'))
        st.plotly_chart(fig)
        avg = sum(skor)/5
        msgs = ["Butuh Kalibrasi Segera!", "Kondisi Stabil.", "Luar Biasa, Anda di Peak State!"]
        if avg < 5: st.error(random.choice(msgs[:1]))
        elif avg < 8: st.warning(random.choice(msgs[1:2]))
        else: st.success(random.choice(msgs[2:]))

# ==========================================
# ULASAN DATABASE GOOGLE SHEETS
# ==========================================
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Suara Transformasi</h3>", unsafe_allow_html=True)
st.write("Lihat apa kata mereka yang telah membongkar pola bawah sadarnya di Neuro Nada.")

# Menarik data ulasan dari Google Sheets
daftar_ulasan = ambil_ulasan()

# Tampilkan Maksimal 10 Ulasan Teratas
for ulasan in daftar_ulasan[:10]:
    nama = ulasan.get("Nama", "Anonim")
    rating = ulasan.get("Rating", "⭐⭐⭐⭐⭐")
    teks = ulasan.get("Komentar", "")
    
    if teks: # Hanya tampilkan jika kolom komentar tidak kosong
        st.markdown(f"""
        <div class="ulasan-box">
            <b>{nama}</b> {rating}<br>
            <i>"{teks}"</i>
        </div>
        """, unsafe_allow_html=True)

# Form Input Ulasan Baru ke Excel
with st.expander("💬 Bagikan Pengalaman Anda di sini"):
    with st.form("form_review"):
        rev_nama = st.text_input("Nama Anda")
        rev_rating = st.radio("Rating Bintang", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐"], horizontal=True)
        rev_komentar = st.text_area("Tulis ulasan Anda di sini...")
        
        if st.form_submit_button("Kirim Ulasan"):
            if rev_nama and rev_komentar:
                # Mengirim data ke Google Sheets
                sukses = kirim_ulasan(rev_nama, rev_rating, rev_komentar)
                if sukses:
                    st.success("Terkirim! Terima kasih atas ulasan Anda. Memperbarui layar...")
                    st.cache_data.clear() # Membersihkan ingatan agar ulasan baru langsung terbaca
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Waduh, koneksi ke database gagal. Coba lagi nanti ya.")
            else:
                st.warning("Mohon isi Nama dan Ulasan Anda terlebih dahulu.")

st.markdown("---")
st.markdown("<center><b>Neuro Nada Academy</b><br><small>Ahmad Septian Dwi Cahyo</small></center>", unsafe_allow_html=True)
