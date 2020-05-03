import config
import math

class Replics():
    def __init__(self):
        pass


    def default_buttons(self, chat_id):
        b = [
                {'text':'Старт 25 мин', 'callback_data':'start_{}'.format(chat_id)},
                {'text':'Отмена', 'callback_data':'delete_{}'.format(chat_id)}
            ]
        return b

    def tomato_hello(self, chat_id):
        text = '''Я поставлю таймер и пришлю музыку чтобы ты не отвлекался. Ну что, поработаем?'''
        r_menu = self.default_buttons(chat_id)
        response = {'text':text,'reply_markup_inline':r_menu}
        return response



    def tomato_start(self, chat_id, url):
        # url = 'https://www.youtube.com/watch?v=gFn7V_pTJ-o'


        text = 'Время пошло! {}'.format(url)
        r_menu = self.default_buttons(chat_id)
        r_menu[0]['text'] = 'Осталось 25 мин'
        r_menu[0]['callback_data'] = 'checktime_{}'.format(chat_id)

        response = {'text':text,'reply_markup_inline':r_menu}
        return response

    def tomato_checktime(self, chat_id, task):
        r_menu = self.default_buttons(chat_id)
        # url = 'https://www.youtube.com/watch?v=gFn7V_pTJ-o'
        url = task['url']
        tr = task['time_remain']
        text = 'До конца сессии: {}:{}. Не трать время, работай :-) {}'.format(math.floor(tr/ 60), round(tr%60), url)

        r_menu[0]['text'] = 'Осталось {} мин'.format(task['time_remain_min'])
        r_menu[0]['callback_data'] = 'checktime_{}'.format(chat_id)

        response = {'text':text,'reply_markup_inline':r_menu}
        return response

    def tomato_update(self, chat_id, task):
        r_menu = self.default_buttons(chat_id)

        r_menu[0]['text'] = '{} мин'.format(task['time_remain_min'])
        r_menu[0]['callback_data'] = 'checktime_{}'.format(chat_id)

        response = {'reply_markup_inline':r_menu}
        return response


    def tomato_finish(self, chat_id, task):
        text = 'Время!'
        r_menu = self.default_buttons(chat_id)
        response = {'text':text,'reply_markup_inline':r_menu}
        return response

    def tomato_finish_text(self, chat_id):
        text = 'Время! Отдохни 5 минут и погнали снова'
        r_menu = self.default_buttons(chat_id)
        response = {'text':text,'reply_markup_inline':r_menu}
        return response

    def tomato_delete(self, chat_id):
        text = 'Мы все обнулили!'
        r_menu = self.default_buttons(chat_id)
        response = {'text':text,'reply_markup_inline':r_menu}
        return response


    def tomato(self, chat_id):
        text = 'Потоматим!'
        r_menu = self.default_buttons(chat_id)
        response = {'text':text,'reply_markup_inline':r_menu}
        return response


    def reset(self, chat_id):
        text = 'Потоматим!'
        r_menu = self.default_buttons(chat_id)
        response = {'text':text, 'reply_markup_inline':r_menu}
        return response


    def not_defined(self, chat_id):
        text = 'Мне нужно подумать над этим 🤔'
        r_menu = self.default_buttons(chat_id)

        response = {'text':text}
        return response


    def playlist_process(self, chat_id):
        r_menu = [
                {'text':'Да', 'callback_data':'addlink_{}'.format(chat_id)},
                {'text':'Нет', 'callback_data':'droplink_{}'.format(chat_id)}
            ]
        text = 'Добавить ссылку на рассмотрение в плейлист?'
        response = {'text':text,'reply_markup_inline':r_menu}

        return response


    def playlist_confirm(self, chat_id):
        text = 'Ссылка добавлена'
        response = {'text':text, 'reply_markup':[]}

        return response

    def playlist_cancel(self, chat_id):
        text = 'Добавление отменено. Ждем новых ссылок'
        response = {'text':text,'reply_markup':[]}

        return response
    # def playlist_process(self, chat_id):
    #     text = 'Ссылка добавлена'
    #     response = {'text':text}
    #
    #     return response


    def feedback_start(self, chat_id):

        text = 'Напишите свой вопрос'
        r_menu = ['Отмена']
        response = {'text':text, 'reply_markup':r_menu}

        return response


    def feedback_name(self, chat_id, text):

        text = 'Отлично! Теперь укажите Ваше имя'
        r_menu = ['Отмена']
        response = {'text':text, 'reply_markup':r_menu}

        return response


    def feedback_name_confirm(self, chat_id, text):

        text = 'Вы указали {}. Теперь укажите контактный телефон'.format(text)
        r_menu = ['Отмена']
        response = {'text':text, 'reply_markup':r_menu}

        return response


    def feedback_phone(self, chat_id, text):
        text = 'Вы указали телефон: {}. Теперь укажите город'.format(text)
        r_menu = ['Отмена']
        response = {'text':text, 'reply_markup':r_menu}

        return response


    def feedback_city(self, chat_id, text):
        text = 'Вы указали город: {}. Отправить заявку?'.format(text)
        r_menu = ['Отправить', 'Отмена']
        response = {'text':text, 'reply_markup':r_menu}

        return response


    def feedback_confirm(self, chat_id):
        text = 'Форма успешно отправлена'
        r_menu = ['Курсы валют', 'Офисы', 'Заявка']
        response = {'text':text, 'reply_markup':r_menu}

        return response

    def feedback_cancel(self, chat_id):
        text = 'Отмена отправки формы'
        r_menu = ['Курсы валют', 'Офисы', 'Заявка']
        response = {'text':text, 'reply_markup':r_menu}
        return response
