from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('products/<int:pk>/', views.ProductRetieveUpdateDeleteViewSet.as_view({'get': 'retrieve', 
                                                                                'put': 'update', 
                                                                                'patch': 'partial_update', 
                                                                                'delete': 'destroy'}), name='product-details'),
    ]

urlpatterns += router.urls