from django.urls import path
from .views import AuthLoginView, UserView, ProductView, CategoryView, AuthSignUpView, AuthCheckToken, OrderView


urlpatterns = [
    path('users/', UserView.as_view(), name='user_list'),
    path('users/<int:id>', UserView.as_view(), name='user_process'),
    path('products/', ProductView.as_view(), name='product_list'),
    path('products/<int:id>', ProductView.as_view(), name='product_process'),
    path('categories/', CategoryView.as_view(), name='category_list'),
    path('auth/login/', AuthLoginView.as_view(), name='user_login'),
    path('auth/signup/', AuthSignUpView.as_view(), name='user_signup'),
    path('auth/check/', AuthCheckToken.as_view(), name='user_checkToken'),
    path('orders/', OrderView.as_view(), name='order_view'),
    path('orders/<int:id>', OrderView.as_view(), name='order_process'),
]
