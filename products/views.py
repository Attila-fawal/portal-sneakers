from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category
from django.http import JsonResponse
from django.views import View
from .models import Size
from django.core import serializers
from .forms import ProductForm, create_product_size_formset
from django.forms import inlineformset_factory
from .models import ProductSize
from comments.forms import CommentForm







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
    
    # Get all the comments related to the product
    comments = product.comments.all()

    # Create a list [1, 2, 3, 4, 5] to generate the stars in the template
    stars = list(range(1, 6))  

    # Instantiate the form
    comment_form = CommentForm()

    context = {
        'product': product,
        'comment_form': comment_form,
        'comments': comments,
        'stars': stars,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = create_product_size_formset(request.POST)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()
            messages.success(request, 'Successfully added product!')
            return redirect('products')
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        formset = create_product_size_formset()

    template = 'products/add_product.html'
    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, template, context)

    
@login_required
def get_sizes(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
        
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

@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = create_product_size_formset(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()
            formset.save_m2m()  # Save ManyToMany relations
            messages.success(request, 'Successfully updated product!')
            return redirect('products')
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        formset = create_product_size_formset(instance=product)

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'formset': formset,
        'product': product,  # Add this line
    }

    return render(request, template, context)





@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    try:
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(request, f'Successfully deleted product: {product.name}!')
    except Product.DoesNotExist:
        messages.error(request, 'Product not found')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    return redirect(reverse('products'))
