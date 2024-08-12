import asyncio
from dev_tsp.telethon.signing_in import client
from telethon.tl.types import User, Chat, Channel
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


# 同时用来记录所有的Chat，channel，megagroup
async def main():
    async with client:
        async for dialog in client.iter_dialogs():
            try:
                # todo 只记录Chat，channel，megagroup 3种
                # todo 记录内容：title，username，type
                # todo 如果username为none，就从usernames中拿第一个
                entity = dialog.entity
                if isinstance(entity, User):
                    #  or entity.first_name
                    print(f"Dialog with User: {entity.username}")
                elif isinstance(entity, Chat):
                    # todo record
                    print(f"Dialog with Chat: {entity.title}")
                elif isinstance(entity, Channel):
                    if entity.megagroup:
                        # todo record
                        print(f"Dialog with megagroup: {entity.title}")
                    elif entity.broadcast:
                        # todo record
                        print(f"Dialog with broadcast: {entity.title}")
                    else:
                        # 这种情况应该不会出现
                        print("Unknown dialog type Channel")
                else:
                    # 这种情况应该不会出现
                    print("Unknown dialog type")

            except Exception as e:
                print(f'An error occurred: {e}')

        await client.run_until_disconnected()


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