import asyncio
from datetime import datetime
from dev_tsp.telethon.signing_in import client
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


# todo 怎么解决发送数据过多过热的问题？
async def from_db_send_messages(source_entity_id: int, target_entity_id: int):
    messages_id = list(db.entity_media.find({'entity_id': source_entity_id, 'state': 1},
                                            {'_id': 0, 'entity_id': 1, 'message_id': 1}))
    print(len(messages_id))
    async with client:
        for message in messages_id:
            message_id = message.get('message_id')
            message = client.get_messages(source_entity_id, message_id)
            try:
                media = message.media
                if media:
                    await client.send_message(entity=target_entity_id, file=media)

                    # 'state': 0,'update_time': dt,
                    filter = {'entity_id': source_entity_id, 'message_id': message_id}
                    dt = str(datetime.now().replace(microsecond=0))
                    update = {
                        '$set': {
                            'state': 0,
                            'update_time': dt,
                        }
                    }
                    return db.entity_media.update_one(filter=filter, update=update)
            except Exception as e:
                print(f'Exception message: {str(e)}')

        await client.run_until_disconnected()


source_entity_id = -4149606141
target_entity_id = -1002220182058
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(from_db_send_messages(source_entity_id, target_entity_id))
