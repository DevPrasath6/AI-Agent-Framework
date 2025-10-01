from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import CustomUser, UserProfile
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserProfileSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Return user data with token
        user_serializer = UserSerializer(user)
        return Response({
            'user': user_serializer.data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(ObtainAuthToken):
    """User login endpoint"""
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Update last login
        user.last_login = timezone.now()
        user.save()

        # Get or create token
        token, created = Token.objects.get_or_create(user=user)

        # Login user for session
        login(request, user)

        # Return user data with token
        user_serializer = UserSerializer(user)
        return Response({
            'user': user_serializer.data,
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout_view(request):
    """User logout endpoint"""
    try:
        # Delete the token
        request.user.auth_token.delete()
    except:
        pass

    # Logout user from session
    logout(request)

    return Response({
        'message': 'Logged out successfully'
    }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """Get and update user profile details"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_me_view(request):
    """Get current user information"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """Change user password"""
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({
            'error': 'Both old_password and new_password are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(old_password):
        return Response({
            'error': 'Old password is incorrect'
        }, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    # Update token
    try:
        user.auth_token.delete()
        Token.objects.create(user=user)
    except:
        pass

    return Response({
        'message': 'Password changed successfully'
    }, status=status.HTTP_200_OK)


# Signal handlers for logging user activity
@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    """Log user login activity"""
    print(f"User {user.email} logged in at {timezone.now()}")


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    """Log user logout activity"""
    if user:
        print(f"User {user.email} logged out at {timezone.now()}")
