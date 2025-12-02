from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = "8550496700:AAHvzLXh3XGA8sgz4FVQmla_fh74D33ZtTs"
ADMIN_ID = 5784318442  # твой Telegram ID

terminals = [
    "Terminal #1 – ЖК Nomad",
    "Terminal #2 – ЖК Турксиб",
    "Terminal #3 – Mega Center"
]

SELECT_TERMINAL, SELECT_PROBLEM = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📄 Сообщить о проблеме"], ["☎ Техподдержка"]]
    await update.message.reply_text(
        "Добро пожаловать в SaitovPrint Support!\n\nЧем я могу помочь?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def report_problem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[t] for t in terminals]
    await update.message.reply_text(
        "Выберите терминал:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return SELECT_TERMINAL

async def select_terminal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["terminal"] = update.message.text

    keyboard = [
        ["📄 Нет бумаги"],
        ["🖨 Не печатает"],
        ["📷 Не сканирует"],
        ["💸 Проблема с оплатой"],
        ["⚙ Другая ошибка"]
    ]

    await update.message.reply_text(
        "Какая проблема возникла?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return SELECT_PROBLEM

async def send_problem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    terminal = context.user_data["terminal"]
    problem = update.message.text

    text = (
        f"⚠ Сообщение от клиента\n\n"
        f"Терминал: {terminal}\n"
        f"Ошибка: {problem}\n"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=text)
    await update.message.reply_text("Спасибо! Техподдержка получила ваше сообщение.")
    return ConversationHandler.END

async def help_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Телефон техподдержки:\n📞 +7 777 777 77 77")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("📄 Сообщить о проблеме"), report_problem)],
        states={
            SELECT_TERMINAL: [MessageHandler(filters.TEXT, select_terminal)],
            SELECT_PROBLEM: [MessageHandler(filters.TEXT, send_problem)],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.Regex("☎ Техподдержка"), help_contact))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
