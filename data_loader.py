import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
from hh_api import get_employer_data, get_vacancies_for_employer


def load_data(employer_ids: list):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cur = conn.cursor()

    companies = get_employer_data(employer_ids)

    for company in companies:
        cur.execute("""
            INSERT INTO companies (name, hh_id) VALUES (%s, %s) RETURNING id
        """, (company["name"], int(company["id"])))
        company_db_id = cur.fetchone()[0]

        vacancies = get_vacancies_for_employer(company["id"])
        for vacancy in vacancies:
            salary = vacancy.get("salary", {})
            if salary is None:
                salary = {}

            cur.execute("""
                INSERT INTO vacancies (company_id, title, salary_from, salary_to, url)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                company_db_id,
                vacancy["name"],
                salary.get("from"),
                salary.get("to"),
                vacancy["alternate_url"]
            ))

    conn.commit()
    conn.close()
