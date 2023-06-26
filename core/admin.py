from django.contrib import admin
from .models import (
    Category, Stock, Product, History, ProductImages
)

uneditable_fields = ('id', 'date_created', 'date_updated')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'description',
        'status'
    )

    fields = [field.name for field in Category._meta.fields if field.name not in uneditable_fields]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'name',
        'image',
        'slug',
        'description',
        'price',
        'status'
    )

    fields = [field.name for field in Product._meta.fields if field.name not in uneditable_fields]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'quantity',
        'type'
    )

    fields = [field.name for field in Stock._meta.fields if field.name not in uneditable_fields]


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        'stock',
        'quantity',
        'type'
    )

    fields = [field.name for field in History._meta.fields if field.name not in uneditable_fields]


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = (
        'image_pk',
        'image_1',
        'image_2',
        'image_3'
    )

    fields = [field.name for field in History._meta.fields if field.name not in uneditable_fields]
