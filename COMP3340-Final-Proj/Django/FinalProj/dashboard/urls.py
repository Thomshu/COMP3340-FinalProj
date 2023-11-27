from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
]
