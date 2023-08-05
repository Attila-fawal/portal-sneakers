from django.shortcuts import render
from products.models import Product  

def index(request):
    """ A view to return the index page with new arrival items """

    # Fetch the items that belong to the category with id 4
    new_arrival_items = Product.objects.filter(category_id=4)

    # Pass the items to the template
    context = {
        'new_arrival_items': new_arrival_items,
    }

    return render(request, 'home/index.html', context)
