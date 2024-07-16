from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Driver(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    license_number = models.CharField(max_length=20, unique=True)
    vehicle_model = models.CharField(max_length=50)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_feedbacks = models.PositiveIntegerField(default=0)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class Ride(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    pickup_point = models.CharField(max_length=100)
    dropoff_point = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ride ID: {self.id} - User: {self.user.username} - Driver: {self.driver.username}"

class Feedback(models.Model):
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Feedback for Ride ID: {self.ride.pk} - Rating: {self.rating}"
