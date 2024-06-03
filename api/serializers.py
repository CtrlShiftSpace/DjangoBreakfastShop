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
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Categories.objects.all())
    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'content', 'is_active', 'categories']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        products = Products.objects.create(**validated_data)
        for category_data in categories_data:
            if type(category_data) is Categories:
                category_id = category_data.id
            else:
                category_id = category_data
            category = Categories.objects.get(id=category_id)
            products.categories.add(category)

        return products

class AdditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Additions
        fields = ['id', 'name', 'price', 'is_active']

