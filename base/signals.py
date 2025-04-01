from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from base.models import Client, Domain  # make sure Client and Domain are imported from your shared app
from .models import CompanyModel  # Import the Profile model
from django.conf import settings
@receiver(post_save, sender=CompanyModel)
def create_tenant_for_user(sender, instance, created, **kwargs):
    if created:
        # Define a schema name. Here we simply use the username in lower case.
        schema_name = instance.company.username.lower()


        
        # Create the tenant. You can add more fields as necessary.
        tenant = Client(schema_name=schema_name, name=instance.company)
        tenant.save()  # This call will trigger the creation of a new schema
        
        # Create a corresponding Domain record.
        # For local development with nip.io, this domain will resolve to 127.0.0.1.
        domain_name = f"{schema_name}.{settings.BASE_DOMAIN}"
        domain = Domain(domain=domain_name, tenant=tenant, is_primary=True)
        domain.save()