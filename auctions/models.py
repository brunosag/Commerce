from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Listing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=None)
    categories = models.ManyToManyField(Category, blank=True, related_name="listings")
    image = models.URLField(blank=True)
    watchlisted = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="watchlist")
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} | {self.title}"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.id} | {self.user} on {self.listing.title}"


class Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    value = models.DecimalField(max_digits=9, decimal_places=2, default=None)

    def __str__(self):
        return f"{self.id} | ${self.value} on {self.listing.title}"
