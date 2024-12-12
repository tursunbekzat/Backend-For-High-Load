from django.shortcuts import render
from .models import Post, Comment
from django.views.decorators.cache import cache_page
from django.core.cache import cache


def posts_with_comments(request):
    posts_with_comments = Post.objects.prefetch_related('comments').all()
    context = [
        posts_with_comments,
    ]
    return render(request, 'base.html', context=posts_with_comments)


@cache_page(60)
def post_list_view(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})


def get_comment_count(post):
    cache_key = f'post_{post.id}_comment_count'
    comment_count = cache.get(cache_key)
    
    if comment_count is None:
        comment_count = post.comments.count()
        cache.set(cache_key, comment_count, timeout=60)
        
    return comment_count


def add_comment(post, content, author):
    Comment.objects.create(post=post, content=content, author=author)
    cache.delete(f'post_{post.id}_comment_count')  # Invalidate cache
