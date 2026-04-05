import streamlit as st
import datetime
import os
import time
import urllib.parse
import math
import plotly.graph_objects as go
import random

# --- PENGATURAN HALAMAN ---
st.set_page_config(
    page_title="Neuro Nada Deep Analysis", 
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
    # 1. Menampilkan Logo Identitas di Puncak Sidebar (Jika ada)
    if os.path.exists("baru.jpg.png"):
        try:
            st.image("baru.jpg.png", use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True) # Jarak pemanis
        except:
            pass

    st.markdown("### 🎬 Hypno-Video Vault")
    st.caption("Fokuskan pandangan Anda pada video ini sambil menggunakan headphone untuk relaksasi maksimal.")
    
    # Putar video YouTube Coach Ahmad
    st.video("https://youtu.be/kkRcH6aH_lI?si=bpUZF3CWl8DKLw5m")
        
    st.markdown("---")
    
    st.markdown("## 🧠 Sesi Transformasi")
    st.info("**Reset Pola Pikir Anda**\n\nSering merasa terhambat oleh pikiran sendiri? Mari kita lakukan kalibrasi ulang dalam sesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    
    # --- LINK WA UNTUK AMANKAN JADWAL ---
    phone_number_sidebar = "628999771486"
    wa_text_sidebar = "Halo Coach Ahmad, saya tertarik untuk mengamankan jadwal Private Session Hypno-NLP. Apakah masih ada kuota?"
    encoded_wa_sidebar = urllib.parse.quote(wa_text_sidebar)
    wa_link_sidebar = f"https://wa.me/{phone_number_sidebar}?text={encoded_wa_sidebar}"
    
    st.markdown(f"[👉 **Amankan Jadwal Anda**]({wa_link_sidebar})")
    
    st.markdown("---")
    st.success("**📚 Seni Persuasi NLP**\n\nPelajari bagaimana bahasa bekerja di tingkat bawah sadar untuk meningkatkan pengaruh Anda.")
    st.markdown("[👉 **Akses Modul Lengkap**](https://lynk.id/username_lu/ebook-nlp)")
    st.markdown("---")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

# --- INTERFACE UTAMA & BANNER ---
# 1. Tampilkan Banner Full (Jika file banner.jpg ada)
if os.path.exists("banner.jpg"):
    try:
        st.image("banner.jpg", use_container_width=True)
    except:
        st.write("🔄 Sedang memproses visual banner...")

# 2. Teks Judul Utama (Langsung muncul di bawah banner)
st.markdown("<h1 style='text-align: center; margin-top: 10px;'>🧠 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #D4AF37;'>Sistem Pemetaan Bawah Sadar & Akselerasi Potensi Diri</p>", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# TAB 1: PERSONAL MAPPING
# ==========================================
with tab1:
    st.subheader("Bongkar Pola Bawah Sadar Anda")
    nama_user = st.text_input("Nama Lengkap Anda:", placeholder="Masukkan nama panggilan Anda...", key="nama_user_t1")
    tgl_today = datetime.date.today()
    tgl_input = st.date_input("Data Input (Tanggal Lahir):", value=tgl_today, min_value=datetime.date(1920, 1, 1), max_value=tgl_today, format="DD/MM/YYYY", key="tgl_user_t1")

    if st.button("Mulai Pemetaan Internal"):
        if not nama_user or len(nama_user.strip()) < 3:
            st.error("🚨 Satpam NLP: Mohon masukkan nama dengan benar (minimal 3 huruf) agar vibrasi identitas bisa terbaca akurat.")
        elif tgl_input == tgl_today:
            st.error("🚨 Satpam NLP: Mohon masukkan tanggal lahir Anda yang valid, bukan hari ini.")
        else:
            with st.spinner('Melakukan kalibrasi pola pikiran Anda...'):
                time.sleep(1)
                
                angka_hasil = hitung_angka(tgl_input)
                angka_nama = hitung_angka_nama(nama_user)
                _, weton_hasil = get_neptu_weton(tgl_input)
                zodiak_hasil = hitung_zodiak(tgl_input)
                f, e, i, state_harian = bioritme_nlp(tgl_input)
                
                insight = data_analisa.get(angka_hasil)
                arketipe = get_arketipe(angka_hasil)
                pain_points = closing_brutal_dinamis.get(angka_hasil, ["Terjebak dalam pola yang sama", "Merasa stuck", "Butuh perubahan"])
                teks_potensi = potensi_dinamis.get(angka_hasil, "punya potensi luar biasa besar jika filternya dibersihkan.\n\nTapi tanpa di-kalibrasi dan diarahkan... itu bisa jadi pola penjara mental yang membelenggu seumur hidup.")
            
            st.markdown(f"### 📋 Hasil Mapping: {nama_user}")
            st.markdown("---")
            
            st.success(f"📊 **RADAR ENERGI HARI INI:** Anda sedang berada dalam **{state_harian}**.")
            st.caption(f"Kapasitas Fisik: {f}% | Emosional: {e}% | Intelektual: {i}%")
            st.markdown("---")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("KODE NAMA", angka_nama)
            c2.metric("KODE PROGRAM", angka_hasil)
            c3.metric("ENERGI WETON", weton_hasil)
            c4.metric("POLA ZODIAK", zodiak_hasil)
            
            st.markdown("---")
            
            st.subheader("🗣️ Vibrasi Identitas (Nama)")
            st.info(vibrasi_nama_dict.get(angka_nama, "Nama Anda memiliki resonansi energi yang unik."))

            st.subheader("💡 Struktur Karakter & Mental")
            st.write(f"Halo **{nama_user}**, sistem mendeteksi filter utama pikiran Anda dipengaruhi pola **{zodiak_hasil}** dengan pondasi energi **{weton_hasil}**.")
            st.info(insight['karakter'])

            st.subheader("❤️ Pola Hubungan & Asmara")
            st.warning(f"**Insight Asmara:** {insight['asmara']}")
            st.info(f"**Tips Komunikasi NLP:** {tips_zodiak_nlp.get(zodiak_hasil)}")

            st.markdown("---")
            st.error(f"🚨 **PERHATIAN {nama_user.upper()}**\n\nPola arketipe **{arketipe}** Anda saat ini belum berjalan maksimal.")
            st.markdown(f"**Karena hambatan mental (Mental Block), Anda mungkin sering:**\n- {pain_points[0]}\n- {pain_points[1]}\n- {pain_points[2]}")
            st.warning("👉 **Mau tetap membiarkan pola merusak ini terjadi?** atau\n👉 **Siap melakukan Re-Programming sekarang?**")
            
            st.success(f"Arketipe **{arketipe}** {teks_potensi}")

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
# TESTIMONI RUNNING TEXT & FORM EXPANDER
# ==========================================
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #D4AF37;'>Telah Diakses oleh 5.500+ Pengguna</h4>", unsafe_allow_html=True)

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
