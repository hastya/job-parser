class Parameters:
    """Класс для работы с параметрами поиска вакансий на сайтах"""
    def __init__(self, text='', area='Россия', page=0, num_vacancies=10):
        """
        Инициализация основных параметров поиска
        :param text: Ключевое слово для поиска вакансий
        :param area: Регион поиска (город, область, край или Россия)
        :param page: Количество страниц со списками вакансий - не изменяется
        :param num_vacancies: Количество вакансий проверенных на каждом из сайтов

        """
        self.text = text
        self.area = area
        self.page = page
        self.num_vacancies = num_vacancies


    def get_params(self):
        """
        Вывод всех параметров в виде словаря
        :return: словарь с параметрами поиска
        """
        return {
            'text': self.text,
            'area': self.area,
            'page': self.page,
            'num_vacancies': self.num_vacancies
        }


class Vacancy:
    """Класс для работы с вакансиями"""
    def __init__(self, vacancy):
        """
        Инициализация каждой вакансии
        :param vacancy: список с вакансиями
        """
        self.__name = vacancy.get('name')
        self.__url = vacancy.get('url')
        self.__salary_full = vacancy.get('salary')

        if self.__salary_full == 'По договоренности':
            self.__salary_min = 0
            self.__salary_max = 0
        else:
            self.__salary_min = vacancy.get('salary').rsplit(None, 3)[1]
            self.__salary_max = vacancy.get('salary').rsplit(None, 3)[3]

        self.salary = max(int(self.__salary_min), int(self.__salary_max))
        self.__experience = vacancy.get('experience')
        self.__requirement_and_responsibility = vacancy.get('requirement_and_responsibility')


    def __str__(self):
        return f"{self.__name} " \
               f"({self.__salary_full}, " \
               f"{self.__url}, " \
               f"{self.__experience}, " \
               f"{self.__requirement_and_responsibility})"


    def __dict__(self):
        vacancy_dict = {'name': self.__name,
                        'url': self.__url,
                        'salary': self.__salary_full,
                        'experience': self.__experience,
                        'requirement_and_responsibility': self.__requirement_and_responsibility}
        return vacancy_dict


    def __add__(self, other):
        if type(other) == Vacancy:
            return self.__salary_full + other.salary

        else:
            raise TypeError


    def __sub__(self, other):
        if type(other) == Vacancy:
            return self.__salary_full - other.salary
        else:
            raise TypeError


    def __lt__(self, other):
        if type(other) == Vacancy:
            return self.__salary_full < other.salary
        else:
            raise TypeError


    def __le__(self, other):
        if type(other) == Vacancy:
            return self.__salary_full <= other.salary
        else:
            raise TypeError


    def __gt__(self, other):
        if type(other) == Vacancy:
            return self.__salary_full > other.salary
        else:
            raise TypeError


    def __ge__(self, other):
        if type(other) == Vacancy:
            return self.__salary_full >= other.salary
        else:
            raise TypeError


    def name(self):
        return self.__name


    def url(self):
        return self.__url


    def salary_full(self):
        return self.__salary_full


    def experience(self):
        return self.__experience


    def requirement_and_responsibility(self):
        return self.__requirement_and_responsibility
