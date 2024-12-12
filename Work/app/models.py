from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(null=True, blank=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  # Indexing author
    created_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='posts')
    
    class Meta:
        indexes = [
            models.Index(fields=['author']),  # Index for filtering by author
        ]
        
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['post', 'created_date']),  # Composite index
        ]
        
        
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
