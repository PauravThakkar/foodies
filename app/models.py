import uuid

from django.contrib.auth.models import User
from django.db import models


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
    profile_picture = models.ImageField(upload_to='foodies/app/static/images/profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    review = models.ForeignKey("Review", on_delete=models.CASCADE, blank=True, null=True)

    image = models.ImageField(upload_to='products/')
    price = models.FloatField()

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    type_choices = [('1', 'Indian'),
                    ('2', 'Mexican'),
                    ('3', 'Italian')]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)
    type = models.CharField(choices=type_choices, default='1', max_length=2)
    menus = models.ManyToManyField(MenuItem, null=True, blank=True)
    review = models.ForeignKey("Review", on_delete = models.CASCADE, null = True, blank = True)

    def __str__(self):
        return self.name


class CartMenu(models.Model):
    menu = models.ForeignKey(MenuItem, on_delete = models.CASCADE, null = True, blank = True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.menu.name
    
    def get_total_price(self):
        return self.menu.price * self.quantity
    
    
    
class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    resturant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, null = True, blank = True)
    cartmenu = models.ManyToManyField(CartMenu, blank=True)
    
    
    def get_total_price(self):
        total_price  = 0
        for item in self.cartmenu.all():
            total_price += item.get_total_price()
            
        print(total_price, "-------") 
        return total_price
    
        

    def __str__(self):
        
        self.get_total_price()
        
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
    # restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=False)

    user = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)

    # rating given to the restaurant
    ratings = models.IntegerField(default=0, choices=RATINGS_RANGE)

    # comment associated with the review
    comment = models.TextField(blank=True, null=True, help_text='Add your comment')

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f" {self.user.username} ({self.ratings} stars)"
