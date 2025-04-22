import requests


def get_employer_data(employer_ids: list) -> list:
    data = []
    for emp_id in employer_ids:
        url = f"https://api.hh.ru/employers/{emp_id}"
        try:
            response = requests.get(url, timeout=10)  # Тайм-аут 10 секунд
            if response.ok:
                data.append(response.json())
        except requests.exceptions.Timeout:
            print(f"Request to employer {emp_id} timed out.")
        except requests.exceptions.RequestException as e:
            print(f"Request to employer {emp_id} failed: {e}")
    return data


def get_vacancies_for_employer(emp_id: int, per_page=50) -> list:
    vacancies = []
    page = 0

    while True:
        try:
            response = requests.get("https://api.hh.ru/vacancies", params={
                "employer_id": emp_id,
                "per_page": per_page,
                "page": page
            }, timeout=10)  # Тайм-аут 10 секунд

            if not response.ok:
                break

            result = response.json()
            vacancies.extend(result["items"])

            if page >= result["pages"] - 1:
                break
            page += 1

        except requests.exceptions.Timeout:
            print(f"Request to get vacancies for employer {emp_id} timed out.")
            break
        except requests.exceptions.RequestException as e:
            print(f"Request to get vacancies for employer {emp_id} failed: {e}")
            break

    return vacancies
