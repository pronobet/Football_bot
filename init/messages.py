from datetime import datetime
from init.class_user import payment_statuses, admin_list


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
            # f'/game_history - История Ваших тренировок\n'
            f'/training - Записать на тренировку\n'
            f'/training_info - Информация о ближайшей тренировке\n'
            
            
            f'Доступно только админу:\n'
            f'/new_training - Создать новую тренировку\n'
            # f'/payment_history - История Ваших пополнений\n'
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
    return f"Введите время начала тренировки:\nПример: 20.00"


def new_training_price_msg() -> str:
    return f"Введите стоимость тренировки:\nПример: 3500"


def new_training_notice(trainig):
    return f"Новая тренировка {trainig.date} в {trainig.time}\nЖдать тебя ?"


def training_notice(training):
    return f"Новая тренировка {training[3]} в {training[4]}\nЖдать тебя ?"


def bad_voice_to_trainig():
    return f"Очень жаль...\nБудем ждать тебя на следующей тренировке !)"


def add_to_training_success():
    return f"Отлично!\nБудем ждать тебя на тренировке!"


def add_to_training_added():
    return f"Вы уже добавлены на предстоящую тренировку!"


def add_to_training_error():
    return f"Ошибка...\nПопробуйте позже"


def training_info(training_info, users_list):
    output_str = f"Ближайшая тренирока {training_info[3]} в {training_info[4]}\nКоличество участников на данный момент: {training_info[5]}\nСписок участников:\n"
    for user in users_list:
        output_str += f"{user}\n"
    return output_str
