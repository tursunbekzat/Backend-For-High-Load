from django.db import models
from encrypted_model_fields.fields import EncryptedTextField
from django.contrib.auth import get_user_model

User = get_user_model()

class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  # Index user for frequent lookups
    file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Index created_at for sorting
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Completed', 'Completed'), ('Failed', 'Failed')],
        default='Pending',
        db_index=True  # Index status for status-based filtering
    )
    error_message = models.TextField(null=True, blank=True)

class ProcessedData(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="processed_data", db_index=True)
    data = EncryptedTextField()
