from django.contrib import admin
from django.urls import path, include
from django_prometheus import exports

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),
    path("metrics/", exports.ExportToDjangoView, name="metrics"),
    path('', include('django_prometheus.urls')),

]
