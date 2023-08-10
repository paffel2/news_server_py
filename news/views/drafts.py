from rest_framework.response import Response
from rest_framework.views import APIView
from ..shared import *
from ..serializers import ShortNewsSerializer, NewsSerializer


class DraftsAPIView(APIView):
    def get(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            token = Token.objects.get(token=token_uuid)
            if token.author_permission and is_token_valid(token):
                author = Author.objects.get(id=token.owner_id)
                drafts = News.objects.filter(is_published=False, author=author)
                serializer = ShortNewsSerializer(drafts, many=True)
                return Response(serializer.data)
            else:
                print("No access")
                return Response(status=404)
        except Token.DoesNotExist:
            print("Token not exist")  # сделать нормальные логи
            return Response(status=404)
        except TokenExpired:
            print("Token expired")  # сделать нормальные логи
            return Response(status=404)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    def post(self, request):
        token_uuid = request.META.get("HTTP_TOKEN")
        if is_author(token_uuid):
            form = NewsForm(request.POST, request.FILES)
            if form.is_valid():
                token = Token.objects.get(token=token_uuid)
                news = News()
                news.category = form.cleaned_data.get("category")
                tags = form.cleaned_data.get("tags")
                news.title = form.cleaned_data.get("title")
                news.text = form.cleaned_data.get("text")
                news.author = Author.objects.get(id=token.owner_id)
                main_image = request.FILES.get("main_image")
                images = request.FILES.getlist("images")
                print("added")
                to_db_main_image = Image()
                to_db_main_image.image.save(main_image.name, main_image)
                news.main_image = to_db_main_image
                news.save()
                images_list = []
                for image in images:
                    if "image" in image.content_type:
                        to_db_image = Image()
                        to_db_image.image.save(image.name, image)
                        images_list.append(to_db_image)
                    else:
                        print("BAD IMAGE")
                        return Response(status=410)
                for tag in tags:
                    news.tags.add(tag)
                for image in images_list:
                    news.images.add(image)
                return Response(f"draft_id: {news.id}", status=200)
            else:
                print(form.errors.as_data())
                return Response(status=404)
        else:
            print("not author")
            return Response(status=404)

    def delete(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            draft_id = request.GET.get("id")
            if is_admin(token_uuid) or is_news_owner(token_uuid, draft_id):
                draft = News.objects.get(id=draft_id)
                if not draft.is_published:
                    draft.delete()
                    return Response(status=200)
                else:
                    print("trying to delete news")
                    return Response("it is news", status=400)
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


class FullDraftAPIView(APIView):
    def get(self, _, draft_id):
        try:
            draft = News.objects.get(id=draft_id)
            if not draft.is_published:
                serializer = NewsSerializer(draft)
                return Response(serializer.data)
            else:
                return Response(
                    "It is not draft", status=400
                )  # исправить все коды ответа
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)
