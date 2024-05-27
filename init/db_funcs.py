from loguru import logger
import sqlite3


db_name = 'bot_db.db'


def create_new_trainig(training, user_id):
    create_trainig_table()
    new_id = get_new_training()
    cancel_new_trainigs()

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO training VALUES(?, ?, ?, ?, ?, ?, ?)",(new_id, 'new', training.price, training.date, training.time, 0, ''))
        db.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with creating new trainig(date={date}): {error}')


def get_new_training():
    """ GET ALL TRAININGs IN DB """

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM training")
        response = cursor.fetchall()
        cursor.close()
        return len(response) + 1
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    return 1


def cancel_new_trainigs():
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


def add_user_to_training(user):
    """ ADD USER TO NEW TRAINIG """

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM training WHERE status='new'")
        training = cursor.fetchall()[0]
        print(training)
        user_count = int(training[5])
        user_list = str(training[6])

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
        print(error)
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    except Exception as ex_error:
        print(ex_error)
    return False


def get_future_training():
    """ GET FUTURE TRAINING """

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM training WHERE status='new'")
        response = cursor.fetchall()[0]
        db.commit()
        cursor.close()
        return response
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    return None


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
                response = cursor.fetchall()[0][3]
                db.commit()
                users_username.append(f"@{response}")
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    return users_username



def payment_history(user_id):
    """ GET ALL USER'S PAYMENTS IN DB """

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM payments WHERE user_id={user_id}")
        response = cursor.fetchall()
        cursor.close()
        logger.info(f"INFO | Info about user(user_id={user_id}): {response}")
        if response:
            return response
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    return False


def create_payment(payment):
    """CREATE NEW PAYMENT """

    create_payment_table()

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO payments VALUES(?, ?, ?, ?)",(payment.user_id, payment.status, payment.amount, payment.date))
        db.commit()
        cursor.close()
        logger.info('SUCCESS | NEW PAYMENTS WAS SAVED IN DB.')
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with creating new payment({payment}): {error}')


def create_user(chat, bot_user_class):
    """ CHECK USER IN DB. IF NOT EXIST CREATE NEW USER """

    create_user_table()
    existing_user = check_user_in_db(chat.id)

    if not existing_user:
        try:
            table = sqlite3.connect(db_name)
            cursor = table.cursor()
            cursor.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)",
                           (bot_user_class.user_id, bot_user_class.first_name, bot_user_class.last_name,
                            bot_user_class.username, bot_user_class.balance, bot_user_class.training_history,
                            bot_user_class.group))
            table.commit()
            cursor.close()
            logger.info('SUCCESS | NEW USER WAS SAVED IN DB.')
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
            bot_user_class.training_history = user[5]
            bot_user_class.group = user[6]
        logger.info('SUCCESS | GET INFO ABOUT USER FROM DB.')
    return bot_user_class


def check_user_in_db(user_id):
    """ CHECK USER IN DB """

    try:
        table = sqlite3.connect(db_name)
        cursor = table.cursor()
        cursor.execute(f"SELECT * FROM users WHERE user_id={user_id}")
        response = cursor.fetchall()
        cursor.close()
        logger.info(f"INFO | Info about user(user_id={user_id}):{response}")
        if response:
            return response
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    return False


def get_all_user_in_db():
    """ GET ALL USERs IN DB """

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM users")
        response = cursor.fetchall()
        cursor.close()
        logger.info(f"INFO | Info about all users:{response}")
        if response:
            user_id = list()
            for user in response:
                user_id.append(user[0])
            return user_id
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with checking user in DB: {error}')
    return False


def create_user_table():
    """ CREATE DB for BOT """

    try:
        table = sqlite3.connect(db_name)
        cursor = table.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, first_name TEXT, last_name TEXT, username TEXT, 
        balance REAL, training_history TEXT, group_name TEXT);""")
        table.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with creating user table: {error}')


def create_payment_table():
    """ CREATE DB for BOT """

    try:
        payment_table = sqlite3.connect(db_name)
        cursor = payment_table.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS payments(user_id INTEGER, status TEXT, amount REAL, date TEXT);""")
        payment_table.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with creating paymen table: {error}')


def create_trainig_table():
    """ CREATE TRAINING TABLE for BOT """

    try:
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS training(id INTEGER, status TEXT, price REAL, date TEXT, time TEXT, members_count INTEGER, members TEXT);""")
        db.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f'ERROR | Error with creating paymen table: {error}')