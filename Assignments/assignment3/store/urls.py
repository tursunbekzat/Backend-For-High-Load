from django.urls import path
from .views import *

urlpatterns = [
    path('kv/', KeyValueCreate.as_view(), name='kv-create'),
    path('kv/all/', KeyValueList.as_view(), name='kv-list'),
    path('kv/<str:key>/', KeyValueRetrieve.as_view(), name='kv-retrieve'),

    # path('read/', read_from_replica, name='read_from_replica'),
    # path('write/', write_to_primary, name='write_to_primary'),
]
