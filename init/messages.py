from datetime import datetime
from init.class_user import payment_statuses, admin_list
from telebot import types


def start_message(message) -> str:
    if message.chat.first_name is not None:
        return f'Здравствуйте, {message.chat.first_name} 👋\n' \
               f'Это бот, который поможет вести посещаемость и оплату тренировок\n'
    return f'Здравствуйте 👋\n' \
           f'Это бот, который поможет вести посещаемость и оплату тренировок\n'


def function_list() -> str:
    return (f'Сегодня: {datetime.now().date().strftime("%d.%m.%Y")}\n\n'
            f'Вы можете воспользоваться командами:\n'
            f'/help — Помощь по командам бота\n'
            f'/balance - Посмотреть состояние Вашего баланса\n'
            f'/pay - Пополнить баланс или оплатить тренировку\n'
            f'/training - Записать на тренировку\n'
            f'/training_info - Информация о ближайшей тренировке\n\n\n'
            
            
            f'Доступно только админу:\n'
            f'/new_training - Создать новую тренировку\n'
            f'/confirm_payments - Подтвердить новые платежи\n'
            f'/confirm_training - Подтвердить завершение последней тренировки\n'
    )


def pay() -> str:
    return f"Чтобы пополнить счет переведите деньги, пройдя по ссылке ниже:\n"


def enter_amount_msg() -> str:
    return f"Введите сумму перевода:"


def success_payment(payment) -> str:
    return (f"Платеж успешно создан !\n"
            f"{payment}")


def check_balance(user) -> str:
    return f""


def payment_history_msg(payments_list):
    output_strig = ''

    for payment in payments_list:
        output_strig += f"Платеж от {payment[3]}\nСумма платежа: {payment[2]} RUB\nСтатус платежа: {payment_statuses[payment[1]]}\n\n"
    return output_strig


def new_training_msg() -> str:
    return f"Начнем создание тренировки.\nВведите дату новой тренировки\nПример: 01.01.2024"


def new_training_time_msg() -> str:
    return f"Введите время начала новой тренировки:\nПример: 20.00"


def new_training_price_msg() -> str:
    return f"Введите стоимость тренировки:\nПример: 3500"


def new_training_notice(trainig):
    return f"Новая тренировка {trainig.date} в {trainig.time}\nЖдать тебя ?\nЕсли ты с нами, воспользуйся командой /training и отправь +"


def training_notice(training):
    return f"Новая тренировка {training[3]} в {training[4]}\nЖдать тебя ?\nДля ответа напиши + или -"


def bad_voice_to_trainig():
    return f"Очень жаль...\nБудем ждать тебя на следующей тренировке !)"


def add_to_training_success():
    return f"Отлично!\nБудем ждать тебя на тренировке!"


def add_to_training_added():
    return f"Вы уже добавлены на предстоящую тренировку!"


def add_to_training_error():
    return f"Ошибка...\nПопробуйте позже"


def training_info(training_info, users_list):
    output_str = f"Ближайшая тренирока {training_info[3]} в {training_info[4]}\nКоличество участников на данный момент: {training_info[5]}\n\n"

    if training_info[5] > 0:
        output_str += "Список участников:\n"
        for user in users_list:
            output_str += f"{user}\n"
    return output_str


def confirm_payments_msg():
    return f"Список новых плаежей на пополнения кошелька пользователя: "






def payment_info_confirm(payment_info):
    return f"Новый платеж!\nСумма: {payment_info[3]}\nДата: {payment_info[4]}\nОт: @{payment_info[1]} "


def no_new_payments_msg():
    return f'Нет новых платежей'


def no_training_info():
    return f"Нет запланированных тренировок...\nКак только администратор создаст тренировку, мы сразу Вам напишем"


def confirm_training_msg():
    return f"Данная команда завершает тренировку со статусом 'Новая' и списывает равную сумму со всех участников тренировки"


def confirm_training(training):
    text = f"Тренировка {training[3]} в {training[4]}\nКоличество участников в тренировке: {training[5]}\nСтоимость тренировки: {training[2]} RUB\n\n"
    text += f"Вы уверены, что хотите завершить тренировку ?"
    return text


def back_from_confirm_training():
    return f"Данные о тренировке НЕ изменены.\nИспользуйте другие возможности бота."


def created_soon():
    return f"Данная функция в разработке\nНо скоро все будет готово !)"


def no_confirm_training_msg():
    return f"На данный момент нет тренировки, которую можно завершить.\nСоздайте тренировку, а уже после ее проведения можно завершить и изменить статус"


def payment_confirm_keyboard(payment) -> types.InlineKeyboardMarkup:
    """ CONFIRM PAYMENT KEYBOARD """

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Потвердить', callback_data=f'confirmed, {payment[0]}, {payment[3]}'))
    keyboard.add(types.InlineKeyboardButton(text='Отклонить', callback_data=f'rejected, {payment[0]}, {payment[3]}'))
    return keyboard


def training_confirm_keyboard() -> types.InlineKeyboardMarkup:
    """ CONFIRM TRAINING KEYBOARD """

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Завершить', callback_data=f'complete training'))
    keyboard.add(types.InlineKeyboardButton(text='Отменить тренировку', callback_data=f'cancel training'))
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f'back'))
    return keyboard
