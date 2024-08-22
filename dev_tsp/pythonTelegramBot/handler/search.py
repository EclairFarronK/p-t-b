import asyncio
import re
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
        title = escape(title)

        count = i.get('count')
        count = escape(count)

        username = i.get('username')
        url = 'https://t.me/' + username
        message = message + f'[{title}\-\-{count}]({url})\n'
    return message


def escape(string: str) -> str:
    return re.sub(r'([\(\)\-\.])', r'\\\1', string)


# 查询数据库，然后将消息返回
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # send_message
    try:
        await context.bot.send_message(chat_id=7188701260, text=text)
    except Exception as e:
        print(f'An error occurred: {e}')

    # todo sleep
    await asyncio.sleep(delay=2)

    # search
    result_list = list(
        db.chat_channel_megagroup_test.find({'title': {'$regex': f'{text}'}},
                                            {'_id': 0, 'title': 1, 'count': 1, 'username': 1}).limit(20))
    message = assemble(result_list)

    # todo 最好先设置一个返回的模板，到时候直接往里面填就行了
    await update.message.reply_text(text=message,
                                    reply_markup=InlineKeyboardMarkup(keyboard),
                                    parse_mode=ParseMode.MARKDOWN_V2,
                                    disable_web_page_preview=True)
