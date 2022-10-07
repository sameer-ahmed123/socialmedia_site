from email.headerregistry import Group
from django.contrib import admin
from profiles.models import Profile
from django.contrib.auth.models import User

# Register your models here.
class Profile_list(admin.ModelAdmin):
    list_display = ["user"]

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    # fields = ['username']
    list_display = ["username", "email", 'last_login' ]
    inlines = [ProfileInline]
    
    
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
#admin.site.unregister(Group)
#admin.site.register(Profile, Profile_list)
