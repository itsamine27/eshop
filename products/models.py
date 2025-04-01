from django.db import models
from base.models import CompanyModel
from cloudinary.models import CloudinaryField
from django.core.validators import MaxValueValidator,MinValueValidator
from functools import cached_property

from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Avg
# Create your models here.

class CompanyProducts(models.Model):
    company=models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=50)
    product_description=models.TextField(max_length=200)
    product_quantity=models.IntegerField()
    product_price=models.FloatField(validators=[MaxValueValidator(1000000.0)])
    product_discount=models.DecimalField(max_digits=5, decimal_places=2, help_text="leave it blanck for no discount",default=0.00)
    
    @cached_property
    def CountDiscount(self):
        price = Decimal(str(self.product_price))
        hundred = Decimal('100')
        # Compute discount percentage (100 - discount)
        discount_multiplier = hundred - self.product_discount
        # Calculate the discounted price.
        discounted_price = (price * discount_multiplier) / hundred
        # Round the result to 2 decimal places.
        return discounted_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    @cached_property
    def Avrage_Rating(self):
        average = self.product_rating.aggregate(avg_rating=Avg('product_rating'))['avg_rating']

        # If there are no ratings, average might be None. Return 0 in that case.
        if average is None:
            return 0
        # Optionally, round the result to 2 decimal places.
        return round(average, 2)



class CompanyProductsImages(models.Model):
    product=models.ForeignKey(CompanyProducts, related_name='product_images', on_delete=models.CASCADE)
    product_image=CloudinaryField('image')
class ProductRating(models.Model):
    product=models.ForeignKey(CompanyProducts, related_name='product_rating', on_delete=models.CASCADE)
    product_rating=models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Value must be between 1 and 5",
        blank=True
    )
    
