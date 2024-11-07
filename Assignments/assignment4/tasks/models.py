from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.utils.html import escape

class Email(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)  # To track when the email was created

    def __str__(self):
        return f"Email to {self.recipient} - {self.subject}"