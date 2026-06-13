import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram.ext import ApplicationBuilder, CommandHandler

# Твой токен
TOKEN = '8820214228:AAFeq2n1P8rtJMBnQr-Br_gDdHgfyBtR7jM'

# 1. Сервер для "проверки пульса" (Health Check)
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    # Render сам задает порт через переменную окружения
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheck)
    print(f"Web server running on port {port}")
    server.serve_forever()

# 2. Логика бота
async def start(update, context):
    await update.message.reply_text("Бот в сети и ждет команды!")

if __name__ == '__main__':
    # Запускаем веб-сервер в отдельном потоке
    threading.Thread(target=run_server, daemon=True).start()
    
    # Запускаем бота
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is polling...")
    app.run_polling()
