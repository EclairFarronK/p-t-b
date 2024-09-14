from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message()
    await update.message.reply_text()

    query.edit_message_text(text="你点击了按钮1")
