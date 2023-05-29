from rest_framework import serializers
from core.models import Product, Category, History
from django.utils.text import slugify


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')
        read_only_fields = ('id', 'date_created', 'date_updated')
        
        def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.name)
            super(ProductSerializer, self).save(*args, **kwargs)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"