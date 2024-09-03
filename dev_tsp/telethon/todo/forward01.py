import asyncio
from datetime import datetime
from dev_tsp.telethon.signing_in import client
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']

source_dialog_id = -1001290788078
target_dialog_id = -1002175448714


# 分两步，先插入数据库去重，然后从数据库拿出来
# todo 能否先去重，然后发送？这样可以提高效率
async def forward_messages(source_chat_id: int, target_chat_id: int):
    async with client:
        offset_id = 0
        limit = 128  # 每次请求的消息数量
        while True:
            messages = []
            medias = []
            async for message in client.iter_messages(source_chat_id, offset_id=offset_id, limit=limit, reverse=True):
                try:
                    media = message.media
                    text = message.text
                    messages.append(message)
                    if media:
                        dialogs = {}
                        medias.append(message)
                except Exception as e:
                    print(f'Exception message: {str(e)}')
                # todo 批量插入数据库
                dt = str(datetime.now().replace(microsecond=0))
                data = [{'message_id': message.id,
                         'create_time': dt,
                         'update_time': dt,
                         'state': 1} for source_dialog_id in
                        dialogs]
                try:
                    result = db.media_message_forward.insert_many(data, ordered=False)
                    print('Inserted IDs:', result.inserted_ids)
                except Exception as e:
                    print('Exception occurred:', e.details)

            # 没有message时，结束
            if not messages:
                break
            offset_id = messages[-1].id

        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(forward_messages(source_dialog_id, target_dialog_id))
