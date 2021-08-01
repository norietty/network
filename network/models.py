from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    n_likes = models.IntegerField(default=0)
    def __str__(self):
        return f'Post by {self.author}'

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower_id = models.IntegerField()

class Post_likes(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.IntegerField()