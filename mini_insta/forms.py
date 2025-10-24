# file: forms.py
# name: Shanika Paul
# email: shanikap@bu.edu
# date: October 19, 2025
# description: Form classes for mini_insta application for creating and updating posts and profiles.

from django import forms
from .models import Post, Photo, Profile

class CreatePostForm(forms.ModelForm):
    '''A form to add a Post to the database.'''
    
    class Meta:
        '''Associate this form with the Post model; select fields.'''
        model = Post
        fields = ['caption']  # Only caption - profile will be set in the view

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a Profile in the database.'''
    
    class Meta:
        '''Associate this form with the Profile model; select fields.'''
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']  # NOT username or join_date
        

class UpdatePostForm(forms.ModelForm):
    '''A form to update a Post in the database.'''
    
    class Meta:
        '''Associate this form with the Post model; select fields.'''
        model = Post
        fields = ['caption']  # Only allow updating the caption


class CreateProfileForm(forms.ModelForm):  ## NEW for Task 3
    '''A form to create a new Profile (along with User registration).'''
    
    class Meta:
        '''Associate this form with the Profile model; select fields.'''
        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']
        # Note: user field is NOT included - it will be set programmatically in the view