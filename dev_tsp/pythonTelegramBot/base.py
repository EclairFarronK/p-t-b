import yaml
import logging
from uuid import uuid4
from handler.search import search
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

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
    await context.bot.send_message(chat_id=update.effective_chat.id, text='I''m a bot, please talk to me! 长风几万里')


# async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print(update.message.to_json())
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


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
    start_handler = CommandHandler(command='start', callback=start)
    application.add_handler(start_handler)

    # 普通消息
    echo_handler = MessageHandler(filters=filters.TEXT & (~filters.COMMAND), callback=search)
    application.add_handler(echo_handler)

    # /命令
    caps_handler = CommandHandler(command='caps', callback=caps)
    application.add_handler(caps_handler)

    # inline模式，暂时还用不到
    # inline_caps_handler = InlineQueryHandler(inline_caps)
    # application.add_handler(inline_caps_handler)

    # todo 启动之后，输入关键词，查询数据库，然后返回
    # todo 能查询group，channel，text

    # Other handlers
    unknown_handler = MessageHandler(filters=filters.COMMAND, callback=unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
