import mock
from datetime import datetime, timedelta
from django.urls import reverse
from django.test import TestCase
from .services import CurrencyService
from .exceptions import SieApiBanxicoRequestException, \
    SieApiInvalidDatesException, SieApiInvalidCurrencyException
from .errors import banxico_invalid_request
from .utils import (
    MockRequestsResponse, mocked_validate_date_true, mocked_get_banxico_data,
    mocked_validate_date_false)


class TestCurrencyService(TestCase):
    def setUp(self):
        self.service = CurrencyService()

    def test_validate_date_wrong_date_format(self):
        self.assertFalse(self.service.validate_date('a', 'b'))

    def test_validate_date_valid_date_format(self):
        self.assertTrue(self.service.validate_date("2020-01-01", "2020-01-02"))

    @mock.patch('requests.get', return_value=MockRequestsResponse('{"bmx": {"series": [{"datos": [{}]}]}}', 200))
    def test_get_banxico_data_returns_json(self, mock1):
        data = self.service.get_banxico_data("2020-01-01", "2020-01-02", "UDI")
        self.assertEqual(data, [{}])

    @mock.patch('requests.get', return_value=MockRequestsResponse('{}', 400))
    def test_get_banxico_data_returns_error(self, mock2):
        with self.assertRaises(SieApiBanxicoRequestException):
            self.service.get_banxico_data("2020-01-01", "2020-01-02", "UDI")

    @mock.patch("SieApi.currencies.services.CurrencyService.validate_date",
                side_effect=mocked_validate_date_true)
    @mock.patch("SieApi.currencies.services.CurrencyService.get_banxico_data",
                side_effect=mocked_get_banxico_data)
    def test_get_data_from_sie(self, mock1, mock2):
        data = self.service.get_data_from_sie("UDI", "2020-01-01",
                                              "2020-01-02")
        self.assertEqual(data, {})

    @mock.patch("SieApi.currencies.services.CurrencyService.validate_date",
                side_effect=mocked_validate_date_false)
    def test_get_data_from_sie_wrong_date(self, mock1):
        with self.assertRaises(SieApiInvalidDatesException):
            self.service.get_data_from_sie("UDI", "pepe", "2020-01-02")

    @mock.patch("SieApi.currencies.services.CurrencyService.validate_date",
                side_effect=mocked_validate_date_true)
    def test_get_data_from_sie_wrong_currency(self, mock1):
        with self.assertRaises(SieApiInvalidCurrencyException):
            self.service.get_data_from_sie("UDIs", "2020-01-01", "2020-01-02")


class TestCurrencyAPIView(TestCase):
    @mock.patch("SieApi.currencies.builders.Report.build_report")
    def test_get_currency_data(self, mock4000):
        start_date = datetime.now()
        end_date = datetime.now() - timedelta(days=1)
        url = reverse('udi',
                      kwargs={"start_date": start_date, "end_date": end_date})
        response = self.client.get(url)
        self.assertEqual(response.json(), {"min": "", "max": "", "average": 0, "data": []})

    @mock.patch("SieApi.currencies.services.CurrencyService.validate_date",
                side_effect=mocked_validate_date_true)
    @mock.patch('requests.get', return_value=MockRequestsResponse('{}', 400))
    def test_get_currency_data_banxico_fails(self, mock4001, mock4002):
        start_date = datetime.now()
        end_date = datetime.now() - timedelta(days=1)
        url = reverse('udi',
                      kwargs={"start_date": start_date,
                              "end_date": end_date})
        data = self.client.get(url)
        self.assertEqual(data, banxico_invalid_request)
