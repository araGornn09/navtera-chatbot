import os
import re
from groq import Groq
from config import Config
from app.knowledge import build_knowledge_text

SYSTEM_PROMPT = (
    "Sen NAVTERA adında lüks bir yat kiralama firmasının yardımsever asistanısın. "
    "Ziyaretçilerle kibar ve samimi bir dille sohbet eder, yatlar ve lokasyonlar hakkındaki soruları cevaplarsın.\n\n"
    "GÖREVLERİN:\n"
    "1. Müşteri bir yatın adını yazdığında (eksik ya da hatalı yazsa bile, örn. 'riva', 'azimut', 'sunseeker') "
    "aşağıdaki bilgi tabanından o yatı bul ve TÜM bilgilerini düzenli bir şekilde ver: tip, uzunluk, "
    "gündüz misafir kapasitesi, konaklama kapasitesi, motor, maksimum hız ve kısa tanıtım.\n"
    "2. Müşteri bir lokasyon sorduğunda (İstanbul, Bodrum, Göcek) o bölgeyi tanıt: öne çıkan yerler, rotalar ve sezon.\n"
    "3. Müşterinin kişi sayısı, konaklama isteği, hız / konfor tercihine göre en uygun yatları öner.\n"
    "4. Şikayetleri dinle ve çözmeye çalış; daha büyük bir sorun varsa ekibimize yönlendir.\n"
    "5. Rezervasyon için müşterinin adını, telefon numarasını, lokasyonu ve tarihini nazikçe iste.\n\n"
    "KURALLAR:\n"
    "- SADECE bilgi tabanındaki bilgileri kullan. Bilgi tabanında olmayan bir yat, özellik veya bilgi uydurma.\n"
    "- Fiyat, müsaitlik, hangi yatın hangi lokasyonda olduğu ve kalkış marinası bilgileri sende yok. "
    "Bunlar sorulursa ekibimizin en kısa sürede dönüş yapacağını söyle ve iletişim bilgilerini iste.\n"
    "- Müşteri filoda olmayan bir yat sorarsa, o yatın filomuzda olmadığını söyle ve benzer bir alternatif öner.\n"
    "- Cevapların sohbet penceresine uygun olsun: kısa paragraflar ve '•' ile madde işaretleri kullan, gereksiz uzatma.\n"
    "- Markdown KULLANMA (**, ##, tablo yok); sohbet penceresi düz metin gösterir.\n"
    "- Müşteri hangi dilde yazarsa o dilde cevap ver.\n\n"
    "BİLGİ TABANI:\n"
    + build_knowledge_text()
)

MAX_HISTORY = 10


def ask_groq_ai(user_message, history=None):
    """Groq AI resmi kütüphanesini kullanarak cevap alır."""
    api_key = Config.GROQ_API_KEY
    if not api_key:
        return "Hata: Groq API anahtarı bulunamadı."

    try:
        client = Groq(api_key=api_key)
        model_to_use = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

        # Onceki mesajlar: bot "bunun hızı ne?" gibi takip sorularında hangi yattan bahsedildiğini bilsin
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in (history or [])[-MAX_HISTORY:]:
            if (isinstance(msg, dict) and msg.get("role") in ("user", "assistant")
                    and isinstance(msg.get("content"), str)):
                messages.append({"role": msg["role"], "content": msg["content"][:2000]})
        messages.append({"role": "user", "content": user_message})

        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model_to_use,
            temperature=0.4
        )

        reply = chat_completion.choices[0].message.content or ""
        # Sohbet penceresi duz metin gosterdigi icin markdown isaretlerini temizliyoruz
        reply = reply.replace("**", "")
        reply = re.sub(r"^#+\s*", "", reply, flags=re.MULTILINE)
        return reply.strip()
    except Exception as e:
        return f"Bağlantı hatası: {str(e)}"
