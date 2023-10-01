from django import forms
from .widgets import CustomClearableFileInput
from .models import ProductSize, Size, Product, Category
from django.forms import inlineformset_factory


class ProductSizeForm(forms.ModelForm):
    size = forms.ModelChoiceField(queryset=Size.objects.all())

    class Meta:
        model = ProductSize
        fields = ['product', 'size', 'quantity']

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category', None)
        super().__init__(*args, **kwargs)
        if self.category:
            qs = Size.objects.filter(size_type=self.category)
            self.fields['size'].queryset = qs

    def clean_size(self):
        size = self.cleaned_data.get('size')
        if size and self.category and size.size_type != self.category:
            msg = "Size must match the selected category."
            raise forms.ValidationError(msg)
        return size

    def id_for_label(self, id_):
        if id_ == 'id_product-size':
            id_ += '-' + str(self.prefix)
        return id_


def create_product_size_formset(*args, **kwargs):
    category = kwargs.pop("category", None)
    ProductSizeFormSet = inlineformset_factory(
        Product,
        ProductSize,
        form=ProductSizeForm,
        fields=('size', 'quantity'),
        extra=1
    )

    class NewProductSizeFormSet(ProductSizeFormSet):
        def __init__(self, *args, **kwargs):
            super(NewProductSizeFormSet, self).__init__(*args, **kwargs)
            for form in self:
                form.category = category

    return NewProductSizeFormSet(*args, **kwargs)


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        friendly_names.insert(0, ("", "Select Category"))

        self.fields['category'].choices = friendly_names
        self.fields['category'].widget.attrs.update(
            {'class': 'category-dropdown'})
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
