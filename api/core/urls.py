from django.urls import path
from .views import ProductsApiView, ProductApiView


urlpatterns = [
    path('products/', ProductsApiView.as_view()),
    path('product/<int:pk>/', ProductApiView.as_view())

    # path('categories/', CategorySerializer.as_view()),
    #
    # path('histories/', HistorySerializer.as_view())
]