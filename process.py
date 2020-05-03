import os
import config
import json
import re
import logging
import random
import talk.dict_replics as dict_replics

from datetime import datetime
from models import *
from semantic import TextProcessor
from search import searchProcessor
from tonque import Tonque
from users import UserProcessor
from replics import Replics
from funnel import funnelProcessor
from timertask import Timertask


class processChat:
    def __init__(self):
        """Constructor"""
        self.ADMIN_IDS = config.admin_ids
        self.textProcessor = TextProcessor()
        self.search = searchProcessor()
        self.tonque = Tonque()
        self.users = UserProcessor()
        self.replics = Replics()
        self.funnel = funnelProcessor()
        self.timertask = Timertask()
        self.path_to_files = '{}/tgsb6/files'.format(os.path.abspath(''))


    def response(self, message):
        response = self.process(message)
        self.tonque.send_message(message.chat.id, response)
        return response


    def process_callback(self, callback_query):
        """Обработка Коллбэка для inline кнопок"""
        response = None

        message = callback_query.message
        chat_id = callback_query.message.chat.id
        command = callback_query.data
        command_s = command.split('_')

        try:
            if len(command_s) > 1:

                callback_types = [
                     ['start', self.timer_start],
                     ['checktime', self.timer_checktime],
                     ['delete', self.timer_delete],
                     ['addlink', self.playlist_confirm],
                     ['droplink', self.playlist_drop],

                ]

                for f in callback_types:
                    if command_s[0] == f[0]:
                        functionName = f[1]
                        response = functionName(chat_id, command_s[1], message.message_id)
                        break

        except Exception as e:
            response = '_process_callback '+str(e)
            self.tonque.send_message(chat_id, {'text':response})

        return response


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


    def process(self, message):
        """Принимает запрос пользователя и отдает ответ в виде словаря с ключем text и markup"""
        response = None
        # if message.text[0] != '/':
        self.users.user_update(message, message.from_user.id)

        if message.reply_to_message is not None:
            return self.message_from_admin(message)

        text, text_raw, emoji  = self.textProcessor.get_content(message)
        text = self.funnel.add_context(message.chat.id, text)

        meaning_nodes  = self.search.handle_request(text, d_type='words')

        if len(meaning_nodes) > 0:
            response = self.process_function(message.chat.id, meaning_nodes[0], text)
            return response
        else:
            response = self.not_defined(message.chat.id, message.message_id, text)
            return response

        return response


    def process_function(self, chat_id, meaning, text):

        ##Проверка на отмену
        if meaning['funnel'] == 'drop':
            r_ = self.process_reset(chat_id, meaning, text)
            return r_

        ##Проверка воронки
        meaning_defined, r_ = self.process_funnel(chat_id, 0, text, 'text_raw')
        if meaning_defined == 1:
            return r_

        if meaning['funnel'] == 'feedback':
            r_ = self.process_feedback(chat_id, meaning, text)

        elif meaning['funnel'] == 'hello':
            r_ = self.process_hello(chat_id, meaning, text)

        elif meaning['funnel'] == 'playlist':
            r_ = self.process_playlist(chat_id, meaning, text)

        elif meaning['funnel'] == 'tomato':
            r_ = self.process_tomato(chat_id, meaning, text)

        else:
            r_ = {'text':meaning['text']}
            if 'menu' in meaning:
                r_['reply_markup'] =[i['title'] for i in meaning['menu']]

        return r_


    def not_defined(self, chat_id, message_id, text):
        """Генерим ответ со ссылкой на оператора, если тема не найдена"""

        response = self.replics.not_defined(chat_id)#not_defined.format(text)
        self.tonque.send_alert_admin(chat_id, message_id, text)
        return response


    def timer_start(self, chat_id, command_id, message_id = 0):


        url = self.get_random_link()

        task_data = {'start':datetime.now(),
                    'chat_id':chat_id,
                    'message_id':message_id,
                    'status':1,
                    'url':url,
                    'lenght':25
                    }

        # t, c = TimerTask.get_or_create(**task_data)

        task = TimerTask(**task_data)
        task.save()

        response = self.replics.tomato_start(chat_id, url)
        self.tonque.edit_message_text(chat_id, message_id, response)

        return response


    def timer_checktime(self, chat_id, command_id, message_id = 0):
        task = self.timertask.update_status(chat_id, message_id)
        response = self.replics.tomato_checktime(chat_id, task)
        self.tonque.edit_message_text(chat_id, message_id, response)

        return response


    def timer_update(self, chat_id, command_id, message_id = 0):

        task = self.timertask.update_status(chat_id)
        response = self.replics.tomato_update(chat_id, task)
        self.tonque.edit_message_text(chat_id, message_id, response)

        return response


    def timer_delete(self, chat_id, command_id, message_id = 0):

        response = self.replics.tomato_delete(chat_id)

        query = TimerTask.delete().where(TimerTask.chat_id == 79711951).where(TimerTask.message_id == message_id)
        query.execute()

        self.tonque.edit_message_text(chat_id, message_id, response)

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


    def playlist_drop(self,chat_id, command_id, message_id = 0):
        response = self.replics.playlist_cancel(chat_id)

        self.funnel.set_funnel(chat_id, 'drop', '')
        self.tonque.edit_message_text(chat_id, message_id, response)

        return response


    def playlist_confirm(self,chat_id, command_id, message_id = 0):

        funnel_current = self.funnel.last_funnel(chat_id, funnel_name='playlist_confirm')

        url = self.textProcessor.detect_url(funnel_current['message'])
        if url:

            playlist_data = {
                        'chat_id':chat_id,
                        'status':0,
                        'url':url
                        }

            playlist = Playlist(**playlist_data)
            playlist.save()

            response = self.replics.playlist_confirm(chat_id)
        else:
            response = self.replics.playlist_cancel(chat_id)

        self.funnel.set_funnel(chat_id, 'drop', '')
        self.tonque.edit_message_text(chat_id, message_id, response)

        return response


    def get_random_link(self):

        q = Playlist.select(Playlist.url).where(Playlist.status==1).dicts()
        url_list = [i['url'] for i in q]
        r = random.randint(0,len(url_list)-1)

        return url_list[r]


    def process_funnel(self, chat_id, message_id, text, text_raw):
        """"""
        meaning_defined = None
        response = None

        funnels = {
            # 'playlist_confirm': self.playlist_confirm
        }

        funnel_current = self.funnel.last_funnel(chat_id)
        if config.debug == 1:
            self.tonque.send_message(chat_id, {'text':str(funnel_current)})

        if funnel_current['chatfunnel'] in funnels:
            meaning_defined = 1
            functionName = funnels[funnel_current['chatfunnel']]

            if config.debug == 1:
                self.tonque.send_message(chat_id, {'text':str(functionName)})

            response = functionName(chat_id, message_id, text)

        return meaning_defined, response
