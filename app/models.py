from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from numerize import numerize
from django.utils.safestring import mark_safe
# Create your models here.

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_name = models.CharField(max_length=150)
    desription = models.CharField(max_length=200)
    image = models.FileField(upload_to="images/uploads")
    like = models.ManyToManyField(User, related_name="liked", blank=True, default=None)
    like_count = models.BigIntegerField(default=0)
    date_added = models.DateField(auto_now_add=True, blank=True)

    def admin_image(self):
        return mark_safe( '<img src="%s" style="width: 45px; height:45px;border-radius:5px;"/>' % self.image.url)
    admin_image.allow_tags =True

    def __str__(self):
        return self.desription

    def like_formatted(self):
        numerized = numerize.numerize(self.like_count,2)  # 2 here is used for notation / e.g 10k, 10M, 10B
        likes = numerized
        return  likes

    class Meta:
        db_table = "Posts"
        ordering = ["-like_count"]

    def get_comment_url(self):
        kwargs = {
            "id" :self.id
        }    
        return reverse("post-comment", kwargs=kwargs)

class Comments(models.Model):
    post = models.ForeignKey(Posts, related_name="comments", on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now=True, blank=True)

    class Meta:
        db_table = "Comments"
        ordering = ['-id']


   

