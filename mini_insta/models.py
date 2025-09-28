from django.db import models

# Create your models here.
class Profile(models.Model):
    '''this is for all the posts'''
    
    #defining data attributes 
    username = models.CharField(max_length=30, unique=True)  # CharField with length limit
    display_name = models.CharField(max_length=50)
    profile_image_url = models.URLField()
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.username} ({self.display_name})"

