from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from faker import Faker
from django.contrib.auth.models import User


def basic_view(request):
    # make_posts()
    return render(request, 'base.html')

def home_view(request):
    return render(request, 'home.html')

# def post_list(request):
#     posts = Post.objects.all()
#     paginator = Paginator(posts, 5)
#     page_number = request.GET.get('page')  # Получаем текущий номер страницы
#     page_obj = paginator.get_page(page_number)  # Получаем объект страницы 
#     return render(request, 'post_list.html', {'page_obj': page_obj})

def post_list(request):
    posts = Post.objects.all()  # Получаем все записи
    paginator = Paginator(posts, 5)  # Показывать 5 записей на странице

    page_number = request.GET.get('page')  # Получаем текущий номер страницы
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы

    # Определяем диапазон страниц для отображения
    page_range = paginator.page_range
    current_page = page_obj.number
    start_page = max(1, current_page - 2)
    end_page = min(paginator.num_pages, current_page + 2)

    if end_page - start_page < 4:
        if start_page == 1:
            end_page = min(5, paginator.num_pages)
        else:
            start_page = max(1, end_page - 4)

    return render(request, 'post_list.html', {
        'page_obj': page_obj,
        'page_range': page_range,
        'start_page': start_page,
        'end_page': end_page
    })

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)  
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # Set the current user as the author
            comment.post = post  # Associate the comment with the current post
            comment.save()
            return redirect('post_detail', id=id)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form':form}) 

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id) 
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, id):
    post = Post.objects.filter(id=id)
    post.delete()
    return redirect('post_list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse("Неверное имя пользователя или пароль. inside")
        else:
            return HttpResponse("Неверное имя пользователя или пароль.outside")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('base')

@login_required
def profile(request):
    return render(request, 'profile.html')
            


def make_posts():
    fake = Faker()

    # Retrieve the user instance
    try:
        user = User.objects.get(username="Bekzat")
    except User.DoesNotExist:
        print("User with username 'Bekzat' does not exist.")
        return

    for _ in range(50):
        post = Post(
            title=fake.sentence(),
            content=fake.paragraph(),
            author=user  # Assign the single user instance
        )
        post.save()
        
def leave_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentForm()