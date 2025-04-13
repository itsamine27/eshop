from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from tenant_schemas.utils import get_tenant_model, get_public_schema_name
from django.http import HttpResponseNotFound

class PathBasedTenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path_parts = request.path_info.strip('/').split('/')
        TenantModel = get_tenant_model()

        if path_parts and path_parts[0] != '':
            tenant_slug = path_parts[0]
            try:
                tenant = TenantModel.objects.get(schema_name=tenant_slug)
                connection.set_tenant(tenant)
                request.tenant = tenant
                request.tenant_path_prefix = '/' + tenant_slug
                # ⚠️ Do NOT override request.urlconf unless you really need it
                # ⚠️ Do NOT rewrite path_info
            except TenantModel.DoesNotExist:
                return HttpResponseNotFound("Tenant not found.")
        else:
            # Public tenant (homepage or shared stuff)
            tenant = TenantModel.objects.get(schema_name=get_public_schema_name())
            connection.set_tenant(tenant)
            request.tenant = tenant
            request.tenant_path_prefix = ''
