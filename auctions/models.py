from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=None)
    categories = models.ManyToManyField(Category, blank=True, related_name="listings")
    image = models.URLField(blank=True)

    def __str__(self):
        return f"{self.id}: {self.title}"


# class Bid(models.Model):
# class Comment(models.Model):
