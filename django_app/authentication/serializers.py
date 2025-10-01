from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'confirm_password')
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        # Use email as username if not provided
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email']

        user = CustomUser.objects.create_user(**validated_data)

        # Create user profile
        UserProfile.objects.get_or_create(user=user)

        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to get user by email
            try:
                user_obj = CustomUser.objects.get(email=email)
                username = user_obj.username
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError('Invalid credentials')

            user = authenticate(request=self.context.get('request'),
                              username=username, password=password)

            if not user:
                raise serializers.ValidationError('Invalid credentials')

            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data"""
    full_name = serializers.ReadOnlyField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                 'full_name', 'avatar', 'is_email_verified', 'created_at', 'profile')
        read_only_fields = ('id', 'created_at', 'is_email_verified')

    def get_profile(self, obj):
        try:
            profile = obj.profile
            return {
                'bio': profile.bio,
                'company': profile.company,
                'job_title': profile.job_title,
                'phone': profile.phone,
                'timezone': profile.timezone,
                'preferences': profile.preferences
            }
        except UserProfile.DoesNotExist:
            return {}


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user',)
