from init.class_user import BotUser, Payment, Training
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from init.messages import *
from datetime import datetime
from decouple import config
from loguru import logger
from typing import Dict
from init.db_funcs import *
import telebot


bot = telebot.TeleBot(config('football_bot'))
users_dict: Dict[int, BotUser] = dict()


@bot.message_handler(content_types=['text'])
def start(message: Message) -> None:
    """ Функция вызова и обработки основных команд бота """
    global users_dict

    user_chat_id = message.chat.id
    users_dict[user_chat_id] = create_user(message.chat, BotUser(message.chat))
    user = users_dict[user_chat_id]

    if message.text == '/start':
        bot.send_message(user_chat_id, start_message(message))
        bot.send_message(user_chat_id, function_list())
    elif message.text == '/help':
        bot.send_message(user_chat_id, function_list())
    elif message.text == '/pay':
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(text='Оплатить', url=url_for_pay()))
        bot.send_message(user_chat_id, pay(), reply_markup=keyboard)
        bot.send_message(user_chat_id, enter_amount_msg())
        bot.register_next_step_handler(message, enter_amount)
    elif message.text == '/balance':
        bot.send_message(user_chat_id, users_dict[user_chat_id].show_balance())
    elif message.text == '/game_history':
        bot.send_message(user_chat_id, users_dict[user_chat_id].show_game_history())
    # elif message.text == '/payment_history':
    #     payments_in_db = payment_history(user_chat_id)
    #     bot.send_message(user_chat_id, payment_history_msg(payments_in_db))
    elif message.text == '/training':
        training = get_future_training()
        bot.send_message(user_chat_id, training_notice(training))
        bot.register_next_step_handler(message, add_to_training, training)
    elif message.text == "/training_info":
        training = get_future_training()
        users_list = get_users_on_training(training[6])
        bot.send_message(user_chat_id, training_info(training, users_list))
    elif message.text == '/new_training' and user.group == 'admin':
        bot.send_message(user_chat_id, new_training_msg())
        bot.register_next_step_handler(message, new_training_date)
    else:
        bot.send_message(user_chat_id, function_list())


def enter_amount(message: Message) -> None:
    pay_amount = message.text
    user_id = message.chat.id
    user = users_dict[user_id]
    today_date = str(datetime.now().date().strftime('%d.%m.%Y'))

    try:
        new_payment = Payment(today_date, float(pay_amount), user_id)
        create_payment(new_payment)
        bot.send_message(message.chat.id, success_payment(new_payment))
    except Exception as error:
        logger.error(f"Wrong input pay amount = {pay_amount} by {user}. Error: {error}")
        bot.send_message(user_id, 'Введено неверная сумма перевода...\nПопробуйте снова')
        bot.register_next_step_handler(message, enter_amount)


def new_training_date(message):
    trainig_date = message.text
    user_id = message.chat.id
    user = users_dict[user_id]
    redirect_to_start(message)

    try:
        date = datetime.strptime(trainig_date, "%d.%m.%Y").date()
        new_trainig = Training(trainig_date)
        bot.send_message(message.chat.id, new_training_time_msg())
        bot.register_next_step_handler(message, new_training_time, new_trainig)
    except Exception as error:
        logger.error(f"Wrong input trainig date = {trainig_date} by {user}. Error: {error}")
        bot.send_message(user_id, 'Введено неверная дата тренировки...\nПопробуйте снова')
        bot.register_next_step_handler(message, new_training_date)


def new_training_time(message, new_trainig):
    trainig_time = message.text
    user_id = message.chat.id
    user = users_dict[user_id]

    try:
        time = trainig_time.split('.')
        if len(time) == 2 and time[0].isdigit() and time[1].isdigit():
            new_trainig.time = trainig_time
            bot.send_message(message.chat.id, new_training_price_msg())
            bot.register_next_step_handler(message, new_training_price, new_trainig)
    except Exception as error:
        logger.error(f"Wrong input trainig time = {trainig_time} by {user}. Error: {error}")
        bot.send_message(user_id, 'Введено неверное время тренировки...\nПопробуйте снова')
        bot.register_next_step_handler(message, new_training_time)


def new_training_price(message, new_trainig):
    trainig_price = message.text
    user_id = message.chat.id
    user = users_dict[user_id]

    try:
        price = float(trainig_price)
        new_trainig.price = price

        create_new_trainig(new_trainig, user_id)
        users = get_all_user_in_db()
        for user_id in users:
            bot.send_message(user_id, new_training_notice(new_trainig))
            bot.register_next_step_handler(message, training_vote)
    except Exception as error:
        logger.error(f"Wrong input trainig time = {trainig_price} by {user}. Error: {error}")
        bot.send_message(user_id, 'Введена неверная стоимость тренировки...\nПопробуйте снова')
        bot.register_next_step_handler(message, new_training_price)


def training_vote(message):
    """ ADD USER TO TRAINING """

    user_voice = message.text
    user_id = message.chat.id
    user = users_dict[user_id]

    try:
        if user_voice == '+':
            add_user_success = add_user_to_training(user)
            print(add_user_success)
        elif user_voice == '-':
            bot.send_message(user_id, bad_voice_to_trainig())
        else:
            bot.send_message(user_id, 'Введен неверный вариант ответа...\nПопробуйте снова')
            bot.register_next_step_handler(message, training_vote)
    except Exception as error:
        bot.send_message(user_id, 'Введен неверный вариант ответа...\nПопробуйте снова')
        bot.register_next_step_handler(message, training_vote)


def add_to_training(message, training):
    """ ADD USER TO TRAINING """

    user_voice = message.text
    user_id = message.chat.id
    user = users_dict[user_id]

    try:
        if user_voice == '+':
            add_user_success = add_user_to_training(user)
            if add_user_success == 'success':
                bot.send_message(user_id, add_to_training_success())
            elif add_user_success == 'added':
                bot.send_message(user_id, add_to_training_added())
            else:
                bot.send_message(user_id, add_to_training_error())
        elif user_voice == '-':
            bot.send_message(user_id, bad_voice_to_trainig())
        else:
            bot.send_message(user_id, 'Введен неверный вариант ответа...\nПопробуйте снова')
            bot.register_next_step_handler(message, add_to_training, training)
    except Exception as error:
        bot.send_message(user_id, 'Введен неверный вариант ответа...\nПопробуйте снова')
        bot.register_next_step_handler(message, add_to_training, training)


def url_for_pay() -> str:
    return 'https://www.tinkoff.ru/rm/agalakov.dmitriy18/CaD269995'


def redirect_to_start(message):
    print(message.text)
    if message.text.startswith('/'):
        bot.register_next_step_handler(message, start)

if __name__ == '__main__':
    logger.add('logger.log', level='DEBUG', format='{time} {level} {message}', encoding='utf-8')
    bot.polling(none_stop=True, interval=0)