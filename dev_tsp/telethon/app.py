import asyncio
from telethon import TelegramClient, events
from signing_in import client


async def main():
    async with client:
        # 测试启动情况
        print((await client.get_me()).username)
        message = await client.send_message('me', 'Hi!')
        await asyncio.sleep(1)
        await message.delete()

        # todo 待添加各种事件
        # @client.on(events.NewMessage(pattern='(?i)hi|hello'))
        # async def handler(event):
        #     await event.reply('hey')
        #     await client.send_message(event.input_sender, 'Hi')

        # 不加这个，client会停下来
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
