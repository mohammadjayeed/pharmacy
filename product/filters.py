from django_filters.rest_framework import FilterSet
from .models import Product

class ProductFilter(FilterSet):
    '''
    product filter class - filters manufacturer, expiration date
    expiration date params :    = > <
    '''
    class Meta:
        model = Product
        fields = {
            'manufacturer':['iexact'],
            'expiration_date':['exact','gt','lt'],

        }