# file: views.py
# name: Shanika Paul
# email: shanikap@bu.edu
# date: October 31, 2025
# description: Views for voter_analytics application including VotersListView, VoterDetailView, and GraphsView with filtering and graphing functionality.

from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go

class VotersListView(ListView):
    '''View to display all voter records.'''
    
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        '''Return the queryset of voters, potentially filtered.'''
        
        # Start with all voters
        qs = super().get_queryset()
        
        # Filter by party affiliation
        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation']
            if party:  # Only filter if a party was selected
                qs = qs.filter(party_affiliation=party)
        
        # Filter by minimum birth year
        if 'min_birth_year' in self.request.GET:
            min_year = self.request.GET['min_birth_year']
            if min_year:
                qs = qs.filter(date_of_birth__year__gte=min_year)
        
        # Filter by maximum birth year
        if 'max_birth_year' in self.request.GET:
            max_year = self.request.GET['max_birth_year']
            if max_year:
                qs = qs.filter(date_of_birth__year__lte=max_year)
        
        # Filter by voter score
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']
            if score:
                qs = qs.filter(voter_score=score)
        
        # Filter by elections voted in
        if 'v20state' in self.request.GET:
            qs = qs.filter(v20state=True)
        
        if 'v21town' in self.request.GET:
            qs = qs.filter(v21town=True)
        
        if 'v21primary' in self.request.GET:
            qs = qs.filter(v21primary=True)
        
        if 'v22general' in self.request.GET:
            qs = qs.filter(v22general=True)
        
        if 'v23town' in self.request.GET:
            qs = qs.filter(v23town=True)
        
        return qs
    
    
class VoterDetailView(DetailView):
    '''View to show detail page for one voter.'''
    
    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'
    
class GraphsView(ListView):
    '''View to display graphs of voter data.'''
    
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'
    
    def get_queryset(self):
        '''Return the queryset of voters, potentially filtered.'''
        
        # Start with all voters
        qs = super().get_queryset()
        
        # Apply the same filters as VotersListView
        # Filter by party affiliation
        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation']
            if party:
                qs = qs.filter(party_affiliation=party)
        
        # Filter by minimum birth year
        if 'min_birth_year' in self.request.GET:
            min_year = self.request.GET['min_birth_year']
            if min_year:
                qs = qs.filter(date_of_birth__year__gte=min_year)
        
        # Filter by maximum birth year
        if 'max_birth_year' in self.request.GET:
            max_year = self.request.GET['max_birth_year']
            if max_year:
                qs = qs.filter(date_of_birth__year__lte=max_year)
        
        # Filter by voter score
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']
            if score:
                qs = qs.filter(voter_score=score)
        
        # Filter by elections voted in
        if 'v20state' in self.request.GET:
            qs = qs.filter(v20state=True)
        
        if 'v21town' in self.request.GET:
            qs = qs.filter(v21town=True)
        
        if 'v21primary' in self.request.GET:
            qs = qs.filter(v21primary=True)
        
        if 'v22general' in self.request.GET:
            qs = qs.filter(v22general=True)
        
        if 'v23town' in self.request.GET:
            qs = qs.filter(v23town=True)
        
        return qs
    
    def get_context_data(self, **kwargs):
        '''Add graph data to context.'''
        
        context = super().get_context_data(**kwargs)
        
        # Get the filtered queryset
        voters = self.get_queryset()
        
        # Graph 1: Distribution by Year of Birth (Histogram)
        birth_years = [voter.date_of_birth.year for voter in voters]
        
        # Count voters by year
        from collections import Counter
        year_counts = Counter(birth_years)
        
        x_years = sorted(year_counts.keys())
        y_counts = [year_counts[year] for year in x_years]
        
        fig_birth_year = go.Bar(x=x_years, y=y_counts)
        graph_birth_year = plotly.offline.plot(
            {"data": [fig_birth_year],
             "layout": {"title": "Distribution of Voters by Year of Birth"}},
            auto_open=False,
            output_type="div"
        )
        context['graph_birth_year'] = graph_birth_year
        
        # Graph 2: Distribution by Party Affiliation (Pie Chart)
        party_counts = {}
        for voter in voters:
            party = voter.party_affiliation
            party_counts[party] = party_counts.get(party, 0) + 1
        
        x_parties = list(party_counts.keys())
        y_party_counts = list(party_counts.values())
        
        fig_party = go.Pie(labels=x_parties, values=y_party_counts)
        graph_party = plotly.offline.plot(
            {"data": [fig_party],
             "layout": {"title": "Distribution of Voters by Party Affiliation"}},
            auto_open=False,
            output_type="div"
        )
        context['graph_party'] = graph_party
        
        # Graph 3: Distribution by Election Participation (Histogram)
        elections = {
            'v20state': 0,
            'v21town': 0,
            'v21primary': 0,
            'v22general': 0,
            'v23town': 0
        }
        
        for voter in voters:
            if voter.v20state:
                elections['v20state'] += 1
            if voter.v21town:
                elections['v21town'] += 1
            if voter.v21primary:
                elections['v21primary'] += 1
            if voter.v22general:
                elections['v22general'] += 1
            if voter.v23town:
                elections['v23town'] += 1
        
        x_elections = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        y_election_counts = [
            elections['v20state'],
            elections['v21town'],
            elections['v21primary'],
            elections['v22general'],
            elections['v23town']
        ]
        
        fig_elections = go.Bar(x=x_elections, y=y_election_counts)
        graph_elections = plotly.offline.plot(
            {"data": [fig_elections],
             "layout": {"title": "Voter Participation in Each Election"}},
            auto_open=False,
            output_type="div"
        )
        context['graph_elections'] = graph_elections
        
        return context