# file: views.py
# name: Shanika Paul
# email: shanikap@bu.edu
# date: October 19, 2025
# description: View classes for mini_insta application including list views, detail views, create/update/delete views, and search functionality.

from django.shortcuts import render
from .models import Profile, Post, Photo, Follow, Comment, Like
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm  ## UPDATED: Added CreateProfileForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin  ## NEW for Task 1
from django.contrib.auth.forms import UserCreationForm  ## NEW for Task 3
from django.contrib.auth.models import User  ## NEW for Task 3
from django.contrib.auth import login  ## NEW for Task 3
from django.shortcuts import redirect
from django.views.generic import View


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


class CreatePostView(LoginRequiredMixin, CreateView):  ## UPDATED: Added LoginRequiredMixin
    '''A view to create a new Post and save it to the database.'''
    
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    
    def get_login_url(self):  ## NEW
        '''Return the URL required for login.'''
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        '''Return the context variables for use in the template.'''
        
        context = super().get_context_data(**kwargs)
        
        # Get the profile of the logged-in user
        profile = Profile.objects.get(user=self.request.user)  ## UPDATED: Use logged-in user
        
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''Handle the form submission and save the Post and Photo to the database.'''
        
        # Get the profile of the logged-in user
        profile = Profile.objects.get(user=self.request.user)  ## UPDATED: Use logged-in user
        
        # Attach profile to the post by foreign key 
        form.instance.profile = profile
        
        # Save the post to get a pk
        post = form.save()
        
        # Read the files from the request
        files = self.request.FILES.getlist('files')
        
        # Create a photo object for each uploaded file
        for file in files:
            photo = Photo()
            photo.post = post
            photo.image_file = file
            photo.save()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
        # Go back to the logged-in user's profile page
        profile = Profile.objects.get(user=self.request.user)  ## UPDATED
        return reverse('show_profile', kwargs={'pk': profile.pk})
    

class UpdateProfileView(LoginRequiredMixin, UpdateView):  ## UPDATED: Added LoginRequiredMixin
    '''A view to update a Profile and save it to the database.'''
    
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    model = Profile
    
    def get_login_url(self):  ## NEW
        '''Return the URL required for login.'''
        return reverse('login')
    
    def get_object(self):  ## NEW: Override to get Profile from logged-in user
        '''Return the Profile object for the logged-in user.'''
        return Profile.objects.get(user=self.request.user)


class DeletePostView(LoginRequiredMixin, DeleteView):  ## UPDATED: Added LoginRequiredMixin
    '''A view to delete a Post and remove it from the database.'''
    
    template_name = 'mini_insta/delete_post_form.html'
    model = Post
    context_object_name = 'post'
    
    def get_login_url(self):  ## NEW
        '''Return the URL required for login.'''
        return reverse('login')
    
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


class UpdatePostView(LoginRequiredMixin, UpdateView):  ## UPDATED: Added LoginRequiredMixin
    '''A view to update a Post and save it to the database.'''
    
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'
    model = Post
    context_object_name = 'post'
    
    def get_login_url(self):  ## NEW
        '''Return the URL required for login.'''
        return reverse('login')


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


class PostFeedListView(LoginRequiredMixin, ListView):  ## UPDATED: Added LoginRequiredMixin
    '''View to show the post feed for a profile (posts from profiles they follow).'''
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'
    
    def get_login_url(self):  ## NEW
        '''Return the URL required for login.'''
        return reverse('login')
    
    def get_queryset(self):
        '''Get the posts for the feed - posts from profiles this profile follows.'''
        # Get the profile of the logged-in user
        profile = Profile.objects.get(user=self.request.user)  ## UPDATED: Use logged-in user
        
        # Get the post feed for this profile
        return profile.get_post_feed()
    
    def get_context_data(self, **kwargs):
        '''Add the profile to the context.'''
        context = super().get_context_data(**kwargs)
        
        # Get the profile of the logged-in user
        profile = Profile.objects.get(user=self.request.user)  ## UPDATED: Use logged-in user
        context['profile'] = profile
        
        return context


class SearchView(LoginRequiredMixin, ListView):  ## UPDATED: Added LoginRequiredMixin
    '''View to search for profiles and posts.'''
    model = Post
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'
    
    def get_login_url(self):  ## NEW
        '''Return the URL required for login.'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        '''Handle the request - check if we have a query or need to show the search form.'''
        
        # Check if 'query' is in the GET parameters
        if 'query' not in request.GET or not request.GET['query']:
            # No query yet, show the search form
            profile = Profile.objects.get(user=self.request.user)  ## UPDATED: Use logged-in user
            context = {'profile': profile}
            return render(request, 'mini_insta/search.html', context)
        
        # Query exists, continue with normal ListView processing
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''Get posts that match the search query.'''
        query = self.request.GET.get('query', '')
        
        # Filter posts where caption contains the query
        posts = Post.objects.filter(caption__icontains=query)
        return posts
    
    def get_context_data(self, **kwargs):
        '''Add profile, query, and matching profiles to context.'''
        context = super().get_context_data(**kwargs)
        
        # Get the profile of the logged-in user
        profile = Profile.objects.get(user=self.request.user)  ## UPDATED: Use logged-in user
        context['profile'] = profile
        
        # Get the query
        query = self.request.GET.get('query', '')
        context['query'] = query
        
        # Get matching profiles (search in username, display_name, and bio_text)
        profiles = Profile.objects.filter(
            username__icontains=query
        ) | Profile.objects.filter(
            display_name__icontains=query
        ) | Profile.objects.filter(
            bio_text__icontains=query
        )
        context['profiles'] = profiles
        
        return context


class CreateProfileView(CreateView):  ## NEW for Task 3
    '''A view to create a new Profile and User account together.'''
    
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'
    model = Profile
    
    def get_context_data(self, **kwargs):
        '''Add the UserCreationForm to the context data.'''
        
        context = super().get_context_data(**kwargs)
        
        # Create an instance of UserCreationForm and add it to context
        # This form will be displayed alongside the CreateProfileForm
        user_form = UserCreationForm()
        context['user_form'] = user_form
        
        return context
    
    def form_valid(self, form):
        '''
        Handle the form submission for both User and Profile creation.
        This method processes BOTH forms at once.
        '''
        
        # Reconstruct the UserCreationForm from the POST data
        user_form = UserCreationForm(self.request.POST)
        
        # Validate the user form
        if user_form.is_valid():
            # Save the User object (creates the Django User)
            user = user_form.save()
            
            # Log the user in automatically after registration
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Attach the User to the Profile instance
            form.instance.user = user
            
            # Let the superclass save the Profile
            return super().form_valid(form)
        else:
            # If user form is invalid, show errors
            return self.form_invalid(form)
    
    def get_success_url(self):
        '''Redirect to the user's new profile page after successful creation.'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
    
class FollowProfileView(LoginRequiredMixin, View):
    '''View to follow another profile.'''
    
    def get_login_url(self):
        '''Return the URL required for login.'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        '''Handle the follow action.'''
        
        # Get the profile to follow (from URL pk parameter)
        profile_to_follow = Profile.objects.get(pk=self.kwargs['pk'])
        
        # Get the logged-in user's profile
        follower_profile = Profile.objects.get(user=self.request.user)
        
        # Check if not already following (prevent duplicates)
        if not Follow.objects.filter(profile=profile_to_follow, follower_profile=follower_profile).exists():
            # Create the Follow relationship
            follow = Follow()
            follow.profile = profile_to_follow
            follow.follower_profile = follower_profile
            follow.save()
        
        # Redirect back to the profile page
        return redirect('show_profile', pk=profile_to_follow.pk)


class UnfollowProfileView(LoginRequiredMixin, View):
    '''View to unfollow a profile.'''
    
    def get_login_url(self):
        '''Return the URL required for login.'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        '''Handle the unfollow action.'''
        
        # Get the profile to unfollow (from URL pk parameter)
        profile_to_unfollow = Profile.objects.get(pk=self.kwargs['pk'])
        
        # Get the logged-in user's profile
        follower_profile = Profile.objects.get(user=self.request.user)
        
        # Find and delete the Follow relationship
        Follow.objects.filter(
            profile=profile_to_unfollow,
            follower_profile=follower_profile
        ).delete()
        
        # Redirect back to the profile page
        return redirect('show_profile', pk=profile_to_unfollow.pk)


# ============================================
# LIKE / UNLIKE VIEWS
# ============================================

class LikePostView(LoginRequiredMixin, View):
    '''View to like a post.'''
    
    def get_login_url(self):
        '''Return the URL required for login.'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        '''Handle the like action.'''
        
        # Get the post to like (from URL pk parameter)
        post = Post.objects.get(pk=self.kwargs['pk'])
        
        # Get the logged-in user's profile
        profile = Profile.objects.get(user=self.request.user)
        
        # Check if not already liked (prevent duplicates)
        if not Like.objects.filter(post=post, profile=profile).exists():
            # Create the Like
            like = Like()
            like.post = post
            like.profile = profile
            like.save()
        
        # Redirect back to the post page
        return redirect('show_post', pk=post.pk)


class UnlikePostView(LoginRequiredMixin, View):
    '''View to unlike a post.'''
    
    def get_login_url(self):
        '''Return the URL required for login.'''
        return reverse('login')
    
    def dispatch(self, request, *args, **kwargs):
        '''Handle the unlike action.'''
        
        # Get the post to unlike (from URL pk parameter)
        post = Post.objects.get(pk=self.kwargs['pk'])
        
        # Get the logged-in user's profile
        profile = Profile.objects.get(user=self.request.user)
        
        # Find and delete the Like
        Like.objects.filter(post=post, profile=profile).delete()
        
        # Redirect back to the post page
        return redirect('show_post', pk=post.pk)