"""
URL configuration for Foodies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from .views import *

urlpatterns = [
    path('ratings/<int:restaurant_id>/', temp_review_view, name='ratings'),
    path('settings/', user_settings, name='Settings'),
    path('history/', user_history,name='user_history'),
    path('', sign_up, name='sign_up'),
    path('signup/', sign_up, name='sign_up'),
    path('home/', home, name='home'),
    path('login/', logedIn, name='login'),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('payment_successful/', payment_successful, name='payment_successful'),
    path('payment/', ask_money, name='payment'),
    path('accounts/', include('django.contrib.auth.urls')),
]
