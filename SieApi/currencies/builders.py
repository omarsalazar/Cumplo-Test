from functools import reduce
from typing import Any, List, Dict
from .services import CurrencyService

from abc import ABC


class ConstructorReport(ABC):
    def __init__(self, currency: str, start_date: str, end_date: str) -> None:
        pass

    @property
    def report(self) -> Dict[str, Any]:
        pass

    def get_max(self) -> None:
        pass

    def get_min(self) -> None:
        pass

    def get_average(self) -> None:
        pass

    def get_currencies_data(self) -> None:
        pass

    def build_report(self) -> None:
        pass


class Report(ConstructorReport):
    data: List[Dict[str, Any]] = []
    service: CurrencyService = CurrencyService()
    currency: str
    start_date: str
    end_date: str
    currency_min: str = ""
    currency_max: str = ""
    currency_average: float = 0

    @property
    def report(self) -> Dict[str, Any]:
        return {
            "min": self.currency_min,
            "max": self.currency_max,
            "average": self.currency_average,
            "data": self.data
        }

    def __init__(self, currency: str, start_date: str, end_date: str):
        self.currency = currency
        self.start_date = start_date
        self.end_date = end_date

    def get_average(self) -> None:
        data = [currency_data['dato'] for currency_data in self.data]
        if len(data) <= 1:
            self.currency_average = float(data[0])
        else:
            self.currency_average = reduce(lambda a, b: float(a) + float(b),
                                           data) / len(data)

    def get_min(self) -> None:
        self.currency_min = min(
            [currency_data['dato'] for currency_data in self.data])

    def get_max(self) -> None:
        self.currency_max = max(
            [currency_data['dato'] for currency_data in self.data])

    def get_currencies_data(self) -> None:
        self.data = self.service.get_data_from_sie(self.currency,
                                                   self.start_date,
                                                   self.end_date)

    def build_report(self) -> None:
        self.get_currencies_data()
        self.get_max()
        self.get_min()
        self.get_average()
