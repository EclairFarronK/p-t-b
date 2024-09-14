import yaml
import logging
from uuid import uuid4
from handler.search import callback_search, callback_search_page
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler

with open('./config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    token = config['bot']['token01']
    proto = config['proxy']['proto']
    ip = config['proxy']['ip']
    port = config['proxy']['port']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
proxy = f'{proto}://{ip}:{port}'
bot_token = token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='I''m a bot, please talk to me!')


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
    application = ApplicationBuilder().token(bot_token).proxy(
        proxy).get_updates_proxy(proxy).build()

    # /命令
    # application.add_handler(CommandHandler(command='start', callback=start))

    # 普通消息
    # todo & (~filters.COMMAND)怎么实现的？
    application.add_handler(MessageHandler(filters=filters.TEXT & (~filters.COMMAND), callback=callback_search))
    application.add_handler(CallbackQueryHandler(callback=callback_search_page))

    # /命令
    # application.add_handler(CommandHandler(command='caps', callback=caps))

    # inline模式，暂时还用不到
    # inline_caps_handler = InlineQueryHandler(inline_caps)
    # application.add_handler(inline_caps_handler)

    # Other handlers
    # application.add_handler(MessageHandler(filters=filters.COMMAND, callback=unknown))

    application.run_polling()
