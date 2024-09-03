import re
from typing import List
from datetime import datetime
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


# todo 只要是能用文本工具打开的应该都能拿到url
def scan_links_from_md(file_path):
    # /后遇到 )]?/\n结束
    # 排除joinchat和*bot
    pattern = r'https?://t\.me/((?!joinchat)(?!.*bot)[^ )\]?/\n]+)'
    # 读取Markdown文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # 使用正则表达式查找所有匹配的链接
        usernames = re.findall(pattern, content, re.IGNORECASE)
    return list(set(usernames))


def save(usernames: List[dict]):
    dt = str(datetime.now().replace(microsecond=0))
    data = [{'username': username,
             'create_time': dt,
             'update_time': dt,
             'state': 1} for username in
            usernames]
    try:
        # ordered=Falsez
        result = db.chat_channel_megagroup.insert_many(data, ordered=False)
        print('Inserted IDs:', result.inserted_ids)
    except Exception as e:
        print('Exception occurred:', e.details)
    return


if __name__ == '__main__':
    usernames = scan_links_from_md('README.md')
    save(usernames)
