import sqlite3
import os

# Veritabanı dosyasının yolu (app klasörü içinde navtera.db olarak tutulacak)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'navtera.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Verileri sözlük (dictionary) formatında çekmek için
    return conn

def init_db():
    """Veritabanını ve tabloyu oluşturur"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            port TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_lead(name, phone, port, date):
    """Yeni gelen lead'i veritabanına kaydeder"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO leads (name, phone, port, date)
        VALUES (?, ?, ?, ?)
    ''', (name, phone, port, date))
    conn.commit()
    conn.close()

def get_all_leads():
    """Veritabanındaki tüm lead'leri Wix'in istediği formatta getirir"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()

    leads = []
    for row in rows:
        # Wix'in Text elementlerine bağladığımız isimlere göre ('isim', 'telefon', 'mesaj') eşitliyoruz
        leads.append({
            "_id": str(row["id"]),  # İŞTE BÜTÜN SORUNU ÇÖZEN WIX ID'Sİ (String olmak zorunda)
            "isim": row["name"],
            "telefon": row["phone"],
            "mesaj": f"Tarih: {row['date']} | Port: {row['port']}"
        })
    return leads