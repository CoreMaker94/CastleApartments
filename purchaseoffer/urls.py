from django.urls import path
from . import views
urlpatterns = [
    path("", views.get_offers, name='get-offers'),
    path("<int:id>/status/", views.change_status_seller, name="change_status_seller"),
    path("<int:id>/finalize/", views.finalize_offer, name="finalize_offer")
]