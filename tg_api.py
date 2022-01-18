import json

import requests

import settings


URL = 'https://api.telegram.org'


def invoke_telegram(method, **kwargs):
    resp = requests.post(f'{URL}/bot{settings.TG_BOT_TOKEN}/{method}', data=kwargs)
    return resp


class TelegramHook:
    def __init__(self, data):
        self.data = json.loads(data)
        self.message = self.data.get('message')





# Цепочка запросов для чата
# Для каждого чата хранится экземпляр его состояния
# Базу данных хранить только для сериализации
# Не хранить локально в памяти
# Класс чат

class ChatMessagesChain:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.state = None


states = {
    'add_train_enter_origin_station': None,
    'add_train_select_origin_station': None,

}
