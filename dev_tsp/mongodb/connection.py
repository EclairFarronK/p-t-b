import yaml
from pymongo import MongoClient

with open('../config.yaml', 'r') as file:
    config = yaml.safe_load(file)
username = config['mongodb']['username']
password = config['mongodb']['password']
ip = config['mongodb']['ip']
port = config['mongodb']['port']

# 只需要导出mongoClient就行了
mongoClient = MongoClient(f'mongodb://{username}:{password}@{ip}:{port}')
