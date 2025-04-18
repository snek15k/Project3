import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute("""
            SELECT c.name, COUNT(v.id)
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.name
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute("""
            SELECT c.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
        """)
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute("""
            SELECT AVG(salary_from) FROM vacancies WHERE salary_from IS NOT NULL
        """)
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cur.execute("""
            SELECT title, salary_from, url FROM vacancies
            WHERE salary_from > %s
        """, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        self.cur.execute("""
            SELECT title, url FROM vacancies WHERE title ILIKE %s
        """, (f'%{keyword}%',))
        return self.cur.fetchall()
