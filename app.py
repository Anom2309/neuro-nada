import streamlit as st
from datetime import date
import urllib.parse

# Konfigurasi Tampilan
st.set_page_config(page_title="Neuro Nada-NLP Analis", page_icon="🧠", layout="centered")

# Visual Estetik
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f7f6;
    }
    .main .block-container {
        background-color: white;
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .btn-premium {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #000 !important;
        padding: 15px 20px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 900;
        display: block;
        text-align: center;
        font-size: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    .btn-premium:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .btn-wa {
        background-color: #25D366;
        color: white !important;
        padding: 12px 20px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        display: block;
        text-align: center;
        font-size: 16px;
        margin-top: 10px;
    }
    .premium-box {
        background-color: #fff9e6;
        border-left: 5px solid #FFD700;
        padding: 20px;
        border-radius: 5px;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧠 Neuro Nada-NLP Analis")
st.markdown("**Temukan Struktur Pikiran & Potensimu di Balik Tanggal Lahir**")
st.write("---")

# Input Data
nama = st.text_input("Siapa nama kamu?", placeholder="Ketik namamu di sini...")
# Tambahan value=None agar kalender kosong dari awal
tgl_lahir = st.date_input("Kapan kamu lahir?", value=None, min_value=date(1930, 1, 1), max_value=date.today())

def hitung_life_path(tgl):
    digits = "".join(filter(str.isdigit, str(tgl)))
    total = sum(int(d) for d in digits)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))
    return total

if st.button("Analisa Karakter Saya Sekarang", type="primary"):
    
    # --- BLOK "SATPAM" VALIDASI ---
    # Jika nama kosong ATAU tanggal lahir kosong, hentikan sistem!
    if not nama or tgl_lahir is None:
        st.error("⚠️ Tunggu dulu! Pikiran bawah sadarmu butuh kejelasan identitas. Tolong isi **Nama** dan **Tanggal Lahirmu** secara manual sebelum kita membedah isi kepalamu.")
        st.stop() # Baris ini bikin kodenya berhenti dan nggak nampilin hasil di bawah
    # ------------------------------

    lp = hitung_life_path(tgl_lahir)
    
    # Database Narasi Deep NLP 
    database = {
        1: {"inti": "🌟 Sang Inisiator Mandiri", "pola": "Pikiranmu beroperasi dengan 'Internal Frame of Reference' yang sangat kuat...", "emosi": "Kamu memiliki daya dorong dan kompetisi yang tinggi...", "saran": "Delegasi bukanlah bentuk kelemahan..."},
        2: {"inti": "🤝 Sang Penyelaras Harmoni", "pola": "Kamu memiliki radar 'External Frame' yang sangat sensitif...", "emosi": "Empatimu adalah kekuatan sekaligus kelemahanmu...", "saran": "Mulailah berlatih 'Ego State' proteksi diri..."},
        3: {"inti": "🎨 Sang Komunikator Kreatif", "pola": "Dalam NLP, kamu adalah tipe 'Options'...", "emosi": "Kamu memiliki energi yang memancar...", "saran": "Ide yang brilian tanpa eksekusi hanyalah hiasan pikiran..."},
        4: {"inti": "🏗️ Sang Arsitek Struktur", "pola": "Pikiranmu berakar kuat pada 'Procedures'...", "emosi": "Kamu adalah sosok yang sangat setia...", "saran": "Latihlah fleksibilitas pikiranmu..."},
        5: {"inti": "🦅 Sang Penjelajah Kebebasan", "pola": "Oksigen bagi otakmu adalah 'Variasi'...", "emosi": "Antusiasmemu sangat magnetis...", "saran": "Kebebasan sejati justru lahir dari kedisiplinan..."},
        6: {"inti": "❤️ Sang Penjaga & Pengayom", "pola": "Filter utamamu adalah 'Others'...", "emosi": "Hatimu sangat luas dan penuh kasih...", "saran": "Kamu tidak bisa menuangkan air dari teko yang kosong..."},
        7: {"inti": "🔍 Sang Pencari Kedalaman", "pola": "Otakmu adalah mesin pemroses data yang sangat mendalam...", "emosi": "Kamu tampak tenang, misterius...", "saran": "Awas jebakan 'Analysis Paralysis'..."},
        8: {"inti": "👑 Sang Pengelola Kekuatan", "pola": "Sistem berpikirmu adalah 'Result-Oriented'...", "emosi": "Tangguh, berwibawa, dan dominan...", "saran": "Kekuasaan yang besar menuntut kerendahan hati..."},
        9: {"inti": "🌍 Sang Humanis Global", "pola": "Pikiranmu beroperasi di level idealisme tinggi...", "emosi": "Kapasitas memaafkanmu sangat luar biasa...", "saran": "Jangan biarkan visi besarmu membuatmu mengabaikan sekitarmu..."},
        11: {"inti": "⚡ Sang Visioner Intuitif", "pola": "Kamu dikaruniai 'High Sensory Acuity'...", "emosi": "Energi mentalmu sangat intens...", "saran": "Intuisimu adalah anugerah, gunakan untuk membimbing..."},
        22: {"inti": "🏛️ Sang Pembangun Utama", "pola": "Kombinasi langka visi setinggi langit dengan kemampuan eksekusi...", "emosi": "Kamu terlihat sangat solid...", "saran": "Kendalikan ekspektasimu. Istirahatlah..."}
    }
    
    res = database.get(lp, {
        "inti": "✨ Karakter Dinamis",
        "pola": "Memiliki kombinasi energi yang unik.",
        "emosi": "Adaptif terhadap lingkungan.",
        "saran": "Teruslah bereksplorasi."
    })

    # 1. TAMPILAN FREE (Umpan)
    st.success(f"Halo **{nama}**, hasil pemetaan pikiranmu adalah:")
    st.markdown(f"### **1. Inti Karakter: {res['inti']}**")
    st.write(f"**2. Pola Pikiran:** {res['pola']}")
    st.write(f"**3. Dinamika Emosi:** {res['emosi']}")
    st.info(f"💡 **Saran Pengembangan:** {res['saran']}")
    
    # 2. TAMPILAN PREMIUM (Cuan) - Kotak Kuning Eksklusif
    link_beli_pdf = "https://lynk.id/neuronada" # <-- GANTI DENGAN LINK KARYAKARSA / LYNK.ID LU NANTI
    
    st.markdown(f"""
        <div class="premium-box">
            <h3 style="color: #B8860B; margin-top: 0;">🔓 Buka 85% Potensi Tersembunyimu</h3>
            <p>Hasil di atas baru <strong>15%</strong> dari cetak biru pikiranmu. Untuk benar-benar melepaskan <i>mental block</i> dan memaksimalkan potensimu, pelajari pedoman lengkapnya.</p>
            <p><strong>Di dalam Premium Report (PDF), kamu akan mendapatkan:</strong></p>
            <ul>
                <li>💎 Karir & Bisnis yang paling cocok untuk Meta Program-mu.</li>
                <li>❤️ Pola Bahasa Cinta (Love Language) & kecocokan pasangan.</li>
                <li>🧠 <b>Worksheet NLP Pribadi</b>: Langkah praktis me-reprogram kelemahanmu menjadi kekuatan.</li>
            </ul>
            <a href="{link_beli_pdf}" target="_blank" class="btn-premium">Unduh Full Report & Worksheet Sekarang</a>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    
    # 3. HIGH TICKET (Sesi Coaching Privat)
    st.subheader("Butuh Bimbingan Langsung?")
    st.write(f"Ingin ngobrol langsung dengan Coach Ahmad untuk sesi *Deep Coaching* atau Hipnoterapi khusus untuk karakter **{res['inti']}**?")
    
    nomor_wa = "6282114982376" # <-- JANGAN LUPA GANTI NOMOR WA LU LAGI YA
    pesan_wa = f"Halo Coach Ahmad, saya {nama}. Hasil Persona-NLP saya adalah {res['inti']}. Saya tertarik untuk ikut sesi privat / konsultasi."
    pesan_encoded = urllib.parse.quote(pesan_wa)
    link_wa = f"https://wa.me/{nomor_wa}?text={pesan_encoded}"

    st.markdown(f'<a href="{link_wa}" target="_blank" class="btn-wa">💬 Chat Coach Ahmad via WhatsApp</a>', unsafe_allow_html=True)
