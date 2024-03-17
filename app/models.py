
from django.db import models
from django.contrib.auth.models import User
import uuid


class Order(models.Model):
    
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.order_id}"
    


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)
    comment = models.TextField()
    ratings = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"Review for {self.restaurant} by {self.user_name} ({self.rating} stars)"



class MeniItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete = models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.name
    


class Restuarant(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)

    menus = models.ManyToManyField(MeniItem, null=True, blank=True)


    def __str__(self):
        return self.name
