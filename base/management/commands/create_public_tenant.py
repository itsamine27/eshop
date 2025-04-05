from django.core.management.base import BaseCommand
from base.models import Client, Domain  # Update if your model paths differ
from django.conf import settings

class Command(BaseCommand):
    help = 'Create the public tenant with domain if it does not exist.'

    def handle(self, *args, **kwargs):
        domain = settings.BASE_DOMAIN

        if not Client.objects.filter(schema_name='public').exists():
            self.stdout.write("Creating public tenant...")
            tenant = Client(schema_name='public', name='public')
            tenant.save()

            domain_obj = Domain(domain=domain, tenant=tenant, is_primary=True)
            domain_obj.save()
            self.stdout.write(self.style.SUCCESS(f"Public tenant created with domain: {domain}"))
        else:
            self.stdout.write("Public tenant already exists.")
