from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from product.models import Product
from decimal import Decimal
import pytest

@pytest.mark.django_db
class TestProductCRUD:
         

    def test_if_user_is_anonymous_then_cannot_create_product(self):

        client = APIClient()
        response = client.post('/api/v1/products/', {'name': 'Test Product', 'price': '9.99'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Multiple assertions in a single test
    def test_if_user_is_anonymous_then_cannot_update_product_delete_product(self):

        user_client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')
        user_client.force_authenticate(user=user)
        
        data = {
            'name': 'Test Product',
            'price': '9.99'
        }
        
        response = user_client.post('/api/v1/products/', data)
        product = Product.objects.first()

        anom_client = APIClient()

        response = anom_client.delete(f'/api/v1/products/{product.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = anom_client.put(f'/api/v1/products/{product.id}/',{'name': 'Test Product','price': '10.99'},content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = anom_client.patch(f'/api/v1/products/{product.id}/',{'manufacturer': 'A Company'},content_type='application/json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Multiple assertions in a single test
    def test_if_user_is_authenticated_then_can_create_product_update_product_delete_product(self):
            
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.force_authenticate(user=user)
        
        data = {
            'name': 'Test Product',
            'price': '9.99'
        }
        
        response = client.post('/api/v1/products/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == 1
        
        product = Product.objects.first()
        assert product.name == 'Test Product'
        assert product.price == Decimal('9.99')