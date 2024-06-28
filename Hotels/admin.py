

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Room, Profile

admin.site.register(Room)
admin.site.register(Profile)
