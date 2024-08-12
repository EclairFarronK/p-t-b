import asyncio
from dev_tsp.telethon.signing_in import client


# 用来测试发送链接
async def main():
    async with client:
        # You can print the message history of any chat:
        # client.get_messages('5768415700')
        entity = await client.get_entity(5768415700)
        async for message in client.iter_messages(entity=entity, limit=None):
            print(message.to_json())

        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
