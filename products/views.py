from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category
from django.http import JsonResponse
from django.views import View
from .models import Size
from django.core import serializers
from .forms import ProductForm, ProductSizeFormSet




# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


class GetSizesView(View):
    def get(self, request, *args, **kwargs):
        size_type = request.GET.get('size_type', None)
        if size_type:
            sizes = list(Size.objects.filter(size_type=size_type).values('id', 'size'))
            return JsonResponse({'sizes': sizes})
        else:
            return JsonResponse({'error': 'Missing size type parameter.'}, status=400)

def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductSizeFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()
            return redirect('products')
    else:
        form = ProductForm()
        formset = ProductSizeFormSet()

    template = 'products/add_product.html'
    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, template, context)
    

def get_sizes(request):
    category = request.GET.get('category', None)

    if category is not None:
        category_id = int(category)

        if category_id in [4, 5]:  # Assuming 'New Arrivals' and 'Deals' category ids are 4 and 5 respectively
            sizes = Size.objects.all().values()
        else:
            size_type = None

            if category_id == 1:  # Assuming 'Men' category id is 1
                size_type = 'M'
            elif category_id == 2:  # Assuming 'Women' category id is 2
                size_type = 'W'
            elif category_id == 3:  # Assuming 'Kids' category id is 3
                size_type = 'K'

            if size_type:
                sizes = Size.objects.filter(size_type=size_type).values()
            else:
                return JsonResponse({'error': 'Invalid category'}, status=400)

        sizes_list = list(sizes)  # important: convert the QuerySet to a list
        return JsonResponse(sizes_list, safe=False)

    return JsonResponse({'error': 'Invalid category'}, status=400)
