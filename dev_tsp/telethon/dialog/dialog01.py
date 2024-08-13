import time
import asyncio
from datetime import datetime
from dev_tsp.telethon.signing_in import client
from telethon.tl.types import User, Chat, Channel
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


# todo 什么时候run？暂时可以manual
# update session
# 同时用来记录所有的channel，megagroup
async def main():
    async with client:
        async for dialog in client.iter_dialogs():
            try:
                entity = dialog.entity
                if isinstance(entity, User):
                    print(f"Dialog with User: {entity.to_json()}")
                elif isinstance(entity, Chat):
                    print(f"Dialog with Chat: {entity.to_json()}")
                elif isinstance(entity, Channel):
                    # 获取username
                    if entity.username:
                        username = entity.username
                    elif entity.usernames:
                        username = entity.usernames[0].username
                    else:
                        username = str(int(time.time()))

                    # 获取type
                    if entity.megagroup:
                        print(f'Dialog with megagroup: {entity.to_json()}')
                        type = 'megagroup'
                    elif entity.broadcast:
                        print(f'Dialog with broadcast: {entity.to_json()}')
                        type = 'broadcast'
                    else:
                        # 这种情况应该不会出现
                        print('Unknown channel type')

                    # 保存数据
                    await save(entity.title, username, type)
                else:
                    # 这种情况应该不会出现
                    print('Unknown entity type')

            except Exception as e:
                print(f'An error occurred: {e}')

        await client.run_until_disconnected()


async def save(title, username, type):
    message_json = {'title': title,
                    'username': username,
                    'type': type,
                    'create_time': datetime.now().replace(microsecond=0),
                    'update_time': datetime.now().replace(microsecond=0),
                    'state': 1}
    db.chat_channel_megagroup.insert_one(message_json)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
