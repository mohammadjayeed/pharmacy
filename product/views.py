import requests
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action, throttle_classes, authentication_classes
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from .serializers import ProductSerializer, ProductRetrieveSerializer
from .models import Product
from .utils import pdf_generate
from .filters import ProductFilter
from .throttling import ProductDetailViewThrottle, TotalAnonVisit
from .pagination import Pagination


# product viewset for list, create, update, partial_update, delete, download
class ProductViewSet(ViewSet):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]  # filterbackend from rest_framework
    filterset_class = ProductFilter # filtering for manufacturer, expiration = > <
    throttle_classes = [TotalAnonVisit] # custom throttle class for total anonymous visit restriction
    

    # @method_decorator(cache_page(2*60))
    def list(self, request):
        
        # cache_test = requests.get('https://httpbin.org/delay/3')
        # result = cache_test.json()

        products = Product.objects.all()
        filter_instance = self.filterset_class(request.GET, queryset=products) # custom filtering in action
        queryset = filter_instance.qs

        paginator = Pagination() # declaring pagination class , this class is custom  , can change parameters in pagination.py
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = ProductSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        
        
        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"status": "error","message": serializer.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        serializer.save()
        return Response({"status": "success","message": "product created."}, status.HTTP_201_CREATED)
    

    

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

   
class ProductRetieveViewSet(ViewSet):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [ProductDetailViewThrottle, TotalAnonVisit]  

    # @method_decorator(cache_page(2*60))
    def retrieve(self, request, pk):
        
        try:
            queryset = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"status": "success","message": "No matching product."}, status.HTTP_404_NOT_FOUND)
        
        serializer = ProductRetrieveSerializer(queryset)
        
        return Response({"status": "success","results": serializer.data})
    

    def delete(self, request, pk):
        
        try:
            queryset = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"status": "success","message": "Sorry, we couldn't find any matching product."}, status.HTTP_404_NOT_FOUND)
        
        queryset.delete()

        return Response({"status": "success","message": "Product deleted successfully."}, status.HTTP_204_NO_CONTENT)