import os
import pandas as pd
import requests
import streamlit as st

# Konfigurasi Halaman Website
st.set_page_config(
    page_title="Pawsitive Journey - Adopsi Hewan Jogja",
    page_icon="🐾",
    layout="wide",
)

# --- CSS STYLING: TABS NAVIGASI PILL ESTETIK & FONT CUSTOM ---
st.markdown(
    """
    <style>
    /* Impor Google Font Estetik (Plus Jakarta Sans) */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

    /* Terapkan font ke seluruh aplikasi */
    .stApp, html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        letter-spacing: 0.4px;
        color: #4A403A;
    }

    /* Background Utama Pastel Lembut Ceria */
    .stApp {
        background: linear-gradient(135deg, #E6F8FA 0%, #FFFDE3 100%);
    }

    /* Efek Ujung Tumpul + Bayangan Menyala (Glow Shadow) untuk Banner Cover */
    div[data-testid="stImage"] img {
        border-radius: 24px !important;
        box-shadow: 0 10px 35px rgba(255, 133, 161, 0.4), 0 0 20px rgba(255, 224, 130, 0.3) !important;
        border: 4px solid #FFFFFF !important;
    }

    /* Styling Kartu Hewan ala Rayo Card */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: #FFFFFF;
        border-radius: 18px;
        border: 3px solid #FFE5EC !important;
        padding: 18px;
        box-shadow: 0 8px 20px rgba(255, 182, 193, 0.2);
    }

    /* Styling Kotak Warning Imut Adopsi */
    .adopt-warning-box {
        background-color: #FFF0F3;
        border: 2px dashed #FF85A1;
        border-radius: 18px;
        padding: 14px 22px;
        text-align: center;
        margin: 15px auto 25px auto;
        max-width: 650px;
        box-shadow: 0 6px 20px rgba(255, 133, 161, 0.2);
    }
    .adopt-warning-box p {
        color: #5A4B42;
        font-size: 15px;
        line-height: 1.6;
        margin: 0;
        font-weight: 500;
        letter-spacing: 0.4px;
    }

    /* KUSTOMISASI TOMBOL UMUM */
    div.stButton > button {
        background-color: #FF85A1;
        color: white;
        border-radius: 20px;
        font-weight: 600;
        letter-spacing: 0.5px;
        border: none;
        padding: 0.6rem 1.8rem;
        box-shadow: 0 4px 10px rgba(255, 133, 161, 0.35);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #FF5C8A;
        color: white;
        transform: scale(1.03);
    }

    /* TOMBOL KATEGORI UTAMA (BENTUK BULAT MANIS & MENYALA) */
    .love-btn div.stButton > button {
        width: 130px !important;
        height: 130px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #FF6B8B 0%, #FF8E9E 100%) !important;
        color: white !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        border: 4px solid #FFFFFF !important;
        box-shadow: 0 10px 25px rgba(255, 107, 139, 0.6), 0 0 20px rgba(255, 182, 193, 0.5) !important;
        margin: 0 auto;
        display: block;
        text-align: center;
        line-height: 1.3 !important;
        transition: all 0.3s ease;
    }
    .love-btn div.stButton > button:hover {
        transform: scale(1.08);
        background: linear-gradient(135deg, #FF4B72 0%, #FF6B8B 100%) !important;
        box-shadow: 0 14px 30px rgba(255, 75, 114, 0.8), 0 0 25px rgba(255, 133, 161, 0.7) !important;
    }

    /* ================= KUSTOMISASI TOMBOL NAVBAR (PILL TABS - GRADASI BIRU LEMBUT) ================= */
    div[data-testid="stHorizontalBlock"] div.stButton > button {
        background: linear-gradient(135deg, #4A90E2 0%, #5CA9F8 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #BEE3F8 !important;
        border-radius: 30px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        letter-spacing: 0.8px !important;
        text-transform: capitalize !important;
        padding: 0.45rem 1.1rem !important;
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.25) !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
        background: linear-gradient(135deg, #357ABD 0%, #4A90E2 100%) !important;
        color: #FFFFFF !important;
        border-color: #90CDF4 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(74, 144, 226, 0.4) !important;
    }
    
    /* Typography Header Estetik */
    h1, h2, h3 {
        color: #3A2F28;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
    }
    p, span, li, label {
        line-height: 1.6 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ================= AMBIL DATA UTAMA DARI GOOGLE SHEETS =================
try:
  sheet_url = "https://docs.google.com/spreadsheets/d/1UkhePDVF1qz7XP07NQI2-rF_OgaQG58LIIj7Juq0ZW8/edit?usp=sharing"
  url_csv = sheet_url.replace("/edit?usp=sharing", "/export?format=csv").replace(
      "/edit#gid=0", "/export?format=csv"
  )
  df = pd.read_csv(url_csv)
  df = df.dropna(subset=["foto"])
  df["kategori_lower"] = df["kategori"].astype(str).str.lower()
  df["foto_lower"] = df["foto"].astype(str).str.lower()
except Exception as e:
  df = pd.DataFrame()


# ================= STATE MANAGEMENT =================
if "selected_animal" not in st.session_state:
  st.session_state.selected_animal = None

if "active_category" not in st.session_state:
  st.session_state.active_category = None

if "menu_atas" not in st.session_state:
  st.session_state.menu_atas = "🏠 Beranda"


def pilih_hewan(nama_hewan):
  st.session_state.selected_animal = nama_hewan


def kembali_ke_menu():
  st.session_state.selected_animal = None


# ================= NAVBAR ATAS (MENGGUNAKAN TOMBOL PILL ESTETIK) =================
col_brand, c_m1, c_m2, c_m3, c_m4 = st.columns([1.5, 0.8, 0.9, 0.9, 0.9])

with col_brand:
  st.markdown(
      "<h3 style='color: #FF5C8A; margin: 0; padding-top: 5px;'>🐾 Pawsitive"
      " Journey</h3>",
      unsafe_allow_html=True,
  )


# Fungsi untuk membuat tombol menu aktif vs tidak aktif secara visual
def render_menu_btn(label_menu, key_name):
  is_active = st.session_state.menu_atas == label_menu
  if is_active:
    return st.button(
        label_menu,
        key=key_name,
        use_container_width=True,
        help="Menu sedang dibuka",
    )
  else:
    return st.button(label_menu, key=key_name, use_container_width=True)


with c_m1:
  if render_menu_btn("🏠 Beranda", "btn_beranda"):
    st.session_state.menu_atas = "🏠 Beranda"
    st.session_state.selected_animal = None
    st.session_state.active_category = None
    st.rerun()

with c_m2:
  if render_menu_btn("📢 Titip Adopsi", "btn_titip"):
    st.session_state.menu_atas = "📢 Titip Adopsi"
    st.session_state.selected_animal = None
    st.session_state.active_category = None
    st.rerun()

with c_m3:
  if render_menu_btn("ℹ️ Tentang Kami", "btn_tentang"):
    st.session_state.menu_atas = "ℹ️ Tentang Kami"
    st.session_state.selected_animal = None
    st.session_state.active_category = None
    st.rerun()

with c_m4:
  if render_menu_btn("🏡 Cara Adopsi", "btn_cara"):
    st.session_state.menu_atas = "🏡 Cara Adopsi"
    st.session_state.selected_animal = None
    st.session_state.active_category = None
    st.rerun()

# Styling khusus tambahan via CSS untuk tombol menu yang SEDANG AKTIF
active_menu_name = st.session_state.menu_atas
if active_menu_name == "🏠 Beranda":
  active_key_selector = "btn_beranda"
elif active_menu_name == "📢 Titip Adopsi":
  active_key_selector = "btn_titip"
elif active_menu_name == "ℹ️ Tentang Kami":
  active_key_selector = "btn_tentang"
else:
  active_key_selector = "btn_cara"

st.markdown(
    f"""
    <style>
    div[data-testid="stHorizontalBlock"] button[kind="secondary"]#{active_key_selector},
    div[data-testid="stHorizontalBlock"] div:has(button[key="{active_key_selector}"]) button {{
        background: linear-gradient(135deg, #2B6CB0 0%, #3182CE 100%) !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        border: 2px solid #90CDF4 !important;
        box-shadow: 0 4px 18px rgba(43, 108, 176, 0.5), 0 0 15px rgba(144, 205, 244, 0.6) !important;
        transform: scale(1.03);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.divider()

menu_atas = st.session_state.menu_atas

# ================= BANNER COVER UTAMA =================
path_banner = os.path.join("foto_hewan", "cover_hewan.png")
if menu_atas == "🏠 Beranda" and st.session_state.selected_animal is None:
  c_b1, c_b2, c_b3 = st.columns([1, 2.5, 1])
  with c_b2:
    if os.path.exists(path_banner):
      st.image(path_banner, use_container_width=True)
    else:
      st.markdown(
          """
            <div style="background: linear-gradient(90deg, #FFFDE3 0%, #E6F8FA 100%); padding: 25px; border-radius: 20px; border: 3px dashed #FF85A1; text-align: center; margin-bottom: 15px;">
                <h1 style="color: #3A2F28; margin-bottom: 5px; font-size: 24px;">🐾 Pawsitive Journey 🐾</h1>
                <p style="color: #555; font-size: 14px;">Temukan sahabat berbulu setiamu di Yogyakarta dengan penuh kasih! ❤️</p>
            </div>
            """,
          unsafe_allow_html=True,
      )
  st.write("")

# ================= KONDISI HALAMAN =================
if menu_atas == "ℹ️ Tentang Kami":
  st.header("ℹ️ Tentang Pawsitive Journey")
  st.write(
      "Platform informasi adopsi hewan terpercaya yang berpusat di Yogyakarta."
      " Kami berdedikasi mempertemukan anabul terlantar dengan keluarga baru"
      " yang penuh kasih secara murni adopsi (bukan jual beli)."
  )
  col_a1, col_a2 = st.columns(2)
  with col_a1:
    st.markdown("### 📍 Lokasi Shelter")
    st.markdown("- Sleman, Bantul, & Yogyakarta Kota")
  with col_a2:
    st.markdown("### 🩺 Kesehatan")
    st.markdown("- Vaksinasi, Steril, & Pemeriksaan Rutin")

elif menu_atas == "🏡 Cara Adopsi":
  st.header("🏡 How To Adopt - Panduan Mengadopsi")
  st.markdown("""
    Langkah mudah membawa pulang anabul kesayangan khusus wilayah Jogja:
    1. **Pilih Hewan:** Klik tombol kategori Kucing atau Anjing di Beranda, lalu pilih anabul favoritmu untuk melihat cerita lengkapnya.
    2. **Hubungi Admin:** Klik tombol WhatsApp yang tersedia di halaman detail hewan untuk konsultasi.
    3. **Verifikasi Singkat:** Pastikan lingkungan rumah nyaman dan siap menyambut anggota keluarga baru.
    4. **Proses Adopsi:** Penjemputan atau pengantaran anabul ke rumahmu di Yogyakarta!
    """)

elif menu_atas == "📢 Titip Adopsi":
  st.header("📢 Titipkan Info Anabul untuk Dibantu Promosi Adopsi")
  st.markdown(
      "Menemukan kucing atau anjing terlantar di sekitar Jogja dan ingin"
      " mencarikan rumah baru yang aman? Isi form di bawah ini. Datanya akan"
      " langsung masuk ke database kami secara otomatis untuk diverifikasi"
      " tim! **(100% Adopsi, Tanpa Jual Beli)** ✨"
  )

  st.write("")
  with st.form("form_titip_adopsi"):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
      nama_penemu = st.text_input(
          "👤 Nama Kamu / Rescuer:", placeholder="Contoh: Kak Sarah"
      )
      kontak_penemu = st.text_input(
          "📞 Nomor WhatsApp Kamu:", placeholder="Contoh: 081234567890"
      )
      nama_anabul = st.text_input(
          "🐾 Nama Panggilan Anabul (Bebas):", placeholder="Contoh: Miko"
      )
    with col_f2:
      kategori_anabul = st.selectbox(
          "🐾 Kategori Hewan:", ["Kucing", "Anjing"]
      )
      lokasi_ketemu = st.text_input(
          "📍 Lokasi Ditemukan di Jogja:",
          placeholder="Contoh: Condongcatur, Sleman",
      )
      kondisi_status = st.selectbox(
          "📌 Status Saat Ini:",
          [
              "Sehat & Siap Adopsi",
              "Perlu Perawatan / Pemulihan",
              "Dalam Penitipan Sementara",
          ],
      )

    story_anabul = st.text_area(
        "📖 Cerita Singkat / Kondisi Anabul:",
        placeholder=(
            "Ceritakan bagaimana anabul ditemukan atau sifat gemasnya agar"
            " calon adopter tertarik..."
        ),
    )

    submitted = st.form_submit_button(
        "🚀 Kirim Data ke Database Pawsitive"
    )

    if submitted:
      if not nama_penemu or not kontak_penemu or not nama_anabul:
        st.warning(
            "⚠️ Harap isi minimal Nama Kamu, No WhatsApp, dan Nama Anabul!"
        )
      else:
        WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw1joZ2t5bcePZJ-l0GDg65TXH52NxjhyAL_EUF60c0EIaJ53tJmrC7QrzjB4rP3oIUuQ/exec"

        payload = {
            "nama_rescuer": nama_penemu,
            "kontak_wa": kontak_penemu,
            "nama_anabul": nama_anabul,
            "kategori": kategori_anabul,
            "lokasi": lokasi_ketemu,
            "status": kondisi_status,
            "cerita": story_anabul,
        }

        try:
          with st.spinner("Sedang mengirim data ke database... ⏳"):
            response = requests.post(WEB_APP_URL, json=payload, timeout=15)

          if response.status_code == 200:
            st.success(
                "🎉 Yeay! Data anabul berhasil dikirim dan tersimpan di"
                " database Google Sheets. Tim kami akan segera meninjau"
                " informasinya. Terima kasih sudah peduli pada anabul"
                " terlantar! 🐾"
            )
          else:
            st.error(
                "⚠️ Gagal mengirim data ke server. Coba beberapa saat lagi."
            )
        except Exception as ex:
          st.error(f"Terjadi kesalahan koneksi: {ex}")

elif menu_atas == "🏠 Beranda":

  # --- 1. HALAMAN DETAIL HEWAN (STORY & HOW TO ADOPT) ---
  if st.session_state.selected_animal is not None:
    animal_name = st.session_state.selected_animal
    animal_data = df[df["nama"] == animal_name]

    if not animal_data.empty:
      row = animal_data.iloc[0]

      if st.button("⬅️ Kembali ke Daftar Hewan"):
        kembali_ke_menu()
        st.rerun()

      st.write("")

      # Membaca nama file foto persis seperti yang tertulis di Google Sheets
      nama_file_foto = str(row["foto"]).strip()
      path_foto = os.path.join("foto_hewan", nama_file_foto)

      col_det1, col_det2 = st.columns([1, 1.2])
      with col_det1:
        if os.path.exists(path_foto):
          st.image(
              path_foto,
              use_container_width=True,
              caption=f"Foto {row['nama']}",
          )
        else:
          st.warning(
              f"Foto '{nama_file_foto}' tidak ditemukan di folder foto_hewan."
          )

      with col_det2:
        st.markdown(f"# 🐾 {row['nama']}")
        st.markdown(f"**🐾 Kategori:** {row['kategori']}")
        st.markdown(f"**📌 Status Adopsi:** `{row['status']}`")

        st.markdown("---")
        st.markdown("### 📖 Kisah Penyelamatan (Story)")

        nama_kcl = str(row["nama"]).lower()
        if "bebi" in nama_kcl:
          story_text = (
              f"Bebi ditemukan di sekitar teras toko di kawasan Malioboro"
              " Jogja dengan bulu putihnya yang menggemaskan namun tampak"
              " kusam karena kehujanan. Ia kucing yang sangat manja, suka"
              " mengeong lembut untuk meminta perhatian, dan sangat betah"
              " dipangku sambil dielus."
          )
        elif "nala" in nama_kcl:
          story_text = (
              f"Nala diselamatkan dari halaman kampus di Sleman saat sedang"
              " pincang akibat terbentur. Kini setelah mendapat perawatan di"
              " shelter kami, Nala sudah pulih dan tumbuh menjadi kucing"
              " betina yang anggun, tenang, serta punya mata bulat yang"
              " memesona."
          )
        elif "boba" in nama_kcl:
          story_text = (
              f"Boba adalah kucing kampung bermotif unik yang ditemukan"
              " sedang kelaparan di dekat warung makan daerah Condongcatur."
              " Badannya yang bulat menggemaskan seperti mutiara boba membuat"
              " ia diberi nama Boba. Ia sangat aktif, suka bermain dengan"
              " bola kertas, dan ramah pada manusia."
          )
        elif "lulu" in nama_kcl:
          story_text = (
              f"Dulu {row['nama']} ditemukan di sekitar kawasan Kaliurang"
              " Jogja dalam keadaan lemas dan kelaparan. Berkat perawatan"
              " intensif di shelter kami, sekarang {row['nama']} tumbuh"
              " menjadi anabul yang sangat aktif, manja, dan hobi mengejar"
              " mainan bola bulu."
          )
        elif "miko" in nama_kcl or "milo" in nama_kcl:
          story_text = (
              f"{row['nama']} sempat berlindung di bawah mobil warga saat hujan"
              " deras melanda kota Jogja. Sifatnya yang tenang, senang dielus"
              " di bagian dagu, dan sangat ramah membuatnya cocok jadi teman"
              " santai di kamarmu."
          )
        else:
          story_text = (
              f"Diselamatkan dari area publik di Yogyakarta, {row['nama']}"
              " dulunya sempat pemalu terhadap manusia. Namun, kini ia"
              " menunjukkan sisi menggemaskannya, sangat ceria, dan sudah"
              " siap menyambut kasih sayang dari keluarga barumu!"
          )

        st.write(story_text)

        st.markdown("---")
        st.markdown("### 🏡 Panduan Adopsi Singkat (How To Adopt)")
        st.write(
            "1. Konsultasikan kesiapan adopsi melalui WhatsApp admin kami di"
            " **081390396760**.\n2. Kirimkan foto sudut area rumah/tempat"
            " tinggalmu.\n3. Sepakati jadwal penjemputan anabul di shelter"
            " Jogja."
        )

        st.write("")
        no_hp = "6281390396760"
        pesan_wa = (
            f"Halo Admin Pawsitive Journey, saya ingin mengadopsi {row['nama']}"
            " ({row['kategori']}). Mohon info selanjutnya ya!"
        )
        link_wa = f"https://wa.me/{no_hp}?text={pesan_wa.replace(' ', '%20')}"
        st.link_button(
            f"📱 Adopsi {row['nama']} via WhatsApp",
            link_wa,
            use_container_width=True,
        )

    else:
      st.error("Data hewan tidak ditemukan.")
      if st.button("Kembali"):
        kembali_ke_menu()
        st.rerun()

  # --- 2. HALAMAN UTAMA (BERANDA) ---
  else:
    # --- PEMBERITAHUAN / WARNING IMUT ---
    st.markdown(
        """
        <div class="adopt-warning-box">
            <p>💡 <b>Catatan Penting:</b> Di sini tempat <u>ADOPSI</u> murni dengan penuh kasih sayang, <b>bukan tempat jual beli yaa!</b> ✨🏠🐾</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- JUDUL KATEGORI DENGAN WARNA PINK SENADA YANG ELEGAN ---
    st.markdown(
        """
        <div style="text-align: center; margin-top: 35px; margin-bottom: 20px;">
            <h2 style="color: #D65A83; font-size: 25px; font-weight: 700; margin-bottom: 5px;">
                Pilih Kategori Sahabat Bulu
            </h2>
            <p style="color: #776A62; font-size: 14px; font-weight: 500;">
                Silakan pilih kategori anabul yang ingin kamu adopsi
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tombol Kategori Bentuk Bulat Manis (Cat & Dog) diposisikan di tengah
    col_sp1, col_b1, col_b2, col_sp2 = st.columns([2.5, 1, 1, 2.5])

    with col_b1:
      st.markdown('<div class="love-btn">', unsafe_allow_html=True)
      if st.button("🐱 Kucing\n(Cat)"):
        st.session_state.active_category = "kucing"
        st.rerun()
      st.markdown("</div>", unsafe_allow_html=True)

    with col_b2:
      st.markdown('<div class="love-btn">', unsafe_allow_html=True)
      if st.button("🐶 Anjing\n(Dog)"):
        st.session_state.active_category = "anjing"
        st.rerun()
      st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # --- 3. MENAMPILKAN DAFTAR HEWAN ---
    if st.session_state.active_category is not None:
      kategori_pilihan = st.session_state.active_category
      st.divider()

      if kategori_pilihan == "kucing":
        st.markdown("## 🐱 Daftar Kucing Adopsi")
        df_tampil = df[
            df["kategori_lower"].str.contains("kucing")
            | df["foto_lower"].str.contains("kucing")
        ]
      else:
        st.markdown("## 🐶 Daftar Anjing Adopsi")
        df_tampil = df[
            df["kategori_lower"].str.contains("anjing")
            | df["foto_lower"].str.contains("anjing")
        ]

      if df_tampil.empty:
        st.info("Belum ada hewan dalam kategori ini.")
      else:
        cols = st.columns(3)
        for index, row in df_tampil.reset_index().iterrows():
          nama_file_foto = str(row["foto"]).strip()
          path_foto = os.path.join("foto_hewan", nama_file_foto)

          with cols[index % 3]:
            with st.container(border=True):
              if os.path.exists(path_foto):
                st.image(path_foto, use_container_width=True)
              else:
                st.warning(f"Foto {nama_file_foto} tidak ditemukan.")
              st.markdown(f"### {row['nama']}")
              st.markdown(f"**🐾 Kategori:** {row['kategori']}")
              st.markdown(f"**📌 Status:** `{row['status']}`")

              if st.button(
                  f"🔍 Lihat Detail & Story", key=f"btn_{row['nama']}_{index}"
              ):
                pilih_hewan(row["nama"])
                st.rerun()

      st.write("")
      if st.button("🔄 Tutup / Pilih Kategori Lain"):
        st.session_state.active_category = None
        st.rerun()

# --- FOOTER / KONTAK WHATSAPP UMUM ---
st.write("")
st.divider()
st.subheader("📍 Tertarik Mengadopsi? Hubungi Kami")
no_hp = "6281390396760"
pesan_wa = (
    "Halo Admin, saya tertarik untuk mengadopsi hewan peliharaan dari Pawsitive"
    " Journey Jogja."
)
link_wa = f"https://wa.me/{no_hp}?text={pesan_wa.replace(' ', '%20')}"
st.link_button("📱 Hubungi Admin via WhatsApp", link_wa)
st.caption(
    "© 2026 Pawsitive Journey - Yogyakarta - Dibangun dengan Streamlit & Google"
    " Sheets"
)