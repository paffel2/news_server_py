from django.urls import path
from .views.categories import CategoryAPIView,FullCategoryInfoAPIView
from .views.tags import TagsAPIView
from .views.users import UsersAPIView, LoginAPIView, ProfileAPIView
from .views.authors import AuthorsAPIView
from .views.images import ImagesAPIView,GetImageAPIView
from .views.news import NewsAPIView
from .views.drafts import DraftsAPIView

urlpatterns = [
    path('categories/', CategoryAPIView.as_view()),
    path('categories/<int:category_id>/', FullCategoryInfoAPIView.as_view()),
    path('tags/', TagsAPIView.as_view()),
    path('users/', UsersAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('authors/',AuthorsAPIView.as_view()),
    path('images/',ImagesAPIView.as_view()),
    path('images/<int:image_id>/',GetImageAPIView.as_view()),
    path('news/',NewsAPIView.as_view()),
    path('drafts/',DraftsAPIView.as_view())
]