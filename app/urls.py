from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/<int:id>/', views.GetOneRestaurantByIdView.as_view(), name = "get_one_restaurant"),
]