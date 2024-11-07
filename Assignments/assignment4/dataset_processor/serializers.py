from rest_framework import serializers
from .models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['file']

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        # Implement malware scanning here (e.g., call an external API)
        return value

class DatasetStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['status', 'error_message']