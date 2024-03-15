from .forms import ReviewForm
from .models import Restaurant, User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import SignUpForm
from .forms import LoginForm
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
            return render(request, 'review_block.html', {'restaurant_id': restaurant_id, 'message': 'Review Submitted Successfully'})
    else:
        return render(request, 'review_block.html', {'review_from': form, 'restaurant_id': restaurant_id, 'restaurant_name': restaurant.name, 'message': ''})


@login_required
def user_settings(request):
    user = request.user
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    return render(request, 'user_settings.html', {'user': user, 'user_profile': user_profile})




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
