import json

from flask import Flask, request

import settings
import tg_api
from models import Chat, InitSQLAlchemy

app = Flask(__name__)
alchemy_conn = InitSQLAlchemy()


@app.route("/api/telegram_hook", methods=["POST"])
def telegram_hook():
    tg_hook = tg_api.TelegramHook(request.data)
    chat = Chat.get_or_create(alchemy_conn.session, {'id': tg_hook.message['chat']['id']})
    if tg_hook.message and tg_hook.message['text'] == '/test':
        tg_api.invoke_telegram(
            'sendMessage',
            chat_id=tg_hook.message['chat']['id'],
            text='test',
            reply_markup=json.dumps({
                'keyboard': [['row 1']],
                'resize_keyboard': True,
                'one_time_keyboard': True
            })
        )
    return 'OK'


if __name__ == '__main__':
    tg_api.invoke_telegram('setWebhook', url=f'{settings.ENDPOINT_URL}/api/telegram_hook')
    app.run()
