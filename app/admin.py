from django.contrib import admin
from .models import *
from .models import Customer, UserProfile, Review, Restaurant

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id']


# Register your models here.
admin.site.register(Customer)

# Registering model for User Setting
admin.site.register(UserProfile)

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(MenuItem)

