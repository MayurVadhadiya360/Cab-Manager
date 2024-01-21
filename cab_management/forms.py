from django import forms
from .models import User, Driver

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class RideBookingForm(forms.Form):
    pickup_point = forms.CharField(max_length=100)
    dropoff_point = forms.CharField(max_length=100)
    vehicle_preference = forms.CharField(max_length=50)

class DriverSignupForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['username', 'email', 'password', 'license_number', 'vehicle_model', 'availability']