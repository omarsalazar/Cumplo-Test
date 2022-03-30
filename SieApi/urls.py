from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from SieApi.currencies import urls as CurrenciesUrls
from SieApi.currencies.views import chart
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView


urlpatterns = [
    path('api/v1/', include(CurrenciesUrls)),
    path('chart', chart),
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'),
                                        permanent=False)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
