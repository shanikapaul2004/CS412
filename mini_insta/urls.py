# file: urls.py
# name: Shanika Paul
# email: shanikap@bu.edu
# date: October 19, 2025
# description: URL patterns for mini_insta application routing requests to appropriate views.

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (ProfileListView, ProfileDetailView, PostDetailView, 
                    CreatePostView, UpdateProfileView, DeletePostView, UpdatePostView,
                    ShowFollowersDetailView, ShowFollowingDetailView, PostFeedListView,
                    SearchView, CreateProfileView,
                    FollowProfileView, UnfollowProfileView, LikePostView, UnlikePostView)  ## UPDATED: Added Task 4 views

urlpatterns = [
    # Public URLs (no login required)
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='show_post'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    
    # URLs for logged-in users (no pk needed - uses logged-in user's profile)
    path('profile/', ProfileDetailView.as_view(), name='show_profile_self'),
    path('profile/create_post', CreatePostView.as_view(), name='create_post'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/feed', PostFeedListView.as_view(), name='show_feed'),
    path('profile/search', SearchView.as_view(), name='search'),
    
    # Post modification URLs (still need pk to identify which post)
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(http_method_names=['get', 'post']), name='logout'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('register/', CreateProfileView.as_view(), name='register'),
    
    # Task 4: Follow/Unfollow URLs
    path('profile/<int:pk>/follow', FollowProfileView.as_view(), name='follow'),  ## NEW
    path('profile/<int:pk>/delete_follow', UnfollowProfileView.as_view(), name='delete_follow'),  ## NEW
    
    # Task 4: Like/Unlike URLs
    path('post/<int:pk>/like', LikePostView.as_view(), name='like'),  ## NEW
    path('post/<int:pk>/delete_like', UnlikePostView.as_view(), name='delete_like'),  ## NEW
]