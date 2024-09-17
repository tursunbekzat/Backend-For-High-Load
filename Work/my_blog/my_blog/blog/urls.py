from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', basic_view, name='base'),
    path('home/', home_view, name='home'),
    path('post/', post_list, name='post_list'),
    path('posts/<int:id>/', post_detail, name='post_detail'),
    path('create_post/', create_post, name='create_post'),
    path('edit_post/<int:id>/', edit_post, name='edit_post'),
    path('delete_post/<int:id>/', delete_post, name='delete_post'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
