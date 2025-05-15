# accounts/urls.py
from django.urls import path
from .views import RegisterView, LoginView, WebsiteCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('websites/', WebsiteCreateView.as_view(), name='create-website'),
]