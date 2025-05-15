from django.urls import path, include

from . import views
from purchaseoffer import views as offer_views

urlpatterns = [
    # http://localhost:8000 (root)
    path('property/', views.property_list, name='property_list'),
    path('', views.home, name='home'),
    path('property/<int:id>/', views.property_by_id, name='property_by_id'),
    path('property/<int:id>/purchaseoffer/',offer_views.make_offer, name="make-offer"),
    path('property/create/', views.create_property, name='create-property'),
    path('property/my', views.my_properties, name='my-properties'),
    path('property/edit/<int:id>/', views.edit_property, name='edit-property'),
]