import streamlit as st
import base64
import requests # <-- Tambahkan ini untuk mengunduh gambar
from PIL import Image # Tetap diperlukan jika Anda ingin memproses gambar (misal: memeriksa format)
import io # Tetap diperlukan untuk bekerja dengan data gambar dalam memori

# Konfigurasi latar belakang dengan gambar titrasi

def set_bg_from_url(image_url):
    # Dapatkan ekstensi file dari URL (atau tebak berdasarkan Content-Type)
    # Ini mungkin tidak selalu akurat jika URL tidak memiliki ekstensi
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status() # Akan menimbulkan HTTPError untuk status kode 4xx/5xx

        # Mengidentifikasi tipe gambar dari header Content-Type
        content_type = response.headers.get('Content-Type', '').lower()
        if 'image/png' in content_type:
            main_bg_ext = "png"
        elif 'image/jpeg' in content_type:
            main_bg_ext = "jpeg"
        elif 'image/webp' in content_type:
            main_bg_ext = "webp"
        else:
            # Fallback jika tipe tidak dikenal atau tidak ada
            # Anda bisa mencoba menebak dari URL atau menggunakan default
            main_bg_ext = "png" # Default jika tidak bisa mendeteksi

        # Baca konten gambar dalam memori dan encode Base64
        image_bytes = response.content
        base64_img = base64.b64encode(image_bytes).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url(data:image/{main_bg_ext};base64,{base64_img});
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except requests.exceptions.RequestException as e:
        st.warning(f"Gagal mengunduh gambar dari URL: {image_url}. Error: {e}. Menggunakan latar putih default.")
        st.markdown(
            """
            <style>
            .stApp {
                background-color: white; /* Latar putih default */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Terjadi kesalahan lain saat mengatur latar belakang dari URL: {e}. Menggunakan latar putih default.")
        st.markdown(
            """
            <style>
            .stApp {
                background-color: white; /* Latar putih default */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

# --- BAGIAN PANGGILAN FUNGSI YANG DIUBAH ---
# Contoh URL gambar dari Google Images (klik kanan gambar, pilih "Copy image address")
# Ganti URL ini dengan URL gambar yang sebenarnya Anda inginkan.
# Pastikan URL tersebut langsung mengarah ke file gambar (.jpg, .png, .webp, dll.)
# bukan halaman web yang berisi gambar tersebut.
image_url_from_google = "https://images.unsplash.com/photo-1582719468968-c923364f3319?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" # Contoh URL

try:
    set_bg_from_url(image_url_from_google)
except Exception as e:
    st.error(f"Terjadi kesalahan fatal saat mencoba mengatur latar belakang: {e}")
    st.warning("Menggunakan latar putih default.")


# CSS untuk mempercantik tampilan (tetap sama)
st.markdown("""
<style>
div[data-testid="stExpander"] div[role="button"] p {
    font-size: 18px;
    font-weight: bold;
    color: #2a3f5f;
}
.css-1aumxhk {
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

# ... (sisa kode aplikasi Streamlit Anda) ...
