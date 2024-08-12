import asyncio
from dev_tsp.telethon.signing_in import client


async def send_message_with_options(chat_id, message, **kwargs):
    # 通过 **kwargs 将可选参数传递给 send_message 方法
    await client.send_message(chat_id, message, **kwargs)


# 用来测试发送链接
# todo 设置参数可变
async def main():
    async with client:
        try:
            entity = await client.get_entity(5768415700)
            # https://www.baidu.com/
            baidu = 'https://www.baidu.com/'
            # https://www.hao123.com/
            jiso = 'http://t.me/jiso'
            zhenwei011 = 'http://t.me/zhenwei011'
            xy91b = 'http://t.me/xy91b'
            list01 = []
            list01.append(baidu)
            list01.append(jiso)
            list01.append(zhenwei011)
            list01.append(xy91b)
            message = '\n'.join(map(str, list01))
            # 比较复杂
            # message = '\n'.join([f'Item {i + 1}: {item}' for i, item in enumerate(list01)])
            # f'[{baidu}]({baidu})\n[{hao123}]({hao123})\n'
            await client.send_message(entity,
                                      message,
                                      link_preview=False)
        except Exception as e:
            print(f'An error occurred: {e}')
        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
