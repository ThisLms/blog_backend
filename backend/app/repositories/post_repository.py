import logging
from contextlib import contextmanager

from app.db.connection import get_connect

logger = logging.getLogger(__name__)

# 트렌젝션 관리
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

# 게시글 등록 트렌젝션 #########

# 1. 댓글 저장
def save_post(conn,data,user_id):
    cursor = None

    try:
        cursor = conn.cursor()

        sql = """
            INSERT INTO post
                (
                user_id,
                title,
                content
                )
            VALUES
                (
                %s,
                %s,
                %s
                );
        """
        cursor.execute(sql,(
            user_id
            ,data.title
            ,data.content
        ))

        # post_id반환
        return cursor.lastrowid
    
    except Exception:
        logger.exception("投稿ができませんでした。")
        raise
    finally:
        if cursor is not None:
            cursor.close()

# 2. 태그 저장

## 2_1 태그 검색
def search_tag(conn,tag):
    cursor = None

    try:
        cursor = conn.cursor()

        sql = """
            SELECT
                tag_id,
                tag_name
            FROM
                tags
            WHERE
                tag_name = %s;
        """

        cursor.execute(sql,(tag,))

        return cursor.fetchone()
    except Exception:
        logger.exception("タグ検索ができませんでした。")
        raise
    finally:
        if cursor is not None:
            cursor.close()

## 태그가 존재하지 않는 경우에는 태그 추가
def save_tag(conn,tag):
    cursor = None

    try:
        cursor = conn.cursor()

        sql = """
            INSERT INTO tags (
                tag_name
                ) 
            VALUE 
                (
                %s
                )
            ON DUPLICATE KEY UPDATE tag_id = LAST_INSERT_ID(tag_id);
        """

        cursor.execute(sql,(tag,))

        # 등록 후 태그 아이디 반환
        return cursor.lastrowid
    except Exception:
        logger.exception("タグ登録ができませんでした。")
        raise
    finally:
        if cursor is not None:
            cursor.close()

# 게시글과 태그를 연결
def connect_post_tag(conn,post_id,tag):
    cursor = None
    
    try:
        cursor = conn.cursor()

        sql = """
            INSERT INTO post_tags 
                (
                post_id,
                tag_id
                )
            VALUES
                (
                %s,
                %s
                );
        """

        cursor.execute(sql,(
            post_id
            ,tag
        ))
    except Exception:
        logger.exception("登録ができませんでした。")
        raise
    finally:
        if cursor is not None:
            cursor.close()
#############################