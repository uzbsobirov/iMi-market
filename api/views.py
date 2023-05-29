from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework import views
from .serializers import ProductSerializer, CategorySerializer, HistorySerializer
from core.models import Product, Category, History
from rest_framework.response import Response
from rest_framework import status


class ProductsApiView(views.APIView):
    serializer_class = ProductSerializer

    def get(self, request, *args,  **kwargs):
        products = Product.objects.all()
        serializer = self.serializer_class(instance=products, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ProductApiView(views.APIView):
    serializer_class = ProductSerializer

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(instance=product)
        return Response(data=serializer.data)

    def put(self, request, pk, *args, **kwargs):
        data = request.data
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(instance=product, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def patch(self, request, pk, *args, **kwargs):
        data = request.data
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(instance=product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(data={'Deleted': 'Product was succesfully deleted'}, status=status.HTTP_204_NO_CONTENT)