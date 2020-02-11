from django.contrib import admin
from django.forms import ModelForm, PasswordInput

# Register your models here.

from senior_web.models import Image
from senior_web.models import User

class ImageAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    widgets = {
            'password': PasswordInput(),
    }

admin.site.register(Image, ImageAdmin)
admin.site.register(User, UserAdmin)