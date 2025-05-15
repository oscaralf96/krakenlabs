# accounts/urls.py
from django.urls import path
from .views import RegisterView, LoginView, WebsiteCreateView, test_login_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', test_login_view, name='login'),
    path('websites/', WebsiteCreateView.as_view(), name='create-website'),
]