from django.db import models

# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=250, unique=True)
    parent_category = models.ForeignKey('self',on_delete=models.CASCADE,null=True, to_field='id')

    class Meta:
        ordering = ["id", "category_name"]

    def __str__(self):
        return self.category_name

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=250,unique=True)

    class Meta:
        ordering = ["id", "tag_name"]
    
    def __str__(self):
        return self.tag_name





'''
class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now=True)
    category = models.CharField
'''