import django.contrib.auth
from django.contrib.auth.views import LoginView
from django.urls import include
from django.urls import path
from django.urls import include, path
from django.views.generic import RedirectView

from . import views
from .views import *
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('ratings/<int:restaurant_id>/', review_view, name='ratings'),
    path('settings/', user_settings, name='Settings'),
    path('history/', user_history, name='user_history'),
    path('', RedirectView.as_view(url='/home/'), name='home'),
    path('signup/', sign_up, name='sign_up'),
    path('home/', home, name='home'),
    path('login/', app_login, name='app_login'),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('payment_successful/', payment_successful, name='payment_successful'),
    path('payment_failed/', payment_failed, name='payment_failed'),
    path('checkout/', ask_money, name='checkout'),
    path('payment_successful/', payment_successful, name='payment_successful'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('menu/<int:id>/', views.GetOneMenuByIdView.as_view(), name="get_one_menu"),
    path('restaurant/<int:id>/', views.GetOneRestaurantByIdView.as_view(), name="get_one_restaurant"),

    # Cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset_password_confirm/<uidb64>/<token>/', PasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-done', PasswordResetDoneView, name='password_reset_done')
]
