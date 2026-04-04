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

# --- INTERFACE UTAMA & LOGO ---
col_logo, col_judul = st.columns([1, 4]) 

with col_logo:
    if os.path.exists("baru.jpg"):
        st.image("baru.jpg", width=120)
    elif os.path.exists("banner.jpg"):
        st.image("banner.jpg", width=120)

with col_judul:
    st.markdown("<h1 style='margin-top: -15px;'>🧠 Neuro Nada Ecosystem</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px; color: #D4AF37;'>Sistem Pemetaan Bawah Sadar & Akselerasi Potensi Diri</p>", unsafe_allow_html=True)

st.markdown("---")

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

closing_
