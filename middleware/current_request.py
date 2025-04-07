from django.db import connection
from base.models import Client  # Your tenant model

class TenantPrefixMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.strip("/").split("/")
        prefix = path[0] if path and path[0] else ""

        if prefix and Client.objects.filter(schema_name=prefix).exists():
            tenant = Client.objects.get(schema_name=prefix)
        else:
            tenant = Client.objects.get(schema_name="public")

        connection.set_schema(tenant.schema_name)
        return self.get_response(request)
