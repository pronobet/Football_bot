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

user_group = {
    'new': 'Новый',
    'confirmed': 'Подтвержден',
    'rejected': 'Отклонен'
}

admin_list = [2010916504, 664588645]

class BotUser:
    """ Class: Telegram bot's user """

    def __init__(self, chat: Chat) -> None:
        self.first_name = chat.first_name
        self.last_name = chat.last_name
        self.username = chat.username
        self.user_id = chat.id
        self.balance = float()
        self.training_history = str()
        self.group = 'admin' if chat.id in admin_list else 'user'

    def add_training(self, training):
        self.training_history.append(training)

    def show_balance(self):
        return (f"Ваш баланс:\n"
                f"{self.balance} RUB")

    def show_game_history(self):
        return (f"История Ваших тренировок:\n"
                f"{self.training_history}")

    def __str__(self) -> str:
        return (f'First name: {self.first_name}, Last name: {self.last_name}, User ID: {self.user_id}, '
                f'Username: @{self.username} {self.balance}, {self.training_history}, {self.group}')


class Training:
    """ Class: Football training"""

    def __init__(self, date):
        self.date = date
        self.id = int()
        self.time = str()
        self.price = float()
        self.members_count = int()
        self.members = str()
        self.status = str()

    def __str__(self) -> str:
        return f"Тренировка {self.date} {self.time}"


class Payment:
    """ Class: Payment"""

    def __init__(self, date, amount, user_id, username):
        self.date = date
        self.amount = amount
        self.user_id = user_id
        self.username = username
        self.status = 'new'

    def __str__(self):
        return (f"Платеж от {self.date}\n"
                f"Сумма: {self.amount}\n"
                f"Статус платежа: {payment_statuses[self.status]}")