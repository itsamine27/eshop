from .serializers import CompanyProductsSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CompanyProducts
class CreateProduct(APIView):
    def post(self, request):
        serializer=CompanyProductsSerializer(data=request.data)
        if serializer.is_valid():
            product=serializer.save()
            return Response(CompanyProductsSerializer(product).data, status=status.HTTP_201_CREATED)
        # If validation fails, return errors with a 400 status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    