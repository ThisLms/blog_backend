import bcrypt

# パスワードハッシュに関する関数
def hash_password(password: str) -> str:
    hash_password: bytes = bcrypt.hashpw(
        password.encode("UTF-8"),
        bcrypt.gensalt()
    )

    return hash_password.decode("UTF-8")

# パスワードを検証する関数
# hashed_password -> データベースから取得したハッシュ化済みのパスワード
# password -> ユーザーから入力してもらったパスワード
def verify_password(hashed_password: str, password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("UTF-8"),
        hashed_password.encode("UTF-8")
    )