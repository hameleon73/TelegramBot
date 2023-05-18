import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException('Валюты должны отличаться!')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Некорректное название валюты: {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Некорректное название валюты: {base}')

        try:
            amount == float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество: {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/83e4e3e09416ec8a28b03690/pair/{quote_ticker}/{base_ticker}')

        total_base = json.loads(r.content)['conversion_rate']

        return total_base