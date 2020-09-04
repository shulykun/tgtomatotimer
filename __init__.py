import os
import telebot
import config
import requests

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from peewee import *
from telebot import types
from process import processChat
from search import searchProcessor
from models import *


app = Flask(__name__)
app.config.from_object(__name__)
bot = telebot.TeleBot(config.tg_token)

processor = processChat()
searcher = searchProcessor()

# DBASE.create_tables([Loghook,ChatUser,TimerTask,Playlist,PlaylistUser,ChatFunnel], safe=True)


@app.route('/')
def hello_world():
    return 'Hello Tomatotimer :-)'


@app.route('/set_hook/')
def set_hook():
    """установка вебхука"""
    try:
        bot.set_webhook(url=config.tg_hook)
        response ='hook set to {}'.format(config.tg_hook)
    except Exception as e:
        response = str(e)
    return response


@app.route('/hook/', methods=['POST'])
def hook():
    """обработка веб хуков"""
    try:
        json_string = request.get_data().decode('utf-8')
        processed = processor.response(json_string)
        return str(processed)

    except Exception as e:

        return str(e)


@app.route('/vector_search')
def vector_search():
    """текстовый поиск"""
    try:
        s = request.args.get('s')
        x = searcher.handle_request(s, d_type='words')
        return str(x)

    except Exception as e:
        return str(e)


@app.route('/vector_search_ngrams')
def vector_search_ngrams():
    """текстовый поиск по н-граммам"""
    try:
        s = request.args.get('s')
        x = searcher.handle_request(s, d_type='ngrams')
        return str(x)

    except Exception as e:
        return str(e)

    return str(x)


@app.route('/search_save_dict')
def search_save_dict():
    """создание словаря для поиска"""
    x = searcher.generate_dict(d_type='words')
    return str(x)



@app.teardown_request
def _db_close(exc):
    if not DBASE.is_closed():
        DBASE.close()


if __name__ == '__main__':
    app.run()
