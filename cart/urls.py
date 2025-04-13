from django.urls import path
from .views import AddCart,AllProductCart,DeleteCart
app_name='cart'
urlpatterns=[
    path('addcart/<int:pk>/', AddCart.as_view(), name='addtocart'),
    path('mycart/', AllProductCart.as_view(), name="allprocart"),
    path('clearcart/', DeleteCart.as_view(), name="clearcart"),
    
]