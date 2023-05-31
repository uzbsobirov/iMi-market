from rest_framework import serializers
from core.models import Product, Category, History, Stock
from django.utils.text import slugify
from django.core.exceptions import ValidationError


def min_value_validator(value):
    if value < 0:
        raise ValidationError(
            '%(value)s must be greater than or equal to 0',
            params={'value': value},
        )


ROF = ('id', 'date_created', 'date_updated')


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField(allow_unicode=True, allow_null=True, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[min_value_validator])

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ROF

    def save(self, *args, **kwargs):
        if not self.validated_data.get('slug'):
            self.validated_data['slug'] = slugify(self.validated_data.get('name'))
        return super(ProductSerializer, self).save(*args, **kwargs)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ROF

    def save(self, *args, **kwargs):
        if not self.validated_data.get('slug'):
            self.validated_data['slug'] = slugify(self.validated_data.get('name'))
        return super(CategorySerializer, self).save(*args, **kwargs)


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"
        read_only_fields = ROF


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"
        read_only_fields = ROF
