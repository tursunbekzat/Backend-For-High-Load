from rest_framework import serializers
from .models import UserProfile, SensitiveData

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class SensitiveDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensitiveData
        fields = ['id', 'ssn', 'credit_card_number']
        extra_kwargs = {
            'ssn': {'write_only': True},  # Optional: Only allow SSN to be set, not retrieved
            'credit_card_number': {'write_only': True},  # Optional: Only allow credit card to be set, not retrieved
        }