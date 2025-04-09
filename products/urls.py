from django.urls import path
from .views import AddProduct,AllProducts,UpdateProduct, DeleteProduct
app_name="product"
urlpatterns =[
    path('addproduct/', AddProduct.as_view(), name='product_creation'),
    path('updateproduct/<int:pk>/', UpdateProduct.as_view(), name='update_product'),
    path('DeleteProduct/<int:pk>/', DeleteProduct.as_view(), name='delete_product'),
    
    path('', AllProducts.as_view(), name="allproducts"),
]