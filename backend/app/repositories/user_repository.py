import logging

from app.db.connection import get_connect

logger = logging.getLogger(__name__)

def repository_signup(user_info,conn = None):
    owns_connection = conn is None
    cursor = None

    try:
        if owns_connection:
            conn = get_connect()

        cursor = conn.cursor()

        sql = """
            INSERT INTO users 
                (login_id
                ,hashed_password
                ,user_name
                ,email
                ,gender
                ,introduction
                ,birthday)
            VALUES
                (%s
                ,%s
                ,%s
                ,%s
                ,%s
                ,%s
                ,%s);
        """

        cursor.execute(sql,(
            user_info["login_id"]
            ,user_info["hashed_password"]
            ,user_info["user_name"]
            ,user_info["email"]
            ,user_info["gender"]
            ,user_info["introduction"]
            ,user_info["birthday"]))

        if owns_connection:
            conn.commit()

        return True
    except Exception as e:
        if owns_connection and conn is not None:
            conn.rollback()

        logger.exception(e)
        raise
    finally:
        if cursor is not None:
            cursor.close()

        if owns_connection and conn is not None:
            conn.close()