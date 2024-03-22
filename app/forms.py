from django import forms
from app.models import Review
from .models import Customer, UserProfile
from django.contrib.auth.forms import PasswordChangeForm


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


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'password', 'email', 'date_of_birth', 'contact_number']
        widgets = {
            'password': forms.PasswordInput(),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
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


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Old Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'Confirm New Password'
