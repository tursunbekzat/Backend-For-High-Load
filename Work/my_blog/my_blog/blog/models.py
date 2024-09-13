from django.db import models


class Post(models.Model):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.TimeField()
    updated_at = models.TimeField(null=True, blank=True)

