import os
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_DIR = Path(__file__).resolve().parent.parent
    from dotenv import load_dotenv
    DEBUG = True if os.getenv('DEBUG', 'False') == 'True' else False
    if DEBUG:
        load_dotenv(BASE_DIR / '.envs/.local')
    else:
        load_dotenv(BASE_DIR / '.envs/.prod')

    SERVER_HOST = os.getenv('SERVER_HOST', '127.0.0.1')
    SERVER_PORT = int(os.getenv('SERVER_PORT', 8080))

    BROKER_URL = os.getenv('BROKER_URL')
    BROKER_HOST = os.getenv('BROKER_HOST')

    DB_SCHEME = os.getenv('DB_SCHEME')
    DB_HOST = os.getenv('POSTGRES_HOST')
    DB_PORT = os.getenv('POSTGRES_PORT')
    DB_USER = os.getenv('POSTGRES_USER')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    DB_NAME = os.getenv('POSTGRES_DB')
    DATABASE_URL: str = os.getenv(
        'DATABASE_URL', f'{DB_SCHEME}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

settings = Settings()
