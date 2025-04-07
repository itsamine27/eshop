# eshop/middleware/conditional_ssl.py

from django.shortcuts import redirect

class ConditionalSSLRedirectMiddleware:
    """
    Redirects to HTTPS only if the current tenant is the public tenant.
    Otherwise, leaves the request as is.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if tenant is available; django-tenants sets `request.tenant`
        tenant = getattr(request, 'tenant', None)
        # Check if this is the public tenant and if the request is not secure.
        if tenant and tenant.schema_name == 'public' and not request.is_secure():
            # Build the secure URL: replace 'http://' with 'https://'
            secure_url = request.build_absolute_uri(request.get_full_path()).replace('http://', 'https://', 1)
            return redirect(secure_url)
        return self.get_response(request)
