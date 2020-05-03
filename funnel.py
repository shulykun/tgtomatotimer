import config

from models import *
from semantic import TextProcessor

class funnelProcessor:

    def __init__(self):
        """Constructor"""
        self.textProcessor = TextProcessor()


    def add_context(self, chat_id, text):
        """добавление контекста к словам на основе предыдущих значений"""
        lf =  self.last_funnel(chat_id)
        if lf['chatfunnel'] == 'location':

            if self.textProcessor.check_location(text):
                pass
            else:
                text_reach = '{} {}'.format(text,lf['message'])
                return text_reach

        if lf['chatfunnel'] == 'office':
            if 'курс' not in text:
                if self.textProcessor.check_location(text):
                    text_reach = '{} {}'.format(text,lf['message'])
                    return text_reach

        if lf['chatfunnel'] == 'currency':
            if 'офис' not in text:
                if self.textProcessor.check_location(text):
                    text_reach = '{} {}'.format(text,lf['message'])
                    return text_reach

        return text


    # def set_funnel_location(self,chat_id,text):
    #     location = self.textProcessor.check_location(text)
    #     if location:
    #         self.set_funnel(chat_id, 'location', location)
    #     return 1


    def set_funnel(self, chat_id, chat_funnel, message_text, type = 1):
        """Сохранение состояния последней беседы. type: 1 запрос, 2 ответ."""

        funnel = ChatFunnel(chatuser_id=chat_id, chatfunnel=chat_funnel, message = message_text, type = type)
        funnel.save()

        return 1


    def last_funnel(self, chat_id, funnel_name=None):
        """определяем была ли уже воронка с фильтром и смотрим какие данные висят в ней"""

        r = {'chatfunnel':None, 'message':None}

        q =  ChatFunnel.select().where(ChatFunnel.chatuser_id == chat_id)
        if funnel_name:
            q = q.where(ChatFunnel.chatfunnel == funnel_name)

        last_funnel = q.order_by(ChatFunnel.id.desc())

        if len(last_funnel):
            last_funnel = last_funnel.get()
            r = {'chatfunnel':last_funnel.chatfunnel, 'message':last_funnel.message}
        return r
