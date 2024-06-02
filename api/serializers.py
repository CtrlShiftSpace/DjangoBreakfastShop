from rest_framework import serializers
from django.contrib.auth.models import User
from products.models import Products, Additions

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Products
        fields = ['name', 'price', 'stock']

class AdditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Additions
        fields = ['name', 'price', 'is_active']

