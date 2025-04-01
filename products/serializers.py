# serializers.py
from rest_framework import serializers
from .models import CompanyProducts, CompanyProductsImages, ProductRating
from django.db.models import Avg
class CompanyProductsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProductsImages
        fields = ['id', 'product_image']

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['id', 'product_rating']
class CompanyProductsSerializer(serializers.ModelSerializer):
    product_images=CompanyProductsImagesSerializer(many=True)
    product_rating=ProductRatingSerializer(many=True)
    #methods
    Avrage_Rating=serializers.SerializerMethodField()
    CountDiscount=serializers.SerializerMethodField()
    class Meta:
        model=CompanyProducts
        fields=[
            'id',
            'company',
            'product_name',
            'product_description',
            'product_quantity',
            'product_price',
            'product_discount',
            'CountDiscount',    # Discount after applying product_discount
            'Avrage_Rating',    # Computed average rating
            'product_images',    # Nested images related to the product
            'product_rating',    # Nested ratings related to the product

        ]
    def get_Avrage_Rating(self, obj):
        # 'obj.product_rating' is the reverse relation manager for ProductRating objects.
        # We aggregate the average of the 'product_rating' field.
        average = obj.product_rating.aggregate(avg_rating=Avg('product_rating'))['avg_rating']

        # If there are no ratings, average might be None. Return 0 in that case.
        if average is None:
            return 0
        # Optionally, round the result to 2 decimal places.
        return round(average, 2)

    def get_CountDiscount(self,obj):
        return obj.CountDiscount
    def create(self, validated_data):
        image_data=validated_data.pop('product_images', [])
        rating_data=validated_data.pop('product_rating', [])
        product=CompanyProducts.objects.create(**validated_data)
        for image in image_data:
            CompanyProductsImages.objects.create(product=product, **image)
        for rating in rating_data:
            ProductRating.objects.create(product=product, **rating)
        return product
        