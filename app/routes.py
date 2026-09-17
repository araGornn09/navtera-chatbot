import re
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify
from app.database import init_db, save_lead, get_all_leads
from app.services.ai_service import ask_groq_ai

# Route tanimlamalari icin Blueprint yapisi
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Ana sayfa - Chatbot arayuzu"""
    return render_template('index.html')

@main.route('/dashboard')
def dashboard():
    """Yonetim paneli - Musteri kayitlarini listeler"""
    leads = get_all_leads()
    return render_template('dashboard.html', leads=leads)

@main.route('/api/chat', methods=['POST'])
def chat():
    """Chatbot ile mesajlasma uc noktasi"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Lutfen gecerli bir mesaj gonderin.'}), 400

    # --- MÜŞTERİ YAKALAMA RADARI (YENİ EKLENEN KISIM) ---
    # Kullanıcının mesajında Türkiye formatında bir telefon numarası arar
    telefon_match = re.search(r'0?\s*5\d{2}\s*\d{3}\s*\d{2}\s*\d{2}', user_message)
    
    if telefon_match:
        telefon = telefon_match.group(0).strip()
        tarih = datetime.now().strftime("%d-%m-%Y %H:%M")
        isim = "Sohbet Müşterisi" 
        mesaj_detayi = user_message[:100]  # Ne yazdığını Wix'te görebilmen için
        
        # Numarayı bulduğu an veritabanına (arka planda sessizce) kaydeder
        save_lead(isim, telefon, mesaj_detayi, tarih)
    # -----------------------------------------------------

    # AI Servisine mesaji gonderip cevap aliyoruz
    bot_response = ask_groq_ai(user_message)
    return jsonify({'response': bot_response})

@main.route('/api/lead', methods=['POST'])
def add_lead():
    """Form uzerinden gelen musteri verilerini kaydeder"""
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    port = data.get('port')
    date = data.get('date')
    
    if name and phone:
        save_lead(name, phone, port, date)
        return jsonify({'status': 'success', 'message': 'Kayit basariyla olusturuldu.'})
        
    return jsonify({'status': 'error', 'message': 'Eksik bilgi gonderildi.'}), 400

@main.route('/api/leads', methods=['GET'])
def api_get_leads():
    """Wix'in verileri JSON olarak çekeceği endpoint"""
    leads = get_all_leads()
    return jsonify({"leads": leads})

@main.route('/api/test-ekle', methods=['GET'])
def test_veri_ekle():
    """Tiklandiginda veritabanina zorla kayit ekleyen sihirli link"""
    save_lead("Arda Bayrakgil", "05551112233", "Bot Testi", "18-09-2026")
    return "Harika! Test kaydi veritabanina eklendi. Simdi Wix'e gecip onizleme yapabilirsin!"