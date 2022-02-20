from utils_tg.db_api import create_connection


def save_admin_user(user_id: int) -> None:
    con = create_connection()
    cursor = con.cursor()
    insert_query = '''INSERT INTO users (user_id, type_user) VALUES (%s, %s)'''
    items = (user_id, 'admin')
    cursor.execute(insert_query, items)
    con.commit()
    cursor.close()
    con.close()


def get_admin_id() -> list:
    con = create_connection()
    cursor = con.cursor()
    insert_query = "SELECT user_id FROM users WHERE type_user ='admin'"
    cursor.execute(insert_query)
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    return rows
