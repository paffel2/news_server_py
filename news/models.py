from django.db import models, router
from django.db.models.deletion import Collector
from django.contrib.auth.models import AbstractUser
from django import forms
import os
from news_server_py.settings import MEDIA_ROOT


class Category(models.Model):
    category_name = models.CharField(max_length=250, unique=True)
    parent_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, to_field="id"
    )

    class Meta:
        ordering = ["id", "category_name"]

    def __str__(self):
        return self.category_name + " " + str(self.id) + " " + str(self.parent_category)


class Tag(models.Model):
    tag_name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ["id", "tag_name"]

    def __str__(self):
        return self.tag_name


class User(AbstractUser):
    class Meta:
        ordering = ["first_name"]

    def __str__(self):
        return self.first_name + " " + self.last_name


class Author(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField()

    class Meta:
        ordering = ["id"]


class Token(models.Model):
    token = models.UUIDField()
    owner_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    creation_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["owner_id"]

    def __str__(self):
        return self.token


class Image(models.Model):
    image = models.ImageField(upload_to="images")

    def delete(self, using=None, keep_parents=False):
        if self.pk is None:
            raise ValueError(
                "%s object can't be deleted because its %s attribute is set "
                "to None." % (self._meta.object_name, self._meta.pk.attname)
            )
        using = using or router.db_for_write(self.__class__, instance=self)
        collector = Collector(using=using, origin=self)
        collector.collect([self], keep_parents=keep_parents)
        os.remove(MEDIA_ROOT + str(self.image))
        return collector.delete()


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image"]


class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main_image = models.OneToOneField(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        related_name="main_image_article_set",
    )
    tags = models.ManyToManyField(Tag)
    images = models.ManyToManyField(Image, related_name="images_article_set")
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False, null=False)

    class Meta:
        ordering = [
            "id",
            "title",
            "category",
            "created",
        ]

    def __str__(self):
        return self.title


class NewsForm(forms.Form):
    title = forms.CharField(max_length=250)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    text = forms.CharField(max_length=20000)


class DraftUpdateForm(NewsForm):
    id = forms.IntegerField()


class Commentary(models.Model):
    news_id = models.ForeignKey(News, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["news_id", "created"]

    def __str__(self):
        return self.text
