import os

DB_NAME = "hh_vacancies"
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
DB_HOST = "localhost"
DB_PORT = "5432"
