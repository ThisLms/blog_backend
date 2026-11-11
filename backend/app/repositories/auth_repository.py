import logging
from contextlib import contextmanager

from app.db.connection import get_connect

logger = logging.getLogger(__name__)

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

def repository_insert_refresh_token(token,conn = None):
    # 초기화
    owns_connection = conn is None
    cursor = None

    try:
        if owns_connection:
            conn = get_connect()

        cursor = conn.cursor()

        sql = """
            INSERT INTO refresh_tokens (
                user_id,
                token_hash,
                family_id,
                expires_at
            )
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (
            token["user_id"],
            token["token_hash"],
            token["family_id"],
            token["expires_at"],
        ))

        if owns_connection:
            conn.commit()

        return True

    except Exception:
        if owns_connection and conn is not None:
            conn.rollback()

        logger.exception("Fail")
        raise

    finally:
        if cursor is not None:
            cursor.close()

        if owns_connection and conn is not None:
            conn.close()