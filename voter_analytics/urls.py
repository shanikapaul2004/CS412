# file: urls.py
# name: Shanika Paul
# email: shanikap@bu.edu
# date: October 31, 2025
# description: URL patterns for voter_analytics application.

from django.urls import path
from .views import VotersListView, VoterDetailView, GraphsView

urlpatterns = [
    path('', VotersListView.as_view(), name='home'),
    path('voters', VotersListView.as_view(), name='voters'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
    path('graphs', GraphsView.as_view(), name='graphs'),
]