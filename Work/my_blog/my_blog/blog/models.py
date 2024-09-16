from django.utils.text import slugify
from django.db import models


class Post(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True, blank=True)
    content = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        original_slug = self.slug
        counter = 1
        while Post.objects.filter(slug=self.slug).exists():
            self.slug = f'{original_slug}-{counter}'
            counter += 1
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title