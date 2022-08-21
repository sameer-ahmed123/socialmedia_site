from django.contrib import admin

from .models import Posts, Comments

# Register your models here.

class POSTS11(admin.ModelAdmin):
    list_display = ['desription']


admin.site.register(Posts, POSTS11)


class Comment(admin.ModelAdmin):
    list_display = ["comment"]

admin.site.register(Comments, Comment)