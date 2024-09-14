import re
from typing import List
from telegram.constants import ParseMode
from dev_tsp.mongodb.connection import mongoClient
from telegram.ext import ContextTypes, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

# todo 想好数据库中数据格式是什么样的？
# todo 只需要管怎么从数据库中数据的结构什么样的，并且组装就行了
db = mongoClient['telegram_db']
page_size = 7
chat_id = 7188701260
keyboard = [
    [
        InlineKeyboardButton("上一页", callback_data='1'),
        InlineKeyboardButton("下一页", callback_data='2'),
    ],
    [InlineKeyboardButton("选项 3", callback_data='3')],
]


async def callback_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # send_message
    text = update.message.text
    try:
        # todo 发送消息给客户端，客户端发送消息给其他bot，然后将数据返回给数据库，这一步可以省略，直接爬虫爬取关键字就行了，
        # todo chat_id设置为dynamic
        await context.bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f'An error occurred: {e}')

    # 第一次设置为1
    page_num = 1
    await show_items(update=update, context=context, text=text, page_current=page_num)


async def callback_search_page(update: Update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data.split('_')

    # 提取参数
    action = query_data[0]
    current_page = int(query_data[1])
    text = query_data[2]

    # new_page
    if action == 'Previous':
        new_page = current_page - 1
    elif action == 'Next':
        new_page = current_page + 1
    else:
        print('应该不会出现这种情况')

    # show_items
    await show_items(update=update, context=context, text=text, page_current=new_page)


async def show_items(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, page_current: int):
    # 第一次查询
    result_list = await search_from_db(text, page_current, page_size)
    total = await get_total(text)
    total_page = total + page_size - 1
    message = assemble(result_list)

    # 构建翻页按钮
    buttons = []
    if page_current > 1:
        buttons.append(InlineKeyboardButton('Previous', callback_data=f'Previous_{page_current}_{text}'))
    if page_current < total_page:
        buttons.append(InlineKeyboardButton('Next', callback_data=f'Next_{page_current}_{text}'))

    # pagination_buttons = generate_pagination_buttons(page_current, total_page, text)
    reply_markup = InlineKeyboardMarkup([buttons])

    if update.callback_query:
        await update.callback_query.edit_message_text(text=message,
                                                      reply_markup=reply_markup,
                                                      parse_mode=ParseMode.MARKDOWN_V2,
                                                      disable_web_page_preview=True)
    else:
        await update.message.reply_text(text=message,
                                        reply_markup=reply_markup,
                                        parse_mode=ParseMode.MARKDOWN_V2,
                                        disable_web_page_preview=True)


# 分页功能暂时先不使用
# def generate_pagination_buttons(current_page, total_page: int, search_text: str):
#     buttons = []
#
#     # 处理 "上一页" 按钮
#     if current_page > 1:
#         buttons.append(InlineKeyboardButton('Previous', callback_data=f'Previous_{current_page}_{search_text}'))
#
#     # 计算要显示的页码范围
#     start_page = max(1, current_page - 5)
#     end_page = min(total_page, current_page + 4)
#
#     # 调整页码范围确保始终显示 10 个页码（如果可能）
#     if end_page - start_page < 9:
#         if start_page == 1:
#             end_page = min(10, total_page)
#         elif end_page == total_page:
#             start_page = max(1, total_page - 9)
#
#     # 添加页码按钮
#     for page in range(start_page, end_page + 1):
#         if page == current_page:
#             buttons.append(InlineKeyboardButton(f'[{page}]', callback_data=f'None_{page}'))  # 当前页不做回调
#         else:
#             buttons.append(InlineKeyboardButton(f'{page}', callback_data=f'Page_{page}_{search_text}'))
#
#     # 处理 "下一页" 按钮
#     if current_page < total_page:
#         buttons.append(InlineKeyboardButton('Next', callback_data=f'Next_{current_page}_{search_text}'))
#
#     return buttons


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


async def search_from_db(text: str, page_current: int, page_size: int):
    skip_count = (page_current - 1) * page_size
    result_list = list(
        db.chat_channel_megagroup_test.find({'title': {'$regex': f'{text}'}},
                                            {'_id': 0, 'title': 1, 'count': 1, 'username': 1})
        .skip(skip_count)
        .limit(page_size))
    return result_list


async def get_total(text: str):
    total = db.chat_channel_megagroup_test.count_documents({'title': {'$regex': f'{text}'}})
    return total
