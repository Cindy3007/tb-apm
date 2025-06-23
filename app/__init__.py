from flask import Flask
from .routes import index_bp
import os

def create_app():
    app = Flask(
        __name__,
        static_folder='../static',
        template_folder='../templates'
    )

    app.config['SECRET_KEY'] = 'kunci-rahasia-unik-dan-acak-milik-anda'
    # -------------------------
    
    app.register_blueprint(index_bp)

    print("Static folder:", os.path.abspath(app.static_folder))

    return app