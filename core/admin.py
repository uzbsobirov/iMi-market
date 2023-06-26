from django.contrib import admin
from .models import (
    Category, Stock, Product, History, ProductImage, ProductSeller
)

uneditable_fields = ('id', 'date_created', 'date_updated')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'icon',
        'description',
        'status'
    )

    fields = [
        field.name for field in Category._meta.fields if field.name not in uneditable_fields]
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

    fields = [
        field.name for field in Product._meta.fields if field.name not in uneditable_fields]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'quantity',
        'type'
    )

    fields = [
        field.name for field in Stock._meta.fields if field.name not in uneditable_fields]


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        'stock',
        'quantity',
        'type'
    )

    fields = [
        field.name for field in History._meta.fields if field.name not in uneditable_fields]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'image'
    )

    fields = [
        field.name for field in ProductImage._meta.fields if field.name not in uneditable_fields]


@admin.register(ProductSeller)
class ProductSellerAdmin(admin.ModelAdmin):
    list_display = (
        'seller_name'
    )

    fields = [
        field.name for field in ProductSeller._meta.fields if field.name not in uneditable_fields]
