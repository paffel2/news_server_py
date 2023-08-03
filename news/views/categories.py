from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers import id_body, CategorySerializer, PutCategorySerializer, id_param
import json
from ..views.shared import *
from drf_yasg.utils import swagger_auto_schema

class CategoryAPIView(APIView):
    
    @swagger_auto_schema(operation_description="Get list of categories", responses={200: 'successfull', 'other':'something went wrong'})
    def get(self, _):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(operation_description="Create category", responses={200: 'successfull', 'other':'something went wrong'},request_body=PutCategorySerializer)
    def post(self,request):
        body = json.loads(request.body.decode("utf-8"))
        #uuid_token = body['token']
        #if is_admin(uuid_token):
        category = Category()
        #        body = json.loads(request.body.decode("utf-8"))
        category.category_name = body['category_name'] #Добавить проверки и исключения
        if 'parent_category' in body:
                        parent_id = int(body['parent_category'])
                        parent = Category.objects.get(id=parent_id)
                        category.parent_category = parent #Добавить проверки и исключения
            
        category.save()
        return Response(status=201)
    @swagger_auto_schema(operation_description="Update category", responses={200: 'successfull', 'other':'something went wrong'},request_body=CategorySerializer)
    def put(self,request):
        body = json.loads(request.body.decode("utf-8"))
        category_id = int(body['id'])
        category = Category.objects.get(id=category_id)
    #Добавить проверку что тело не пустое
        if 'parent_category' in body:
            parent_id = int(body['parent_category'])
            parent = Category.objects.get(id=parent_id)
            category.parent_category = parent #Добавить проверки и исключения
    
        if 'category_name' in body:
            category_name = body['category_name']
            category.category_name = category_name #Добавить проверки и исключения
        category.save()
        return Response(status=201)

    @swagger_auto_schema(operation_description="Delete category", responses={200: 'successfull', 'other':'something went wrong'},manual_parameters=[id_param('category id')])
    def delete(self,request):
        category_id = request.GET.get('id')
        category = Category.objects.get(id=category_id)
        category.delete()
        return Response(status=200)