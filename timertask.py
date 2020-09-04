import random
import config

from models import *
from datetime import datetime,timedelta

from replics import Replics
from playlist import PlaylistProcessor
from tonque import Tonque


class TimerProcessor:
    """Управление заданиями таймера"""

    def __init__(self):
        self.playlist = PlaylistProcessor()
        self.replics = Replics()



    def timer_start(self, chat_id, command_id, message_id = 0):

        url = self.playlist.get_random_link(chat_id)

        task_data = {
                    'start':datetime.now(),
                    'chat_id':chat_id,
                    'message_id':message_id,
                    'status':1,
                    'url':url,
                    'lenght':25
                    }

        task = TimerTask(**task_data)
        task.save()

        response = self.replics.tomato_start(chat_id, url)
        response['message_id'] = message_id

        return response


    def timer_checktime(self, chat_id, command_id, message_id = 0):
        task = self.update_status(chat_id, message_id)
        response = self.replics.tomato_checktime(chat_id, task)
        response['message_id'] = message_id

        return response


    def timer_update(self, chat_id, command_id, message_id = 0):

        task = self.update_status(chat_id)
        response = self.replics.tomato_update(chat_id, task)

        response['message_id'] = message_id

        return response


    def timer_delete(self, chat_id, command_id, message_id = 0):

        response = self.replics.tomato_delete(chat_id)

        query = TimerTask.delete().where(TimerTask.chat_id == chat_id).where(TimerTask.message_id == message_id)
        query.execute()

        response['message_id'] = message_id

        return response


    def open_last_task(self,chat_id, message_id):

        if message_id >0:
            t =  TimerTask.select().where(TimerTask.chat_id == chat_id)\
            .where(TimerTask.message_id == message_id).order_by(TimerTask.id.desc()).dicts()
        else:
            t =  TimerTask.select().where(TimerTask.chat_id == chat_id)\
            .order_by(TimerTask.id.desc()).dicts()

        if len(t):
            t = t.get()
        return t


    def get_time_remain(self,task):

        timer_end = task['start'] + timedelta(seconds=task['lenght']*60)
        timer_remain = timer_end - datetime.now()

        return timer_remain.total_seconds()


    def update_status(self,chat_id, message_id=0):

        last_task = self.open_last_task(chat_id, message_id)
        time_remain = self.get_time_remain(last_task)
        last_task['time_remain'] = time_remain
        last_task['time_remain_min'] = round(time_remain /60)

        return last_task


    # def send_debug(self,txt):
    #     if config.debug == 1:
    #         for a in config.admin_ids:
    #             self.tonque.send_message(a, {'text':txt})
    #     return True
