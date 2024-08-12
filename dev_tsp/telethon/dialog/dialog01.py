import asyncio
from dev_tsp.telethon.signing_in import client
from telethon.tl.types import User, Chat, Channel
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


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
                    if entity.megagroup:
                        # 可能有多个名字的情况
                        username = entity.username or entity.usernames[0].username
                        await save(entity.title, username, 'megagroup')
                        print(f'Dialog with megagroup: {entity.to_json()}')
                    elif entity.broadcast:
                        # 只有一个名字
                        await save(entity.title, entity.username, 'broadcast')
                        print(f'Dialog with broadcast: {entity.to_json()}')
                    else:
                        # 这种情况应该不会出现
                        print('Unknown dialog type Channel')
                else:
                    # 这种情况应该不会出现
                    print('Unknown dialog type')
            except Exception as e:
                print(f'An error occurred: {e}')

        await client.run_until_disconnected()


# todo 在save的时候，如果message_json中的username已经有了，就不重复插入
async def save(title, username, type):
    message_json = {'title': title,
                    'username': username,
                    'type': type}
    db.chat_channel_megagroup.insert_one(message_json)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
