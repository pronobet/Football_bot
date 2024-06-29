from init.class_user import payment_statuses
from datetime import datetime
from init.db_funcs import *
from telebot import types


ADMINS = [2010916504, 664588645]


def start_message(message) -> str:
    if message.chat.first_name is not None:
        return (f'Привет, {message.chat.first_name}, добро пожаловать на добрый вечерний футбик!\n\n'
                f'Меня сделали, чтобы организация встреч была более автоматизированной и интерактивной. '
                f'Я помогу тебе узнать о ближайшем сборе, записаться на футбол, пополнить и узнать свой баланс.\n\n'
                f'Разработал @gavril_23')
    return (f'Привет, добро пожаловать на добрый вечерний футбик!\n\n'
            f'Меня сделали, чтобы организация встреч была более автоматизированной и интерактивной. '
            f'Я помогу тебе узнать о ближайшем сборе, записаться на футбол, пополнить и узнать свой баланс.\n\n'
            f'Разработал @gavril_23')


def function_list(user_id) -> str:
    output_str = (
        # f'Сегодня: {datetime.now().date().strftime("%d.%m.%Y")}\n\n'
        f'Вы можете воспользоваться командами:\n'
        f'/help — Помощь по командам бота\n'
        f'/training_info - Информация о ближайшей тренировке\n'
        f'/training - Записать на тренировку\n'
        f'/balance - Посмотреть состояние Вашего баланса\n'
        f'/pay - Пополнить баланс или оплатить тренировку'
    )
    if user_id in ADMINS:
        output_str += (f'\n\n/new_training - Создать новую тренировку\n'
                       f'/confirm_payments - Подтвердить новые платежи\n'
                       f'/confirm_training - Подтвердить завершение последней тренировки\n'
                       f'/change_training - Изменить параметры предстоящей тренировки\n'
                       f'/active_subscription - Активировать подписку для пользователя\n'
                       f'/users - Получить список всех пользователей\n'
                       f'/payments - Получить список всех платежей')
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
            f"Если ты с нами, отправь '+' в ответ на это сообщение.\n"
            f"А если в этот раз не получится, то отправь '-'")


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
    output_str += f"Имя пользователя: @{user_info[3]}\n" if user_info[3] else ''
    output_str += f"В этом месяце у Вас действует абонемент" if user_info[5] else f"Ваш баланс: {user_info[4]} RUB"
    return output_str


def training_info(training_info, users_list) -> str:
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


def confirm_payments_msg() -> str:
    return f"Список новых платежей на пополнение кошелька:"


def no_confirm_payments_msg() -> str:
    return f"На данный момент неподтвержденных платежей нет."


def payment_info_confirm(payment_info) -> str:
    output_str = f"Новый платеж!\nНа сумму: {payment_info[3]} RUB\nДата платежа: {payment_info[2]}\n"

    if payment_info[1] and payment_info[1] != '':
        output_str += f"От @{payment_info[1]}\n"
    else:
        user = get_info_about_user(payment_info[0])
        output_str += f"От {user[1]} {user[2]} (#{user[0]})\n"

    payment_status = payment_info[4]
    output_str += f"Статус платежа: {payment_statuses[payment_status]}"
    return output_str


def payment_success_confirmed(user_id) -> str:
    user_info = get_info_about_user(user_id)
    output_str = f"Платеж был успешно подтвержден\n\n"

    if user_info[3] and user_info[3] != "":
        output_str += f"Баланс пользователя @{user_info[3]}"
    else:
        output_str += f"Баланс пользователя {user_info[1]} {user_info[2]}"

    output_str += f" успешно пополнен"
    return output_str


def payment_success_rejected(user_id) -> str:
    return f"Платеж был отклонен"


def payment_success_error() -> str:
    return f"Произошла ошибка...\n\nПопрообуйте снова"


def confirm_training_msg() -> str:
    return f'Данная команда завершает тренировку со статусом "Новая" и списывает сумму со всех участников тренировки'


def confirm_training(training, users_list) -> str:
    output_str = (
        f"Тренировка {training[4]} в {training[5]}\n"
        f"Стоимость тренировки без подписки: {training[3]} RUB\n"
        f"Стоимость тренировки с подпиской: {training[2]} RUB\n"
        f"Количество участников в тренировке: {training[6]}\n\n"
    )

    if training[6] > 0:
        output_str += "Список участников:\n"
        for user in users_list:
            output_str += f"{user}\n"

    output_str += f"\nВы уверены, что хотите завершить тренировку ?"
    return output_str


def back_from_confirm_training() -> str:
    return (
        f"Данные об этой тренировке НЕ изменены.\n"
        f"Используйте другие возможности бота.\n\n"
        f"Список команд - /help"
    )


def no_confirm_training_msg() -> str:
    return (
        f"На данный момент нет тренировки, которую можно завершить.\n"
        f"Создайте тренировку, а уже после проведения её можно завершить или изменить статус"
    )


def created_soon():
    return f"Данная функция в разработке\nНо скоро все будет готово !)"


def success_cancel_training() -> str:
    return f"Тренировка успешно отменена"


def error_cancel_training() -> str:
    return f"Упс...\nИз-за ошибки не удалось отменить тренировку\n\nПопробуйте еще раз"


def success_complete_training() -> str:
    return f"Тренировка была успешно завершена!\n\nДеньги за тренировку были успешно списаны с участников"


def error_complete_training() -> str:
    return f"Упс...\nИз-за ошибки не удалось завершить тренировку\n\nПопробуйте еще раз"


def users_list_doc() -> str:
    return f"Список всех пользователей бота с данными из их личных кабинетов:"


def payments_list_doc() -> str:
    return f"Список всех платежей:"


def input_username() -> str:
    return f"Введите ID или username пользователя, чтобы изменить его данные о подписке:"


def error_change_subscription() -> str:
    return f"Упс...\nИз-за ошибки не удалось изменить статус подписки\n\nПопробуйте еще раз"


def action_subscription(user_dict) -> str:
    return (
        f"Пользователь:  {user_dict['name']} {user_dict['second_name']} (#{user_dict['id']})\n"
        f"Имя пользователя: {user_dict['username']}\n"
        f"Баланс: {user_dict['balance']}\n"
        f"Подписка на этот месяц: {'Активна' if user_dict['subscription'] else 'Не активна'}"
    )


def success_change_subscription() -> str:
    return f"Статус подписки успешно изменен!"


def change_training_msg(training_info, users_list) -> str:
    output_str = (
        f"Ближайшая тренирока\nДата: {training_info[4]}\nВремя: {training_info[5]}\n"
        f"Цена с подпиской: {training_info[2]} RUB\nЦена без подписки: {training_info[3]} RUB\n\n"
        f"Количество участников на данный момент: {training_info[6]}\n"
    )

    if training_info[6] > 0:
        output_str += "Список участников:\n"
        for user in users_list:
            output_str += f"{user}\n"

    output_str += f"\nВыберите какой параметр Вы хотите изменить:"
    return output_str


def change_training_date_msg() -> str:
    return f"Введите новую дату тренировки\nПример: 01.01.2024"


def change_training_time_msg() -> str:
    return f"Введите новое время начала тренировки:\nПример: 20.00"


def change_training_sub_price_msg() -> str:
    return f"Введите стоимость тренировки с подпиской:\nПример: 750"


def change_training_usual_price_msg() -> str:
    return f"Введите стоимость тренировки без подписки:\nПример: 1000"


def date_was_changed() -> str:
    return f"Дата тренировки была успешно изменена"


def time_was_changed() -> str:
    return f"Время тренировки было успешно изменено"


def sub_price_was_changed() -> str:
    return f"Цена с подпиской была успешно изменена"


def usual_price_was_changed() -> str:
    return f"Цена без подписки была успешно изменена"


def error_change_training() -> str:
    return f"Что-то пошло не так...\nПопробуйте позже или обратитесь к разработчику"
