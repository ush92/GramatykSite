from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'', include('gramatyk.urls', namespace="gramatyk")),
    url(r'^gramatyk/', include('gramatyk.urls', namespace="gramatyk")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
]

admin.site.site_header = 'Gramatyk-> administracja'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
