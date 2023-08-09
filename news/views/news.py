from rest_framework.response import Response
from rest_framework.views import APIView
from ..views.shared import *
from django.http import FileResponse


class NewsAPIView(APIView):
    
    def post(self,request):
        token_uuid = request.META.get('HTTP_TOKEN')
        if is_author(token_uuid):
            form = NewsForm(request.POST,request.FILES)
            if form.is_valid():
                token = Token.objects.get(token=token_uuid)
                news = News()
                news.category = form.cleaned_data.get("category")
                tags = form.cleaned_data.get("tags")
                news.title = form.cleaned_data.get("title")
                news.text = form.cleaned_data.get("text")
                news.author = token.owner_id
                images = request.FILES.getlist("images")
                images_list = []
                for image in images:
                    if "image" in image.content_type:
                        to_db_image=Image()
                        to_db_image.image.save(image.name,image)
                        images_list.append(to_db_image)
                    else:
                        print("BAD IMAGE")
                        return Response(status=410)
                news.save()
                print("added")
                for tag in tags:
                    news.tags.add(tag)
                for image in images_list:
                    news.images.add(image)
                return Response(str(news.id),status=200)
            else:
                print(form.errors.as_data())
                return Response(status=404)
        else:
            print("not author")
            return Response(status=404)
    
    