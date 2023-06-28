from django.urls import path
from .views import (
    ProductsApiView, ProductApiView, CategoriesApiView, CategoryApiView, HistoriesApiView, HistoryApiView
)


urlpatterns = [
    path('products/', ProductsApiView.as_view()),
    path('product/<int:pk>/', ProductApiView.as_view()),

    path('categories/', CategoriesApiView.as_view()),
    path('category/<int:pk>/', CategoryApiView.as_view()),

    path('histories/', HistoriesApiView.as_view()),
    path('history/<int:pk>/', HistoryApiView.as_view())
]