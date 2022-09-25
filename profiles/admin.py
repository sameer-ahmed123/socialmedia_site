from django.contrib import admin
from profiles.models import Profile

# Register your models here.
class Profile_list(admin.ModelAdmin):
    list_display = ["user"]

admin.site.register(Profile, Profile_list)
