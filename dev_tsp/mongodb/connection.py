import yaml
from pymongo import MongoClient

with open('../config.yaml', 'r') as file:
    config = yaml.safe_load(file)
username = config['mongodb']['username']
password = config['mongodb']['password']
ip = config['mongodb']['ip']
port = config['mongodb']['port']
client = MongoClient(f'mongodb://{username}:{password}@{ip}:{port}')
db = client['telegram_db']

# 开始
user = {"name": "tsp", "age": "25"}
result = db.users.insert_one(user)
print(f"Inserted user with id: {result.inserted_id}")
