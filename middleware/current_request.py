from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from base.models import Client  # Your tenant model

class TenantPrefixMiddleware(MiddlewareMixin):
    """
    A simple middleware that extracts the tenant prefix from the URL path.
    For example, a request to /tenant1/dashboard/ will set tenant 'tenant1'.
    """

    def process_request(self, request):
        path_parts = request.path_info.split('/')
        # Expecting URL in the format: /<tenant>/...
        if len(path_parts) > 1 and path_parts[1]:
            tenant_prefix = path_parts[1]
            try:
                tenant = Client.objects.get(schema_name=tenant_prefix)
                request.tenant = tenant
                # Optionally, strip the tenant prefix from the path so your URLconf works normally.
                request.path_info = '/' + '/'.join(path_parts[2:])
            except Client.DoesNotExist:
                raise Http404("Tenant does not exist")
        else:
            # No tenant specified; you could assign the public tenant or raise 404.
            raise Http404("Tenant prefix missing from URL")
