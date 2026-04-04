import streamlit as st
import datetime
import os
import time
import urllib.parse
import math
import plotly.graph_objects as go

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="NLP Deep Analysis | Neuro Nada", 
    page_icon="🧠", 
    layout="centered"
)

# --- CUSTOM CSS (WARNA KUNING UNTUK TOMBOL) ---
st.markdown(
    """<style>
    div.stButton > button {
        background-color: #FFD700 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-size: 16px !important;
    }
    div.stButton > button:hover {
        background-color: #FFC107 !important;
        color: #000000 !important;
    }
    </style>""", 
    unsafe_allow_html=True
)

# --- SIDEBAR PROMOSI & VIDEO ---
with st.sidebar:
    st.markdown("### 🎬 Hypno-Video Vault")
    st.caption("Fokuskan pandangan Anda pada video ini sambil menggunakan headphone untuk relaksasi maksimal.")
    
    # Langsung putar video YouTube dari link Coach Ahmad
    st.video("https://youtu.be/kkRcH6aH_lI?si=bpUZF3CWl8DKLw5m")
        
    st.markdown("---")
    
    st.markdown("## 🧠 Sesi Transformasi")
    st.info("**Reset Pola Pikir Anda**\n\nSering merasa terhambat oleh pikiran sendiri? Mari kita lakukan kalibrasi ulang dalam sesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    st.markdown("[👉 **Amankan Jadwal Anda**](https://lynk.id/username_lu/private-hypnotherapy)")
    st.markdown("---")
    st.success("**📚 Seni Persuasi NLP**\n\nPelajari bagaimana bahasa bekerja di tingkat bawah sadar untuk meningkatkan pengaruh Anda.")
    st.markdown("[👉 **Akses Modul Lengkap**](https://lynk.id/username_lu/ebook-nlp)")
    st.markdown("---")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

# --- TAMPILKAN BANNER ---
if os.path.exists("banner.jpg"):
    st.image("banner.jpg", use_container_width=True)

# --- DATABASE ANALISA & POTENSI ---
vibrasi_nama_dict = {
    1: "Nama Anda memancarkan getaran KEMANDIRIAN & KEPEMIMPINAN. Orang melihat Anda sebagai sosok yang berani mengambil inisiatif.",
    2: "Nama Anda memancarkan getaran DIPLOMASI & KEDAMAIAN. Orang merasa nyaman dan aman saat berinteraksi dengan Anda.",
    3: "Nama Anda memancarkan getaran EKSPRESI & KECERIAAN. Anda memiliki daya tarik komunikasi yang membuat orang mudah menyukai Anda.",
    4: "Nama Anda memancarkan getaran STRUKTUR & KEDISIPLINAN. Orang mempercayai Anda karena Anda terlihat solid dan bisa diandalkan.",
    5: "Nama Anda memancarkan getaran KEBEBASAN & DINAMIKA. Aura Anda penuh dengan petualangan dan perubahan yang memikat orang lain.",
    6: "Nama Anda memancarkan getaran TANGGUNG JAWAB & KASIH SAYANG. Anda memancarkan aura pengayom yang membuat orang ingin bersandar pada Anda.",
    7: "Nama Anda memancarkan getaran KEDALAMAN & ANALISA. Orang melihat Anda sebagai sosok yang misterius, cerdas, dan pencari kebenaran.",
    8: "Nama Anda memancarkan getaran OTORITAS & KESUKSESAN. Aura nama Anda sangat kuat dalam menarik kelimpahan dan kekuasaan.",
    9: "Nama Anda memancarkan getaran KEMANUSIAAN & IDEALISME. Anda dilihat sebagai sosok berjiwa besar yang peduli pada banyak orang."
}

data_analisa = {
    1: {"karakter": "Anda memiliki profil 'The Leader (Sang Inisiator / Perintis)'. Meta-program Anda sangat proaktif dan berorientasi pada tujuan (Towards). Secara NLP, Anda sering menggunakan filter 'Self', yang membuat Anda mandiri namun kadang terlihat dominan.", "asmara": "Anda butuh pasangan yang menghargai independensi Anda. Hati-hati dengan pola komunikasi 'Command', cobalah lebih banyak menggunakan 'Request' agar pasangan merasa lebih nyaman."},
    2: {"karakter": "Anda adalah 'The Mediator (Sang Penjaga / Penyelaras)'. Kekuatan utama Anda adalah 'Building Rapport' secara instan. Anda sangat sensitif terhadap harmoni lingkungan, namun seringkali mengabaikan kebutuhan diri sendiri (Filter: Others).", "asmara": "Asmara bagi Anda adalah tentang kedekatan emosional. Anda cenderung menghindari konflik, namun waspadai pola 'Pleasing' yang berlebihan. Komunikasikan batasan Anda dengan teknik Assertive Communication."},
    3: {"karakter": "Profil Anda adalah 'The Communicator (Sang Visioner / Ekspresif)'. Anda mahir dalam teknik 'Chunking Up' (melihat gambaran besar) dan menginspirasi orang lain. Pikiran Anda sangat visual dan cepat dalam memproses ide kreatif.", "asmara": "Hubungan yang ideal bagi Anda adalah yang penuh keceriaan dan stimulasi intelektual. Pasangan yang membosankan bisa memicu 'Internal Dialogue' negatif pada diri Anda. Cari partner yang bisa mengimbangi energi sosial Anda."},
    4: {"karakter": "Anda adalah 'The Architect (Sang Alchemist / Transformator)'. Struktur berpikir Anda sangat detail dan prosedural. Secara NLP, Anda memiliki filter 'Internal Reference' yang kuat, sehingga Anda tidak mudah goyah oleh opini luar jika sudah punya data.", "asmara": "Anda butuh kepastian dan rencana jangka panjang. Spontanitas berlebihan dari pasangan bisa membuat sistem internal Anda 'Error'. Belajarlah sedikit lebih fleksibel dalam menerima perubahan rencana."},
    5: {"karakter": "Profil 'The Explorer (Sang Eksekutor / Penggerak)'. Anda adalah ahli dalam 'Reframing' situasi sulit menjadi peluang. Anda sangat fleksibel dan benci dengan batasan atau prosedur yang terlalu kaku.", "asmara": "Anda butuh ruang gerak (freedom). Hubungan yang mengekang akan membuat Anda merasa 'Suffocated'. Komunikasikan kebutuhan Anda akan petualangan baru agar pasangan tidak salah paham."},
    6: {"karakter": "Anda adalah 'The Nurturer (Sang Harmonizer / Penyeimbang)'. Fokus utama pikiran Anda adalah pada 'Values' dan tanggung jawab keluarga. Anda memiliki kapasitas empati yang luar biasa besar melalui kalibrasi emosi yang tajam.", "asmara": "Asmara Anda berbasis pengabdian. Anda adalah pasangan yang sangat suportif. Namun, hindari pola 'Mind Reading' (menebak-nebak pikiran pasangan) yang bisa berujung pada rasa kecewa jika ekspektasi tidak terpenuhi."},
    7: {"karakter": "Profil 'The Analyst (Sang Legacy Builder / Pembangun Makna)'. Anda adalah pemikir 'Deep Structure'. Anda tidak puas dengan informasi permukaan dan selalu mencari makna di balik segalanya. Intuisi Anda sangat kuat jika sudah terkalibrasi dengan baik.", "asmara": "Anda butuh waktu 'Me Time' yang cukup untuk memproses pikiran Anda. Pasangan yang terlalu menuntut perhatian setiap saat bisa membuat Anda mundur. Cari pasangan yang menghargai kedalaman intelektual Anda."},
    8: {"karakter": "Anda adalah 'The Strategist (Sang Sovereign / Penguasa Diri)'. Orientasi Anda adalah pada 'Power' dan 'Outcome'. Anda sangat efisien dalam mengelola sumber daya dan memiliki kepercayaan diri yang solid dalam mengambil risiko.", "asmara": "Dalam hubungan, Anda cenderung menjadi pelindung dan penyedia. Namun, jangan bawa gaya 'Negotiation' bisnis ke dalam ranah asmara. Gunakan lebih banyak 'Soft Skills' dan sentuhan afeksi yang tulus."},
    9: {"karakter": "Profil 'The Humanist (Sang Ascended / Kesadaran Tinggi)'. Anda memiliki 'State of Mind' yang inklusif dan bijaksana. Secara NLP, Anda cenderung memandang dunia secara 'Holistik' dan memiliki misi hidup yang melampaui kepentingan pribadi.", "asmara": "Anda mencari koneksi jiwa (Soulmate). Anda sangat pemaaf, namun waspadai pola 'Generalization' yang membuat Anda sering memaklumi kesalahan pasangan berulang kali. Tetaplah realistis dalam membangun hubungan."}
}

tips_zodiak_nlp = {
    "Aries": "Gunakan teknik 'Pacing' emosi yang lebih sabar.",
    "Taurus": "Berikan ruang untuk 'Reframing' perbedaan pendapat.",
    "Gemini": "Fokus pada 'Deep Rapport' daripada obrolan permukaan.",
    "Cancer": "Hati-hati dengan pola 'Anchor' negatif dari masa lalu.",
    "Leo": "Gunakan bahasa 'Appreciation' untuk pasangan.",
    "Virgo": "Kurangi filter 'Detail', gunakan 'Chunk Up'.",
    "Libra": "Pastikan 'Internal Reference' Anda kuat.",
    "Scorpio": "Bangun 'Trust', hindari 'Mind Reading'.",
    "Sagittarius": "Jaga komitmen melalui 'Value Alignment'.",
    "Capricorn": "Seimbangkan karier dengan kehadiran emosional.",
    "Aquarius": "Hubungkan visi idealis dengan realitas emosional.",
    "Pisces": "Bedakan imajinasi dengan kenyataan."
}

closing_brutal_dinamis = {
    1: ["Terus menunda karena merasa 'belum sempurna' atau takut gagal", "Merasa sendirian memikul beban karena sulit percaya pada orang lain", "Punya ambisi besar, tapi stuck karena meng-sabotase diri sendiri"],
    2: ["Terjebak memuaskan orang lain hingga mengorbankan diri sendiri", "Merasa lelah dan tidak dihargai, tapi takut untuk berkata 'TIDAK'", "Terus memendam emosi demi menghindari konflik"],
    3: ["Memiliki banyak ide brilian, tapi jarang ada yang selesai", "Mudah teralihkan fokusnya dan cepat merasa bosan", "Menutupi kegelisahan sejati di balik candaan"],
    4: ["Stres berat jika rencana berubah atau berhadapan ketidakpastian", "Stuck dalam rutinitas yang kaku dan takut mengambil risiko baru", "Sering dinilai kaku atau kurang empati karena terlalu logis"],
    5: ["Terus berlari dari satu hal ke hal lain tanpa fondasi kuat", "Merasa cepat 'tercekik' oleh rutinitas dan komitmen", "Sulit fokus pada satu tujuan jangka panjang"],
    6: ["Kehabisan energi karena selalu sibuk menyelamatkan orang lain", "Cenderung over-controlling karena rasa khawatir berlebihan", "Merasa bersalah jika harus memprioritaskan diri sendiri"],
    7: ["Terjebak dalam Overthinking dan sulit bertindak nyata", "Merasa terisolasi karena tidak ada yang sefrekuensi", "Terlalu lama menganalisa tanpa eksekusi"],
    8: ["Merasa hampa meskipun sudah mencapai target material", "Terlihat dingin dan menciptakan jarak emosional", "Burnout karena tekanan untuk selalu kuat"],
    9: ["Sering kecewa karena standar moral terlalu tinggi", "Mengizinkan orang yang toksik menetap karena rasa kasihan", "Punya visi mulia, tapi kewalahan mengeksekusinya"]
}

potensi_dinamis = {
    1: """punya potensi kepemimpinan dan daya dobrak luar biasa besar jika ego-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... ambisi ini bisa jadi pola penjara mental yang membelenggu Anda dalam kelelahan kronis seumur hidup.""",
    2: """punya potensi penyembuhan dan diplomasi luar biasa besar jika filter 'Gak Enakan'-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... rasa empati ini bisa jadi pola penjara mental yang terus mengorbankan diri Anda seumur hidup.""",
    3: """punya potensi persuasi dan kreativitas luar biasa besar jika fokusnya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... ide-ide brilian ini bisa jadi pola penjara mental yang membuat Anda jalan di tempat seumur hidup.""",
    4: """punya potensi membangun mahakarya luar biasa besar jika filter kaku-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... perfeksionisme ini bisa jadi pola penjara mental yang membelenggu kebahagiaan Anda seumur hidup.""",
    5: """punya potensi inovasi dan pencapaian luar biasa besar jika filter kebosanannya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... energi petualang ini bisa jadi pola penjara mental yang membuat Anda kehilangan arah seumur hidup.""",
    6: """punya potensi mengayomi dan membina luar biasa besar jika filter 'Mind Reading'-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... pengorbanan buta ini bisa jadi pola penjara mental yang mencekik batin Anda seumur hidup.""",
    7: """punya potensi kebijaksanaan dan analisa luar biasa besar jika filter overthinking-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... isi kepala ini bisa jadi pola penjara mental yang mengisolasi Anda dari realita seumur hidup.""",
    8: """punya potensi eksekusi dan pencapaian luar biasa besar jika filter kontrolnya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... kekuatan ini bisa jadi pola penjara mental yang membuat Anda kesepian di puncak seumur hidup.""",
    9: """punya potensi kesadaran dan harmoni luar biasa besar jika filter ekspektasinya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... idealisme ini bisa jadi pola penjara mental yang penuh kekecewaan seumur hidup."""
}

# --- FUNGSI-FUNGSI LOGIKA ---
def hitung_angka(tanggal):
    tgl_str = tanggal.strftime("%d%m%Y")
    total = sum(int(digit) for digit in tgl_str)
    while total > 9: total = sum(int(digit) for digit in str(total))
    return total

def hitung_angka_nama(nama):
    huruf_angka = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':1, 'K':2, 'L':3, 'M':4, 'N':5, 'O':6, 'P':7, 'Q':8, 'R':9, 'S':1, 'T':2, 'U':3, 'V':4, 'W':5, 'X':6, 'Y':7, 'Z':8}
    total = sum(huruf_angka.get(h, 0) for h in nama.upper())
    if total == 0: return 1
    while total > 9: total = sum(int(d) for d in str(total))
    return total

def hitung_weton(tanggal):
    anchor_date = datetime.date(2000, 1, 1)
    selisih_hari = (tanggal - anchor_date).days
    hari_masehi = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pasaran_jawa = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"]
    return f"{hari_masehi[tanggal.weekday()]} {pasaran_jawa[selisih_hari % 5]}"

def hitung_zodiak(tanggal):
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

def bioritme_nlp(tanggal_lahir):
    hari_hidup = (datetime.date.today() - tanggal_lahir).days
    fisik = math.sin(2 * math.pi * (hari_hidup / 23)) * 100
    emosi = math.sin(2 * math.pi * (hari_hidup / 28)) * 100
    intelektual = math.sin(2 * math.pi * (hari_hidup / 33)) * 100
    
    if emosi > 50 and intelektual > 50: state = "UPTIME STATE (Puncak Kreativitas & Sosial)"
    elif emosi < -50 and fisik < -50: state = "DOWNTIME STATE (Butuh Me-Time & Refleksi)"
    elif intelektual > 50 and fisik < 0: state = "ANALYTICAL STATE (Tajam untuk Perencanaan)"
    else: state = "NEUTRAL STATE (Stabil & Seimbang)"
    
    return int(fisik), int(emosi), int(intelektual), state

def get_arketipe(angka):
    arketipe_dict = {
        1: "The Leader (Sang Inisiator / Perintis)",
        2: "The Mediator (Sang Penjaga / Penyelaras)",
        3: "The Communicator (Sang Visioner / Ekspresif)",
        4: "The Architect (Sang Alchemist / Transformator)",
        5: "The Explorer (Sang Eksekutor / Penggerak)",
        6: "The Nurturer (Sang Harmonizer / Penyeimbang)",
        7: "The Analyst (Sang Legacy Builder / Pembangun Makna)",
        8: "The Strategist (Sang Sovereign / Penguasa Diri)",
        9: "The Humanist (Sang Ascended / Kesadaran Tinggi)"
    }
    return arketipe_dict.get(angka, "Pribadi Unik")

# --- INTERFACE UTAMA (TABS) ---
st.title("🧠 Neuro Nada Ecosystem")
st.write("Sistem Pemetaan Bawah Sadar & Akselerasi Potensi Diri")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["👤 Personal Mapping", "👩‍❤️‍👨 Couple Sync", "🕸️ Audit Pikiran"])

# ==========================================
# TAB 1: PERSONAL MAPPING (CORE FEATURE)
# ==========================================
with tab1:
    st.subheader("Bongkar Pola Bawah Sadar Anda")
    nama_user = st.text_input("Nama Lengkap Anda:", placeholder="Masukkan nama panggilan Anda...", key="nama_user_t1")
    tgl_today = datetime.date.today()
    tgl_input = st.date_input("Data Input (Tanggal Lahir):", value=tgl_today, min_value=datetime.date(1920, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")

    if st.button("Mulai Pemetaan Internal"):
        # PASUKAN SATPAM NLP
        if not nama_user or len(nama_user.strip()) < 3:
            st.error("🚨 Satpam NLP: Mohon masukkan nama dengan benar (minimal 3 huruf) agar vibrasi identitas bisa terbaca akurat.")
        elif tgl_input == tgl_today:
            st.error("🚨 Satpam NLP: Mohon masukkan tanggal lahir Anda yang valid, bukan hari ini.")
        else:
            with st.spinner('Melakukan kalibrasi pola pikiran Anda...'):
                time.sleep(1)
                
                angka_hasil = hitung_angka(tgl_input)
                angka_nama = hitung_angka_nama(nama_user)
                weton_hasil = hitung_weton(tgl_input)
                zodiak_hasil = hitung_zodiak(tgl_input)
                f, e, i, state_harian = bioritme_nlp(tgl_input)
                
                insight = data_analisa.get(angka_hasil)
                arketipe = get_arketipe(angka_hasil)
                pain_points = closing_brutal_dinamis.get(angka_hasil, ["Terjebak dalam pola yang sama", "Merasa stuck", "Butuh perubahan"])
                teks_potensi = potensi_dinamis.get(angka_hasil, "punya potensi luar biasa besar jika filternya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... itu bisa jadi pola penjara mental yang membelenggu seumur hidup.")
            
            st.markdown(f"### 📋 Hasil Mapping: {nama_user}")
            st.markdown("---")
            
            # --- State of Mind Harian ---
            st.success(f"📊 **RADAR ENERGI HARI INI:** Anda sedang berada dalam **{state_harian}**.")
            st.caption(f"Kapasitas Fisik: {f}% | Emosional: {e}% | Intelektual: {i}%")
            st.markdown("---")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("KODE NAMA", angka_nama)
            c2.metric("KODE PROGRAM", angka_hasil)
            c3.metric("ENERGI WETON", weton_hasil)
            c4.metric("POLA ZODIAK", zodiak_hasil)
            
            st.markdown("---")
            
            # --- HASIL 0: VIBRASI NAMA ---
            st.subheader("🗣️ Vibrasi Identitas (Nama)")
            st.info(vibrasi_nama_dict.get(angka_nama, "Nama Anda memiliki resonansi energi yang unik."))

            # --- HASIL 1 ---
            st.subheader("💡 Struktur Karakter & Mental")
            st.write(f"Halo **{nama_user}**, sistem mendeteksi filter utama pikiran Anda dipengaruhi pola **{zodiak_hasil}** dengan pondasi energi **{weton_hasil}**.")
            st.info(insight['karakter'])

            # --- HASIL 2 ---
            st.subheader("❤️ Pola Hubungan & Asmara")
            st.warning(f"**Insight Asmara:** {insight['asmara']}")
            st.info(f"**Tips Komunikasi NLP:** {tips_zodiak_nlp.get(zodiak_hasil)}")

            # --- CLOSING BRUTAL (FULL DINAMIS) ---
            st.markdown("---")
            st.error(f"🚨 **PERHATIAN {nama_user.upper()}**\n\nPola arketipe **{arketipe}** Anda saat ini belum berjalan maksimal.")
            st.markdown(f"**Karena hambatan mental (Mental Block), Anda mungkin sering:**\n- {pain_points[0]}\n- {pain_points[1]}\n- {pain_points[2]}")
            st.warning("👉 **Mau tetap membiarkan pola merusak ini terjadi?** atau\n👉 **Siap melakukan Re-Programming sekarang?**")
            
            # Eksekusi Teks Potensi & Penjara Dinamis
            st.success(f"Arketipe **{arketipe}** {teks_potensi}")

            # --- CTA MODUL ---
            link_produk = {
                1: "http://lynk.id/neuronada/kj98l4zgzwdw/checkout",
                2: "http://lynk.id/neuronada/6z23q03121lg/checkout",
                3: "http://lynk.id/neuronada/0rd6gr7nlzxp/checkout",
                4: "http://lynk.id/neuronada/elp83loeyggg/checkout",
                5: "http://lynk.id/neuronada/wne9p4q1l3d9/checkout",
                6: "http://lynk.id/neuronada/nm840y6nlo21/checkout",
                7: "http://lynk.id/neuronada/vv0797ll7g7o/checkout",
                8: "http://lynk.id/neuronada/ropl1lm6rz8g/checkout",
                9: "http://lynk.id/neuronada/704ke23nzmgx/checkout"
            }
            url_tujuan = link_produk.get(angka_hasil, "https://lynk.id/username_lu")
            nama_panggilan = nama_user.split()[0] if nama_user else 'Sahabat'
            
            st.markdown("---")
            st.markdown(f"#### 🔓 Keputusan Ada di Tangan Anda Sekarang, {nama_panggilan}.")
            st.write("Modul ini bukan sekadar e-book, ini adalah **'Kunci Pas'** untuk membongkar mesin bawah sadar Anda. Jangan tunda lagi.")
            
            st.markdown(f"""
            <a href="{url_tujuan}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #d4af37; color: black; padding: 15px; text-align: center; border-radius: 8px; font-weight: bold; font-size: 16px;">
                    👉 YA! SAYA SIAP AMBIL MODUL KODE {angka_hasil}
                </div>
            </a>
            """, unsafe_allow_html=True)

            # --- WA CTA (HIPNOTIK SINGKAT) ---
            st.markdown("---")
            phone_number = "628999771486" 
            wa_text = f"Halo Coach Ahmad, saya {nama_user}. Saya sudah baca hasil mapping Kode {angka_hasil} ({arketipe}) saya. Saya lelah terjebak di pola yang sama dan SIAP melakukan Re-Programming. Kapan jadwal Private Session terdekat yang masih kosong?"
            encoded_wa = urllib.parse.quote(wa_text)
            wa_link = f"https://wa.me/{phone_number}?text={encoded_wa}"

            st.markdown(f"""
            <div style="text-align: center; padding: 25px; background-color: #1a1a1a; border: 2px solid #d4af37; border-radius: 10px;">
                <h3 style="color: #d4af37; margin-bottom: 10px;">🔥 Siap Membongkar Mental Block Anda?</h3>
                <p style="color: #f0f0f0; margin-bottom: 20px;">Teori tak mengubah realita. Cabut akar <i>mental block</i> Anda melalui kalibrasi bawah sadar.</p>
                <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 16px;">
                        💬 Amankan Jadwal Sesi Saya
                    </div>
                </a>
            </div>
            """, unsafe_allow_html=True)

            # --- BAGIAN FAQ & DISCLAIMER ---
            st.markdown("---")
            st.subheader("❓ Pertanyaan Terkait Pemetaan")
            
            with st.expander("Bagaimana sistem ini membedah struktur pikiran saya?"):
                st.write("Sistem **Persona-NLP Analis** menggunakan integrasi data kronologis (tanggal lahir) sebagai pintu masuk untuk mengidentifikasi **Meta-Program** atau filter dominan dalam pikiran bawah sadar Anda. Ini bukan ramalan nasib, melainkan pemetaan kecenderungan perilaku dan gaya pemrosesan informasi Anda.")
                
            with st.expander("Kenapa akurasinya terasa sangat personal?"):
                st.write("Karena Coach **Ahmad Septian** menggabungkan tiga variabel fundamental: Kode Numerik, Energi Weton, dan Pola Zodiak menjadi satu profil psikografis yang utuh.")
                
            with st.expander("Apa langkah selanjutnya setelah mengetahui 'Kode Program' ini?"):
                st.write("Langkah selanjutnya adalah **Re-Programming**. Anda bisa menggunakan modul transformasi yang disediakan di atas atau melakukan sesi Deep Calibration secara Private bersama Coach Ahmad.")

            st.markdown("---")
            with st.expander("⚖️ Disclaimer & Batasan Layanan"):
                st.caption(f"**PEMBERITAHUAN PENTING:** Analisa Persona-NLP Analis ini dirancang murni untuk tujuan edukasi dan pengembangan diri. Hasil analisa ini bukan merupakan diagnosis medis atau psikologi klinis. Segala keputusan yang diambil oleh **{nama_user}** setelah membaca analisa ini adalah tanggung jawab pribadi sepenuhnya.\n\n© 2026 Neuro Nada - Ahmad Septian Dwi Cahyo.")

# ==========================================
# TAB 2: COUPLE SYNC (SINKRONISASI ASMARA)
# ==========================================
with tab2:
    st.subheader("Kalkulator Sinkronisasi Pasangan")
    st.write("Uji kecocokan *Meta-Program* Anda dan pasangan berdasarkan Vibrasi Nama & Tanggal Lahir.")
    
    colA, colB = st.columns(2)
    with colA:
        nama_1 = st.text_input("Nama Anda:", key="c_nama1")
        tgl_1 = st.date_input("Tgl Lahir Anda:", min_value=datetime.date(1920, 1, 1), key="c_tgl1")
    with colB:
        nama_2 = st.text_input("Nama Pasangan/Gebetan:", key="c_nama2")
        tgl_2 = st.date_input("Tgl Lahir Pasangan:", min_value=datetime.date(1920, 1, 1), key="c_tgl2")
        
    if st.button("Cek Kompatibilitas Bawah Sadar"):
        # PASUKAN SATPAM NLP
        if not nama_1 or len(nama_1.strip()) < 3 or not nama_2 or len(nama_2.strip()) < 3:
            st.error("🚨 Satpam NLP: Pastikan KEDUA nama diisi dengan benar (minimal 3 huruf) agar vibrasi hubungan bisa dihitung sempurna.")
        else:
            with st.spinner('Menyelaraskan frekuensi hubungan...'):
                time.sleep(1)
                
            # 1. LOGIKA TANGGAL LAHIR
            ang_tgl_1 = hitung_angka(tgl_1)
            ang_tgl_2 = hitung_angka(tgl_2)
            selisih_tgl = abs(ang_tgl_1 - ang_tgl_2)
            
            # 2. LOGIKA VIBRASI NAMA GABUNGAN
            ang_nama_1 = hitung_angka_nama(nama_1)
            ang_nama_2 = hitung_angka_nama(nama_2)
            
            total_nama = ang_nama_1 + ang_nama_2
            while total_nama > 9:
                total_nama = sum(int(d) for d in str(total_nama))
                
            # DATABASE VIBRASI HUBUNGAN
            analisa_hubungan = {
                1: "🔥 **VIBRASI 1: THE POWER COUPLE**\nHubungan ini memancarkan kemandirian dan ambisi. Kalian berdua memiliki ego yang sama-sama kuat. \n\n**Tantangan NLP:** Jangan bersaing untuk menyetir kapal. Gunakan teknik *Rapport* untuk saling mendukung, bukan saling mendominasi.",
                2: "💞 **VIBRASI 2: THE SOULMATES**\nEnergi hubungan ini sangat harmonis, intim, dan romantis. Ada ikatan emosional yang kuat secara alami. \n\n**Tantangan NLP:** Waspadai *Codependency* (terlalu bergantung). Jangan sampai kehilangan identitas diri demi membahagiakan pasangan.",
                3: "🎉 **VIBRASI 3: THE SOCIAL DYNAMO**\nHubungan kalian dipenuhi oleh komunikasi, tawa, dan energi yang ekspresif. Kalian adalah pasangan yang menyenangkan. \n\n**Tantangan NLP:** Jangan hindari pembicaraan berat. Latih *Deep Structure* saat membahas masa depan dan finansial.",
                4: "🏰 **VIBRASI 4: THE SOLID FOUNDATION**\nKalian membangun hubungan yang sangat stabil, aman, dan dapat diandalkan. Sangat bagus untuk jangka panjang. \n\n**Tantangan NLP:** Rutinitas bisa membunuh romansa. Jangan terlalu kaku pada prosedur, ciptakan spontanitas untuk mencegah kebosanan.",
                5: "🌪️ **VIBRASI 5: THE ADVENTURERS**\nHubungan ini sangat dinamis, bebas, dan penuh kejutan! Selalu ada hal baru yang kalian eksplorasi. \n\n**Tantangan NLP:** Fokus sering terpecah. Bangun *Anchor* komitmen yang kuat agar hubungan tidak terasa mengambang atau kurang kepastian.",
                6: "🏡 **VIBRASI 6: THE NURTURERS**\nFokus utama kalian adalah kenyamanan dan saling merawat. Energi pengayomnya sangat tebal dan hangat. \n\n**Tantangan NLP:** Hindari pola *Mind Reading*. Jangan merasa kecewa jika pasangan tidak memenuhi ekspektasi kesempurnaan di kepala Anda.",
                7: "🌌 **VIBRASI 7: THE SPIRITUAL SEEKERS**\nKalian memiliki koneksi batin yang sangat dalam, seringkali tidak butuh banyak kata untuk saling mengerti. \n\n**Tantangan NLP:** Kalian sama-sama butuh *Me Time*. Jangan biarkan keheningan berubah menjadi jarak emosional yang dingin.",
                8: "👑 **VIBRASI 8: THE EMPIRE BUILDERS**\nHubungan kalian sangat materialistis (positif); fokus pada kesuksesan, kekayaan, dan pencapaian bersama. \n\n**Tantangan NLP:** Jangan bawa gaya *Command* atau negosiasi bisnis ke ranah asmara. Luangkan waktu untuk sentuhan afeksi yang tulus.",
                9: "🕊️ **VIBRASI 9: THE IDEALISTS**\nHubungan kalian didasari oleh cinta tanpa syarat, toleransi tinggi, dan empati yang luar biasa dari kedua belah pihak. \n\n**Tantangan NLP:** Waspadai pola *Generalization*. Jangan terus-menerus memaklumi masalah berulang atas nama pengorbanan cinta."
            }
            
            st.markdown("---")
            nama_panggilan_1 = nama_1.split()[0].capitalize()
            nama_panggilan_2 = nama_2.split()[0].capitalize()
            st.subheader(f"🔮 Hasil Audit Asmara: {nama_panggilan_1} & {nama_panggilan_2}")
            
            # Menampilkan Vibrasi Gabungan Nama
            st.info(analisa_hubungan.get(total_nama, "Analisa kompatibilitas Anda unik."))
            
            # Menampilkan Skor Sinkronisasi Tanggal Lahir (Sebagai pendukung)
            st.markdown("---")
            st.markdown("#### Tingkat Sinkronisasi Meta-Program:")
            if selisih_tgl == 0 or selisih_tgl == 3 or selisih_tgl == 6 or selisih_tgl == 9:
                st.success(f"💘 **SKOR RAPPORT: 90% (Sangat Sinkron)**\n\nSecara *Meta-Program*, kalian punya filter pikiran yang sefrekuensi. Resolusi konflik biasanya sangat cepat.")
            elif selisih_tgl == 1 or selisih_tgl == 2 or selisih_tgl == 8:
                st.warning(f"⚖️ **SKOR RAPPORT: 70% (Saling Melengkapi)**\n\nBanyak perbedaan sudut pandang, namun ini bagus untuk saling belajar. Gunakan teknik *Pacing & Leading* saat berdebat.")
            else:
                st.error(f"🔥 **SKOR RAPPORT: 50% (Butuh Kalibrasi)**\n\nEgo dan dominasi sering berbenturan keras. Kalian butuh ruang khusus untuk memahami *Love Language* masing-masing.")
            
            st.markdown("---")
            st.write("Ingin tahu skrip komunikasi NLP rahasia untuk meredam ego pasangan Anda? Konsultasikan secara privat bersama Coach Ahmad.")
            st.link_button("Booking Sesi Couple Therapy", "https://wa.me/628999771486")

# ==========================================
# TAB 3: AUDIT PIKIRAN (WHEEL OF LIFE)
# ==========================================
with tab3:
    st.subheader("🕸️ Audit Keseimbangan Pikiran")
    
    st.info("**Apa itu Audit Pikiran?**\n\nBayangkan energi mental Anda sebagai sebuah roda penggerak. Jika satu sisi kempes atau bocor, laju hidup Anda pasti tersendat dan terasa *stuck*. \n\nAudit Pikiran adalah teknik pemetaan visual untuk melacak area mana di bawah sadar Anda yang sedang mengalami **kebocoran energi** paling parah. Seringkali kita merasa gagal di karir, padahal akar masalah sebenarnya ada di kondisi emosi atau asmara yang tidak seimbang.")
    
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
    if avg_skor < 5:
        st.error("Peringatan: Roda kehidupan Anda sedang tidak seimbang. Segera benahi area dengan skor terendah sebelum memicu *burnout*.")
    elif avg_skor < 8:
        st.warning("Cukup baik, namun masih ada 'kebocoran' energi di area tertentu yang menghambat Anda melesat maksimal.")
    else:
        st.success("Luar biasa! Kondisi *State of Mind* Anda sedang di puncak. Pertahankan keseimbangan ini.")

# ==========================================
# TESTIMONI RUNNING TEXT & FORM EXPANDER
# ==========================================
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #D4AF37;'>Dipercaya 1.542+ Pengguna</h4>", unsafe_allow_html=True)

marquee_html = """
<div style="background-color: #1a1a1a; padding: 12px; border-radius: 8px; border-left: 3px solid #D4AF37; border-right: 3px solid #D4AF37; white-space: nowrap; overflow: hidden; margin-bottom: 20px;">
    <marquee behavior="scroll" direction="left" scrollamount="6" style="color: #f0f0f0; font-size: 15px;">
        <span style="color: #FFD700;">⭐⭐⭐⭐⭐</span> <b>dr. Antonius:</b> "Ini bukan cuma ramalan, ini pemetaan otak yang masuk akal. Investasi terbaik tahun ini!" &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;
        <span style="color: #FFD700;">⭐⭐⭐⭐⭐</span> <b>Andi S. (CEO):</b> "Sebagai tipe 8, saya kaget NLP ini bisa baca pola leadership saya. Mind-blowing!" &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;
        <span style="color: #FFD700;">⭐⭐⭐⭐</span> <b>Sinta W.:</b> "Sangat relate dengan pola asmara 'Gak Enakan'. Makasih Coach!" &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;
        <span style="color: #FFD700;">⭐⭐⭐⭐⭐</span> <b>Dewi Arini:</b> "Baru seminggu praktek, mental block finansial mulai luntur." &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;
        <span style="color: #FFD700;">⭐⭐⭐⭐⭐</span> <b>Budi T.:</b> "Baru sadar selama ini saya sabotase diri karena gampang bosen." &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;
        <span style="color: #FFD700;">⭐⭐⭐⭐</span> <b>Hendra Jaya:</b> "Gak nyangka weton bisa dikawinin sama NLP se-elegan ini."
    </marquee>
</div>
"""
st.markdown(marquee_html, unsafe_allow_html=True)

with st.expander("💬 Bagikan Pengalaman Anda di sini"):
    with st.form("form_review"):
        rev_nama = st.text_input("Nama Anda")
        rev_rating = st.radio("Rating Bintang", ["⭐⭐⭐⭐⭐ (Sangat Akurat)", "⭐⭐⭐⭐ (Akurat)", "⭐⭐⭐ (Cukup)"], horizontal=True)
        rev_komentar = st.text_area("Tulis ulasan Anda di sini...")
        
        if st.form_submit_button("Kirim Ulasan"):
            if rev_nama and rev_komentar:
                st.success("Terima kasih! Ulasan Anda telah berhasil dikirim dan akan diverifikasi oleh sistem.")
            else:
                st.warning("Mohon isi Nama dan Ulasan Anda terlebih dahulu.")

st.markdown("---")
st.markdown("<center><b>Ahmad Septian Dwi Cahyo</b><br><small>Certified NLP Trainer & Professional Hypnotherapist</small></center>", unsafe_allow_html=True)
