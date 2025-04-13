from django.db import connection
from django.utils.deprecation import MiddlewareMixin
from tenant_schemas.utils import get_tenant_model, get_public_schema_name
from django.http import HttpResponseNotFound
import logging

logger = logging.getLogger(__name__)

class PathBasedTenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path_info = request.path_info.strip('/')
        path_parts = path_info.split('/')

        TenantModel = get_tenant_model()

        if path_parts and path_parts[0]:  # e.g., /samsung/
            tenant_slug = path_parts[0].strip()
            try:
                tenant = TenantModel.objects.get(schema_name=tenant_slug)
                connection.set_tenant(tenant)
                request.tenant = tenant
                request.tenant_path_prefix = '/' + tenant_slug
                logger.debug(f"[TenantMiddleware] Tenant found: {tenant_slug}")
            except TenantModel.DoesNotExist:
                logger.warning(f"[TenantMiddleware] Tenant not found for slug: {tenant_slug}")
                return HttpResponseNotFound("Tenant not found.")
        else:
            # Fallback to public schema
            try:
                public_tenant = TenantModel.objects.get(schema_name=get_public_schema_name())
                connection.set_tenant(public_tenant)
                request.tenant = public_tenant
                request.tenant_path_prefix = ''
                logger.debug("[TenantMiddleware] Public tenant set")
            except TenantModel.DoesNotExist:
                logger.critical("[TenantMiddleware] Public tenant not found!")
                return HttpResponseNotFound("Public tenant not configured.")
