from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls.base import reverse
from paypal.standard.forms import PayPalPaymentsForm

from .forms import LoginForm
from .forms import ReviewForm, UserProfileForm
from .forms import SignUpForm
from .models import Restaurant
from .models import UserProfile

from django.shortcuts import render, get_object_or_404
from .models import Restaurant


def restaurant_list(request):
    restaurants = Restaurant.objects.all()

    search_value = "test"
    # Filter according to name in search
    filtered_restaurants = restaurants.objects.filter(name__icontains=search_value)

    # Filter according to ratings
    rating_value = 1
    filtered_restaurants = filtered_restaurants.objects.filter(rating__gte=rating_value)

    # Filter according to Cuisine
    cuisine = []
    filtered_restaurants = filtered_restaurants.objects.filter(cuisine__in=cuisine).all()

    # TODO return proper template
    return ''


def temp_review_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    # TODO: Fetch user form request and add its ID
    user = get_object_or_404(User, pk=1)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.restaurant = restaurant
            review.user = user
            review.save()
            return render(request, 'review_block.html',
                          {'restaurant_id': restaurant_id, 'message': 'Review Submitted Successfully'})
    else:
        return render(request, 'review_block.html',
                      {'review_from': form, 'restaurant_id': restaurant_id, 'restaurant_name': restaurant.name,
                       'message': ''})

@login_required(login_url='/login/')
def user_settings(request):
    user = 1
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    if request.method == 'POST':
        password_form = PasswordChangeForm(user, request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if password_form.is_valid() and profile_form.is_valid():
            password_form.save()
            profile_form.save()
            return redirect('user_settings')
    else:
        password_form = PasswordChangeForm(user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'user_settings.html',
                  {'password_form': password_form, 'profile_form': profile_form, 'user_profile': user_profile})


# Define a class to hold static order data
class StaticOrder:
    def __init__(self, order_id, restaurant_name, item_name, cuisine_price, cuisine_quantity,totalprice):
        self.order_id = order_id
        self.restaurant_name = restaurant_name
        self.item_name = item_name
        self.cuisine_price = cuisine_price
        self.quantity = cuisine_quantity
        self.totalprice = totalprice

def user_history(request):
    # Get the current user
    user_id = 1

    # Static order data
    static_orders = [
        StaticOrder(order_id=1, restaurant_name='Restaurant A', item_name='Italian',cuisine_price='$20',cuisine_quantity='1',totalprice='40'),
        StaticOrder(order_id=2, restaurant_name='Restaurant B', item_name='Mexican',cuisine_price='$50',cuisine_quantity='2',totalprice='100'),
        StaticOrder(order_id=3, restaurant_name='Restaurant C', item_name='Indian',cuisine_price='$15',cuisine_quantity='1',totalprice='15'),
        StaticOrder(order_id=4, restaurant_name='Restaurant C', item_name='Indian', cuisine_price='$15', cuisine_quantity='1', totalprice='15'),
        # Add more static orders as needed
    ]

    # Filter orders made by the current user
    user_orders = [order for order in static_orders]

    # Create a list to hold order details (restaurant name and order ID)
    order_details = []

    # Iterate through each order to extract restaurant name and order ID
    for order in user_orders:
        order_details.append((order.order_id, order.restaurant_name, order.item_name,order.cuisine_price,order.quantity,order.totalprice))

    # Pass the order details to the template for rendering
    return render(request, 'user_history.html', {'order_details': order_details})
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful sign-up
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Process login data
            # Example: Check credentials and log the user in
            return redirect('home')  # Redirect to home page after successful login
    else:
        form = LoginForm()
    return render(request, 'sign_in.html', {'form': form})


def payment_successful(request):
    return render(request, 'payment_sucessful.html')


def ask_money(request):
    # What you want the button to do.
    paypal_dict = {
        "business": "sb-pkdqf30042076@business.example.com",
        "amount": "1.00",
        "item_name": "SOME ITEM",
        "invoice": "ORDER ID",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment_successful')),
        # TODO: Add cancel return URL
        "cancel_return": request.build_absolute_uri(reverse('payment_successful')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, "payments.html", {"form": form})


def home(request):
    restaurants = Restaurant.objects.all()
    print(restaurants)
    return render(request, 'home.html', {'restaurants': restaurants})

