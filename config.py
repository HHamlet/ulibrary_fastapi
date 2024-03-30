from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"
DATABASE_USER = "postgres"
DATABASE_PASS = "postgres"
DATABASE_NAME = "library_1"

CONNECTION_STRING = (
    f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/"
    f"{DATABASE_NAME}"
)


class AppConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SALT_KEY = os.getenv("SALT_KEY")
