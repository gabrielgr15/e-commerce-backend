from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .utils import generateToken, sendVerificationEmail
from .models import UserVerificationModel, CustomUser
from .serializers import UserRegistrationSerializer
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        verification_token = generateToken()
        user_verificiation = UserVerificationModel(user=user, token=token)
        user_verificiation.save()
        sendVerificationEmail(user, verification_token, request)
        token = RefreshToken.for_user(user=user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        return Response({'refresh_token': refresh_token, 'access_token': access_token,
                         'message': 'Registration succesful! We have sent a verification email to your address'},
                        status=status.HTTP_201_CREATED)
    

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_verified:
            return Response({'error': 'Your email address is not verified. Please check your inbox for the verification link'},
                            status=status.HTTP_403_FORBIDDEN)
        token = RefreshToken.for_user(user=user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        return Response({'refresh_token': refresh_token, 'access_token': access_token},
                        status=status.HTTP_200_OK)


class UserVerificationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        url_token = request.query_params.get('token')
        if url_token is None:
            return Response({'error': 'Verification token was not provided in the URL'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user_verification = UserVerificationModel.objects.get(token=url_token)
            created = user_verification.created
            now = timezone.now
            expiration_time = timedelta(hours=24)
            if now - created > expiration_time:
                return Response({'message': 'The token has expired, please request a new verification email'},
                                status=status.HTTP_400_BAD_REQUEST)
            user = user_verification.user
            user.is_verified = True
            user.save()
            user_verification.delete()
            return Response({'message': 'User succesfully verified'},
                            status=status.HTTP_200_OK)
        except UserVerificationModel.DoesNotExist:
            return Response({'error': 'Invalid or expired token'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ResendVerificationEmailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email address is required'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_verified:
                return Response({'error': 'User already verified'},
                                status=status.HTTP_200_OK)
            
            cache_key = f'resend_limit_{email}'
            limit = 3
            timeout_seconds = 60 * 60
            resend_count = cache.get(cache_key)

            if resend_count is not None and resend_count >= limit:
                return Response({'error': 'Too many resend attempts. Please wait before trying again'},
                                status=status.HTTP_429_TOO_MANY_REQUESTS)
            token = generateToken()
            try:
                user_verification = UserVerificationModel.objects.get(user=user)
                user_verification.token = token
                user_verification.save()
            except UserVerificationModel.DoesNotExist:
                UserVerificationModel.objects.create(token=token, user=user)
            
            sendVerificationEmail(user, token, request)
            new_resend_count = (resend_count or 0) + 1
            cache.set(cache_key,new_resend_count,timeout_seconds)
            return Response({'message': 'A new verification email has been sent to your address'},
                            status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'No user found with this email address'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'An error occurred: {e}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)