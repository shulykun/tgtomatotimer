# import json
from models import *
from telebot import types

class menuChat:

    def __init__(self):
        """Constructor"""
        pass

    def genInlineButtons(self, inline_buttons):
        """Генерация inline-кнопок в меню"""

        keyboard = types.InlineKeyboardMarkup()

        buttons = []
        for ib in inline_buttons:
            buttons.append(types.InlineKeyboardButton(**ib))

        keyboard.add(*buttons)

        return keyboard


    def genButtons(self, menu_content):
        """составление меню"""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        buttons = []
        for b_content in menu_content:
            buttons.append(types.KeyboardButton(b_content))
        keyboard.add(*buttons)

        return keyboard


    def startMenu(self):
        '''Меню при начале работы с ботом'''

        menu_content = ['Каталог', 'Магазины', 'Подписка на скидки', 'Акции']
        markup = self.genButtons(menu_content)

        return markup
