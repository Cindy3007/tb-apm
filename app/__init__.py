from flask import Flask
from .routes import index_bp
import os

def create_app():
    # Menggunakan konfigurasi path yang Anda berikan
    app = Flask(
        __name__,
        static_folder='../static',
        template_folder='../templates'
    )

    # --- PERBAIKAN DI SINI ---
    # WAJIB: Tambahkan secret key untuk mengaktifkan session.
    # Ini diperlukan agar kita bisa menyimpan hasil rekomendasi dari API
    # untuk ditampilkan di halaman selanjutnya.
    app.config['SECRET_KEY'] = 'kunci-rahasia-unik-dan-acak-milik-anda'
    # -------------------------
    
    app.register_blueprint(index_bp)

    # Menggunakan print statement dari kode Anda
    print("Static folder:", os.path.abspath(app.static_folder))

    return app