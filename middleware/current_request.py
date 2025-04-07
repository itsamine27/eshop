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
                request.urlconf = tenant_slug + '.urls'
                connection.set_tenant(tenant)
            except TenantModel.DoesNotExist:
                # Handle the case where the tenant does not exist
                pass
