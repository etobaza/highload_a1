from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from blog.forms import PostForm, UserRegisterForm, CommentForm
from blog.models import Post


# Create your views here.
def hello_blog(request):
    return HttpResponse('Hello, Blog!')

def list_posts(request):
    post_list = Post.objects.all().order_by('-created_at')  # Order by latest posts
    paginator = Paginator(post_list, 5)  # Show 5 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list_posts.html', {'page_obj': page_obj})

def list_post_by_id(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm()
    return render(request, 'list_post_by_id.html', {'post': post, 'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('list_posts')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('list_posts')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('list_post_by_id', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return redirect('list_posts')

    if request.method == 'POST':
        post.delete()
        return redirect('list_posts')

    return render(request, 'delete_post.html', {'post': post})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('list_posts')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('list_post_by_id', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'list_post_by_id.html', {'form': form, 'post': post})