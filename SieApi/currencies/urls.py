from django.urls import path
from .views import USDAPIView, TIIEAPIView, UDIAPIView, CurrencyAPIView

urlpatterns = [
    path('udi/<str:start_date>/<str:end_date>',
         UDIAPIView.as_view(), name='udi'),
    path('usd/<str:start_date>/<str:end_date>',
         USDAPIView.as_view(), name='usd'),
    path('tiie/<str:start_date>/<str:end_date>',
         TIIEAPIView.as_view(), name='tiie'),
]
