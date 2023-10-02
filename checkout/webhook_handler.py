from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile

import json
import time
import stripe

# Setting the Stripe API key using the key from Django's settings
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info
       # Retrieve charges using Stripe API
        charges = stripe.Charge.list(payment_intent=intent.id)
        if charges.data:
            billing_details = charges.data[0].billing_details
            grand_total = round(charges.data[0].amount / 100, 2)
        else:
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    f'ERROR: No charges found for the payment intent'
                ),
                status=400
            )

        shipping_details = intent.shipping
        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile_data = {
                    'default_phone_number': shipping_details.phone,
                    'default_country': shipping_details.address.country,
                    'default_postcode': shipping_details.address.postal_code,
                    'default_town_or_city': shipping_details.address.city,
                    'default_street_address1': shipping_details.address.line1,
                    'default_street_address2': shipping_details.address.line2,
                    'default_county': shipping_details.address.state
                }
                for field, value in profile_data.items():
                    setattr(profile, field, value)
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    f'SUCCESS: Verified order already in database'
                ),
                status=200
            )
        else:
            order = self._create_order(intent, profile, bag, pid,
                                       shipping_details, billing_details)
            if order:
                self._send_confirmation_email(order)
                return HttpResponse(
                    content=(
                        f'Webhook received: {event["type"]} | '
                        f'SUCCESS: Created order in webhook'
                    ),
                    status=200
                )

    def _create_order(self, intent, profile, bag, pid,
                      shipping_details, billing_details):
        """Helper method to create order from webhook"""
        try:
            order = Order.objects.create(
                full_name=shipping_details.name,
                user_profile=profile,
                email=billing_details.email,
                phone_number=shipping_details.phone,
                country=shipping_details.address.country,
                postcode=shipping_details.address.postal_code,
                town_or_city=shipping_details.address.city,
                street_address1=shipping_details.address.line1,
                street_address2=shipping_details.address.line2,
                county=shipping_details.address.state,
                original_bag=bag,
                stripe_pid=pid
            )
            for item_id, item_data in json.loads(bag).items():
                product = Product.objects.get(id=item_id)
                if isinstance(item_data, int):
                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item_data
                    )
                else:
                    for size, quantity in item_data['items_by_size'].items():
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            product_size=size
                        )
            return order
        except Exception as e:
            if order:
                order.delete()
            HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {e}',
                status=500
            )
            return None

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
