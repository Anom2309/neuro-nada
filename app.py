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

def hitung_angka(tanggal):
    tgl_str = tanggal.strftime("%d%m%Y")
    total = sum(int(digit) for digit in tgl_str)
    while total > 9: total = sum(int(digit) for digit in str(total))
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

# --- INTERFACE UTAMA ---
st.title("🧠 NLP Deep Analysis")
st.subheader("Membedah Struktur Pikiran & Potensi Diri")
st.write("Sinkronisasi data personal Anda untuk memetakan program bawah sadar dalam aspek Karakter dan Asmara.")
st.markdown("---")

nama_user = st.text_input("Siapa nama lengkap Anda?", placeholder="Masukkan nama panggilan Anda...")
tgl_today = datetime.date.today()
tgl_input = st.date_input("Data Input (Tanggal Lahir):", value=tgl_today, min_value=datetime.date(1920, 1, 1), max_value=tgl_today, format="DD/MM/YYYY")

st.markdown("---")

if st.button("Mulai Pemetaan Internal"):
    if not nama_user:
        st.error("🚨 Peringatan: Nama diperlukan untuk proses identifikasi pola.")
    elif tgl_input == tgl_today:
        st.error("🚨 Peringatan: Mohon masukkan tanggal lahir Anda yang valid.")
    else:
        with st.spinner('Melakukan kalibrasi pola pikiran Anda...'):
            time.sleep(1)
            
            angka_hasil = hitung_angka(tgl_input)
            weton_hasil = hitung_weton(tgl_input)
            zodiak_hasil = hitung_zodiak(tgl_input)
            insight = data_analisa.get(angka_hasil)
            arketipe = get_arketipe(angka_hasil)
            pain_points = closing_brutal_dinamis.get(angka_hasil, ["Terjebak dalam pola yang sama", "Merasa stuck", "Butuh perubahan"])
        
        st.markdown(f"### 📋 Hasil Mapping: {nama_user}")
        st.markdown("---")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("KODE PROGRAM", angka_hasil)
        c2.metric("ENERGI WETON", weton_hasil)
        c3.metric("POLA ZODIAK", zodiak_hasil)
        
        st.markdown("---")
        
        # --- HASIL 1 ---
        st.subheader("💡 Struktur Karakter & Mental")
        st.write(f"Halo **{nama_user}**, sistem mendeteksi filter utama pikiran Anda dipengaruhi pola **{zodiak_hasil}** dengan pondasi energi **{weton_hasil}**.")
        st.info(insight['karakter'])

        # --- HASIL 2 ---
        st.subheader("❤️ Pola Hubungan & Asmara")
        st.warning(f"**Insight Asmara:** {insight['asmara']}")
        st.info(f"**Tips Komunikasi NLP:** {tips_zodiak_nlp.get(zodiak_hasil)}")

        # --- CLOSING BRUTAL ---
        st.markdown("---")
        st.error(f"🚨 **PERHATIAN {nama_user.upper()}**\n\nPola arketipe **{arketipe}** Anda saat ini belum berjalan maksimal.")
        st.markdown(f"**Karena hambatan mental (Mental Block), Anda mungkin sering:**\n- {pain_points[0]}\n- {pain_points[1]}\n- {pain_points[2]}")
        st.warning("👉 **Mau tetap membiarkan pola merusak ini terjadi?** atau\n👉 **Siap melakukan Re-Programming sekarang?**")
        st.success(f"Arketipe **{arketipe}** punya potensi luar biasa besar jika filternya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan...\nItu bisa jadi pola penjara mental yang membelenggu seumur hidup.")

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

        # --- WA CTA ---
        st.markdown("---")
        phone_number = "628999771486" 
        wa_text = f"Halo Coach Ahmad, saya {nama_user}. Saya sudah baca hasil mapping Kode {angka_hasil} ({arketipe}) saya. Saya lelah terjebak di pola yang sama dan SIAP melakukan Re-Programming. Kapan jadwal Private Session terdekat yang masih kosong?"
        encoded_wa = urllib.parse.quote(wa_text)
        wa_link = f"https://wa.me/{phone_number}?text={encoded_wa}"

        st.markdown(f"""
        <div style="text-align: center; padding: 25px; background-color: #1a1a1a; border: 2px solid #d4af37; border-radius: 10px;">
            <h3 style="color: #d4af37; margin-bottom: 10px;">🔥 Butuh Perubahan Instan & Permanen?</h3>
            <p style="color: #f0f0f0; margin-bottom: 20px;">Membaca modul adalah langkah pertama. Tapi jika Anda butuh pembedahan mental yang dibimbing langsung 1-on-1...</p>
            <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 16px;">
                    💬 Amankan Jadwal Private Sesi Saya
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)

        # --- BAGIAN FAQ & DISCLAIMER (DIKEMBALIKAN FULL) ---
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

st.markdown("---")
st.markdown("<center><b>Ahmad Septian Dwi Cahyo</b><br><small>Certified NLP Trainer & Professional Hypnotherapist</small></center>", unsafe_allow_html=True)
