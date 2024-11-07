from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'age', 'website', 'bio']

    # Additional validation for custom sanitization
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Add further validation as needed, e.g., sanitizing special characters
        if "<" in username or ">" in username:
            raise forms.ValidationError("Username cannot contain HTML characters.")
        return username

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        # Ensure bio does not contain HTML that could lead to XSS
        if "<script>" in bio:
            raise forms.ValidationError("Bio cannot contain JavaScript.")
        return bio