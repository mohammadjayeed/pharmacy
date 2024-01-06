from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('products/<int:pk>/', views.ProductRetieveViewSet.as_view({'get': 'retrieve'}), name='product-details'),
    ]

urlpatterns += router.urls