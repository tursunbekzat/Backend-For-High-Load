from django.db import models

class KeyValue(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    version_history = models.JSONField(default=list)  # Store version history as a list
