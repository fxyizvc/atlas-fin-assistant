import os
import logging
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from groq import Groq
from ai_engine import generate_response
from document_handler import handle_document

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Atlas AI Financial Assistant")

telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text
    chat_id = update.message.chat_id
    
    logger.info(f"Received text from {chat_id}: {user_text}")
    
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    response_text = generate_response(chat_id, user_text)
    await update.message.reply_text(response_text)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.voice:
        return

    chat_id = update.message.chat_id
    logger.info(f"Received voice message from {chat_id}")
    
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        voice_file = await context.bot.get_file(update.message.voice.file_id)
        file_path = f"voice_{chat_id}.ogg"
        await voice_file.download_to_drive(file_path)

        with open(file_path, "rb") as audio_file:
            transcription = groq_client.audio.transcriptions.create(
                file=(file_path, audio_file.read()),
                model="whisper-large-v3",
                response_format="text"
            )

        if os.path.exists(file_path):
            os.remove(file_path)

        user_text = transcription.strip()
        logger.info(f"Voice Transcribed [{chat_id}]: {user_text}")

        response_text = generate_response(chat_id, user_text)
        
        reply = f"🎤 *Transcribed Voice:* \"_{user_text}_\"\n\n{response_text}"
        await update.message.reply_text(reply, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error processing voice note: {str(e)}")
        await update.message.reply_text("I couldn't process that voice message. Could you try re-recording or typing?")

# Register Message Handlers
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
telegram_app.add_handler(MessageHandler(filters.VOICE, handle_voice))
telegram_app.add_handler(MessageHandler(filters.Document.PDF, handle_document))

@app.on_event("startup")
async def startup_event():
    await telegram_app.initialize()
    await telegram_app.start()
    webhook_url = f"{os.getenv('WEBHOOK_URL')}/webhook"
    await telegram_app.bot.set_webhook(url=webhook_url)
    logger.info(f"Webhook set to: {webhook_url}")

@app.on_event("shutdown")
async def shutdown_event():
    await telegram_app.stop()
    await telegram_app.shutdown()

@app.get("/")
def health_check():
    return {"status": "Atlas Financial Assistant Webhook Active"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}