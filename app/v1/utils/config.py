import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):

    db: str = os.getenv('DB')
    db_name: str = os.getenv('DB_NAME')
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')
    db_host: str = os.getenv('DB_HOST')
    db_port: str = os.getenv('DB_PORT')
    db_url: str = f"{db}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    secret_key: str = os.getenv('SECRET_KEY')
    smtp_server: str = os.getenv('SMTP_SERVER')
    smtp_port: str = os.getenv('SMTP_PORT')
    smtp_username: str = os.getenv('SMTP_USERNAME')
    smtp_password: str = os.getenv('SMTP_PASSWORD')
    from_address: str = os.getenv('FROM_ADDRESS')
    namespace_name: str = os.getenv('NAMESPACE_NAME')
    bucket_name: str = os.getenv('BUCKET_NAME')
    bucket_endpoint: str = os.getenv('BUCKET_ENDPOINT')

settings = Settings()