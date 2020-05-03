import talk.dict_input as dict_input
import os

from models import *
from semantic import TextProcessor
from search import searchProcessor

class Meaning:
    def __init__(self):
        """Constructor"""
        self.TextProcessor = TextProcessor()
        self.Search = searchProcessor()

        pass


    def define_theme(self, message_norm, message_data):

        found = False
        response_list = self.Search.offers_vector_search(message_norm, d_type='words')
        if len(response_list) > 0:
            found = True

        return response_list, found


    # def form_filling(self, message_norm, message):
    #     """Выделение компонентов в запросе"""
    #
    #     message_norm_list = message_norm.split(' ')
    #
    #     form = {}
    #     components = [
    #                     ['quality', self.define_quality, message_norm_list],
    #                     ['time', self.define_time, message_norm_list],
    #                     ['origin', self.define_origin, message_norm_list],
    #                     ['names', self.define_names, message_norm]
    #                 ]
    #
    #     for c in components:
    #
    #         functionName = c[1]
    #
    #         form_value = functionName(c[2])
    #         form[c[0]] = form_value
    #
    #     return form


    # def utility_check_operation_many(self, message_list, dict_values):
    #     """Перебор данных для  сопоставления слову - множество значений"""
    #     word_def = []
    #     for word in message_list:
    #         if word in dict_values:
    #             word_def.append(word)
    #
    #     return word_def
    #
    #
    # def utility_check_operation(self, message_list, dict_values):
    #     """Перебор данных для сопоставления слову"""
    #     word_def = 'not_set'
    #     for word in message_list:
    #         if word in dict_values:
    #             word_def = word
    #             break
    #
    #     return word_def
    #
    #
    # def utility_check_operation_dict(self, message_list, dict_values):
    #     """Перебор данных для сопоставления слову"""
    #     word_def = 'not_set'
    #     for word in message_list:
    #         if word in dict_values.keys():
    #             word_def = dict_values[word]
    #             break
    #
    #     return word_def


    # def get_list_genre(self):
    #     genres = VodMovies.select(VodMovies.genres).distinct()
    #     genres = [self.TextProcessor.normalise(i.genres) for i in genres]
    #     #dict_genres = {i: i for  i in genres}
    #
    #     return genres


    # def get_dict_origin(self):
    #     """"Есть ли слова указывающие на страну"""
    #     dict_origin_noun = {i: i for  i in dict_input.origin_adj.values()}
    #     dict_origin_adj = dict_input.origin_adj
    #     dict_origin = {}
    #     for d in (dict_origin_noun,dict_origin_adj):
    #         dict_origin.update(d)
    #     return  dict_origin
    #
    #
    # def get_dict_quality(self):
    #     '''есть ли слова указывающие на качество'''
    #     words_good = {i:'good' for  i in dict_input.words_excellent}
    #     words_bad = {i:'bad' for  i in dict_input.words_bad}
    #     words_quality = {}
    #     for d in (words_bad,words_good):
    #         words_quality.update(d)
    #     return  words_quality
    #
    #
    # def get_dict_time(self):
    #     '''есть ли слова указывающие на старый-новый''''
    #     words_new = {i:'new' for  i in dict_input.words_new}
    #     words_old = {i:'old' for  i in dict_input.words_old}
    #     words_quality = {}
    #     for d in (words_new,words_old):
    #         words_quality.update(d)
    #     return  words_quality
    #
    #
    # def define_origin(self, message_list):
    #     """"Есть ли слова указывающие на страну"""
    #     dict_origin = self.get_dict_origin()
    #     check = self.utility_check_operation_dict(message_list, dict_origin)
    #
    #     return check
    #
    #
    # def define_quality(self, message_list):
    #     """"Есть ли слова указывающие на качество"""
    #     words = self.get_dict_quality()
    #     check = self.utility_check_operation_dict(message_list, words)
    #
    #     return check
    #
    #
    # def define_time(self, message_list):
    #     """"Есть ли слова указывающие на свежий фильм"""
    #     words = self.get_dict_time()
    #     check  = self.utility_check_operation_dict(message_list, words)
    #
    #     return check
    #
    #
    # # def define_genre(self, message_list):
    # #     """"Есть ли слова указывающие на жанр"""
    # #     list_genres = self.get_list_genre()
    # #     check  = self.utility_check_operation_many(message_list, list_genres)
    # #
    # #     return check
    #
    #
    # def define_film_name(self, message):
    #     """"Есть ли слова указывающие на название фильма"""
    #
    #     #text = ' '.join(message_list).strip()
    #     #message = '''В минувшие выходные известному актеру исполнилось 57 лет. Это событие Джордж Клуни решил отметить
    #     #вдвоем с женой.'''
    #
    #     #names = self.TextProcessor.find_names(message)
    #
    #     return names
    #
    #
    # def define_names(self, message):
    #     """"Есть ли слова указывающие на имена"""
    #
    #     #text = ' '.join(message_list).strip()
    #     #message = '''В минувшие выходные известному актеру исполнилось 57 лет. Это событие Джордж Клуни решил отметить
    #     #вдвоем с женой.'''
    #
    #     names = self.TextProcessor.find_names(message)
    #     names = [' '.join(i) for i in names]
    #     return names
