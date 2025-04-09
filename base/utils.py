from django.conf import settings

def build_tenant_url(subdomain: str, port: int = 8000) -> str:
    """
    Build a full tenant URL given the subdomain. 
    e.g., for subdomain 'nike' and BASE_DOMAIN 'lvh.me', returns:
          "http://nike.lvh.me:8000/"
    """
    return f"https://{settings.BASE_DOMAIN}/{subdomain}"