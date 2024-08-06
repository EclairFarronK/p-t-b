import yaml
from telethon import TelegramClient

with open('../config.yaml', 'r') as file:
    config = yaml.safe_load(file)
api_id = config['api_id']
api_hash = config['api_hash']
proxy = (config['proxy']['proto'], config['proxy']['ip'], config['proxy']['port'])

if __name__ == '__main__':
    with TelegramClient(session='signing_in', api_id=api_id, api_hash=api_hash, proxy=proxy) as client:
        client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))
