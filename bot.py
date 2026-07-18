import os
import sys
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Asegurar que Python encuentre los módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database
from ai_router import AIRouter
from modules.trading import TradingModule
from modules.youtube import YouTubeModule

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.owner_id = int(os.getenv('YOUR_TELEGRAM_USER_ID'))
        self.db = Database()
        self.router = AIRouter()
        self.trading = TradingModule(self.db)
        self.youtube = YouTubeModule()
        self.db.add_user(self.owner_id, "owner")  # Permitir owner

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != self.owner_id:
            await update.message.reply_text("Acceso denegado.")
            return
        await update.message.reply_text("¡Bot iniciado! Usa /help")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if not self.db.is_allowed(user_id):
            return
        
        message = update.message.text
        memory = self.db.get_memory(user_id)
        
        model = self.router.choose_model(message)
        response = self.router.generate_response(message, model, memory)
        
        self.db.save_conversation(user_id, message, response, model)
        
        await update.message.reply_text(response)
    
    # Añadir handlers para /trade, /youtube, notifications, etc.

    def run(self):
        app = Application.builder().token(self.token).build()
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        app.run_polling()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()