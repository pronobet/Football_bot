from init.class_user import payment_statuses
from datetime import datetime
from telebot import types


ADMINS = [2010916504, 664588645]


def start_message(message) -> str:
    if message.chat.first_name is not None:
        return (f'Привет, {message.chat.first_name}, добро пожаловать на добрый вечерний футбик!\n\n'
                f'Меня сделали что бы организация встреч была более автоматизированной и интерактивной. '
                f'Я помогу тебе узнать о ближайшем сборе, записаться на футбол, пополнить и узнать свой баланс.\n\n'
                f'Разработал @gavril_23')
    return (f'Привет, добро пожаловать на добрый вечерний футбик!\n\n'
            f'Меня сделали что бы организация встреч была более автоматизированной и интерактивной. '
            f'Я помогу тебе узнать о ближайшем сборе, записаться на футбол, пополнить и узнать свой баланс.\n\n'
            f'Разработал @gavril_23')


def function_list(user_id) -> str:
    output_str = (f'Сегодня: {datetime.now().date().strftime("%d.%m.%Y")}\n\n '
                  f'Вы можете воспользоваться командами:\n'
                  f'/help — Помощь по командам бота\n'
                  f'/training_info - Информация о ближайшей тренировке\n'
                  f'/training - Записать на тренировку\n'
                  f'/balance - Посмотреть состояние Вашего баланса\n'
                  f'/pay - Пополнить баланс или оплатить тренировку')
    if user_id in ADMINS:
        output_str += (f'\n\n/new_training - Создать новую тренировку\n'
                       f'/confirm_payments - Подтвердить новые платежи\n'
                       f'/confirm_training - Подтвердить завершение последней тренировки\n')
    return output_str


def new_training_msg() -> str:
    return f"Начнем создание тренировки.\nВведите дату новой тренировки\nПример: 01.01.2024"


def new_training_time_msg() -> str:
    return f"Введите время начала новой тренировки:\nПример: 20.00"


def new_training_price_subscription_msg() -> str:
    return f"Введите стоимость тренировки для пользователей с подпиской:\nПример: 850"


def new_training_price_msg() -> str:
    return f"Введите стоимость тренировки для пользователей без подписки:\nПример: 1000"


def new_training_notice(new_trainig) -> str:
    return f"Новая тренировка {new_trainig.date} в {new_trainig.time}!!!\nЕсли ты с нами, воспользуйся командой /training и отправь '+' в ответ на мое сообщение."


def new_training_was_created(new_trainig) -> str:
    return (f"Новая тренировка успешно создана!\n\n"
            f"Дата: {new_trainig.date}\n"
            f"Время: {new_trainig.time}\n"
            f"Цена тренировки для участников с подпиской: {new_trainig.price_for_subscribe}\n"
            f"Цена тренировки для участников без подписки: {new_trainig.price_for_usual}\n\n"
            f"Сообщение о новой тренировке были разозланы всем пользователям бота.")


def training_notice(new_trainig) -> str:
    return (f"Новая тренировка {new_trainig[4]} в {new_trainig[5]}\n"
            f"Если ты с нами, воспользуйся командой /training и отправь '+' в ответ на мое сообщение.\n"
            f"А если в этот раз не получится, то отправь '-'.")


def add_to_training_success() -> str:
    return (f"Отлично!\n"
            f"Я добавил Вас на тренировку.\n"
            f"До встречи!")


def add_to_training_added() -> str:
    return f"Вы уже добавлены на предстоящую тренировку!"


def add_to_training_error() -> str:
    return (f"Упссс...\n"
            f"Возникла ошибка, попробуйте позже")


def bad_voice_to_trainig() -> str:
    return (f"Очень жаль...\n"
            f"Будем ждать тебя на следующей тренировке!")


def no_training_info() -> str:
    return f"Нет запланированных тренировок...\nКак только администратор создаст тренировку, я сразу Вам напишу"


def show_user_balance(user_info) -> str:
    output_str = f"Ваше имя: {user_info[1]} {user_info[2]}\n" if user_info[1] or user_info[2] else ''
    output_str += f"Имя пользователя: {user_info[3]}\n" if user_info[3] else ''
    output_str += f"В этом месяце у Вас действует абонемент" if user_info[5] else f"Ваш баланс: {user_info[4]}"
    return output_str


def training_info(training_info, users_list):
    output_str = (
        f"Ближайшая тренирока {training_info[4]} в {training_info[5]}\n"
        f"Количество участников на данный момент: {training_info[6]}\n\n"
    )

    if training_info[6] > 0:
        output_str += "Список участников:\n"
        for user in users_list:
            output_str += f"{user}\n"
    return output_str


def pay() -> str:
    return f"Чтобы пополнить Ваш счет переведите деньги, пройдя по ссылке ниже:\n"


def enter_amount_msg() -> str:
    return f"Введите сумму пополнения:"


def success_payment(payment) -> str:
    return (
        f"Платеж успешно создан!\n"
        f"{payment}\n"
        f"Ожидайте подтверждение платежа администратором!"
    )














def check_balance(user) -> str:
    return f""


def payment_history_msg(payments_list):
    output_strig = ''

    for payment in payments_list:
        output_strig += f"Платеж от {payment[3]}\nСумма платежа: {payment[2]} RUB\nСтатус платежа: {payment_statuses[payment[1]]}\n\n"
    return output_strig


def confirm_payments_msg():
    return f"Список новых плаежей на пополнения кошелька пользователя: "


def payment_info_confirm(payment_info):
    return f"Новый платеж!\nСумма: {payment_info[3]}\nДата: {payment_info[4]}\nОт: @{payment_info[1]} "


def no_new_payments_msg():
    return f'Нет новых платежей'


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
