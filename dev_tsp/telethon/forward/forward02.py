import asyncio
from dev_tsp.telethon.signing_in import client


# 将a entity的message发送到b entity
async def forward_messages(source_entity_id: int, target_entity_id: int, offset_id: int = 0):
    async with client:
        limit = 128
        while True:
            messages = []
            async for message in client.iter_messages(source_entity_id, offset_id=offset_id, limit=limit, reverse=True):
                try:
                    media = message.media
                    text = message.text
                    messages.append(message)
                    if media:
                        await client.send_message(entity=target_entity_id, message=text, file=media)
                        print(message.id)
                except Exception as e:
                    print(f'Exception message: {str(e)}')

            # finish
            if not messages:
                break
            offset_id = messages[-1].id
        print('finish')

        await client.run_until_disconnected()


# Name: 拍胸走光合集_backup, ID: -1002220182058
# Name: 原创地铁高抄奶拍胸群, ID: -1002048115337
source_entity_id = -996504816
target_entity_id = -1002220182058
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(forward_messages(source_entity_id, target_entity_id, offset_id=0))
