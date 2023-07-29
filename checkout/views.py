from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51NUnRsEcDHEeVZ1vnyjcLw1WSUq6AFE7FgQ09EEwM1FwQzy2v5IN7qb95tp4R6gEjXrJ5gttkeSaPna4NN7VmaKE0095Gl0BFd',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)