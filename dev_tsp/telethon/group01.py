from signing_in import client
from telethon.tl.types import User, Chat, Channel

async def get_participants():
    async with client:
        # client.get_dialogs()
        async for dialog in client.iter_dialogs(limit=None):
            entity = dialog.entity
            if isinstance(entity, User):
                print(f"Dialog with User: {entity.username or entity.first_name}")
            elif isinstance(entity, Chat):
                print(f"Dialog with Chat (Group): {entity.title}")
            elif isinstance(entity, Channel):
                if entity.megagroup:
                    print(f"Dialog with Supergroup: {entity.title}")
                else:
                    print(f"Dialog with Channel: {entity.title}")
            else:
                print("Unknown dialog type")

        await client.run_until_disconnected()


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(get_participants())
