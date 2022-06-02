import requests
import json
from datetime import datetime


class SaraWeather:
    def __init__(self):
        with open('keys.json') as json_file:
            data = json.load(json_file)
            self.__apikey = data['yandex-weather']
        self.lat = '55.75396'
        self.lon = '37.620393'
        self.name = 'Москве'
        self.condition_dict = {
            'clear': 'ясно',
            'partly-cloudy': 'малооблачно',
            'cloudy': 'облачно',
            'overcast': 'пасмурно',
            'drizzle': 'морось',
            'light-rain': 'небольшой дождь',
            'rain': 'дождь',
            'moderate-rain': 'значительный дождь',
            'heavy-rain': 'сильный дождь',
            'continuous-heavy-rain': 'долго идет сильный дождь',
            'showers': 'ливень',
            'wet-snow': 'дождь со снегом',
            'light-snow': 'небольшой снег',
            'snow': 'снег',
            'snow-showers': 'снегопад',
            'hail': 'град',
            'thunderstorm': 'гроза',
            'thunderstorm-with-rain': 'дождь с грозой',
            'thunderstorm-with-hail': 'гроза с градом',
        }
        self.periods_dict = {
            'night': 'ночь',
            'morning': 'утро',
            'day': 'день',
            'evening': 'вечер',
        }
        self.weekdays_dict = {
            0: 'понедельника',
            1: 'вторника',
            2: 'среды',
            3: 'четверга',
            4: 'пятницы',
            5: 'субботы',
            6: 'воскресенья',
        }

    def today(self):
        res = json.loads(requests.get(f'https://api.weather.yandex.ru/v2/informers?lat={self.lat}&lon={self.lon}',
                                      headers={'X-Yandex-API-Key': self.__apikey}).text)
        return f"Сегодня в {self.name} {self.condition_dict[res['fact']['condition']]}. " \
               f"{res['fact']['temp']} градусов."

    def closest(self):
        res = json.loads(requests.get(f'https://api.weather.yandex.ru/v2/informers?lat={self.lat}&lon={self.lon}',
                                      headers={'X-Yandex-API-Key': self.__apikey}).text)
        return f"Ближайший прогноз в {self.name} на {self.periods_dict[res['forecast']['parts'][1]['part_name']]} " \
               f"{self.weekdays_dict[datetime.strptime(res['forecast']['date'], '%Y-%m-%d').weekday()]}" \
               f"{self.condition_dict[res['forecast']['parts'][1]['condition']]}. " \
               f"{res['forecast']['parts'][1]['temp_avg']} градусов."
