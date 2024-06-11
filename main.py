from telebot.types import Message, CallbackQuery
from init.class_user import *
from init.keyboards import *
from init.messages import *
from init.db_funcs import *
from datetime import datetime
from decouple import config
from loguru import logger
import telebot


bot = telebot.TeleBot(config('football_bot'))
payment_link = config('payment_link')
admin_list = [2010916504, 664588645]
users_dict = dict()


@bot.message_handler(content_types=['text'])
def start(message: Message) -> None:
    """ CALLING AND PROCESSING BASIC BOT COMMANDS """

    global users_dict

    user_chat_id = message.chat.id
    users_dict[user_chat_id] = create_user(message.chat, BotUser(message.chat))
    user = users_dict[user_chat_id]

    if message.text == '/start':
        bot.send_message(user_chat_id, start_message(message))
        bot.send_message(user_chat_id, function_list(user_chat_id))
    elif message.text == '/help':
        bot.send_message(user_chat_id, function_list(user_chat_id))
    elif message.text == '/training':
        training = get_future_training()
        if training:
            bot.send_message(user_chat_id, training_notice(training))
            bot.register_next_step_handler(message, add_to_training, training)
        else:
            bot.send_message(user_chat_id, no_training_info())
    elif message.text == "/training_info":
        training = get_future_training()
        if training:
            users_list = get_users_on_training(training[7])
            bot.send_message(user_chat_id, training_info(training, users_list))
        else:
            bot.send_message(user_chat_id, no_training_info())
    elif message.text == '/balance':
        user_info = get_info_about_user(user_chat_id)
        bot.send_message(user_chat_id, show_user_balance(user_info))
    elif message.text == '/pay':
        bot.send_message(user_chat_id, pay(), reply_markup=payment_link_keyboard(payment_link))
        bot.send_message(user_chat_id, enter_amount_msg())
        bot.register_next_step_handler(message, enter_amount)
    elif message.text == '/confirm_payments' and user.user_id in admin_list:
        new_payments = get_new_payments()
        if new_payments and len(new_payments) > 0:
            bot.send_message(user_chat_id, confirm_payments_msg())
            confirm_payment(user_chat_id, new_payments[0])
        else:
            bot.send_message(user_chat_id, no_confirm_payments_msg())
    elif message.text == '/confirm_training' and user.user_id in admin_list:
        training = get_future_training()

        if training:
            bot.send_message(user_chat_id, confirm_training_msg())
            users_list = get_users_on_training(training[7])
            bot.send_message(user_chat_id, text=confirm_training(training, users_list), reply_markup=training_confirm_keyboard())
        else:
            bot.send_message(user_chat_id, no_confirm_training_msg())
    elif message.text == '/new_training' and user.user_id in admin_list:
        bot.send_message(user_chat_id, new_training_msg())
        bot.register_next_step_handler(message, new_training_date)
    else:
        bot.send_message(user_chat_id, function_list(user_chat_id))


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call: CallbackQuery) -> None:
    """ UPDATE PAYMENT STATUS FOR USER IN DB """

    user_id = call.message.chat.id
    user = users_dict[user_id]

    if ', ' in call.data:
        new_payment_status = call.data.split(', ')

        if new_payment_status[0] == 'confirmed':
            response, user_id = update_payment_in_db(new_payment_status)
        elif new_payment_status[0] == 'rejected':
            response, user_id = update_payment_in_db(new_payment_status)
        else:
            bot.send_message(user_id, 'Введен неверный вариант ответа...\nВыберите вариант из предложенных выше')
            response, user_id = 'error', None

        if response == 'confirmed':
            bot.send_message(user_id, payment_success_confirmed(user_id))
        elif response == 'rejected':
            bot.send_message(user_id, payment_success_rejected(user_id))
        else:
            bot.send_message(user_id, payment_success_error())

        bot.delete_message(user_id, call.message.message_id)
        new_payments = get_new_payments()
        if new_payments and len(new_payments) > 0:
            bot.send_message(user_id, confirm_payments_msg())
            confirm_payment(user_id, new_payments[0])
        else:
            bot.send_message(user_id, no_confirm_payments_msg())
    else:
        action = call.data

        if action == 'complete_training':
            training = get_future_training()
            response = complete_training(training)
            if response:
                bot.send_message(user_id, success_complete_training())
            else:
                bot.send_message(user_id, error_complete_training())
        elif action == 'cancel_training':
            training = get_future_training()
            response = cancel_training(training)
            if response:
                bot.send_message(user_id, success_cancel_training())
            else:
                bot.send_message(user_id, error_cancel_training())
        elif action == 'back_training':
            bot.send_message(user_id, back_from_confirm_training())
        bot.delete_message(user_id, call.message.message_id)


def new_training_date(message):
    """ START TO CREATE NEW TRAINING FROM DATE """

    trainig_date = message.text
    user_id = message.chat.id
    user = users_dict[user_id]

    try:
        date = datetime.strptime(trainig_date, "%d.%m.%Y").date()
        new_trainig = Training(trainig_date)
        bot.send_message(user_id, new_training_time_msg())
        bot.register_next_step_handler(message, new_training_time, new_trainig)
    except Exception as error:
        logger.error(f"Wrong input trainig date = {trainig_date} by {user}. Error: {error}")
        bot.send_message(user_id, 'Введена неверная дата тренировки...\nПопробуйте снова')
        bot.register_next_step_handler(message, new_training_date)


def new_training_time(message, new_trainig):
    """ CREATE NEW TRAINING FROM TIME """

    trainig_time = message.text
    user_id = message.chat.id
    user = users_dict[user_id]

    try:
        time = trainig_time.split('.')
        if len(time) == 2 and time[0].isdigit() and time[1].isdigit():
            new_trainig.time = trainig_time
            bot.send_message(user_id, new_training_price_subscription_msg())
            bot.register_next_step_handler(message, new_training_price_subscribe, new_trainig)
    except Exception as error:
        logger.error(f"Wrong input trainig time = {trainig_time} by {user}. Error: {error}")
        bot.send_message(user_id, 'Введено неверное время тренировки...\nПопробуйте снова')
        bot.register_next_step_handler(message, new_training_time)


def new_training_price_subscribe(message, new_trainig):
    """ CREATE THE NEW TRAINING, ADD PRICE FOR SUBSCRIBE"""

    price = message.text
    user_id = message.chat.id
    user = users_dict[user_id]

    try:
        price_for_subscribe = float(price)
        new_trainig.price_for_subscribe = price_for_subscribe
        bot.send_message(user_id, new_training_price_msg())
        bot.register_next_step_handler(message, new_training_price, new_trainig)
    except Exception as error:
        logger.error(f"Wrong input trainig time = {trainig_price} by {user}. Error: {error}")
        bot.send_message(user_id, 'Введена неверная стоимость тренировки...\nПопробуйте снова')
        bot.register_next_step_handler(message, new_training_price_subscribe, new_trainig)


def new_training_price(message, new_trainig):
    """ CREATE THE NEW TRAINING, ADD PRICE FOR USUAL """

    price = message.text
    user_id = message.chat.id
    user = users_dict[user_id]

    try:
        price_for_usual = float(price)
        new_trainig.price_for_usual = price_for_usual

        create_new_trainig(new_trainig)
        users = get_all_users_in_db()
        for user_id_in_db in users:
            if user_id_in_db == user_id:
                bot.send_message(user_id_in_db, new_training_was_created(new_trainig))
            else:
                bot.send_message(user_id_in_db, new_training_notice(new_trainig))
    except Exception as error:
        logger.error(f"Wrong input trainig time = {trainig_price} by {user}. Error: {error}")
        bot.send_message(user_id, 'Введена неверная стоимость тренировки...\nПопробуйте снова')
        bot.register_next_step_handler(message, new_training_price, new_trainig)


def add_to_training(message, training):
    """ ADD USER TO TRAINING """

    user_voice = message.text
    user_id = message.chat.id
    user = users_dict[user_id]

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


def enter_amount(message: Message) -> None:
    """ CREATE A NEW PAYMENT FOR USER """

    pay_amount = message.text
    user_id = message.chat.id
    user = users_dict[user_id]
    today_date = str(datetime.now().date().strftime('%d.%m.%Y'))

    try:
        new_payment = Payment(user_id, user.username, today_date, float(pay_amount))
        create_payment(new_payment)
        bot.send_message(user_id, success_payment(new_payment))
    except Exception as error:
        logger.error(f"Wrong input pay amount = {pay_amount} by {user}. Error: {error}")
        bot.send_message(user_id, 'Введено неверная сумма перевода...\nПопробуйте снова')
        bot.register_next_step_handler(message, enter_amount)


def confirm_payment(user_id, new_payment):
    """ START TO CONFIRM NEW PAYMENT """

    bot.send_message(
        user_id,
        text=payment_info_confirm(new_payment),
        reply_markup=payment_confirm_keyboard(new_payment)
    )


if __name__ == '__main__':
    logger.add('logger.log', level='DEBUG', format='{time} | {level} | {message}', encoding='utf-8')
    bot.polling(none_stop=True, interval=0)
