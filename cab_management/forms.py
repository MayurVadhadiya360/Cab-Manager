from django import forms
from .models import User, Driver

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'required': True}),
            'email': forms.EmailInput(attrs={'required': True}),
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class RideBookingForm(forms.Form):
    pickup_point = forms.CharField(max_length=100, required=True)
    dropoff_point = forms.CharField(max_length=100, required=True)
    vehicle_preference = forms.CharField(max_length=50, required=True)

class DriverSignupForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['username', 'email', 'password', 'license_number', 'vehicle_model', 'availability']
        widgets = {
            'username': forms.TextInput(attrs={'required': True}),
            'email': forms.EmailInput(attrs={'required': True}),
            'password': forms.PasswordInput(attrs={'required': True}),
            'license_number': forms.TextInput(attrs={'required': True}),
            'vehicle_model': forms.TextInput(attrs={'required': True}),
            'availability': forms.CheckboxInput(attrs={'required': True}),
        }