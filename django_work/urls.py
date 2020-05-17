"""django_work URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views    #since we are importing multiple views so in order to prevent collision we use "as" keyword.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from social import views as social_views
#the login and logout views used over here are class based views and they will handle the logic and not the templates for login and logout.
#By writting template_name = 'path' we said Django the follow the given  path for login and logout templates instead of following the default path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/final_login.html'), name='login'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/like/', social_views.like, name='profile-like'),
    path('profile/unlike/', social_views.unlike, name='profile-unlike'),
    path('edit_profile/', user_views.edit_profile, name='edit_profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('',include('social.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   
