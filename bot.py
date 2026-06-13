from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8820214228:AAFeq2n1P8rtJMBnQr-Br_gDdHgfyBtR7jM'
MY_ID = 8252113012 # СЮДА ТВОЙ ID

# Начальный статус
status = "Выключен"

def get_keyboard(current_status):
    if current_status == "Включен":
        # Если включен: ВКЛЮЧИТЬ подсвечено, ВЫКЛЮЧИТЬ обычно
        keyboard = [[
            InlineKeyboardButton("ВКЛЮЧИТЬ ✅", callback_data='on'),
            InlineKeyboardButton("ВЫКЛЮЧИТЬ ❎", callback_data='off')
        ]]
    else:
        # Если выключен: ВКЛЮЧИТЬ обычно, ВЫКЛЮЧИТЬ подсвечено
        keyboard = [[
            InlineKeyboardButton("ВКЛЮЧИТЬ ❎", callback_data='on'),
            InlineKeyboardButton("ВЫКЛЮЧИТЬ ✅", callback_data='off')
        ]]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID: return
    text = f"Привет Klaxer!\nСтатус пк: {status}\n\nВыбери что хочешь сделать!"
    await update.message.reply_text(text, reply_markup=get_keyboard(status))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global status
    query = update.callback_query
    if update.effective_user.id != MY_ID: return
    await query.answer()

    if query.data == 'on':
        status = "Включен"
        text = f"Привет Klaxer!\nСтатус пк: {status}\n\nВыбери что хочешь сделать!"
        await query.edit_message_text(text, reply_markup=get_keyboard(status))
        
    elif query.data == 'off':
        status = "Выключен"
        text = f"Привет Klaxer!\nСтатус пк: {status}\n\nВыбери что хочешь сделать!"
        await query.edit_message_text(text, reply_markup=get_keyboard(status))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == '__main__':
    main()
