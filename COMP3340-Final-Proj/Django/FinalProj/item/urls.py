# Clean and more organized way by making another urls.py in this '.item' folder

from django.urls import path
from . import views

app_name = 'item' 

urlpatterns = [
    path('', views.browse, name='browse'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'), #for delete items path
    path('<int:pk>/edit/', views.edit, name='edit'), #for Edit items path
    path('export-csv/', views.export_items_to_csv, name='export_items_to_csv'),
]