from src.job_api import HeadHunterAPI, SuperJobAPI
from src.saver import JSONSaver
from src.vacancy import Vacancy, Parameters


def user_interaction():
    """
    Функция для работы с пользователем
    :return: Параметры поиска вакансий
    """
    print('Приветствую Вас, в парсере вакансий по сайтам "hh.ru" и "superjob.ru"')
    # Запрос ключевого слова поиска
    filter_word = input('Для начала напишите ключевые слова для поиска по вакансиям:\n')
    # Запрос региона поиска
    user_area = input('Введите нужный вам регион: (По умолчанию Россия)\n')
    # Выставление региона по умолчанию
    if user_area == '':
        user_area = 'Россия'
    # Запрос количества желаемых вакансий
    user_num_vacancies = input('Введите число вакансий, которое будет выведено по каждому сервису: (По умолчанию 10, НО не более 100)\n')
    # Выставление количества по умолчанию
    if user_num_vacancies == '':
        user_num_vacancies = 10
    # Создание экземпляра класса из параметров пользователя
    inquiry = Parameters(filter_word, user_area, 0, int(user_num_vacancies))
    return inquiry


# Начало программы
# Сбор параметров поиска
inquiry = user_interaction()
# Перевод параметров в словарь
params = inquiry.get_params()

# Создание экземпляра класса для работы с API сайтов с вакансиями
hh_api = HeadHunterAPI(params)
superjob_api = SuperJobAPI(params)

# Получение вакансий с разных платформ
hh_vacancies = hh_api.vacancy_filtering()
superjob_vacancies = superjob_api.vacancy_filtering()

# Обьединение списков вакансий с разных платформ
vacancies_full_list = (superjob_vacancies + hh_vacancies)

# Создание экземпляров класса для работы с вакансиями
# Пустой словарь для экземпляров класса вакансий
names_vac = []
# Иттерация по всем собранным вакансиям
for i in range(len(vacancies_full_list)):
    # Создание и добавление переменных по количество найденных вакансий
    names_vac.append(f'vacancy{i}')
    # Создание экзкмпляров класса по количеству вакансий
    names_vac[i] = Vacancy(vacancies_full_list[i])

# Сортировка всех найденных экземпляров класса по зарплате ("По договоренности" в конце)
names_vac.sort(key=lambda x: x.salary, reverse=True)

# Иттерация по 'топ - N' экземпляров класса ваканций
for i in range(int(len(names_vac) / 2)):
    # Вывод 'топ - N' вакансий в консоль
    print(f'{i + 1}: {names_vac[i]}')
    # Инициализация __dict__-функции класса вакансии в класс для сохранения в json
    json_saver = JSONSaver(names_vac[i].__dict__())

# Запуск записи массива с информацией об вакансиях в json-файл
json_saver.json_file()
# Вывод пользователя по окончанию записи вакансий в файл
print('\nДанные сохранены в "vacancies.json"')

