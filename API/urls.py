# api/urls.py
from django.urls import path
from .views import list_products, create_product, update_product, destroy_product, register,login,list_orders,create_order
from Front.views import index, documentacion


urlpatterns = [
    path('', index,name='pagina_principal'),
    path('documentacion/',documentacion,name='documentacion'),
    path('register/', register,name='register'),
    path('login/',login,name='login'),
    path('products/', list_products, name='list_products'),
    path('products/create/', create_product, name='create_product'),
    path('products/<pk>/update/', update_product, name='update_product'),
    path('products/<pk>/delete/', destroy_product, name='destroy_product'),
    path('products/orders/list/', list_orders, name='list_orders'),
    path('products/orders/create/', create_order, name='create_order'),
]