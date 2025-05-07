from django.urls import path
from . import views
urlpatterns = [
    path("",views.offer_list, name='offer_list'),
    #path for finalized
]