# Generated by Django 5.1.3 on 2024-11-07 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExampleModel',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
