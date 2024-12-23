
from rest_framework import serializers
from .models import  Product, Order, ProductsOrders
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class ProductsOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsOrders
        fields = ['product', 'quantity']

class ProductsOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsOrders
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = ProductsOrdersSerializer(many=True)

    class Meta:
        model = Order
        fields = ['products']  # No necesitas el campo 'username'

    def create(self, validated_data):
        products_data = validated_data.pop('products')  # Extrae los datos de productos
        
        # Obtén el usuario desde el contexto de la solicitud
        user = self.context['request'].user
        
        # Crea la orden
        order = Order.objects.create(user=user, **validated_data)

        for product_data in products_data:
            product = Product.objects.get(id=product_data['product'])  # Obtiene el producto
            ProductsOrders.objects.create(order=order, product=product, **product_data)

        return order