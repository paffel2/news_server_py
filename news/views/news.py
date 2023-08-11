from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters
from ..shared import *
from ..serializers import ShortNewsSerializer, NewsSerializer
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime


class NewsAPIView(generics.GenericAPIView):
    pagination_class = PaginationClass

    def post(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            news_id = request.GET.get("id")
            if is_news_owner(token_uuid, news_id):
                news = News.objects.get(id=news_id)
                if news.is_published:
                    print("News already published")
                    return Response(status=401)
                else:
                    news.is_published = True
                    news.save()
                    return Response(f"news_id: {news.id}", status=201)
            else:
                print("Not author")
                return Response(status=404)
        except TokenExpired:
            print("Token expired")  # сделать нормальные логи
            return Response(status=404)
        except Token.DoesNotExist:
            print("Token not exist")  # сделать нормальные логи
            return Response(status=404)
        except News.DoesNotExist:
            print("News doesn't exist")
            return Response(status=500)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    def get(self, _):
        try:
            news = News.objects.filter(is_published=True)
            serializer = ShortNewsSerializer(news, many=True)
            page = self.paginate_queryset(serializer.data)
            return Response(page, status=200)
        except NotFound as e:
            return Response(str(e), status=404)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    def delete(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            news_id = request.GET.get("id")
            if is_admin(token_uuid) or is_news_owner(token_uuid, news_id):
                news = News.objects.get(id=news_id)
                if news.is_published:
                    news.delete()
                    return Response(status=200)
                else:
                    print("trying to delete draft")
                    return Response("it is draft", status=400)
            else:
                print("No acess")
                return Response(status=404)
        except TokenExpired:
            print("Token expired")  # сделать нормальные логи
            return Response(status=404)
        except Token.DoesNotExist:
            print("Token not exist")  # сделать нормальные логи
            return Response(status=404)
        except News.DoesNotExist:
            print("News doesn't exist")
            return Response(status=500)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)


class FullNewsAPIView(APIView):
    def get(self, _, news_id):
        try:
            news = News.objects.get(id=news_id)
            serializer = NewsSerializer(news)
            return Response(serializer.data)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)


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
        list_of_ids = from_str_to_list_of_ints(
            tag_in_str
        )  # добавить возможную обработку ошибок
        return queryset.filter(tags__id__in=list_of_ids).distinct()


class ListOfNewsAPIView(generics.ListAPIView):
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
