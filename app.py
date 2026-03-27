import streamlit as st
from datetime import datetime

# Konfigurasi Tampilan
st.set_page_config(page_title="Persona-NLP Analis", page_icon="🧠")

st.title("🧠 Persona-NLP Analis")
st.subheader("Temukan Pola Pikiran di Balik Tanggal Lahirmu")
st.write("st.subheader("💡 Langkah Selanjutnya untuk Kamu")
    st.write(f"Hasil di atas adalah gambaran permukaan pola pikiranmu. Ingin membedah hambatan diri atau memaksimalkan potensi {res['inti']} secara lebih mendalam?")
    
    # Pesan otomatis yang akan terkirim ke WA kamu
    pesan_wa = f"Halo Mas Ahmad, saya {nama}. Saya baru saja mencoba Persona-NLP Analis dan hasilnya adalah {res['inti']}. Saya ingin diskusi lebih dalam tentang sesi coaching/hipnoterapi."
    
    # Encode pesan agar bisa dibaca URL (mengganti spasi jadi %20)
    import urllib.parse
    pesan_encoded = urllib.parse.quote(pesan_wa)
    
    # Ganti nomor di bawah dengan nomor WA kamu (awali dengan 62)
    nomor_wa = "6281234567890" # <-- GANTI DENGAN NOMOR KAMU
    link_wa = f"https://wa.me/{nomor_wa}?text={pesan_encoded}"

    if st.button("Konsultasi Deep Coaching via WhatsApp"):
        st.markdown(f'<p style="text-align:center;"><a href="{link_wa}" target="_blank" style="background-color:#25D366;color:white;padding:10px 20px;border-radius:10px;text-decoration:none;font-weight:bold;">KLIK DI SINI UNTUK CHAT SEKARANG</a></p>', unsafe_allow_html=True)")

# Input Data
nama = st.text_input("Siapa nama kamu?", placeholder="Ahmad...")
tgl_lahir = st.date_input("Kapan kamu lahir?", min_value=datetime(1950, 1, 1))

def hitung_life_path(tgl):
    digits = "".join(filter(str.isdigit, str(tgl)))
    total = sum(int(d) for d in digits)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(d) for d in str(total))
    return total

if st.button("Analisa Karakter Saya"):
    lp = hitung_life_path(tgl_lahir)
    
    # Database Narasi (Contoh untuk Angka 1 & 7)
    database = {
        1: {
            "inti": "Pemimpin yang Berdikari",
            "pola": "Kamu cenderung proaktif dengan 'Internal Frame of Reference' yang kuat. Kamu tahu apa yang kamu mau tanpa perlu validasi berlebih.",
            "emosi": "Mandiri, namun terkadang merasa kesepian di puncak.",
            "saran": "Belajarlah bahwa delegasi bukan berarti kehilangan kontrol, tapi meluaskan pengaruh."
        },
        7: {
            "inti": "Pencari Kedalaman Jati Diri",
            "pola": "Otakmu bekerja secara reflektif. Kamu tidak puas dengan permukaan; kamu harus menemukan 'mengapa' di balik segalanya.",
            "emosi": "Introspektif, butuh ruang sendiri (me-time) untuk mengisi energi.",
            "saran": "Jangan biarkan analisismu berubah menjadi kelumpuhan. Terkadang, jawaban ditemukan dalam tindakan, bukan pemikiran."
        }
        # Tambahkan angka 2-6, 8, 9, 11, 22 di sini
    }
    
    res = database.get(lp, {
        "inti": "Karakter Unik",
        "pola": "Memiliki kombinasi energi yang dinamis.",
        "emosi": "Adaptif terhadap lingkungan.",
        "saran": "Teruslah bereksplorasi dengan potensi dirimu."
    })

    # Output Display
    st.success(f"Halo {nama}, hasil analisamu adalah:")
    st.markdown(f"### **1. Inti Karakter: {res['inti']}**")
    st.write(f"**2. Pola Pikiran:** {res['pola']}")
    st.write(f"**3. Emosi & Relasi:** {res['emosi']}")
    st.info(f"💡 **Saran Pengembangan:** {res['saran']}")
    
    st.write("---")
    st.caption("Analisis ini bersifat reflektif berdasarkan pola psikologi & numerologi ringan.")
    database = {
    1: {
        "inti": "Sang Inisiator Mandiri",
        "pola": "Memiliki 'Internal Frame of Reference' yang kuat. Kamu adalah pengemudi bagi hidupmu sendiri, cenderung proaktif, dan sulit menerima perintah jika tidak logis bagimu.",
        "emosi": "Mandiri dan kompetitif. Terkadang merasa harus memikul semuanya sendirian karena standar tinggi yang kamu miliki.",
        "saran": "Belajarlah bahwa delegasi adalah bentuk perluasan pengaruh, bukan kehilangan kendali. Izinkan orang lain membantu perjalananmu."
    },
    2: {
        "inti": "Sang Penyelaras Harmoni",
        "pola": "Sangat peka terhadap lingkungan ('External Frame'). Kamu ahli dalam melihat detail kecil dan nuansa emosi orang lain yang sering dilewatkan orang.",
        "emosi": "Empati tinggi, namun rentan terseret arus emosi orang lain. Kamu butuh kedamaian di lingkungan sekitarmu.",
        "saran": "Belajarlah untuk berkata 'tidak' tanpa merasa bersalah. Menjaga batas diri adalah cara terbaik untuk membantu orang lain secara tulus."
    },
    3: {
        "inti": "Sang Komunikator Kreatif",
        "pola": "Berpikir secara 'Options' (banyak peluang). Otakmu adalah pabrik ide yang tidak pernah tidur. Kamu melihat dunia sebagai panggung ekspresi.",
        "emosi": "Ceria dan ekspresif, namun sering mengalami 'up and down' emosional yang drastis jika ide-idemu tidak tersalurkan.",
        "saran": "Fokuslah pada penyelesaian (finishing). Ide hebat tanpa eksekusi hanyalah hiasan pikiran. Pilih satu, jalankan sampai tuntas."
    },
    4: {
        "inti": "Sang Arsitek Struktur",
        "pola": "Sangat kuat dalam 'Procedures'. Kamu merasa aman saat ada sistem, aturan, dan rencana yang jelas. Detail adalah sahabat karibmu.",
        "emosi": "Setia dan stabil. Kamu adalah jangkar bagi orang-orang di sekitarmu, namun terkadang sulit beradaptasi dengan perubahan mendadak.",
        "saran": "Berikan ruang untuk ketidakpastian. Terkadang, keajaiban hidup terjadi di luar rencana yang telah kamu susun dengan rapi."
    },
    5: {
        "inti": "Sang Penjelajah Kebebasan",
        "pola": "Variasi adalah oksigenmu. Kamu cenderung menghindari batasan dan selalu mencari pengalaman baru. Sangat adaptif dalam berbagai situasi.",
        "emosi": "Antusias dan magnetis. Namun, rasa bosan adalah musuh terbesarmu yang sering membuatmu meninggalkan hal-hal penting di tengah jalan.",
        "saran": "Kebebasan sejati ditemukan dalam disiplin. Dengan sedikit struktur, petualanganmu akan menghasilkan dampak yang lebih permanen."
    },
    6: {
        "inti": "Sang Penjaga & Pengayom",
        "pola": "Fokus pada 'Others' (orang lain). Kamu memiliki insting alami untuk merawat, melindungi, dan menciptakan kenyamanan bagi orang tercinta.",
        "emosi": "Penuh kasih, namun sering merasa bertanggung jawab atas kebahagiaan orang lain secara berlebihan.",
        "saran": "Kamu tidak bisa menuang air dari cangkir yang kosong. Rawatlah dirimu sendiri terlebih dahulu sebelum kamu merawat dunia."
    },
    7: {
        "inti": "Sang Pencari Kedalaman",
        "pola": "Refleksi internal yang sangat dalam. Kamu adalah 'The Analyst' yang selalu mencari makna di balik fakta. Butuh kesendirian untuk memproses data.",
        "emosi": "Tenang dan misterius. Kamu tidak mudah percaya pada permukaan, karena bagimu kebenaran ada di kedalaman.",
        "saran": "Jangan biarkan analisismu menjadi kelumpuhan (analysis paralysis). Terkadang, jawaban terbaik ditemukan melalui tindakan nyata, bukan perenungan."
    },
    8: {
        "inti": "Sang Pengelola Kekuatan",
        "pola": "Hasil adalah segalanya ('Result Oriented'). Kamu memiliki kemampuan melihat gambaran besar dan mengorganisir sumber daya untuk mencapainya.",
        "emosi": "Tangguh dan berwibawa. Namun, kamu sering lupa untuk merayakan kemenangan kecil karena selalu mengejar target berikutnya.",
        "saran": "Kekuasaan yang besar menuntut kerendahan hati yang besar pula. Hubungkan ambisimu dengan nilai-nilai kemanusiaan yang lebih luas."
    },
    9: {
        "inti": "Sang Humanis Global",
        "pola": "Berpikir secara 'Global Chunking'. Kamu peduli pada dampak luas dan nilai-nilai kemanusiaan. Idealismemu adalah bensin bagi tindakanmu.",
        "emosi": "Sangat luas dan pemaaf. Namun, kamu sering kecewa jika kenyataan dunia tidak seindah idealisme yang ada di kepalamu.",
        "saran": "Mulailah dari langkah kecil yang nyata di depan mata. Idealisme besar membutuhkan pondasi kecil yang kokoh setiap harinya."
    },
    11: {
        "inti": "Sang Visioner Intuitif",
        "pola": "Memiliki sensitivitas tinggi (High Sensory Acuity). Kamu mampu menangkap sinyal-sinyal masa depan atau perasaan orang lain secara intuitif.",
        "emosi": "Intens dan penuh inspirasi. Sering merasa 'berbeda' dari orang kebanyakan yang membuatmu merasa terasing.",
        "saran": "Gunakan intuisimu untuk membimbing orang lain, bukan untuk menghakimi. Temukan jangkar agar pikiranmu tidak melayang terlalu jauh."
    },
    22: {
        "inti": "Sang Pembangun Utama",
        "pola": "Kombinasi antara mimpi besar dan disiplin baja. Kamu punya kemampuan untuk mewujudkan visi yang dianggap mustahil oleh orang lain.",
        "emosi": "Stabil namun penuh tekanan karena tanggung jawab besar yang kamu emban secara sukarela.",
        "saran": "Istirahat bukanlah tanda kelemahan. Untuk membangun gedung pencakar langit yang tinggi, pondasi (kesehatanmu) harus tetap kuat."
    }
}
