from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView

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