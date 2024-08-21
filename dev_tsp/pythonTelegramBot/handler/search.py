from typing import List
from telegram.constants import ParseMode
from dev_tsp.mongodb.connection import mongoClient
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, Updater, CommandHandler, CallbackQueryHandler, CallbackContext

db = mongoClient['telegram_db']
keyboard = [
    [
        InlineKeyboardButton("选项 1", callback_data='1'),
        InlineKeyboardButton("选项 2", callback_data='2'),
    ],
    [InlineKeyboardButton("选项 3", callback_data='3')],
]


# 参数为list，返回一个
def assemble(result_list: List[dict]) -> str:
    message = 'result:\n'
    for i in result_list:
        title = i.get('title')
        username = i.get('username')
        url = 'https://t.me/' + username
        message = message + f'[{title}]({url})\n'
    return message


# 查询数据库，然后将消息返回
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        # todo 7188701260
        # todo 告诉那边是搜索什么
        await context.bot.send_message(chat_id=7188701260, text=text)
    except Exception as e:
        print(f'An error occurred: {e}')
    # message、group/channel
    result_list = list(db.chat_channel_megagroup.find({'title': {'$regex': f'{text}'}}).limit(1))
    message = assemble(result_list)

    # todo 最好先设置一个返回的模板，到时候直接往里面填就行了
    await update.message.reply_text(text=message,
                                    reply_markup=InlineKeyboardMarkup(keyboard),
                                    parse_mode=ParseMode.MARKDOWN_V2,
                                    disable_web_page_preview=True)
