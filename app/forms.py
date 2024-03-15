from django import forms

from app.models import Review
from app.models import UserProfile


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


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile

        fields = ('Name','profile_picture','e-mail','bio', 'favorite_food', 'favorite_restaurant',)

        fields = ('bio', 'favorite_food', 'favorite_restaurant', 'profile_picture',)

