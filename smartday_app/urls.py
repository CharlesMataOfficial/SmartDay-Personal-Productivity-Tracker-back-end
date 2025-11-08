# smartday_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task, name='task'),
    path('get_categories/', views.get_categories, name='get_categories'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_item/', views.add_item, name='add_item'),
    path('toggle_item/', views.toggle_item, name='toggle_item'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('get_items/<int:category_id>/', views.get_items, name='get_items'),
]
