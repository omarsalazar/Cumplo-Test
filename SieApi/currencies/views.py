from datetime import datetime
from datetime import timedelta
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from .exceptions import (
    SieApiInvalidDatesException, SieApiInvalidCurrencyException,
    SieApiBanxicoRequestException)
from .forms import CurrencyForm
from .responses import common_response
from .builders import Report


class CurrencyAPIView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, currency: str, start_date: str = None,
            end_date: str = None) -> Response:
        report = Report(currency, start_date, end_date)
        try:
            report.build_report()
            data = report.report
        except SieApiInvalidDatesException as e:
            return Response(data=e.get_data(), status=400)
        except SieApiInvalidCurrencyException as e:
            return Response(data=e.get_data(), status=400)
        except SieApiBanxicoRequestException as e:
            return Response(data=e.get_data(), status=400)
        return Response(status=200, data=data)


class TIIEAPIView(CurrencyAPIView):
    @extend_schema(
        auth=[],
        description='Obtener valor del TIIE',
        responses=common_response,
        operation_id="Currencies.tiie",
        tags=["Currencies"],
    )
    def get(self, request, start_date: str = None, end_date: str = None,
            **kwargs) -> Response:
        return super().get(request, currency="TIIE", start_date=start_date,
                           end_date=end_date)


class UDIAPIView(CurrencyAPIView):
    @extend_schema(
        auth=[],
        description='Obtener valor del UDI',
        responses=common_response,
        operation_id="Currencies.udi",
        tags=["Currencies"],
    )
    def get(self, request, start_date: str = None, end_date: str = None,
            **kwargs) -> Response:
        return super().get(request, currency="UDI", start_date=start_date,
                           end_date=end_date)


class USDAPIView(CurrencyAPIView):
    @extend_schema(
        auth=[],
        description='Obtener valor del USD',
        responses=common_response,
        operation_id="Currencies.usd",
        tags=["Currencies"],
    )
    def get(self, request, start_date: str = None, end_date: str = None,
            **kwargs) -> Response:
        return super().get(request, currency="USD", start_date=start_date,
                           end_date=end_date)


def chart(request):
    currency = "USD"
    if request.method == 'GET':
        start_date = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
    else:
        form = CurrencyForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date'].strftime("%Y-%m-%d")
            end_date = form.cleaned_data['end_date'].strftime("%Y-%m-%d")
            currency = form.cleaned_data['currency']
    report = Report(currency, start_date, end_date)
    error = None
    try:
        report.build_report()
        data = report.report
    except SieApiInvalidDatesException as e:
        error = e.get_data()
    except SieApiInvalidCurrencyException as e:
        error = e.get_data()
    except SieApiBanxicoRequestException as e:
        error = e.get_data()
    if not error is None:
        return render(request, 'chart.html',
                      context={'data': [],
                               'error': error,
                               "form": CurrencyForm(), "currency": currency,
                               "start_date": start_date,
                               "end_date": end_date})
    return render(request, 'chart.html',
                  context={'data': data,
                           "form": CurrencyForm(), "currency": currency,
                           "start_date": start_date,
                           "end_date": end_date})