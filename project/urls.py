"""
File: urls.py
Author: Shanika Paul
Description: URL routing for fashion trend analytics platform.
"""

from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Designer URLs
    path('designers/', views.DesignerListView.as_view(), name='designer_list'),
    path('designers/<int:pk>/', views.DesignerDetailView.as_view(), name='designer_detail'),
    path('designers/create/', views.DesignerCreateView.as_view(), name='designer_create'),
    path('designers/<int:pk>/update/', views.DesignerUpdateView.as_view(), name='designer_update'),
    path('designers/<int:pk>/delete/', views.DesignerDeleteView.as_view(), name='designer_delete'),
    
    # Collection URLs
    path('collections/', views.CollectionListView.as_view(), name='collection_list'),
    path('collections/<int:pk>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('collections/create/', views.CollectionCreateView.as_view(), name='collection_create'),
    path('collections/<int:pk>/update/', views.CollectionUpdateView.as_view(), name='collection_update'),
    path('collections/<int:pk>/delete/', views.CollectionDeleteView.as_view(), name='collection_delete'),
    
    # TrendItem URLs
    path('trends/', views.TrendItemListView.as_view(), name='trenditem_list'),
    path('trends/<int:pk>/', views.TrendItemDetailView.as_view(), name='trenditem_detail'),
    path('trends/create/', views.TrendItemCreateView.as_view(), name='trenditem_create'),
    path('trends/<int:pk>/update/', views.TrendItemUpdateView.as_view(), name='trenditem_update'),
    path('trends/<int:pk>/delete/', views.TrendItemDeleteView.as_view(), name='trenditem_delete'),
    
    # TrendTracking URLs
    path('tracking/', views.TrendTrackingListView.as_view(), name='trendtracking_list'),
    path('tracking/<int:pk>/', views.TrendTrackingDetailView.as_view(), name='trendtracking_detail'),
    path('tracking/create/', views.TrendTrackingCreateView.as_view(), name='trendtracking_create'),
    path('tracking/<int:pk>/update/', views.TrendTrackingUpdateView.as_view(), name='trendtracking_update'),
    path('tracking/<int:pk>/delete/', views.TrendTrackingDeleteView.as_view(), name='trendtracking_delete'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
]