import secrets

def generate_secret_key(length=32):
    return secrets.token_hex(length // 2)

APP_SECRET_KEY = generate_secret_key()
print(APP_SECRET_KEY)
