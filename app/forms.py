from django import forms
from django.contrib.auth.forms import UserCreationForm

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
        fields = ('bio', 'favorite_food', 'favorite_restaurant', 'profile_picture',)

class CustomerForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    date_of_birth = forms.DateField(label='Date of Birth')

    class Meta:
        model = Customer
        fields = ('date_of_birth', 'contact_number', 'profile_picture')