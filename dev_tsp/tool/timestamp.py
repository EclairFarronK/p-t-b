import time
from datetime import datetime

# 获取当前时间戳（秒为单位的整数部分）
timestamp = 'standard' + str(int(time.time()))
print(timestamp)
print(datetime.now().replace(microsecond=0))
