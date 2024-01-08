from django.urls import path
from django.urls.conf import include
from . import views


urlpatterns = [
    path('products/', views.ProductViewSet.as_view({'get': 'list','post': 'create'}), name='product'),
    path('products/<int:pk>/', views.ProductRetieveUpdateDeleteViewSet.as_view({'get': 'retrieve', 
                                                                                'put': 'update', 
                                                                                'patch': 'partial_update', 
                                                                                'delete': 'destroy'}), name='product-details'),
    path('products/<int:pk>/download/', views.ProductInfoDownloadViewSet.as_view({'get': 'retrieve'}), name='product-info-download'),
    ]
