from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Post


def basic_view(request):
    return HttpResponse("Hello, Blog!")


def blog_list(request):
    blogs = Post.objects.all()
    return render(request, 'post_list.html', {'blogs': blogs})

def blog_detail(request, id):
    blog = get_object_or_404(Post, id=id)
    return render(request, 'post_detail.html', {'blog': blog})
