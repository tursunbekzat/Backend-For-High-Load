from django.urls import path
from .views import *


urlpatterns = [
    path('', basic_view),
    path('blogs/', blog_list, name='blog_list'),
    path('blogs/<int:id>/', blog_detail, name='blog_detail'),
]
