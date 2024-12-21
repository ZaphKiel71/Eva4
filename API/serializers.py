
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



class ProductsOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsOrders
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = ProductsOrdersSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user', 'products']

    def create(self, validated_data):
        user = validated_data.pop('user')  # Extrae el usuario
        products_data = validated_data.pop('products')
        order = Order.objects.create(user=user, **validated_data)  # Asigna el usuario aquí
        
        total_price = 0  # Inicializa el precio total

        for product_data in products_data:
            product = Product.objects.get(id=product_data['product'])  # Obtiene el producto
            quantity = product_data['quantity']
            price = product.price  # Precio unitario del producto
            total_price += price * quantity  
      
            ProductsOrders.objects.create(order=order, product=product, quantity=quantity, price=price)

       
        return order