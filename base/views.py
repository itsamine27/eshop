from django.shortcuts import render, redirect
from .forms import SignupUserForm, LogintUserForm, CompanyProfileForm,SearchCompany
from django.views.generic.edit import FormView
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
# Import our new utility function
from base.utils import build_tenant_url
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
import bleach
# ------------------------------------------------------------------------------
# Mixin to prevent authenticated users from accessing login/register pages.
# ------------------------------------------------------------------------------
class AnonymousRequiredMixin(AccessMixin):
    redirect_url = reverse_lazy('/')  # adjust to your desired URL for logged-in users

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)


# ------------------------------------------------------------------------------
# Mixin for optionally retrieving a "next" parameter.
#
# If a valid "next" parameter is passed (from POST or GET), it is returned.
# Otherwise, an empty string ("") is returned.
# (The individual views can then decide how to use—or ignore—the result.)
# ------------------------------------------------------------------------------
class SuccessUrlRedirectMixin:
    def get_success_url(self):
        next_param = (self.request.POST.get('next') or self.request.GET.get('next') or "").strip()
        next_param= bleach.clean(next_param)  # Strips harmful tags or scripts
        if next_param and url_has_allowed_host_and_scheme(
            url=next_param,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure()
        ):
            # If next_param does not start with a scheme, return it as-is; the view may build a full URL.
            if not (next_param.startswith("http://") or next_param.startswith("https://")):
                return next_param
            return next_param
        return ""  # no safe next URL provided


# ... (Mixin definitions remain the same)
@method_decorator(ratelimit(key='ip', rate='7/m', block=True, method="POST"), name='dispatch')
class Sign_Up_User(AnonymousRequiredMixin, SuccessUrlRedirectMixin, FormView):
    template_name = "base/register.html"
    form_class = SignupUserForm

    def form_valid(self, form):
        user = form.save()
        backends = get_backends()
        if backends:
            user.backend = f"{backends[0].__module__}.{backends[0].__class__.__name__}"
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, "You have successfully signed up!")
        
        
        central_host = f"{settings.BASE_DOMAIN}/"
        
        
        next_url = self.get_success_url()
        if next_url:
            if not (next_url.startswith("http://") or next_url.startswith("https://")):
                return redirect(build_tenant_url(next_url))
            return redirect(central_host+next_url)
        else:
            return redirect(reverse_lazy('create_company_profile'))
@method_decorator(ratelimit(key='ip', rate='7/m', block=True, method="POST"), name='dispatch')
class Log_In_User(AnonymousRequiredMixin, SuccessUrlRedirectMixin, FormView):
    template_name = 'base/login.html'
    form_class = LogintUserForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            next_url = self.get_success_url()
            if next_url:
                if not (next_url.startswith("http://") or next_url.startswith("https://")):
                    return redirect(build_tenant_url(next_url))
                return redirect(next_url)
            else:
                host = self.request.get_host()
                central_host = settings.BASE_DOMAIN
                if host == central_host:
                    return redirect(build_tenant_url(username))
                else:
                    return redirect(f"https://{central_host}/{host}/")
        else:
            messages.error(self.request, "User not found")
            return self.form_invalid(form)

# ------------------------------------------------------------------------------
# Logout View
# ------------------------------------------------------------------------------

class Log_Out_User(SuccessUrlRedirectMixin, View):
    def get(self, request):
        logout(request)
        url = self.get_success_url()
        if url:
            return redirect(f'https://{settings.BASE_DOMAIN}/{url}')
        else:
            return redirect('/')

# ------------------------------------------------------------------------------
# NewProfile View – for creating a company profile and then redirecting to the tenant.
# ------------------------------------------------------------------------------
class NewProfile(LoginRequiredMixin, FormView):
    form_class = CompanyProfileForm
    template_name = "base/profilecompany.html"

    def form_valid(self, form):
        try:
            company = form.save(commit=False)
            company.company = self.request.user
            company.save()
            # Build tenant URL using the username (assumes each tenant's domain is formed with username)
            username = self.request.user.username.lower()
            tenant_domain = f"https://{settings.BASE_DOMAIN}/{username}"
            return redirect(tenant_domain)
        except:
            return redirect('/')
    
class HomeView(FormView):
    form_class=SearchCompany
    template_name="base/home.html"
    def form_valid(self, form):
        company=form.cleaned_data['name']
        return redirect("https://"+settings.BASE_DOMAIN+"/"+company)


