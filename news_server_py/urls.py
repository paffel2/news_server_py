"""
URL configuration for news_server_py project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from news.views import users 
from news.views import categories
from news.views import tags
from news.views import authors
from news.views import images

urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/', categories.category_handle),
    path('tags/', tags.tags_handle),
    path('user/', users.user_handle),
    path('authors/', authors.author_handle),
    path('login/',users.login),
    path('images/',images.images_handler),
    path('images/<int:image_id>/',images.get_image)
]
