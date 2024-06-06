from telebot.types import Chat
from datetime import datetime


payment_statuses = {
    'new': 'Новый',
    'confirmed': 'Подтвержден',
    'rejected': 'Отклонен'
}

training_statuses = {
    'new': 'Новая',
    'confirmed': 'Завершена',
    'rejected': 'Отменена'
}


class BotUser:
    """ Class: Telegram bot's user """

    def __init__(self, chat: Chat) -> None:
        self.first_name = chat.first_name
        self.last_name = chat.last_name
        self.username = chat.username
        self.user_id = chat.id
        self.balance = float()
        self.subscription = False


class Training:
    """ Class: Football training """

    def __init__(self, date):
        self.status = 'new'
        self.price_for_subscribe = float()
        self.price_for_usual = float()
        self.date = date
        self.time = str()
        self.members_count = int()
        self.members = str()


class Payment:
    """ Class: Payment"""

    def __init__(self, user_id, username, date,  amount):
        self.user_id = user_id
        self.username = username
        self.date = date
        self.amount = amount
        self.status = 'new'

    def __str__(self):
        return (
            f"Платеж от {self.date}\n"
            f"Сумма платежа: {self.amount} RUB\n"
        )
