from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, ProductSize

def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):

    """ Add a quantity of the specified product to the shopping bag """
    product = get_object_or_404(Product, pk=item_id)
    size_id = str(request.POST.get('size'))  # convert to string here instead of int
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    # Check if the quantity is less than 1
    if quantity < 1:
        messages.error(request, 'Quantity must be at least 1.')
        return redirect(redirect_url)

    # Retrieve the ProductSize instance for this product and size
    product_size = ProductSize.objects.get(product=product, size__id=int(size_id))  # convert to int here for DB query

    # Calculate the current quantity of the product in the bag
    current_quantity = bag.get(item_id, {}).get(size_id, 0)
    
    # Check if the requested quantity exceeds the available inventory
    if quantity + current_quantity > product_size.quantity:
        messages.error(request, f'Sorry, only {product_size.quantity - current_quantity} more items are available.')
    else: 
        # Ensure we have a dictionary for this item in the bag
        if item_id not in bag:
            bag[item_id] = {}

        # Check if we already have the product size in the bag
        if size_id in bag[item_id]:
            bag[item_id][size_id] += quantity
            messages.success(request, f'Updated size {product_size.size} quantity of {product.name} to {bag[item_id][size_id]}')
        else:
            bag[item_id][size_id] = quantity
            messages.success(request, f'Added size {product_size.size} of {product.name} to your bag')

        request.session['bag'] = bag

    return redirect(redirect_url)
