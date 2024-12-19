
from rest_framework import serializers
from .models import  Product, Order, ProductsOrders
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ProductsOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsOrders
        fields = '__all__'