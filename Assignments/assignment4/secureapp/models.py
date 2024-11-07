from django.db import models
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from encrypted_model_fields.fields import EncryptedTextField


class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    website = models.URLField(validators=[URLValidator()])
    bio = models.TextField()


class SensitiveData(models.Model):
    ssn = EncryptedTextField()
    credit_card_number = EncryptedTextField()

    def __str__(self):
        return f"Sensitive data for SSN: {self.ssn[:4]}****"  # Only partial display for security