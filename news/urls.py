from django.urls import path
from .views.categories import CategoryAPIView

urlpatterns = [
    path('categories/', CategoryAPIView.as_view()),
]