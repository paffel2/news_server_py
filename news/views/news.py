from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters
from ..shared import *
from ..serializers import NewsSerializer, id_param, token_param
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema, no_body
import logging as log


class AuthorUsernameFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, _):
        author_name = request.GET.get("author")
        if not author_name:
            return queryset
        return queryset.filter(author__id__username=author_name)


class TitleFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, _):
        title = request.GET.get("title")
        if not title:
            return queryset
        return queryset.filter(title__contains=title)


class TextFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, _):
        text = request.GET.get("text")
        if not text:
            return queryset
        return queryset.filter(text__contains=text)


class DateFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, _):
        created_str = request.GET.get("created")
        if not created_str:
            return queryset
        created = datetime.strptime(created_str, "%Y-%m-%d").date()
        return queryset.filter(created__date=created)


class DateBeforeFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, _):
        created_lt_str = request.GET.get("created_lt")
        if not created_lt_str:
            return queryset
        created_lt = datetime.strptime(created_lt_str, "%Y-%m-%d").date()
        return queryset.filter(created__date__lt=created_lt)


class DateAfterFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, _):
        created_gt_str = request.GET.get("created_gt")
        if not created_gt_str:
            return queryset
        created_gt = datetime.strptime(created_gt_str, "%Y-%m-%d").date()
        return queryset.filter(created__date__gt=created_gt)


class TagsAllFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, _):
        tag_all_str = request.GET.get("tags_all")
        if not tag_all_str:
            return queryset
        list_of_ids = from_str_to_list_of_ints(tag_all_str)
        result = queryset
        for i in list_of_ids:
            result = result.filter(tags__id=i)
        return result


class TagsInFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, _):
        tag_in_str = request.GET.get("tags_in")
        if not tag_in_str:
            return queryset
        list_of_ids = from_str_to_list_of_ints(tag_in_str)
        return queryset.filter(tags__id__in=list_of_ids).distinct()


class NewsAPIView(generics.ListAPIView):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer
    ordering_fields = ["created", "author__id__username", "category__category_name"]
    ordering = ["created"]
    pagination_class = PaginationClass
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
        AuthorUsernameFilter,
        TitleFilter,
        TextFilter,
        DateFilter,
        DateBeforeFilter,
        DateAfterFilter,
        TagsAllFilter,
        TagsInFilter,
    ]
    filterset_fields = ["category", "tags"]
    search_fields = [
        "author__id__username",
        "category__category_name",
        "tags__tag_name",
        "text",
        "title",
    ]

    def get_queryset(self):
        return News.objects.filter(is_published=True)

    @swagger_auto_schema(
        operation_description="Publish news",
        request_body=no_body,
        manual_parameters=[id_param("id"), token_param],
    )
    def post(self, request):
        try:
            log.info("Publish news")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Getting draft id from query params")
            news_id = request.GET.get("id")
            log.debug("Checking draft")
            if is_news_owner(token_uuid, news_id):
                log.debug("Getting draft from database")
                news = News.objects.get(id=news_id)
                log.debug("Checking news status")
                if news.is_published:
                    log.error("News already published")
                    return Response("News already published", status=403)
                else:
                    log.debug("Publishing")
                    news.is_published = True
                    news.save()
                    return Response(f"news_id: {news.id}", status=201)
            else:
                log.error("Not author")
                return Response(status=404)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except News.DoesNotExist:
            log.error("News doesn't exist")
            return Response(status=404)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Get list of news",
    )
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete news",
        manual_parameters=[id_param("id"), token_param],
        responses={200: "successful", "other": "something went wrong"},
    )
    def delete(self, request):
        try:
            log.info("Deleting news")
            log.debug("Reading token from header")
            token_uuid = request.META.get("HTTP_TOKEN")
            log.debug("Getting draft id from query params")
            news_id = request.GET.get("id")
            log.debug("Checking author and news")
            if is_admin(token_uuid) or is_news_owner(token_uuid, news_id):
                log.debug("Getting news from database")
                news = News.objects.get(id=news_id)
                if news.is_published:
                    log.debug("Deleting images")
                    for image in news.images.all():
                        image.delete()
                    news.main_image.delete()
                    log.debug("Deleting news")
                    news.delete()
                    return Response(status=200)
                else:
                    log.error("Trying to delete draft")
                    return Response("It is draft", status=403)
            else:
                log.error("No access")
                return Response(status=404)
        except TokenExpired:
            log.error("Token expired")
            return Response("Token expired", status=403)
        except Token.DoesNotExist:
            log.error("Token not exist")
            return Response(status=404)
        except News.DoesNotExist:
            log.error("News doesn't exist")
            return Response(status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=500)


class FullNewsAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Get news by id",
    )
    def get(self, _, news_id):
        try:
            log.info("Getting news by id")
            log.debug("Getting news from database")
            news = News.objects.get(id=news_id)
            log.debug("Serializing")
            serializer = NewsSerializer(news)
            log.debug("Sending")
            return Response(serializer.data)
        except News.DoesNotExist:
            log.error("News doesn't exist")
            return Response(status=500)
        except Exception as e:
            log.error(f"Something went wrong {e}")
            return Response(status=500)
