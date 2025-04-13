from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from tenant_schemas.utils import get_tenant_model, get_public_schema_name
from django.http import HttpResponseNotFound
import logging

logger = logging.getLogger(__name__)

EXCLUDED_PREFIXES = {'accounts', 'admin', 'static', 'media', 'favicon.ico', 'robots.txt', 'addproduct'}

class PathBasedTenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path_info = request.path_info.strip('/')
        path_parts = path_info.split('/')

        TenantModel = get_tenant_model()

        if path_parts and path_parts[0]:
            prefix = path_parts[0].strip().lower()  # ⬅️ Always lowercased

            # 🚫 Skip paths that should not be treated as tenants
            if prefix in EXCLUDED_PREFIXES:
                tenant = TenantModel.objects.get(schema_name=get_public_schema_name())
                connection.set_tenant(tenant)
                request.tenant = tenant
                request.tenant_path_prefix = ''
                logger.debug(f"[TenantMiddleware] '{prefix}' excluded — using public tenant")
                return

            try:
                tenant = TenantModel.objects.get(schema_name=prefix)
                connection.set_tenant(tenant)
                request.tenant = tenant
                request.tenant_path_prefix = '/' + prefix
                logger.debug(f"[TenantMiddleware] Tenant found: {prefix}")
            except TenantModel.DoesNotExist:
                logger.warning(f"[TenantMiddleware] Tenant not found for slug: {prefix}")
                return HttpResponseNotFound("Tenant not found.")
        else:
            # Public schema fallback
            tenant = TenantModel.objects.get(schema_name=get_public_schema_name())
            connection.set_tenant(tenant)
            request.tenant = tenant
            request.tenant_path_prefix = ''
            logger.debug("[TenantMiddleware] Public tenant set")
