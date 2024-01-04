import os
from django.db import models
from django.core.validators import MinValueValidator
from validators import validate_pdf, validate_image

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6,decimal_places=2,validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='product/images/', null=True, blank=True,validators=[validate_image])
    digital_catalog = models.FileField(upload_to='product/catalog/', null=True, blank=True,validators=[validate_pdf])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def delete(self, **kwargs):
        os.remove(self.image.path)
        super().delete(**kwargs)
