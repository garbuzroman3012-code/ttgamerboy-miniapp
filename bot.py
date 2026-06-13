import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8820214228:AAFeq2n1P8rtJMBnQr-Br_gDdHgfyBTr7jM'
MY_ID = 8252113012

# Время последнего сигнала от ПК
last_ping_time = 0
shutdown_requested = False

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global last_ping_time, shutdown_requested
        if self.path == "/ping":
            last_ping_time = time.time()  # Комп сигналит, что он онлайн
            if shutdown_requested:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"SHUTDOWN")
                shutdown_requested = False
                return
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is active")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), WebServerHandler)
    server.serve_forever()

def get_keyboard(is_online):
    if is_online:
        return InlineKeyboardMarkup([[InlineKeyboardButton("ВЫКЛЮЧИТЬ ❎", callback_data='off')]])
    else:
        return InlineKeyboardMarkup([[InlineKeyboardButton("ВКЛЮЧИТЬ ✅", callback_data='on')]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID: 
        return
    
    # Если последний пинг был меньше 10 секунд назад — комп онлайн
    is_online = (time.time() - last_ping_time) < 10
    status = "Включен ✅" if is_online else "Выключен ❎"
    
    await update.message.reply_text(
        f"Привет Klaxer!\nСтатус ПК: {status}\n\nВыбери действие:",
        reply_markup=get_keyboard(is_online)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global shutdown_requested
    query = update.callback_query
    if update.effective_user.id != MY_ID: 
        return
    await query.answer()

    is_online = (time.time() - last_ping_time) < 10

    if query.data == 'off' and is_online:
        shutdown_requested = True
        await query.edit_message_text("Отправлена команда на выключение... Ждем ответа ПК.")
    else:
        status = "Включен ✅" if is_online else "Выключен ❎"
        await query.edit_message_text(f"Статус ПК: {status}", reply_markup=get_keyboard(is_online))

def main():
    threading.Thread(target=run_web_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == '__main__':
    main()
