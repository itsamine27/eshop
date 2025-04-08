from django.db import connection

def tenant_context_processor(request):
    """
    Adds the current tenant name to the template context.
    """
    tenant_name = getattr(request.tenant, "name", "")  # Get tenant name if available
    return {
        "tenant_name": tenant_name,
    }
