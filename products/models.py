from django.db import models


class Category(models.Model):
    """
    Represents a product category with a name and its friendly name.
    """
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        # For example, to order by name:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    """
    Represents a product with its details like SKU, name, description, etc.
    """
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2,
                                 null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        # For example, to order by name:
        ordering = ['name']

    def __str__(self):
        return self.name


class Size(models.Model):
    """
    Represents a size associated with a specific type (Men, Women, or Kids).
    """
    size = models.IntegerField()
    SIZE_TYPE_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
        ('K', 'Kids'),
    ]
    size_type = models.CharField(max_length=1, choices=SIZE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.size} - {self.get_size_type_display()}"


class ProductSize(models.Model):
    """
    Represents a mapping between a product and
    its available sizes with quantities.
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.size.size}"
