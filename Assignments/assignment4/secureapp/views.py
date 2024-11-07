# secureapp/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import SensitiveDataSerializer, UserProfileSerializer
from .permissions import IsAdminUser, IsRegularUser
from .throttling import UserRoleThrottle
from .models import UserProfile
from .forms import UserProfileForm
from .models import SensitiveData
from .utils.logging import log_suspicious_activity


import logging


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'secureapp/register.html', {'form': form})


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        return JsonResponse({'message': 'Login successful'})
    else:
        log_suspicious_activity(f"Failed login attempt for username: {username}")
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

@login_required
def protected_view(request):
    return HttpResponse("This is the protected page!")


@method_decorator(login_required, name='dispatch')
class UserProfileListCreateView(View):
    throttle_classes = [UserRoleThrottle]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [IsAuthenticated]
    permission_classes = [IsAdminUser]

    def get(self, request):
        profiles = UserProfile.objects.all()
        profiles_data = [{'username': p.username, 'age': p.age, 'website': p.website, 'bio': p.bio} for p in profiles]
        return JsonResponse({'profiles': profiles_data})

    def post(self, request):
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Profile created successfully'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

@method_decorator(login_required, name='dispatch')
class UserProfileDetailView(View):
    throttle_classes = [UserRoleThrottle]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [IsAuthenticated]
    permission_classes = [IsRegularUser]

    def get(self, request, pk):
        try:
            profile = UserProfile.objects.get(pk=pk)
            profile_data = {
                'username': profile.username,
                'age': profile.age,
                'website': profile.website,
                'bio': profile.bio
            }
            return JsonResponse({'profile': profile_data})
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'Profile not found'}, status=404)


logger = logging.getLogger('django.security')
def get_sensitive_data(request, pk):
    if not request.user.is_superuser:
        log_suspicious_activity(f"Unauthorized access attempt by user: {request.user.username}")
        return JsonResponse({'error': 'Access denied'}, status=403)

    # Log access to sensitive data
    logger.info(f'Sensitive data access attempt for record ID: {pk} by user {request.user.username}')
    
    # Retrieve and return sensitive data
    sensitive_data = get_object_or_404(SensitiveData, pk=pk)
    response_data = {
        'ssn': sensitive_data.ssn,
        'credit_card_number': sensitive_data.credit_card_number
    }
    return JsonResponse(response_data)


# Create sensitive data
class SensitiveDataCreateView(generics.CreateAPIView):
    queryset = SensitiveData.objects.all()
    serializer_class = SensitiveDataSerializer
    permission_classes = [IsAdminUser]  # Only admins can create sensitive data

    def perform_create(self, serializer):
        instance = serializer.save()
        # Log sensitive data creation
        logger.info(f"Sensitive data created with ID: {instance.pk} by user: {self.request.user.username}")

# Retrieve and update sensitive data
class SensitiveDataRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = SensitiveData.objects.all()
    serializer_class = SensitiveDataSerializer
    permission_classes = [IsAdminUser]  # Only admins can access and update sensitive data

    def retrieve(self, request, *args, **kwargs):
        # Log sensitive data access
        instance = self.get_object()
        logger.info(f"Sensitive data accessed with ID: {instance.pk} by user: {request.user.username}")
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()
        # Log sensitive data update
        logger.info(f"Sensitive data updated with ID: {instance.pk} by user: {self.request.user.username}")