from app.db.connection import get_connect

def repository_confirm_user(login_id):
    try:
        conn = get_connect()
        cursor = conn.cursor()

        sql = """
            SELECT
                u.user_id,
                u.hashed_password,
                u.user_name,
                a.authority_name
            FROM
                users as u INNER JOIN authority as a
            ON
                u.authority_id = a.authority_id
            WHERE
                login_id=%s;
        """

        cursor.execute(sql,(login_id,))

        result = cursor.fetchone()

        return result
    finally:
        conn.close()