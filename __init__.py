
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from peewee import *
import os
import telebot
import config
import requests

from ga import gaTracker
from telebot import types
from process import processChat
from search import searchProcessor
from models import *

bot = telebot.TeleBot(config.token)
app = Flask(__name__)
app.config.from_object(__name__)

DBASE.create_tables([Loghook,ChatUser,TimerTask,Playlist,PlaylistUser,ChatFunnel], safe=True)

processor = processChat()
searcher = searchProcessor()
tracker = gaTracker()


# @app.before_request
# def _db_connect():
#     DBASE.connect()


@app.route('/')
def hello_world():
    return 'Hello Tomatotimer :-)'


@app.route('/my_hook/')
def t():
    h = config.my_hook
    return h


@app.route('/me/')
def me():
    user = bot.get_me()
    username = user.username
    return username


@app.route('/set_hook/')
def set_hook():
    """установка вебхука"""
    try:
        bot.set_webhook(url=config.my_hook)
        r ='hook set to {}'.format(config.my_hook)
    except Exception as e:
        r = str(e)
    return r

# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     bot.reply_to(message, ("Здравствуйте! Вас приветствует ассистент СолидБанка. Оперативная информация о курсах валют, офисы, услуги и ответы на вопросы."))


@app.route('/hook/', methods=['POST'])
def hook():
    try:

        response_log = '_'
        if request.headers.get('content-type') == 'application/json':

            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])

            #сохранение лога запросов
            json_stored = Loghook(fulljson=json_string, chat_id = 1)#update.message.chat.id)
            json_stored.save()

            tracker.storeInputMessage(update.message)
            for u in [[update.message, processor.response], [update.callback_query, processor.process_callback]]:

                try:
                    #Как только находится не ошибка, выбираем
                    user_id = u[0].from_user.id
                    functionProcess = u[1]
                    response_log = 'Data Processed'
                    break

                except Exception as e:
                    response_log = 'Data Not Processed'
                    pass

            processed = functionProcess(u[0])
            # processed = processor.response(update.message)
            response_log = str(processed)

        else:
            response_log = request.headers.get('content-type')

    except Exception as e:
        response_log = str(e)

    return response_log


@app.route('/vector_search')
def vector_search():
    """поиск текстовый"""
    try:
        s = request.args.get('s')
        x = searcher.handle_request(s, d_type='words')

    except Exception as e:
        x = e

    #     x = catalogProc.search_words(79711951, 6500, 'мерло', 'мерло')
    return str(x)


@app.route('/vector_search_ngrams')
def vector_search_ngrams():
    """Получение списка товаров из выгрузок"""
    try:
        s = request.args.get('s')
        x = searcher.handle_request(s, d_type='ngrams')

    except Exception as e:
        x = e

    return str(x)


@app.route('/search_save_dict')
def search_save_dict():
    """"""
    # try:
    x = searcher.generate_dict(d_type='words')
    # except Exception as e:
    #     x = e
    return str(x)


@app.teardown_request
def _db_close(exc):
    if not DBASE.is_closed():
        DBASE.close()


if __name__ == '__main__':
    app.run()
