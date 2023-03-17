import json
import requests
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(amount: str, quote: str, base: str):
        if quote == base:
            raise APIException('Вы ввели одинаковые валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"')

        r = requests.get(
            f'https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key=f8acf2fbb0c47cee1aca60ee93d34199')
        total_base = json.loads(r.content)['data'][keys[quote] + keys[base]]
        total_base = round(float(total_base) * amount, 3)
        return total_base
