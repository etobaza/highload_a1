from django.urls import path
from .views import hello_blog, list_posts, list_post_by_id, create_post, edit_post, delete_post, register, \
    create_comment
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', hello_blog),
    path('posts/', list_posts, name='list_posts'),
    path('posts/<int:post_id>/', list_post_by_id, name='list_post_by_id'),
    path('posts/new/', create_post, name='create_post'),
    path('posts/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('register/', register, name='register'),
    path('posts/<int:post_id>/comment/', create_comment, name='create_comment'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]