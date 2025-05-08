from django.urls import path
from . import views
urlpatterns = [
    path('', views.profile, name='profile'),
    path('<int:id>', views.get_profile_by_id, name='profile-by-id'),
]