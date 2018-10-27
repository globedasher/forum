from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'forum'
urlpatterns  = [
    path('', views.index, name = "index"),
    path('register/', views.register, name = "register"),
    path('invite/', login_required(views.invite), name = "invite"),
    path('login/', views.login_view, name = "login"),
    path('logout/', login_required(views.logout_view), name = "logout"),
    path('home/', login_required(views.home), name = "home"),
    path('users/', login_required(views.users), name = "users"),
    path('categories/<int:category_id>', views.categories, name = "categories"),
    path('categories/', login_required(views.categories), name = "categories"),
    path('post/<int:category_id>', login_required(views.post), name = "post"),
    path('post/', login_required(views.post), name = "post"),
]
