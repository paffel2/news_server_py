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
    id = models.AutoField(primary_key=True)

    class Meta:
        ordering = ["first_name"]
    
    def __str__(self):
        return (self.first_name + " " + self.last_name)

class Author(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    bio = models.TextField()
   

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


class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #main_image = models.ForeignKey(Image,on_delete=models.SET_NULL,null=True) #подумать, а надо ли оно вообще
    tags = models.ManyToManyField(Tag)
    images = models.ManyToManyField(Image)
    text = models.TextField()
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    is_published = models.BooleanField(default=False,null=False)

    class Meta:
        ordering = ["id","title","category","created",]

    def __str__(self):
        return self.title
    
class MainImage(models.Model):
    news_id = models.OneToOneField(News,on_delete=models.CASCADE)
    image_id = models.ForeignKey(Image,on_delete=models.CASCADE)

class NewsForm(forms.Form):
    title = forms.CharField(max_length=250)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    text = forms.CharField(max_length=20000)
    #main_image = forms.ImageField()

class Commentary(models.Model):
    news_id = models.OneToOneField(News, on_delete=models.CASCADE)
    author_id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["news_id","created"]
    
    def __str__(self):
        return self.text