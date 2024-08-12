import asyncio
from dev_tsp.telethon.signing_in import client
from telethon.tl.types import User, Chat, Channel
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


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


async def save(title, username, type):
    message_json = {'title': title,
                    'username': username,
                    'type': type}
    db.chat_channel_megagroup.insert_one(message_json)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

# entity = 5768415700
# # todo 异步任务在外面定义一个计数器会影响效率吗？
# async for message in client.iter_messages(entity=entity, limit=None):
#     print(message.to_json())
#     print(message.from_id)
#     print(message.text)
#     # 在哪个dialog，id，text，link
#     # todo 有link了直接跳转过去，好像
#     # todo 提高效率，先批量保存到内存中，然后批量存到MongoDB
#     message_json = {"entity": entity,
#                     "id": message.id,
#                     # rguo1
#                     "from_id": message.from_id,
#                     "text": message.text, }
#     # db.dialog.insert_one(message_json)
