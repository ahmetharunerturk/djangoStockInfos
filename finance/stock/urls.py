from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_stock_info, name='get_stock_info'),
]
