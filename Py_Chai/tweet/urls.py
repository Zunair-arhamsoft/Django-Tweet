from django.urls import path
from . import views

app_name = "tweet"

urlpatterns = [
    path('', views.tweet_list , name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('edit/<int:tweet_id>/', views.tweet_edit, name='tweet_edit'),
    path('delete/<int:tweet_id>/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('<int:tweet_id>/like/', views.toggle_like, name='tweet_like'),
]
