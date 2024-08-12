import asyncio
from dev_tsp.telethon.signing_in import client


async def main():
    async with client:
        async for dialog in client.iter_dialogs():
            print(dialog.name, 'has ID', dialog.id)

        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
