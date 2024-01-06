from django_filters.rest_framework import FilterSet
from .models import Product

class ProductFilter(FilterSet):

    class Meta:
        model = Product
        fields = {
            'manufacturer':['exact'],
            'expiration':['exact','gt','lt'],

        }