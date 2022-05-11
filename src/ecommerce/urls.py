from django.urls import path
from .views import UserView, ProductView, CategoryView


urlpatterns = [
    path('users/', UserView.as_view(), name='user_list'),
    path('users/<int:id>', UserView.as_view(), name='user_process'),
    path('products/', ProductView.as_view(), name='product_list'),
    path('products/<int:id>', ProductView.as_view(), name='product_process'),
    path('categories/', CategoryView.as_view(), name='category_list'),
]
