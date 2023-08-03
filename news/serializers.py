from .models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    category_name = serializers.CharField(max_length=250)
    parent_category = models.IntegerField()

    class Meta:
        model = Category
        fields = ['id','category_name','parent_category']