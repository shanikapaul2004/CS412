"""
File: views.py
Author: Shanika Paul
Description: Views for fashion trend analytics platform.
Includes list, detail, create, update, delete views and analytics reports.
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count, Avg, Q
from .models import Designer, Collection, TrendItem, TrendTracking
from .forms import DesignerForm, CollectionForm, TrendItemForm, TrendTrackingForm

# Home View
def home(request):
    """
    Display dashboard with overview of fashion trends and recent activity.
    """
    total_designers = Designer.objects.count()
    total_collections = Collection.objects.count()
    total_trends = TrendItem.objects.count()
    
    # Get recent collections
    recent_collections = Collection.objects.all()[:5]
    
    # Get top trends by popularity
    top_trends = TrendItem.objects.order_by('-popularity_score')[:5]
    
    # Get trending styles
    trending_tracking = TrendTracking.objects.filter(trend_status='rising')[:5]
    
    context = {
        'total_designers': total_designers,
        'total_collections': total_collections,
        'total_trends': total_trends,
        'recent_collections': recent_collections,
        'top_trends': top_trends,
        'trending_tracking': trending_tracking,
    }
    return render(request, 'project/home.html', context)


# Designer Views
class DesignerListView(ListView):
    """Display list of all designers with filtering options."""
    model = Designer
    template_name = 'project/designer_list.html'
    context_object_name = 'designers'
    
    def get_queryset(self):
        """Filter designers based on query parameters."""
        queryset = Designer.objects.all()
        
        # Filter by style category
        style = self.request.GET.get('style')
        if style:
            queryset = queryset.filter(style_category=style)
        
        # Filter by country
        country = self.request.GET.get('country')
        if country:
            queryset = queryset.filter(country__icontains=country)
        
        # Search by name
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        
        return queryset


class DesignerDetailView(DetailView):
    """Display detailed view of a designer including their collections and trends."""
    model = Designer
    template_name = 'project/designer_detail.html'
    context_object_name = 'designer'
    
    def get_context_data(self, **kwargs):
        """Add designer's collections and statistics to context."""
        context = super().get_context_data(**kwargs)
        context['collections'] = self.object.collection_set.all()
        
        # Get all trends from this designer's collections
        context['trends'] = TrendItem.objects.filter(collection__designer=self.object)
        
        return context


class DesignerCreateView(CreateView):
    """Create a new designer."""
    model = Designer
    form_class = DesignerForm
    template_name = 'project/designer_form.html'
    success_url = reverse_lazy('project:designer_list')


class DesignerUpdateView(UpdateView):
    """Update an existing designer."""
    model = Designer
    form_class = DesignerForm
    template_name = 'project/designer_form.html'
    success_url = reverse_lazy('project:designer_list')


class DesignerDeleteView(DeleteView):
    """Delete a designer."""
    model = Designer
    template_name = 'project/designer_confirm_delete.html'
    success_url = reverse_lazy('project:designer_list')


# Collection Views
class CollectionListView(ListView):
    """Display list of all collections with filtering options."""
    model = Collection
    template_name = 'project/collection_list.html'
    context_object_name = 'collections'
    paginate_by = 20
    
    def get_queryset(self):
        """Filter collections based on query parameters."""
        queryset = Collection.objects.all()
        
        # Filter by season
        season = self.request.GET.get('season')
        if season:
            queryset = queryset.filter(season=season)
        
        # Filter by year
        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(year=year)
        
        # Filter by location
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location=location)
        
        # Filter by designer
        designer_id = self.request.GET.get('designer')
        if designer_id:
            queryset = queryset.filter(designer_id=designer_id)
        
        # Search by theme
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(theme__icontains=search) | Q(notes__icontains=search))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add filter options to context."""
        context = super().get_context_data(**kwargs)
        context['designers'] = Designer.objects.all()
        return context


class CollectionDetailView(DetailView):
    """Display detailed view of a collection including all its trends."""
    model = Collection
    template_name = 'project/collection_detail.html'
    context_object_name = 'collection'
    
    def get_context_data(self, **kwargs):
        """Add collection's trends to context."""
        context = super().get_context_data(**kwargs)
        context['trends'] = self.object.trenditem_set.all()
        return context


class CollectionCreateView(CreateView):
    """Create a new collection."""
    model = Collection
    form_class = CollectionForm
    template_name = 'project/collection_form.html'
    success_url = reverse_lazy('project:collection_list')


class CollectionUpdateView(UpdateView):
    """Update an existing collection."""
    model = Collection
    form_class = CollectionForm
    template_name = 'project/collection_form.html'
    success_url = reverse_lazy('project:collection_list')


class CollectionDeleteView(DeleteView):
    """Delete a collection."""
    model = Collection
    template_name = 'project/collection_confirm_delete.html'
    success_url = reverse_lazy('project:collection_list')


# TrendItem Views
class TrendItemListView(ListView):
    """Display list of all trends with filtering options."""
    model = TrendItem
    template_name = 'project/trenditem_list.html'
    context_object_name = 'trends'
    paginate_by = 30
    
    def get_queryset(self):
        """Filter trends based on query parameters."""
        queryset = TrendItem.objects.all()
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by influence level
        influence = self.request.GET.get('influence')
        if influence:
            queryset = queryset.filter(influence_level=influence)
        
        # Filter by popularity (minimum score)
        min_popularity = self.request.GET.get('min_popularity')
        if min_popularity:
            queryset = queryset.filter(popularity_score__gte=min_popularity)
        
        # Filter by year
        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(collection__year=year)
        
        # Search by trend name
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(trend_name__icontains=search) | Q(description__icontains=search))
        
        return queryset


class TrendItemDetailView(DetailView):
    """Display detailed view of a trend."""
    model = TrendItem
    template_name = 'project/trenditem_detail.html'
    context_object_name = 'trend'


class TrendItemCreateView(CreateView):
    """Create a new trend."""
    model = TrendItem
    form_class = TrendItemForm
    template_name = 'project/trenditem_form.html'
    success_url = reverse_lazy('project:trenditem_list')


class TrendItemUpdateView(UpdateView):
    """Update an existing trend."""
    model = TrendItem
    form_class = TrendItemForm
    template_name = 'project/trenditem_form.html'
    success_url = reverse_lazy('project:trenditem_list')


class TrendItemDeleteView(DeleteView):
    """Delete a trend."""
    model = TrendItem
    template_name = 'project/trenditem_confirm_delete.html'
    success_url = reverse_lazy('project:trenditem_list')


# TrendTracking Views
class TrendTrackingListView(ListView):
    """Display list of all trend tracking records."""
    model = TrendTracking
    template_name = 'project/trendtracking_list.html'
    context_object_name = 'trackings'
    paginate_by = 20
    
    def get_queryset(self):
        """Filter trend tracking based on query parameters."""
        queryset = TrendTracking.objects.all()
        
        # Filter by year
        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(year=year)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(trend_status=status)
        
        # Search by trend name
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(trend_name__icontains=search)
        
        return queryset


class TrendTrackingDetailView(DetailView):
    """Display detailed view of trend tracking including related collections."""
    model = TrendTracking
    template_name = 'project/trendtracking_detail.html'
    context_object_name = 'tracking'
    
    def get_context_data(self, **kwargs):
        """Add related trend items to context."""
        context = super().get_context_data(**kwargs)
        context['related_trends'] = self.object.get_related_collections()
        return context


class TrendTrackingCreateView(CreateView):
    """Create a new trend tracking record."""
    model = TrendTracking
    form_class = TrendTrackingForm
    template_name = 'project/trendtracking_form.html'
    success_url = reverse_lazy('project:trendtracking_list')


class TrendTrackingUpdateView(UpdateView):
    """Update an existing trend tracking record."""
    model = TrendTracking
    form_class = TrendTrackingForm
    template_name = 'project/trendtracking_form.html'
    success_url = reverse_lazy('project:trendtracking_list')


class TrendTrackingDeleteView(DeleteView):
    """Delete a trend tracking record."""
    model = TrendTracking
    template_name = 'project/trendtracking_confirm_delete.html'
    success_url = reverse_lazy('project:trendtracking_list')


# Analytics/Reports View
def analytics(request):
    """
    Display analytics and reports about fashion trends.
    Includes charts and statistics.
    """
    # Top designers by collection count
    top_designers = Designer.objects.annotate(
        num_collections=Count('collection')
    ).order_by('-num_collections')[:10]
    
    # Trends by category
    trends_by_category = TrendItem.objects.values('category').annotate(
        count=Count('id'),
        avg_popularity=Avg('popularity_score')
    ).order_by('-count')
    
    # Collections by location
    collections_by_location = Collection.objects.values('location').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Recent years analysis
    years = Collection.objects.values_list('year', flat=True).distinct().order_by('-year')[:5]
    year_stats = []
    for year in years:
        collections = Collection.objects.filter(year=year)
        trends = TrendItem.objects.filter(collection__year=year)
        year_stats.append({
            'year': year,
            'collections': collections.count(),
            'trends': trends.count(),
            'avg_popularity': trends.aggregate(avg=Avg('popularity_score'))['avg'] or 0,
        })
    
    # Top 10 most popular trends
    top_trends = TrendItem.objects.order_by('-popularity_score')[:10]
    
    # Trending status distribution
    trend_status_dist = TrendTracking.objects.values('trend_status').annotate(
        count=Count('id')
    )
    
    context = {
        'top_designers': top_designers,
        'trends_by_category': trends_by_category,
        'collections_by_location': collections_by_location,
        'year_stats': year_stats,
        'top_trends': top_trends,
        'trend_status_dist': trend_status_dist,
    }
    return render(request, 'project/analytics.html', context)