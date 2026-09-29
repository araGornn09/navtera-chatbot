import os
from groq import Groq
from config import Config

def ask_groq_ai(user_message):
    """Groq AI resmi kütüphanesini kullanarak cevap alır."""
    api_key = Config.GROQ_API_KEY
    if not api_key:
        return "Hata: Groq API anahtarı bulunamadı."

    try:
        client = Groq(api_key=api_key)
        model_to_use = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
        
        system_prompt = (
            "Sen NAVTERA adında lüks bir yat kiralama firmasının yardımsever asistanısın. "
            "Amacın ziyaretçilerle kibarca sohbet etmek ve misafirlerin sana yönelttiği soruları cevaplamak: "
            "1. Yatların uzunlukları, 2. Yatları tanıtmak, 3. Hangi yatı tecih edecekleri, 4. Şikayetleri dinleyip çözmek eğer daha büyük bir sorun varsa yönlendirmek: "
            "Kullanıcıya nazikçe yardımcı ol ve eksik bilgileri tek tek sormaya çalış."
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model=model_to_use,
            temperature=0.7
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Bağlantı hatası: {str(e)}"