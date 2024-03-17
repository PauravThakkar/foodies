from django.contrib import admin
from .models import *



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

@admin.register(MeniItem)
class MeniItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'review']

@admin.register(Restuarant)
class RestuarantAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'phone_number']