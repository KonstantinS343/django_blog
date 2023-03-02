from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('categories/<int:cat_id>/', views.Categories.as_view(), name='categories'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('addpost/', views.AddPost.as_view(), name='add_post'),
    path('search/', views.Search.as_view(), name='search'),
    path('post/update/<slug:slug>', views.UpdatePost.as_view(), name='update_post'),
    path('post/delete/<slug:slug>', views.DeletePost.as_view(), name='delete_post'),
]
    
