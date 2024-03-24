import re
from datetime import date

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from app.models import *
from app.models import Review
from .models import Customer, UserProfile


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError("Password must contain at least one special character.")
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password2')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError("Password must contain at least one special character.")
        return password

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not contact_number.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        if len(contact_number) != 10:  # Adjust the length as per your requirements
            raise forms.ValidationError("Contact number must be 10 digits long.")
        return contact_number

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob and dob >= date.today():
            raise ValidationError("The date of birth must be in the past.")
        return dob

    class Meta:
        model = Customer
        fields = ['username', 'password1', 'password2', 'email', 'date_of_birth', 'contact_number', 'profile_picture']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'username-class', 'placeholder': 'Username', 'style': 'border: 1px solid #000'}),
            'password1': forms.PasswordInput(
                attrs={'class': 'password-class', 'placeholder': 'Password', 'style': 'border: 1px solid #000'},
            ),
            'password2': forms.PasswordInput(
                attrs={'class': 'password-class', 'placeholder': 'Password', 'style': 'border: 1px solid #000'}),
            'email': forms.EmailInput(
                attrs={'class': 'email-class', 'placeholder': 'Email', 'style': 'border: 1px solid #000'}),
            'date_of_birth': forms.DateInput(
                attrs={'class': 'dob-class', 'type': 'date', 'placeholder': 'Date of Birth',
                       'style': 'border: 1px solid #000'}),
            'contact_number': forms.TextInput(
                attrs={'class': 'contact-class', 'placeholder': 'Contact Number', 'style': 'border: 1px solid #000'}),
            'profile_picture': forms.FileInput(attrs={'class': 'pro-class', 'placeholder': 'Upload your image',
                                                      'style': 'margin-left:15px ; padding:10px'})
        }
        help_texts = {
            'username': None,
        },


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'email-class', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password-class', 'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''


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
    Cuisines = Cuisine.objects.values_list('id', 'name').all()
    Search = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Cuisine = forms.ChoiceField(required=False, choices=Cuisines, widget=forms.Select(attrs={'class': 'form-select'}))
    ratings_choice = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
    Ratings = forms.ChoiceField(choices=ratings_choice, widget=forms.NumberInput(
        attrs={'type': 'range', 'class': 'form-range', 'min': '1', 'max': '5'}))


class CustomerForm(forms.ModelForm):
    date_of_birth = forms.DateField(label='Date of Birth')

    class Meta:
        model = Customer
        fields = ('date_of_birth', 'contact_number', 'profile_picture')


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Old Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm New Password'
