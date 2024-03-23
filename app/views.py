from cart.cart import Cart
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views import View
from paypal.standard.forms import PayPalPaymentsForm

from .forms import FilterForm
from .forms import LoginForm
from .forms import ReviewForm, CustomerForm
from .forms import SignUpForm
from .models import Customer
from .models import MenuItem
from .models import Order
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
    
    # Need login required decorator for request.user otherwise getting error 
    # user = request.user
    
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user
            review.save()
            
            restaurant.review = review
            restaurant.save()
           
            
            return render(request, 'review_block.html',
                          {'restaurant_id': restaurant_id, 'message': 'Review Submitted Successfully'})
    else:
        return render(request, 'review_block.html',
                      {'review_from': form, 'restaurant_id': restaurant_id, 'restaurant_name': restaurant.name,
                       'message': ''})


@login_required(login_url='/login/')
def user_settings(request):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(username=request.user.username)
        except Customer.DoesNotExist:
            # Create a new Customer instance if it doesn't exist
            customer = Customer.objects.create(user_ptr=request.user)
    else:
        # Create a temporary anonymous user for development
        return redirect('/login')

    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        customer_form = CustomerForm(request.POST, request.FILES, instance=customer)

        if password_form.is_valid() and customer_form.is_valid():
            password_form.save()
            customer_form.save()
            return redirect('user_settings')
    else:
        password_form = PasswordChangeForm(request.user)
        customer_form = CustomerForm(instance=customer)

    return render(request, 'user_settings.html', {
        'password_form': password_form,
        'customer_form': customer_form,
        'customer': customer,
    })


# Define a class to hold static order data
class StaticOrder:
    def __init__(self, order_id, restaurant_name, item_name, cuisine_price, cuisine_quantity, totalprice):
        self.order_id = order_id
        self.restaurant_name = restaurant_name
        self.item_name = item_name
        self.cuisine_price = cuisine_price
        self.quantity = cuisine_quantity
        self.totalprice = totalprice


def user_history(request):
    # Get the current user
    user = User.objects.get()

    # Static order data
    static_orders = [
        StaticOrder(order_id=1, restaurant_name='Restaurant A', item_name='Italian', cuisine_price='$20',
                    cuisine_quantity='1', totalprice='40'),
        StaticOrder(order_id=2, restaurant_name='Restaurant B', item_name='Mexican', cuisine_price='$50',
                    cuisine_quantity='2', totalprice='100'),
        StaticOrder(order_id=3, restaurant_name='Restaurant C', item_name='Indian', cuisine_price='$15',
                    cuisine_quantity='1', totalprice='15'),
        StaticOrder(order_id=4, restaurant_name='Restaurant C', item_name='Indian', cuisine_price='$15',
                    cuisine_quantity='1', totalprice='15'),
        # Add more static orders as needed
    ]

    # Filter orders made by the current user
    user_orders = [order for order in static_orders]

    # Create a list to hold order details (restaurant name and order ID)
    order_details = []

    # Iterate through each order to extract restaurant name and order ID
    for order in user_orders:
        order_details.append((order.order_id, order.restaurant_name, order.item_name, order.cuisine_price,
                              order.quantity, order.totalprice))

    # Pass the order details to the template for rendering
    return render(request, 'user_history.html', {'order_details': order_details})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app_login')  # Redirect to login page after successful sign-up
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def app_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            myuser = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, myuser)
            return redirect('Settings')  # Redirect to home page after successful login
    else:
        form = LoginForm()
    return render(request, 'sign_in.html', {'form': form})


def payment_successful(request):
    # TODO: Add Payer ID from URL to Database, along with the order details/User ID
    # EX URL: http://localhost:8000/payment_successful/?PayerID=VUZ7HNUFNA8Y6
    return render(request, 'payment_successful.html')


def payment_failed(request):
    return render(request, 'payment_failed.html')


def filter_temp(req):
    return render(req, 'filters.html', {'form': FilterForm})


def home(request):
    return render(request, 'home.html')


def ask_money(request):
    # TODO: Fetch order details from the database
    order_details = Order.objects.all().first()

    # TODO: set price from order object
    price = 15.00
    item_name = "Manchurian"

    paypal_dict = {
        "business": "sb-pkdqf30042076@business.example.com",
        "amount": price,
        "item_name": item_name,
        "invoice": order_details.order_id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment_successful')),
        # TODO: Add cancel return URL
        "cancel_return": request.build_absolute_uri(reverse('payment_failed')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, "payments.html", {"form": form})


class GetOneMenuByIdView(View):

    def get_obj(self, id):

        try:
            obj = MenuItem.objects.get(id=id)
        except:
            raise ValueError(f"Menu item not exist with id: {id}")

        return obj

    def get(self, request, id):

        menu_item_details = self.get_obj(id=id)

        context = {
            "menu_details": menu_item_details
        }

        return render(request, "one_menu.html", context=context)


class GetOneRestaurantByIdView(View):

    def get_obj(self, id):

        try:
            obj = Restaurant.objects.get(id=id)
        except:
            raise ValueError(f"Restaurant not exist with id: {id}")

        return obj

    def get(self, request, id):

        restaurant_details = self.get_obj(id=id)

       
        context = {
            'restaurant_details': restaurant_details,
           
        }

        return render(request, "one_restaurant.html", context=context)


def homeview(request):
    return render(request, "home.html")


# cart

# @login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    menu_item = MenuItem.objects.get(id=id)
    cart.add(product=menu_item)
    return redirect("cart_detail")


# @login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    menu_item = MenuItem.objects.get(id=id)
    cart.remove(product=menu_item)
    return redirect("cart_detail")


# @login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    menu_item = MenuItem.objects.get(id=id)
    cart.add(product=menu_item)
    return redirect("cart_detail")


# @login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    menu_item = MenuItem.objects.get(id=id)
    cart.decrement(product=menu_item)
    return redirect("cart_detail")


# @login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


# @login_required(login_url="/users/login")
# def cart_detail(request):
#     return render(request, 'cart/cart_detail.html')


# @login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, "cart_details.html")
