from signing_in import client


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
