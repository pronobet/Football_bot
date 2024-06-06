from loguru import logger
import sqlite3


db_name = 'bot_db.db'


# OPERATIONS WITH PAYMENT TABLE
def create_payment_table():
    """ CREATE PAYMENT TABLE """

    try:
        payment_table = sqlite3.connect(db_name)
        cursor = payment_table.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS payments(user_id INTEGER, username TEXT, date TEXT, amount REAL, status TEXT);""")
        payment_table.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with creating payment table: {error}')


def create_payment(payment):
    """CREATE NEW PAYMENT """

    create_payment_table()

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO payments VALUES(?, ?, ?, ?, ?)", (payment.user_id, payment.username, payment.date, payment.amount, payment.status))
        db.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with creating new payment({payment}): {error}')


def payment_history(user_id):
    """ GET ALL USER'S PAYMENTS IN DB """

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM payments WHERE user_id={user_id}")
        response = cursor.fetchall()
        cursor.close()
        if response:
            return response
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    return False


def get_new_payments():
    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM payments WHERE status='new'")
        response = cursor.fetchall()
        cursor.close()
        if response:
            return response
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    return None


def update_payment_in_db(payment):
    """ UPDATE PAYMENT STATUS IN DB"""
    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(f"UPDATE payments SET status = ? WHERE user_id = ? AND status = ? AND amount = ?", (payment[0], int(payment[1]), 'new', float(payment[2])))
        db.commit()
        if payment[0] == 'confirmed':
            cursor.execute(f"SELECT * FROM users WHERE user_id={int(payment[1])}")
            response = cursor.fetchall()[0]
            user_balance = float(response[4]) + float(payment[2])
            cursor.execute(f"UPDATE users SET balance = ? WHERE user_id = ?", (user_balance, response[0]))
            db.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with update payment status in DB: {error}')
    return 'error'


# OPERATIONS WITH TRAINING TABLE
def create_trainig_table():
    """ CREATE TRAINING TABLE for BOT """

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS training(id INTEGER, status TEXT, price_for_subscribe REAL, price_for_usual REAL, date TEXT, time TEXT, members_count INTEGER, members TEXT);""")
        db.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with creating paymen table: {error}')


def cancel_new_trainings():
    """ GET ALL TRAININGS WITH STATUS = NEW AND CANCEL THEM """

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM training WHERE status='new'")
        response = cursor.fetchall()
        for training in response:
            cursor.execute(f"UPDATE training SET status='rejected' WHERE id={training[0]}")
            response = cursor.fetchall()
            db.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')


def get_new_training_id():
    """ GET ALL TRAININGs COUNT IN DB """

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM training")
        response = cursor.fetchall()
        cursor.close()
        return len(response) + 1
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    return 0


def create_new_trainig(training):
    """ CREATE NEW TRAINING IN DB """

    create_trainig_table()
    new_id = get_new_training_id()
    cancel_new_trainings()

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO training VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (new_id, 'new', training.price_for_subscribe, training.price_for_usual, training.date, training.time, 0, ''))
        db.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with creating new trainig(date={date}): {error}')


def get_future_training():
    """ GET FUTURE TRAINING WITH STATUS 'new' IN DB"""

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM training WHERE status='new'")
        response = cursor.fetchall()[0]
        db.commit()
        cursor.close()
        return response
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with get training in DB with status = "new": {error}')
    return None


def add_user_to_training(user):
    """ ADD USER TO NEW TRAINIG """

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM training WHERE status='new'")
        training = cursor.fetchall()[0]
        user_count = int(training[6])
        user_list = str(training[7])

        if str(user.user_id) not in user_list:
            new_user_list = user_list + f'{str(user.user_id)}, '
            cursor.execute(f"UPDATE training SET members_count = ? WHERE id = ?", (user_count + 1, training[0]))
            db.commit()
            cursor.execute(f"UPDATE training SET members = ? WHERE id = ?", (new_user_list, training[0]))
            db.commit()
            cursor.close()
            return 'success'
        else:
            cursor.close()
            return 'added'
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    except Exception as ex_error:
        pass
    return False


def get_users_on_training(users_id_list):
    """ GET USERS ON TRAINING """

    users_list = users_id_list.split(', ')
    users_username = list()

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        for user_id in users_list:
            if user_id:
                cursor.execute(f"SELECT * FROM users WHERE user_id={int(user_id)}")
                response = cursor.fetchall()[0]
                db.commit()
                if response[3]:
                    users_username.append(f"@{response[3]}")
                else:
                    users_username.append(f"{response[1] if response[1] else None} {response[2] if response[2] else None} (#{response[0]})")
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with get users on training in DB: {error}')
    return users_username


# OPERATIONS WITH USERS TABLE
def create_user_table():
    """ CREATE DB for BOT """

    try:
        table = sqlite3.connect(db_name)
        cursor = table.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, first_name TEXT, last_name TEXT, username TEXT,  balance REAL, subscription BOOLEAN);""")
        table.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with creating user table: {error}')


def check_user_in_db(user_id):
    """ CHECK USER IN DB """

    try:
        table = sqlite3.connect(db_name)
        cursor = table.cursor()
        cursor.execute(f"SELECT * FROM users WHERE user_id={user_id}")
        response = cursor.fetchall()
        cursor.close()
        if response:
            return response
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    return False


def get_all_users_in_db():
    """ GET ALL USERs IN DB """

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users")
        response = cursor.fetchall()
        cursor.close()
        if response:
            user_id = list()
            for user in response:
                user_id.append(user[0])
            return user_id
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    return False


def create_user(chat, bot_user_class):
    """ CHECK USER IN DB. IF NOT EXIST CREATE NEW USER """

    create_user_table()
    existing_user = check_user_in_db(chat.id)

    if not existing_user:
        try:
            table = sqlite3.connect(db_name)
            cursor = table.cursor()
            cursor.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)",
                           (bot_user_class.user_id, bot_user_class.first_name, bot_user_class.last_name,
                            bot_user_class.username, bot_user_class.balance, bot_user_class.subscription))
            table.commit()
            cursor.close()
        except sqlite3.Error as error:
            logger.error(f'ERROR | Error with database {error}')
    else:
        user = existing_user[0] if existing_user and existing_user[0] else None

        if user:
            bot_user_class.user_id = user[0]
            bot_user_class.first_name = user[1]
            bot_user_class.last_name = user[2]
            bot_user_class.username = user[3]
            bot_user_class.balance = user[4]
            bot_user_class.subscription = user[5]
    return bot_user_class


def get_info_about_user(user_id):
    """ GET INFO ABOUT USER IN DB """

    create_user_table()

    try:
        table = sqlite3.connect(db_name)
        cursor = table.cursor()
        cursor.execute(f"SELECT * FROM users WHERE user_id={user_id}")
        response = cursor.fetchall()
        cursor.close()
        if response and response[0]:
            return response[0]
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    return False
