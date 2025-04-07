from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from tenant_schemas.utils import get_tenant_model
class PathBasedTenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path_parts = request.path_info.strip('/').split('/')
        if path_parts:
            tenant_slug = path_parts[0]
            TenantModel = get_tenant_model()
            try:
                tenant = TenantModel.objects.get(schema_name=tenant_slug)
                connection.set_tenant(tenant)
                request.urlconf = 'eshop.urls'  # all tenants share one urls.py
                # Update path so the rest of Django ignores the tenant slug
                request.path_info = '/' + '/'.join(path_parts[1:])
                request.tenant_path_prefix = '/' + tenant_slug
            except TenantModel.DoesNotExist:
                # Show 404 or fallback to public tenant
                pass
        else:
            # No tenant path = public tenant
            from tenant_schemas.utils import get_public_schema_name, get_tenant_model
            tenant = get_tenant_model().objects.get(schema_name=get_public_schema_name())
            connection.set_tenant(tenant)
            request.urlconf = 'eshop.public_urls'
