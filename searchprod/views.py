from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
# Create your views here.
from django.contrib import messages
from products.models import CompanyProducts, ProductRating
import bleach
from .utils import search_with_fuzzy
from django.views.generic import ListView
from django.views import View
from cart.views import OnlyCustomer
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RatingForm
class SearchListView(ListView):
    model = CompanyProducts  # Your model
    template_name = 'products/products.html'  # Template to render
    context_object_name = 'products'  # Name used to access objects in the template

    # Override the get_queryset method for fuzzy search
    def get_queryset(self):
        # Get and sanitize the user input
        user_input = self.request.GET.get('q', '').strip()
        user_input = bleach.clean(user_input)
        sort_input=self.request.GET.get('sort' ,'').strip()
        sort_input = bleach.clean(sort_input)
    # Fetch product names for fuzzy matching
        reference_list = CompanyProducts.objects.all().values_list('product_name', flat=True)

    # Perform fuzzy matching
        fuzzy_results = search_with_fuzzy(user_input, reference_list)

    # Extract only the product names from fuzzy_results
        high_quality_match_names = [result[0] for result in fuzzy_results]
        if high_quality_match_names:
            products=CompanyProducts.objects.filter(product_name__in=high_quality_match_names)
        else:
            products=CompanyProducts.objects.all()
        sort_input=bleach.clean(sort_input)
        if sort_input == "name_asc":
            products=products.order_by('product_name')
        elif sort_input == 'name_desc':
            products=products.order_by('-product_name')
        elif sort_input == 'price_asc':
            products=sorted(products, key=lambda product: product.CountDiscount)
        elif sort_input == 'price_desc':
            products=sorted(products, key=lambda product: product.CountDiscount, reverse=True)
        elif sort_input == "rating":
            products=sorted(products, key=lambda product: product.Avrage_Rating, reverse=True)
        if products:
            return products
        return HttpResponse('no products available')
    
class RatingView(LoginRequiredMixin,OnlyCustomer,View):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        product = get_object_or_404(CompanyProducts, pk=pk)
        form = RatingForm()
        return render(request, 'searchprod/rating.html', {'form': form, 'product': product})

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        product = get_object_or_404(CompanyProducts, pk=pk)
        form = RatingForm(request.POST)

        if form.is_valid():
            rating = form.cleaned_data['rating']
            ProductRating.objects.create(product_rating=rating, product=product)
            messages.success(request, 'Rating successfully submitted!')
            return redirect('/')
        else:
            messages.error(request, 'Invalid input. Please provide a valid rating.')
            return render(request, 'searchprod/rating.html', {'form': form, 'product': product})