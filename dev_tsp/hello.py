import asyncio
import telegram


# todo 没有成功，不知道怎么设置代理
async def main():
    # 设置 SOCKS5 代理

    bot = telegram.Bot(token='7294402442:AAEh75iyVxlC8V2nUcO7-J0fqze2tOTASbM')
    async with bot:
        print(await bot.get_me())
        # # todo 项目是不是一直在启动中？
        # updates = (await bot.get_updates())[0]
        # print(updates)
        # # todo
        # await bot.send_message(text='Hi John!', chat_id=1234567890)


if __name__ == '__main__':
    asyncio.run(main())
