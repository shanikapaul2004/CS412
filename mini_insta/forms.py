from django import forms
from .models import Post, Photo

class CreatePostForm(forms.ModelForm):
    '''A form to add a Post to the database.'''
    
    # this is an extra field for the image url (not part of Post model)
    image_url = forms.URLField(required=False, label='Image URL')
    
    class Meta:
        '''Associate this form with the Post model; select fields.'''
        model = Post
        fields = ['caption']  # Only caption - profile will be set in the view