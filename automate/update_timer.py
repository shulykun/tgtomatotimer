import sys
sys.path.insert(0, '..')
sys.path.insert(0, '/home/v/vstoch2s/tgtmt4/tgtmt4')

from timertask import Timertask
from replics import Replics
from tonque import Tonque
from models import *
import pandas as pd

replics = Replics()
timertask = Timertask()
tonque = Tonque()

def get_chat_id():
    c = TimerTask.select(TimerTask.chat_id).where(TimerTask.status==1).distinct().dicts()
    c = [i['chat_id'] for i in c]
    return c

def update_timer():

    chat_ids = get_chat_id()


    for chat_id in chat_ids:
        task = timertask.update_status(chat_id)
        # print(task)
        if task['time_remain'] > 0:
            response = replics.tomato_update(task['chat_id'], task)
            tonque.edit_message_text(task['chat_id'], task['message_id'], response)

        else:

                # response = replics.tomato_finish(chat_id, task)
                # tonque.edit_message_text(task['chat_id'], task['message_id'], response)

            try:
                tonque.delete_message(task['chat_id'], task['message_id'])
            except Exception as e:
                print(e)
                pd.DataFrame([str(e), task['chat_id'], task['message_id']]).to_csv('error_update_del.csv')

            try:
                tonque.send_message(task['chat_id'], replics.tomato_finish_text(chat_id))
            except Exception as e:
                print(e)
                pd.DataFrame([str(e), task['chat_id'], task['message_id']]).to_csv('error_update_send.csv')


            query = TimerTask.update(status=0).where(TimerTask.id == task['id'])
            query.execute()

    return 1

if __name__ == '__main__':

    update_timer()
