from utils_tg.db_api import create_connection


def save_message(text, periodicity, near_data_publ, time_publ, type_chat='Преподавательский') -> None:
    con = create_connection()
    cursor = con.cursor()
    insert_query = '''INSERT INTO messages 
    (text, periodicity, near_data_publ, time_publ, type_chat) VALUES (%s, %s, %s, %s, %s)'''
    items = (text, periodicity, near_data_publ, time_publ, type_chat)
    cursor.execute(insert_query, items)
    con.commit()
    cursor.close()
    con.close()


def get_text_all_messages() -> list:
    con = create_connection()
    cursor = con.cursor()
    insert_query = '''SELECT text FROM messages'''
    cursor.execute(insert_query)
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    return rows


def get_message_by_text(text: str) -> list:
    con = create_connection()
    cursor = con.cursor()
    insert_query = '''SELECT id, text, periodicity, near_data_publ, time_publ, type_chat FROM messages 
    WHERE text=%s'''
    items = (text,)
    cursor.execute(insert_query, items)
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    return rows


def get_sent_message(near_data_publ: str, time_publ: str) -> list:
    con = create_connection()
    cursor = con.cursor()
    insert_query = '''SELECT id, text, periodicity, type_chat FROM messages 
    WHERE near_data_publ=%s AND time_publ=%s'''
    items = (near_data_publ, time_publ)
    cursor.execute(insert_query, items)
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    return rows


def change_near_date(number: str, new_near_date: str) -> None:
    con = create_connection()
    cursor = con.cursor()
    insert_query = '''UPDATE messages set near_data_publ = %s WHERE id=%s'''
    items = (new_near_date, number)
    cursor.execute(insert_query, items)
    con.commit()
    cursor.close()
    con.close()


def change_message(command: str, new_value: str, my_id: str):
    con = create_connection()
    cursor = con.cursor()
    insert_query = f'''UPDATE messages set {command} = %s WHERE id=%s'''
    items = (new_value, my_id)
    cursor.execute(insert_query, items)
    con.commit()
    cursor.close()
    con.close()


def delete_message(my_id: str):
    con = create_connection()
    cursor = con.cursor()
    insert_query = '''DELETE FROM messages WHERE id=%s'''
    items = (my_id,)
    cursor.execute(insert_query, items)
    con.commit()
    cursor.close()
    con.close()
