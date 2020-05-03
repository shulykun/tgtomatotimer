import random

from models import *
from datetime import datetime,timedelta
from random import random

class PlaylistProcess:
    """Управление заданиями таймера"""
    def __init__(self):
        pass

    def get_random_link():

            q = Playlist.select(Playlist.url).where(Playlist.status==1).dicts()
            url_list = [i['url'] for i in q]
            r = random.randint(0,len(url_list)-1)

            return url_list[r]
