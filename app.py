import streamlit as st
import datetime
import time

# --- JUDUL ---
st.title("🧠 NLP Deep Analysis")
st.write("Mapping Your Internal Program")

# --- INPUT ---
nama_user = st.text_input("Nama Lengkap:")
tgl_input = st.date_input("Tanggal Lahir:", value=datetime.date(2000, 1, 1))

# --- DATABASE ANALISA ---
def get_analysis(angka, nama):
    data = {
        1: [f"Halo {nama}, Anda pemimpin alami. Jangan terlalu keras pada diri sendiri.", "Butuh Active Listening.", "Meminta bantuan adalah strategi."],
        2: [f"{nama}, Anda intuitif. Kurangi pola People Pleasing.", "Jangan memendam emosi.", "Jujur pada diri sendiri."],
        3: [f"{nama}, pikiran Anda cepat. Fokus selesaikan satu misi.", "Jangan tutupi kegelisahan dengan candaan.", "Gunakan teknik Chunking Down."],
        4: [f"{nama}, Anda pilar stabilitas. Belajarlah lebih fleksibel.", "Tunjukkan cinta lewat kata-kata juga.", "Terima ketidakpastian."],
        5: [f"{nama}, kebebasan itu penting. Tapi disiplin itu jembatan sukses.", "Jangan lari dari komitmen.", "Temukan satu fokus."],
        6: [f"{nama}, Anda pelindung. Rawat diri sendiri dulu.", "Jangan terlalu mengatur pasangan.", "Isi gelas Anda dulu."],
        7: [f"{nama}, Anda pemikir dalam. Kurangi Overthinking.", "Cari koneksi intelektual.", "Tindakan lebih nyata dari pikiran."],
        8: [f"{nama}, Anda berorientasi hasil. Lembutkan hati Anda.", "Kehadiran emosional itu utama.", "Apresiasi prosesnya."],
        9: [f"{nama}, Anda humanis. Tegaskan batasan diri (Boundaries).", "Jangan biarkan orang salah menetap lama.", "Membantu orang jangan hancurkan diri."]
    }
    return data.get(angka, ["Data tidak ditemukan", "", ""])

# --- TOMBOL ---
if st.button("Mulai Analisa"):
    if not nama_user:
        st.error("Isi nama dulu bro!")
    else:
        # Itung Angka Sederhana
        tgl_str = tgl_input.strftime("%d%m%Y")
        angka = sum(int(d) for d in tgl_str)
        while angka > 9: angka = sum(int(d) for d in str(angka))
        
        res = get_analysis(angka, nama_user)
        
        st.success(f"Analisa Selesai untuk {nama_user}!")
        st.metric("KODE PROGRAM", angka)
        
        st.subheader("💡 Karakter")
        st.info(res[0])
        
        st.subheader("❤️ Asmara")
        st.warning(res[1])
        
        st.subheader("🔍 Insight")
        st.success(res[2])
        
        st.markdown("---")
        st.link_button(f"👉 DOWNLOAD MODUL KODE {angka}", f"https://lynk.id/username_lu/produk-angka-{angka}")

st.write("© 2026 Ahmad Septian Dwi Cahyo")
