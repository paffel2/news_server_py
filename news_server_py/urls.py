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
from django.urls import path, include
from news.views import users 
from news.views import categories
from news.views import tags
from news.views import authors
from news.views import images
from drf_yasg.views import get_schema_view  # new
from drf_yasg import openapi  # new
from rest_framework import permissions
from django.views.generic import TemplateView
#from django.conf.urls import url




schema_view = get_schema_view(  # new
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    # url=f'{settings.APP_URL}/api/v3/',
    #patterns=[path('api/', include('myapi.urls')), ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/', categories.category_handle),
    path('tags/', tags.tags_handle),
    path('user/', users.user_handle),
    path('user/list/',users.users_list),
    path('authors/', authors.author_handle),
    path('login/',users.login),
    path('images/',images.images_handler),
    path('images/<int:image_id>/',images.get_image),
    path('user/check_token/',users.check_token),
    path(  # new
        'swagger_ui/',
        TemplateView.as_view(
            template_name='swaggerui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ),
        name='swagger-ui'),
]
