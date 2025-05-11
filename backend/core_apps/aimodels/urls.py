# accounts/urls.py
from django.urls import path
from .views import FeedbackFormView

urlpatterns = [
    path('feedback/', FeedbackFormView.as_view(), name='feedback'),
]