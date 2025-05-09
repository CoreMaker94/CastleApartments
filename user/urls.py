from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name="user/login.html"), name='login'),
    path('logout', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile', views.profile, name='profile'),
    path('<int:id>', views.get_profile_by_id, name='profile-by-id'),
]