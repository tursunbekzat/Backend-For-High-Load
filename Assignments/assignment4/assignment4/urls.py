from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from tasks.views import home
from secureapp.views import protected_view

urlpatterns = [
    path('', home, name='home'),

    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('secureapp/', include('secureapp.urls')),

    # JWT token endpoints for API auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Protected page URL (ensure this route is working correctly)
    path('protected/', protected_view, name='protected'),
]
