from django import forms
from .models import ProductSize, Size, Product, Category
from django.forms import inlineformset_factory

class ProductSizeForm(forms.ModelForm):
    size = forms.ModelChoiceField(queryset=Size.objects.none())
    
    class Meta:
        model = ProductSize
        fields = ['product', 'size', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in kwargs:
            self.fields['size'].queryset = Size.objects.filter(size_type=kwargs['category'])

    def id_for_label(self, id_):
        """
        Include index in label for size field.
        """
        if id_ == 'id_product-size':
            id_ += '-' + str(self.prefix)
        return id_

ProductSizeFormSet = inlineformset_factory(Product, ProductSize, form=ProductSizeForm, fields=('size', 'quantity'), extra=1)

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        self.fields['category'].widget.attrs.update({'class': 'category-dropdown'})
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
