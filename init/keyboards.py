from telebot import types


def payment_confirm_keyboard(payment) -> types.InlineKeyboardMarkup:
    """ CONFIRM PAYMENT KEYBOARD """

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Потвердить', callback_data=f'confirmed, {payment[0]}, {payment[3]}'))
    keyboard.add(types.InlineKeyboardButton(text='Отклонить', callback_data=f'rejected, {payment[0]}, {payment[3]}'))
    return keyboard


def training_confirm_keyboard() -> types.InlineKeyboardMarkup:
    """ CONFIRM TRAINING KEYBOARD """

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Завершить', callback_data=f'complete_training'))
    keyboard.add(types.InlineKeyboardButton(text='Отменить тренировку', callback_data=f'cancel_training'))
    keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data=f'back_training'))
    return keyboard


def payment_link_keyboard(payment_link) -> types.InlineKeyboardMarkup:
    """ PAYMENT URL LINK KEYBOARD """

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='Оплатить', url=payment_link))
    return keyboard


def action_subscription_keyboard(user_id) -> types.InlineKeyboardMarkup:
    """ CHOOSE ACTION FOR SUBSCRIPTION KEYBOARD """

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Активировать', callback_data=f'active_subscription-{user_id}'))
    keyboard.add(types.InlineKeyboardButton(text='Отменить', callback_data=f'cancel_subscription-{user_id}'))
    return keyboard


def change_training_keyboard() -> types.InlineKeyboardMarkup:
    """ CHOOSE ACTION FOR SUBSCRIPTION KEYBOARD """

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Время', callback_data=f'time'))
    keyboard.add(types.InlineKeyboardButton(text='Дата', callback_data=f'date'))
    keyboard.add(types.InlineKeyboardButton(text='Цена с подпиской', callback_data=f'prive_with_subscription'))
    keyboard.add(types.InlineKeyboardButton(text='Цена без подписки', callback_data=f'prive_without_subscription'))
    keyboard.add(types.InlineKeyboardButton(text='< Назад', callback_data=f'back_training'))
    return keyboard
