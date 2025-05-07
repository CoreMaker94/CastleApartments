from django.urls import path

from . import views

urlpatterns = [
    # http://localhost:8000 (root)
    path('property', views.property_list, name='property_list'),
    path('', views.home, name='home'),
    path('<int:id>', views.property_by_id, name='property_by_id'),
]