# Generated by Django 5.1.3 on 2024-11-06 12:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(120)])),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField(validators=[django.core.validators.URLValidator()])),
                ('bio', models.TextField()),
            ],
        ),
    ]
