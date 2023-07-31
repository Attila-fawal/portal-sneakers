from django.urls import path
from . import views
from .views import GetSizesView


urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/get_sizes/', views.GetSizesView.as_view(), name='get_sizes'),
    path('add/', views.add_product, name='add_product'),
]
