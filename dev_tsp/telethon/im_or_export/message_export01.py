import asyncio
from dev_tsp.telethon.signing_in import client

username = '@sosoZHbot'


# 根据username导出message
async def main():
    async with client:
        entity = await client.get_entity(username)
        async for message in client.iter_messages(entity=entity, limit=None):
            entity_text = message.raw_text[5:5 + 28]
            # print(f"Entity: {get_display_name(entity)}, Text: {entity_text}")
            print(f'Text: {entity_text}')

        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
