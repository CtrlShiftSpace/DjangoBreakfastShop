from rest_framework import serializers
from django.contrib.auth.models import User
from products.models import Categories, Products, Additions

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name', 'is_active']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'content', 'is_active']

class AdditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Additions
        fields = ['id', 'name', 'price', 'is_active']

