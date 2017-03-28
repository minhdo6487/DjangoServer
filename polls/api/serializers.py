from rest_framework.serializers import ModelSerializer
#from rest_framework import serializers

from polls.models import Restaurant
from django import forms

class PollsSerializers(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'restaurantName',
            'restaurantAddress',
            'restaurantLatLng',
            'image',
            'user',
        ]

class PollsDetailSerializers(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'restaurantName',
            'restaurantAddress',
            'restaurantLatLng',
            'image'
        ]

class PollsCreateSerializers(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'restaurantName',
            'restaurantAddress',
            'restaurantLatLng',
            'image'
        ]
