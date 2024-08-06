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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='I''m a bot, please talk to me! 长风几万里')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # todo 普通消息需要将消息保存
    print(update.message.to_json())
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

    # /命令
    start_handler = CommandHandler(command='start', callback=start)
    application.add_handler(start_handler)

    # 普通消息
    echo_handler = MessageHandler(filters=filters.TEXT & (~filters.COMMAND), callback=echo)
    application.add_handler(echo_handler)

    # /命令
    caps_handler = CommandHandler(command='caps', callback=caps)
    application.add_handler(caps_handler)

    # inline模式，暂时还用不到
    # inline_caps_handler = InlineQueryHandler(inline_caps)
    # application.add_handler(inline_caps_handler)

    # Other handlers
    unknown_handler = MessageHandler(filters=filters.COMMAND, callback=unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
