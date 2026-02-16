from cryptography.fernet import Fernet
import os

KEY = os.getenv("ENCRYPTION_KEY")

if not KEY:
    raise ValueError("ENCRYPTION_KEY não definida nas variáveis de ambiente.")

if isinstance(KEY, str):
    KEY = KEY.encode()

f = Fernet(KEY)


def encrypt_data(data: str) -> str:
    return f.encrypt(data.encode()).decode()


def decrypt_data(token: str) -> str:
    return f.decrypt(token.encode()).decode()
