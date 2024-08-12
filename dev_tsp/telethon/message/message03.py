import asyncio
from dev_tsp.telethon.signing_in import client


# 用来测试发送链接
# todo 设置参数可变
async def main():
    async with client:
        try:
            entity = await client.get_entity(5768415700)
            baidu = 'https://www.baidu.com/'
            hao123 = 'https://www.hao123.com/'
            await client.send_message(entity,
                                      f'[{baidu}]({baidu})\n[{hao123}]({hao123})\n',
                                      link_preview=False)
        except Exception as e:
            print(f'An error occurred: {e}')
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
