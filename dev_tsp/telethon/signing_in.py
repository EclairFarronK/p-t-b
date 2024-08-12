import os
import yaml
from telethon import TelegramClient

b_dir = os.path.dirname(os.path.abspath(__file__))
config = os.path.join(b_dir, '../config.yaml')
signing_in = os.path.join(b_dir, './signing_in.session')

with open(config, 'r') as file:
    config = yaml.safe_load(file)
api_id = config['api_id']
api_hash = config['api_hash']
proxy = (config['proxy']['proto'], config['proxy']['ip'], config['proxy']['port'])

client = TelegramClient(session=signing_in, api_id=api_id, api_hash=api_hash, proxy=proxy)
