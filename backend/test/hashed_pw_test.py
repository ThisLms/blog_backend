from app.core.hashed_pw_verify import hash_password

test_pw = "admin_test_123"

print(test_pw)
print(hash_password(test_pw))