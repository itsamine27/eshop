from django.urls import path
from .views import AddCart,AllProductCart,delete_cart
urlpatterns=[
    path('addcart/<int:pk>', AddCart.as_view(), name='addtocart'),
    path('mycart/', AllProductCart.as_view(), name="allprocart"),
    path('clearcart/', delete_cart.as_view(), name="clearcart"),
    
]