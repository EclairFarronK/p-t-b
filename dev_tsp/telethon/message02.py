import asyncio
from signing_in import client
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


async def main():
    # client.get_dialogs()
    # async for dialog in client.iter_dialogs(limit=None):
    #     print(dialog.name, 'has ID', dialog.id)

    # You can print the message history of any chat:
    # client.get_messages('5768415700')
    async with client:
        entity = 5768415700
        async for message in client.iter_messages(entity=entity, limit=None):
            # 在哪个dialog，id，text，link
            # todo 有link了直接跳转过去，好像
            message_json = {"dialog_id": entity, "id": message.id, "text": message.text, }
            db.dialog.insert_one(message_json)

        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
