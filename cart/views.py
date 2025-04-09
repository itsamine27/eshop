from django.shortcuts import render, redirect
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
import json
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from products.models import CompanyProducts
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse


class OnlyCustomer(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        tenant_name = kwargs.get('tenant_name') or request.path.strip('/').split('/')[0]
        if not request.user.is_authenticated or request.user.username.lower() != tenant_name.lower():
            return HttpResponse("Forbidden", status=403)
        return super().dispatch(request, *args, **kwargs)


class AddCart(LoginRequiredMixin, OnlyCustomer, View):
    def dispatch(self, request, *args, **kwargs):
        cur_val = request.COOKIES.get('cart')
        try:
            cart_items = json.loads(cur_val) if cur_val else []
        except json.JSONDecodeError:
            cart_items = []

        pk = kwargs.get('pk')
        if pk:
            cart_items.append(pk)

        tenant_name = kwargs.get('tenant_name')
        response = HttpResponseRedirect(reverse('product:allproducts', kwargs={'tenant_name': tenant_name}))
        response.set_cookie('cart', json.dumps(cart_items), max_age=3600)
        return response


class AllProductCart( TemplateView):
    template_name = "cart/allcart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.COOKIES.get('cart', '[]')
        try:
            cart_ids = json.loads(cart)
        except json.JSONDecodeError:
            cart_ids = []
        context['products'] = CompanyProducts.objects.filter(pk__in=cart_ids)
        return context


class DeleteCart(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        tenant_name = kwargs.get('tenant_name')
        response = HttpResponseRedirect(reverse_lazy('product:allproducts', kwargs={'tenant_name': tenant_name}))
        response.delete_cookie('cart')
        return response
