import asyncio
from dev_tsp.telethon.signing_in import client

# source_dialog_id = -1001290788078
# target_dialog_id = -1002175448714
source_dialog_id = -1001290788078
target_dialog_id = -1002175448714


# todo 从数据库拿到数据，然后发送到其他group
# todo 拿到一个group后，然后去重
# 1，写一个方法，从数据库拿到数据
# 2，
async def forward_messages(source_dialog_id: int, target_dialog_id: int, offset_id: int = 0):
    async with client:
        limit = 64  # 每次请求的消息数量
        while True:
            messages = []
            async for message in client.iter_messages(source_dialog_id, offset_id=offset_id, limit=limit, reverse=True):
                try:
                    media = message.media
                    text = message.text
                    messages.append(message)
                    if media:
                        await client.send_message(entity=target_dialog_id, message=text, file=media)
                        # 34608
                        print(message.id)
                except Exception as e:
                    print(f'Exception message: {str(e)}')
            # 没有message时，结束
            if not messages:
                break
            offset_id = messages[-1].id

        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(forward_messages(source_dialog_id, target_dialog_id, offset_id=11511))
