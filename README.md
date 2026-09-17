# SmartLead AI - Navtera Asistanı

Bu proje, ziyaretçilerle yapay zekâ üzerinden akıllı sohbet eden ve potansiyel müşteri (lead) bilgilerini toplayıp yöneten modüler bir Flask ve Wix Studio web uygulamasıdır.

## 🏗️ Mimari ve Katmanlar (Separation of Concerns)
Proje, her dosyanın tek bir sorumluluğu olacağı şekilde katmanlı bir mimariyle geliştirilmiştir:
- **`run.py`**: Uygulamayı başlatan ana giriş noktası.
- **`config.py`**: Ortam değişkenlerini (`.env`) ve yapılandırmaları yöneten katman.
- **`app/database.py`**: SQLite veritabanı bağlantısı ve tablo yönetimi (SQL sorguları yalnızca burada yer alır).
- **`app/services/ai_service.py`**: Groq AI (Llama 3) entegrasyonunu ve yapay zekâ çağrılarını izole eden servis katmanı.
- **`app/routes.py`**: HTTP isteklerini karşılayan Blueprint tabanlı rota kontrolcüsü.

## 🛠️ Kullanılan Teknolojiler
- **Backend:** Python, Flask, Flask-CORS, SQLite, Requests
- **Yapay Zekâ:** Groq API (`llama-3.1-8b-instant`)
- **Frontend & Arayüz:** Wix Studio, Velo (JavaScript)
- **Yayınlama (Deployment):** GitHub, Render

## 🚀 Kurulum ve Çalıştırma (Yerel Ortam)

Projeyi yerel makinenizde çalıştırmak için şu adımları izleyin:

1. **Depoyu klonlayın:**
   ```bash
   git clone <repo-url>
   cd smartlead-ai