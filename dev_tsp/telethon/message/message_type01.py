import asyncio
from dev_tsp.telethon.signing_in import client


# 用来判断dialog的type
async def main():
    # You can print the message history of any chat:
    # client.get_messages('5768415700')
    async with client:
        # client.get_dialogs()
        async for dialog in client.iter_dialogs(limit=None):
            entity = dialog.entity
            if entity.user:
                #  or entity.first_name
                print(f"Dialog with User: {entity.username}")
            elif entity.chat:
                print(f"Dialog with Chat: {entity.username}")
            elif entity.broadcast:
                print(f"Dialog with Broadcast: {entity.username}")
            elif entity.megagroup:
                print(f"Dialog with Megagroup: {entity.username}")
            else:
                print("Unknown dialog type")

        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
