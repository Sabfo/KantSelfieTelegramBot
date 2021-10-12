import flask
import telebot

import time
import os

from config import TG_TOKEN, PATH_TO_PHOTOS, PHOTO_EXTENSION, HOSTNAME

WEBHOOK_HOST = HOSTNAME
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(TG_TOKEN)


bot = telebot.TeleBot(TG_TOKEN)

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    print('post method to webhook url...')
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


@bot.message_handler(commands=['help', 'start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Введите номер')


@bot.message_handler(content_types=['text'])
def echo(message):
    # bot.send_message(message.chat.id, message.text)
    text: str = message.text
    filename = PATH_TO_PHOTOS + text + PHOTO_EXTENSION
    if text.isnumeric() and os.path.isfile(filename):
        with open(filename, 'rb') as file:
            bot.send_document(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, 'Файл не найден')


if __name__ == '__main__':
    print('Starting bot...')
    # Сначала проверить, что работает всё через long_polling, если всё ок, то настраивать webhook
    bot.polling()

    # Webhook

    # bot.remove_webhook()
    #
    # time.sleep(1.2)
    # bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
    #                 certificate=open(WEBHOOK_SSL_CERT, 'r'))
    #
    # app.run(host=WEBHOOK_LISTEN,
    #         port=WEBHOOK_PORT,
    #         ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
    #         debug=False)

