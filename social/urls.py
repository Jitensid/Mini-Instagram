from django.urls import path
from . import views
from social import views as social_views

urlpatterns = [
    path('', views.home, name='social-home'),
    path('like/', views.like, name='social-like'),
    path('unlike/',views.unlike, name='social-unlike'),
    path('about/', views.about, name='social-about'),
    path('search/', views.search_users, name='search_users'),
    path('other_profile/<visited_user>/', views.other_profile, name='other_profile'),
    path('other_profile/<visited_user>/follow/', views.follow, name='follow'),
    path('other_profile/<visited_user>/unfollow/', views.unfollow, name='unfollow'),
    path('other_profile/<visited_user>/like/', views.like, name='like_other_profile'),
    path('other_profile/<visited_user>/unlike/',views.unlike, name='unlike_other_profile'),
    path('chat/',views.chat,name='chat'),
    path('create_a_post/',views.create_a_post, name='create_a_post'),
    path('<str:room_name>/',views.instagram_chatting,name='chatting'),
    ] 