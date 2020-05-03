import config
import telebot
import emoji
from menu import menuChat
from ga import gaTracker
from models import *

class Tonque:
    """Класс через который проходят все сообщения"""

    def __init__(self):
        self.bot = telebot.TeleBot(config.token)
        self.tracker = gaTracker()
        self.ADMIN_IDS = config.admin_ids
        self.menuChat = menuChat()


    def transform_buttons(self, response):
        if 'reply_markup' in response:
            response['reply_markup'] = self.menuChat.genButtons(response['reply_markup'])

        if 'reply_markup_inline' in response:
            response['reply_markup'] = self.menuChat.genInlineButtons(response['reply_markup_inline'])
            del response['reply_markup_inline']
        return response


    def send_message(self, chat_id, response):
        """Отправка сообщения"""

        response['disable_web_page_preview'] = False

        json_stored = Loghook(fulljson=str(response), chat_id = 2)#update.message.chat.id)
        json_stored.save()

        response = self.transform_buttons(response)

        if 'location' in response:
            location = response['location']
            del response['location']

            self.bot.send_message(chat_id, **response)
            self.send_location(chat_id, location)

        if 'text' in response:
            response['text'] = emoji.emojize(response['text'])
            self.bot.send_message(chat_id, **response)

        else:
            self.bot.send_message(chat_id, **response)

        url = self.tracker.storeOutputMessage(chat_id, response)

        return response


    def send_location(self, chat_id, location):
        """Отправка месторасположения"""
        self.bot.send_location(chat_id, location['lat'], location['lng'])
        self.tracker.storeOutputMessage(chat_id, {'text':'location'})
        return True


    def send_photo(self, chat_id, img, caption='', reply_markup=''):
        """Отправка фото"""

        self.bot.send_photo(chat_id, img, caption=caption, reply_markup=reply_markup)
        #self.bot.send_message(chat_id, **response)
        self.tracker.storeOutputMessage(chat_id, {'text':'photo'})
        return True


    def edit_message_caption(self, chat_id, message_id, response):
        """Отправка сообщения"""
        self.bot.edit_message_caption(response[0], chat_id=chat_id, message_id=message_id, reply_markup=response[1])
        return True


    def delete_message(self, chat_id, message_id):
        self.bot.delete_message(chat_id,message_id)
        return True


    def edit_message_text(self, chat_id, message_id, response):
        """Отправка сообщения"""
        response = self.transform_buttons(response)
        if 'text' in response:
            self.bot.edit_message_text(
                                        text=response['text'],
                                        chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=response['reply_markup']
                                    )
        else:
            self.bot.edit_message_reply_markup(
                                        chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=response['reply_markup']
                                    )

        return True


    def send_alert_admin(self, chat_id, message_id, text):
        """Отправка фото"""
        # for a_id in self.ADMIN_IDS:
        # self.send_message(a_id, {'text': alert_text})
        for a_id in self.ADMIN_IDS:
            # self.send_message(a_id, {'text': 'Вопрос от пользователя:'})
            self.bot.forward_message(a_id, chat_id, message_id)



        return True
