from rest_framework.viewsets import ViewSet
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from easy_pdf.rendering import render_to_pdf_response
from .utils import pdf_generate
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas 
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

class ProductViewSet(ViewSet):
    
    permission_classes = [IsAuthenticated]


    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"status": "success","results": serializer.data})

    def create(self, request):
        
        
        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"status": "error","message": serializer.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        serializer.save()
        return Response({"status": "success","message": "product created."}, status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk):
        
        try:
            queryset = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"status": "success","message": "No matching product."}, status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(queryset)
        
        return Response({"status": "success","results": serializer.data})
    

    def update_product(self, request, pk, partial=False):
        try:
            queryset = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"status": "success", "message": "No matching product."}, status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(queryset, data=request.data, partial=partial)

        if not serializer.is_valid():
            return Response({"status": "error", "message": serializer.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        serializer.save()

        return Response({"status": "success", "message": "Product updated successfully."})

    def update(self, request, pk):
        return self.update_product(request, pk)

    def partial_update(self, request, pk):
        return self.update_product(request, pk, partial=True)

   

    def delete(self, request, pk):
        
        try:
            queryset = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"status": "success","message": "Sorry, we couldn't find any matching product."}, status.HTTP_404_NOT_FOUND)
        
        queryset.delete()

        return Response({"status": "success","message": "Product deleted successfully."}, status.HTTP_204_NO_CONTENT)
    

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):

        try:
            queryset = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"status": "success", "message": "No matching product."}, status.HTTP_404_NOT_FOUND)


        name = queryset.name
        description = queryset.description
        price = queryset.price
        image = queryset.image.path if queryset.image else None

        return pdf_generate(name,description,price,image)
       
