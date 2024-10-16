from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

# Define a serializer for user registration
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
    
    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])
        user = User(**validated_data)
        user.save()
        return user

# Signup view
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_token_valid(request):
    # Get token from the Authorization header
    token = (request.headers.get('Authorization'))

    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]  # Extract the token from the 'Bearer ' part

        try:
            # Validate the token
            token_backend = TokenBackend(algorithm='HS256', signing_key=settings.SECRET_KEY)
            valid_data = token_backend.decode(token, verify=True)

            # If no error, token is valid
            return Response({'detail': 'Token is valid'}, status=200)
        except TokenError:
            # Token is invalid or expired
            return Response({'detail': 'Token is invalid or expired'}, status=401)
        except Exception as e:
            # Handle unexpected exceptions
            return Response({'detail': str(e)}, status=400)
    else:
        return Response({'detail': 'No token provided'}, status=400)
    
# Login view
class CustomTokenObtainPairView(TokenObtainPairView):
    # can add custom logic (currently inherits default from TokenObtainPairView class)
    # can modify the response data or add additional validation if needed
    pass
