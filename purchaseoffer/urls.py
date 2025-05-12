from django.urls import path
from . import views
urlpatterns = [
    path("", views.get_offers, name='get-offers')
]