from random import random,randint
from datetime import datetime,timedelta

from models import *
from replics import Replics
from funnel import funnelProcessor
from semantic import TextProcessor


class PlaylistProcessor:
    """Управление музыкой таймера"""
    def __init__(self):
        self.replics = Replics()
        self.funnel = funnelProcessor()
        self.textProcessor = TextProcessor()


    def get_random_link(self, chat_id):
        q = """SELECT p.url url, c
                FROM (
                    SELECT url, count(message_id) c
                    FROM timer_task tt
                    where tt.chat_id = 79711951
                    group by url
                ) tf

                right join playlist p on p.url = tf.url
                where p.status = 1
                order by c DESC
            """.format(chat_id)


        q = Playlist.raw(q).dicts()
        url_list = [i['url'] for i in q]
        url_list = url_list[5:]
        # q = Playlist.select(Playlist.url).where(Playlist.status==1).dicts()
        r = randint(0,len(url_list)-1)

        return url_list[r]


    def playlist_drop(self,chat_id, command_id, message_id = 0):

        response = self.replics.playlist_cancel(chat_id)
        self.funnel.set_funnel(chat_id, 'drop', '')

        # self.tonque.edit_message_text(chat_id, message_id, response)
        response['message_id'] = message_id

        return response


    def playlist_confirm(self, chat_id, command_id, message_id = 0):

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

        # self.tonque.edit_message_text(chat_id, message_id, response)
        response['message_id'] = message_id

        return response




    # def get_random_link():
    #
    #         q = Playlist.select(Playlist.url).where(Playlist.status==1).dicts()
    #         url_list = [i['url'] for i in q]
    #         r = random.randint(0,len(url_list)-1)
    #
    #         return url_list[r]
