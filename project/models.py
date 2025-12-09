"""
File: models.py
Author: Shanika Paul
Description: Data models for fashion trend analytics platform.
Tracks designers, collections, trends, and their evolution over time.
"""

from django.db import models
from django.db.models import Count, Avg

class Designer(models.Model):
    """
    Represents a fashion designer or brand.
    This model can exist independently without foreign keys.
    """
    STYLE_CHOICES = [
        ('luxury', 'Luxury'),
        ('streetwear', 'Streetwear'),
        ('fast_fashion', 'Fast Fashion'),
        ('sustainable', 'Sustainable'),
        ('avant_garde', 'Avant-Garde'),
        ('minimalist', 'Minimalist'),
    ]
    
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    style_category = models.CharField(max_length=50, choices=STYLE_CHOICES)
    description = models.TextField()
    website = models.URLField(blank=True)
    
    def __str__(self):
        """Return string representation of designer."""
        return f"{self.name} ({self.country})"
    
    def collection_count(self):
        """Return number of collections by this designer."""
        return self.collection_set.count()
    
    def average_trend_popularity(self):
        """Calculate average popularity of trends from this designer's collections."""
        trends = TrendItem.objects.filter(collection__designer=self)
        if trends.exists():
            return trends.aggregate(avg=Avg('popularity_score'))['avg']
        return 0


class Collection(models.Model):
    """
    Represents a fashion collection (e.g., Spring 2024 Paris Fashion Week).
    Requires foreign key to Designer.
    """
    SEASON_CHOICES = [
        ('SS', 'Spring/Summer'),
        ('FW', 'Fall/Winter'),
        ('Resort', 'Resort'),
        ('Pre-Fall', 'Pre-Fall'),
    ]
    
    LOCATION_CHOICES = [
        ('Paris', 'Paris'),
        ('Milan', 'Milan'),
        ('New York', 'New York'),
        ('London', 'London'),
        ('Tokyo', 'Tokyo'),
        ('Other', 'Other'),
    ]
    
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE)
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    year = models.IntegerField()
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    theme = models.CharField(max_length=300)
    show_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-year', 'season']
        unique_together = ['designer', 'season', 'year']
    
    def __str__(self):
        """Return string representation of collection."""
        return f"{self.designer.name} {self.season} {self.year}"
    
    def trend_count(self):
        """Return number of trends in this collection."""
        return self.trenditem_set.count()


class TrendItem(models.Model):
    """
    Represents a specific trend from a collection.
    Requires foreign key to Collection.
    """
    CATEGORY_CHOICES = [
        ('color', 'Color'),
        ('silhouette', 'Silhouette'),
        ('fabric', 'Fabric/Material'),
        ('pattern', 'Pattern'),
        ('accessory', 'Accessory'),
        ('styling', 'Styling'),
        ('theme', 'Theme/Concept'),
    ]
    
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    trend_name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    popularity_score = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)],
        help_text="Rate from 1 (low) to 10 (high)"
    )
    description = models.TextField()
    influence_level = models.CharField(
        max_length=20,
        choices=[
            ('niche', 'Niche'),
            ('emerging', 'Emerging'),
            ('mainstream', 'Mainstream'),
            ('iconic', 'Iconic'),
        ],
        default='emerging'
    )
    
    class Meta:
        ordering = ['-popularity_score', 'trend_name']
    
    def __str__(self):
        """Return string representation of trend."""
        return f"{self.trend_name} - {self.collection.designer.name} {self.collection.year}"


class TrendTracking(models.Model):
    """
    Tracks how trends evolve over time across multiple collections.
    Aggregates trend data by time period.
    """
    trend_name = models.CharField(max_length=200)
    year = models.IntegerField()
    quarter = models.IntegerField(choices=[(i, f'Q{i}') for i in range(1, 5)])
    mentions_count = models.IntegerField(
        default=0,
        help_text="Number of collections featuring this trend"
    )
    popularity_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Average popularity score"
    )
    trend_status = models.CharField(
        max_length=20,
        choices=[
            ('emerging', 'Emerging'),
            ('rising', 'Rising'),
            ('peak', 'Peak'),
            ('declining', 'Declining'),
            ('archived', 'Archived'),
        ],
        default='emerging'
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-year', '-quarter']
        unique_together = ['trend_name', 'year', 'quarter']
    
    def __str__(self):
        """Return string representation of trend tracking."""
        return f"{self.trend_name} - Q{self.quarter} {self.year}"
    
    def get_related_collections(self):
        """Find collections featuring this trend in the tracked period."""
        # Determine season based on quarter
        if self.quarter in [1, 2]:
            season = 'SS'
        else:
            season = 'FW'
        
        return TrendItem.objects.filter(
            trend_name__icontains=self.trend_name,
            collection__year=self.year,
            collection__season=season
        )