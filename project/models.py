from django.db import models
from django.contrib.auth.models import User


class Trail(models.Model):
    """A hiking trail """

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Moderate', 'Moderate'),
        ('Hard', 'Hard'),
        ('Expert', 'Expert'),
    ]

    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    distance_miles = models.FloatField()
    elevation_gain_ft = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    is_loop = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    min_nights = models.IntegerField(default=1)
    max_nights = models.IntegerField(default=3)

    def night_range(self):
        """show nights as a range like '2-3' or just '2' if equal"""
        if self.min_nights == self.max_nights:
            return str(self.min_nights)
        return f"{self.min_nights}-{self.max_nights}"

    def __str__(self):
        return f"{self.name} ({self.region})"


class Profile(models.Model):
    """Extends Django User with backpacking preferences"""

    EXPERIENCE_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile')
    home_latitude = models.FloatField()
    home_longitude = models.FloatField()
    home_location = models.CharField(max_length=200)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='Beginner')

    def __str__(self):
        return f"{self.user.username}"


class GearItem(models.Model):
    """A piece of gear owned by a user"""

    CATEGORY_CHOICES = [
        ('Shelter', 'Shelter'),
        ('Sleeping Bag', 'Sleeping Bag'),
        ('Sleeping Pad', 'Sleeping Pad'),
        ('Cook Kit', 'Cook Kit'),
        ('Clothing', 'Clothing'),
        ('Pack/Bag', 'Pack/Bag'),
        ('Electronics', 'Electronics'),
        ('Safety/First Aid', 'Safety/First Aid'),
        ('Other', 'Other'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    weight_oz = models.FloatField()
    temp_rating_f = models.IntegerField(null=True, blank=True)
    is_rain_gear = models.BooleanField(default=False)
    is_snow_gear = models.BooleanField(default=False)
    brand = models.CharField(max_length=100, blank=True)
    
    def weight_lbs(self):
        return round(self.weight_oz / 16, 2)

    def weight_display(self):
        """show as '0.5 lbs / 8 oz'"""
        return f"{self.weight_lbs()} lbs / {self.weight_oz} oz"
    
    def display_name(self):
        if self.brand:
            return f"{self.brand} {self.name}"
        return self.name

    def __str__(self):
        return f"{self.name} — {self.weight_oz} oz"


class Trip(models.Model):
    """A planned or completed backpacking trip"""

    STATUS_CHOICES = [
        ('Planning', 'Planning'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    trail = models.ForeignKey(Trail, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planning')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.trail.name} — {self.start_date}"


class PackListItem(models.Model):
    """An item packed for a specific trip"""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    gear_item = models.ForeignKey(GearItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_packed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.gear_item.name} x{self.quantity}"