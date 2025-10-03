from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''The data of an Instagram user profile.'''
    
    # defining data attributes 
    username = models.CharField(max_length=30, unique=True)
    display_name = models.CharField(max_length=50)
    profile_image_url = models.URLField()
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.display_name})"
    
    def get_absolute_url(self):
        '''Return the URL to display this Profile.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_all_posts(self):
        '''Return all Posts for this Profile, ordered by timestamp.'''
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts


class Post(models.Model):
    '''The data of an Instagram post.'''
    
    # data attributes of a Post
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Post by {self.profile.username} at {self.timestamp}"
    
    def get_absolute_url(self):
        '''Return the URL to display this Post.'''
        return reverse('show_post', kwargs={'pk': self.pk})
    
    def get_all_photos(self):
        '''Return all Photos for this Post.'''
        photos = Photo.objects.filter(post=self)
        return photos


class Photo(models.Model):
    '''The data of a photo associated with a Post.'''
    
    # data attributes of a Photo
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    image_url = models.URLField()
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Photo for post {self.post.pk} at {self.timestamp}"