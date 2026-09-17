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
    """Chatbot ile mesajlasma uc noktasi ve akilli musteri radari"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Lutfen gecerli bir mesaj gonderin.'}), 400

    # --- AKILLI MÜŞTERİ YAKALAMA RADARI ---
    telefon_match = re.search(r'0?\s*5\d{2}\s*\d{3}\s*\d{2}\s*\d{2}', user_message)
    
    if telefon_match:
        telefon = telefon_match.group(0).strip()
        kayit_tarihi = datetime.now().strftime("%d-%m-%Y %H:%M")
        
        # 1. İSİM BULMA
        text_before_phone = user_message[:telefon_match.start()].strip()
        lines = text_before_phone.split('\n')
        if lines and lines[0].strip():
            isim_kelimeleri = lines[0].strip().split()
            if len(isim_kelimeleri) > 3:
                isim = " ".join(isim_kelimeleri[-2:]) 
            else:
                isim = lines[0].strip()
        else:
            isim = "İsim Belirtilmedi"
            
        # 2. LİMAN BULMA
        port = "Belirtilmedi"
        limanlar = ["istanbul", "bodrum", "göcek", "gocek", "fethiye", "marmaris", "antalya", "izmir", "çeşme", "cesme"]
        lower_msg = user_message.lower()
        for liman in limanlar:
            if liman in lower_msg:
                port = liman.capitalize()
                break
                
        # 3. KİRALAMA TARİHİ BULMA (Örn: 16/10/2026, 16.10.2026, 16-10)
        # Mesajın içindeki gün/ay/yıl veya gün.ay.yıl formatlarını yakalar
        tarih_match = re.search(r'\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}', user_message)
        kiralama_tarihi = tarih_match.group(0) if tarih_match else "Belirtilmedi"

        # 4. WIX İÇİN ŞIK FORMATLAMA
        # Port sütununa liman ve kiralama tarihini, Date sütununa ise kayıt tarihini yazıyoruz.
        gosterilecek_detay = f"Liman: {port} | Kiralama: {kiralama_tarihi}"
        gosterilecek_kayit = f"Kayıt Tarihi: {kayit_tarihi}"
        
        # Veritabanına tertemiz gönderiyoruz
        save_lead(isim.title(), telefon, gosterilecek_detay, gosterilecek_kayit)
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