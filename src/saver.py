import json


class JSONSaver:
    """
    Класс для сохранения и записи списка вакансий
    """
    # Пустой список для словарей вакансий
    json_vacancy_dict = []

    def __init__(self, vacancy):
        """
        Инициализация словарей вакансий
        :param vacancy: словарь с информацией по вакансии
        """
        self.vacancy = vacancy
        # Добавление словаря в список
        self.json_vacancy_dict.append(self.vacancy)

    def json_file(self):
        """
        Функция для записи списка в json-файл
        """
        with open('vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(self.json_vacancy_dict, file, ensure_ascii=False)
