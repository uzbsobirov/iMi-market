from django import forms
from .models import (
    History,
    Product,
    Category,
    Stock
)


class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = "__all__"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"
