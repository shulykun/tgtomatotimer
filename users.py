from models import *

class UserProcessor:
    def __init__(self):
        pass

    def user_update(self, message, user_id):
        """Сохранение пользователя"""
        try:
            c = ChatUser.get(ChatUser.id == user_id)

        except ChatUser.DoesNotExist:
            user_first_name = getattr(message.from_user, 'first_name', '-')
            user_last_name = getattr(message.from_user, 'last_name', '-')
            user_username = getattr(message.from_user, 'username', '-')
            user_phone = getattr(message.from_user, 'phone', '-')
            c = ChatUser.create(id=user_id, first_name=user_first_name, last_name=user_last_name,
                                username=user_username, phone=user_phone, subscribed=0)

        except AttributeError:
            return 'Wrong Attribute'

        return 1
