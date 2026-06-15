import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = '8820214228:AAFeq2n1P8rtJMBnQr-Br_gDdHgfyBtR7jM'

# 1. Веб-сервер для "удержания" Render в сети
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
        
def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheck)
    server.serve_forever()

# 2. Логика бота с кнопками
async def start(update, context):
    kb = [[InlineKeyboardButton("ВЫКЛЮЧИТЬ ПК 🛑", callback_data='off')]]
    reply_markup = InlineKeyboardMarkup(kb)
    await update.message.reply_text("ПК на связи! Выбери действие:", reply_markup=reply_markup)

async def button(update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'off':
        await query.edit_message_text(text="Команда на выключение отправлена!")
        # Тут будет интеграция с твоим скриптом на ПК

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
