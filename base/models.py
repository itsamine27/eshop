from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from tenant_schemas.models import TenantMixin
from django.db import models

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

class CompanyOwner(models.Manager):
    def CompanyUser(self,name):
        comapany=User.objects.get(username=name)
        return self.get(company=comapany)
    

class CompanyModel(models.Model):
    company = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE
    )
    company_logo = CloudinaryField(
        'image', 
        blank=True,  # Allows the field to be optional
        null=True     # Ensures the database allows NULL values
    )
    company_slogan = models.CharField(
        max_length=30,
    )
    discount_points = models.BooleanField(
        default=True,
        help_text="Allow users to gain points on purchases that get transformed into discounts"
    )
    objects=CompanyOwner()
    def __str__(self):
        return f"{self.company.username} Profile"
    
