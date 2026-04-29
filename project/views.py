from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse
from django.http import Http404
from .models import Trail, Profile, GearItem, Trip, PackListItem
from .forms import ProfileForm, GearItemForm, TripForm, PackListItemForm, TripFinderForm, TrailForm
import json
from math import radians, cos, sqrt
from datetime import date, timedelta
 


class MyLoginRequiredMixin(LoginRequiredMixin):

    def get_login_url(self):
        return reverse('project:login')

    def get_logged_in_profile(self):
        return Profile.objects.get(user=self.request.user)


# weather API using open metro

import requests

def get_weather_forecast(lat, lng, start_date):
    """get weather forecast from open-metro api for a location and date"""
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lng}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        f"&temperature_unit=fahrenheit"
        f"&timezone=America/New_York"
        f"&start_date={start_date}&end_date={start_date}"
    )
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return {
            'temp_high': data['daily']['temperature_2m_max'][0],
            'temp_low': data['daily']['temperature_2m_min'][0],
            'precip_chance': data['daily']['precipitation_probability_max'][0] or 0,
        }
    except Exception as e:
        print(f"WEATHER ERROR: {e}")
        return None


# recomendation alg

def recommend_for_category(category, gear_items, weather, nights):
    """pick the best item for every category"""
    if not gear_items:
        return None

    if category == 'Sleeping Bag':
        warm_enough = [g for g in gear_items if g.temp_rating_f and g.temp_rating_f <= weather['temp_low']]
        if warm_enough:
            return min(warm_enough, key=lambda g: g.weight_oz)
        # nothing warm enough recommend the user buys 
        return {'needs_purchase': True, 'message': f"You don't have a bag rated for {weather['temp_low']}°F. Consider buying one rated for at least {weather['temp_low'] - 10}°F."}

    elif category == 'Sleeping Pad':
        warm_enough = [g for g in gear_items if g.temp_rating_f and g.temp_rating_f <= weather['temp_low']]
        if warm_enough:
            return min(warm_enough, key=lambda g: g.weight_oz)
        return {'needs_purchase': True, 'message': f"No sleep pad rated for {weather['temp_low']}°F. Consider buying one for cold-weather camping."}

    elif category == 'Shelter':
        # heavy rain expected so we go with largest since bigger tents are usually stronger and more waterproof
        if weather['precip_chance'] >= 50:
            return max(gear_items, key=lambda g: g.weight_oz)
        # otherwise pick the lightest
        return min(gear_items, key=lambda g: g.weight_oz)

    elif category == 'Clothing':
        # cold beflow freezing + wet means its snowing so we select items with snow rating
        if weather['temp_high'] < 32:
            snow = [g for g in gear_items if g.is_snow_gear]
            if snow:
                return snow[0]
        #rain gear
        if weather['precip_chance'] >= 30:
            rain = [g for g in gear_items if g.is_rain_gear]
            if rain:
                return rain[0]
        # default is the lightest gear
        return min(gear_items, key=lambda g: g.weight_oz)
    elif category == 'Cook Kit':
        # butane stops working under 10 degrees so recomend white gas 
        if weather['temp_low'] < 10:
            white_gas = [g for g in gear_items if 'white gas' in g.name.lower()]
            if white_gas:
                return white_gas[0]
        else:
            butane = [g for g in gear_items if 'butane' in g.name.lower()]
            if butane:
                return butane[0]
        # fallback if neither is found by name
        return min(gear_items, key=lambda g: g.weight_oz)

    else:
        return None


# landing page view

class LandingView(TemplateView):
    template_name = 'project/landing.html'


# list view

class TrailListView(ListView):
    model = Trail
    template_name = 'project/trail_list.html'
    context_object_name = 'trails'

    def get_queryset(self):
        qs = Trail.objects.all()
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trails_json'] = json.dumps([
            {'name': t.name, 'lat': t.latitude, 'lng': t.longitude, 'id': t.pk}
            for t in self.get_queryset()
        ])
        return context


class GearListView(MyLoginRequiredMixin, ListView):
    model = GearItem
    template_name = 'project/gear_list.html'
    context_object_name = 'gear_items'

    def get_queryset(self):
        profile = self.get_logged_in_profile()
        qs = GearItem.objects.filter(profile=profile)
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gear = self.get_queryset()
        total_oz = sum(item.weight_oz for item in gear)
        context['total_weight_lbs'] = round(total_oz / 16, 2)
        context['categories'] = GearItem.CATEGORY_CHOICES
        context['total_weight_lbs'] = round(total_oz / 16, 2)
        context['total_weight_oz'] = round(total_oz, 1) 
        return context


class TripListView(MyLoginRequiredMixin, ListView):
    model = Trip
    template_name = 'project/trip_list.html'
    context_object_name = 'trips'

    def get_queryset(self):
        profile = self.get_logged_in_profile()
        return Trip.objects.filter(profile=profile)


# detail views

class TrailDetailView(DetailView):
    model = Trail
    template_name = 'project/trail_detail.html'
    context_object_name = 'trail'


class ProfileDetailView(MyLoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'


class GearDetailView(MyLoginRequiredMixin, DetailView):
    model = GearItem
    template_name = 'project/gear_detail.html'
    context_object_name = 'gear_item'


class TripDetailView(MyLoginRequiredMixin, DetailView):
    model = Trip
    template_name = 'project/trip_detail.html'
    context_object_name = 'trip'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = self.object
        profile = self.get_logged_in_profile()

        # get the weatehr for the trail location and date
        weather = get_weather_forecast(trip.trail.latitude, trip.trail.longitude, trip.start_date)
        context['weather'] = weather

        #num nights
        nights = (trip.end_date - trip.start_date).days

        # every gear category is a section to keep planning simple
        sections = []
        for cat_value, cat_label in GearItem.CATEGORY_CHOICES:
            items = list(GearItem.objects.filter(profile=profile, category=cat_value))
            if not items:
                continue  # skip empty categories

            # recomendations are only based on weather so no weather means no recomendations
            if weather:
                recommended = recommend_for_category(cat_value, items, weather, nights)
            else:
                # if there isnt weather forcast we reocmend the lightest item
                recommended = min(items, key=lambda g: g.weight_oz)

            # what's already in the pack list for this category?
            packed_ids = set(
                PackListItem.objects.filter(trip=trip, gear_item__category=cat_value)
                .values_list('gear_item_id', flat=True)
            )

            recommended = recommend_for_category(cat_value, items, weather, nights)
            needs_purchase = isinstance(recommended, dict) # either the recomendation or the message saying you have the wrong gear

            sections.append({
                'label': cat_label,
                'category': cat_value,
                'items': items,
                'recommended': recommended if not needs_purchase else None,
                'needs_purchase': needs_purchase,
                'purchase_message': recommended.get('message') if needs_purchase else None, 
                'packed_ids': packed_ids,
            })
        context['sections'] = sections
        context['daily_mileage'] = round(trip.trail.distance_miles / (nights + 1), 1)
        context['total_mileage'] = trip.trail.distance_miles

       
        # pack list totals
        pack_items = PackListItem.objects.filter(trip=trip)
        context['pack_items'] = pack_items
        total_oz = sum(i.gear_item.weight_oz * i.quantity for i in pack_items)
        context['total_weight_lbs'] = round(total_oz / 16, 2)
        context['nights'] = nights
        context['total_weight_lbs'] = round(total_oz / 16, 2)
        context['total_weight_oz'] = round(total_oz, 1)

        return context


# create views

class CreateProfileView(CreateView):
    '''view to create a profile'''
    model = Profile
    form_class = ProfileForm
    template_name = 'project/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_creation_form = UserCreationForm(self.request.POST)

        if not user_creation_form.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form)
            )

        user = user_creation_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project:landing')


class GearCreateView(MyLoginRequiredMixin, CreateView):
    '''view to add a gear item'''
    model = GearItem
    form_class = GearItemForm
    template_name = 'project/gear_form.html'

    def get_initial(self):
        initial = super().get_initial()
        category = self.request.GET.get('category')
        if category:
            initial['category'] = category
        return initial

    def form_valid(self, form):
        form.instance.profile = self.get_logged_in_profile()
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('project:gear_list')


class TripCreateView(MyLoginRequiredMixin, CreateView):
    '''gear to make a new trip'''
    model = Trip
    form_class = TripForm
    template_name = 'project/trip_form.html'

    def get_initial(self):
        initial = super().get_initial()
        trail_id = self.request.GET.get('trail')
        nights = self.request.GET.get('nights')
        if trail_id:
            initial['trail'] = trail_id
        if nights:
            try:
                n = int(nights)
                start = date.today() + timedelta(days=7)
                initial['start_date'] = start
                initial['end_date'] = start + timedelta(days=n)
            except ValueError:
                pass
        return initial

    def form_valid(self, form):
        form.instance.profile = self.get_logged_in_profile()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project:trip_detail', kwargs={'pk': self.object.pk})

class TrailCreateView(MyLoginRequiredMixin, CreateView):
    '''view to add a trail'''
    model = Trail
    form_class = TrailForm
    template_name = 'project/trail_form.html'

    def get_success_url(self):
        return reverse('project:trail_detail', kwargs={'pk': self.object.pk})
    
# update Views

class ProfileUpdateView(MyLoginRequiredMixin, UpdateView):
    '''view to update a profile'''
    model = Profile
    form_class = ProfileForm
    template_name = 'project/profile_form.html'

    def get_object(self):
        return self.get_logged_in_profile()

    def get_success_url(self):
        return reverse('project:profile_detail', kwargs={'pk': self.object.pk})


class GearUpdateView(MyLoginRequiredMixin, UpdateView):
    ''''view to update gear item'''
    model = GearItem
    form_class = GearItemForm
    template_name = 'project/gear_form.html'

    def get_success_url(self):
        return reverse('project:gear_detail', kwargs={'pk': self.object.pk})


class TripUpdateView(MyLoginRequiredMixin, UpdateView):
    '''view to update a trip'''
    model = Trip
    form_class = TripForm
    template_name = 'project/trip_form.html'

    def get_success_url(self):
        return reverse('project:trip_detail', kwargs={'pk': self.object.pk})

class TrailUpdateView(MyLoginRequiredMixin, UpdateView):
    '''view to update a trail'''
    model = Trail
    form_class = TrailForm 
    template_name = 'project/trail_form.html'

    def get_success_url(self):
        return reverse('project:trail_detail', kwargs={'pk': self.object.pk})



# delete Views

class GearDeleteView(MyLoginRequiredMixin, DeleteView):
    model = GearItem
    template_name = 'project/gear_confirm_delete.html'

    def get_success_url(self):
        return reverse('project:gear_list')


class TripDeleteView(MyLoginRequiredMixin, DeleteView):
    model = Trip
    template_name = 'project/trip_confirm_delete.html'

    def get_success_url(self):
        return reverse('project:trip_list')

class TrailDeleteView(MyLoginRequiredMixin, DeleteView):
    model = Trail
    template_name = 'project/trail_confirm_delete.html'

    def get_success_url(self):
        return reverse('project:trail_list')


# pack list item view functions

def add_pack_items(request, trip_pk):
    try:
        trip = Trip.objects.get(pk=trip_pk)
    except Trip.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        gear_ids = request.POST.getlist('gear_ids')
        section = request.POST.get('section', '')

        for gear_id in gear_ids:
            try:
                gear = GearItem.objects.get(pk=gear_id)
                PackListItem.objects.get_or_create(trip=trip, gear_item=gear)
            except GearItem.DoesNotExist:
                pass

        url = reverse('project:trip_detail', kwargs={'pk': trip_pk})
        if section:
            url += f'#section-{section}' ##start from the section where we were adding
        return redirect(url)

    return redirect('project:trip_detail', pk=trip_pk)



def remove_pack_item(request, pk):
    try:
        item = PackListItem.objects.get(pk=pk)
    except PackListItem.DoesNotExist:
        raise Http404

    trip_pk = item.trip.pk
    item.delete()
    return redirect('project:trip_detail', pk=trip_pk)


def toggle_packed(request, pk):
    try:
        item = PackListItem.objects.get(pk=pk)
    except PackListItem.DoesNotExist:
        raise Http404

    item.is_packed = not item.is_packed
    item.save()
    return redirect('project:trip_detail', pk=item.trip.pk)


# trip finder functions

def rough_distance_miles(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    x = (lon2 - lon1) * cos((lat1 + lat2) / 2)
    y = lat2 - lat1
    return sqrt(x * x + y * y) * 3963


def trip_finder(request):
    profile = request.user.project_profile
    results = None
    nights = None
    trails_json = '[]'

    if request.method == 'POST':
        form = TripFinderForm(request.POST)
        if form.is_valid():
            max_drive_hours = form.cleaned_data['max_drive_hours']
            nights = form.cleaned_data['nights']
            max_miles = max_drive_hours * 50 # here we assume 50mph as an average of highway speed and back country driving which is slower

            nearby = []
            for trail in Trail.objects.all():
                if nights < trail.min_nights or nights > trail.max_nights:
                    continue

                dist = rough_distance_miles(
                    profile.home_latitude, profile.home_longitude,
                    trail.latitude, trail.longitude
                )
                if dist <= max_miles:
                    nearby.append({'trail': trail, 'distance': round(dist, 1)})

            nearby.sort(key=lambda x: x['distance'])
            results = nearby

            trails_json = json.dumps([
                {'name': r['trail'].name, 'lat': r['trail'].latitude,
                 'lng': r['trail'].longitude, 'id': r['trail'].pk,
                 'distance': r['distance']}
                for r in nearby
            ])
    else:
        form = TripFinderForm()

    return render(request, 'project/trip_finder.html', {
        'form': form,
        'results': results,
        'nights': nights,
        'trails_json': trails_json,
        'profile': profile,
    })

