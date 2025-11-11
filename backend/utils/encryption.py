"""Fernet 암호화 유틸리티"""
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY environment variable is not set")

fernet = Fernet(ENCRYPTION_KEY.encode())


def encrypt(plain_text: str) -> str:
    """텍스트 암호화"""
    return fernet.encrypt(plain_text.encode()).decode()


def decrypt(encrypted_text: str) -> str:
    """텍스트 복호화"""
    return fernet.decrypt(encrypted_text.encode()).decode()
