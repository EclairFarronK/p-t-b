import asyncio
from datetime import datetime
from dev_tsp.telethon.signing_in import client
from telethon.tl.types import User, Chat, Channel
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


# todo 不使用一次性insert数据库
async def main():
    # count = db.chat_channel_megagroup_test.count_documents({'title': {"$exists": False}})
    # count = db.chat_channel_megagroup_test.count_documents({'title': None})
    # print(count)
    documents = db.chat_channel_megagroup.find({'title': None, "state": 1}, {'_id': 0, 'username': 1})
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
                        await update(username, entity.title, type)
                    elif entity.broadcast:
                        # print(f'Dialog with broadcast: {entity.title}')
                        type = 'broadcast'
                        await update(username, entity.title, type)
                    else:
                        # 这种情况应该不会出现
                        print('Unknown channel type')
                else:
                    # 这种情况应该不会出现
                    print('Unknown entity type')
            except Exception as e:
                # 异常先不处理，因为有可能是telegram限制了frequency
                print(f'An error occurred: {username}-----{e}')

        await client.run_until_disconnected()


async def update(username: str, title: str, type: str):
    dt = str(datetime.now().replace(microsecond=0))
    # $inc（递增字段值）、$unset（删除字段）、$push（数组追加）
    message_json = {'$set': {'title': title,
                             'type': type,
                             'update_time': dt}}
    db.chat_channel_megagroup_test.update_one({'username': username}, message_json)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
