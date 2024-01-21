from django.contrib import admin

# Register your models here.
from .models import User, Driver, Ride, Feedback

admin.site.register(User)
admin.site.register(Driver)
admin.site.register(Ride)
admin.site.register(Feedback)