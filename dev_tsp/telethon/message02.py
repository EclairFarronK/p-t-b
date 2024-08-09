import asyncio
from signing_in import client
from dev_tsp.mongodb.connection import mongoClient

db = mongoClient['telegram_db']


async def main():
    # You can print the message history of any chat:
    # client.get_messages('5768415700')
    async with client:
        # client.get_dialogs()
        # async for dialog in client.iter_dialogs(limit=None):
        #     print(dialog.name, 'has ID', dialog.id)

        entity = 5768415700
        async for message in client.iter_messages(entity=entity, limit=None):
            print(message.to_json())
            print(message.from_id)
            print(message.text)
            # 在哪个dialog，id，text，link
            # todo 有link了直接跳转过去，好像
            # todo 提高效率，先批量保存到内存中，然后批量存到MongoDB
            message_json = {"entity": entity,
                            "id": message.id,
                            # rguo1
                            "from_id": message.from_id,
                            "text": message.text, }
            # db.dialog.insert_one(message_json)

        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
