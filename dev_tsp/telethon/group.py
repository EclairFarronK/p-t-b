import yaml
from telethon import TelegramClient

with open('../config.yaml', 'r') as file:
    config = yaml.safe_load(file)
api_id = config['api_id']
api_hash = config['api_hash']
proxy = (config['proxy']['proto'], config['proxy']['ip'], config['proxy']['port'])
client = TelegramClient(session='signing_in', api_id=api_id, api_hash=api_hash, proxy=proxy)


async def get_participants():
    # 替换为目标群组或频道的用户名或ID
    target_chat = 1002125229305

    # 获取参与者列表
    participants = await client.get_participants(target_chat, limit=None)

    for participant in participants:
        print(participant.id, participant.username, participant.status)


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(get_participants())
