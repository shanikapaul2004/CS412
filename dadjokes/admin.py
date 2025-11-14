from django.contrib import admin
from .models import Joke, Picture

@admin.register(Joke)
class JokeAdmin(admin.ModelAdmin):
    list_display = ['text', 'contributor', 'created_at']
    list_filter = ['created_at', 'contributor']

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ['image_url', 'contributor', 'created_at']
    list_filter = ['created_at', 'contributor']