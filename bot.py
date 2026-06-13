import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram.ext import ApplicationBuilder, CommandHandler

# Твой токен (проверь, чтобы он был верным)
TOKEN = '8820214228:AAFeq2n1P8rtJMBnQr-Br_gDdHgfyBTr7jM'

# 1. Веб-сервер для "удержания" Render в режиме Live
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheck)
    server.serve_forever()

# 2. Логика бота
async def start(update, context):
    await update.message.reply_text("Бот работает!")

if __name__ == '__main__':
    # Запускаем веб-часть
    threading.Thread(target=run_server, daemon=True).start()
    
    # Запускаем бота
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
