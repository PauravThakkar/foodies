from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import *


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['ratings', 'comment']
        widgets = {
            'ratings': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})
        }
        labels = {
            'ratings': 'Ratings',
            'comment': 'Comment',
        }


class SignUpForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'email', 'date_of_birth', 'contact_number']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label="User Name")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('bio', 'favorite_food', 'favorite_restaurant', 'profile_picture')


# class FilterForm(forms.ModelForm):
#     class Meta:
#         model = Restaurant
#         Search = forms.CharField()
#         fields = ['type', 'Search']
#         labels = {
#             'type': 'Cuisine'
#         }
#         widgets = {
#             'type': forms.Select(attrs={'class': 'cuisine_selection'})
#         }


class FilterForm(forms.Form):
    Cuisines = Restaurant.objects.all()
    choices = [('1', 'Indian'), ('2', 'Mexican'), ('3', 'Italian')]
    Search = forms.CharField(label='Search', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Cuisine = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class': 'form-select'}))
    ratings_choice = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    Ratings = forms.ChoiceField(
        widget=forms.NumberInput(attrs={'type': 'range', 'class': 'form-range', 'min': '1', 'max': '5'}))


class CustomerForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    date_of_birth = forms.DateField(label='Date of Birth')

    class Meta:
        model = Customer
        fields = ('date_of_birth', 'contact_number', 'profile_picture')
