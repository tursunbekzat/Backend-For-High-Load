# Generated by Django 5.1.1 on 2024-09-16 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
