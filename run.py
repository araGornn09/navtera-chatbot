from flask import Flask
from flask_cors import CORS
from config import Config
from app.database import init_db
from app.routes import main

def create_app():
    """Flask uygulamasini baslatan fabrika fonksiyonu"""
    app = Flask(__name__, template_folder='app/templates')
    app.config.from_object(Config)

    # Tarayici erisim izinlerini (CORS) tanimliyoruz
    CORS(app)

    # Veritabanini baslatiyoruz
    with app.app_context():
        init_db()

    # Route baglantisini yapiyoruz
    app.register_blueprint(main)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)