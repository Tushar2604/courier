'''from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# used django's (AbstractUser) to differentiate roles
class User(AbstractUser):
    is_sender = models.BooleanField(default=False)
    is_traveler = models.BooleanField(default=False)

# stores parcel related information
class Parcel(models.Model):
    sender = models.ForeignKey(User, related_name='sent_parcels', on_delete=models.CASCADE)
    traveler = models.ForeignKey(User, related_name='carried_parcel', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    weight = models.FloatField()
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    deadline = models.DateField()
    status = models.CharField(max_length=50, default='Pending') # other values can be, in transit, delivered
    created_at = models.DateTimeField(auto_now_add=True)

# stores travel information for travelers
class TravelDetails(models.Model):
    traveler = models.ForeignKey(User, related_name='travel_details', on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    travel_date = models.DateField()
    pnr_number = models.CharField(max_length=10)
    pnr_valid = models.BooleanField(default=False)

# handles payment between users
class Transaction(models.Model):
    parcel = models.OneToOneField(Parcel, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='transactions_made', on_delete=models.CASCADE)
    traveler = models.ForeignKey(User, related_name='transactions_received', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, default='Pending') # other value can be completed
    created_at = models.DateTimeField(auto_now_add=True)

# stores notifications for users
class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    '''