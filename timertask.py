import random
from models import *
from datetime import datetime,timedelta

class Timertask:
    """Управление заданиями таймера"""

    def __init__(self):
        pass

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
