import streamlit as st
import datetime
import os
import time
import urllib.parse
import urllib.request
import math
import random
import csv
import io
import hashlib

# --- (SEBELUMNYA SAMA SEPERTI KODE LU, LANGSUNG KE FUNGSI COUPLE MATRIX) ---

def generate_seed(base_str):
    return int(hashlib.md5(base_str.encode('utf-8')).hexdigest(), 16) % (10**8)

def proc_penjelasan_matriks(n1, n2, eso_val, nep_val):
    random.seed(generate_seed(f"pm_v3_{n1}_{n2}_{eso_val}_{nep_val}"))
    header = random.choice(["⚙️ ARSITEKTUR MESIN NEURO-RELATIONSHIP", "📡 DEKODE SINYAL KOSMIK PASANGAN", "📜 LOGIKA ALGORITMA PENYATUAN"])
    
    f_eso = random.choice([
        f"Fusi vibrasi nama <b>{n1}</b> dan <b>{n2}</b> tidak terjadi secara kebetulan. Hasil ekstraksi mengunci pada Frekuensi <b>{eso_val}</b>. Angka ini adalah 'Wajah Ketiga'—yakni persona entitas gabungan yang akan selalu dilihat dan dirasakan oleh orang-orang di sekitar saat kalian tampil berdua.", 
        f"Gesekan energi dari struktur huruf <b>{n1}</b> dan <b>{n2}</b> menciptakan resonansi baru di angka <b>{eso_val}</b>. Ini mendefinisikan *Soul Purpose* (Tujuan Jiwa) kenapa kalian berdua dipertemukan di garis waktu ini."
    ])
    
    f_nep = random.choice([
        f"Kalkulasi sinkronisasi waktu dan gravitasi lahir (Total Benturan Neptu <b>{nep_val}</b>) memetakan titik buta (*Blind Spot*) dari ego bawah sadar kalian. Ini adalah peta letak ranjau konflik yang akan selalu berulang jika tidak disadari.", 
        f"Analisa siklus (Parameter Akselerasi Neptu <b>{nep_val}</b>) menjadi radar pendeteksi stabilitas mental kalian. Angka ini membongkar bagaimana filter otak kalian berbenturan saat sedang dalam kondisi stres parah."
    ])
    
    return f'<div class="info-metric-box"><b style="color:#FFD700; font-size:14px;">{header}:</b><br><br>• <b style="color:white;">TOTAL FREKUENSI ESOTERIK:</b><br><span style="color:#ccc; display:inline-block; margin-top:4px; margin-bottom:8px;">{f_eso}</span><br>• <b style="color:white;">TOTAL BENTURAN NEPTU:</b><br><span style="color:#ccc; display:inline-block; margin-top:4px;">{f_nep}</span></div>'

def proc_couple_persona(root_c, n1, n2):
    random.seed(generate_seed(f"cp_deep_{n1}_{n2}_{root_c}"))
    buka = random.choice([
        f"Hukum tarikan resonansi mencatat bahwa penyatuan DNA psikologis **{n1}** dan **{n2}** menghasilkan gelombang **Root {root_c}**.",
        f"Ketika ego **{n1}** dilebur dengan frekuensi **{n2}**, sistem mendeteksi lahirnya entitas baru yang terkunci di **Root {root_c}**."
    ])
    
    desc = {
        1: ("THE EMPIRE BUILDERS (Kekuatan & Dominasi)", f"Penyatuan kalian memancarkan aura Alpha yang sangat intimidatif dan dominan. Saat {n1} dan {n2} bersatu, fokus bawah sadar kalian bukan lagi sekadar urusan romansa menye-menye, melainkan ambisi mutlak untuk menaklukkan target, karir, dan status sosial. Waspadai persaingan ego di dalam selimut; jangan sampai kalian berdua berebut setir kemudi kapal yang sama."),
        2: ("THE EMPATHIC RESONANCE (Telepati Batin)", f"Kalian diberkahi dengan 'Wi-Fi Batin' berfrekuensi tinggi. Sangat mudah bagi {n1} maupun {n2} untuk saling membaca perubahan *mood* hanya dari tarikan napas atau tatapan mata tanpa perlu mengucapkan sepatah kata pun. Kekuatan utama kalian adalah harmoni dan kemampuan menetralisir racun mental (anxiety) satu sama lain."),
        3: ("THE MAGNETIC CHARM (Daya Tarik Sosial)", f"Vibrasi gabungan kalian bertindak bagaikan magnet gravitasi di tengah keramaian. {n1} dan {n2} adalah entitas pasangan yang mampu menghidupkan suasana mati menjadi penuh letupan ide dan tawa. Energi komunikasi kalian sangat membius, membuat relasi dan koneksi bisnis mudah terpikat untuk membantu kalian."),
        4: ("THE ARCHITECTS OF REALITY (Pondasi Baja)", f"Hubungan ini tidak dibangun di atas awan angan-angan romantis yang rapuh, melainkan dipaku kuat di atas kerasnya realitas bumi. Otak {n1} dan {n2} secara otomatis berorientasi pada keamanan, membangun struktur aset keluarga, dan menjunjung tinggi loyalitas absolut. Badai sekencang apapun sulit merobohkan akar kalian."),
        5: ("THE QUANTUM NOMADS (Akselerasi & Eksplorasi)", f"Kalian berdua dipenuhi bahan bakar adrenalin! Rutinitas yang monoton adalah racun mematikan bagi hubungan ini. Cinta dan daya tarik antara {n1} dan {n2} akan terus menyala hebat selama kalian terus memberikan kejutan, menantang hal baru, dan menolak tunduk pada aturan tradisional yang membosankan."),
        6: ("THE SANCTUARY (Benteng Pengayom)", f"Simbol perlindungan emosional tertinggi. Rumah tangga dan hubungan {n1} dan {n2} bertindak sebagai 'Pusat Penyembuhan' (*Sanctuary*). Bukan hanya untuk kalian berdua, tapi sirkel pertemanan dan keluarga besar seringkali menyerap energi kedamaian dan meminta perlindungan moral dari entitas kalian berdua."),
        7: ("THE MYSTIC SYNERGY (Koneksi Eksklusif)", f"Hubungan ini sangat tertutup, eksklusif, dan memiliki kedalaman intelektual/spiritual yang tidak bisa dipahami oleh logika sirkel luar. {n1} dan {n2} lebih menyukai ruang *private* yang hening daripada validasi publik. Kalian adalah pengamat dunia yang saling menemukan tempat bersembunyi."),
        8: ("THE MATERIAL GRAVITY (Mesin Kelimpahan)", f"Jika ego kalian berdua berhasil ditundukkan dan disinkronkan, penyatuan {n1} dan {n2} adalah mesin pencetak kekayaan material. Alam semesta merespons persatuan kalian dengan membukakan pintu otoritas bisnis dan finansial kelas atas. Hati-hati, uang bisa menjadi alat ukur cinta jika kalian kehilangan kesadaran diri."),
        9: ("THE CONSCIOUS UNION (Kesadaran Spiritual)", f"Tingkat penerimaan batin kalian telah melampaui ego fisik. {n1} dan {n2} dipertemukan untuk saling menyembuhkan trauma (Luka *Inner-Child*) masa lalu. Interaksi kalian dipenuhi dengan toleransi tinggi dan pandangan welas asih. Kalian adalah obat penawar bagi racun penderitaan satu sama lain.")
    }
    
    data = desc.get(root_c, ("UNCHARTED ANOMALY", "Entitas frekuensi tak tertebak."))
    return data[0], f"{buka} {data[1]}"

def proc_weton_kombo(sisa, n1, n2, z1, z2):
    random.seed(generate_seed(f"wt_deep_{n1}_{n2}_{sisa}_{z1}_{z2}"))
    
    do_list = {
        1: [
            f"Gunakan teknik *Pacing-Leading* (Samakan lalu Arahkan). Saat argumen memanas, hentikan refleks membantah! Validasi dulu emosi {n2} dengan mendengarkan aktif sebelum Anda menyuntikkan logika perbaikan.", 
            f"Terapkan interupsi *Time-Out* secara disiplin. Saat nada suara mulai meninggi, segera ambil jeda 15 menit. Biarkan amygdala (otak emosi) bawaan {z1} dan {z2} melakukan *cooling down* sebelum kata-kata sarkastik terlanjur terucap."
        ],
        2: [
            f"Posisikan {n2} sebagai *Mastermind Partner* yang setara. Jangan pernah mengambil keputusan strategis sendirian diam-diam! Libatkan dia, karena energi rezeki kalian mengalir dari rasa dihargai.", 
            f"Bangun *Rapport* batin dengan apresiasi mikroskopis. Jangan tunggu momen besar untuk memuji; hargai tindakan kecil {n1} secara verbal dan terbuka. Wibawa hubungan kalian tumbuh dari validasi ini."
        ],
        3: [
            f"Suntikkan *Pattern Interrupt* (Pola Kejutan Instan) secara berkala. Ubah rute jalan-jalan, lakukan kencan tanpa rencana, atau kejutkan {n2} agar sirkuit dopamin cinta kalian tidak mati rasa digerus rutinitas.", 
            f"Jadwalkan sesi *Deep-Talk* tanpa distraksi layar HP minimal dua minggu sekali. Bongkar peta pikiran masa depan bersama untuk menjaga keselarasan frekuensi jiwa kalian berdua."
        ],
        4: [
            f"Kuasai seni *Reframing* (Pembingkaian Ulang Perspektif) saat dilanda krisis hebat. Ubah pola pikir dari 'Kamu vs Aku' menjadi 'Kita Berdua vs Masalah Ini'. Jangan biarkan masalah luar memecah belah benteng dalam.", 
            f"Baja dibentuk dari tempaan panas. Pahami bahwa badai gesekan sifat di fase awal adaptasi ini hanyalah *test ombak* dari Semesta. Tahan ego Anda; ini adalah harga tiket mutlak menuju kelimpahan besar."
        ],
        5: [
            f"Gelar sesi penyelarasan visi material secara transparan. Bicarakan angka, aset, dan target secara terbuka. Sinkronisasi frekuensi syukur di antara {n1} dan {n2} adalah saklar utama penyedot rezeki kalian.", 
            f"Bertindaklah sebagai jangkar penyelamat emosi (*Emotional Anchor*). Jika salah satu sedang tenggelam dalam energi pesimis/ketakutan finansial, tugas absolut pasangannya adalah segera menariknya kembali ke frekuensi kelimpahan."
        ],
        6: [
            f"Berikan jarak spasial (*Space*) sesaat ketika tensi saraf sudah memerah. Otak kalian berdua memiliki filter bahasa (*Meta-Model*) yang berbeda. Saat terjadi *miskomunikasi*, mundur selangkah untuk mereset *State* (kondisi mental).", 
            f"Jadikan humor *absurd* sebagai penawar racun (*Antidote*). Saat perdebatan mulai terasa terlalu serius dan menyesakkan dada, sebuah ledakan tawa spontan sangat ampuh me-reset sirkuit ego yang tegang."
        ],
        7: [
            f"Komunikasi harus bersifat *Sensory Based* (Berbasis Fakta Indrawi). Jangan menebak-nebak! Selalu klarifikasi dengan kalimat: 'Apakah maksud ucapan kamu tadi X atau Y?'. Bunuh asumsi sebelum ia menjadi monster cemburu.", 
            f"Banjiri pasangan dengan bahasa cintanya yang paling dominan (*Love Language*). Tingkatkan intensitas sentuhan fisik atau waktu berkualitas untuk membungkam *insecurity* bawah sadar dan rasa curiga tanpa alasan."
        ],
        8: [
            f"Cegah kematian rasa (*Boredom*) dengan menciptakan tantangan buatan. Otak kalian terlalu damai hingga rawan hampa. Cari proyek bisnis baru atau hobi gila yang bisa dikerjakan berdua untuk memancing hormon adrenalin.", 
            f"Jangan biarkan rasa aman berubah menjadi kelalaian foya-foya perasaan. Tetaplah menjadi sosok misterius yang terus memperbaiki kualitas diri agar pasangan tetap memiliki *trigger* rasa kagum setiap harinya."
        ]
    }
    
    dont_list = {
        1: [
            f"DILARANG KERAS melakukan *Mind-Reading* negatif (Membaca Pikiran). Jangan pernah berasumsi bahwa {n2} memiliki niat jahat atau meremehkan Anda tanpa klarifikasi bukti eksplisit.", 
            f"Haram hukumnya mengkonfrontasi masalah prinsip saat salah satu pihak sedang berada dalam kondisi *H.A.L.T* (Hungry, Angry, Lonely, Tired). Logika tumpul, yang merespons hanyalah ego binatang buas."
        ],
        2: [
            f"Jauhi jebakan ilusi 'Pencitraan Sempurna' di media sosial. Jangan memalsukan kebahagiaan di luar padahal kalian sedang saling mendiamkan di dalam rumah. *Fake positivity* akan mensabotase wibawa kalian.", 
            f"Dilarang memberikan celah sekecil apapun bagi intervensi keluarga besar atau sahabat dekat untuk mengatur ritme rumah tangga kalian. Entitas pengambil keputusan absolut haruslah kalian berdua."
        ],
        3: [
            f"Waspadai jebakan *Comfort Zone* (Zona Nyaman Mematikan). Saking nyamannya satu sama lain, jangan sampai ambisi karir atau finansial kalian tumpul karena merasa 'cinta saja sudah cukup'.", 
            f"Dilarang mengabaikan *grooming* (perawatan fisik/penampilan) hanya karena merasa posisi Anda sudah sangat aman dan diterima seadanya di hati {n1}. Kehilangan daya tarik visual membunuh percikan gairah pelan-pelan."
        ],
        4: [
            f"Jangan gunakan gengsi dan dominasi ego masa lalu sebagai pedang untuk menikam harga diri {n2}. Adaptasi ini menuntut Anda membuang karakter lama yang *toxic* jika ingin pondasi ini bertahan.", 
            f"Pantang melempar handuk menyerah di fase transisi awal (1-3 tahun pertama). Mengucapkan kata ancaman 'Pisah/Cerai' di saat emosi sesaat adalah bom waktu yang menghancurkan struktur *Trust* secara permanen."
        ],
        5: [
            f"Dilarang keras menjadikan metrik uang/materi sebagai satu-satunya lem perekat jiwa antara {n1} dan {n2}. Jika akar spiritual dilupakan, uang yang banyak justru akan menjadi sumber kehancuran batin.", 
            f"Bahaya kesombongan! Dilarang memandang rendah atau meremehkan orang lain secara verbal saat pintu rezeki hasil persatuan kalian mulai meledak terbuka. Kesombongan instan akan memutus aliran berkah dengan sangat cepat."
        ],
        6: [
            f"Saat sedang marah besar, DILARANG KERAS menyerang fisik, mengungkit masa lalu yang memalukan, atau menghancurkan harga diri fundamental {n2}. Argumen boleh tajam, tapi martabat harus dijaga.", 
            f"Hindari senjata psikologis *Silent Treatment* (Mendiamkan Pasangan Tanpa Kejelasan) lebih dari batas wajar. Menghukum pasangan dengan keheningan adalah bentuk manipulasi emosi tingkat tinggi yang menciptakan luka *trauma*."
        ],
        7: [
            f"DILARANG MENGGUNAKAN kata-kata absolut / *Universal Quantifiers* saat bertengkar, seperti: 'Kamu SELALU begini!' atau 'Kamu TIDAK PERNAH peduli!'. Ini adalah virus NLP yang mengunci otak pasangan dalam mode tempur defensif.", 
            f"Jangan merendahkan diri menjadi agen detektif amatir yang mengintai privasi isi HP, dompet, atau riwayat chat pasangan secara diam-diam. Penyakit *Trust Issue* adalah kanker ganas pembunuh kedamaian batin."
        ],
        8: [
            f"Waspadai virus *Take it for granted* (Menggampangkan Kehadiran Pasangan). Dilarang berhenti memberikan *effort* (usaha lebih) untuk menaklukkan hati {n2} setiap harinya layaknya kalian masih dalam masa PDKT.", 
            f"Jangan biarkan roda gigi rutinitas yang damai menidurkan insting romantisme liar Anda. Kedamaian yang statis membutuhkan kejutan gairah buatan agar aliran energi kehidupan kalian tidak berkarat."
        ]
    }
    
    hasil = {
        1: ("💔 SINDROM PEGAT (Ujian Ego Fatal)", "Kalkulasi menunjuk pada perbedaan arsitektur neurologis yang sangat tajam dalam memproses rasa kecewa. Jika ego defensif (gengsi) tidak segera ditundukkan, interaksi kalian rawan menghasilkan adu argumen yang saling melukai harga diri terdalam."),
        2: ("👑 RESONANSI RATU (Kharisma Dominan)", "Entitas kalian dianugerahi daya pancar wibawa pasangan kelas atas. Ada magnet *respect* otomatis di alam bawah sadar yang membuat orang lain, rekan bisnis, dan lingkungan sosial tunduk dan menaruh hormat pada kalian berdua."),
        3: ("💞 FREKUENSI JODOH (Sinkronisasi Jiwa)", "Koneksi kalian terjalin tanpa paksaan. Ada tingkat penerimaan bawah sadar yang sangat dalam seolah *Blueprint* energi jiwa kalian sudah pernah saling terhubung di garis waktu sebelumnya. Segala perbedaan mudah dicarikan jalan tengah."),
        4: ("🌱 FASE TOPO (Ujian Transmutasi)", "Ibarat ulat yang sedang diuji dalam ruang kepompong. Awal kolaborasi ini dijamin akan dipenuhi gesekan adaptasi yang menguras kewarasan mental. Namun, jika ego kalian berhasil *survive* melewati masa kritis ini, pondasi kalian di masa depan mustahil bisa dihancurkan badai apapun."),
        5: ("💰 ALGORITMA TINARI (Magnet Kelimpahan)", "Bersyukurlah! Entitas pasangan ini memancarkan vibrasi penyedot kelimpahan finansial tingkat tinggi. Kemacetan rezeki masa lalu secara ajaib mendadak terurai dan pintu kolaborasi bisnis terbuka lebar semenjak kalian memutuskan untuk bersatu."),
        6: ("⚡ FRIKSI PADU (Benturan Filter Realitas)", "Sistem mendeteksi adanya *noise* (kebisingan). Bersiaplah menghadapi letupan perdebatan yang repetitif. Ini terjadi bukan karena kalian kekurangan cinta, melainkan karena *Filter* persepsi otak kalian dalam menangkap informasi benar-benar beroperasi di gelombang yang berbeda."),
        7: ("👁️ JEBAKAN SUJANAN (Ilusi Cemburu Buta)", "Vibrasi penyatuan ini secara aneh sangat rentan menarik *noise* negatif berupa miskomunikasi parah, prasangka buruk, dan racun kecurigaan. Banyak asumsi ilusi (pikiran yang tidak nyata) yang menipu persepsi kalian hingga berujung pada pertengkaran yang tak beralasan."),
        8: ("🕊️ ANCHOR PESTHI (Ketenangan Absolut)", "Kehadiran fisik kalian saling beresonansi kuat untuk menetralisir racun stres (Kortisol) dari kerasnya kehidupan luar. Kalian adalah oasis satu sama lain. Relasi batin kalian berjalan sangat adem, minim drama tak penting, dan stabil dalam kedamaian.")
    }
    
    return hasil[sisa][0], hasil[sisa][1], random.choice(do_list[sisa]), random.choice(dont_list[sisa])

# --- TAB 2 UI STREAMLIT (Bagian Output Saja, yang lainnya tetep sama) ---
# ... (Pastikan paste di dalam block `with tab2:` pas nampilin hasil)

                    # --- GANTI BAGIAN OUTPUT TAB 2 DENGAN INI ---
                    st.markdown(f"### 🔮 The Unified Resonance: {safe_n1} & {safe_n2}")
                    st.markdown(f"""<div class="matrix-container soft-fade"><div class="matrix-item"><div class="matrix-label">Beban Neptu {safe_n1}</div><div class="matrix-value">{hc1} {pc1} ({nep_1})</div></div><div class="matrix-item"><div class="matrix-label">Beban Neptu {safe_n2}</div><div class="matrix-value">{hc2} {pc2} ({nep_2})</div></div><div class="matrix-item" style="background: rgba(212,175,55,0.2); border-left: 1px solid #D4AF37; border-right: 1px solid #D4AF37;"><div class="matrix-label" style="color:#FFD700;">TOTAL BENTURAN NEPTU</div><div class="matrix-value matrix-value-special">{nep_1 + nep_2}</div></div><div class="matrix-item"><div class="matrix-label">Total Frekuensi Esoterik</div><div class="matrix-value">{total_couple}</div></div></div>""", unsafe_allow_html=True)
                    
                    st.markdown(proc_penjelasan_matriks(safe_n1, safe_n2, total_couple, (nep_1+nep_2)), unsafe_allow_html=True)
                    
                    st.markdown(f'<div class="dynamic-reading-box soft-fade" style="border-left-color: #25D366; background: rgba(10,30,15,0.8);"><h4 style="color: #25D366; margin-top:0; letter-spacing:1px;">🧬 Persona Entitas Baru: {c_title}</h4><p style="color:#e0e0e0; line-height:1.7; font-size:15px;">{c_desc}</p></div>', unsafe_allow_html=True)
                    
                    st.markdown(f"""<div class="soft-fade" style="background: rgba(30,20,20,0.8); border: 1px solid #ff4b4b; border-left: 5px solid #ff4b4b; padding: 20px; border-radius: 8px; margin-bottom:20px;">
                    <b style="color:#ff4b4b; font-size:16px;">Titik Benturan Gesekan Bawah Sadar ({judul_jodoh}):</b><br>
                    <span style="color:#ccc; display:inline-block; margin-top:8px; line-height:1.6; font-size:15px;">{desk_jodoh}</span>
                    </div>""", unsafe_allow_html=True)
                    
                    if sel in [0, 3, 6, 9]: 
                        st.markdown(f"<div class='info-metric-box soft-fade' style='border-color:#25D366; background:rgba(37,211,102,0.05);'><span style='font-size:24px;'>💘</span> <b style='color:#25D366; font-size:15px;'>SKOR META-PROGRAM (NLP): Resonansi Sangat Sinkron.</b><br><span style='color:#ccc; margin-top:5px; display:inline-block;'>Otak sadar maupun bawah sadar kalian memproses manajemen konflik dengan sintaksis bahasa ego yang serupa. Transmisi pesan cepat ditangkap tanpa distorsi.</span></div>", unsafe_allow_html=True)
                    elif sel in [1, 2, 8]: 
                        st.markdown(f"<div class='info-metric-box soft-fade' style='border-color:#FFD700; background:rgba(255,215,0,0.05);'><span style='font-size:24px;'>⚖️</span> <b style='color:#FFD700; font-size:15px;'>SKOR META-PROGRAM (NLP): Dinamika Labil (Adaptif).</b><br><span style='color:#ccc; margin-top:5px; display:inline-block;'>Hubungan ini butuh kalibrasi empati tingkat tinggi secara konstan. Gelombang kalian sering tumpang tindih; di satu waktu sangat sehati, di waktu lain miskomunikasi total.</span></div>", unsafe_allow_html=True)
                    else: 
                        st.markdown(f"<div class='info-metric-box soft-fade' style='border-color:#ff4b4b; background:rgba(255,75,75,0.05);'><span style='font-size:24px;'>🔥</span> <b style='color:#ff4b4b; font-size:15px;'>SKOR META-PROGRAM (NLP): Rawan Gesekan / Disosiasi.</b><br><span style='color:#ccc; margin-top:5px; display:inline-block;'>Sinyal waspada! Secara genetik psikologis, kalian memiliki filter penerimaan informasi (*Map of Reality*) yang bertolak belakang. Anda bilang A, otak pasangan memprosesnya sebagai Z. Butuh toleransi ego baja.</span></div>", unsafe_allow_html=True)
         
                    c_do_c, c_dont_c = st.columns(2)
                    with c_do_c: 
                        st.markdown(f"<div class='soft-fade' style='background:rgba(37,211,102,0.05); padding:20px; border-radius:10px; border:1px solid #25D366; height:100%; box-shadow: inset 0 0 20px rgba(37,211,102,0.05);'><b style='color:#25D366; font-size:16px; letter-spacing:1px;'>✅ PROTOKOL HUBUNGAN (DO):</b><hr style='border-color:rgba(37,211,102,0.2); margin-top:10px; margin-bottom:15px;'><span style='color:#e0e0e0; line-height:1.7; font-size:14px;'>{d_do}</span></div>", unsafe_allow_html=True)
                    with c_dont_c: 
                        st.markdown(f"<div class='soft-fade' style='background:rgba(255,75,75,0.05); padding:20px; border-radius:10px; border:1px solid #ff4b4b; height:100%; box-shadow: inset 0 0 20px rgba(255,75,75,0.05);'><b style='color:#ff4b4b; font-size:16px; letter-spacing:1px;'>❌ RED ZONE (DON'T):</b><hr style='border-color:rgba(255,75,75,0.2); margin-top:10px; margin-bottom:15px;'><span style='color:#e0e0e0; line-height:1.7; font-size:14px;'>{d_dont}</span></div>", unsafe_allow_html=True)
