from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from app.models import Posts
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=500, blank =True, null=True)
    last_name = models.CharField(max_length = 500, blank = True, null = True)
    age = models.IntegerField(blank=True, null=True)
    bio = models.TextField()
    country = models.CharField(max_length=500, blank =True, null = True)
    address = models.CharField(max_length = 500, blank=True, null = True)
    
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)  
    is_private = models.BooleanField(default=False)
    avatar = models.ImageField(default="default.jpg", upload_to= "profile_images", blank = True , )
    favorites = models.ManyToManyField(Posts ,related_name="saved_posts")
    background_image = models.ImageField(default="default.jpg", upload_to="profile_images/background_images", blank = True )
    
    def save(self, *args, **kwargs):
        super().save()
        
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
              
    
    def following_count(self):
        following_count = self.follows.count()
        return following_count
    
    # def follower_count(self):
    #     follower_count = self.follows.followed_by.count()
    #     return follower_count
    
    def __str__(self):
        return self.user.username
    
