from django.shortcuts import render,redirect
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
import json
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from products.models import CompanyProducts
from django.http import HttpResponse
from django.urls import reverse_lazy


class OnlyCustomer(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        tenant_name = kwargs.get('tenant_name') or request.path.strip('/').split('/')[0]
        if request.user.is_authenticated and request.user.username.lower() == tenant_name.lower():
            return redirect(f'/{tenant_name}/')
        return super().dispatch(request, *args, **kwargs)

    

class AddCart(LoginRequiredMixin,OnlyCustomer,View):
    def dispatch(self, request, *args, **kwargs):
        cur_val = request.COOKIES.get('cart')
        if cur_val:
            try:
                # Deserialize the cookie value to a Python list
                cart_items = json.loads(cur_val)
            except json.JSONDecodeError:
                cart_items = []  # Initialize an empty cart if decoding fails
        else:
            cart_items = []  # Initialize an empty cart if no cookie exists

        # Update the cart items
        pk = kwargs.get('pk')  # Get the product ID from the URL
        
        cart_items.append(pk)  # Add the product ID to the cart

        # Serialize the updated cart and set it in the cookie
        response = HttpResponseRedirect('/')  # Redirect to the home page or another route
        response.set_cookie('cart', json.dumps(cart_items), max_age=3600)  # Save as JSON in the cookie
        return response
class AllProductCart(OnlyCustomer,TemplateView):
    template_name="cart/allcart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Decode the cart cookie (default to an empty list if no cookie exists)
        cart = self.request.COOKIES.get('cart', '[]')
        cart_ids = json.loads(cart)  # Decode cart cookie into a list of IDs
        # Fetch all products matching the IDs in the cart
        context['products'] = CompanyProducts.objects.filter(pk__in=cart_ids)
        return context

class delete_cart(View):
    suceess_url=reverse_lazy('product:allproducts')
    def dispatch(self, request, *args, **kwargs):
        # Create a redirect response
        response = HttpResponseRedirect(reverse_lazy('product:allproducts'))
        # Delete the 'cart' cookie
        response.delete_cookie('cart')
        return response