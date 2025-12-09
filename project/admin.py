"""
File: admin.py
Author: Shanika Paul
Description: Admin interface configuration for fashion trend analytics models.
"""

from django.contrib import admin
from .models import Designer, Collection, TrendItem, TrendTracking

@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    """Admin interface for Designer model."""
    list_display = ['name', 'country', 'founded_year', 'style_category', 'collection_count']
    list_filter = ['style_category', 'country']
    search_fields = ['name', 'country', 'description']
    ordering = ['name']

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """Admin interface for Collection model."""
    list_display = ['designer', 'season', 'year', 'location', 'theme', 'trend_count']
    list_filter = ['season', 'year', 'location', 'designer']
    search_fields = ['theme', 'notes', 'designer__name']
    date_hierarchy = 'show_date'
    ordering = ['-year', 'season']

@admin.register(TrendItem)
class TrendItemAdmin(admin.ModelAdmin):
    """Admin interface for TrendItem model."""
    list_display = ['trend_name', 'category', 'popularity_score', 'influence_level', 'collection']
    list_filter = ['category', 'influence_level', 'popularity_score', 'collection__year']
    search_fields = ['trend_name', 'description', 'collection__designer__name']
    ordering = ['-popularity_score', 'trend_name']

@admin.register(TrendTracking)
class TrendTrackingAdmin(admin.ModelAdmin):
    """Admin interface for TrendTracking model."""
    list_display = ['trend_name', 'year', 'quarter', 'mentions_count', 'popularity_rating', 'trend_status']
    list_filter = ['year', 'quarter', 'trend_status']
    search_fields = ['trend_name', 'notes']
    ordering = ['-year', '-quarter', 'trend_name']