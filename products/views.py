from .models import CompanyProducts,CompanyProductsImages
from django.views.generic import CreateView,ListView, UpdateView, DeleteView
from .forms import ProductForm,CompanyProductsImagesFormSet
from base.models import CompanyModel
from django.contrib.auth.mixins import AccessMixin,LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class OnlyOwner(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        host=request.get_host()
        if  not request.user.is_authenticated or request.user.username.lower() not in host:
            
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(ratelimit(key='ip', rate='7/m', block=True), name='dispatch')
class AddProduct(LoginRequiredMixin,OnlyOwner,CreateView):
    form_class=ProductForm
    model=CompanyProducts
    template_name="products/addproduct.html"
    success_url="allproducts"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset']=CompanyProductsImagesFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset']=CompanyProductsImagesFormSet()
        return context
    def form_valid(self, form):
        form.instance.company=CompanyModel.objects.CompanyUser(self.request.user.username)
        context=self.get_context_data()
        formset=context['formset']
        if formset.is_valid():
            self.objects=form.save()
            formset.instance=self.objects
            formset.save()
            return redirect('/')
        else:
            return super().form_invalid(form)
        

class UpdateProduct(OnlyOwner, UpdateView):
    model = CompanyProducts
    form_class = ProductForm
    template_name = 'products/updateproduct.html'
    success_url=reverse_lazy('product:allproducts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product=CompanyProductsImages.objects.filter(product=self.object)
        existing_fields=product.count()
        extra_fields=(3-existing_fields)
        if self.request.method == 'POST':
            context['image_formset'] = CompanyProductsImagesFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['image_formset'] = CompanyProductsImagesFormSet(instance=self.object)
        context['image_formset'].extra=extra_fields
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        if image_formset.is_valid():
            form.save()
            image_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
class DeleteProduct(OnlyOwner,DeleteView):
    model=CompanyProducts
    template_name="products/confirm_delete.html"
    success_url=reverse_lazy('product:allproducts')



class AllProducts(ListView):
    template_name="products/products.html"
    model=CompanyProducts
    context_object_name = 'products'
    paginate_by=5
    
    def dispatch(self, request, *args, **kwargs):
        response=super().dispatch(request, *args, **kwargs)
        
        cart_cookie = request.COOKIES.get('cart')
        if not cart_cookie:  # Check if the 'cart' cookie is missing
            response.set_cookie('cart', '[]', max_age=3600)  # Set an empty 'cart' cookie
        return response

