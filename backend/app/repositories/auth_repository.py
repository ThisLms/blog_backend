from app.db.connection import get_connect

def get_user_info(user_id):
    try:
        conn = get_connect()
        cursor = conn.cursor()

        sql = """
            SELECT
                *
            FROM
                users
            WHERE
                login_id = %s;
        """

        cursor.execute(sql,(user_id,))

        result = cursor.fetchone()

        return result
    finally:
        conn.close()