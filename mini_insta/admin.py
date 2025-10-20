# file: admin.py
# name: Shanika Paul
# email: shanikap@bu.edu
# date: October 19, 2025
# description: Admin configuration for mini_insta application models.

from django.contrib import admin
from .models import Profile, Post, Photo, Follow, Comment, Like

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)