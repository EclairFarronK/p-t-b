import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# proxy_url = "socks5://user:pass@127.0.0.1:1080"
proxy_url = 'socks5://127.0.0.1:1080'
token = '7294402442:AAEh75iyVxlC8V2nUcO7-J0fqze2tOTASbM'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='I''m a bot, please talk to me! 长风几万里')


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).proxy(
        proxy_url).get_updates_proxy(proxy_url).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
