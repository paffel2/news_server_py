from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=250, unique=True)
    parent_category = models.ForeignKey('self',on_delete=models.CASCADE,null=True, to_field='id')

    class Meta:
        ordering = ["id", "category_name"]

    def __str__(self):
        return self.category_name + " " + str(self.id) + " " + str(self.parent_category)

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
    bio = models.TextField(null=True)
    

class Token(models.Model):
    token = models.UUIDField()
    owner_id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    admin_permission = models.BooleanField(default=False)
    author_permission = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["owner_id"]
    
    def __str__(self):
        return (self.token)

class Image(models.Model):
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.image.name
    
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

'''
class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now=True)
    category = models.CharField
'''