import yaml
import asyncio
from telethon import TelegramClient, events

with open('../config.yaml', 'r') as file:
    config = yaml.safe_load(file)
api_id = config['api_id']
api_hash = config['api_hash']
proxy = (config['proxy']['proto'], config['proxy']['ip'], config['proxy']['port'])
client = TelegramClient(session='signing_in', api_id=api_id, api_hash=api_hash, proxy=proxy)


async def main():
    async with client:
        print((await client.get_me()).username)
        #     ^_____________________^ notice these parenthesis
        #     You want to ``await`` the call, not the username.
        #
        message = await client.send_message('me', 'Hi!')
        await asyncio.sleep(2)
        await message.delete()

        # @client.on(events.NewMessage(pattern='(?i)hi|hello'))
        # async def handler(event):
        #     await event.reply('hey')

        await client.run_until_disconnected()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
