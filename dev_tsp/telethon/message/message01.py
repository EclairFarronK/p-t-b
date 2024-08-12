import asyncio
from dev_tsp.telethon.signing_in import client


async def main():
    async with client:
        async for dialog in client.iter_dialogs():
            print(dialog.name, 'has ID', dialog.id)
        # todo 测试不使用sleep可不可以？
        # await asyncio.sleep(3)
        try:
            await client.send_message(5768415700, 'Hello, group!')
            # await client.send_message(1002177155167, 'Hello, group!')
            entity = await client.get_entity(4250131789)
            await client.send_message(entity, 'Hello, group!')
        except Exception as e:
            print(f'An error occurred: {e}')
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
