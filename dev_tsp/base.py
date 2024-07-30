import logging
from uuid import uuid4
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, InlineQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# proxy_url = "socks5://user:pass@127.0.0.1:1080"
proxy_url = 'socks5://127.0.0.1:1080'
token = '7294402442:AAEh75iyVxlC8V2nUcO7-J0fqze2tOTASbM'


def error_handler(update, context):
    """Log Errors caused by Updates."""
    logging.error('Update "%s" caused error "%s"', update, context.error)


def print_all_messages(update, context: ContextTypes.DEFAULT_TYPE):
    print(update.to_json())
    print(update.message.to_json())
    # print(f"Received a message from {message.chat.id}: {message.text}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='I''m a bot, please talk to me! 长风几万里')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.to_json())
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def echo1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.to_json())
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# 将输入的小写转大写
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('context.args=', context.args)
    text_caps = ' '.join(context.args).upper()
    print('text_caps=', text_caps)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).proxy(
        proxy_url).get_updates_proxy(proxy_url).build()

    # application.add_error_handler(error_handler)

    # 打印所有消息
    # message_handler = MessageHandler(filters.ALL, print_all_messages)
    # application.add_handler(message_handler)

    # /命令
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # 普通消息
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    echo_handler1 = MessageHandler(filters.TEXT & (~filters.COMMAND), echo1)
    application.add_handler(echo_handler1)

    # /命令
    caps_handler = CommandHandler('caps', caps)
    application.add_handler(caps_handler)

    # inline模式，暂时还用不到
    # inline_caps_handler = InlineQueryHandler(inline_caps)
    # application.add_handler(inline_caps_handler)

    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
