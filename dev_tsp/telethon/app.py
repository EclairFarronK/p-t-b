import asyncio
import re

from telethon import TelegramClient, events
from signing_in import client
from datetime import datetime
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


def extract_abc(message: str):
    pattern = r'([📢👥])\[(.*?)\-\-(.*?)\]\(https?://t\.me/(.*?)\)'
    matches = re.findall(pattern, message)
    return [list(match) for match in matches]


async def save_or_update(title: str, count: str, username: str, type: str):
    filter = {'username': username}
    dt = str(datetime.now().replace(microsecond=0))
    update = {
        '$set': {
            'title': title,
            'count': count,
            'update_time': dt,
        },
        '$setOnInsert': {
            'username': username,
            'type': type,
            'create_time': dt,
            'state': 1,
        }
    }
    return db.chat_channel_megagroup_test.update_one(filter=filter, update=update, upsert=True)


# todo 最好将handler配置在一个地方，这样就不需要改代码，先从一个地方加载handler
async def main():
    async with client:
        await client.send_message('me', '原神，启动！')

        @client.on(events.NewMessage(from_users='@python_telegram_bot_240730_bot'))
        async def handler(event):
            # todo 发给多个搜索群
            await client.send_message(entity='@sosoZHbot', message=event.message)
            # await client.send_message(entity='@sosoZHbot', message=event.message)
            # await client.send_message(entity='@sosoZHbot', message=event.message)
            # await client.send_message(entity='@sosoZHbot', message=event.message)
            # await client.send_message(entity='@sosoZHbot', message=event.message)

        @client.on(events.NewMessage(from_users='@sosoZHbot'))
        async def handler(event):
            group_or_channel_list = extract_abc(event.message.text)
            print(group_or_channel_list)
            # todo 批量插入
            for group_or_channel in group_or_channel_list:
                if group_or_channel[0] == '👥':
                    result = await save_or_update(group_or_channel[1], group_or_channel[2], group_or_channel[3],
                                                  'megagroup')
                elif group_or_channel[0] == '📢':
                    result = await save_or_update(group_or_channel[1], group_or_channel[2], group_or_channel[3],
                                                  'broadcast')
                else:
                    print('这种情况应该不存在!')

        # todo 解析
        @client.on(events.NewMessage(from_users='@jisou'))
        async def handler(event):
            print(event.message)

        # todo 待添加各种事件，来解析各种bot返回的消息
        # @client.on(events.NewMessage(pattern='(?i)hi|hello'))
        # async def handler(event):
        #     await event.reply('hey')
        #     await client.send_message(event.input_sender, 'Hi')

        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
