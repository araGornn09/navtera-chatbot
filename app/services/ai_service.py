import os
from groq import Groq
from config import Config

def get_active_model(client):
    """Groq üzerindeki aktif modelleri sorgulayıp çalışan ilk modeli seçer."""
    try:
        models_list = client.models.list()
        if models_list and models_list.data:
            active_ids = [m.id for m in models_list.data]
            # Öncelikli aktif modeller
            preferred_models = ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.6-27b"]
            for model_id in preferred_models:
                if model_id in active_ids:
                    return model_id
            return active_ids[0]
    except Exception:
        pass
    return "openai/gpt-oss-20b"

def ask_groq_ai(user_message):
    """Groq AI resmi kütüphanesini kullanarak cevap alır."""
    api_key = Config.GROQ_API_KEY
    if not api_key:
        return "Hata: Groq API anahtarı bulunamadı."

    try:
        client = Groq(api_key=api_key)
        model_to_use = get_active_model(client)
        
        system_prompt = (
            "Sen NAVTERA adında lüks bir yat kiralama firmasının yardımsever asistanısın. "
            "Amacın ziyaretçilerle kibarca sohbet etmek ve rezervasyon için şu 4 bilgiyi toplamak: "
            "1. İsim-Soyisim, 2. Telefon Numarası, 3. Hangi liman/lokasyon, 4. Hangi tarih. "
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