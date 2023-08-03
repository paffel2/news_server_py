from django.urls import path
from .views.categories import CategoryAPIView
from .views.tags import TagsAPIView

urlpatterns = [
    path('categories/', CategoryAPIView.as_view()),
    path('tags/', TagsAPIView.as_view()),
]