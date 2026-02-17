import os
from cryptography.fernet import Fernet

KEY = os.getenv("ENCRYPTION_KEY")

if not KEY:
    raise ValueError("ENCRYPTION_KEY is not defined at env.")

if isinstance(KEY, str):
    KEY = KEY.encode()

f = Fernet(KEY)


def encrypt_data(data: str) -> str:
    return f.encrypt(data.encode()).decode()


def decrypt_data(token: str) -> str:
    return f.decrypt(token.encode()).decode()
