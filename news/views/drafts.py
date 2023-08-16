from rest_framework.response import Response
from rest_framework.views import APIView
from ..shared import *
from ..serializers import NewsSerializer, id_param
from rest_framework import generics
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema


class DraftsAPIView(generics.GenericAPIView):
    pagination_class = PaginationClass

    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.none()

    @swagger_auto_schema(
        operation_description="Get list of drafts",
    )
    def get(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            token = Token.objects.get(token=token_uuid)
            if is_author(token_uuid):
                author = Author.objects.get(id=token.owner_id)
                drafts = News.objects.filter(is_published=False, author=author)
                serializer = NewsSerializer(drafts, many=True)
                page = self.paginate_queryset(serializer.data)
                return Response(page, status=200)
            else:
                print("No access")
                return Response(status=404)
        except NotFound as e:
            return Response(str(e), status=404)
        except Token.DoesNotExist:
            print("Token not exist")  # сделать нормальные логи
            return Response(status=404)
        except TokenExpired:
            print("Token expired")  # сделать нормальные логи
            return Response(status=404)
        except Exception as e:
            print(f"Something went wrong {e}")
            return Response(status=500)

    @swagger_auto_schema(
        operation_description="Add draft",
        request_body=None,
        responses={201: "draft_id: integer", "other": "something went wrong"},
    )  # узнать как добавить в сваггер пример формы
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

    @swagger_auto_schema(
        operation_description="Delete draft",
        responses={200: "successful", "other": "something went wrong"},
        manual_parameters=[id_param("category id")],
    )
    def delete(self, request):
        try:
            token_uuid = request.META.get("HTTP_TOKEN")
            draft_id = request.GET.get("id")
            if is_admin(token_uuid) or is_news_owner(token_uuid, draft_id):
                draft = News.objects.get(id=draft_id)
                if not draft.is_published:
                    for image in draft.images.all():
                        image.delete()
                    draft.main_image.delete()
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

    @swagger_auto_schema(
        operation_description="Update draft",
        request_body=None,
        responses={201: "draft_id: integer", "other": "something went wrong"},
    )  # узнать как добавить в сваггер пример формы
    def put(self, request):
        token_uuid = request.META.get("HTTP_TOKEN")
        form = DraftUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            draft_id = form.cleaned_data.get("id")
            if is_news_owner(token_uuid, draft_id):
                news = News.objects.get(id=draft_id)
                news.category = form.cleaned_data.get("category")
                tags = form.cleaned_data.get("tags")
                news.title = form.cleaned_data.get("title")
                news.text = form.cleaned_data.get("text")
                for image in news.images.all():
                    image.delete()
                news.main_image.delete()
                main_image = request.FILES.get("main_image")
                images = request.FILES.getlist("images")
                print("added")
                to_db_main_image = Image()
                to_db_main_image.image.save(main_image.name, main_image)
                news.main_image = to_db_main_image
                print(news.id)
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
                print("not author")
                return Response(status=404)
        else:
            print(form.errors.as_data())
            return Response(status=404)


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
