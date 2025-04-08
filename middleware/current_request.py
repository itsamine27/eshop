from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from tenant_schemas.utils import get_tenant_model, get_public_schema_name

class PathBasedTenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path_parts = request.path_info.strip('/').split('/')
        if path_parts and path_parts[0] != '':
            tenant_slug = path_parts[0]
            TenantModel = get_tenant_model()
            try:
                tenant = TenantModel.objects.get(schema_name=tenant_slug)
                connection.set_tenant(tenant)  # Set the database connection's tenant
                request.urlconf = 'eshop.urls'
                request.path_info = '/' + '/'.join(path_parts[1:])
                request.tenant = tenant  # Add this line to set the tenant on the request object
                request.tenant_path_prefix = '/' + tenant_slug
            except TenantModel.DoesNotExist:
                return  # Handle tenant not found (e.g., return a 404 response)
        else:
            # Public tenant
            tenant = get_tenant_model().objects.get(schema_name=get_public_schema_name())
            connection.set_tenant(tenant)  # Set the public schema
            request.urlconf = 'eshop.public_urls'
            request.tenant = tenant  # Add this line for public tenant
