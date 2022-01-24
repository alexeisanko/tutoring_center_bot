import psycopg2
from psycopg2 import OperationalError


def create_connection():
    try:
        con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="alexei",
            host="localhost",
            port="5432"
        )
        return con
    except OperationalError as err:
        print(f'Ошибка: "{err}"')


def create_admin_table():
    con = create_connection()
    try:
        cursor = con.cursor()
        cursor.execute('''
        CREATE TABLE admin_user 
        (id SERIAL,
        user_id INT NOT NULL);''')
        con.commit()
        cursor.close()
    except OperationalError as err:
        print('Ошибка при подключении', err)
    finally:
        if con:
            con.close()


def create_messages_table():
    con = create_connection()
    try:
        cursor = con.cursor()
        cursor.execute('''
        CREATE TABLE messages 
        (id SERIAL,
        text TEXT NOT NULL,
        periodicity VARCHAR(15) NOT NULL,
        near_data_publ VARCHAR(10) NOT NULL,
        time_publ VARCHAR (5) NOT NULL,
        type_chat VARCHAR (20) NOT NULL);''')
        con.commit()
        cursor.close()
    except OperationalError as err:
        print('Ошибка при подключении', err)
    finally:
        if con:
            con.close()

if __name__ == '__main__':
    create_admin_table()
    create_messages_table()
