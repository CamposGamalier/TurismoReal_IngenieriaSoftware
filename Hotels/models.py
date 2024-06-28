from django.db import models
from django.contrib.auth.models import User
from datetime import date 
from decimal import Decimal
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
    
 
    
class Room(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='room_images/')
    capacity = models.IntegerField()
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    check_in_date = models.DateField(default=date.today)
    check_out_date = models.DateField()
    has_breakfast = models.BooleanField(default=False)
    has_lunch = models.BooleanField(default=False)
    has_transportation = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)