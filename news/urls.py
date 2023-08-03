from django.urls import path
from .views.categories import CategoryAPIView
from .views.tags import TagsAPIView
from .views.users import UsersAPIView, LoginAPIView, ProfileAPIView

urlpatterns = [
    path('categories/', CategoryAPIView.as_view()),
    path('tags/', TagsAPIView.as_view()),
    path('users/', UsersAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view())
]