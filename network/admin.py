from django.contrib import admin
from .models import User, Post, Follower, Post_likes

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Post_likes)
admin.site.register(Follower)