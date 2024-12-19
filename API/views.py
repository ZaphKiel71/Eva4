# api/views.py
from rest_framework.response import Response 
from rest_framework.authtoken.models import  Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Product, User
from django.shortcuts import get_object_or_404

from .serializers import ProductSerializer, UserSerializer


@api_view(['POST'])
def register(request):
    try:
        serializer = UserSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            user = User.objects.get(username=serializer.data['username'])
            user.set_password(serializer.data['password'])
            user.save()

            token = Token.objects.create(user = user)
            print(token)
            return Response({'token': token.key,  "user":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error {e}")
        return Response(e, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login(request):
    
    user = get_object_or_404(User,username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"error":"Invalid Password"}, status= status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    
    return Response({"token": token.key}, status =  status.HTTP_200_OK)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):

    # Obtenemos el usuario a partir del username​

    user = get_object_or_404(User, username=request.user.username)

    # Serializamos el objeto del usuario​

    user_serialized = UserSerializer(user)

    data = user_serialized.data

    data.pop('password', None) #eliminamos el password para que no se visualice​

    

    return Response({"message": "Usuario autorizado", "user": data}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def destroy_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)