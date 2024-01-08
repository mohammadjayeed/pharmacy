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
from .serializers import ProductSerializer
from .models import Product
from .utils import pdf_generate
from .filters import ProductFilter
from .throttling import ProductDetailViewThrottle, TotalAnonVisit
from .pagination import Pagination
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
# product viewset for list, create, update, partial_update, delete, download
class ProductViewSet(ViewSet):

    '''
    Viewset responsible for create and get of products
    '''
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]  # filterbackend from rest_framework
    filterset_class = ProductFilter # filtering for manufacturer, expiration = > <
    throttle_classes = [TotalAnonVisit] # custom throttle class for total anonymous visit restriction
    parser_classes = (MultiPartParser,)
    
    @swagger_auto_schema(request_body=ProductSerializer) # decorator so that swagger picks up the endpoint
    def create(self, request):
        
        
        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"status": "error","message": serializer.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        serializer.save()
        return Response({"status": "success","message": "product created."}, status.HTTP_201_CREATED)
    
    

    # enable/disable  cache_page decorator for cache_page management of GET endpoint , time is 1 minute
    # @method_decorator(cache_page(1*60))  
    def list(self, request):
        

        # demonstrating delay of 2 seconds, once cached, delay will be cancelled 
        # will execute again once cache resets
        cache_test = requests.get('https://httpbin.org/delay/1')
        result = cache_test.json()  

        products = Product.objects.all()
        filter_instance = self.filterset_class(request.GET, queryset=products) # custom filtering in action
        queryset = filter_instance.qs

        paginator = Pagination() # declaring pagination class , this class is custom  , can change parameters in pagination.py
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = ProductSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    
class ProductRetieveUpdateDeleteViewSet(ViewSet):

    '''
    Viewset responsible for detail-view, put, patch, delete of products
    '''
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser,)
    throttle_classes = [ProductDetailViewThrottle, TotalAnonVisit]  


    # enable/disable  cache_page decorator for cache management of GET endpoint , time is 1 minute
    # @method_decorator(cache_page(1*60))
    def retrieve(self, request, pk):
        
        try:
            queryset = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"status": "success","message": "No matching product."}, status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(queryset)
        
        return Response({"status": "success","results": serializer.data})
    
    
    def destroy(self, request, pk):
        
        try:
            queryset = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"status": "success","message": "Sorry, we couldn't find any matching product."}, status.HTTP_404_NOT_FOUND)
        
        queryset.delete()

        return Response({"status": "success","message": "Product deleted successfully."}, status.HTTP_204_NO_CONTENT)
    

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
    

    @swagger_auto_schema(request_body=ProductSerializer)
    def update(self, request, pk):
        return self.update_product(request, pk)
    

    @swagger_auto_schema(request_body=ProductSerializer(partial=True))
    def partial_update(self, request, pk):
        return self.update_product(request, pk, partial=True)

    
class ProductInfoDownloadViewSet(ViewSet):
    '''
    Viewset responsible for downloading product information in pdf format
    '''
    def retrieve(self,request,pk):

        try:
            queryset = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"status": "success", "message": "No matching product."}, status.HTTP_404_NOT_FOUND)


        name = queryset.name
        description = queryset.description
        price = queryset.price
        image = queryset.image.path if queryset.image else None

        return pdf_generate(name,description,price,image)