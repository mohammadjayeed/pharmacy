from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'partial' in kwargs:
            for field_name in self.fields:
                field = self.fields[field_name]
                field.required = False