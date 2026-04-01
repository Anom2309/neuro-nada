import streamlit as st
import datetime
import os
import time
import urllib.parse

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="NLP Deep Analysis | Neuro Nada", 
    page_icon="🧠", 
    layout="centered"
)

# --- CUSTOM CSS (WARNA KUNING UNTUK TOMBOL) ---
st.markdown(
    "<style>\n"
    "div.stButton > button {\n"
    "    background-color: #FFD700 !important;\n"
    "    color: #000000 !important;\n"
    "    font-weight: bold !important;\n"
    "    border: none !important;\n"
    "    padding: 12px 24px !important;\n"
    "    border-radius: 8px !important;\n"
    "    width: 100% !important;\n"
    "    font-size: 16px !important;\n"
    "}\n"
    "div.stButton > button:hover {\n"
    "    background-color: #FFC107 !important;\n"
    "    color: #000000 !important;\n"
    "}\n"
    "</style>", 
    unsafe_allow_html=True
)

# --- SIDEBAR PROMOSI ---
with st.sidebar:
    st.markdown("## 🧠 Sesi Transformasi")
    st.markdown("---")
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

# --- DATABASE ANALISA ---
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

# --- DATABASE CLOSING BRUTAL ---
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

# --- DATABASE PENJARA MENTAL (BARU & DINAMIS) ---
potensi_dinamis = {
    1: "punya potensi kepemimpinan dan daya dobrak luar biasa besar jika ego-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... ambisi ini bisa jadi pola penjara mental yang membelenggu Anda dalam kelelahan kronis seumur hidup.",
    2: "punya potensi penyembuhan dan diplomasi luar biasa besar jika filter 'Gak Enakan'-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... rasa empati ini bisa jadi pola penjara mental yang terus mengorbankan diri Anda seumur hidup.",
    3: "punya potensi persuasi dan kreativitas luar biasa besar jika fokusnya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... ide-ide brilian ini bisa jadi pola penjara mental yang membuat Anda jalan di tempat seumur hidup.",
    4: "punya potensi membangun mahakarya luar biasa besar jika filter kaku-nya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... perfeksionisme ini bisa jadi pola penjara mental yang membelenggu kebahagiaan Anda seumur hidup.",
    5: "punya potensi inovasi dan pencapaian luar biasa besar jika filter kebosanannya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... energi petualang ini bisa jadi pola penjara mental yang membuat Anda kehilangan arah seumur hidup.",
    6: "punya potensi mengayomi dan membina luar biasa besar jika filter 'Mind Reading'-nya dibersihkan.\n
