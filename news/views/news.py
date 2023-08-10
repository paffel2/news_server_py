from rest_framework.response import Response
from rest_framework.views import APIView
from ..shared import *
from django.http import FileResponse
from ..serializers import ShortNewsSerializer, NewsSerializer


class NewsAPIView(APIView):
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

    def get(self, _):  # добавить пагинацию и фильтрацию, переработать сериализатор
        try:
            news = News.objects.filter(is_published=True)
            serializer = ShortNewsSerializer(news, many=True)
            return Response(serializer.data)
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