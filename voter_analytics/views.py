from django.shortcuts import render

# Create your views here.


from django.views.generic import ListView, DetailView
from . models import Voter

import plotly
import plotly.graph_objs as go

class VoterListView(ListView):
    '''display a list of voters'''
 
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
 
    def get_queryset(self):
        '''filter voters by form submission'''
 
        voters = super().get_queryset()
 
        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation']
            if party:
                voters = voters.filter(party_affiliation=party)
 
        if 'min_year' in self.request.GET:
            min_year = self.request.GET['min_year']
            if min_year:
                voters = voters.filter(date_of_birth__year__gte=int(min_year))
 
        if 'max_year' in self.request.GET:
            max_year = self.request.GET['max_year']
            if max_year:
                voters = voters.filter(date_of_birth__year__lte=int(max_year))
 
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']
            if score:
                voters = voters.filter(voter_score=int(score))
 
        if 'v20state' in self.request.GET:
            voters = voters.filter(v20state=True)
        if 'v21town' in self.request.GET:
            voters = voters.filter(v21town=True)
        if 'v21primary' in self.request.GET:
            voters = voters.filter(v21primary=True)
        if 'v22general' in self.request.GET:
            voters = voters.filter(v22general=True)
        if 'v23town' in self.request.GET:
            voters = voters.filter(v23town=True)
 
        return voters
 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
 
        context['years'] = range(1900, 2026)
        context['voter_scores'] = range(0, 6)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
 
        context['selected_party'] = self.request.GET.get('party_affiliation', '')
        context['selected_min_year'] = self.request.GET.get('min_year', '')
        context['selected_max_year'] = self.request.GET.get('max_year', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['selected_v20state'] = 'v20state' in self.request.GET
        context['selected_v21town'] = 'v21town' in self.request.GET
        context['selected_v21primary'] = 'v21primary' in self.request.GET
        context['selected_v22general'] = 'v22general' in self.request.GET
        context['selected_v23town'] = 'v23town' in self.request.GET
 
        return context
 
 
class VoterDetailView(DetailView):
    '''view to show a single voter'''
 
    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'voter'
 
 
class VoterGraphsView(ListView):
    '''view to display graphs'''
 
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'
 
    def get_queryset(self):
        '''filter voters based on the form'''
 
        voters = super().get_queryset()
 
        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation']
            if party:
                voters = voters.filter(party_affiliation=party)
 
        if 'min_year' in self.request.GET:
            min_year = self.request.GET['min_year']
            if min_year:
                voters = voters.filter(date_of_birth__year__gte=int(min_year))
 
        if 'max_year' in self.request.GET:
            max_year = self.request.GET['max_year']
            if max_year:
                voters = voters.filter(date_of_birth__year__lte=int(max_year))
 
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']
            if score:
                voters = voters.filter(voter_score=int(score))
 
        if 'v20state' in self.request.GET:
            voters = voters.filter(v20state=True)
        if 'v21town' in self.request.GET:
            voters = voters.filter(v21town=True)
        if 'v21primary' in self.request.GET:
            voters = voters.filter(v21primary=True)
        if 'v22general' in self.request.GET:
            voters = voters.filter(v22general=True)
        if 'v23town' in self.request.GET:
            voters = voters.filter(v23town=True)
 
        return voters
 
    def get_context_data(self, **kwargs):
        '''
        Provide context variables for use in template
        '''
        context = super().get_context_data(**kwargs)
        voters = context['voters']
 
        context['years'] = range(1900, 2026)
        context['voter_scores'] = range(0, 6)
        context['party_affiliations'] = Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
 
        context['selected_party'] = self.request.GET.get('party_affiliation', '')
        context['selected_min_year'] = self.request.GET.get('min_year', '')
        context['selected_max_year'] = self.request.GET.get('max_year', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['selected_v20state'] = 'v20state' in self.request.GET
        context['selected_v21town'] = 'v21town' in self.request.GET
        context['selected_v21primary'] = 'v21primary' in self.request.GET
        context['selected_v22general'] = 'v22general' in self.request.GET
        context['selected_v23town'] = 'v23town' in self.request.GET
 
        x = sorted(set([v.date_of_birth.year for v in voters]))
        y = [len(voters.filter(date_of_birth__year=yr)) for yr in x]
 
        fig = go.Bar(x=x, y=y)
        title_text = f"Voter Distribution by Year of Birth"
        graph_div_birth = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        context['graph_div_birth'] = graph_div_birth
 
        x = sorted(set([v.party_affiliation for v in voters]))
        y = [len(voters.filter(party_affiliation=p)) for p in x]
 
        fig = go.Pie(labels=x, values=y)
        title_text = f"Voter Distribution by Party Affiliation"
        graph_div_party = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        context['graph_div_party'] = graph_div_party
 
        x = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        y = [voters.filter(v20state=True).count(),
             voters.filter(v21town=True).count(),
             voters.filter(v21primary=True).count(),
             voters.filter(v22general=True).count(),
             voters.filter(v23town=True).count(),
            ]
 
        fig = go.Bar(x=x, y=y)
        title_text = f"Voter Participation by Election"
        graph_div_elections = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        context['graph_div_elections'] = graph_div_elections

        return context