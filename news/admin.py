from django.contrib import admin
from .models import User
import django.contrib.auth.admin as adm

# Register your models here.


class UserAdmin(adm.UserAdmin):
    pass


admin.site.register(User, UserAdmin)
