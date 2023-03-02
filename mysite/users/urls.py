from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *
from BLOG.views import *

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', user_logout, name='logout'),
    path('profile/<slug:slug>', user_profile, name='profile'),
    path('profile/<slug:slug>/posts', UserPosts.as_view(), name='user_posts')
]