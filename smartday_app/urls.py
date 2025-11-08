# smartday_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task, name='task'),
     path('api/get_categories/', views.get_categories, name='get_categories'),
    path('api/add_category/', views.add_category, name='add_category'),
    path('api/add_item/', views.add_item, name='add_item'),
    path('api/toggle_item/', views.toggle_item, name='toggle_item'),
    path('api/delete_item/', views.delete_item, name='delete_item'),
    path('api/get_items/<int:category_id>/', views.get_items, name='get_items'),
]
