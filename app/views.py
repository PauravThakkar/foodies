from cart.cart import Cart
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse
from django.views import View
from paypal.standard.forms import PayPalPaymentsForm

from Foodies.settings import PAYPAL_EMAIL
from .forms import FilterForm
from .forms import LoginForm
from .forms import ReviewForm, CustomerForm
from .forms import SignUpForm
from .models import *


@login_required(login_url='/login/')
def review_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    user_id = request.user.id
    user = get_object_or_404(Customer, pk=user_id)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user
            review.restaurant = restaurant
            review.save()

            return render(request, 'review_block.html',
                          {'restaurant_id': restaurant.id, 'message': 'Review Submitted Successfully'})
    else:
        reviews = Review.objects.filter(restaurant=restaurant)
        return render(request, 'review_block.html',
                      {'review_from': form, 'restaurant_id': restaurant_id, 'restaurant_name': restaurant.name,
                       'message': '', 'reviews': reviews})


@login_required(login_url='/login/')
def user_settings(request):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(username=request.user.username)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user_ptr=request.user)
    else:
        return redirect('/login')

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, request.FILES, instance=customer)
        if customer_form.is_valid():
            customer_form.save()
            return redirect('Settings')
    else:
        customer_form = CustomerForm(instance=customer)

    return render(request, 'user_settings.html', {
        'customer_form': customer_form,
        'customer': customer,
        'status': 'signedIn'
    })


@login_required(login_url='/login/')
def user_history(request):
    # Initialize visit count to 0
    visit_count = 0

    # Check if 'visit_count' is already stored in session
    if 'visit_count' in request.session:
        visit_count = request.session['visit_count']

    # Increment visit count
    visit_count += 1

    # Update session with new visit count
    request.session['visit_count'] = visit_count
    # Get the current user
    # user = Customer.objects.all()
    current_user = request.user

    # Filter orders made by the current user
    user_orders = Order.objects.filter(user=current_user)

    # Create a list to hold order details (restaurant name and order ID)
    order_details = []

    # Iterate through each order to extract restaurant name and order ID
    for order in user_orders.all():
        order_details.append((order.order_id, order.items.all(), order.total))

    # Pass the order details to the template for rendering
    return render(request, 'user_history.html', {'order_details': order_details, 'visit_count': visit_count, 'status': 'signedIn'})


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
        next = '/home/'

        if form.is_valid():
            myuser = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, myuser)

            return redirect(next)  # Redirect to home page after successful login
    else:
        message = 'Welcome to Foodies'
        if request.GET.get('error') is not None:
            message = 'Please sign in to continue'
        form = LoginForm()
    return render(request, 'sign_in.html', {'form': form, 'message': message})


@login_required(login_url='/login/')
def payment_successful(request):
    payer_id = request.GET.get('PayerID')
    price = 0.0
    items = set()

    for item in request.session['cart'].values():
        price += float(item['price']) * float(item['quantity'])
        items.add(MenuItem.objects.get(id=item['product_id']))

    order = Order.objects.create(
        payer_id=payer_id,
        user=request.user,
        total=price
    )
    order.items.set(items)

    order.save()

    request.session['cart'] = {}

    return render(request, 'payment_successful.html')


@login_required(login_url='/login/')
def payment_failed(request):
    return render(request, 'payment_failed.html')


@login_required(login_url='/login/')
def ask_money(request):
    if request.POST:
        price = 0.0

        for item in request.session['cart'].values():
            price += float(item['price']) * float(item['quantity'])

        paypal_dict = {
            "business": PAYPAL_EMAIL,
            "amount": price,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('payment_successful')),
            "cancel_return": request.build_absolute_uri(reverse('payment_failed')),
        }

        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)

        return render(request, "payments.html", {"form": form, 'cart': request.session['cart']})


def home(request):
    restaurants = Restaurant.objects.all()
    form = FilterForm()
    status = ''
    if request.user.is_authenticated:
        status = 'signedIn'
    if request.method == "POST":
        form = FilterForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['Search']
            Cuisince = form.cleaned_data['Cuisine']
            Ratings = form.cleaned_data['Ratings']
            if search != '':
                restaurants = restaurants.filter(name__icontains=search)
            restaurants = restaurants.filter(cuisines=Cuisince)
            restaurants = restaurants.filter(avg_ratings__gte=Ratings)
            return render(request, 'home.html', {'restaurants': restaurants, 'form': form, 'status': status})
    else:
        for restaurant in restaurants:
            print(restaurant.respicture.url)
        return render(request, 'home.html', {'restaurants': restaurants, 'form': form, 'status': status})


class GetOneMenuByIdView(View):
    def get_obj(self, id):
        status = ''
        try:
            obj = MenuItem.objects.get(id=id)
        except:
            raise ValueError(f"Menu item not exist with id: {id}")

        return obj

    def get(self, request, id):
        status = ''
        if self.request.user.is_authenticated:
            status = 'signedIn'
        menu_item_details = self.get_obj(id=id)
        context = {
            "menu_details": menu_item_details,
            'status': status
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

# @login_required(login_url="login/?error=true&next=/cart/cart_detail/")
def cart_add(request, id):
    cart = Cart(request)
    menu_item = MenuItem.objects.get(id=id)
    cart.add(product=menu_item)
    return redirect("cart_detail")


# @login_required(login_url='/login/')
def item_clear(request, id):
    cart = Cart(request)
    menu_item = MenuItem.objects.get(id=id)
    cart.remove(product=menu_item)
    return redirect("cart_detail")


# @login_required(login_url='/login/')
def item_increment(request, id):
    cart = Cart(request)
    menu_item = MenuItem.objects.get(id=id)
    cart.add(product=menu_item)
    return redirect("cart_detail")


# @login_required(login_url='/login/')
def item_decrement(request, id):
    cart = Cart(request)
    menu_item = MenuItem.objects.get(id=id)
    cart.decrement(product=menu_item)
    return redirect("cart_detail")


# @login_required(login_url='/login/')
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


# @login_required(login_url="/login/?error=true")
def cart_detail(request):
    status = ''
    if request.user.is_authenticated:
        status = 'signedIn'
    return render(request, "cart_details.html", {'status': status})
