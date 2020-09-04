import os
import config
import json
import re
import logging
import random

from telebot import types
from datetime import datetime
from models import *
from semantic import TextProcessor
from search import searchProcessor
from tonque import Tonque
from users import UserProcessor
from replics import Replics
from funnel import funnelProcessor
from ga import gaTracker

from timertask import TimerProcessor
from playlist import PlaylistProcessor


class processChat:
    def __init__(self):
        """Constructor"""

        self.textProcessor = TextProcessor()
        self.search = searchProcessor()
        self.tonque = Tonque()
        self.users = UserProcessor()
        self.replics = Replics()
        self.funnel = funnelProcessor()
        self.timertask = TimerProcessor()
        self.playlist = PlaylistProcessor()
        self.tracker = gaTracker()


    def response(self, json_string):
        update = types.Update.de_json(json_string)
        try:
            if update.callback_query is not None:

                self.send_debug('process_callback')
                response =  self.process_callback(update.callback_query)
                chat_id = update.callback_query.message.chat.id
            else:

                self.send_debug('process')
                response=  self.process(update.message)
                chat_id = update.message.from_user.id

            if 'message_id' in response:
                message_id = response['message_id']
                del response['message_id']
                self.tonque.edit_message_text(chat_id, message_id, response)

            else:
                self.tonque.send_message(chat_id, response)

            self.tracker.storeInputMessage(update.message)

        except Exception as e:
            self.tracker.storeInputMessage(str(e))
            return str(e) + str(update.message)



        return response


    def process(self, message):
        """Принимает запрос пользователя и отдает ответ в виде словаря с ключем text и markup"""
        response = None
        # if message.text[0] != '/':
        self.users.user_update(message, message.from_user.id)

        if message.reply_to_message is not None:
            return self.message_from_admin(message)

        chat_id  =  message.chat.id
        self.send_debug('textProcessor')
        text, text_raw, emoji  = self.textProcessor.get_content(message)

        self.send_debug('add_context')

        text = self.funnel.add_context(chat_id, text)

        self.send_debug('handle_request')
        meaning_nodes  = self.search.handle_request(text, d_type='words')

        self.send_debug(str(meaning_nodes))
        if len(meaning_nodes) > 0:

            if self.check_reset(meaning_nodes[0]):

                self.send_debug('process_reset')
                ##Собщение об отмене действия
                response = self.process_reset(chat_id, meaning_nodes[0], text)
            else:

                ##Проверка воронки
                self.send_debug('process_funnel')
                meaning_defined, response = self.process_funnel(chat_id, 0, text, 'text_raw')
                if meaning_defined:
                    return response

                else:
                    self.send_debug('process_function')
                    ##Проверка воронки
                    response = self.process_function(chat_id, meaning_nodes[0], text)

        else:
            self.send_debug('process_not_defined')
            response = self.not_defined(chat_id, message.message_id, text)

        return response



    def process_callback(self, callback_query):
        """Обработка Коллбэка для inline кнопок"""
        response = None
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id

        command_split = callback_query.data.split('_')

        try:
            if len(command_split) > 1:

                callback_types = {
                    'start':self.timertask.timer_start,
                    'checktime': self.timertask.timer_checktime,
                    'delete': self.timertask.timer_delete,
                    'addlink': self.playlist.playlist_confirm,
                    'droplink': self.playlist.playlist_drop
                }

                if command_split[0] in callback_types:
                    functionName = callback_types[command_split[0]]
                    response = functionName(chat_id, command_split[1], message_id)

        except Exception as e:
            response = {'text':'_process_callback '+str(e)}

        return response


    def process_function(self, user_id, meaning, text):
        """Обработка функци назначенных интентам в common.js"""

        self.send_debug('process_function')

        functions = {
            'drop':self.process_reset,
            'hello':self.process_hello,
            'playlist':self.process_playlist,
            'tomato':self.process_tomato,
            'feedback':self.process_feedback
        }

        if meaning['function'] in functions:
            function_name = functions[meaning['function']]
            response = function_name(user_id, meaning, text)
        else:
            response = self.process_text(user_id,meaning,text)

        return response


    def process_text(self,user_id,meaning,text):
        """Ответ тектом в common.js без дополгнительной обработки фугкциями"""

        self.send_debug('process_text')

        response = {'text':meaning['text']}
        if 'menu' in meaning:
            response['reply_markup'] =[i['title'] for i in meaning['menu']]

        if 'funnel' in meaning:
            self.funnel.set_funnel(user_id, meaning['funnel'], '')

        return response


    def check_reset(self, meaning):
        """Проверка на отмену действия"""

        self.send_debug('check_reset')
        if meaning['function'] == 'drop':
            return True
        else:
            return False


    def not_defined(self, chat_id, message_id, text):
        """Генерим ответ со ссылкой на оператора, если тема не найдена"""

        response = self.replics.not_defined(chat_id)#not_defined.format(text)
        self.tonque.send_alert_admin(chat_id, message_id, text)
        return response


    def process_hello(self,chat_id, meaning, text):
        response = self.replics.tomato_hello(chat_id)
        return response


    def process_tomato(self,chat_id, meaning, text):
        response = self.replics.tomato(chat_id)
        return response


    def process_reset(self,chat_id, meaning, text):
        response = self.replics.reset(chat_id)
        self.funnel.set_funnel(chat_id, 'drop', '')
        return response

    def process_feedback(self,chat_id, meaning, text):
        pass

    def process_playlist(self,chat_id, meaning, text):
        response = self.replics.playlist_process(chat_id)
        self.funnel.set_funnel(chat_id, 'playlist_confirm', text)
        return response


    def process_funnel(self, chat_id, message_id, text, text_raw):
        """"""
        meaning_defined = False
        response = False

        funnels = {
            'playlist_confirm': self.playlist.playlist_confirm
        }

        funnel_current = self.funnel.last_funnel(chat_id)
        funnel_current = funnel_current['chatfunnel']

        if funnel_current in funnels:

            meaning_defined = 1
            functionName = funnels[funnel_current]
            response = functionName(chat_id, message_id, text)

        return meaning_defined, response


    def message_from_admin(self, message):
        response = {}
        # Ответ пользователю от Админа
        if message.reply_to_message.forward_from is not None:
            client_id = message.reply_to_message.forward_from.id
            # response = self.replySupport(text, message.chat.id)
            response = {'text': 'Вы ответили клиенту', 'reply_markup': ''}
            message_to_client = {'text': message.text}
            self.tonque.send_message(client_id, message_to_client)

        return response


    def send_debug(self,txt):
        if config.debug == 1:
            for a in config.admin_ids:
                self.tonque.send_message(a, {'text':txt})
        return True
