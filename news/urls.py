from django.urls import path
from .views.categories import CategoryViewSet
from .views.tags import TagsViewSet
from .views.users import UsersAPIView, LoginAPIView, ProfileAPIView
from .views.authors import AuthorsAPIView
from .views.images import GetImageAPIView
from .views.news import NewsAPIView, FullNewsAPIView
from .views.drafts import DraftsAPIView, FullDraftAPIView
from .views.commentaries import CommentsAPIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"tags", TagsViewSet, "tags")
router.register(r"categories", CategoryViewSet, "categories")


urlpatterns = [
    path("users/", UsersAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("profile/", ProfileAPIView.as_view()),
    path("authors/", AuthorsAPIView.as_view()),
    path("images/<int:image_id>/", GetImageAPIView.as_view(), name="image"),
    path("news/", NewsAPIView.as_view()),
    path("news/<int:news_id>/", FullNewsAPIView.as_view()),
    path("drafts/", DraftsAPIView.as_view()),
    path("drafts/<int:draft_id>/", FullDraftAPIView.as_view()),
    path("news/<int:news_id>/commentaries/", CommentsAPIView.as_view()),
] + router.urls
