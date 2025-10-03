from django.shortcuts import render
from .models import Profile, Post, Photo
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreatePostForm
from django.urls import reverse

class ProfileListView(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''Show the details for one profile.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class PostDetailView(DetailView):
    '''Show the details for one post.'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    '''A view to create a new Post and save it to the database.'''
    
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    
    def get_context_data(self, **kwargs):
        '''Return the context variables i created for use in the template.'''
        
        # Get the superclass context
        context = super().get_context_data(**kwargs)
        
        # Find the Profile from the URL parameter
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        
        # Add the profile to context
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''Handle the form submission and save the Post and Photo to the database.'''
        
        # Get the Profile from the URL
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        
        # Attach the profile to the post (set FK)
        form.instance.profile = profile
        
        # Save the Post to get a pk
        post = form.save()
        
        # Get the image_url from the form data
        image_url = form.cleaned_data.get('image_url')
        
        # If there's an image_url, create a Photo object
        if image_url:
            photo = Photo()
            photo.post = post
            photo.image_url = image_url
            photo.save()
        
        # Delegate to superclass
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        # Redirect back to the profile page
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': pk})