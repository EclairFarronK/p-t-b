import asyncio
from dev_tsp.telethon.signing_in import client

# source_dialog_id = -1001290788078
# target_dialog_id = -1002175448714
source_dialog_id = -1001290788078
target_dialog_id = -1002175448714


# 分两步，先插入数据库去重，然后从数据库拿出来
# todo 能否先去重，然后发送？这样可以提高效率
async def forward_messages(source_dialog_id: int, target_dialog_id: int):
    async with client:
        offset_id = 0
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
    asyncio.get_event_loop().run_until_complete(forward_messages(source_dialog_id, target_dialog_id))
