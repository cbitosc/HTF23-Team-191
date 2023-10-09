from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
class User(AbstractUser):
    pass

from django.db import models
from django.utils import timezone

class auctionlist(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    desc = models.TextField()
    starting_bid = models.IntegerField()
    image_url = models.CharField(max_length=228, default=None, blank=True, null=True)
    category = models.CharField(max_length=64)
    active_bool = models.BooleanField(default=True)
    daysleft = models.PositiveIntegerField(default=3)  # Example for 3 days
    end_time = models.DateTimeField(blank=True, null=True)  # Field to store the calculated end time

    def save(self, *args, **kwargs):
        if not self.end_time:
            # Calculate the initial end time based on the current date and time
            self.end_time = timezone.now() + timezone.timedelta(minutes=self.daysleft)
            print("heflkjfj",timezone.now())
        else:
            # If end_time is already set, add daysleft (in minutes) to it
            self.end_time += timezone.timedelta(minutes=self.daysleft)
        super().save(*args, **kwargs)

class bids(models.Model):
    user = models.CharField(max_length=30)
    listingid = models.IntegerField()
    bid = models.IntegerField()
    

class comments(models.Model):
    user = models.CharField(max_length=64)
    comment = models.TextField()
    listingid = models.IntegerField()
    

class watchlist(models.Model):
    watch_list = models.ForeignKey(auctionlist, on_delete=models.CASCADE)
    user = models.CharField(max_length=64)

class winner(models.Model):
    bid_win_list = models.ForeignKey(auctionlist, on_delete = models.CASCADE)
    user = models.CharField(max_length=64, default = None)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    verification_token_expires = models.DateTimeField(null=True, blank=True)