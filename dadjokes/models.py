from django.db import models
from django.utils import timezone

class Joke(models.Model):
    """Model to store dad jokes."""
    text = models.TextField()
    contributor = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.text[:50]}... by {self.contributor}"

class Picture(models.Model):
    """Model to store silly pictures/GIFs."""
    image_url = models.URLField(max_length=500)
    contributor = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Picture by {self.contributor}"