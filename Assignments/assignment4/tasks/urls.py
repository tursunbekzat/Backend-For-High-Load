from django.urls import path
from . import views

urlpatterns = [
    path('send_email/', views.send_email_view, name='send_email'),
]
