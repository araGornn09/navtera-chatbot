import sqlite3
from config import Config

def get_db_connection():
    """Veritabani baglantisi olusturur."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Veritabani tablosunu yoksa olusturur."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Musteri bilgilerini (Lead) tutacak tabloyu olusturuyoruz
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            port TEXT,
            date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_lead(name, phone, port, date):
    """Yeni bir musteri bilgisini veritabanına kaydeder."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO leads (name, phone, port, date)
        VALUES (?, ?, ?, ?)
    ''', (name, phone, port, date))
    
    conn.commit()
    conn.close()

def get_all_leads():
    """Tum kayitli musterileri getirir (Dashboard icin)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM leads ORDER BY created_at DESC')
    leads = cursor.fetchall()
    
    conn.close()
    return leads