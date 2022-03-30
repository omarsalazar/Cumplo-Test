import requests
from django.conf import settings
from datetime import datetime
from typing import Any, Dict, List
from .exceptions import (
    SieApiInvalidDatesException, SieApiInvalidCurrencyException,
    SieApiBanxicoRequestException)
from . import errors


class CurrencyService():
    currencies: Dict[str, Any] = {
        "UDI": "SP68257",
        "USD": "SF43718",
        "TIIE": "SF331451,SF43783,SF43878"
    }

    @staticmethod
    def validate_date(start_date: str = None, end_date: str = None) -> bool:
        if not start_date or not end_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
            end_date = datetime.now().strftime("%Y-%m-%d")
        try:
            date_format = "%Y-%m-%d"
            datetime.strptime(start_date, date_format)
            datetime.strptime(end_date, date_format)
        except ValueError:
            return False
        return True

    def get_banxico_data(self, start_date: str = None,
                         end_date: str = None,
                         currency: str = None) -> List[Dict[str, Any]]:
        currency_value = self.currencies[currency]
        url = settings.BANXICO_URL.format(currency_value, start_date, end_date)
        response = requests.get(url=url,
                                headers={"content-type": "application/json",
                                         'Bmx-Token': settings.BANXICO_TOKEN})
        if response.status_code != 200:
            raise SieApiBanxicoRequestException(
                **errors.banxico_invalid_request)
        return response.json()['bmx']['series'][0]['datos']

    def get_data_from_sie(self, currency: str, start_date: str,
                          end_date: str) -> List[Dict[str, Any]]:
        if not self.validate_date(start_date, end_date):
            raise SieApiInvalidDatesException(**errors.invalid_date)
        if currency in self.currencies.keys():
            return self.get_banxico_data(start_date, end_date, currency)
        else:
            raise SieApiInvalidCurrencyException(**errors.invalid_currency)
