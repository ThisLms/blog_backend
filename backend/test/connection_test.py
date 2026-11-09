from app.db.connection import get_connect

def test_db():
    try:
        conn = get_connect()
        cursor = conn.cursor()
        sql = """
            SELECT VERSION();
        """

        cursor.execute(sql)

        result = cursor.fetchone()

        return result
    except Exception as e:
        print("Fail")
    finally:
        conn.close()

print(test_db())