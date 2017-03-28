from .models import Restaurant
from django import forms

class PollsRestaurant(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'restaurantName',
            'restaurantAddress',
            'image'
        ]