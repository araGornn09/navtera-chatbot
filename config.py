import os
from dotenv import load_dotenv

# .env dosyasindaki gizli bilgileri yukluyoruz
load_dotenv()

class Config:
    # Flask icin gizli anahtar
    SECRET_KEY = os.getenv('SECRET_KEY', 'varsayilan-gizli-anahtar')
    
    # Groq AI API Anahtari
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    
    # Kullanilacak AI Servisi
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'groq')
    
    # SQLite Veritabani dosyamizin adi ve yolu
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, 'navtera.db')