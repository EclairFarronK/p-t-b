import yaml
from telethon import TelegramClient

with open('../config.yaml', 'r') as file:
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

    # async for dialog in client.iter_dialogs():
    #     print(dialog.name, 'has ID', dialog.id)

    # await client.send_message('me', 'Hello, myself!')  # yourself
    # 7188701260
    # await client.send_message(5768415700, 'Hello, group!')  # chat ID
    # await client.send_message('+8615197415820', 'Hello, friend!')  # contacts
    # await client.send_message('@XKCCER', 'Testing Telethon!')  # username

    # message = await client.send_message('me',
    #                                     'This message has **bold**, `code`, __italics__ and a [nice website](https://example.com)!',
    #                                     link_preview=False)
    # print(message.raw_text)
    # await message.reply('Cool!')

    # Or send files, songs, documents, albums...
    # await client.send_file(5768415700, '../source/flower.jpeg')

    # You can print the message history of any chat:
    async for message in client.iter_messages(5768415700):
        print(message.id)
        print(message.to_json())

        # if message.photo:
        #     path = await message.download_media()
        #     print('File saved to', path)


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
