import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = '8820214228:AAFeq2n1P8rtJMBnQr-Br_gDdHgfyBTr7jM'
# Переменная-флаг для команды выключения
shutdown_requested = False

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global shutdown_requested
        if self.path == "/ping":
            self.send_response(200)
            self.end_headers()
            if shutdown_requested:
                self.wfile.write(b"SHUTDOWN")
                shutdown_requested = False
            else:
                self.wfile.write(b"OK")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is active")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), WebServer)
    server.serve_forever()

async def start(update, context):
    kb = [[InlineKeyboardButton("ВЫКЛЮЧИТЬ ПК 🛑", callback_data='off')]]
    await update.message.reply_text("ПК на связи! Выбери действие:", reply_markup=InlineKeyboardMarkup(kb))

async def button(update, context):
    global shutdown_requested
    query = update.callback_query
    if query.data == 'off':
        shutdown_requested = True
        await query.answer("Отправляю команду на выключение!")

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
