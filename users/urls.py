from django.urls import path
from .views import RegistrationAPIView, ConfirmAPIView, AuthorizationAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='api_register'),
    path('confirm/', ConfirmAPIView.as_view(), name='api_confirm'),
    path('login/', AuthorizationAPIView.as_view(), name='api_login'),
]