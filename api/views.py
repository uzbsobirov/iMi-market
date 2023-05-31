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


class CategoriesApiView(views.APIView):
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = self.serializer_class(instance=categories, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        categories = Category.objects.all()
        seri = self.serializer_class(instance=categories, many=True)
        return Response(data=seri.data, status=status.HTTP_201_CREATED)


class CategoryApiView(views.APIView):
    serializer_class = CategorySerializer

    def get(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(instance=category)
        return Response(data=serializer.data)

    def put(self, request, pk, *args, **kwargs):
        data = request.data
        category = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(instance=category, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def patch(self, request, pk, *args, **kwargs):
        data = request.data
        category = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(instance=category, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(data={'Deleted': 'Category was succesfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class HistoriesApiView(views.APIView):
    serializer_class = HistorySerializer

    def get(self, request, *args, **kwargs):
        histories = History.objects.all()
        serializer = self.serializer_class(instance=histories, many=True)
        return Response(data=serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        histories = History.objects.all()
        seria = self.serializer_class(instance=histories, many=True)
        return Response(data=seria.data, status=status.HTTP_201_CREATED)


class HistoryApiView(views.APIView):
    serializer_class = HistorySerializer

    def get(self, request, pk, *args, **kwargs):
        history = get_object_or_404(History, pk=pk)
        serializer = self.serializer_class(instance=history)
        return Response(data=serializer.data)

    def put(self, request, pk, *args, **kwargs):
        data = request.data
        history = get_object_or_404(History, pk=pk)
        serializer = self.serializer_class(instance=history, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def patch(self, request, pk, *args, **kwargs):
        data = request.data
        history = get_object_or_404(History, pk=pk)
        serializer = self.serializer_class(instance=history, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        history = get_object_or_404(History, pk=pk)
        history.delete()
        return Response(data={'Deleted': 'History was succesfully deleted'}, status=status.HTTP_204_NO_CONTENT)