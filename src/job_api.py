import json
from abc import ABC, abstractmethod
import requests
from dotenv import load_dotenv
import os

load_dotenv()


class JobAPI(ABC):
    """Абстрактный класс для работы с сайтами для поиска вакансий по API"""
    def __init__(self, params):
        """
        Инициализация параметров поиска вакансий пользователя
        :param params: параметры поиска
        """
        self.params = params
        # Создание self-переменной для хранения id города или области из функции
        self.town_id = self.get_region_id()
        # Создание self-переменной для хранения полученных данных
        self.vacancy_data = self.get_vacancies()

    @abstractmethod
    def get_vacancies(self):
        """
        Абстрактный метод, который получает информацию через API сайта
        :return: Массив с вакансиями hh.ru
        """
        pass

    @abstractmethod
    def get_region_id(self):
        """
        Абстракный метод для получения id региона поиска вакансий (у своего сайта все id разные)
        :return: id региона
        """
        pass

    @abstractmethod
    def vacancy_filtering(self):
        """
        Абстракный метод для фильтрации массива данных о вакансиях
        :return: Отфильтрованный и приведенный к общему шаблону массив с необходимой информацией об вакансиях
        """
        pass


class HeadHunterAPI(JobAPI):
    """Дочерний класс для работы с API hh.ru"""
    def get_region_id(self):
        """
        Метод для получения id региона
        :return: id региона
        """
        user_area_hh = self.params.get('area').lower()
        regions_dict = json.loads(requests.get('https://api.hh.ru/areas').content.decode())[0].get('areas')
        for region in regions_dict:
            for town in region.get('areas'):
                if user_area_hh == town.get('name').lower():
                    return town.get('id')
                elif user_area_hh == 'Россия':
                    return '1'

    def get_vacancies(self):
        """
        Метод для получения информации об вакансиях с hh.ru
        :return: Массив с вакансиями
        """
        parametrs = {'text': self.params.get('text'), 'area': self.town_id, 'page': 0,
                     'num_vacancies': self.params.get('num_vacancies')}
        try:
            data = json.loads(requests.get('https://api.hh.ru/vacancies', parametrs).content.decode())['items']
            return data
        except KeyError:
            exit('Слишком большое число вакансий!')

    def vacancy_filtering(self):
        """
        Метод для фильтрации массива данных о вакансиях с hh.ru
        :return: Отфильтрованный и приведенный к общему шаблону массив с необходимой информацией об вакансиях
        """
        filtered_vacancies = []
        for vac in self.vacancy_data:
            name_vacancy = vac.get('name')
            url_vacancy = vac.get('alternate_url')
            if vac.get('salary') is None:
                salary_vacancy = 'По договоренности'
            else:
                if vac.get("salary").get("from") is None:
                    salary_vacancy = f'от {0} до {vac.get("salary").get("to")}'
                elif vac.get("salary").get("to") is None:
                    salary_vacancy = f'от {vac.get("salary").get("from")} до {0}'
                else:
                    salary_vacancy = f'от {vac.get("salary").get("from")} до {vac.get("salary").get("to")}'
            experience_vacancy = vac.get('experience').get('name')
            requirement = f"Требования: {vac.get('snippet').get('requirement')}\n" \
                          f"Обязаности: {vac.get('snippet').get('responsibility')}"
            requirement_and_responsibility = requirement.replace('\n', '').replace('<highlighttext>', '').replace(
                '</highlighttext>', '')
            filtered_vacancy = {'name': name_vacancy,
                                'url': url_vacancy,
                                'salary': salary_vacancy,
                                'experience': experience_vacancy,
                                'requirement_and_responsibility': requirement_and_responsibility}
            filtered_vacancies.append(filtered_vacancy)
        return filtered_vacancies


class SuperJobAPI(JobAPI):
    """Класс для работы с API SuperJob"""
    def get_region_id(self):
        """
        Метод для получения id региона
        :return: id региона
        """
        user_area_sj = self.params.get('area').lower()
        regions_list = json.loads(requests.get('https://api.superjob.ru/2.0/towns/?all=1').content.decode()).get(
            'objects')
        for town in regions_list:
            if user_area_sj == town.get('title').lower():
                return town.get('id')

    def get_vacancies(self):
        """
        Метод для получения информации об вакансиях с SuperJob
        :return: Массив с вакансиями
        """
        self.params['area'] = self.town_id
        parametrs = {'town': self.params.get('area'), 'catalogues': None, 'count': self.params.get('num_vacancies'),
                     'keyword': self.params.get('text')}
        headers = {
            'X-Api-App-Id': os.getenv('SUPERJOB_SECRET_KEY')}
        data = (requests.get('https://api.superjob.ru/2.0/vacancies/', params=parametrs, headers=headers)).json()[
            'objects']
        return data

    def vacancy_filtering(self):
        """
        Метод для фильтрации массива данных о вакансиях с SuperJob
        :return: Отфильтрованный и приведенный к общему шаблону массив с необходимой информацией об вакансиях
        """
        filtered_vacancies = []
        for vac in self.vacancy_data:
            name_vacancy = vac.get('profession')
            url_vacancy = vac.get('link')
            if int(vac.get('payment_from')) == 0:
                salary_vacancy = 'По договоренности'
            else:
                salary_vacancy = f'от {vac.get("payment_from")} до {vac.get("payment_to")}'
            experience_vacancy = vac.get('experience').get('title')
            requirement = vac.get('candidat')
            if requirement is None:
                requirement_and_responsibility = 'Нет'
            else:
                requirement_and_responsibility = requirement.replace('\n', '').replace('<highlighttext>', '').replace(
                    '</highlighttext>', '')
            filtered_vacancy = {'name': name_vacancy,
                                'url': url_vacancy,
                                'salary': salary_vacancy,
                                'experience': experience_vacancy,
                                'requirement_and_responsibility': requirement_and_responsibility}
            filtered_vacancies.append(filtered_vacancy)
        return filtered_vacancies
