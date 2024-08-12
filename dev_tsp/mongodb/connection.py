import os
import yaml
from pymongo import MongoClient

b_dir = os.path.dirname(os.path.abspath(__file__))
config = os.path.join(b_dir, '../config.yaml')

with open(config, 'r') as file:
    config = yaml.safe_load(file)
username = config['mongodb']['username']
password = config['mongodb']['password']
ip = config['mongodb']['ip']
port = config['mongodb']['port']

# 只需要导出mongoClient就行了
mongoClient = MongoClient(f'mongodb://{username}:{password}@{ip}:{port}')
