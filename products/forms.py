from django import forms
from .models import ProductSize, Size, Product

class ProductSizeForm(forms.ModelForm):
    class Meta:
        model = ProductSize
        fields = ['product', 'size', 'quantity']
        widgets = {
            'size': forms.Select(),
        }

    size_type = forms.ChoiceField(choices=Size.SIZE_TYPE_CHOICES)

ProductSizeFormset = forms.inlineformset_factory(Product, ProductSize, form=ProductSizeForm, extra=1)
