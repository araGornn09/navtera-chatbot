# Navtera - Yapay Zeka Destekli Yat Kiralama Platformu

Navtera, kullanıcıların chatbot ile sohbet ederek yat kiralama süreçlerini yönetebildiği, yapay zeka entegreli modern bir web platformudur.

## 🚀 Kullanılan Teknolojiler
- **Backend:** Python, Flask, Gunicorn
- **Frontend / Arayüz:** Wix Studio (Velo)
- **Yapay Zeka & Servisler:** Groq AI API, Regex tabanlı akıllı veri yakalama radarı
- **Hosting:** Render (Cloud Hosting)

## 📌 Projenin Amacı ve Çalışma Mantığı
1. Müşteri Wix üzerindeki chatbot ile sohbet ederken adını, telefonunu, gitmek istediği limanı ve kiralama tarihini mesajına yazar.
2. Flask tabanlı backend sunucusu mesajı analiz eder, akıllı radarlar sayesinde bilgileri cımbızlar ve veritabanına kaydeder.
3. Wix Studio Dashboard paneli, `/api/leads` uç noktası üzerinden bu verileri canlı olarak çekip şık bir repeater (liste) yapısında görüntüler.

## ⚙️ Nasıl Çalıştırılır?
1. Repoyu klonlayın: `git clone <repo-url>`
2. Gerekli kütüphaneleri yükleyin: `pip install -r requirements.txt`
3. Projeyi yerel ortamda başlatın: `python run.py`