import config
import os
import re
import json
import talk.dict_input as dict_input

from models import *
from gensim import corpora, models, similarities
from gensim.similarities import MatrixSimilarity
# from nltk.corpus import stopwords
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer

os.environ["PYTHONIOENCODING"] = "utf-8"


class searchProcessor:

    def __init__(self):
        self.window = [1,2]
        self.stopwords = dict_input.nltk_stopwords
        self.path_to_files = config.path_to_files+'/files'

    #
    # def offers_vector_search(self, search_string, d_type, skip = 0):
    #     """Вывод товаров по настройкам поиска"""
    #     sims = self.handle_request(search_string, d_type)
    #     return sims

    def my_tokenizer(self, s):
	       return s.split()



    def handle_request(self, search_string, d_type):
        """"""
        response = []
        content_list  = self.get_content_list()

        char_dictionary = self.open_dict(d_type)

        sims = self.get_similar_words(search_string, char_dictionary, content_list, d_type)

        if len(sims) > 0:
            response = sims
        # (content_txt, s[1], content_id)
        return response#,char_dictionary


    def get_similar_words(self, q_word, char_dictionary, content_map, d_type):
        """Получение списка похожих слов по близости с заданым окном"""

        dictionary = corpora.Dictionary([[i] for i in char_dictionary])

        # content_txt, content_id = zip(*content_list.items())
        content_txt = [i['index'] for i in content_map]

        corpus, query = self.transform_corpus(q_word, content_txt, dictionary, d_type)
        #return corpus, corpus_w, query
        index = MatrixSimilarity(corpus, num_features=len(dictionary))
        sims = index[query]
        sims_sorted = sorted(enumerate(sims), key=lambda item: -item[1])

        response = []
        for s in sims_sorted:
            if s[1] >= config.treshold_sim:
                c = content_map[s[0]]
                c['sim'] = s[1]
                response.append(c)

        return response


    def transform_corpus(self, q_word, offers_txt, dictionary, d_type):

        if d_type == 'ngrams':
            corpus = [dictionary.doc2bow(self.get_word_chars(text, windows = self.window)) for text in offers_txt]
            #corpus_w = [self.get_word_chars(text, windows = self.window) for text in offers_txt]
            query = dictionary.doc2bow(self.get_word_chars(q_word, windows = self.window))
        else:
            corpus = [dictionary.doc2bow(self.get_words(text)) for text in offers_txt]
            #corpus_w = [self.get_word_chars(text, windows = self.window) for text in offers_txt]
            query = dictionary.doc2bow(self.get_words(q_word))

        return corpus, query


    def open_dict(self, d_type):
        """словарь с н-граммами"""

        fn = self.dict_filename(d_type)
        char_dictionary = json.loads(open('{}/{}'.format(self.path_to_files,fn)).read())

        return char_dictionary


    def get_content_list(self):
        """сбор доступного контента"""

        # path = 'storage/'
        # path = '{}/storage/'.format(os.path.abspath(''))
        path = config.path_to_files+'/storage/'
        # return path
        files = os.listdir(path)

        content_data = []
        for i in files:
            try:
                with open(path+i, 'r', encoding="utf-8") as f:
                    f = f.read()
                    f = re.sub('\n', '',f)
                    j = json.loads(f)
                    content_data = content_data + j['map']
            except:
                pass
        # content_data

        return content_data


    def offers_single_words(self, offers_txt):
        """преобразование списка товаров в одномерный список слов"""
        offers_txt_s = [[i for i in j.split()] for j in offers_txt]
        return list(set([i for sublist in offers_txt_s for i in sublist if len(i) > 2]))


    def get_words(self, text):
        """преобразование текста в набор слов"""
        return set(text.split())


    def get_word_chars(self, text, windows):
        """преобразование текста в набор н-грам"""
        v = []
        for w in windows:
            for i in range(0, len(text)):
                start = i
                end = i + w
                text_to_add = text[start:end]
                if len(text_to_add) == w:
                    v.append(text_to_add)
        return v


    def make_dict(self, content_list, dict_type = 'ngrams'):
        '''Cоздание словаря'''

        if dict_type == 'ngrams':
            n_range = (1,2)
            analyzer = 'char_wb'
            max_features = 1000
        else:
            n_range = (1,1)
            analyzer = 'word'
            max_features = 30000

        vectorizer = CountVectorizer(ngram_range=n_range, lowercase=True,
        analyzer=analyzer, max_features=max_features, tokenizer=self.my_tokenizer)

        vectorizer.fit(content_list)

        v = vectorizer.vocabulary_
        v ={v_key: str(v[v_key]) for v_key in v}

        return v


    def dict_filename(self, d_type):

        if d_type == 'ngrams':
            fn = 'dict_nrgams_dict_w123.json'
        else:
            fn = 'dict_dict_w1.json'

        return fn


    def save_dict(self, fn, char_dict):

        fp = open('{}/{}'.format(self.path_to_files, fn), 'w')
        fp.write(json.dumps(char_dict))
        fp.close()

        return True



    def generate_dict(self, d_type):
        '''Создание словаря n-грам'''

        content_list = self.get_content_list()
        # return str(content_list)
        content_txt  = [i['index'] for i in content_list]

        char_dict = self.make_dict(content_txt, d_type)

        fn = self.dict_filename(d_type)

        self.save_dict(fn, char_dict)

        return 'dict saved {} {}'.format(len(content_list), str(char_dict))

    # def stop_words_gen():
    #     """стоп-слова"""
    #     russian_stopwords = stopwords.words("russian")
    #     return russian_stopwords
