import psycopg2
from typing import List, Tuple
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


class DBManager:
    """
    Класс для управления подключением к базе данных PostgreSQL и выполнения запросов
    к таблицам компаний и вакансий.
    """

    def __init__(self):
        """
        Устанавливает соединение с базой данных.
        """
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Возвращает список компаний и количество вакансий у каждой.
        """
        self.cur.execute("""
            SELECT c.name, COUNT(v.id)
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.name
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, int, str]]:
        """
        Возвращает список всех вакансий с названием компании, вакансии, зарплатой и URL.
        """
        self.cur.execute("""
            SELECT c.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
        """)
        return self.cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Вычисляет и возвращает среднюю зарплату (salary_from) по всем вакансиям.
        """
        self.cur.execute("""
            SELECT AVG(salary_from) FROM vacancies WHERE salary_from IS NOT NULL
        """)
        result = self.cur.fetchone()[0]
        return result if result else 0.0

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, int, str]]:
        """
        Возвращает список вакансий с зарплатой выше средней.
        """
        avg_salary = self.get_avg_salary()
        self.cur.execute("""
            SELECT title, salary_from, url FROM vacancies
            WHERE salary_from > %s
        """, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str]]:
        """
        Возвращает список вакансий, в названии которых содержится указанное ключевое слово.
        """
        self.cur.execute("""
            SELECT title, url FROM vacancies WHERE title ILIKE %s
        """, (f'%{keyword}%',))
        return self.cur.fetchall()
