import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


def create_database():
    conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    cur.execute(f"CREATE DATABASE {DB_NAME}")
    conn.close()


def create_tables():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            hh_id INT UNIQUE NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE vacancies (
            id SERIAL PRIMARY KEY,
            company_id INT REFERENCES companies(id),
            title VARCHAR NOT NULL,
            salary_from INT,
            salary_to INT,
            url TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
