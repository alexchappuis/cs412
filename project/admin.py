from django.contrib import admin

# Register your models here.

from .models import Trail, Profile, GearItem, Trip, PackListItem

admin.site.register(Trail)
admin.site.register(Profile)
admin.site.register(GearItem)
admin.site.register(Trip)
admin.site.register(PackListItem)