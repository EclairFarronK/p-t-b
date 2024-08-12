from telethon import events


@client.on(events.NewMessage(incoming=True, pattern='(?i)hi'))
async def handler(event):
    await event.reply('Hello!')


client.run_until_disconnected()

client.get_entity(PeerUser(some_id))

# 判断是否为群组或频道
if entity.broadcast:  # 频道
    url = f"https://t.me/{entity.username}"
    print(f"频道: {entity.title}, URL: {url}")
elif entity.megagroup:  # 超级群组
    url = f"https://t.me/{entity.username}"
    print(f"群组: {entity.title}, URL: {url}")
