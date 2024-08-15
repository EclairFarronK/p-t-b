import time
from datetime import datetime

if __name__ == '__main__':
    print(str(int(time.time())))
    print(datetime.now().replace(microsecond=0))
