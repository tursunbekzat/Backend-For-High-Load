# Generated by Django 5.1.3 on 2024-11-07 05:45

import django.db.models.deletion
import encrypted_model_fields.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_examplemodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', encrypted_model_fields.fields.EncryptedCharField()),
                ('email', encrypted_model_fields.fields.EncryptedTextField()),
                ('phone_number', encrypted_model_fields.fields.EncryptedTextField()),
                ('address', encrypted_model_fields.fields.EncryptedTextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]