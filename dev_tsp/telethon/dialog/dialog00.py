import asyncio
from dev_tsp.telethon.signing_in import client
from telethon.tl.types import User, Chat, Channel


# export所有dialog
async def export_dialog():
    async with client:
        async for dialog in client.iter_dialogs():
            print(f"Name: {dialog.name}, ID: {dialog.id}")

        # await client.run_until_disconnected()


# 根据dialog.id检测dialog.type
async def detect_dialog_type(dialog_id: int):
    async with client:
        try:
            dialog = await client.get_entity(dialog_id)
            if isinstance(dialog, User):
                print(f'Dialog is User')
            elif isinstance(dialog, Chat):
                print(f'Dialog is Chat')
            elif isinstance(dialog, Channel):
                if dialog.megagroup:
                    print(f'Dialog is megagroup')
                elif dialog.broadcast:
                    print(f'Dialog is broadcast')
                else:
                    print('Unknown channel type')
            else:
                print('Unknown dialog type')
        except Exception as e:
            print(f'An error occurred: {e}')

        # await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(export_dialog())
    # asyncio.get_event_loop().run_until_complete(detect_dialog_type())
