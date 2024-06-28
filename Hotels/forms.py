# En Hotels/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Room

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone_number', 'address', 'profile_picture']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'image', 'capacity', 'description', 'price_per_night']

class CartItemForm(forms.Form):
    days = forms.IntegerField(label='Cantidad de días', min_value=1)
    has_breakfast = forms.BooleanField(label='Desayuno', required=False)
    has_lunch = forms.BooleanField(label='Almuerzo', required=False)
    has_transportation = forms.BooleanField(label='Transporte', required=False)        