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


def repository_delete_refresh_token(family_id,conn = None):
    # 초기화
    owns_connection = conn is None
    cursor = None

    try:
        if owns_connection:
            conn = get_connect()

        cursor = conn.cursor()

        sql = """
            DELETE FROM
                refresh_tokens
            WHERE
                family_id = %s;
        """

        cursor.execute(sql,(family_id,))
        
        if owns_connection:
            conn.commit()
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

# refresh token
@contextmanager
def transaction():
    conn = get_connect()

    try:
        conn.begin()
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# refresh tokenの存在確認
def get_refresh_token_info(conn,token_hash):
    cursor = None

    try:
        cursor = conn.cursor()

        sql = """
            SELECT
                id,
                user_id,
                token_hash,
                family_id,
                expires_at,
                used_at,
                revoked_at
            FROM refresh_tokens
            WHERE token_hash = %s
            FOR UPDATE
        """

        cursor.execute(sql,(token_hash,))

        return cursor.fetchone()
    except Exception:
        logger.exception("refresh tokenが見つかりませんでした。")
        raise
    finally:
        if cursor is not None:
            cursor.close()

# 同じログインで発行されたrefresh tokenをすべて破棄する
def revoke_refresh_token_family(conn,family_id):
    cursor = None

    try:
        cursor = conn.cursor()

        sql = """
            UPDATE 
                refresh_tokens
            SET 
                revoked_at = UTC_TIMESTAMP(6)
            WHERE 
                family_id = %s
                AND revoked_at IS NULL
        """

        cursor.execute(sql, (family_id,))
    except Exception as e:
        logger.exception("refresh token破棄失敗")
        raise
    finally:
        if cursor is not None:
            cursor.close()

# トークンに紐づいているuser_idをもとに最新の情報を取得する
def get_user_info_for_reissue_token(conn,user_id):
    cursor = None

    try:
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
                user_id=%s;
        """

        cursor.execute(sql,(user_id,))

        return cursor.fetchone()
    except Exception as e:
        logger.exception("会員情報取得に失敗しました。")
        raise
    finally:
        if cursor is not None:
            cursor.close()

# 既存のトークンを使用済みにする
def mark_refresh_token_use(conn,id):
    cursor = None

    try:
        cursor = conn.cursor()

        sql = """
            UPDATE 
                refresh_tokens
            SET 
                used_at = UTC_TIMESTAMP(6)
            WHERE 
                id = %s
                AND used_at IS NULL
        """

        cursor.execute(sql, (id,))
    except Exception as e:
        logger.exception("refresg token使用済み設定失敗")
        raise
    finally:
        if cursor is not None:
            cursor.close()