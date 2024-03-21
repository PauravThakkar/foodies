from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    favorite_food = models.CharField(max_length=100, blank=True)
    favorite_restaurant = models.CharField(max_length=100, blank=True)

    # additional fields for user settings will be updated as per requirements

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    # Short title of the comment
    title = models.CharField(max_length=100)
    # Detailed comment
    details = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Customer(User):
    date_of_birth = models.DateField(null=True, blank=True, default=None)
    contact_number = models.CharField(max_length=15, null=True, blank=True, default=None)
    def __str__(self):
       return self.username


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)

    menus = models.ManyToManyField(MenuItem, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.order_id}"


class Review(models.Model):
    RATINGS_RANGE = (
        (1, 'Poor'),
        (2, 'Bad'),
        (3, 'Mediocre'),
        (4, 'Good'),
        (5, 'Excellent'),
    )

    # timestamp to track when the review was given
    timestamp = models.DateTimeField(auto_now_add=True)

    # reference of the restaurant the review was given to
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    # rating given to the restaurant
    ratings = models.IntegerField(default=0, choices=RATINGS_RANGE)

    # comment associated with the review
    comment = models.TextField(blank=True, null=True, help_text='Add your comment')

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Review for {self.restaurant} by {self.user.username} ({self.ratings} stars)"


from django.db import models

class Cuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cuisines = models.ManyToManyField(Cuisine)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


