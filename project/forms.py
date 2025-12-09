"""
File: forms.py
Author: Shanika Paul
Description: Forms for fashion trend analytics platform.
"""

from django import forms
from .models import Designer, Collection, TrendItem, TrendTracking

class DesignerForm(forms.ModelForm):
    """Form for creating and updating Designer records."""
    class Meta:
        model = Designer
        fields = ['name', 'country', 'founded_year', 'style_category', 'description', 'website']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CollectionForm(forms.ModelForm):
    """Form for creating and updating Collection records."""
    class Meta:
        model = Collection
        fields = ['designer', 'season', 'year', 'location', 'theme', 'show_date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'show_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TrendItemForm(forms.ModelForm):
    """Form for creating and updating TrendItem records."""
    class Meta:
        model = TrendItem
        fields = ['collection', 'trend_name', 'category', 'popularity_score', 'description', 'influence_level']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TrendTrackingForm(forms.ModelForm):
    """Form for creating and updating TrendTracking records."""
    class Meta:
        model = TrendTracking
        fields = ['trend_name', 'year', 'quarter', 'mentions_count', 'popularity_rating', 'trend_status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }