from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from app.models import Posts
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    follows = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)  
    
    avatar = models.ImageField(default="default.jpg", upload_to= "profile_images")
    background_image = models.ImageField(default="default.jpg", upload_to="profile_images/background_images")
    bio = models.TextField()
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
    
