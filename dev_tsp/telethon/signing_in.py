import os
import yaml
from telethon import TelegramClient

# 以后切换账号修改这里就行了
account = 'tsp_5820'

b_dir = os.path.dirname(os.path.abspath(__file__))
config = os.path.join(b_dir, '../config.yaml')

with open(config, 'r') as file:
    config = yaml.safe_load(file)
    name = config['session'][account]
    api_id = name['api_id']
    api_hash = name['api_hash']
    proxy = (config['proxy']['proto'], config['proxy']['ip'], config['proxy']['port'])

signing_in = os.path.join(b_dir, f'./{account}.session')
client = TelegramClient(session=signing_in, api_id=api_id, api_hash=api_hash, proxy=proxy)
