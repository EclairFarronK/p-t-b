import sys
import site
dependency_package_path = site.getsitepackages()[0]
sys.path.insert(0, dependency_package_path)
import telegram

from telegram.client import Telegram
from telegram.text import Spoiler

tg = Telegram(
    api_id='api_id',
    api_hash='api_hash',
    phone='+31611111111',  # you can pass 'bot_token' instead
    database_encryption_key='changekey123',
    files_directory='/tmp/.tdlib_files/',
)
tg.login()

# If this is the first run, the library needs to preload all chats.
# Otherwise, the message will not be sent.
result = tg.get_chats()
result.wait()

chat_id: int
result = tg.send_message(chat_id, Spoiler('Hello world!'))

# `tdlib` is asynchronous, so `python-telegram` always returns an `AsyncResult` object.
# You can receive a result with the `wait` method of this object.
result.wait()
print(result.update)

tg.stop()  # You must call `stop` at the end of the script.
