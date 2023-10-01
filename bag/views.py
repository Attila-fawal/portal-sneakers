from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, ProductSize
from django.http import HttpResponse, JsonResponse
from django.urls import reverse


def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    product = get_object_or_404(Product, pk=item_id)
    size_id = str(request.POST.get('size')).split(' ')[0]
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if quantity < 1:
        messages.error(request, 'Quantity must be at least 1.')
        return redirect(redirect_url)

    product_size = ProductSize.objects.get(
        product=product, size__id=int(size_id)
    )

    current_qty = bag.get(item_id, {}).get(size_id, 0)

    if quantity + current_qty > product_size.quantity:
        avail_qty = product_size.quantity - current_qty
        msg = f'Sorry, only {avail_qty} more items are available.'
        messages.error(request, msg)
    else:
        if item_id not in bag:
            bag[item_id] = {}

        if size_id in bag[item_id]:
            bag[item_id][size_id] += quantity
            msg = (
                f'Updated size {product_size.size} of {product.name} '
                f'to {bag[item_id][size_id]}'
            )
            messages.success(request, msg)
        else:
            bag[item_id][size_id] = quantity
            msg = (
                f'Added size {product_size.size} of {product.name} '
                'to your bag'
            )
            messages.success(request, msg)

        request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id, size):
    """Adjust quantity of the specified product to the specified amount"""
    try:
        item_id = str(item_id)
        product = get_object_or_404(Product, pk=item_id)
        size_id = str(request.POST.get('size'))
        quantity = int(request.POST.get('quantity'))
        bag = request.session.get('bag', {})

        product_size = ProductSize.objects.get(
            product=product, size__id=int(size_id)
        )

        if quantity < 1:
            messages.error(request, 'Quantity must be at least 1.')
            return JsonResponse({
                                'success': False,
                                'redirect_url': reverse('view_bag')})

        if quantity > product_size.quantity:
            msg = f'Sorry, only {product_size.quantity} items available.'
            messages.error(request, msg)
            return JsonResponse({
                                'success': False,
                                'redirect_url': reverse('view_bag')})

        bag[item_id][size_id] = quantity
        request.session['bag'] = bag

        msg = (
            f'Updated size {product_size.size} of {product.name} '
            f'to {quantity}'
        )
        messages.success(request, msg)
        return JsonResponse({
                            'success': True,
                            'redirect_url': reverse('view_bag')})

    except Exception as e:
        messages.error(request, f'Error occurred: {e}')
        return JsonResponse({'success': False})


def remove_from_bag(request, item_id, size):
    """Remove the item from the shopping bag"""
    try:
        item_id = str(item_id)
        size_id = str(request.POST.get('size'))
        bag = request.session.get('bag', {})

        if item_id in bag and size_id in bag[item_id]:
            del bag[item_id][size_id]
            if not bag[item_id]:
                bag.pop(item_id)

            request.session['bag'] = bag
            msg = 'Item removed from your bag.'
            messages.success(request, msg)
        else:
            msg = 'Item or size not found in your bag.'
            messages.error(request, msg)
            return JsonResponse({'success': False})

        return JsonResponse({'success': True})

    except Exception as e:
        msg = f'Error occurred: {e}'
        messages.error(request, msg)
        return HttpResponse(status=500)
