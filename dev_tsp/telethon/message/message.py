# from dev_tsp.telethon.signing_in import client
import asyncio
import os
import yaml
from telethon import TelegramClient

b_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(b_dir, '../../config.yaml')

with open(file_path, 'r') as file:
    config = yaml.safe_load(file)
api_id = config['api_id']
api_hash = config['api_hash']
proxy = (config['proxy']['proto'], config['proxy']['ip'], config['proxy']['port'])

client = TelegramClient(session='signing_in', api_id=api_id, api_hash=api_hash, proxy=proxy)


async def main():
    # Getting information about yourself
    # me = await client.get_me()
    # print(me.stringify())
    # print(me.username)
    # print(me.phone)

    # client.get_dialogs()
    # async for dialog in client.iter_dialogs(limit=None):
    #     print(dialog.name, 'has ID', dialog.id)

    # await client(SendMessageRequest('me', 'hello'))
    # await client.send_message('me', 'Hello, myself!')  # yourself
    # await client.send_message(entity, 'Hello, myself!')  # entity
    # 7188701260
    # await client.send_message(5768415700, 'Hello, group!')  # chat ID
    # await client.send_message('+8615197415820', 'Hello, friend!')  # contacts
    # await client.send_message('@XKCCER', 'Testing Telethon!')  # username

    # message = await client.send_message('me',
    #                                     'This message has **bold**, `code`, __italics__ and a [nice website](https://example.com)!',
    #                                     link_preview=False)
    # print(message.raw_text)
    # await message.reply('Cool!')
    # await message.delete()

    # Or send files, songs, documents, albums...
    # await client.send_file(5768415700, '../source/flower.jpeg')

    # You can print the message history of any chat:
    # client.get_messages('5768415700')
    async with client:
        async for message in client.iter_messages(entity=5768415700, limit=None):
            print(message.id, message.text)
            print(message.to_json())

    # todo 还有没有选择方法？
    # if message.photo:
    #     path = await message.download_media()
    #     print('File saved to', path)
    # await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
