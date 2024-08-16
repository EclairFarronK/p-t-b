from typing import List
from telegram.constants import ParseMode
from dev_tsp.mongodb.connection import mongoClient
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, Updater, CommandHandler, CallbackQueryHandler, CallbackContext

db = mongoClient['telegram_db']


# todo 启动之后，输入关键词，查询数据库，然后返回
# todo 能查询group，channel，text
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
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=message,
                                   parse_mode=ParseMode.MARKDOWN_V2,
                                   disable_web_page_preview=True)


# 定义一个命令处理函数，发送消息并带有可选项按钮
async def startt(update: Update, context: CallbackContext) -> None:
    # 定义按钮
    keyboard = [
        [
            InlineKeyboardButton("选项 1", callback_data='1'),
            InlineKeyboardButton("选项 2", callback_data='2'),
        ],
        [InlineKeyboardButton("选项 3", callback_data='3')],
    ]

    # 创建内联键盘
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 发送消息并带上内联键盘
    update.message.reply_text('请选择一个选项:', reply_markup=reply_markup)


# 回调处理函数，当用户点击按钮时触发
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # 根据用户选择的选项回传消息
    query.edit_message_text(text=f"您选择了选项: {query.data}")
