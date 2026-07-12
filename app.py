import os
import telebot
from google import genai
from PIL import Image
import io

TOKEN_TELEGRAM = "8693676560:AAGpkdatG3w05C1Mwi7TB-qTY3Ex93F1Meo"
# Configurando a chave no formato novo exigido pela Google
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6LYgZ9NZpoG-uO1X-vS2AImw5g"

bot = telebot.TeleBot(TOKEN_TELEGRAM)
client = genai.Client()

print("Bot Universal Iniciado!")

@bot.message_handler(content_types=['photo'])
def responder_foto(mensagem):
    status = bot.reply_to(mensagem, "📥 Analisando imagem e detectando o idioma... Aguarde.")
    try:
        file_info = bot.get_file(mensagem.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        imagem_pil = Image.open(io.BytesIO(downloaded_file))
        
        prompt = (
            "Analise esta imagem (página de quadrinho, mangá, manhwa ou comic). "
            "Identifique o idioma original do texto nos balões e faça uma tradução completa "
            "para o português brasileiro. A tradução deve ser natural, fluida e adaptada ao contexto "
            "da história. Retorne apenas o texto final traduzido, organizado por balões ou diálogos."
        )
        
        resposta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[imagem_pil, prompt]
        )
        
        bot.delete_message(mensagem.chat.id, status.message_id)
        bot.reply_to(mensagem, f"🇧🇷 **Tradução (Qualquer Idioma):**\n\n{resposta.text}")
        
    except Exception as e:
        bot.edit_message_text(f"❌ Erro ao processar: {str(e)}", message_id=status.message_id, chat_id=mensagem.chat.id)

bot.infinity_polling()
