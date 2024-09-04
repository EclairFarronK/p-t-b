import asyncio
from datetime import datetime
from dev_tsp.telethon.signing_in import client
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


# todo 这里的media多一些，在telegram查看时，要少一点。
#  迭代次数过多，中途失败了，很麻烦
# 将entity中的media保存到database
async def save_media(entity_id: int):
    async with client:
        offset_id = 0
        limit = 128
        messages_save = []
        messages_save_actually = set()
        count = 0
        while True:
            # 打印iteration次数
            count += 1
            print(f'iteration:{count}')

            # messages用来迭代
            messages = []
            async for message in client.iter_messages(entity=entity_id, offset_id=offset_id, limit=limit, reverse=True):
                try:
                    messages.append(message)
                    media = message.media
                    if media:
                        if isinstance(media, MessageMediaPhoto):
                            messages_save.append({'message_id': message.id, 'media_id': media.photo.id})
                            messages_save_actually.add(media.photo.id)
                            print(f'MessageMediaPhoto:{media.photo.id}')
                        elif isinstance(media, MessageMediaDocument):
                            messages_save.append({'message_id': message.id, 'media_id': media.document.id})
                            messages_save_actually.add(media.document.id)
                            print(f'MessageMediaDocument:{media.document.id}')
                        else:
                            # telethon.tl.types.MessageMediaContact
                            print('media is unknown type')
                except Exception as e:
                    print(f'Exception message: {str(e)}')
            # 没有message时，finish
            if not messages:
                break
            offset_id = messages[-1].id

        print(len(messages_save))
        print(len(messages_save_actually))
        # 将数据保存到数据库
        dt = str(datetime.now().replace(microsecond=0))
        data = [{'entity_id': entity_id,
                 'message_id': message.get('message_id'),
                 'media_id': message.get('media_id'),
                 'create_time': dt,
                 'update_time': dt,
                 'state': 1} for message in messages_save]
        try:
            result = db.entity_media.insert_many(data, ordered=False)
            print('Inserted IDs:', result.inserted_ids)
        except Exception as e:
            print('Exception occurred:', e.details)
        print('save success')

        await client.run_until_disconnected()


entity_id = -1002220182058
entity_id = -1002175448714
entity_id = -1001290788078
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(save_media(entity_id))
