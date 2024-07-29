import asyncio
import telegram


async def main():
    bot = telegram.Bot('')
    async with bot:
        print(await bot.get_me())
        # todo 项目是不是一直在启动中？
        updates = (await bot.get_updates())[0]
        print(updates)
        # todo
        await bot.send_message(text='Hi John!', chat_id=1234567890)


if __name__ == '__main__':
    asyncio.run(main())
