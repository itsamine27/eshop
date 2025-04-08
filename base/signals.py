from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from base.models import Client  # make sure Client and Domain are imported from your shared app
from .models import CompanyModel  # Import the Profile model
from django.conf import settings
@receiver(post_save, sender=CompanyModel)
def create_tenant_for_user(sender, instance, created, **kwargs):
    if created:
        # Define a schema name. Here we simply use the username in lower case.
        schema_name = instance.company.username.lower()


        
        # Create the tenant. You can add more fields as necessary.
        tenant = Client(schema_name=schema_name, name=instance.company, domain_url="eshop-m942.onrender.com/"+schema_name)
        tenant.save()  # This call will trigger the creation of a new schema