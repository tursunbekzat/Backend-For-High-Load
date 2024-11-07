from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView

from two_factor.urls import urlpatterns as tf_urls

from . import views
from .views import UserProfileListCreateView, UserProfileDetailView, SensitiveDataCreateView, SensitiveDataRetrieveUpdateView

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='two_factor/login.html'), name='login'),
    # path('login/', views.login_view, name='login'),
    
    path('profiles/', UserProfileListCreateView.as_view(), name='profile-list-create'),
    path('profiles/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),

    path('sensitive-data/', SensitiveDataCreateView.as_view(), name='sensitive-data-create'),
    path('sensitive-data/<int:pk>/', SensitiveDataRetrieveUpdateView.as_view(), name='sensitive-data-detail'),

    path('two-factor/', include(tf_urls)),
]
