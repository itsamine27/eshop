from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from django_tenants.utils import schema_context

class TenantSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_app(self, request, provider,**kwargs):
        """
        Retrieve the SocialApp for the given provider. If not found in the current schema,
        attempt to fetch it from the public schema.
        """
        try:
            # Try getting it in the current schema first
            return SocialApp.objects.get(provider=provider)
        except SocialApp.DoesNotExist:
            # Fallback to the public schema if not found
            with schema_context('public'):
                return SocialApp.objects.get(provider=provider)
