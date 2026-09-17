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
        return jsonify({'status': 'success', 'message': 'Kayıt başarıyla oluşturuldu.'})
    
    return jsonify({'status': 'error', 'message': 'Eksik bilgi gönderildi.'}), 400

@main.route('/api/leads', methods=['GET'])
def api_get_leads():
    """Wix'in verileri JSON olarak çekeceği endpoint"""
    leads = get_all_leads() # Artık veritabanından, Wix formatında çekiyor
    return jsonify({"leads": leads})