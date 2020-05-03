from models import *
from funnel import funnelProcessor
from replics import Replics
from semantic import TextProcessor
from emailsender import EmailSender

class feedbackChat:
    def __init__(self):
        """Constructor"""
        self.replics = Replics()
        self.funnel = funnelProcessor()
        self.textProcessor = TextProcessor()
        self.email = EmailSender()


    def new_chat(self, chat_id, message_id, text, text_raw):
        fb = ChatFeedback(chatuser_id=chat_id)
        fb.save()
        return fb.id


    def open_last_chat(self, chat_id):
        fb =  ChatFeedback.select().where((ChatFeedback.chatuser_id == chat_id)).order_by(ChatFeedback.id.desc()).dicts()
        if len(fb):
            fb = fb.get()

        return fb


    def update_chat(self, id, fields):
        # query = ChatFeedback.update(**fields).where(ChatFeedback.id == id)
        query = ChatFeedback.update(**fields).where(ChatFeedback.id == id)
        query.execute()
        return query


    def name_add(self, chat_id, message_id, text, text_raw):

        last_chat = self.open_last_chat(chat_id)
        self.update_chat(last_chat['id'], {'name':text_raw})

        response = self.replics.feedback_name_confirm(chat_id, text_raw)
        self.funnel.set_funnel(chat_id, 'feedback_phone', '')
        return response


    def name_confirm(self, chat_id, message_id, text, text_raw):
        pass


    def phone_add(self, chat_id, message_id, text, text_raw):
        response = self.replics.feedback_phone(chat_id, text_raw)

        last_chat = self.open_last_chat(chat_id)
        self.update_chat(last_chat['id'], {'phone':text_raw})

        self.funnel.set_funnel(chat_id, 'feedback_city', '')
        return response


    def phone_confirm(self, chat_id, message_id, text, text_raw):
        pass


    def city_add(self, chat_id, message_id, text, text_raw):

        last_chat = self.open_last_chat(chat_id)
        self.update_chat(last_chat['id'], {'location':text_raw})

        response = self.replics.feedback_city(chat_id, text_raw)
        self.funnel.set_funnel(chat_id, 'feedback_form_confirm', '')

        return response


    def text_add(self, chat_id, message_id, text, text_raw):

        last_chat = self.open_last_chat(chat_id)
        self.update_chat(last_chat['id'], {'message':text_raw})

        response = self.replics.feedback_name(chat_id, text_raw)
        self.funnel.set_funnel(chat_id, 'feedback_name', '')

        return response


    def city_confirm(self, chat_id, message_id, text, text_raw):
        pass

    def time_add(self, chat_id, message_id, text, text_raw):
        pass

    def time_confirm(self, chat_id, message_id, text, text_raw):
        pass

    def form_confirm(self, chat_id, message_id, text, text_raw):
        # last_chat = self.open_last_chat(chat_id)
        # self.update_chat(last_chat['id'], {'location':text_raw})

        sentiment = self.textProcessor.define_positive(text_raw)

        if sentiment == 1:
            response = self.replics.feedback_confirm(chat_id)
            self.funnel.set_funnel(chat_id, 'drop', '')
        else:
            response = self.replics.feedback_cancel(chat_id)
            self.funnel.set_funnel(chat_id, 'drop', '')

        self.send_email(chat_id)

        return response

    def get_username(self, chat_id):
        fb =  ChatUser.select().where((ChatUser.id == chat_id)).get()
        if fb.username:
            un = '(ник: @{})'.format(fb.username)
        else:
            un = ''
        return un



    def send_email(self, chat_id):
        last_chat = self.open_last_chat(chat_id)
        username = self.get_username(chat_id)

        message = 'Клиент: {} {}\n\nГород: {}\n\nТелефон: {}\n\nСообщение: {}'.format(last_chat['name'],
                                          username,
                                          last_chat['location'],
                                          last_chat['phone'],
                                          last_chat['message']
                                        )
        self.email.send_email(message)

        return 1
