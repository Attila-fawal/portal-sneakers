from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('get_sizes/', views.get_sizes, name='get_sizes'),  # Updated URL pattern for get_sizes function
    path('add/', views.add_product, name='add_product'),
]
