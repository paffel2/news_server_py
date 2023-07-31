from django.db import models
from django.contrib.auth.models import AbstractUser
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

class User(AbstractUser):
    #is_author = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)

    class Meta:
        ordering = ["first_name"]
    
    def __str__(self):
        return (self.first_name + " " + self.last_name)

class Author(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    bio = models.TextField()
    




'''
class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now=True)
    category = models.CharField
'''