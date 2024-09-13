import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
print(env_path)
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):

    db: str = os.getenv('DB')
    db_name: str = os.getenv('DB_NAME')
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')
    db_host: str = os.getenv('DB_HOST')
    db_port: str = os.getenv('DB_PORT')
    db_url: str = f"{db}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


settings = Settings()