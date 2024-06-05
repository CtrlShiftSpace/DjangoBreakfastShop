from rest_framework import serializers
from django.contrib.auth.models import User
from products.models import Categories, Products, Additions, AdditionCategories

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Categories.objects.all())
    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'content', 'is_active', 'categories']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        products = Products.objects.create(**validated_data)
        # 關聯欄位
        products.categories.add(*categories_data)
        return products

class AdditionCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionCategories
        fields = ['id', 'name', 'is_multiple', 'is_active']

class AdditionSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Products.objects.all())
    addition_categories = serializers.PrimaryKeyRelatedField(queryset=AdditionCategories.objects.all())
    class Meta:
        model = Additions
        fields = ['id', 'name', 'price', 'is_active', 'products', 'addition_categories']

