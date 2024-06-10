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
