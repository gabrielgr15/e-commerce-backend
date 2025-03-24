from django.urls import path
from .views import UserRegistrationView, LoginView, UserVerificationView, ResendVerificationEmailView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('email-verification/', UserVerificationView.as_view, name='login'),
    path('resend-verification-email', ResendVerificationEmailView.as_view(), name='resend-verification-email'),
]