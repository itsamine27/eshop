from django.db import connection

def tenant_context_processor(request):
    tenant_name = getattr(request, "tenant", None)
    schema_name = connection.schema_name
    return {
        "tenant_name": tenant_name.name if tenant_name else schema_name
    }
