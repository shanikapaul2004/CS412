# file: models.py
# name: Shanika Paul
# email: shanikap@bu.edu
# date: October 19, 2025
# description: Data models for mini_insta application including Profile, Post, Photo, Follow, Comment, and Like.


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
    
    def get_followers(self):
        '''Return a list of Profiles who follow this profile.'''
        follows = Follow.objects.filter(profile=self)
        #return list of the follower profiles 
        return [follow.follower_profile for follow in follows]
    
    def get_num_followers(self):
        '''Return the count of followers for this profile.'''
        return len(self.get_followers())
    
    def get_following(self):
        '''Return a list of Profiles that this profile follows.'''
        follows = Follow.objects.filter(follower_profile=self)
        # return list of following profiles 
        return [follow.profile for follow in follows]
    
    def get_num_following(self):
        '''Return the count of profiles this profile is following.'''
        return len(self.get_following())
    
    def get_post_feed(self):
        '''Return a QuerySet of Posts from profiles this profile follows, ordered by most recent.'''
        following = self.get_following()
        
        # order from most recent and get all posts from those profiles
        posts = Post.objects.filter(profile__in=following).order_by('-timestamp')
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
    
    def get_all_comments(self):
        '''Return all Comments for this Post, ordered by timestamp.'''
        comments = Comment.objects.filter(post=self).order_by('-timestamp')
        return comments
    
    def get_likes(self):
        '''Return all Likes for this Post.'''
        likes = Like.objects.filter(post=self)
        return likes


class Photo(models.Model):
    '''The data of a photo associated with a Post.'''
    
    # data attributes of a Photo
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)  # Keep for backwards compatibility
    image_file = models.ImageField(blank=True)  # Actual image file
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Photo.'''
        if self.image_file:
            return f"Photo (file) for post {self.post.pk}"
        else:
            return f"Photo (URL) for post {self.post.pk}"
    
    def get_image_url(self):
        '''Return the URL to the image, either from image_url or image_file.'''
        if self.image_file:
            return self.image_file.url
        else:
            return self.image_url


class Follow(models.Model):
    '''The data representing one profile following another.'''
    
    # Data attributes
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="followed")
    follower_profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="followers")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        '''Return a string representation of this Follow relationship.'''
        return f"{self.follower_profile.username} follows {self.profile.username}"


class Comment(models.Model):
    '''The data representing a comment on a post.'''
    
    # Data attributes
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        '''Return a string representation of this Comment.'''
        return f"Comment by {self.profile.username} on post {self.post.pk}"


class Like(models.Model):
    '''The data representing a like on a post.'''
    
    # Data attributes
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        '''Return a string representation of this Like.'''
        return f"{self.profile.username} likes post {self.post.pk}"