# views.py
from django.shortcuts import render
from .models import Profile, Post, Photo
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
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
        '''Return the context variables for use in the template.'''
        
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
        
        # Read the files from the request
        files = self.request.FILES.getlist('files')
        
        # Create a Photo object for each uploaded file
        for file in files:
            photo = Photo()
            photo.post = post
            photo.image_file = file
            photo.save()
        
        # Delegate to superclass
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        # Redirect back to the profile page
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': pk})
    

class UpdateProfileView(UpdateView):
    '''A view to update a Profile and save it to the database.'''
    
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    model = Profile
    
class DeletePostView(DeleteView):
    '''A view to delete a Post and remove it from the database.'''
    
    template_name = 'mini_insta/delete_post_form.html'
    model = Post
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        '''Provide context data for the template.'''
        context = super().get_context_data(**kwargs)
        
        # Add the post and profile to context
        post = self.get_object()
        context['post'] = post
        context['profile'] = post.profile
        
        return context
    
    def get_success_url(self):
        '''Return the URL to redirect to after successful delete.'''
        # Get the post being deleted
        post = self.get_object()
        
        # Redirect to the profile page of the user who made the post
        return reverse('show_profile', kwargs={'pk': post.profile.pk})

class UpdatePostView(UpdateView):
    '''A view to update a Post and save it to the database.'''
    
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'
    model = Post
    context_object_name = 'post'
