from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_name = models.CharField(max_length=150)
    desription = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/uploads")
    like = models.ManyToManyField(User, related_name="liked", blank=True, default=None)
    # like_count = models.BigIntegerField(default=0)
    date_added = models.DateField(auto_now_add=True, blank=True)

    @property
    def like_count(self):
        return self.like.count()

    def __str__(self):
        return self.desription

    class Meta:
        db_table = "Posts"
        ordering = ["date_added"]


class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now=True, blank=True)

    class Meta:
        db_table = "Comments"
        ordering = ['date_added']

