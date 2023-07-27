from django.urls import path
from . import views
from .views import GetSizesView


urlpatterns = [
    path('', views.all_products, name='products'),
    path('<product_id>', views.product_detail, name='product_detail'),
    path('get_sizes/', GetSizesView.as_view(), name='get_sizes'),


]