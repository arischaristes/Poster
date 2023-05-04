from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.registerPage, name = 'register'),

    path('', views.home, name = 'home'),
    
    path('profile/<str:pk>/', views.userProfile, name = 'user-profile'),
    path('post/<str:pk>/', views.post, name = 'post'),
    path('create-post/', views.createPost, name = 'create-post'),
    path('update-post/<str:pk>/', views.updatePost, name = 'update-post'),
    path('delete-post/<str:pk>/', views.deletePost, name = 'delete-post'),
    path('delete-comment/<str:pk>/', views.deleteComment, name = 'delete-comment'),

    path('update-user', views.updateUser, name = 'update-user'),

    path('categories/', views.categoriesPage, name="categories"),
    path('activity/', views.activityPage, name="activity"),
]