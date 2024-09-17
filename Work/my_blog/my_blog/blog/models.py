from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True, blank=True)
    content = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Field for the comment author
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
    
    
class Comment(models.Model):
    text = models.TextField()  # Field for the comment text
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Field for the comment author
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # Field for the related post
    created_at = models.DateTimeField(default=timezone.now)  # Field for the created date

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'