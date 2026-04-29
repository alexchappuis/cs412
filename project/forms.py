from django import forms
from .models import Profile, GearItem, Trip, PackListItem, Trail

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['home_latitude', 'home_longitude', 'home_location', 'experience_level']
 
 
class GearItemForm(forms.ModelForm):
    class Meta:
        model = GearItem
        fields = ['name', 'category', 'weight_oz', 'temp_rating_f', 'is_rain_gear', 'is_snow_gear', 'brand']
 
 
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['trail', 'start_date', 'end_date', 'status', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
 
class TrailForm(forms.ModelForm):
    class Meta:
        model = Trail
        fields = ['name', 'region', 'latitude', 'longitude', 'distance_miles',
                  'elevation_gain_ft', 'difficulty', 'is_loop', 'description',
                  'min_nights', 'max_nights']

class PackListItemForm(forms.ModelForm):
    class Meta:
        model = PackListItem
        fields = ['gear_item', 'quantity']
 
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['gear_item'].queryset = GearItem.objects.filter(profile=user.project_profile)
 
 
class TripFinderForm(forms.Form):
    max_drive_hours = forms.FloatField(label='Max drive time (hours)', min_value=0.5, max_value=12)
    nights = forms.IntegerField(label='Number of nights', min_value=1, max_value=14)
    start_date = forms.DateField(
        label='Start date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
 