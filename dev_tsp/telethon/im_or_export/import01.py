import asyncio
from dev_tsp.telethon.signing_in import client
from telethon.tl.types import User, Chat, Channel
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


async def main():
    # count = db.chat_channel_megagroup_test.count_documents({'title': {"$exists": False}})
    # count = db.chat_channel_megagroup_test.count_documents({'title': None})
    # print(count)
    documents = db.chat_channel_megagroup_test.find({'title': None, "state": 1}, {'_id': 0, 'username': 1})
    documents_list = list(documents)
    async with client:
        i = 0
        for document in documents_list:
            i = i + 1
            print(i)
            try:
                username = document.get('username')
                entity = await client.get_entity(f'@{username}')
                if isinstance(entity, User):
                    print(f'Dialog with User: {entity.title}')
                elif isinstance(entity, Chat):
                    print(f'Dialog with Chat: {entity.title}')
                elif isinstance(entity, Channel):
                    # 获取type
                    if entity.megagroup:
                        # print(f'Dialog with megagroup: {entity.title}')
                        type = 'megagroup'
                    elif entity.broadcast:
                        # print(f'Dialog with broadcast: {entity.title}')
                        type = 'broadcast'
                    else:
                        # 这种情况应该不会出现
                        print('Unknown channel type')
                else:
                    # 这种情况应该不会出现
                    print('Unknown entity type')
            except Exception as e:
                # todo 如果有异常，就将state改为0，最好也是一次性插入
                print(f'An error occurred: {username}-----{e}')

            # todo 将所有数据组装起来，一次性插入到MongoDB中去
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
