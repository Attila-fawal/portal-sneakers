from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Comment(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=1000)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment {self.text[:20]} by {self.user.username} on {self.product.name}'
