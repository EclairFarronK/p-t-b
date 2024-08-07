from telethon import events


@client.on(events.NewMessage(incoming=True, pattern='(?i)hi'))
async def handler(event):
    await event.reply('Hello!')


client.run_until_disconnected()


client.get_entity(PeerUser(some_id))
