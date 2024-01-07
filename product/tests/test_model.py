import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from product.models import Product
from django.utils import timezone
import datetime

@pytest.mark.django_db
class TestProductModel:
    def test_create_product(self):
        # Creating in-memory files for testing
        memory_image = SimpleUploadedFile('test_image.jpg', b'Test Image Content', content_type='image/jpeg')
        memory_catalog = SimpleUploadedFile('test_catalog.pdf', b'Test PDF Content', content_type='application/pdf')

        # Creating a product instance
        product = Product(
            name="Test Product",
            manufacturer="Test Manufacturer",
            description="Test Description",
            price=Decimal('99.99'),
            image=memory_image,
            digital_catalog=memory_catalog,
            expiration_date=timezone.now().date() + datetime.timedelta(days=30)
        )

        # Saving the product
        product.save()

        # Fetching the product from the database
        dummy_product = Product.objects.get(name="Test Product")

        # Assertions to check if the product was correctly created
        assert dummy_product.name == "Test Product"
        assert dummy_product.manufacturer == "Test Manufacturer"
        assert dummy_product.description == "Test Description"
        assert dummy_product.price == Decimal('99.99')
        assert dummy_product.image is not None
        assert dummy_product.digital_catalog is not None
        assert dummy_product.expiration_date > timezone.now().date()

    def test_product_str(self):
        product = Product(name="Test Product")
        assert str(product) == "Test Product"

    def test_price_validation(self):
        # Creating a product with invalid price
        product = Product(
            name="Invalid Price Product",
            price=Decimal('-99.99')
        )

        # Expecting a validation error
        with pytest.raises(ValidationError):
            product.full_clean()
