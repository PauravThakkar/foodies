
from django.urls import include
from django.urls import path
from . import views

from .views import *

urlpatterns = [
    path('ratings/<int:restaurant_id>/', temp_review_view, name='ratings'),
    path('settings/', user_settings, name='Settings'),
    path('history/', user_history,name='user_history'),
    path('', sign_up, name='sign_up'),
    path('signup/', sign_up, name='sign_up'),
    path('home/', home, name='home'),
    path('login/', login, name='login'),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('payment_successful/', payment_successful, name='payment_successful'),
    path('payment_failed/', payment_failed, name='payment_failed'),
    path('payment/', ask_money, name='payment'),
    path('payment_successful/', payment_successful, name='payment_successful'),
    path('temp_filter/', filter_temp, name='temp_filter'),
    
    path('menu/<int:id>/', views.GetOneMenuByIdView.as_view(), name = "get_one_menu"),
    path('restaurant/<int:id>/', views.GetOneRestaurantByIdView.as_view(), name = "get_one_restaurant"),
    
    
    # Cart 
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

]
