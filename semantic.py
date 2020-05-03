#Разбинение на элементы поступающего текста
import emoji
import json
import pymorphy2
import re
import talk.dict_input as dict_input
import config

class TextProcessor:

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        pass


    def get_content(self, message):
        """Извлекаем из сообщения контент """

        text, emoji, text_raw, photo_id = '', False, '', None

        if message.text is not None:

            text, text_raw = message.text, message.text

            check_text = re.search('[A-Za-zА-Яа-я]', text)
            if check_text:
                text = self.normalise(text)

            emoji, text_raw = self.check_emoji(text_raw)

        return text, text_raw, emoji


    def get_content(self, message):
        """Извлекаем из сообщения контент """

        text, emoji, text_raw, photo_id = '', False, '', None

        if message.text is not None:

            text, text_raw = message.text, message.text

            check_text = re.search('[A-Za-zА-Яа-я]', text)
            if check_text:
                text = self.normalise(text)

            emoji, text_raw = self.check_emoji(text_raw)

        return text, text_raw, emoji


    def detect_url(self, text):

        f = re.search('https://[^\s]+', text)
        if f:
            return f.group(0)
        else:
            return None


    def detect_playlist(self, text):

        for u in ['youtube','soundcloud']:
            if u in text:
                text = u + ' ' + text

        return text


    def normalise(self, text):
        """Приведение формы к единственному числу именительному падежу"""
        phrase_norm = []

        text_clean = re.sub('[^\w\s-]', '', text)

        for part in text_clean.split(' '):
            part = part.lower().strip()
            if part not in dict_input.words_stoplist:
                if part not in dict_input.normalize_exclude:
                    phrase_norm.append(self.morph.parse(part)[0].normal_form)
                else:
                    phrase_norm.append(part)

        url = self.detect_url(text)
        if url:
            phrase_norm.append(url)

        response = ' '.join(phrase_norm).strip()

        response= self.detect_playlist(response)

        return response


    def show_emoji(self, text):
        """Проверка на эмодзи"""
        text = emoji.emojize(text)

        return text


    def check_emoji(self, text):
        """Проверка на эмодзи"""
        js_text = text
        j = False

        if len(text) > len(text.encode('windows-1251', 'ignore')):

            js_text = json.loads('["{}"]'.format(text))[0]

            j = [t for t in js_text if t in emoji.UNICODE_EMOJI]

            js_text = emoji.demojize(js_text)

        return j,js_text


    def check_location(self, text):
        """Проверка на эмодзи"""
        for i in config.cities:
            if i.lower() in text:
                return i.lower()
        return False


    def define_positive(self, text):
        """Определяем тональность фразы 0 негатив 1 позитив 3 далее 2 не определено"""

        ## Четкое выражение с одним словом
        positive_list =  ['да', 'давай', 'ага', 'угу', 'ок', 'согласен', 'da','отправить']
        negative_list = ['отмена', 'нет', 'не надо', 'cancel']
        more_list = ['ещё', 'дальше', 'следующий', 'далее','ближайший']

        response = 2

        for phrases_list in [[positive_list, 1], [negative_list, 0], [more_list, 3]]:

            phrases_list_restricted = ['^{}$'.format(e) for e in phrases_list[0]]
            phrases = '({})'.format('|'.join(phrases_list_restricted))

            if re.search(phrases, text):
                response = phrases_list[1]
                break

        if response == 2:

            ## Нечеткое выражение - содержит ключевое слово и еще пару слово
            if len(text.split(' ')) < 4:

                for phrases_list in [[positive_list, 1], [negative_list, 0], [more_list, 3]]:

                    phrases_list_spaces = ['{}(,|\.|\s)'.format(e) for e in phrases_list[0]]

                    phrases = '({})'.format('|'.join(phrases_list_spaces))

                    if re.search(phrases, text):
                        response = phrases_list[1]
                        break



        return response
