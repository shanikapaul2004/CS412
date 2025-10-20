# file: views.py
# name: Shanika Paul
# email: shanikap@bu.edu
# date: October 19, 2025
# description: View classes for mini_insta application including list views, detail views, create/update/delete views, and search functionality.

from django.shortcuts import render
from .models import Profile, Post, Photo, Follow, Comment, Like
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
        
        context = super().get_context_data(**kwargs)
    
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''Handle the form submission and save the Post and Photo to the database.'''
        
        #get the profile from the URL 
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        
        #attach profile to the post by foreign key 
        form.instance.profile = profile
        
        #save the post to get a pk
        post = form.save()
        
        #read the files from the request
        files = self.request.FILES.getlist('files')
        
        #create a photo object for each uploaded file
        for file in files:
            photo = Photo()
            photo.post = post
            photo.image_file = file
            photo.save()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        #go back to the profile page
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
        
        #add the post and profile to context
        post = self.get_object()
        context['post'] = post
        context['profile'] = post.profile
        
        return context
    
    def get_success_url(self):
        '''Return the URL to redirect to after successful delete.'''
        #get the post being deleted
        post = self.get_object()
        
        #redirect to the profile page of the user who made the post
        return reverse('show_profile', kwargs={'pk': post.profile.pk})

class UpdatePostView(UpdateView):
    '''A view to update a Post and save it to the database.'''
    
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'
    model = Post
    context_object_name = 'post'
    
class ShowFollowersDetailView(DetailView):
    '''View to show all followers of a profile.'''
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'


class ShowFollowingDetailView(DetailView):
    '''View to show all profiles that this profile follows.'''
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'
    
class PostFeedListView(ListView):
    '''View to show the post feed for a profile (posts from profiles they follow).'''
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        '''Get the posts for the feed - posts from profiles this profile follows.'''
        #get the profile from URL
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        
        #get the post feed for this profile
        return profile.get_post_feed()
    
    def get_context_data(self, **kwargs):
        '''Add the profile to the context.'''
        context = super().get_context_data(**kwargs)
        
        #get the profile from the URL
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        context['profile'] = profile
        
        return context
    
class SearchView(ListView):
    '''View to search for profiles and posts.'''
    model = Post
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'
    
    def dispatch(self, request, *args, **kwargs):
        '''Handle the request - check if we have a query or need to show the search form.'''
        
        #check if 'query' is in the GET parameters
        if 'query' not in request.GET or not request.GET['query']:
            # No query yet, show the search form
            profile_pk = self.kwargs['pk']
            profile = Profile.objects.get(pk=profile_pk)
            context = {'profile': profile}
            return render(request, 'mini_insta/search.html', context)
        
        #query exists, continue with normal ListView processing
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''Get posts that match the search query.'''
        query = self.request.GET.get('query', '')
        
        #filter posts where caption contains the query
        posts = Post.objects.filter(caption__icontains=query)
        return posts
    
    def get_context_data(self, **kwargs):
        '''Add profile, query, and matching profiles to context.'''
        context = super().get_context_data(**kwargs)
        
        #get the profile
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        context['profile'] = profile
        
        #get the query
        query = self.request.GET.get('query', '')
        context['query'] = query
        
        #get matching profiles (search in username, display_name, and bio_text)
        profiles = Profile.objects.filter(
            username__icontains=query
        ) | Profile.objects.filter(
            display_name__icontains=query
        ) | Profile.objects.filter(
            bio_text__icontains=query
        )
        context['profiles'] = profiles
        
        return context
