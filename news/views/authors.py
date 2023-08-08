'''
from django.http import HttpResponse
from ..models import *
from django.core.serializers.json import Serializer
import json
from django.core.exceptions import ObjectDoesNotExist

class AuthorSerializer(Serializer):
    def get_dump_object(self, obj):
        return {"id":obj.id.id, "first_name":obj.id.first_name,"last_name":obj.id.last_name,"bio":obj.bio}

def make_author(request):
    author = Author()
    body = json.loads(request.body.decode("utf-8"))
    user_id = int(body['id'])
    if 'bio' in body:
        bio = body['bio']
        author.bio = bio
    user = User.objects.get(id=user_id)
    author.id = user
    author.save()
    return HttpResponse(status=201)

def check_author(request): #служебный энд, возможно стоит его просто убрать и переработать
    body = json.loads(request.body.decode("utf-8"))
    user_id = int(body['id'])
    try:
        _ = Author.objects.get(id=user_id)
        return HttpResponse('true')
    except ObjectDoesNotExist:
        return HttpResponse('false')

def get_all_authors():
    authors = Author.objects.select_related('id')
    data = AuthorSerializer().serialize(authors)
    return HttpResponse(data, content_type="application/json")

def delete_author(request):
    body = json.loads(request.body.decode("utf-8"))
    user_id = int(body['id'])
    author = Author.objects.get(id=user_id)
    author.delete()
    return HttpResponse(status=200)

def update_author(request):
    
    body = json.loads(request.body.decode("utf-8"))
    author_id = int(body['id'])
    author = Author.objects.get(id=author_id)
    if 'bio' in body:
            bio = body['bio']
            author.bio = bio
    author.save()
    return HttpResponse(status=200)
    
def author_handle(request):
    if request.method == 'GET':
        return get_all_authors()
        #return check_author(request)
    elif request.method == 'POST':
        return make_author(request)
    elif request.method == 'DELETE':
        return delete_author(request)
    elif request.method == 'PUT':
        return update_author(request)
'''


from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import PutAuthorSerializer,AuthorInfo,id_param
from ..views.shared import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from django.db.utils import IntegrityError 


class AuthorsAPIView(APIView):
    
    @swagger_auto_schema(operation_description="Get list of authors", responses={200: 'successfull', 'other':'something went wrong'})
    def get(self, _):
        try:
            authors = Author.objects.all()
            serializer = AuthorInfo(authors,many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f'Something went wrong {e}')
            return Response(status=500)
    
    @swagger_auto_schema(operation_description="Create author", responses={201: 'successfull', 'other':'something went wrong'},request_body=PutAuthorSerializer)
    def post(self,request):
        try:
            token_uuid = request.META.get('HTTP_TOKEN')
            if is_admin(token_uuid):
                data = JSONParser().parse(request)
                serializer_req = PutAuthorSerializer(data=data)
                serializer_req.is_valid(raise_exception=True)
                serializer_req.save()
                return Response (status=201)
            else:
                print("Not admin")
                return Response(status=404)
        except serializers.ValidationError as e:
            print(e)
            return Response(status=500)
        except IntegrityError as e:
            if 'FOREIGN KEY constraint failed' in e.args[0]:
               return Response("user not exists", status=403)
            return Response(status=404)
        except TokenExpired:
            print("Token expired") # сделать нормальные логи
            return Response(status=404)
        except Token.DoesNotExist:
            print("Token not exist") # сделать нормальные логи
            return Response(status=404)
        except Exception as e:
            print(f'Something went wrong {e}')
            return Response(status=500)
    
    @swagger_auto_schema(operation_description="Update author", responses={200: 'successfull', 'other':'something went wrong'},request_body=PutAuthorSerializer)
    def put(self,request):
        try:
            token_uuid = request.META.get('HTTP_TOKEN')
            if is_admin(token_uuid):
                data = JSONParser().parse(request)
                serializer_req = PutAuthorSerializer(data=data)
                serializer_req.is_valid(raise_exception=True)
                instance = Author.objects.get(id=data['id'])
                serializer = PutAuthorSerializer(data=data,instance=instance)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(status=201)
            else:
                print("Not admin")
                return Response(status=404)

        except serializers.ValidationError as e:
            print("ValidationError:")
            print(e) #добавить описание логам
            return Response(status=500)
        except IntegrityError as e:
            if 'FOREIGN KEY constraint failed' in e.args[0]:
               return Response("user not exists", status=403)
            return Response(status=404)
        except TokenExpired:
            print("Token expired") # сделать нормальные логи
            return Response(status=404)
        except Token.DoesNotExist:
            print("Token not exist") # сделать нормальные логи
            return Response(status=404)
        except Author.DoesNotExist:
            print("Author doesn't exist")
            return Response(status=404)
        except Exception as e:
            print(f'Something went wrong {e}')
            return Response(status=500)
    
    @swagger_auto_schema(operation_description="Delete author", responses={200: 'successfull', 'other':'something went wrong'},manual_parameters=[id_param('author id')])
    def delete(self,request):
        try:
            token_uuid = request.META.get('HTTP_TOKEN')
            if is_admin(token_uuid):
                author_id = request.GET.get('id')
                author = Author.objects.get(id=author_id)
                author.delete()
                return Response(status=200)
            else:
                print("Not admin")
                return Response(status=404)
        except TokenExpired:
            print("Token expired") # сделать нормальные логи
            return Response(status=404)
        except Token.DoesNotExist:
            print("Token not exist") # сделать нормальные логи
            return Response(status=404)
        except Author.DoesNotExist:
            print("User is not author")
            return Response(status=404)
        except Exception as e:
            print(f'Something went wrong {e}')
            return Response(status=404)