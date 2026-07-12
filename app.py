import os
import telebot
import requests
import base64
import io
from PIL import Image

TOKEN_TELEGRAM = "8693676560:AAGpkdatG3w05C1Mwi7TB-qTY3Ex93F1Meo"
CHAVE_GEMINI = "AQ.Ab8RN6LYgZ9NZpoG-uO1X-vS2AImw5g"

bot = telebot.TeleBot(TOKEN_TELEGRAM)

print("Bot Universal Iniciado!")

@bot.message_handler(content_types=['photo'])
def responder_foto(mensagem):
    status = bot.reply_to(mensagem, "📥 Analisando imagem e detectando o idioma... Aguarde.")
    try:
        # Baixa a foto vinda do Telegram
        file_info = bot.get_file(mensagem.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Converte a imagem para Base64 para enviar na chamada de internet
        encoded_image = base64.b64encode(downloaded_file).decode('utf-8')
        
        # URL da API do Gemini adaptada para o formato novo de chave
        url = f"https://googleapis.com{CHAVE_GEMINI}"
        
        headers = {"Content-Type": "application/json"}
        
        prompt = (
            "Analise esta imagem (página de quadrinho, mangá, manhwa ou comic). "
            "Identifique o idioma original do texto nos balões e faça uma tradução completa "
            "para o português brasileiro. A tradução deve ser natural, fluida e adaptada ao contexto "
            "da história. Retorne apenas o texto final traduzido, organizado por balões ou diálogos."
        )
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": "image/png",
                            "data": encoded_image
                        }
                    }
                ]
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        res_json = response.json()
        
        # Extrai o texto da resposta da Google
        texto_traduzido = res_json['candidates'][0]['content']['parts'][0]['text']
        
        bot.delete_message(mensagem.chat.id, status.message_id)
        bot.reply_to(mensagem, f"🇧🇷 **Tradução (Qualquer Idioma):**\n\n{texto_traduzido}")
        
    except Exception as e:
        bot.edit_message_text(f"❌ Erro ao processar: {str(e)}", message_id=status.message_id, chat_id=mensagem.chat.id)

bot.infinity_polling()
