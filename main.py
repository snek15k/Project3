from db_creator import create_database, create_tables
from data_loader import load_data
from db_manager import DBManager


# Топовые компании (пример ID работодателей с hh.ru)
EMPLOYER_IDS = [1740, 3529, 78638, 15478, 4181, 1122462, 1455, 9498113, 3527, 4934]


def main():
    create_database()
    create_tables()
    load_data(EMPLOYER_IDS)

    manager = DBManager()

    print("\nКомпании и количество вакансий:")
    for row in manager.get_companies_and_vacancies_count():
        print(f"{row[0]}: {row[1]} вакансий")

    print("\nВсе вакансии:")
    for row in manager.get_all_vacancies():
        print(f"{row[0]} — {row[1]} | {row[2]}–{row[3]} руб. | {row[4]}")

    print(f"\nСредняя зарплата: {manager.get_avg_salary()}")

    print("\nВакансии с ЗП выше средней:")
    for row in manager.get_vacancies_with_higher_salary():
        print(f"{row[0]} | от {row[1]} руб. | {row[2]}")

    print("\nПоиск вакансий по ключевому слову 'python':")
    for row in manager.get_vacancies_with_keyword('python'):
        print(f"{row[0]} | {row[1]}")


if __name__ == "__main__":
    main()
