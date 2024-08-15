from typing import List
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


# todo 随意切换，然后查询不同的数据库
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
    # 查询数据库
    result_list = list(db.chat_channel_megagroup.find({'title': {'$regex': f'{text}'}}).limit(2))
    message = assemble(result_list)

    # todo 最好先设置一个返回的模板，到时候直接往里面填就行了
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.MARKDOWN_V2,
                                   disable_web_page_preview=True)
