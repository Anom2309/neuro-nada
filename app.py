import streamlit as st
import datetime
import os
import time
import urllib.parse
import urllib.request
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

# --- CUSTOM CSS ---
st.markdown(
    """<style>
    div.stButton > button {
        background-color: #FFD700 !important; color: #000000 !important;
        font-weight: bold !important; border: none !important;
        padding: 12px 24px !important; border-radius: 50px !important;
        width: 100% !important; font-size: 16px !important; transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.02); background-color: #FFC107 !important; }
    .ulasan-box {
        background-color: #1e1e1e; padding: 15px; border-radius: 8px;
        border-left: 4px solid #FFD700; margin-bottom: 10px;
    }
    </style>""", unsafe_allow_html=True
)

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("baru.jpg"): st.image("baru.jpg", use_container_width=True)
    st.markdown(f"### {get_greeting()}")
    st.markdown("### 🎬 Hypno-Video Vault")
    st.video("https://youtu.be/kkRcH6aH_lI?si=bpUZF3CWl8DKLw5m")
    st.markdown("---")
    st.info("**Sesi Transformasi Pikiran**\n\nMari kita lakukan kalibrasi ulang dalam sesi *Private Hypno-NLP* bersama **Ahmad Septian**.")
    st.link_button("👉 Amankan Jadwal Anda", "https://wa.me/628999771486?text=Halo%20Coach%20Ahmad,%20saya%20siap%20kalibrasi.")
    st.caption("© 2026 Ahmad Septian Dwi Cahyo")

# --- INTERFACE UTAMA ---
if os.path.exists("banner.jpg"): st.image("banner.jpg", use_container_width=True)
st.markdown("<h1 style='text-align: center; margin-top: 10px;'>🧠 Neuro Nada Deep Analysis</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 18px; color: #D4AF37;'>{get_greeting()}</p>", unsafe_allow_html=True)
st.markdown("---")

# --- LOGIKA MATEMATIKA, WETON & ZODIAK ---
def hitung_angka(tanggal):
    total = sum(int(digit) for digit in tanggal.strftime("%d%m%Y"))
    while total > 9: total = sum(int(digit) for digit in str(total))
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
    if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "Aries", "Keberanian & Eksekusi"
    elif (m == 4 and d >= 20) or (m == 5 and d <= 20): return "Taurus", "Kestabilan & Ketekunan"
    elif (m == 5 and d >= 21) or (m == 6 and d <= 20): return "Gemini", "Komunikasi & Fleksibilitas"
    elif (m == 6 and d >= 21) or (m == 7 and d <= 22): return "Cancer", "Perasaan & Perlindungan"
    elif (m == 7 and d >= 23) or (m == 8 and d <= 22): return "Leo", "Kharisma & Kepemimpinan"
    elif (m == 8 and d >= 23) or (m == 9 and d <= 22): return "Virgo", "Analisa & Kesempurnaan"
    elif (m == 9 and d >= 23) or (m == 10 and d <= 22): return "Libra", "Keseimbangan & Harmoni"
    elif (m == 10 and d >= 23) or (m == 11 and d <= 21): return "Scorpio", "Intensitas & Ketajaman Insting"
    elif (m == 11 and d >= 22) or (m == 12 and d <= 21): return "Sagittarius", "Kebebasan & Visi Luas"
    elif (m == 12 and d >= 22) or (m == 1 and d <= 19): return "Capricorn", "Struktur & Kedisiplinan"
    elif (m == 1 and d >= 20) or (m == 2 and d <= 18): return "Aquarius", "Inovasi & Anti-Mainstream"
    else: return "Pisces", "Empati & Imajinasi Kuat"

# --- DATABASE ANALISA (DIRAPIKAN AGAR TIDAK ERROR COPY-PASTE) ---
data_analisa = {
    1: {
        "karakter": "Anda pada dasarnya adalah sosok perintis. Seringkali Anda merasa gatal kalau harus menunggu orang lain bergerak lebih dulu. Di luar, Anda mungkin terlihat tangguh dan mandiri, tapi di dalam hati, Anda terkadang merasa lelah memikul semuanya sendirian. Pikiran Anda selalu fokus pada tujuan masa depan.", 
        "asmara": "Anda butuh pasangan yang tidak mengekang tapi tetap bisa mengimbangi langkah cepat Anda. Terkadang tanpa sadar bahasa Anda terdengar seperti 'memerintah' karena Anda ingin semuanya efisien. Cobalah sesekali menurunkan ego dan sekadar mendengarkan."
    },
    2: {
        "karakter": "Anda punya bakat alami sebagai 'penyerap energi' orang di sekitar Anda. Anda sangat peka terhadap perubahan suasana hati seseorang meski mereka diam. Kehebatan Anda adalah membuat orang merasa nyaman, namun kelemahan Anda adalah sering mengorbankan perasaan sendiri demi menjaga perasaan orang lain.", 
        "asmara": "Asmara bagi Anda adalah tentang rasa aman secara emosional. Berhentilah menjadi 'Penyelamat' untuk pasangan Anda. Anda berhak menuntut kebahagiaan yang sama rata, bukan sekadar memberi."
    },
    3: {
        "karakter": "Pikiran Anda sangat kaya akan imajinasi dan skenario. Anda sering memikirkan banyak ide brilian sekaligus, meski kadang kesulitan menyelesaikannya satu per satu. Anda pandai mencairkan suasana, tapi saat sedang sendirian, Anda sering memutar ulang percakapan masa lalu di kepala Anda.", 
        "asmara": "Anda butuh koneksi yang menyenangkan dan tidak membosankan. Kebisuan adalah hal yang paling menyiksa Anda. Cari pasangan yang bisa menjadi tempat Anda bercerita tanpa dihakimi."
    },
    4: {
        "karakter": "Anda adalah perencana yang detail. Anda benci ketidakpastian dan kejutan yang tidak direncanakan. Pikiran Anda bekerja seperti laci-laci yang rapi. Orang mungkin melihat Anda kaku, padahal itu adalah cara bawah sadar Anda untuk memastikan semuanya aman dan terkendali.", 
        "asmara": "Anda sangat setia pada komitmen, namun terkadang lupa untuk memberikan 'bumbu' romantis karena terlalu fokus pada hal logis dan praktis. Ingat, asmara itu urusan hati, bukan sekadar hitung-hitungan logika."
    },
    5: {
        "karakter": "Anda benci rutinitas yang monoton. Jiwa Anda butuh ruang gerak yang luas. Anda hebat dalam mencari celah di saat orang lain buntu. Namun di sisi lain, karena terlalu sering berpindah fokus, Anda kadang kehilangan arah dan bingung sebenarnya apa yang paling Anda cari dalam hidup ini.", 
        "asmara": "Kata kunci untuk Anda adalah 'Kebebasan'. Hubungan yang terlalu menuntut akan membuat Anda diam-diam ingin melarikan diri. Anda butuh pasangan yang terasa seperti sahabat petualang."
    },
    6: {
        "karakter": "Pusat dari hidup Anda adalah keluarga dan orang-orang yang Anda sayangi. Anda seringkali menempatkan kebutuhan orang lain di atas kebutuhan Anda sendiri. Anda punya standar tanggung jawab yang sangat tinggi, yang terkadang membuat Anda gampang kecewa kalau orang lain tidak melakukan hal yang sama.", 
        "asmara": "Anda sangat peduli, namun terkadang kepedulian Anda terasa seperti sedang 'mengatur'. Belajarlah untuk berhenti menebak-nebak apa yang dipikirkan pasangan. Tanyakan saja langsung padanya."
    },
    7: {
        "karakter": "Anda punya intuisi yang sangat tajam; seringkali firasat Anda terbukti benar. Anda bukan tipe orang yang mudah percaya begitu saja pada omongan orang (skeptis). Anda butuh banyak waktu sendirian ('Me Time') untuk menata ulang energi Anda setelah terlalu banyak interaksi sosial.", 
        "asmara": "Anda cukup sulit ditebak dan susah terbuka 100% pada awalnya. Anda mencari pasangan yang obrolannya 'nyambung' sampai ke level yang dalam, bukan sekadar basa-basi cinta."
    },
    8: {
        "karakter": "Anda punya dorongan kuat untuk sukses dan memegang kendali. Anda tidak suka diremehkan. Di balik sikap Anda yang terlihat tegas dan logis, sebenarnya ada keinginan kuat untuk diakui dan dihargai atas pencapaian Anda. Anda tahan banting terhadap tekanan mental.", 
        "asmara": "Jangan bawa kebiasaan 'negosiasi keras' Anda dari tempat kerja ke dalam hubungan rumah tangga. Pasangan Anda butuh disentuh hatinya dengan kelembutan, bukan ditundukkan dengan logika."
    },
    9: {
        "karakter": "Anda sering merasa menjadi 'jiwa tua' (old soul). Anda peduli pada hal-hal kemanusiaan dan punya standar moral yang tinggi. Anda memandang masalah dari sudut pandang yang sangat luas. Masalahnya, Anda sering merasa kecewa melihat realita dunia yang tidak seindah ekspektasi Anda.", 
        "asmara": "Anda mencari cinta yang ideal, sebuah koneksi jiwa yang murni. Namun ingatlah bahwa manusia tempatnya salah. Menerima ketidaksempurnaan pasangan adalah kunci kedamaian Anda."
    }
}

closing_brutal = {
    1: ["Sering overthinking karena merasa hasil kerja 'belum sempurna'", "Memendam lelah sendirian karena sulit minta tolong orang lain", "Membangun tembok pertahanan diri agar tidak terlihat lemah"],
    2: ["Terjebak memuaskan orang lain sampai lupa membahagiakan diri sendiri", "Sulit bilang 'TIDAK' dan memendam amarah yang berujung stres fisik", "Sering mengalah hanya agar tidak terjadi keributan"],
    3: ["Menyembunyikan rasa cemas dan gelisah di balik senyuman", "Mudah kehilangan motivasi jika tidak ada apresiasi", "Pikiran yang terlalu penuh sering bikin susah tidur"],
    4: ["Sangat gampang stres dan uring-uringan kalau rencana mendadak berubah", "Terjebak di rutinitas karena takut mengambil resiko baru", "Sering dianggap kurang peka perasaannya oleh orang terdekat"],
    5: ["Cepat bosan yang membuat banyak hal berhenti di tengah jalan", "Kelelahan saraf karena otak tidak pernah benar-benar berhenti berpikir", "Terkadang merasa hampa karena kehilangan pijakan hidup yang pasti"],
    6: ["Kehabisan energi secara drastis (Burnout) karena terlalu sibuk mengurus hidup orang lain", "Cenderung Over-Protective dan cemas berlebihan", "Merasa bersalah luar biasa saat memakai uang/waktu untuk kesenangan pribadi"],
    7: ["Terjebak dalam labirin analisa pikiran sendiri tanpa eksekusi nyata", "Sering merasa kesepian dan merasa tidak ada yang benar-benar memahami Anda", "Mencurigai niat baik orang lain akibat luka masa lalu"],
    8: ["Sering merasa hampa justru ketika target sudah tercapai", "Sangat sulit memaafkan pengkhianatan", "Mengabaikan alarm tubuh yang sudah kelelahan demi sebuah ambisi"],
    9: ["Terlalu sering memaklumi orang toxic dengan alasan 'kasihan'", "Sering patah hati karena berekspektasi terlalu tinggi pada manusia", "Merasa menanggung beban dunia yang bukan tanggung jawab Anda"]
}

# --- MENU TABS ---
tab1, tab2, tab3 = st.tabs(["👤 Personal Mapping", "👩‍❤️‍👨 Couple Sync", "🕸️ Audit Pikiran"])

# ==========================================
# TAB 1: PERSONAL MAPPING (WETON + ZODIAK + NLP)
# ==========================================
with tab1:
    st.subheader("Bongkar Pola Bawah Sadar Anda")
    nama_user = st.text_input("Nama Lengkap:", key="t1_nama", placeholder="Siapa nama Anda?")
    
    batas_bawah = datetime.date(1920, 1, 1)
    batas_atas = datetime.date.today()
    tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date(1995, 1, 1), min_value=batas_bawah, max_value=batas_atas, format="DD/MM/YYYY")

    if st.button("Mulai Kalibrasi"):
        if len(nama_user) > 2 and tgl_input != datetime.date.today():
            with st.spinner('Membongkar program pikiran bawah sadar...'):
                time.sleep(1.5)
                kode_p = hitung_angka(tgl_input)
                nep, wet = get_neptu_weton(tgl_input)
                zod_nama, zod_sifat = get_zodiak(tgl_input)
                insight = data_analisa.get(kode_p)
                pains = closing_brutal.get(kode_p)
            
            st.balloons()
            st.markdown(f"### Meta-Profil: {nama_user}")
            st.info(f"**Zodiak:** {zod_nama} | **Weton:** {wet} | **Kode Core:** {kode_p}")
            
            st.subheader("💡 Korelasi Karakter Anda")
            sintesis = f"Kombinasi energi **{zod_nama}** ({zod_sifat}) yang berpadu dengan akar karakter weton **{wet}**, menciptakan struktur pikiran yang sangat khas dalam diri Anda. "
            sintesis += insight['karakter']
            st.write(sintesis)
            
            st.subheader("❤️ Pola Asmara & Hubungan")
            st.warning(insight['asmara'])
            
            st.markdown("---")
            st.error(f"🚨 **SISI GELAP BAWAH SADAR (Shadow Self):**\nDi balik kehebatan Anda, hal-hal inilah yang diam-diam sering menggerogoti energi mental Anda:\n- {pains[0]}\n- {pains[1]}\n- {pains[2]}")
            
            st.link_button(f"🔓 Buka Solusi & Terapi Khusus Karakter Anda", f"https://lynk.id/neuronada/checkout-kode-{kode_p}")
        else:
            st.warning("Mohon ketik nama lengkap Anda dengan benar.")

# ==========================================
# TAB 2: COUPLE SYNC (DEEP ANALYSIS)
# ==========================================
with tab2:
    st.subheader("Sinkronisasi Gelombang Pasangan")
    st.caption("Menganalisa benturan logika dan resonansi emosi Anda berdua.")
    c1, c2 = st.columns(2)
    with c1: 
        n1 = st.text_input("Nama Anda", key="n1")
        d1 = st.date_input("Lahir Anda", value=datetime.date(1995, 1, 1), min_value=batas_bawah, max_value=batas_atas, key="d1")
    with c2: 
        n2 = st.text_input("Nama Pasangan", key="n2")
        d2 = st.date_input("Lahir Pasangan", value=datetime.date(1995, 1, 1), min_value=batas_bawah, max_value=batas_atas, key="d2")
    
    if st.button("Audit Keselarasan Asmara"):
        if n1 and n2 and d1 != datetime.date.today():
            with st.spinner('Menghitung benturan Logika & Emosi...'):
                time.sleep(1.5)
                
                nep1, weton1 = get_neptu_weton(d1)
                nep2, weton2 = get_neptu_weton(d2)
                res = (nep1 + nep2) % 8
                
                hasil_weton_dinamis = {
                    1: [("💔 PEGAT (Rentan Gesekan)", "Terdapat perbedaan pola pikir yang cukup tajam. Ego sering berbenturan saat berdebat. Solusinya: Jangan membalas emosi dengan emosi. Dengarkan dulu, baru beri penjelasan logika.")],
                    2: [("👑 RATU (Aura Harmonis)", "Kalian memancarkan aura pasangan yang serasi dan disegani lingkungan. Namun hati-hati, jangan sampai ada yang merasa terlalu mendominasi atau mengatur pasangan.")],
                    3: [("💞 JODOH (Resonansi Inti)", "Koneksi batin kalian sangat kuat. Kadang kalian bisa tahu apa yang dipikirkan pasangan hanya dari tatapan matanya. Saling melengkapi kelebihan dan kekurangan secara natural.")],
                    4: [("🌱 TOPO (Fase Pendewasaan)", "Hubungan ini akan memaksa kalian berdua untuk menjadi lebih dewasa. Awalnya mungkin sering ada salah paham kecil, namun jika dilewati, ikatan kalian akan sekuat baja.")],
                    5: [("💰 TINARI (Magnet Rezeki)", "Kalau kalian bersatu dan kompak, jalan mencari rezeki terasa lebih gampang. Otak kalian saling melengkapi untuk membangun masa depan. Hati-hati, jangan sampai lupa waktu romantis karena terlalu sibuk bekerja.")],
                    6: [("⚡ PADU (Beda Frekuensi)", "Kalian sering meributkan hal-hal sepele karena cara kalian memandang masalah berbeda 180 derajat. Yang satu mengandalkan perasaan, yang satu pakai logika dingin. Turunkan gengsi.")],
                    7: [("👁️ SUJANAN (Ujian Percaya)", "Rentan terjadi salah paham, asumsi negatif, dan kecemburuan. Kalian butuh ruang aman untuk saling jujur tanpa saling menghakimi. Jangan bawa bayang-bayang masa lalu ke hubungan ini.")],
                    0: [("🕊️ PESTHI (Ketenangan Batin)", "Hubungan yang adem ayem dan stabil. Kalian berhasil menjadi tempat bersandar satu sama lain saat lelah. Tapi awas, rutinitas yang monoton bisa mematikan gairah cinta.")]
                }
                
                judul_dinamis, desc_dinamis = random.choice(hasil_weton_dinamis.get(res, hasil_weton_dinamis[0]))
                
                ang_tgl_1 = hitung_angka(d1)
                ang_tgl_2 = hitung_angka(d2)
                selisih_tgl = abs(ang_tgl_1 - ang_tgl_2)
                
                pesan_rapport = {
                    0: "💘 **SKOR KECOCOKAN NLP: 95% (Sangat Identik)**\nCara kalian berpikir nyaris sama. Kalian memandang dunia dengan kacamata yang serupa.",
                    3: "💘 **SKOR KECOCOKAN NLP: 90% (Sangat Sinkron)**\nKalian gampang nyambung. Mudah memahami bahasa tubuh dan maksud hati satu sama lain.",
                    6: "💘 **SKOR KECOCOKAN NLP: 88% (Saling Melengkapi)**\nKoneksi alam bawah sadar yang matang. Saling menutupi kekurangan tanpa merasa direndahkan.",
                    9: "💘 **SKOR KECOCOKAN NLP: 92% (Tarik-Menarik Kuat)**\nAda ikatan magnetis di luar logika rasional yang membuat kalian selalu ingin kembali bersama.",
                    1: "⚖️ **SKOR KECOCOKAN NLP: 75% (Butuh Pengertian Lebih)**\nKalian saling melengkapi, tapi sering capek karena harus menerjemahkan maksud pasangan. Belajar pakai bahasa kasihnya.",
                    2: "⚖️ **SKOR KECOCOKAN NLP: 70% (Beda Sudut Pandang)**\nKarakter dasar kalian lumayan bertolak belakang. Jangan memaksakan pasangan untuk berpikir dengan cara Anda.",
                    8: "⚖️ **SKOR KECOCOKAN NLP: 78% (Dinamis & Ekstrim)**\nKadang mesra banget, kadang bisa dingin banget. Jangan biarkan emosi sesaat merusak pondasi hubungan kalian.",
                }
                rapport_text = pesan_rapport.get(selisih_tgl, "🔥 **SKOR KECOCOKAN NLP: 50% (Sering Miskomunikasi)**\nSinyal bahaya. Kalian sering bicara pakai bahasa yang nggak dimengerti pasangan. Butuh pendampingan ahli.")

            st.markdown("---")
            st.subheader(f"🔮 Hasil Audit Asmara: {n1.split()[0].capitalize()} & {n2.split()[0].capitalize()}")
            st.info(f"#### {judul_dinamis}\n{desc_dinamis}")
            
            st.markdown("#### Tingkat Sinkronisasi Pikiran Bawah Sadar:")
            if selisih_tgl in [0, 3, 6, 9]: 
                st.success(rapport_text)
            elif selisih_tgl in [1, 2, 8]: 
                st.warning(rapport_text)
            else: 
                st.error(rapport_text)
            
            st.markdown("---")
            st.link_button("Urai Benang Kusut Hubungan Bersama Coach Ahmad", "https://wa.me/628999771486")
        else: 
            st.warning("Isi nama dan tanggal lahir berdua dengan lengkap.")

# ==========================================
# TAB 3: AUDIT PIKIRAN (DEEP RADAR)
# ==========================================
with tab3:
    st.subheader("🕸️ Audit Keseimbangan Pikiran (Wheel of Life)")
    st.caption("Jujurlah pada diri sendiri. Geser titik di bawah ini sesuai dengan kepuasan batin Anda saat ini (1 = Sangat Kacau, 10 = Sangat Sempurna).")
    
    kategori = ['Mental & Emosi', 'Karir & Keuangan', 'Asmara & Hubungan', 'Spiritual & Kedamaian', 'Fisik & Kesehatan']
    skor = [st.slider(k, 1, 10, 5) for k in kategori]
    
    if st.button("Bangkitkan Radar Analisa"):
        fig = go.Figure(data=go.Scatterpolar(
            r=skor+[skor[0]], 
            theta=['Mental','Karir','Asmara','Spiritual','Fisik','Mental'], 
            fill='toself',
            line=dict(color='#FFD700'),
            marker=dict(color='#FFD700')
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFF')
        )
        st.plotly_chart(fig)
        
        avg = sum(skor)/5
        idx_terendah = skor.index(min(skor))
        idx_tertinggi = skor.index(max(skor))
        area_bocor = kategori[idx_terendah]
        area_kuat = kategori[idx_tertinggi]
        
        st.markdown("### Diagnosa Bawah Sadar Anda:")
        if avg < 5:
            st.error(f"🚨 **WARNING (Kelelahan Sistemik):** Baterai kehidupan Anda sedang *lowbat*. Terlalu banyak pikiran dan tekanan membuat Anda kesulitan fokus.")
        elif avg < 8:
            st.warning(f"⚖️ **ZONA AMAN (Stagnan):** Hidup Anda berjalan baik-baik saja, tapi Anda tahu bahwa Anda punya potensi untuk mencapai hal yang jauh lebih besar dari ini.")
        else:
            st.success(f"🔥 **PEAK STATE (Gelombang Puncak):** Luar biasa! Seluruh energi kehidupan Anda sedang sinkron. Ini adalah saat terbaik untuk mengambil keputusan besar!")
            
        st.info(f"**Titik Kritis (Kebocoran Energi):** Sektor **{area_bocor}** Anda butuh perhatian serius (Skor {min(skor)}). Dalam ilmu pikiran, stres di satu titik lama-lama akan merembet menghancurkan area lainnya jika dibiarkan!\n\n**Solusi:** Gunakan rasa syukur dan energi positif dari sektor **{area_kuat}** Anda untuk perlahan membenahi area yang sedang bocor tadi.")

# ==========================================
# ULASAN DATABASE GOOGLE SHEETS (REAL-TIME)
# ==========================================
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #D4AF37;'>Jejak Transformasi</h3>", unsafe_allow_html=True)
st.write("Bukti nyata mereka yang telah membongkar dan mereset pola bawah sadarnya bersama Neuro Nada.")

daftar_ulasan = ambil_ulasan()

if not daftar_ulasan:
    st.caption("Belum ada ulasan, atau koneksi ke server sedang menyesuaikan.")
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

with st.expander("💬 Tinggalkan Jejak Transformasi Anda"):
    with st.form("form_review"):
        rev_nama = st.text_input("Nama Anda (Boleh Inisial)")
        rev_rating = st.radio("Seberapa akurat tebakan karakter ini?", ["⭐⭐⭐⭐⭐ (Sangat Akurat)", "⭐⭐⭐⭐ (Akurat)", "⭐⭐⭐ (Cukup)"], horizontal=True)
        rev_komentar = st.text_area("Ceritakan perasaan atau insight baru yang Anda temukan di sini...")
        
        if st.form_submit_button("Kirim Kesaksian"):
            if rev_nama and rev_komentar:
                sukses = kirim_ulasan(rev_nama, rev_rating.split(" ")[0], rev_komentar)
                if sukses:
                    st.success("Terkirim! Kesaksian Anda langsung ter-update detik ini juga.")
                    time.sleep(1) 
                    st.rerun() 
                else:
                    st.error("Koneksi ke database sedang terganggu. Coba sebentar lagi.")
            else:
                st.warning("Mohon isi Nama dan Cerita Anda sebelum mengirim.")

st.markdown("---")
st.markdown("<center><b>Neuro Nada Academy</b><br><small>Ahmad Septian Dwi Cahyo • Master Hypnotherapy & NLP Trainer</small></center>", unsafe_allow_html=True)
