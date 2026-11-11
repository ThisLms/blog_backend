import hashlib

def hash_refresh_token(refresh_token: str):
    return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()